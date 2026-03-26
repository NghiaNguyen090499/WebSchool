import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_website.settings")
django.setup()

from news.models import News
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from django.utils.text import slugify

sys.stdout.reconfigure(encoding='utf-8')

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

def download_image(url, folder):
    if not url: return ""
    try:
        res = session.get(url, timeout=10)
        if res.status_code == 200:
            filename = os.path.basename(urlparse(url).path)
            if not filename:
                filename = 'image.jpg'
            from django.conf import settings
            target_dir = os.path.join(settings.MEDIA_ROOT, folder)
            os.makedirs(target_dir, exist_ok=True)
            
            base, ext = os.path.splitext(filename)
            unique_name = f"{base}_{int(time.time()*1000)}{ext}"
            file_path = os.path.join(target_dir, unique_name)
            
            with open(file_path, 'wb') as f:
                f.write(res.content)
            
            return f"{folder}/{unique_name}"
    except Exception:
        pass
    return ""

def fix_page(page):
    url = f'https://misvn.edu.vn/category/tin-tuc/page/{page}/' if page > 1 else 'https://misvn.edu.vn/category/tin-tuc/'
    res = session.get(url, timeout=10)
    if res.status_code != 200:
        return 0
        
    soup = BeautifulSoup(res.text, 'html.parser')
    fixed = 0
    for article in soup.select('article'):
        a_title = article.select_one('.jeg_post_title a')
        if not a_title: continue
        title = a_title.text.strip()
        slug = slugify(title)[:40] # Since we matched by base_slug roughly, exact matching is tricky due to suffix -1
        # Let's match by title directly to be safe, since title was exact! Or startswith slug.
        
        # Better: match by title
        news = News.all_objects.filter(title__iexact=title).first()
        if not news:
            continue
            
        thumb_el = article.select_one('.thumbnail-container img')
        if not thumb_el: continue
        
        thumb_url = thumb_el.get('data-src') or thumb_el.get('src')
        if thumb_url:
            thumb_url = get_original_image_url(thumb_url)
            local_path = download_image(thumb_url, 'news/thumbnails')
            if local_path:
                news.thumbnail.name = local_path
                news.save(update_fields=['thumbnail'])
                fixed += 1
    return fixed

def main():
    total_fixed = 0
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fix_page, p): p for p in range(1, 154)}
        for future in as_completed(futures):
            fixed = future.result()
            total_fixed += fixed
            print(f"Page {futures[future]} done, fixed {fixed}")
    
    print("Total thumbnails fixed:", total_fixed)

if __name__ == "__main__":
    main()
