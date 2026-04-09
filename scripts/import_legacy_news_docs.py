from __future__ import annotations

import argparse
from datetime import datetime
import io
import os
import re
import sys
import unicodedata
import zipfile
from dataclasses import dataclass
from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_website.settings")
os.environ.setdefault("DEBUG", "False")

import django

django.setup()

from django.utils import timezone

from docx import Document

from news.models import Category, News
from portal.news_import import import_news_from_upload


sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
WEBSITE_SOURCE_DIR = REPO_ROOT / "Bài viết website"
APRIL_SOURCE_DIR = REPO_ROOT / "Bài viết Tháng 4"
APRIL_EXTRA_IMAGE_DIR = APRIL_SOURCE_DIR / "Ảnh HSG đăng thêm vào gương mặt"

WEBSITE_CATEGORY_MAP = {
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
WEBSITE_FEATURED = {3, 10, 25}

APRIL_CATEGORY_PREFIXES = [
    ("mis-ghi-dau-an-tai-ky-thi-hoc-gioi-khoi-10", "Gương mặt Misers", None),
    ("mis-innovation-day-2026", "Sự kiện nhà trường", None),
    ("mis-ky-ket-hop-tac-chien-luoc-voi-ismart-va-edulive", "Hợp tác quốc tế", None),
    ("mis-vinh-danh-hoc-sinh-le-khanh-hoa", "Gương mặt Misers", APRIL_EXTRA_IMAGE_DIR),
    ("misers-toa-sang-tai-cuoc-thi-hung-bien-tieng-anh-soundbites-2026", "Cuộc thi & Học thuật", None),
    ("trai-sang-tao-innovation", "Sự kiện nhà trường", None),
]


@dataclass(frozen=True)
class ImportTarget:
    batch: str
    path: Path
    category_name: str
    is_featured: bool = False
    extra_images_dir: Path | None = None


def clean_text(value: str) -> str:
    value = (value or "").replace("\xa0", " ")
    value = value.replace("\u2028", " ").replace("\u2029", " ")
    value = value.replace("\u200b", "")
    value = value.replace("\r", "\n")
    lines = [re.sub(r"\s+", " ", line).strip() for line in value.split("\n")]
    return "\n".join(line for line in lines if line)


def make_slug(value: str) -> str:
    value = clean_text(value)
    value = unicodedata.normalize("NFKC", value)
    value = value.replace("Đ", "D").replace("đ", "d")
    value = unicodedata.normalize("NFD", value)
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = re.sub(r"[^A-Za-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value)
    return value.strip("-").lower()


def extract_title(path: Path) -> str:
    document = Document(str(path))
    for paragraph in document.paragraphs:
        text = clean_text(paragraph.text)
        if text:
            return text
    return clean_text(path.stem)


def extract_number(filename: str) -> int | None:
    match = re.match(r"^\s*(\d+)\s*[\.\-]", filename)
    if match:
        return int(match.group(1))
    return None


def ensure_category(name: str) -> Category:
    category = Category.objects.filter(name=name).first()
    if category:
        return category
    return Category.objects.create(name=name)


def build_extra_images_zip(directory: Path | None) -> SimpleUploadedFile | None:
    if not directory or not directory.exists():
        return None

    payload = io.BytesIO()
    with zipfile.ZipFile(payload, "w", zipfile.ZIP_DEFLATED) as archive:
        for image_path in sorted(directory.iterdir()):
            if not image_path.is_file():
                continue
            if image_path.suffix.lower() not in ALLOWED_IMAGE_EXTENSIONS:
                continue
            archive.writestr(image_path.name, image_path.read_bytes())

    payload.seek(0)
    return SimpleUploadedFile("extra-images.zip", payload.getvalue(), content_type="application/zip")


def resolve_website_targets() -> list[ImportTarget]:
    targets: list[ImportTarget] = []
    for path in sorted(WEBSITE_SOURCE_DIR.glob("*.docx")):
        article_number = extract_number(path.name)
        if article_number is None:
            print(f"[SKIP] Không xác định được số bài từ tên file: {path.name}")
            continue
        category_name = WEBSITE_CATEGORY_MAP.get(article_number, "Tin tức")
        targets.append(
            ImportTarget(
                batch="website",
                path=path,
                category_name=category_name,
                is_featured=article_number in WEBSITE_FEATURED,
            )
        )
    return targets


def resolve_april_targets() -> list[ImportTarget]:
    targets: list[ImportTarget] = []
    for path in sorted(APRIL_SOURCE_DIR.glob("*.docx")):
        normalized = make_slug(path.stem)
        matched = False
        for prefix, category_name, extra_images_dir in APRIL_CATEGORY_PREFIXES:
            if normalized.startswith(prefix):
                targets.append(
                    ImportTarget(
                        batch="april",
                        path=path,
                        category_name=category_name,
                        extra_images_dir=extra_images_dir,
                    )
                )
                matched = True
                break
        if not matched:
            print(f"[SKIP] Chưa có mapping cho file tháng 4: {path.name}")
    return targets


def plan_targets(source_set: str) -> list[ImportTarget]:
    targets: list[ImportTarget] = []
    if source_set in {"all", "website"}:
        targets.extend(resolve_website_targets())
    if source_set in {"all", "april"}:
        targets.extend(resolve_april_targets())
    return targets


def preview_action(path: Path) -> tuple[str, str, str]:
    title = extract_title(path)
    slug = make_slug(title)
    existing = News.all_objects.filter(title=title).first()
    if not existing:
        existing = News.all_objects.filter(slug=slug).first()
    return ("update" if existing else "create", title, slug)


def import_target(target: ImportTarget) -> str:
    category = ensure_category(target.category_name)
    extra_images_zip = build_extra_images_zip(target.extra_images_dir)
    with target.path.open("rb") as source_file:
        result = import_news_from_upload(
            source_file,
            category=category,
            is_featured=target.is_featured,
            overwrite_existing=True,
            extra_images_zip=extra_images_zip,
        )
    created_at = timezone.make_aware(datetime.fromtimestamp(target.path.stat().st_mtime), timezone.get_current_timezone())
    News.all_objects.filter(pk=result.news.pk).update(created_at=created_at)
    return result.action


def run_import(source_set: str, dry_run: bool) -> int:
    targets = plan_targets(source_set)
    if not targets:
        print("Không tìm thấy file .docx phù hợp để import.")
        return 0

    print(f"Tìm thấy {len(targets)} file .docx trong batch `{source_set}`.")
    created = 0
    updated = 0

    for target in targets:
        action, title, slug = preview_action(target.path)
        extra = " + extra images" if target.extra_images_dir else ""
        print(f"[{action.upper()}] {target.batch}: {target.path.name}")
        print(f"  title: {title}")
        print(f"  slug: {slug}")
        print(f"  category: {target.category_name}{extra}")

        if dry_run:
            if action == "create":
                created += 1
            else:
                updated += 1
            continue

        final_action = import_target(target)
        if final_action == "create":
            created += 1
        else:
            updated += 1

    print(f"Hoàn tất: create={created}, update={updated}, total={len(targets)}")
    return len(targets)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import legacy MIS news docx files and preserve source Word documents.")
    parser.add_argument(
        "--source-set",
        choices=["all", "website", "april"],
        default="all",
        help="Chọn batch nguồn cần import.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Chỉ in kế hoạch import, không ghi DB/media.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_import(source_set=args.source_set, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
