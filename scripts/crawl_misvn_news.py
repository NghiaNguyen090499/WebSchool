# -*- coding: utf-8 -*-
"""
Script crawl tin tuc tu https://misvn.edu.vn/category/tin-tuc/
Duyet 50 trang listing (page 1 -> page 50), lay tat ca bai viet.
Luu vao database Django thong qua ORM (News, Category models).

Cach dung:
    cd d:/NGHIA/WebsiteSchool
    python scripts/crawl_misvn_news.py
"""

import os
import sys
import time
import re
import hashlib
import unicodedata
from io import BytesIO
from urllib.parse import urljoin, urlparse

# Fix Windows console encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

import requests
from bs4 import BeautifulSoup

# ── Django setup ──────────────────────────────────────────────────────────
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_website.settings")

import django
django.setup()

from django.core.files.base import ContentFile
from django.utils.text import slugify as django_slugify
from news.models import News, Category

# ── Config ────────────────────────────────────────────────────────────────
BASE_URL = "https://misvn.edu.vn"
CATEGORY_URL = f"{BASE_URL}/category/tin-tuc/"
START_PAGE = 1           # Trang bat dau crawl
END_PAGE = 1             # Trang ket thuc crawl (chi trang 1 - bai moi nhat)
REQUEST_DELAY = 1.5      # delay giua cac request (tranh bi block)
UPDATE_MODE = True       # True = cap nhat bai da ton tai, False = bo qua
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "vi-VN,vi;q=0.9,en;q=0.8",
}


# ── Helpers ───────────────────────────────────────────────────────────────
def vietnamese_to_ascii(text):
    """Remove Vietnamese diacritics via Unicode NFKD decomposition."""
    nfkd = unicodedata.normalize('NFKD', text)
    ascii_text = ''
    for char in nfkd:
        if char == '\u0111':  # d-
            ascii_text += 'd'
        elif char == '\u0110':  # D-
            ascii_text += 'D'
        elif unicodedata.category(char) == 'Mn':  # combining mark
            continue
        else:
            ascii_text += char
    return ascii_text


def safe_slugify(text, max_length=200):
    """Tao slug ASCII-only (khong dau tieng Viet)."""
    ascii_text = vietnamese_to_ascii(text)
    slug = django_slugify(ascii_text)
    if not slug:
        slug = hashlib.md5(text.encode()).hexdigest()[:12]
    return slug[:max_length]


def fetch_page(url, retries=3):
    """GET request voi retry logic."""
    for attempt in range(retries):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=30)
            resp.raise_for_status()
            return resp
        except requests.RequestException as e:
            print(f"  [!] Loi lan {attempt + 1}/{retries}: {e}")
            if attempt < retries - 1:
                time.sleep(3)
    return None


def get_article_urls_from_listing(start_page=START_PAGE, end_page=END_PAGE):
    """
    Duyet cac trang listing /category/tin-tuc/page/N/
    tu start_page den end_page (bao gom).
    Tra ve list URLs cua tat ca bai viet tim duoc.
    """
    article_urls = []

    for page_num in range(start_page, end_page + 1):
        if page_num == 1:
            url = CATEGORY_URL
        else:
            url = f"{CATEGORY_URL}page/{page_num}/"

        print(f"[Trang {page_num}/{end_page}] {url}")
        resp = fetch_page(url)
        if not resp:
            if resp is None and page_num > 1:
                # Co the da het trang
                print(f"  [!] Khong the tai trang {page_num}. Co the da het bai viet.")
                break
            print(f"  [X] Khong the tai trang {page_num}. Dung.")
            break

        # Kiem tra 404 (het trang)
        if resp.status_code == 404:
            print(f"  [!] Trang {page_num} khong ton tai (404). Dung.")
            break

        soup = BeautifulSoup(resp.text, "html.parser")
        found_on_page = 0

        # Strategy 1: Tim cac <article> elements
        articles = soup.select("article")
        if articles:
            for article in articles:
                link_tag = article.find("a", href=True)
                if link_tag:
                    href = link_tag["href"]
                    if (href.startswith(BASE_URL) and
                        "/category/" not in href and
                        href not in article_urls):
                        article_urls.append(href)
                        found_on_page += 1

        # Strategy 2: Neu khong tim thay article tags, tim qua heading links
        if found_on_page == 0:
            headings = soup.select("h2 a[href], h3 a[href]")
            for h in headings:
                href = h.get("href", "")
                if (href.startswith(BASE_URL) and
                    "/category/" not in href and
                    "/page/" not in href and
                    "/tag/" not in href and
                    href not in article_urls):
                    article_urls.append(href)
                    found_on_page += 1

        print(f"  -> Tim duoc {found_on_page} bai viet (tong: {len(article_urls)})")

        if found_on_page == 0:
            print("  [!] Khong tim them bai viet. Dung pagination.")
            break

        time.sleep(REQUEST_DELAY)

    return article_urls


def scrape_article(url):
    """
    Truy cap mot bai viet va trich xuat:
    - title
    - content (HTML)
    - excerpt (text ngan)
    - thumbnail_url
    - categories
    """
    resp = fetch_page(url)
    if not resp:
        return None

    soup = BeautifulSoup(resp.text, "html.parser")

    # ── Title ──
    title = ""
    h1 = soup.select_one("h1.entry-title, h1.post-title, article h1, .single-post-title h1, h1")
    if h1:
        title = h1.get_text(strip=True)
    if not title:
        og_title = soup.find("meta", property="og:title")
        if og_title:
            title = og_title.get("content", "")
    if not title:
        title_tag = soup.find("title")
        if title_tag:
            title = title_tag.get_text(strip=True).split("–")[0].strip()

    # ── Thumbnail ──
    thumbnail_url = ""
    og_image = soup.find("meta", property="og:image")
    if og_image:
        thumbnail_url = og_image.get("content", "")
    if not thumbnail_url:
        featured = soup.select_one(".post-thumbnail img, .entry-thumbnail img, .featured-image img")
        if featured:
            thumbnail_url = featured.get("data-src") or featured.get("src", "")

    # ── Content ──
    content_html = ""
    content_text = ""

    content_area = soup.select_one(
        ".entry-content, .post-content, .single-post-content, "
        "article .content, .td-post-content, .post_content"
    )

    if content_area:
        # Loai bo cac phan khong can thiet
        for tag in content_area.select(
            "script, style, .sharedaddy, .jp-relatedposts, "
            ".post-tags, .social-share, .related-posts, "
            ".comments-area, .navigation, .yarpp-related, "
            "iframe[src*='facebook'], .fb-comments"
        ):
            tag.decompose()

        content_html = str(content_area)
        content_text = content_area.get_text(separator="\n", strip=True)

    # ── Excerpt ──
    excerpt = ""
    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc:
        excerpt = meta_desc.get("content", "")[:300]
    if not excerpt:
        og_desc = soup.find("meta", property="og:description")
        if og_desc:
            excerpt = og_desc.get("content", "")[:300]
    if not excerpt and content_text:
        excerpt = content_text[:300].rsplit(" ", 1)[0] + "..."

    # ── Categories ──
    categories = []
    cat_links = soup.select(
        'a[rel="category tag"], .cat-links a, '
        '.post-categories a, .entry-categories a, '
        '.td-post-category a'
    )
    for cat_link in cat_links:
        cat_name = cat_link.get_text(strip=True)
        if cat_name and cat_name not in categories:
            categories.append(cat_name)

    if not categories:
        categories = ["Tin tuc"]

    return {
        "title": title,
        "content": content_html,
        "excerpt": excerpt,
        "thumbnail_url": thumbnail_url,
        "categories": categories,
        "source_url": url,
    }


def download_thumbnail(image_url):
    """Tai thumbnail va tra ve ContentFile."""
    if not image_url:
        return None

    try:
        resp = requests.get(image_url, headers=HEADERS, timeout=30, stream=True)
        resp.raise_for_status()

        content_type = resp.headers.get("content-type", "")
        if "jpeg" in content_type or "jpg" in content_type:
            ext = ".jpg"
        elif "png" in content_type:
            ext = ".png"
        elif "webp" in content_type:
            ext = ".webp"
        elif "gif" in content_type:
            ext = ".gif"
        else:
            parsed = urlparse(image_url)
            path_ext = os.path.splitext(parsed.path)[1]
            ext = path_ext if path_ext else ".jpg"

        fname = hashlib.md5(image_url.encode()).hexdigest()[:16] + ext

        return ContentFile(resp.content, name=fname)
    except Exception as e:
        print(f"  [!] Loi tai thumbnail: {e}")
        return None


def save_to_database(article_data):
    """Luu bai viet vao database Django. Ho tro UPDATE_MODE."""
    title = article_data["title"]
    if not title:
        print("  [!] Bai viet khong co tieu de. Bo qua.")
        return None  # None = failed

    slug = safe_slugify(title)

    # Tao/lay category
    category_obj = None
    if article_data["categories"]:
        cat_name = article_data["categories"][0]
        cat_slug = safe_slugify(cat_name)
        category_obj, created = Category.objects.get_or_create(
            slug=cat_slug,
            defaults={"name": cat_name}
        )
        if created:
            print(f"  [NEW CAT] {cat_name}")

    # Kiem tra trung lap
    existing = News.objects.filter(slug=slug).first()
    if existing:
        if not UPDATE_MODE:
            print(f"  [SKIP] Da ton tai: {title[:60]}...")
            return False  # False = skipped

        # UPDATE MODE: cap nhat noi dung
        existing.title = title
        existing.content = article_data["content"]
        existing.excerpt = article_data["excerpt"]
        if category_obj:
            existing.category = category_obj

        # Tai thumbnail moi (neu co)
        thumbnail_file = download_thumbnail(article_data["thumbnail_url"])
        if thumbnail_file:
            existing.thumbnail.save(thumbnail_file.name, thumbnail_file, save=False)

        existing.save()
        print(f"  [UPDATED] {title[:60]}")
        return 'updated'

    # Tao bai viet moi
    thumbnail_file = download_thumbnail(article_data["thumbnail_url"])

    news = News(
        title=title,
        slug=slug,
        content=article_data["content"],
        excerpt=article_data["excerpt"],
        category=category_obj,
        is_featured=False,
    )

    if thumbnail_file:
        news.thumbnail.save(thumbnail_file.name, thumbnail_file, save=False)

    news.save()
    return True  # True = new


# ── Main ──────────────────────────────────────────────────────────────────
def run():
    print("=" * 70)
    print("  CRAWL TIN TUC TU MISVN.EDU.VN")
    print(f"  Duyet trang listing: {START_PAGE} -> {END_PAGE}")
    print("=" * 70)

    # Buoc 1: Thu thap URLs tu cac trang listing
    print(f"\n[BUOC 1] Thu thap danh sach bai viet tu {END_PAGE - START_PAGE + 1} trang listing...")
    article_urls = get_article_urls_from_listing(START_PAGE, END_PAGE)
    print(f"\n=> Tong URL thu thap: {len(article_urls)}")

    if not article_urls:
        print("[X] Khong tim thay bai viet nao. Kiem tra lai!")
        return

    # Buoc 2: Crawl tung bai
    mode_label = 'UPDATE' if UPDATE_MODE else 'SKIP duplicates'
    print(f"\n[BUOC 2] Crawl noi dung {len(article_urls)} bai viet... (mode: {mode_label})")
    saved = 0
    updated = 0
    skipped = 0
    failed = 0

    for i, url in enumerate(article_urls, 1):
        print(f"\n[{i}/{len(article_urls)}] {url}")

        data = scrape_article(url)
        if not data or not data["title"]:
            print("  [X] Khong lay duoc noi dung.")
            failed += 1
            continue

        print(f"  {data['title'][:70]}")
        print(f"  Categories: {', '.join(data['categories'][:3])}")

        result = save_to_database(data)
        if result is True:
            saved += 1
            print(f"  [OK] Da luu thanh cong!")
        elif result == 'updated':
            updated += 1
        elif result is False:
            skipped += 1
        else:
            failed += 1

        time.sleep(REQUEST_DELAY)

    # Ket qua
    print("\n" + "=" * 70)
    print("  KET QUA CRAWL")
    print(f"  Bai moi:     {saved}")
    print(f"  Cap nhat:    {updated}")
    print(f"  Bo qua:      {skipped}")
    print(f"  That bai:    {failed}")
    print(f"  Tong News:   {News.objects.count()}")
    print(f"  Tong Cats:   {Category.objects.count()}")
    print("=" * 70)


if __name__ == "__main__":
    run()
