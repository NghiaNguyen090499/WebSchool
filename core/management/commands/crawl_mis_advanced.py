"""
Advanced crawler với khả năng xử lý tốt hơn cấu trúc thực tế của misvn.edu.vn
Sử dụng API hoặc sitemap nếu có, hoặc parse HTML tốt hơn
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.core.files.base import ContentFile
from news.models import News, Category
from events.models import Event
from about.models import AboutPage
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from datetime import datetime
import time
import json


class Command(BaseCommand):
    help = 'Advanced crawler for misvn.edu.vn with better parsing'

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
            help='Limit number of items to crawl (default: 50)',
        )

    def handle(self, *args, **options):
        base_url = 'https://misvn.edu.vn'
        
        if options['all']:
            options['news'] = True
            options['events'] = True
            options['about'] = True

        limit = options['limit']

        if options['news']:
            self.stdout.write(self.style.SUCCESS('Starting news crawl...'))
            self.crawl_news(base_url, limit)
            
        if options['events']:
            self.stdout.write(self.style.SUCCESS('Starting events crawl...'))
            self.crawl_events(base_url, limit)
            
        if options['about']:
            self.stdout.write(self.style.SUCCESS('Starting about pages crawl...'))
            self.crawl_about(base_url)

    def get_page(self, url, retries=3):
        """Fetch a page with retries and proper encoding"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        
        for attempt in range(retries):
            try:
                response = requests.get(url, headers=headers, timeout=30, verify=True)
                response.raise_for_status()
                
                # Try to detect encoding
                if response.encoding is None or response.encoding == 'ISO-8859-1':
                    response.encoding = 'utf-8'
                
                return BeautifulSoup(response.text, 'html.parser')
            except requests.exceptions.RequestException as e:
                if attempt < retries - 1:
                    wait_time = 2 ** attempt
                    self.stdout.write(self.style.WARNING(f'Retrying in {wait_time}s...'))
                    time.sleep(wait_time)
                    continue
                self.stdout.write(self.style.ERROR(f'Error fetching {url}: {str(e)}'))
                return None
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Unexpected error: {str(e)}'))
                return None
        return None

    def download_image(self, image_url, base_url):
        """Download image from URL with better error handling"""
        try:
            if not image_url:
                return None
                
            # Normalize URL
            if image_url.startswith('//'):
                image_url = 'https:' + image_url
            elif image_url.startswith('/'):
                image_url = urljoin(base_url, image_url)
            elif not image_url.startswith('http'):
                image_url = urljoin(base_url, image_url)
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': base_url,
            }
            
            response = requests.get(image_url, headers=headers, timeout=30, stream=True)
            response.raise_for_status()
            
            # Check if it's actually an image
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                return None
            
            return ContentFile(response.content)
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Could not download image {image_url}: {str(e)}'))
            return None

    def clean_text(self, text):
        """Clean and normalize Vietnamese text"""
        if not text:
            return ''
        # Remove HTML entities
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove leading/trailing whitespace
        return text.strip()

    def extract_date_vietnamese(self, text):
        """Extract date from Vietnamese text with better patterns"""
        if not text:
            return None
            
        # Vietnamese month names
        months_vi = {
            'tháng một': 1, 'tháng 1': 1, 'tháng giêng': 1,
            'tháng hai': 2, 'tháng 2': 2,
            'tháng ba': 3, 'tháng 3': 3,
            'tháng tư': 4, 'tháng 4': 4,
            'tháng năm': 5, 'tháng 5': 5,
            'tháng sáu': 6, 'tháng 6': 6,
            'tháng bảy': 7, 'tháng 7': 7,
            'tháng tám': 8, 'tháng 8': 8,
            'tháng chín': 9, 'tháng 9': 9,
            'tháng mười': 10, 'tháng 10': 10,
            'tháng mười một': 11, 'tháng 11': 11,
            'tháng mười hai': 12, 'tháng 12': 12,
        }
        
        # Pattern 1: "Thứ Năm, Tháng 12 4, 2025"
        pattern1 = r'Tháng\s+(\d{1,2})\s+(\d{1,2}),\s+(\d{4})'
        match = re.search(pattern1, text, re.IGNORECASE)
        if match:
            try:
                month, day, year = map(int, match.groups())
                return datetime(year, month, day).date()
            except:
                pass
        
        # Pattern 2: "04/12/2025" or "4/12/2025"
        pattern2 = r'(\d{1,2})/(\d{1,2})/(\d{4})'
        match = re.search(pattern2, text)
        if match:
            try:
                day, month, year = map(int, match.groups())
                return datetime(year, month, day).date()
            except:
                pass
        
        # Pattern 3: "2025-12-04"
        pattern3 = r'(\d{4})-(\d{1,2})-(\d{1,2})'
        match = re.search(pattern3, text)
        if match:
            try:
                year, month, day = map(int, match.groups())
                return datetime(year, month, day).date()
            except:
                pass
        
        return None

    def find_all_links(self, soup, base_url, pattern):
        """Find all links matching a pattern"""
        links = set()
        
        # Find all <a> tags
        for a_tag in soup.find_all('a', href=True):
            href = a_tag.get('href', '')
            if not href:
                continue
            
            # Make absolute URL
            full_url = urljoin(base_url, href)
            
            # Check if matches pattern
            if re.search(pattern, full_url, re.IGNORECASE):
                links.add(full_url)
        
        return list(links)

    def crawl_news(self, base_url, limit=50):
        """Crawl news articles with improved parsing"""
        # Try multiple news URLs
        news_urls = [
            urljoin(base_url, '/tin-tuc/'),
            urljoin(base_url, '/tin-tuc/tin-nha-truong/'),
            urljoin(base_url, '/tin-tuc/tin-giao-duc/'),
            urljoin(base_url, '/tin-tuc/thong-bao/'),
        ]
        
        # Get or create categories
        categories = {
            'Thông báo': Category.objects.get_or_create(slug='thong-bao', defaults={'name': 'Thông báo'})[0],
            'Tin nhà trường': Category.objects.get_or_create(slug='tin-nha-truong', defaults={'name': 'Tin nhà trường'})[0],
            'Tin giáo dục': Category.objects.get_or_create(slug='tin-giao-duc', defaults={'name': 'Tin giáo dục'})[0],
            'Tin tức – Sự kiện': Category.objects.get_or_create(slug='tin-tuc-su-kien', defaults={'name': 'Tin tức – Sự kiện'})[0],
        }
        
        all_news_links = set()
        
        # Collect all news links
        for news_url in news_urls:
            soup = self.get_page(news_url)
            if not soup:
                continue
            
            # Find news article links
            links = self.find_all_links(soup, base_url, r'/tin-tuc/')
            all_news_links.update(links)
            
            self.stdout.write(f'Found {len(links)} links from {news_url}')
        
        self.stdout.write(f'Total unique news links: {len(all_news_links)}')
        
        count = 0
        for news_url in list(all_news_links)[:limit]:
            try:
                # Check if already exists
                # Extract potential slug from URL
                url_parts = news_url.strip('/').split('/')
                potential_slug = url_parts[-1] if url_parts else None
                
                if potential_slug and News.objects.filter(slug=potential_slug).exists():
                    continue
                
                # Fetch article
                soup = self.get_page(news_url)
                if not soup:
                    continue
                
                # Extract title
                title = None
                title_elem = soup.find('h1') or soup.find(['h2', 'h3'], class_=re.compile(r'title|heading', re.I))
                if title_elem:
                    title = self.clean_text(title_elem.get_text())
                
                if not title:
                    # Try meta title
                    meta_title = soup.find('meta', property='og:title') or soup.find('title')
                    if meta_title:
                        title = self.clean_text(meta_title.get('content') or meta_title.get_text())
                
                if not title:
                    self.stdout.write(self.style.WARNING(f'No title found for {news_url}'))
                    continue
                
                # Extract content
                content = ''
                content_selectors = [
                    {'tag': 'div', 'class': re.compile(r'content|post-content|entry-content', re.I)},
                    {'tag': 'article'},
                    {'tag': 'div', 'class': re.compile(r'post|entry', re.I)},
                    {'tag': 'main'},
                ]
                
                for selector in content_selectors:
                    content_elem = soup.find(selector['tag'], selector.get('class'))
                    if content_elem:
                        # Remove script and style tags
                        for script in content_elem(['script', 'style', 'nav', 'footer', 'header']):
                            script.decompose()
                        content = self.clean_text(content_elem.get_text())
                        if len(content) > 100:  # Valid content
                            break
                
                if not content or len(content) < 50:
                    content = title  # Fallback
                
                # Extract date
                created_at = datetime.now()
                date_selectors = [
                    {'tag': 'time'},
                    {'tag': 'span', 'class': re.compile(r'date|time|published', re.I)},
                    {'tag': 'div', 'class': re.compile(r'date|time|published', re.I)},
                ]
                
                for selector in date_selectors:
                    date_elem = soup.find(selector['tag'], selector.get('class'))
                    if date_elem:
                        date_text = date_elem.get_text() or date_elem.get('datetime', '')
                        extracted_date = self.extract_date_vietnamese(date_text)
                        if extracted_date:
                            created_at = datetime.combine(extracted_date, datetime.min.time())
                            break
                
                # Extract image
                thumbnail_file = None
                img_selectors = [
                    {'tag': 'img', 'class': re.compile(r'featured|thumbnail|main', re.I)},
                    {'tag': 'meta', 'property': 'og:image'},
                    {'tag': 'img'},
                ]
                
                for selector in img_selectors:
                    img_elem = soup.find(selector['tag'], selector.get('class') or selector.get('property'))
                    if img_elem:
                        img_url = img_elem.get('src') or img_elem.get('content') or img_elem.get('data-src')
                        if img_url:
                            thumbnail_file = self.download_image(img_url, base_url)
                            if thumbnail_file:
                                break
                
                # Determine category from URL
                category = None
                for cat_name, cat_obj in categories.items():
                    if cat_name.lower().replace(' ', '-') in news_url.lower():
                        category = cat_obj
                        break
                
                # Create excerpt
                excerpt = content[:300] if len(content) > 300 else content
                
                # Create news article
                news = News(
                    title=title[:200],
                    content=content,
                    excerpt=excerpt[:300],
                    category=category,
                    is_featured=False,
                )
                news.created_at = created_at
                
                if thumbnail_file:
                    slug = slugify(title)
                    news.thumbnail.save(
                        f"{slug}.jpg",
                        thumbnail_file,
                        save=False
                    )
                
                news.save()
                count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ [{count}] {title[:60]}...'))
                time.sleep(1)
                
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Error processing {news_url}: {str(e)}'))
                continue
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully crawled {count} news articles'))

    def crawl_events(self, base_url, limit=30):
        """Crawl events with improved parsing"""
        events_url = urljoin(base_url, '/tin-tuc/tin-tuc-su-kien/')
        soup = self.get_page(events_url)
        
        if not soup:
            self.stdout.write(self.style.ERROR('Could not fetch events page'))
            return

        # Find event links
        event_links = self.find_all_links(soup, base_url, r'/tin-tuc/.*su-kien|/event')
        
        count = 0
        for event_url in event_links[:limit]:
            try:
                soup = self.get_page(event_url)
                if not soup:
                    continue
                
                # Similar parsing as news
                title_elem = soup.find('h1') or soup.find(['h2', 'h3'], class_=re.compile(r'title', re.I))
                title = self.clean_text(title_elem.get_text()) if title_elem else None
                
                if not title:
                    continue
                
                slug = slugify(title)
                if Event.objects.filter(slug=slug).exists():
                    continue
                
                # Extract content
                content_elem = soup.find('div', class_=re.compile(r'content|post', re.I)) or soup.find('article')
                description = self.clean_text(content_elem.get_text()) if content_elem else title
                
                # Extract date
                event_date = datetime.now().date()
                date_elem = soup.find('time') or soup.find('span', class_=re.compile(r'date', re.I))
                if date_elem:
                    date_text = date_elem.get_text() or date_elem.get('datetime', '')
                    extracted_date = self.extract_date_vietnamese(date_text)
                    if extracted_date:
                        event_date = extracted_date
                
                location = "Hệ thống giáo dục MIS, 37 Hoàng Quán Chi, Dịch Vọng, Cầu Giấy, Hà Nội"
                
                # Extract image
                img_elem = soup.find('img')
                image_file = None
                if img_elem:
                    img_url = img_elem.get('src') or img_elem.get('data-src')
                    image_file = self.download_image(img_url, base_url)
                
                event = Event(
                    title=title[:200],
                    date=event_date,
                    location=location,
                    description=description,
                    is_featured=False,
                )
                
                if image_file:
                    event.image.save(f"{slug}.jpg", image_file, save=False)
                
                event.save()
                count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ [{count}] {title[:50]}...'))
                time.sleep(1)
                
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Error: {str(e)}'))
                continue
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully crawled {count} events'))

    def crawl_about(self, base_url):
        """Crawl about pages"""
        pages_config = {
            'mission': {
                'urls': [
                    '/gioi-thieu/gioi-thieu-chung-ve-mis/',
                    '/gioi-thieu/',
                ],
                'title': 'Giới thiệu chung về MIS'
            },
            'vision': {
                'urls': [
                    '/gioi-thieu/he-thong-giao-duc-mis-doi-moi-de-dot-pha/',
                ],
                'title': 'Hệ thống giáo dục MIS – Đổi mới để đột phá'
            },
            'principal': {
                'urls': [
                    '/gioi-thieu/thong-diep-cua-tong-giam-doc-dieu-hanh-mis/',
                ],
                'title': 'Thông điệp của Tổng Giám đốc điều hành MIS'
            }
        }
        
        for page_type, config in pages_config.items():
            content_found = False
            
            for url_path in config['urls']:
                full_url = urljoin(base_url, url_path)
                soup = self.get_page(full_url)
                
                if not soup:
                    continue
                
                # Extract title
                title_elem = soup.find('h1') or soup.find(['h2', 'h3'], class_=re.compile(r'title', re.I))
                title = config['title']
                if title_elem:
                    title = self.clean_text(title_elem.get_text())
                
                # Extract content
                content_elem = soup.find('div', class_=re.compile(r'content|post|entry', re.I)) or soup.find('main')
                content = self.clean_text(content_elem.get_text()) if content_elem else ''
                
                if not content or len(content) < 100:
                    continue
                
                # Extract image
                img_elem = soup.find('img')
                image_file = None
                if img_elem:
                    img_url = img_elem.get('src') or img_elem.get('data-src')
                    image_file = self.download_image(img_url, base_url)
                
                about_page, created = AboutPage.objects.update_or_create(
                    page_type=page_type,
                    defaults={
                        'title': title[:200],
                        'content': content,
                    }
                )
                
                if image_file:
                    about_page.image.save(f"{page_type}.jpg", image_file, save=False)
                
                about_page.save()
                content_found = True
                self.stdout.write(self.style.SUCCESS(f'✓ Crawled {page_type}: {title[:50]}...'))
                break
            
            if not content_found:
                self.stdout.write(self.style.WARNING(f'⚠ Could not find content for {page_type}'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Successfully crawled about pages'))



