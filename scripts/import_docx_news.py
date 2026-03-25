# -*- coding: utf-8 -*-
"""
Import 25 bài viết từ file .docx vào database News.
Các bước:
  1. Archive tất cả bài viết cũ (is_archived=True)
  2. Tạo 6 danh mục mới
  3. Parse .docx → HTML + images
  4. Tạo News objects với thumbnail, content, excerpt, category

Cách dùng:
    cd d:/NGHIA/WebsiteSchool
    python scripts/import_docx_news.py
"""

import os
import sys
import re
import hashlib
import unicodedata
from io import BytesIO

# Fix console encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

# ── Django setup ──
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_website.settings")

import django
django.setup()

from django.core.files.base import ContentFile
from django.utils.text import slugify as django_slugify
from django.conf import settings
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

from news.models import News, Category


# ============================================================
# CONFIGURATION
# ============================================================

# Category mapping: file_number → category_name
CATEGORY_MAP = {
    1: "Công nghệ & Đổi mới",
    2: "Hoạt động trải nghiệm",
    3: "Cuộc thi & Học thuật",
    4: "Hoạt động trải nghiệm",
    5: "Hoạt động trải nghiệm",
    6: "Sự kiện nhà trường",
    7: "Hoạt động trải nghiệm",
    8: "Cuộc thi & Học thuật",
    9: "Hợp tác quốc tế",
    10: "Cuộc thi & Học thuật",
    11: "Công nghệ & Đổi mới",
    12: "Hợp tác quốc tế",
    13: "Hợp tác quốc tế",
    14: "Cuộc thi & Học thuật",
    15: "Hợp tác quốc tế",
    16: "Sự kiện nhà trường",
    17: "Sự kiện nhà trường",
    18: "Thông báo & Tuyển sinh",
    19: "Thông báo & Tuyển sinh",
    20: "Thông báo & Tuyển sinh",
    21: "Thông báo & Tuyển sinh",
    22: "Sự kiện nhà trường",
    23: "Hoạt động trải nghiệm",
    24: "Sự kiện nhà trường",
    25: "Thông báo & Tuyển sinh",
}

# Featured articles (sẽ hiển thị nổi bật trên giao diện)
FEATURED_ARTICLES = [25, 3, 10]  # Thư mời Innovation Day, MIS Talks, KHKT

# Category slugs (Vietnamese ASCII)
CATEGORY_SLUGS = {
    "Công nghệ & Đổi mới": "cong-nghe-doi-moi",
    "Hoạt động trải nghiệm": "hoat-dong-trai-nghiem",
    "Cuộc thi & Học thuật": "cuoc-thi-hoc-thuat",
    "Hợp tác quốc tế": "hop-tac-quoc-te",
    "Sự kiện nhà trường": "su-kien-nha-truong",
    "Thông báo & Tuyển sinh": "thong-bao-tuyen-sinh",
}


# ============================================================
# HELPERS
# ============================================================

def vietnamese_to_ascii(text):
    """Remove Vietnamese diacritics via Unicode NFKD decomposition."""
    nfkd = unicodedata.normalize('NFKD', text)
    ascii_text = ''
    for char in nfkd:
        if char == '\u0111':
            ascii_text += 'd'
        elif char == '\u0110':
            ascii_text += 'D'
        elif unicodedata.category(char) == 'Mn':
            continue
        else:
            ascii_text += char
    return ascii_text


def safe_slugify(text, max_length=200):
    """Tao slug ASCII-only."""
    ascii_text = vietnamese_to_ascii(text)
    slug = django_slugify(ascii_text)
    if not slug:
        slug = hashlib.md5(text.encode()).hexdigest()[:12]
    return slug[:max_length]


def extract_file_number(filename):
    """Extract the article number from filename like '1. TITLE.docx' or '20.TITLE.docx'."""
    match = re.match(r'^(\d+)[\.\s]', filename)
    if match:
        return int(match.group(1))
    return None


def get_run_formatting(run):
    """Get formatting info from a run."""
    is_bold = run.bold
    is_italic = run.italic
    is_underline = run.underline
    return is_bold, is_italic, is_underline


def paragraph_to_html(paragraph):
    """Convert a docx paragraph to HTML, preserving basic formatting."""
    if not paragraph.text.strip():
        return ""

    # Check paragraph style
    style_name = paragraph.style.name.lower() if paragraph.style else ""

    html_parts = []
    for run in paragraph.runs:
        text = run.text
        if not text:
            continue

        is_bold, is_italic, is_underline = get_run_formatting(run)

        if is_bold:
            text = f"<strong>{text}</strong>"
        if is_italic:
            text = f"<em>{text}</em>"
        if is_underline:
            text = f"<u>{text}</u>"

        html_parts.append(text)

    content = "".join(html_parts)
    if not content.strip():
        return ""

    # Determine tag based on style
    if "heading 1" in style_name or "title" in style_name:
        return f"<h2>{content}</h2>"
    elif "heading 2" in style_name:
        return f"<h3>{content}</h3>"
    elif "heading 3" in style_name:
        return f"<h4>{content}</h4>"
    elif "list" in style_name:
        return f"<li>{content}</li>"
    else:
        # Check if entire paragraph is bold - might be a heading
        all_bold = all(
            run.bold for run in paragraph.runs if run.text.strip()
        ) if paragraph.runs else False

        text_len = len(paragraph.text.strip())
        is_upper = paragraph.text.strip().isupper()

        if all_bold and text_len < 100 and is_upper:
            return f"<h3>{content}</h3>"
        elif all_bold and text_len < 120:
            return f"<h4>{content}</h4>"
        else:
            return f"<p>{content}</p>"


def parse_docx(filepath, slug_base):
    """
    Parse a .docx file and return:
    - title: string
    - subtitle: string (second heading/bold line)
    - content_html: full HTML content
    - images: list of (image_bytes, extension, filename)
    """
    doc = Document(filepath)

    title = ""
    subtitle = ""
    content_parts = []
    images = []
    image_index = 0
    seen_title = False
    seen_subtitle = False

    # Extract images from rels first
    image_rels = {}
    for rel_id, rel in doc.part.rels.items():
        if "image" in rel.reltype:
            image_rels[rel_id] = rel

    # Process paragraphs and inline images
    for paragraph in doc.paragraphs:
        # Check for inline images in the paragraph
        for run in paragraph.runs:
            if run._element.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}drawing'):
                drawing_elements = run._element.findall(
                    './/{http://schemas.openxmlformats.org/wordprocessingml/2006/main}drawing'
                )
                for drawing in drawing_elements:
                    # Try to find the blip (embedded image reference)
                    blips = drawing.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/main}blip')
                    for blip in blips:
                        embed = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                        if embed and embed in image_rels:
                            rel = image_rels[embed]
                            image_data = rel.target_part.blob
                            ct = rel.target_part.content_type
                            if 'jpeg' in ct or 'jpg' in ct:
                                ext = '.jpg'
                            elif 'png' in ct:
                                ext = '.png'
                            elif 'webp' in ct:
                                ext = '.webp'
                            elif 'gif' in ct:
                                ext = '.gif'
                            else:
                                ext = '.jpg'

                            image_index += 1
                            img_filename = f"{slug_base}-{image_index:02d}{ext}"
                            images.append((image_data, ext, img_filename))
                            content_parts.append(
                                f'<figure class="news-article-figure">'
                                f'<img src="/media/news/images/{img_filename}" '
                                f'alt="{title or "MIS"}" loading="lazy" class="news-article-image">'
                                f'</figure>'
                            )

        # Title extraction
        text = paragraph.text.strip()
        if not text:
            continue

        if not seen_title:
            title = text
            seen_title = True
            continue

        if not seen_subtitle:
            # Second non-empty paragraph is usually the subtitle
            subtitle = text
            seen_subtitle = True
            # Add subtitle as a lead paragraph in content
            content_parts.append(f'<p class="news-lead">{text}</p>')
            continue

        # Regular content
        html = paragraph_to_html(paragraph)
        if html:
            content_parts.append(html)

    # Post-process: wrap consecutive <li> tags in <ul>
    final_parts = []
    in_list = False
    for part in content_parts:
        if part.startswith('<li>'):
            if not in_list:
                final_parts.append('<ul>')
                in_list = True
            final_parts.append(part)
        else:
            if in_list:
                final_parts.append('</ul>')
                in_list = False
            final_parts.append(part)
    if in_list:
        final_parts.append('</ul>')

    content_html = "\n".join(final_parts)

    return {
        "title": title,
        "subtitle": subtitle,
        "content_html": content_html,
        "images": images,
    }


def save_image(image_data, filename, subfolder="news/images"):
    """Save image to media directory."""
    media_root = settings.MEDIA_ROOT
    target_dir = os.path.join(media_root, subfolder)
    os.makedirs(target_dir, exist_ok=True)

    filepath = os.path.join(target_dir, filename)
    with open(filepath, 'wb') as f:
        f.write(image_data)

    return os.path.join(subfolder, filename)


# ============================================================
# MAIN
# ============================================================

def find_docx_folder():
    """Find the 'Bài viết website' folder."""
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for d in os.listdir(base):
        full = os.path.join(base, d)
        if os.path.isdir(full) and "vi" in d.lower() and "website" in d.lower():
            return full
    return None


def run():
    print("=" * 70)
    print("  IMPORT BÀI VIẾT TỪ FILE DOCX")
    print("=" * 70)

    # ── Step 1: Find docx folder ──
    docx_folder = find_docx_folder()
    if not docx_folder:
        print("[X] Không tìm thấy thư mục 'Bài viết website'!")
        return

    print(f"\n[1] Thư mục source: {docx_folder}")

    import glob
    docx_files = sorted(glob.glob(os.path.join(docx_folder, "*.docx")))
    print(f"    Tìm thấy {len(docx_files)} file .docx")

    # ── Step 2: Archive all existing news ──
    print(f"\n[2] Archive bài viết cũ...")
    archived_count = News.all_objects.filter(is_archived=False).update(is_archived=True)
    print(f"    Đã archive {archived_count} bài viết cũ")

    # Unfeatured all old news
    News.all_objects.filter(is_archived=True).update(is_featured=False)

    # ── Step 3: Create new categories ──
    print(f"\n[3] Tạo danh mục mới...")
    categories = {}
    for cat_name, cat_slug in CATEGORY_SLUGS.items():
        cat, created = Category.objects.get_or_create(
            slug=cat_slug,
            defaults={"name": cat_name}
        )
        if created:
            print(f"    [NEW] {cat_name} ({cat_slug})")
        else:
            # Update name if category exists
            if cat.name != cat_name:
                cat.name = cat_name
                cat.save()
            print(f"    [OK]  {cat_name} ({cat_slug})")
        categories[cat_name] = cat

    # ── Step 4: Import each docx ──
    print(f"\n[4] Import bài viết từ docx...")
    success = 0
    failed = 0

    for fpath in docx_files:
        fname = os.path.basename(fpath)
        file_num = extract_file_number(fname)

        if file_num is None:
            print(f"\n  [!] Không xác định được số thứ tự: {fname}")
            failed += 1
            continue

        print(f"\n  [{file_num:02d}] {fname}")

        # Determine category
        cat_name = CATEGORY_MAP.get(file_num, "Sự kiện nhà trường")
        category = categories.get(cat_name)

        try:
            # Parse docx
            slug_base = safe_slugify(fname.replace('.docx', ''))
            # Remove leading number from slug
            slug_base = re.sub(r'^\d+-', '', slug_base)
            if not slug_base:
                slug_base = f"mis-article-{file_num}"

            parsed = parse_docx(fpath, slug_base)

            if not parsed["title"]:
                print(f"       [X] Không có tiêu đề!")
                failed += 1
                continue

            title = parsed["title"]
            slug = safe_slugify(title)

            # Check for slug collision
            if News.all_objects.filter(slug=slug).exists():
                slug = f"{slug}-{file_num}"

            print(f"       Tiêu đề: {title[:70]}")
            print(f"       Slug: {slug}")
            print(f"       Danh mục: {cat_name}")
            print(f"       Ảnh: {len(parsed['images'])}")

            # Save images
            for img_data, ext, img_filename in parsed["images"]:
                save_image(img_data, img_filename)

            # Generate excerpt from subtitle + first paragraph
            excerpt = parsed["subtitle"][:300] if parsed["subtitle"] else ""
            if not excerpt:
                # Extract from content
                text_parts = re.findall(r'<p[^>]*>(.*?)</p>', parsed["content_html"])
                clean_parts = [re.sub(r'<[^>]+>', '', p) for p in text_parts[:2]]
                excerpt = " ".join(clean_parts)[:300]

            # Determine if featured
            is_featured = file_num in FEATURED_ARTICLES

            # Create News object
            news = News(
                title=title,
                slug=slug,
                content=parsed["content_html"],
                excerpt=excerpt,
                category=category,
                is_featured=is_featured,
                is_archived=False,
            )

            # Set thumbnail (first image)
            if parsed["images"]:
                first_img_data, first_ext, first_fname = parsed["images"][0]
                thumb_filename = f"thumb-{slug_base}{first_ext}"
                content_file = ContentFile(first_img_data, name=thumb_filename)
                news.thumbnail.save(thumb_filename, content_file, save=False)

            news.save()
            status = "⭐ FEATURED" if is_featured else "✅ OK"
            print(f"       [{status}] Đã lưu thành công!")
            success += 1

        except Exception as e:
            print(f"       [X] Lỗi: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    # ── Results ──
    print("\n" + "=" * 70)
    print("  KẾT QUẢ IMPORT")
    print(f"  Thành công: {success}")
    print(f"  Thất bại:   {failed}")
    print(f"  Tổng News (active):   {News.objects.count()}")
    print(f"  Tổng News (archived): {News.all_objects.filter(is_archived=True).count()}")
    print(f"  Tổng Categories:      {Category.objects.count()}")
    print("=" * 70)

    # Show featured articles
    print("\n  📌 Bài viết nổi bật (featured):")
    for news in News.objects.filter(is_featured=True):
        print(f"     ⭐ {news.title}")

    # Show category breakdown
    print("\n  📂 Phân loại danh mục:")
    for cat in Category.objects.all():
        count = News.objects.filter(category=cat).count()
        if count > 0:
            print(f"     • {cat.name}: {count} bài")


if __name__ == "__main__":
    run()
