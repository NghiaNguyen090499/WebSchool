from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_website.settings")
os.environ["DEBUG"] = "False"

import django

django.setup()

from django.db.models import Q

from news.models import News
from news.word_export import export_news_to_source_document


sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")


def build_queryset(args: argparse.Namespace):
    queryset = News.all_objects.order_by("pk")

    if args.news_id is not None:
        queryset = queryset.filter(pk=args.news_id)

    if args.slug:
        queryset = queryset.filter(slug=args.slug)

    if not args.overwrite:
        queryset = queryset.filter(Q(source_document__isnull=True) | Q(source_document=""))

    if args.limit:
        queryset = queryset[: args.limit]

    return queryset


def run(args: argparse.Namespace) -> int:
    queryset = build_queryset(args)
    total = queryset.count()
    if total == 0:
        print("Khong co bai viet nao phu hop de tao file Word.")
        return 0

    print(f"Tim thay {total} bai viet can xu ly.")
    if args.dry_run:
        for news in queryset[: min(total, 20)]:
            print(f"[DRY-RUN] #{news.pk} {news.slug} -> {news.title}")
        if total > 20:
            print(f"... va {total - 20} bai viet khac.")
        return total

    created = 0
    replaced = 0
    skipped = 0
    failed = 0

    for index, news in enumerate(queryset.iterator(chunk_size=100), start=1):
        try:
            result = export_news_to_source_document(
                news,
                overwrite=args.overwrite,
                site_base_url=args.site_base_url,
            )
        except Exception as exc:  # pragma: no cover - CLI safety path.
            failed += 1
            print(f"[ERROR] #{news.pk} {news.slug}: {exc}")
            continue

        if result.action == "create":
            created += 1
        elif result.action == "replace":
            replaced += 1
        else:
            skipped += 1

        if index % 50 == 0 or index == total:
            print(
                f"Tien do {index}/{total} | create={created} replace={replaced} skip={skipped} error={failed}"
            )

    print(f"Hoan tat | create={created} replace={replaced} skip={skipped} error={failed} total={total}")
    return total


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate .docx source documents for News records and store them in source_document."
    )
    parser.add_argument("--news-id", type=int, help="Chi xu ly mot bai viet theo ID.")
    parser.add_argument("--slug", help="Chi xu ly mot bai viet theo slug.")
    parser.add_argument("--limit", type=int, help="Gioi han so bai viet xu ly.")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Ghi de file source_document dang co. Mac dinh chi tao cho bai chua co file Word.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Chi in danh sach bai viet se xu ly, khong ghi DB/media.",
    )
    parser.add_argument(
        "--site-base-url",
        default="https://misvn.edu.vn",
        help="Base URL de ghi vao metadata va danh sach anh trong file Word.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run(args)


if __name__ == "__main__":
    main()
