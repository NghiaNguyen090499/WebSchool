import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import django
import argparse

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_website.settings")
django.setup()

from news.models import News, Category
from django.core.files.base import ContentFile
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.utils.text import slugify

session = requests.Session()
adapter = requests.adapters.HTTPAdapter(pool_connections=20, pool_maxsize=20)
session.mount('https://', adapter)
session.mount('http://', adapter)

def get_original_image_url(url):
    orig = re.sub(r'-\d+x\d+(?=\.\w+)', '', url)
    orig_unscaled = re.sub(r'-scaled(?=\.\w+)', '', orig)
    
    try:
        if orig_unscaled != url:
            h = session.head(orig_unscaled, timeout=5)
            if h.status_code == 200: return orig_unscaled
        if orig != url:
            h = session.head(orig, timeout=5)
            if h.status_code == 200: return orig
    except:
        pass
    return url

def guess_date_from_image(url):
    match = re.search(r'/wp-content/uploads/(\d{4})/(\d{2})/', url)
    if match:
        year, month = int(match.group(1)), int(match.group(2))
        return make_aware(datetime(year, month, 15, 12, 0, 0))
    return None

def download_image(url, folder):
    try:
        res = session.get(url, timeout=10)
        if res.status_code == 200:
            filename = os.path.basename(urlparse(url).path)
            if not filename:
                filename = 'image.jpg'
            # Save to MEDIA_ROOT/folder
            from django.conf import settings
            target_dir = os.path.join(settings.MEDIA_ROOT, folder)
            os.makedirs(target_dir, exist_ok=True)
            
            # Make unique filename
            base, ext = os.path.splitext(filename)
            unique_name = f"{base}_{int(time.time()*1000)}{ext}"
            file_path = os.path.join(target_dir, unique_name)
            
            with open(file_path, 'wb') as f:
                f.write(res.content)
            
            return f"{folder}/{unique_name}"
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    return ""

def process_article(href):
    try:
        res = session.get(href, timeout=15)
        if res.status_code != 200:
            return None
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Title
        title_el = soup.select_one('.jeg_post_title')
        if not title_el: return None
        title = title_el.text.strip()
        
        # Slug check
        base_slug = slugify(title)[:40] # Prevent slug from being too long
        slug = base_slug
        counter = 1
        while News.all_objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
            
        # Category
        cat_els = soup.select('.jeg_meta_category a')
        category_name = cat_els[0].text.strip() if cat_els else "Tin tức"
        cat = Category.objects.filter(name=category_name).first()
        if not cat:
            cat = Category.objects.create(name=category_name)
        
        # Content
        content_area = soup.select_one('.content-inner')
        if not content_area: return None
        
        # Excerpt
        excerpt_el = soup.select_one('.jeg_post_excerpt')
        excerpt = excerpt_el.text.strip()[:300] if excerpt_el else ""
        
        # Images in content
        first_img_url = ""
        for img in content_area.select('img'):
            src = img.get('data-src') or img.get('src')
            if not src:
                continue
                
            orig_src = get_original_image_url(src)
            if not first_img_url:
                first_img_url = orig_src
                
            local_path = download_image(orig_src, 'news/content')
            if local_path:
                from django.conf import settings
                img['src'] = f"{settings.MEDIA_URL}{local_path}"
                # remove srcset to force using the downloaded image
                if img.has_attr('srcset'): del img['srcset']
                if img.has_attr('data-srcset'): del img['data-srcset']
                if img.has_attr('data-src'): del img['data-src']
                if img.has_attr('sizes'): del img['sizes']

        content_html = str(content_area)
        
        # Date
        created_at = None
        if first_img_url:
            created_at = guess_date_from_image(first_img_url)
        
        if not created_at:
            created_at = make_aware(datetime.now())
            
        # We need thumbnail (try feature image if available outside content-inner, else first image)
        thumb_el = soup.select_one('.featured_image img')
        thumb_url = ""
        if thumb_el:
            thumb_url = thumb_el.get('data-src') or thumb_el.get('src')
            thumb_url = get_original_image_url(thumb_url)
        if not thumb_url:
            thumb_url = first_img_url
            
        thumb_local = ""
        if thumb_url:
            thumb_local = download_image(thumb_url, 'news/thumbnails')
            
        news = News(
            title=title,
            slug=slug,
            content=content_html,
            excerpt=excerpt,
            category=cat,
            created_at=created_at,
            is_featured=False,
            is_archived=False
        )
        if thumb_local:
            news.thumbnail.name = thumb_local
            
        # To avoid the manager/auto_now overwriting the date, we normally save it, then update date
        news.save()
        News.objects.filter(id=news.id).update(created_at=created_at)
        
        print(f"Created: {title}")
        return True
    except Exception as e:
        print(f"Error processing {href}: {e}")
        return False

def get_article_links(page):
    url = f'https://misvn.edu.vn/category/tin-tuc/page/{page}/' if page > 1 else 'https://misvn.edu.vn/category/tin-tuc/'
    res = session.get(url, timeout=10)
    if res.status_code != 200:
        return []
        
    soup = BeautifulSoup(res.text, 'html.parser')
    links = []
    for article in soup.select('article'):
        a = article.select_one('.jeg_post_title a')
        if a:
            links.append(a['href'])
    return links

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true', help='Crawl only the first page and a maximum of 3 articles.')
    args = parser.parse_args()

    total_pages = 1 if args.test else 153
    all_links = []
    print("Fetching article links from pages...")
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(get_article_links, p): p for p in range(1, total_pages + 1)}
        for future in as_completed(futures):
            page = futures[future]
            try:
                links = future.result()
                all_links.extend(links)
                print(f"Page {page} done, got {len(links)} links")
            except Exception as e:
                print(f"Page {page} error: {e}")
                
    all_links = list(set(all_links))
    if args.test:
        all_links = all_links[:3]
    
    print(f"Total unique article links: {len(all_links)}")
    
    print("Processing articles...")
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(process_article, link): link for link in all_links}
        for i, future in enumerate(as_completed(futures)):
            if (i+1) % 10 == 0 or args.test:
                print(f"Processed {i+1}/{len(all_links)} articles")

if __name__ == "__main__":
    main()
