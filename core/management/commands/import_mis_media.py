import csv
import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from core.models import MediaAsset
from core.utils.media_import import (
    build_tags,
    choose_preset,
    compute_checksum,
    copy_or_move_file,
    detect_file_type,
    detect_people_flags,
    derive_category,
    extract_video_poster,
    heuristic_map_for_path,
    humanize_filename,
    load_media_map,
    make_slug,
    match_map_entry,
    media_root,
    process_image,
    probe_duration,
    to_media_relative,
)


class Command(BaseCommand):
    help = "Import MIS media from a local folder into MediaAsset records"

    def add_arguments(self, parser):
        parser.add_argument("--source", required=True, help="Source directory path")
        parser.add_argument("--map", dest="map_file", help="Media map file (CSV/JSON/YAML)")
        parser.add_argument("--dry-run", action="store_true", help="No DB or file writes")
        parser.add_argument("--commit", action="store_true", help="Write DB and files")
        parser.add_argument("--move", action="store_true", help="Move source files to MEDIA_ROOT")
        parser.add_argument("--copy", action="store_true", help="Copy source files to MEDIA_ROOT")
        parser.add_argument("--reset-unmapped", action="store_true", help="Reset duplicates to unmapped")
        parser.add_argument("--only-images", action="store_true", help="Only process images")
        parser.add_argument("--only-videos", action="store_true", help="Only process videos")
        parser.add_argument("--approve", action="store_true", help="Auto-approve safe assets")

    def handle(self, *args, **options):
        source_dir = Path(options["source"]).expanduser()
        if not source_dir.exists() or not source_dir.is_dir():
            raise CommandError(f"Source directory not found: {source_dir}")

        if options["move"] and options["copy"]:
            raise CommandError("Use only one of --move or --copy")
        if options["only_images"] and options["only_videos"]:
            raise CommandError("Use only one of --only-images or --only-videos")

        dry_run = options["dry_run"] or not options["commit"]
        move_files = options["move"]

        map_entries = load_media_map(Path(options["map_file"])) if options["map_file"] else []

        report_rows = []
        imported = skipped = duplicates = errors = 0

        for path in sorted(source_dir.rglob("*")):
            if not path.is_file():
                continue

            rel_path = path.relative_to(source_dir)
            file_type = detect_file_type(path)

            if file_type == "other":
                skipped += 1
                report_rows.append(self._report_row(rel_path, "skipped", file_type, message="unsupported"))
                continue
            if options["only_images"] and file_type != "image":
                skipped += 1
                report_rows.append(self._report_row(rel_path, "skipped", file_type, message="only_images"))
                continue
            if options["only_videos"] and file_type != "video":
                skipped += 1
                report_rows.append(self._report_row(rel_path, "skipped", file_type, message="only_videos"))
                continue

            try:
                checksum = compute_checksum(path)
                file_size = path.stat().st_size

                existing = MediaAsset.objects.filter(checksum=checksum, file_size=file_size).first()
                map_entry = match_map_entry(rel_path, map_entries) if map_entries else None
                if not map_entry:
                    map_entry = heuristic_map_for_path(rel_path)

                page_target = map_entry.page_template if map_entry else ""
                block_target = map_entry.block_key if map_entry else ""
                purpose = map_entry.purpose if map_entry else ""
                notes = map_entry.notes if map_entry else ""
                category = (map_entry.category if map_entry else "") or derive_category(page_target)
                category = (category or "unmapped").lower()
                preset = (map_entry.preset if map_entry else "") or choose_preset(block_target)
                preset = preset.upper() if preset else "THUMB"
                caption = map_entry.caption if map_entry else ""
                alt_text = map_entry.alt_text if map_entry else ""

                contains_student, contains_parent = detect_people_flags(rel_path, block_target, purpose)
                needs_consent = contains_student or contains_parent
                is_approved = bool(options["approve"] and not needs_consent)
                usage_status = "approved" if is_approved else "pending"
                tags = build_tags(category, purpose, contains_student, contains_parent)

                if not alt_text:
                    alt_text = caption or humanize_filename(path)

                if existing:
                    duplicates += 1
                    if options["reset_unmapped"] and not map_entry and options["commit"]:
                        existing.category = "unmapped"
                        existing.page_target = ""
                        existing.block_target = ""
                        existing.tags = []
                        existing.save(update_fields=["category", "page_target", "block_target", "tags"])
                    report_rows.append(
                        self._report_row(
                            rel_path,
                            "duplicate",
                            file_type,
                            category=category,
                            page_target=page_target,
                            block_target=block_target,
                            needs_consent=needs_consent,
                            is_approved=is_approved,
                            message="checksum_duplicate",
                        )
                    )
                    continue

                slug = make_slug(path.stem, checksum)
                dest_dir = media_root() / "mis" / "2026" / category

                primary_path = None
                webp_path = None
                jpeg_path = None
                poster_path = None
                width = None
                height = None
                duration = None
                file_action = ""

                if file_type == "image":
                    original_dest = dest_dir / f"{slug}_orig{path.suffix.lower()}"
                    image_result = process_image(path, dest_dir, slug, preset, dry_run)
                    file_action = copy_or_move_file(path, original_dest, move_files, dry_run)
                    webp_path = image_result["webp_path"]
                    jpeg_path = image_result["jpeg_path"]
                    width = image_result["width"]
                    height = image_result["height"]
                    primary_path = original_dest
                elif file_type == "video":
                    primary_path = dest_dir / f"{slug}{path.suffix.lower()}"
                    file_action = copy_or_move_file(path, primary_path, move_files, dry_run)
                    poster_path = extract_video_poster(path, dest_dir / f"{slug}_poster.jpg", dry_run)
                    duration = probe_duration(path)
                else:
                    primary_path = dest_dir / f"{slug}{path.suffix.lower()}"
                    file_action = copy_or_move_file(path, primary_path, move_files, dry_run)

                if dry_run:
                    imported += 1
                    report_rows.append(
                        self._report_row(
                            rel_path,
                            "dry_run",
                            file_type,
                            category=category,
                            page_target=page_target,
                            block_target=block_target,
                            primary_path=primary_path,
                            webp_path=webp_path,
                            jpeg_path=jpeg_path,
                            poster_path=poster_path,
                            needs_consent=needs_consent,
                            is_approved=is_approved,
                            message=file_action,
                        )
                    )
                    continue

                with transaction.atomic():
                    asset = MediaAsset(
                        file_type=file_type,
                        original_name=path.name,
                        slug=slug,
                        category=category,
                        tags=tags,
                        page_target=page_target,
                        block_target=block_target,
                        caption=caption,
                        alt_text=alt_text,
                        notes=notes,
                        width=width,
                        height=height,
                        duration=duration,
                        is_approved=is_approved,
                        needs_consent=needs_consent,
                        contains_student=contains_student,
                        contains_parent=contains_parent,
                        source="drive_2026",
                        usage_rights_status=usage_status,
                        checksum=checksum,
                        file_size=file_size,
                    )
                    if primary_path:
                        asset.file.name = to_media_relative(primary_path)
                    if webp_path:
                        asset.file_webp.name = to_media_relative(webp_path)
                    if jpeg_path:
                        asset.file_jpeg.name = to_media_relative(jpeg_path)
                    if poster_path:
                        asset.poster.name = to_media_relative(poster_path)

                    asset.save()

                imported += 1
                report_rows.append(
                    self._report_row(
                        rel_path,
                        "imported",
                        file_type,
                        category=category,
                        page_target=page_target,
                        block_target=block_target,
                        primary_path=primary_path,
                        webp_path=webp_path,
                        jpeg_path=jpeg_path,
                        poster_path=poster_path,
                        needs_consent=needs_consent,
                        is_approved=is_approved,
                        db_id=asset.id,
                        message=file_action,
                    )
                )
            except Exception as exc:
                errors += 1
                report_rows.append(
                    self._report_row(
                        rel_path,
                        "error",
                        file_type,
                        message=str(exc),
                    )
                )

        report_dir = Path.cwd()
        json_path = report_dir / "import_report.json"
        csv_path = report_dir / "import_report.csv"
        self._write_reports(report_rows, json_path, csv_path)

        self.stdout.write(self.style.SUCCESS(f"Imported: {imported}"))
        self.stdout.write(self.style.WARNING(f"Skipped: {skipped}"))
        self.stdout.write(self.style.WARNING(f"Duplicates: {duplicates}"))
        self.stdout.write(self.style.ERROR(f"Errors: {errors}"))
        self.stdout.write(f"Report JSON: {json_path}")
        self.stdout.write(f"Report CSV: {csv_path}")
        if dry_run:
            self.stdout.write(self.style.WARNING("Dry-run mode: no DB/files were written"))

    def _report_row(
        self,
        rel_path: Path,
        action: str,
        file_type: str,
        category: str = "",
        page_target: str = "",
        block_target: str = "",
        primary_path: Path | None = None,
        webp_path: Path | None = None,
        jpeg_path: Path | None = None,
        poster_path: Path | None = None,
        needs_consent: bool | None = None,
        is_approved: bool | None = None,
        db_id: int | None = None,
        message: str = "",
    ) -> dict:
        return {
            "source_path": rel_path.as_posix(),
            "action": action,
            "file_type": file_type,
            "category": category,
            "page_target": page_target,
            "block_target": block_target,
            "primary_path": to_media_relative(primary_path) if primary_path else "",
            "webp_path": to_media_relative(webp_path) if webp_path else "",
            "jpeg_path": to_media_relative(jpeg_path) if jpeg_path else "",
            "poster_path": to_media_relative(poster_path) if poster_path else "",
            "needs_consent": needs_consent,
            "is_approved": is_approved,
            "db_id": db_id,
            "message": message,
        }

    def _write_reports(self, rows: list[dict], json_path: Path, csv_path: Path) -> None:
        json_path.write_text(json.dumps(rows, indent=2, ensure_ascii=True), encoding="utf-8")

        fieldnames = [
            "source_path",
            "action",
            "file_type",
            "category",
            "page_target",
            "block_target",
            "primary_path",
            "webp_path",
            "jpeg_path",
            "poster_path",
            "needs_consent",
            "is_approved",
            "db_id",
            "message",
        ]
        with csv_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
