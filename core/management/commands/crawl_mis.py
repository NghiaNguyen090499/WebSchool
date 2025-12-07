"""
Django management command to crawl data from misvn.edu.vn
Usage: python manage.py crawl_mis [--news] [--events] [--about] [--all]
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.core.files.base import ContentFile
import tempfile
import os
from news.models import News, Category
from events.models import Event
from about.models import AboutPage
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from datetime import datetime
import time


class Command(BaseCommand):
    help = 'Crawl data from misvn.edu.vn and sync to database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--news',
            action='store_true',
            help='Crawl news articles',
        )
        parser.add_argument(
            '--events',
            action='store_true',
            help='Crawl events',
        )
        parser.add_argument(
            '--about',
            action='store_true',
            help='Crawl about pages',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Crawl all content types',
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=50,
            help='Limit number of items to crawl per type (default: 50)',
        )

    def handle(self, *args, **options):
        base_url = 'https://misvn.edu.vn'
        
        if options['all']:
            options['news'] = True
            options['events'] = True
            options['about'] = True

        # Discover actual URLs from homepage first
        self.stdout.write(self.style.SUCCESS('Discovering URLs from homepage...'))
        discovered_urls = self.discover_urls(base_url)

        limit = options.get('limit', 50)

        if options['news']:
            self.stdout.write(self.style.SUCCESS('Starting news crawl...'))
            self.crawl_news(base_url, discovered_urls, limit)
            
        if options['events']:
            self.stdout.write(self.style.SUCCESS('Starting events crawl...'))
            self.crawl_events(base_url, discovered_urls, limit)
            
        if options['about']:
            self.stdout.write(self.style.SUCCESS('Starting about pages crawl...'))
            self.crawl_about(base_url, discovered_urls)
    
    def discover_urls(self, base_url):
        """Discover actual URLs from homepage navigation"""
        discovered = {
            'news': [],
            'events': [],
            'about': [],
        }
        
        homepage = self.get_page(base_url)
        if not homepage:
            return discovered
        
        # Find all links
        all_links = homepage.find_all('a', href=True)
        
        for link in all_links:
            href = link.get('href', '')
            if not href:
                continue
            
            full_url = urljoin(base_url, href)
            href_lower = href.lower()
            
            # Categorize links
            if 'tin-tuc' in href_lower or 'news' in href_lower:
                if 'su-kien' in href_lower or 'event' in href_lower:
                    if full_url not in discovered['events']:
                        discovered['events'].append(full_url)
                else:
                    if full_url not in discovered['news']:
                        discovered['news'].append(full_url)
            elif 'su-kien' in href_lower or 'event' in href_lower:
                if full_url not in discovered['events']:
                    discovered['events'].append(full_url)
            elif 'gioi-thieu' in href_lower or 'about' in href_lower:
                if full_url not in discovered['about']:
                    discovered['about'].append(full_url)
        
        self.stdout.write(f'  Discovered {len(discovered["news"])} news URLs, {len(discovered["events"])} event URLs, {len(discovered["about"])} about URLs')
        return discovered

    def get_page(self, url, retries=3):
        """Fetch a page with retries"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        for attempt in range(retries):
            try:
                response = requests.get(url, headers=headers, timeout=30)
                response.raise_for_status()
                response.encoding = 'utf-8'
                return BeautifulSoup(response.text, 'html.parser')
            except Exception as e:
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                self.stdout.write(self.style.ERROR(f'Error fetching {url}: {str(e)}'))
                return None
        return None

    def download_image(self, image_url, base_url):
        """Download image from URL"""
        try:
            if not image_url:
                return None
                
            # Make absolute URL
            if image_url.startswith('//'):
                image_url = 'https:' + image_url
            elif image_url.startswith('/'):
                image_url = urljoin(base_url, image_url)
            elif not image_url.startswith('http'):
                image_url = urljoin(base_url, image_url)
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(image_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Check if it's actually an image
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                return None
            
            # Create ContentFile directly from response content
            return ContentFile(response.content)
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Could not download image {image_url}: {str(e)}'))
            return None

    def clean_text(self, text):
        """Clean and normalize text"""
        if not text:
            return ''
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def extract_date(self, text):
        """Extract date from Vietnamese text"""
        # Try to find date patterns in Vietnamese
        # Format: "Thứ Năm, Tháng 12 4, 2025" or "04/12/2025"
        date_patterns = [
            r'(\d{1,2})/(\d{1,2})/(\d{4})',
            r'Tháng\s+(\d{1,2})\s+(\d{1,2}),\s+(\d{4})',
            r'(\d{4})-(\d{1,2})-(\d{1,2})',
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    if '/' in pattern:
                        day, month, year = match.groups()
                    elif 'Tháng' in pattern:
                        month, day, year = match.groups()
                    else:
                        year, month, day = match.groups()
                    return datetime(int(year), int(month), int(day)).date()
                except:
                    continue
        return None

    def crawl_news(self, base_url, discovered_urls=None, limit=50):
        """Crawl news articles"""
        if discovered_urls is None:
            discovered_urls = {'news': []}
        
        # Use discovered URLs or fallback to defaults
        news_urls = discovered_urls.get('news', [])
        if not news_urls:
            news_urls = [
                urljoin(base_url, '/tin-tuc/'),
                urljoin(base_url, '/tin-tuc'),
                base_url,
            ]
        
        soup = None
        for news_url in news_urls:
            soup = self.get_page(news_url)
            if soup:
                self.stdout.write(f'  ✓ Using news URL: {news_url}')
                break
        
        if not soup:
            self.stdout.write(self.style.ERROR('Could not fetch any news page'))
            return

        # Get or create categories
        categories_map = {
            'Thông báo': 'announcements',
            'Tin tức – Sự kiện': 'news-events',
            'Tin nhà trường': 'school-news',
            'Tin giáo dục': 'education-news',
            'Văn bản': 'documents',
        }
        
        for cat_name, cat_slug in categories_map.items():
            Category.objects.get_or_create(
                slug=cat_slug,
                defaults={'name': cat_name}
            )

        # Find all article links from the category page
        # Strategy: Find links that look like actual articles, not category pages
        all_links = soup.find_all('a', href=True)
        article_links = set()
        
        for link in all_links:
            href = link.get('href', '')
            if not href:
                continue
            
            # Skip category pages, navigation, and non-article links
            href_lower = href.lower()
            
            # Skip social media, external links, and non-article patterns
            skip_patterns = [
                '/category/', '/tag/', '/author/', '/page/', 
                '#', 'javascript:', 'mailto:', 'tel:',
                'facebook.com', 'twitter.com', 'instagram.com',
                'linkedin.com', 'youtube.com', 'zalo.me',
                'sharer.php', 'share.php', 'feed',
                '/wp-admin/', '/wp-content/', '/wp-includes/',
                '/search', '/?', 'mailto:', 'tel:'
            ]
            
            if any(skip in href_lower for skip in skip_patterns):
                continue
            
            # Only process links from the same domain
            if href.startswith('http') and 'misvn.edu.vn' not in href_lower:
                continue
            
            # Look for article-like patterns
            # WordPress pattern: /2025/01/article-slug/ or /tin-tuc/article-slug/ or single article slug
            article_patterns = [
                r'/\d{4}/\d{2}/[^/]+/$',  # /2025/01/article-slug/
                r'/tin-tuc/[^/]+/$',       # /tin-tuc/article-slug/
                r'/su-kien/[^/]+/$',       # /su-kien/event-slug/
                r'/phong-trao/[^/]+/$',    # /phong-trao/article-slug/
            ]
            
            is_article = False
            for pattern in article_patterns:
                if re.search(pattern, href):
                    is_article = True
                    break
            
            if is_article:
                full_url = urljoin(base_url, href)
                # Make sure it's not a category page and is from misvn.edu.vn
                if '/category/' not in full_url.lower() and 'misvn.edu.vn' in full_url.lower() and full_url not in article_links:
                    article_links.add(full_url)
        
        # Also try finding article containers
        article_containers = soup.find_all(['article', 'div'], class_=re.compile(r'post|entry|article|news-item', re.I))
        for container in article_containers:
            link_elem = container.find('a', href=True)
            if link_elem:
                href = link_elem.get('href', '')
                if href and '/category/' not in href.lower():
                    full_url = urljoin(base_url, href)
                    article_links.add(full_url)
        
        if not article_links:
            self.stdout.write(self.style.WARNING('No article links found. Trying alternative method...'))
            # Fallback: get all links and filter
            for link in all_links:
                href = link.get('href', '')
                if href and href.startswith('http') and 'misvn.edu.vn' in href:
                    if '/category/' not in href.lower() and '/tag/' not in href.lower():
                        article_links.add(href)
        
        self.stdout.write(f'  Found {len(article_links)} potential article links')
        
        count = 0
        for article_url in list(article_links)[:limit]:
            try:
                # Check if already exists by URL slug
                url_parts = article_url.rstrip('/').split('/')
                potential_slug = url_parts[-1] if url_parts else None
                
                if potential_slug and News.objects.filter(slug=potential_slug).exists():
                    continue
                
                # Fetch article detail
                article_soup = self.get_page(article_url)
                if not article_soup:
                    continue
                
                # Extract title from article page (not from link text)
                title_text = None
                
                # Try h1 first (most reliable)
                title_elem = article_soup.find('h1', class_=re.compile(r'entry-title|post-title|title', re.I))
                if not title_elem:
                    title_elem = article_soup.find('h1')
                
                if title_elem:
                    title_text = self.clean_text(title_elem.get_text())
                
                # Try meta tags if h1 not found
                if not title_text:
                    meta_title = article_soup.find('meta', property='og:title')
                    if meta_title:
                        title_text = self.clean_text(meta_title.get('content', ''))
                
                # Try page title as last resort
                if not title_text:
                    page_title = article_soup.find('title')
                    if page_title:
                        title_text = self.clean_text(page_title.get_text())
                        # Remove site name if present
                        title_text = title_text.split('|')[0].split('-')[0].strip()
                
                if not title_text or len(title_text) < 5:
                    self.stdout.write(self.style.WARNING(f'  ⚠ Skipping {article_url}: No valid title found (found: {title_text})'))
                    continue
                
                # Check if exists by title slug
                slug = slugify(title_text)
                if News.objects.filter(slug=slug).exists():
                    self.stdout.write(self.style.WARNING(f'  ⚠ Skipping {article_url}: Already exists (slug: {slug})'))
                    continue
                
                # Extract content - try multiple selectors
                content = ''
                content_selectors = [
                    {'tag': 'div', 'class': re.compile(r'entry-content|post-content|article-content', re.I)},
                    {'tag': 'article'},
                    {'tag': 'div', 'class': re.compile(r'content|post-body', re.I)},
                    {'tag': 'main'},
                ]
                
                for selector in content_selectors:
                    content_elem = article_soup.find(selector['tag'], selector.get('class'))
                    if content_elem:
                        # Remove unwanted elements
                        for unwanted in content_elem.find_all(['script', 'style', 'nav', 'footer', 'aside', 'advertisement']):
                            unwanted.decompose()
                        content = self.clean_text(content_elem.get_text())
                        if len(content) > 100:  # Valid content
                            break
                
                if not content or len(content) < 50:
                    content = title_text  # Fallback to title
                
                # Extract image - try featured image first
                thumbnail_file = None
                
                # Try featured image meta tag
                meta_image = article_soup.find('meta', property='og:image')
                if meta_image:
                    img_url = meta_image.get('content', '')
                    if img_url:
                        thumbnail_file = self.download_image(img_url, base_url)
                
                # Try first image in content
                if not thumbnail_file:
                    img_elem = article_soup.find('img', class_=re.compile(r'wp-post-image|featured|thumbnail', re.I))
                    if not img_elem:
                        img_elem = article_soup.find('img')
                    if img_elem:
                        img_url = img_elem.get('src') or img_elem.get('data-src') or img_elem.get('data-lazy-src')
                        if img_url:
                            thumbnail_file = self.download_image(img_url, base_url)
                
                # Extract date
                date_elem = article_soup.find(['time', 'span'], class_=re.compile(r'date|time', re.I))
                created_at = datetime.now()
                if date_elem:
                    date_text = date_elem.get_text()
                    extracted_date = self.extract_date(date_text)
                    if extracted_date:
                        created_at = datetime.combine(extracted_date, datetime.min.time())
                
                # Extract excerpt
                excerpt = content[:300] if len(content) > 300 else content
                
                # Determine category from URL or breadcrumb
                category = None
                article_url_lower = article_url.lower()
                
                # Try to find category from breadcrumb
                breadcrumb = article_soup.find(['nav', 'div'], class_=re.compile(r'breadcrumb', re.I))
                if breadcrumb:
                    breadcrumb_text = breadcrumb.get_text().lower()
                    if 'thông báo' in breadcrumb_text or 'thong-bao' in breadcrumb_text:
                        category = Category.objects.filter(slug='announcements').first()
                    elif 'văn bản' in breadcrumb_text or 'van-ban' in breadcrumb_text:
                        category = Category.objects.filter(slug='documents').first()
                    elif 'tin nhà trường' in breadcrumb_text or 'tin-nha-truong' in breadcrumb_text:
                        category = Category.objects.filter(slug='school-news').first()
                    elif 'tin giáo dục' in breadcrumb_text or 'tin-giao-duc' in breadcrumb_text:
                        category = Category.objects.filter(slug='education-news').first()
                
                # Fallback to URL pattern
                if not category:
                    if '/thong-bao/' in article_url_lower or '/thông-báo/' in article_url_lower:
                        category = Category.objects.filter(slug='announcements').first()
                    elif '/van-ban/' in article_url_lower or '/văn-bản/' in article_url_lower:
                        category = Category.objects.filter(slug='documents').first()
                    elif '/tin-nha-truong/' in article_url_lower:
                        category = Category.objects.filter(slug='school-news').first()
                    elif '/tin-giao-duc/' in article_url_lower:
                        category = Category.objects.filter(slug='education-news').first()
                
                # Create news article
                news = News(
                    title=title_text[:200],
                    content=content,
                    excerpt=excerpt[:300],
                    category=category,
                    is_featured=False,
                )
                news.created_at = created_at
                
                if thumbnail_file:
                    news.thumbnail.save(
                        f"{slug}.jpg",
                        thumbnail_file,
                        save=False
                    )
                
                news.save()
                count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ [{count}] {title_text[:60]}...'))
                time.sleep(1)  # Be respectful
                
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Error processing news item: {str(e)}'))
                continue
        
        self.stdout.write(self.style.SUCCESS(f'Successfully crawled {count} news articles'))

    def crawl_events(self, base_url, discovered_urls=None, limit=30):
        """Crawl events"""
        if discovered_urls is None:
            discovered_urls = {'events': []}
        
        # Use discovered URLs or fallback to defaults
        event_urls = discovered_urls.get('events', [])
        if not event_urls:
            event_urls = [
                urljoin(base_url, '/tin-tuc/tin-tuc-su-kien/'),
                urljoin(base_url, '/tin-tuc/tin-tuc-su-kien'),
                urljoin(base_url, '/su-kien/'),
                base_url,
            ]
        
        soup = None
        for event_url in event_urls:
            soup = self.get_page(event_url)
            if soup:
                self.stdout.write(f'  ✓ Using event URL: {event_url}')
                break
        
        if not soup:
            self.stdout.write(self.style.ERROR('Could not fetch events page'))
            return

        # Find all event article links
        all_links = soup.find_all('a', href=True)
        event_links = set()
        
        for link in all_links:
            href = link.get('href', '')
            if not href:
                continue
            
            href_lower = href.lower()
            
            # Skip social media, external links, and non-event patterns
            skip_patterns = [
                '/category/', '/tag/', '/author/', '/page/', 
                '#', 'javascript:', 'mailto:', 'tel:',
                'facebook.com', 'twitter.com', 'instagram.com',
                'linkedin.com', 'youtube.com', 'zalo.me',
                'sharer.php', 'share.php', 'feed',
                '/wp-admin/', '/wp-content/', '/wp-includes/',
                '/search', '/?'
            ]
            
            if any(skip in href_lower for skip in skip_patterns):
                continue
            
            # Only process links from the same domain
            if href.startswith('http') and 'misvn.edu.vn' not in href_lower:
                continue
            
            # Look for event-like patterns
            event_patterns = [
                r'/su-kien/[^/]+/$',
                r'/event/[^/]+/$',
                r'/tin-tuc-su-kien/[^/]+/$',
                r'/phong-trao/[^/]+/$',
            ]
            
            is_event = False
            for pattern in event_patterns:
                if re.search(pattern, href):
                    is_event = True
                    break
            
            if is_event:
                full_url = urljoin(base_url, href)
                if '/category/' not in full_url.lower() and 'misvn.edu.vn' in full_url.lower() and full_url not in event_links:
                    event_links.add(full_url)
        
        # Also try finding event containers
        event_containers = soup.find_all(['article', 'div'], class_=re.compile(r'event|post|entry|su-kien', re.I))
        for container in event_containers:
            link_elem = container.find('a', href=True)
            if link_elem:
                href = link_elem.get('href', '')
                if href and '/category/' not in href.lower():
                    full_url = urljoin(base_url, href)
                    event_links.add(full_url)
        
        if not event_links:
            self.stdout.write(self.style.WARNING('No event links found. Trying alternative method...'))
            for link in all_links:
                href = link.get('href', '')
                if href and 'su-kien' in href.lower() or 'event' in href.lower():
                    full_url = urljoin(base_url, href)
                    if '/category/' not in full_url.lower():
                        event_links.add(full_url)
        
        self.stdout.write(f'  Found {len(event_links)} potential event links')
        
        count = 0
        for event_url in list(event_links)[:limit]:
            try:
                # Check if already exists
                url_parts = event_url.rstrip('/').split('/')
                potential_slug = url_parts[-1] if url_parts else None
                
                if potential_slug and Event.objects.filter(slug=potential_slug).exists():
                    continue
                
                # Fetch event detail
                event_soup = self.get_page(event_url)
                if not event_soup:
                    continue
                
                # Extract title from event page
                title_text = None
                title_elem = event_soup.find('h1', class_=re.compile(r'entry-title|post-title|title', re.I))
                if not title_elem:
                    title_elem = event_soup.find('h1')
                
                if title_elem:
                    title_text = self.clean_text(title_elem.get_text())
                
                if not title_text:
                    meta_title = event_soup.find('meta', property='og:title')
                    if meta_title:
                        title_text = self.clean_text(meta_title.get('content', ''))
                
                if not title_text:
                    page_title = event_soup.find('title')
                    if page_title:
                        title_text = self.clean_text(page_title.get_text())
                        title_text = title_text.split('|')[0].split('-')[0].strip()
                
                if not title_text or len(title_text) < 5:
                    self.stdout.write(self.style.WARNING(f'  ⚠ Skipping {event_url}: No valid title found'))
                    continue
                
                slug = slugify(title_text)
                if Event.objects.filter(slug=slug).exists():
                    continue
                
                # Extract content
                description = ''
                content_selectors = [
                    {'tag': 'div', 'class': re.compile(r'entry-content|post-content|event-content', re.I)},
                    {'tag': 'article'},
                    {'tag': 'div', 'class': re.compile(r'content|post-body', re.I)},
                ]
                
                for selector in content_selectors:
                    content_elem = event_soup.find(selector['tag'], selector.get('class'))
                    if content_elem:
                        for unwanted in content_elem.find_all(['script', 'style', 'nav', 'footer']):
                            unwanted.decompose()
                        description = self.clean_text(content_elem.get_text())
                        if len(description) > 50:
                            break
                
                if not description:
                    description = title_text
                
                # Extract date
                date_elem = event_soup.find(['time', 'span'], class_=re.compile(r'date|time', re.I))
                event_date = datetime.now().date()
                if date_elem:
                    date_text = date_elem.get_text()
                    extracted_date = self.extract_date(date_text)
                    if extracted_date:
                        event_date = extracted_date
                
                # Extract location (default)
                location = "Hệ thống giáo dục MIS, Hà Nội"
                
                # Extract image
                img_elem = event_soup.find('img')
                image_file = None
                if img_elem:
                    img_url = img_elem.get('src') or img_elem.get('data-src')
                    image_file = self.download_image(img_url, base_url)
                
                # Create event
                event = Event(
                    title=title_text[:200],
                    date=event_date,
                    location=location,
                    description=description,
                    is_featured=False,
                )
                
                if image_file:
                    event.image.save(
                        f"{slug}.jpg",
                        image_file,
                        save=False
                    )
                
                event.save()
                count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ [{count}] Event: {title_text[:60]}...'))
                time.sleep(1)
                
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Error processing event: {str(e)}'))
                continue
        
        self.stdout.write(self.style.SUCCESS(f'Successfully crawled {count} events'))

    def crawl_about(self, base_url, discovered_urls=None):
        """Crawl about pages"""
        if discovered_urls is None:
            discovered_urls = {'about': []}
        
        # Map pages with multiple URL options
        pages_to_crawl = {
            'mission': {
                'urls': [
                    '/gioi-thieu/gioi-thieu-chung-ve-mis/',
                    '/gioi-thieu/gioi-thieu-chung-ve-mis',
                    '/gioi-thieu/',
                    '/gioi-thieu',
                    '/',
                ],
                'title': 'Giới thiệu chung về MIS'
            },
            'vision': {
                'urls': [
                    '/gioi-thieu/he-thong-giao-duc-mis-doi-moi-de-dot-pha/',
                    '/gioi-thieu/he-thong-giao-duc-mis-doi-moi-de-dot-pha',
                    '/gioi-thieu/',
                ],
                'title': 'Hệ thống giáo dục MIS – Đổi mới để đột phá'
            },
            'principal': {
                'urls': [
                    '/gioi-thieu/thong-diep-cua-tong-giam-doc-dieu-hanh-mis/',
                    '/gioi-thieu/thong-diep-cua-tong-giam-doc-dieu-hanh-mis',
                    '/gioi-thieu/',
                ],
                'title': 'Thông điệp của Tổng Giám đốc điều hành MIS'
            }
        }
        
        # Add discovered about URLs to the list
        discovered_about = discovered_urls.get('about', [])
        
        for page_type, page_info in pages_to_crawl.items():
            try:
                content_found = False
                
                # Combine discovered URLs with default URLs, discovered first
                urls_to_try = []
                
                # Add discovered URLs first (if they match the page type)
                for disc_url in discovered_about:
                    if disc_url not in urls_to_try:
                        urls_to_try.append(disc_url)
                
                # Add default URLs
                for url_path in page_info['urls']:
                    full_url = urljoin(base_url, url_path)
                    if full_url not in urls_to_try:
                        urls_to_try.append(full_url)
                
                for url_item in urls_to_try:
                    # If it's already a full URL, use it; otherwise join with base_url
                    if url_item.startswith('http'):
                        full_url = url_item
                    else:
                        full_url = urljoin(base_url, url_item)
                    
                    page_soup = self.get_page(full_url)
                    
                    if not page_soup:
                        continue
                    
                    # Extract content
                    content_elem = page_soup.find(['div', 'article', 'main'], class_=re.compile(r'content|post|entry|main', re.I))
                    if not content_elem:
                        content_elem = page_soup.find('main') or page_soup.find('body')
                    
                    content = self.clean_text(content_elem.get_text()) if content_elem else ''
                    
                    if not content:
                        continue
                    
                    # Extract title
                    title_elem = page_soup.find(['h1', 'h2'], class_=re.compile(r'title|heading', re.I))
                    title = page_info['title']
                    if title_elem:
                        title = self.clean_text(title_elem.get_text())
                    
                    # Extract image
                    img_elem = page_soup.find('img')
                    image_file = None
                    if img_elem:
                        img_url = img_elem.get('src') or img_elem.get('data-src')
                        image_file = self.download_image(img_url, base_url)
                    
                    # Update or create about page
                    about_page, created = AboutPage.objects.get_or_create(
                        page_type=page_type,
                        defaults={
                            'title': title[:200],
                            'content': content,
                        }
                    )
                    
                    if not created:
                        about_page.title = title[:200]
                        about_page.content = content
                    
                    if image_file:
                        about_page.image.save(
                            f"{page_type}.jpg",
                            image_file,
                            save=False
                        )
                    
                    about_page.save()
                    content_found = True
                    self.stdout.write(self.style.SUCCESS(f'✓ Crawled {page_type}: {title[:50]}...'))
                    break
                
                if not content_found:
                    self.stdout.write(self.style.WARNING(f'Could not find content for {page_type}'))
                    
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Error processing {page_type}: {str(e)}'))
                continue
        
        self.stdout.write(self.style.SUCCESS('Successfully crawled about pages'))

