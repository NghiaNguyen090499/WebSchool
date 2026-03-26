import os
import sys
import django
import re
import time
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_website.settings")
django.setup()

from news.models import News
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 429, 500, 502, 503, 504 ])
adapter = HTTPAdapter(max_retries=retries, pool_connections=15, pool_maxsize=15)
session.mount('http://', adapter)
session.mount('https://', adapter)

from django.conf import settings

def download_image(url, folder='news/content'):
    try:
        # Prevent downloading emoji junk that caused issues earlier (if we want, but misvn serves them)
        if 's.w.org' in url:
            return "" # Skip WP emoji CDNs
            
        # Clean URL if it's scaled or thumbnailed (like we did before)
        orig = re.sub(r'-\d+x\d+(?=\.\w+)', '', url)
        orig_unscaled = re.sub(r'-scaled(?=\.\w+)', '', orig)
        
        target_url = url
        # Just download whatever URL it currently is, if we try HEAD it takes too long.
        # Let's just download the unscaled version, if it 404s, download original.
        res = session.get(orig_unscaled, timeout=10)
        if res.status_code != 200:
            res = session.get(orig, timeout=10)
        if res.status_code != 200:
            res = session.get(url, timeout=10)
            
        if res.status_code == 200:
            filename = os.path.basename(urlparse(res.url).path)
            if not filename: filename = 'image.jpg'
            
            target_dir = os.path.join(settings.MEDIA_ROOT, folder)
            os.makedirs(target_dir, exist_ok=True)
            
            base, ext = os.path.splitext(filename)
            unique_name = f"{base}_{int(time.time()*1000)}{ext}"
            file_path = os.path.join(target_dir, unique_name)
            
            with open(file_path, 'wb') as f:
                f.write(res.content)
            
            return f"{folder}/{unique_name}"
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    return ""

def rescue_article_images(news_id):
    news = News.all_objects.get(id=news_id)
    soup = BeautifulSoup(news.content, 'html.parser')
    
    changed = False
    
    # Fix internal links while we're at it!
    for a in soup.select('a[href]'):
        href = a['href']
        if 'misvn.edu.vn' in href:
            # e.g https://misvn.edu.vn/slug/ -> /tin-tuc/slug/
            # e.g https://misvn.edu.vn/category/tin-tuc/ -> /tin-tuc/
            if '/category/tin-tuc' in href:
                a['href'] = '/tin-tuc/'
                changed = True
            else:
                match = re.search(r'misvn\.edu\.vn/([^/]+)/?', href)
                if match:
                    if match.group(1) not in ['wp-content', 'category', 'tag', 'author']:
                        a['href'] = f"/tin-tuc/{match.group(1)}/"
                        changed = True

    for img in soup.select('img'):
        src = img.get('src') or ''
        # If it's still missing or pointing to misvn
        if 'misvn.edu.vn' in src or 's.w.org' in src:
            if 'misvn.edu.vn' in src:
                # Need to download real image
                local_path = download_image(src)
                if local_path:
                    img['src'] = f"{settings.MEDIA_URL}{local_path}"
                    changed = True
                    # Clean WP image attrs
                    for attr in ['srcset', 'data-srcset', 'data-src', 'sizes']:
                        if img.has_attr(attr): del img[attr]
            else:
                # Emoji -> just delete it or ignore, we can just leave it as is if from s.w.org
                pass

    if changed:
        news.content = str(soup)
        news.save(update_fields=['content'])
        return 1
    return 0

def main():
    qs = News.all_objects.filter(content__icontains='misvn.edu.vn')
    ids = list(qs.values_list('id', flat=True))
    print(f"Found {len(ids)} articles to rescue...")
    
    fixed = 0
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(rescue_article_images, nid): nid for nid in ids}
        for future in as_completed(futures):
            fixed += future.result()
            print(f"Rescued {fixed} articles...", end='\\r', flush=True)

    print(f"\\nFinished! Successfully rescued content for {fixed} articles.")

if __name__ == '__main__':
    main()
