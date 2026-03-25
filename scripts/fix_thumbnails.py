# -*- coding: utf-8 -*-
"""
Script de tai lai thumbnail cho cac bai viet da crawl nhung thieu anh.
Cach lam:
  1. Duyet trang listing cua misvn.edu.vn de lay mapping: URL -> thumbnail URL
  2. Tim bai viet trong DB khop voi URL (bang cach so sanh slug)  
  3. Tai anh va cap nhat DB

Cach dung:
    cd d:/NGHIA/WebsiteSchool
    python scripts/fix_thumbnails.py
"""

import os
import sys
import time
import re
import hashlib
import unicodedata
from urllib.parse import urlparse

# Fix Windows console encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

import requests
from bs4 import BeautifulSoup

# Django setup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_website.settings")

import django
django.setup()

from django.core.files.base import ContentFile
from news.models import News

# Config
BASE_URL = "https://misvn.edu.vn"
LISTING_URL = f"{BASE_URL}/category/tin-tuc/"
MAX_PAGES = 55  # Duyet du 55 trang listing
REQUEST_DELAY = 1.0
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "vi-VN,vi;q=0.9,en;q=0.8",
}


def vietnamese_to_ascii(text):
    """Chuyen tieng Viet co dau thanh khong dau."""
    nfkd = unicodedata.normalize('NFKD', text)
    result = ''
    for c in nfkd:
        if c == '\u0111':
            result += 'd'
        elif c == '\u0110':
            result += 'D'
        elif unicodedata.category(c) == 'Mn':
            continue
        else:
            result += c
    return result


def make_slug(text):
    """Tao slug ASCII tu text."""
    from django.utils.text import slugify
    return slugify(vietnamese_to_ascii(text))


def fetch_page(url, retries=3):
    for attempt in range(retries):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=30)
            resp.raise_for_status()
            return resp
        except requests.RequestException as e:
            print(f"  [!] Loi {attempt+1}/{retries}: {e}")
            if attempt < retries - 1:
                time.sleep(3)
    return None


def download_image(image_url):
    """Tai anh va tra ve ContentFile."""
    if not image_url:
        return None
    try:
        resp = requests.get(image_url, headers=HEADERS, timeout=30, stream=True)
        resp.raise_for_status()

        # Kiem tra content-type
        ct = resp.headers.get("content-type", "")
        if "jpeg" in ct or "jpg" in ct:
            ext = ".jpg"
        elif "png" in ct:
            ext = ".png"
        elif "webp" in ct:
            ext = ".webp"
        elif "gif" in ct:
            ext = ".gif"
        else:
            path_ext = os.path.splitext(urlparse(image_url).path)[1]
            ext = path_ext if path_ext else ".jpg"

        # Kiem tra kich thuoc (it nhat 5KB)
        if len(resp.content) < 5000:
            return None

        fname = hashlib.md5(image_url.encode()).hexdigest()[:16] + ext
        return ContentFile(resp.content, name=fname)
    except Exception as e:
        print(f"  [!] Loi tai anh: {e}")
        return None


def get_thumbnail_from_article_page(article_url):
    """Truy cap trang bai viet va lay og:image hoac featured image."""
    resp = fetch_page(article_url)
    if not resp:
        return None

    soup = BeautifulSoup(resp.text, "html.parser")

    # Strategy 1: og:image (most reliable)
    og_img = soup.find("meta", property="og:image")
    if og_img:
        url = og_img.get("content", "")
        if url and not url.endswith("logo") and "placeholder" not in url.lower():
            return url

    # Strategy 2: Featured image in post
    selectors = [
        ".post-thumbnail img",
        ".entry-thumbnail img",
        ".featured-image img",
        "article img",
        ".td-post-featured-image img",
        ".entry-content img",
    ]
    for sel in selectors:
        img = soup.select_one(sel)
        if img:
            src = img.get("data-lazy-src") or img.get("data-src") or img.get("src", "")
            if src and "logo" not in src.lower() and src.startswith("http"):
                return src

    return None


def get_listings_with_thumbnails(max_pages=MAX_PAGES):
    """
    Duyet cac trang listing va lay mapping:
    article_url -> thumbnail_url
    Tu listing page co the lay thumbnail nhanh hon (1 request = nhieu bai)
    """
    mapping = {}

    for page_num in range(1, max_pages + 1):
        url = LISTING_URL if page_num == 1 else f"{LISTING_URL}page/{page_num}/"
        print(f"[Listing {page_num}/{max_pages}] {url}")

        resp = fetch_page(url)
        if not resp or resp.status_code == 404:
            print(f"  [!] Het trang. Dung.")
            break

        soup = BeautifulSoup(resp.text, "html.parser")
        articles = soup.select("article")
        found = 0

        for article in articles:
            # Tim link bai viet
            link_tag = article.find("a", href=True)
            if not link_tag:
                continue
            href = link_tag["href"]
            if "/category/" in href:
                continue

            # Tim thumbnail trong listing
            img = article.find("img")
            thumb_url = None
            if img:
                # Thu cac attribute khac nhau
                thumb_url = (
                    img.get("data-lazy-src") or
                    img.get("data-src") or 
                    img.get("src", "")
                )
                # Bo qua placeholder/dummy images
                if thumb_url and ("data:image" in thumb_url or "placeholder" in thumb_url.lower()):
                    thumb_url = None

            if thumb_url and href not in mapping:
                mapping[href] = thumb_url
                found += 1

        print(f"  -> {found} thumbnails (tong: {len(mapping)})")

        if not articles:
            break

        time.sleep(REQUEST_DELAY)

    return mapping


def run():
    print("=" * 70)
    print("  FIX THUMBNAILS - TAI ANH CHO BAI VIET THIEU")
    print("=" * 70)

    # Buoc 1: Tim cac bai viet thieu thumbnail
    missing = News.objects.filter(thumbnail='') | News.objects.filter(thumbnail__isnull=True)
    total_missing = missing.count()
    total = News.objects.count()
    print(f"\nTong bai viet: {total}")
    print(f"Thieu thumbnail: {total_missing}")
    print(f"Da co thumbnail: {total - total_missing}")

    if total_missing == 0:
        print("\n[OK] Tat ca bai viet da co thumbnail!")
        return

    # Buoc 2: Duyet listing de lay URL thumbnail
    print(f"\n[BUOC 1] Duyet listing lay URL thumbnail...")
    listing_map = get_listings_with_thumbnails()
    print(f"\n=> Thu thap duoc {len(listing_map)} URLs thumbnail tu listing")

    # Buoc 3: Thu match va tai thumbnail
    print(f"\n[BUOC 2] Tai thumbnail cho cac bai viet thieu anh...")
    updated = 0
    failed = 0
    skipped = 0

    for i, news_item in enumerate(missing.iterator(), 1):
        # Tim URL bai viet tren misvn bangcach tim slug trong listing_map
        slug = news_item.slug
        title_lower = news_item.title.lower()
        
        # Tim URL khop trong listing mapping
        matched_url = None
        matched_thumb = None
        
        for article_url, thumb_url in listing_map.items():
            # So sanh slug trong URL
            url_path = urlparse(article_url).path.strip("/").split("/")[-1]
            if url_path and url_path == slug:
                matched_url = article_url
                matched_thumb = thumb_url
                break
        
        if not matched_thumb:
            # Thu tim bang cach so sanh title (chuyen thanh slug roi compare)
            for article_url, thumb_url in listing_map.items():
                url_path = urlparse(article_url).path.strip("/").split("/")[-1]
                # Tao slug ASCII tu url_path
                url_slug_ascii = make_slug(url_path.replace("-", " "))
                if url_slug_ascii and url_slug_ascii == slug:
                    matched_url = article_url
                    matched_thumb = thumb_url
                    break

        if matched_thumb:
            # Tai thumbnail tu listing
            cf = download_image(matched_thumb)
            if cf:
                news_item.thumbnail.save(cf.name, cf, save=True)
                updated += 1
                print(f"  [{updated}] OK: {news_item.title[:50]}...")
            else:
                failed += 1
                print(f"  [!] Loi tai: {news_item.title[:50]}...")
        else:
            skipped += 1

        # Moi 50 bai in progress
        if i % 50 == 0:
            print(f"\n--- Progress: {i}/{total_missing} | Updated: {updated} | Failed: {failed} | Skipped: {skipped} ---\n")

    # Buoc 4: Nhung bai khong tim thay trong listing -> truy cap truc tiep trang bai viet
    remaining = News.objects.filter(thumbnail='') | News.objects.filter(thumbnail__isnull=True)
    remaining_count = remaining.count()
    
    if remaining_count > 0:
        print(f"\n[BUOC 3] Con {remaining_count} bai chua co anh. Thu truy cap truc tiep bai viet...")
        
        for i, news_item in enumerate(remaining.iterator(), 1):
            # Thu di trang bai viet goc de lay og:image
            # Tim URL bai viet
            possible_urls = []
            for article_url in listing_map.keys():
                url_path = urlparse(article_url).path.strip("/").split("/")[-1]
                url_slug_ascii = make_slug(url_path.replace("-", " "))
                if url_slug_ascii == news_item.slug:
                    possible_urls.append(article_url)
            
            if possible_urls:
                article_url = possible_urls[0]
                thumb_url = get_thumbnail_from_article_page(article_url)
                if thumb_url:
                    cf = download_image(thumb_url)
                    if cf:
                        news_item.thumbnail.save(cf.name, cf, save=True)
                        updated += 1
                        print(f"  [{updated}] OK (direct): {news_item.title[:50]}...")
                        time.sleep(REQUEST_DELAY)
                        continue
            
            # Thu tim tren Google cache / truc tiep
            # Build potential URL
            for article_url in listing_map.keys():
                pass  # Skip nếu không tìm được

            if i % 20 == 0:
                print(f"  --- Direct access progress: {i}/{remaining_count} ---")

    # Ket qua
    final_missing = (News.objects.filter(thumbnail='') | News.objects.filter(thumbnail__isnull=True)).count()
    print("\n" + "=" * 70)
    print("  KET QUA FIX THUMBNAILS")
    print(f"  Da cap nhat:  {updated}")
    print(f"  That bai:     {failed}")
    print(f"  Khong tim:    {skipped}")
    print(f"  Con thieu:    {final_missing}/{total}")
    print("=" * 70)


if __name__ == "__main__":
    run()
