"""
Django management command to crawl ALL images from misvn.edu.vn
Usage: python manage.py crawl_images [--gallery] [--all] [--limit N]

This command will:
1. Crawl all images from the website
2. Organize them into Albums in the Gallery app
3. Download and save images to media folder
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.core.files.base import ContentFile
from gallery.models import Album, Photo
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from datetime import datetime
import time
import os
import hashlib


class Command(BaseCommand):
    help = 'Crawl all images from misvn.edu.vn and import to Gallery'

    def add_arguments(self, parser):
        parser.add_argument(
            '--gallery',
            action='store_true',
            help='Crawl images and create gallery albums',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Crawl images from all pages',
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=100,
            help='Limit number of images per album (default: 100)',
        )
        parser.add_argument(
            '--pages',
            type=int,
            default=5,
            help='Number of pages to crawl per section (default: 5)',
        )

    def handle(self, *args, **options):
        base_url = 'https://misvn.edu.vn'
        
        if options['all'] or options['gallery']:
            self.stdout.write(self.style.SUCCESS('[IMG] Starting image crawl from misvn.edu.vn...'))
            self.crawl_all_images(base_url, options['limit'], options['pages'])
        else:
            self.stdout.write(self.style.WARNING('Please specify --gallery or --all flag'))
            self.stdout.write('Usage: python manage.py crawl_images --gallery')

    def get_page(self, url, retries=3):
        """Fetch a page with retries"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
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
        """Download image from URL and return ContentFile with filename"""
        try:
            if not image_url:
                return None, None
            
            # Skip tiny/placeholder images
            skip_patterns = [
                'data:image', 'placeholder', 'loading', 'blank',
                '1x1', 'pixel', 'transparent', 'spacer',
                '.gif',  # Usually tracking pixels
            ]
            
            for pattern in skip_patterns:
                if pattern in image_url.lower():
                    return None, None
            
            # Make absolute URL
            if image_url.startswith('//'):
                image_url = 'https:' + image_url
            elif image_url.startswith('/'):
                image_url = urljoin(base_url, image_url)
            elif not image_url.startswith('http'):
                image_url = urljoin(base_url, image_url)
            
            # Skip external images (not from misvn.edu.vn)
            parsed = urlparse(image_url)
            if parsed.netloc and 'misvn.edu.vn' not in parsed.netloc:
                # Allow some common CDN domains
                allowed_domains = ['wp.com', 'wordpress.com', 'cloudflare', 'cdn']
                if not any(domain in parsed.netloc for domain in allowed_domains):
                    return None, None
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': base_url,
            }
            
            response = requests.get(image_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Check if it's actually an image
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                return None, None
            
            # Check minimum size (skip tiny images)
            content_length = len(response.content)
            if content_length < 5000:  # Skip images smaller than 5KB
                return None, None
            
            # Generate filename from URL
            url_path = urlparse(image_url).path
            original_filename = os.path.basename(url_path)
            
            # Clean filename
            if not original_filename or '.' not in original_filename:
                # Generate filename from hash
                hash_str = hashlib.md5(image_url.encode()).hexdigest()[:10]
                ext = 'jpg'  # Default extension
                if 'png' in content_type:
                    ext = 'png'
                elif 'webp' in content_type:
                    ext = 'webp'
                original_filename = f'image_{hash_str}.{ext}'
            
            return ContentFile(response.content), original_filename
            
        except Exception as e:
            return None, None

    def get_image_hash(self, content):
        """Generate hash of image content to detect duplicates"""
        return hashlib.md5(content).hexdigest()

    def crawl_all_images(self, base_url, limit=100, max_pages=5):
        """Crawl images from multiple sections of the website"""
        
        # Define sections to crawl with their album names
        sections = [
            {
                'name': 'Homepage',
                'slug': 'trang-chu',
                'urls': [base_url],
            },
            {
                'name': 'News Events',
                'slug': 'tin-tuc-su-kien',
                'urls': [
                    f'{base_url}/tin-tuc/',
                    f'{base_url}/tin-tuc/tin-tuc-su-kien/',
                ],
            },
            {
                'name': 'Curriculum',
                'slug': 'chuong-trinh-hoc',
                'urls': [
                    f'{base_url}/chuong-trinh-hoc/',
                    f'{base_url}/chuong-trinh-hoc/mam-non-tieu-hoc/',
                    f'{base_url}/chuong-trinh-hoc/thcs/',
                    f'{base_url}/chuong-trinh-hoc/thpt/',
                ],
            },
            {
                'name': 'Photo Gallery',
                'slug': 'thu-vien-anh',
                'urls': [
                    f'{base_url}/thu-vien/',
                    f'{base_url}/thu-vien-anh/',
                    f'{base_url}/gallery/',
                ],
            },
            {
                'name': 'Student Activities',
                'slug': 'hoat-dong-hoc-sinh',
                'urls': [
                    f'{base_url}/hoat-dong/',
                    f'{base_url}/ngoai-khoa/',
                    f'{base_url}/tin-tuc/hoat-dong-hoc-sinh/',
                ],
            },
            {
                'name': 'About MIS',
                'slug': 'gioi-thieu-mis',
                'urls': [
                    f'{base_url}/gioi-thieu/',
                    f'{base_url}/gioi-thieu/gioi-thieu-chung-ve-mis/',
                ],
            },
        ]
        
        total_images = 0
        seen_hashes = set()  # Track downloaded image hashes to avoid duplicates
        
        for section in sections:
            self.stdout.write(self.style.SUCCESS(f'\n=== Processing section: {section["name"]} ===' ))
            
            # Get or create album for this section
            album, created = Album.objects.get_or_create(
                slug=section['slug'],
                defaults={
                    'name': section['name'],
                    'description': f'Hình ảnh từ mục {section["name"]} - misvn.edu.vn',
                }
            )
            
            if created:
                self.stdout.write(f'  [+] Created album: {section["name"]}')
            else:
                self.stdout.write(f'  [i] Using existing album: {section["name"]}')
            
            section_images = 0
            all_image_urls = set()
            
            # Crawl all URLs in this section
            for url in section['urls']:
                self.stdout.write(f'  >> Scanning: {url}')
                
                soup = self.get_page(url)
                if not soup:
                    continue
                
                # Find all images on the page
                images = self.find_images(soup, base_url)
                all_image_urls.update(images)
                
                # Also find article links and crawl their images
                article_links = self.find_article_links(soup, base_url)
                
                for i, article_url in enumerate(article_links[:max_pages]):
                    self.stdout.write(f'  -> Scanning article {i+1}/{min(len(article_links), max_pages)}: {article_url[:60]}...')
                    
                    article_soup = self.get_page(article_url)
                    if article_soup:
                        article_images = self.find_images(article_soup, base_url)
                        all_image_urls.update(article_images)
                    
                    time.sleep(0.5)  # Be respectful
            
            self.stdout.write(f'  Found {len(all_image_urls)} unique image URLs')
            
            # Download and save images
            for i, img_url in enumerate(list(all_image_urls)[:limit]):
                try:
                    content_file, filename = self.download_image(img_url, base_url)
                    
                    if not content_file:
                        continue
                    
                    # Check for duplicate by content hash
                    content_hash = self.get_image_hash(content_file.read())
                    content_file.seek(0)  # Reset file pointer
                    
                    if content_hash in seen_hashes:
                        continue
                    
                    seen_hashes.add(content_hash)
                    
                    # Check if photo already exists by caption (URL-based)
                    url_hash = hashlib.md5(img_url.encode()).hexdigest()[:15]
                    if Photo.objects.filter(album=album, caption__contains=url_hash).exists():
                        continue
                    
                    # Create photo entry
                    photo = Photo(
                        album=album,
                        caption=f'{filename} ({url_hash})',
                        order=i,
                    )
                    
                    photo.image.save(filename, content_file, save=False)
                    photo.save()
                    
                    section_images += 1
                    total_images += 1
                    
                    if section_images % 10 == 0:
                        self.stdout.write(f'  [+] Downloaded {section_images} images...')
                    
                except Exception as e:
                    continue
            
            # Update album cover if needed
            if section_images > 0 and not album.cover_image:
                first_photo = album.photos.first()
                if first_photo:
                    album.cover_image = first_photo.image
                    album.save()
                    self.stdout.write(f'  [+] Set album cover image')
            
            self.stdout.write(self.style.SUCCESS(f'  [OK] Downloaded {section_images} images to album "{section["name"]}"'))
            time.sleep(1)
        
        self.stdout.write(self.style.SUCCESS(f'\n=== DONE: Downloaded {total_images} images across all albums ===' ))

    def find_images(self, soup, base_url):
        """Find all valid image URLs from a page"""
        image_urls = set()
        
        # Find all img tags
        for img in soup.find_all('img'):
            # Try multiple source attributes
            for attr in ['src', 'data-src', 'data-lazy-src', 'data-original', 'srcset']:
                img_url = img.get(attr, '')
                if img_url:
                    # Handle srcset (take the largest image)
                    if attr == 'srcset':
                        parts = img_url.split(',')
                        if parts:
                            # Get the last (usually largest) image
                            img_url = parts[-1].strip().split(' ')[0]
                    
                    if self.is_valid_image_url(img_url):
                        image_urls.add(img_url)
        
        # Find background images in style attributes
        for elem in soup.find_all(style=True):
            style = elem.get('style', '')
            # Extract url() from background-image
            matches = re.findall(r'url\([\'"]?([^\'"()]+)[\'"]?\)', style)
            for match in matches:
                if self.is_valid_image_url(match):
                    image_urls.add(match)
        
        # Find images in figure/picture elements
        for figure in soup.find_all(['figure', 'picture']):
            source = figure.find('source')
            if source:
                srcset = source.get('srcset', '')
                if srcset:
                    parts = srcset.split(',')
                    if parts:
                        img_url = parts[-1].strip().split(' ')[0]
                        if self.is_valid_image_url(img_url):
                            image_urls.add(img_url)
        
        # Find gallery/slider images
        for gallery in soup.find_all(['div', 'ul'], class_=re.compile(r'gallery|slider|carousel|lightbox', re.I)):
            for img in gallery.find_all('img'):
                img_url = img.get('src') or img.get('data-src')
                if img_url and self.is_valid_image_url(img_url):
                    image_urls.add(img_url)
        
        return image_urls

    def is_valid_image_url(self, url):
        """Check if URL is a valid image URL"""
        if not url:
            return False
        
        # Skip data URIs and placeholders
        skip_patterns = [
            'data:image', 'placeholder', 'loading', 'blank',
            '1x1', 'pixel', 'transparent', 'spacer',
            'logo', 'icon', 'favicon', 'avatar',
            '.svg', '.gif'  # Skip SVGs and GIFs
        ]
        
        url_lower = url.lower()
        for pattern in skip_patterns:
            if pattern in url_lower:
                return False
        
        # Check for image extensions
        image_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        has_image_ext = any(ext in url_lower for ext in image_extensions)
        
        # Also accept URLs that look like image paths
        looks_like_image = any(pattern in url_lower for pattern in [
            '/uploads/', '/images/', '/photos/', '/media/',
            '/wp-content/uploads/', '/gallery/'
        ])
        
        return has_image_ext or looks_like_image

    def find_article_links(self, soup, base_url):
        """Find article links on a page"""
        links = set()
        
        for a in soup.find_all('a', href=True):
            href = a.get('href', '')
            
            if not href or href == '#':
                continue
            
            # Skip external links
            if href.startswith('http') and 'misvn.edu.vn' not in href:
                continue
            
            # Skip certain patterns
            skip_patterns = [
                'javascript:', 'mailto:', 'tel:', '#',
                '/category/', '/tag/', '/author/', '/page/',
                'facebook.com', 'twitter.com', 'youtube.com',
                '/wp-admin/', '/feed/', '/search'
            ]
            
            if any(pattern in href.lower() for pattern in skip_patterns):
                continue
            
            # Look for article patterns
            article_patterns = [
                r'/\d{4}/\d{2}/[^/]+',  # /2025/01/article-slug
                r'/tin-tuc/[^/]+',
                r'/su-kien/[^/]+',
                r'/hoat-dong/[^/]+',
            ]
            
            for pattern in article_patterns:
                if re.search(pattern, href):
                    full_url = urljoin(base_url, href)
                    links.add(full_url)
                    break
        
        return list(links)
