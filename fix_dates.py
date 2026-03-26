import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_website.settings")
django.setup()

from news.models import News
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
adapter = requests.adapters.HTTPAdapter(pool_connections=20, pool_maxsize=20)
session.mount('https://', adapter)
session.mount('http://', adapter)

start_date = make_aware(datetime.now())

def get_page_titles(page):
    url = f'https://misvn.edu.vn/category/tin-tuc/page/{page}/' if page > 1 else 'https://misvn.edu.vn/category/tin-tuc/'
    res = session.get(url, timeout=10)
    if res.status_code != 200:
        return []
        
    soup = BeautifulSoup(res.text, 'html.parser')
    titles = []
    for article in soup.select('article'):
        a_title = article.select_one('.jeg_post_title a')
        if a_title:
            titles.append(a_title.text.strip())
    return titles

def main():
    print("Fetching titles from pages to rebuild chronological order...")
    page_to_titles = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(get_page_titles, p): p for p in range(1, 154)}
        for future in as_completed(futures):
            p = futures[future]
            try:
                page_to_titles[p] = future.result()
            except Exception:
                pass

    print("Executing database update...")
    fixed = 0
    for page in range(1, 154):
        titles = page_to_titles.get(page, [])
        for idx, title in enumerate(titles):
            rank = (page - 1) * 10 + idx
            # ~ 1.8 days per article
            new_date = start_date - timedelta(hours=rank * 43)
            
            # Using update() is much faster and avoids save() overriding
            updated = News.all_objects.filter(title__iexact=title).update(created_at=new_date)
            fixed += updated
                
    print(f"Update complete! Fixed dates for {fixed} database records safely.")

if __name__ == "__main__":
    main()
