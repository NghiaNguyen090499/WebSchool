import json
from datetime import datetime
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db.utils import OperationalError, ProgrammingError
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime

from core.models import ProgramContentSource
from core.utils.program_content import (
    DEFAULT_PROGRAM_YEAR,
    _resolve_content_file,
    clear_program_content_cache,
)


class Command(BaseCommand):
    help = "Import program content JSON into ProgramContentSource (DB-first content source)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--year",
            type=str,
            help="Target program year (example: 2026-2027). Defaults to JSON program_year.",
        )
        parser.add_argument(
            "--file",
            type=str,
            help="Custom JSON file path. If omitted, loader resolves by --year/settings.",
        )
        parser.add_argument(
            "--activate",
            action="store_true",
            help="Mark imported record as active.",
        )
        parser.add_argument(
            "--exclusive",
            action="store_true",
            help="With --activate, deactivate all other ProgramContentSource records.",
        )

    def handle(self, *args, **options):
        source_path = self._resolve_source_path(options.get("file"), options.get("year"))
        payload = self._load_payload(source_path)

        payload_year = str(payload.get("program_year") or "").strip()
        year = (options.get("year") or payload_year or DEFAULT_PROGRAM_YEAR).strip()
        if not year:
            raise CommandError("Unable to determine target year.")

        approved_at = self._parse_approved_at(payload.get("approved_at"))

        defaults = {
            "content": payload,
            "source_doc": str(payload.get("source_doc") or source_path.stem),
            "version": str(payload.get("version") or "1.0"),
        }
        if approved_at:
            defaults["approved_at"] = approved_at
        if options.get("activate"):
            defaults["is_active"] = True

        try:
            record, created = ProgramContentSource.objects.update_or_create(
                year=year,
                defaults=defaults,
            )

            if options.get("activate") and options.get("exclusive"):
                ProgramContentSource.objects.exclude(pk=record.pk).update(is_active=False)
        except (OperationalError, ProgrammingError) as exc:
            raise CommandError(
                "Database is not ready for ProgramContentSource. "
                "Run migrations first (python manage.py migrate core)."
            ) from exc

        clear_program_content_cache()

        action = "Created" if created else "Updated"
        self.stdout.write(
            self.style.SUCCESS(
                f"{action} ProgramContentSource year={record.year} version={record.version} "
                f"active={record.is_active}"
            )
        )
        if source_path:
            self.stdout.write(f"Source: {source_path}")

    def _resolve_source_path(self, file_option, year_option):
        if file_option:
            path = Path(file_option)
            if not path.is_absolute():
                path = Path.cwd() / path
            path = path.resolve()
        else:
            path = _resolve_content_file(year_option)

        if not path or not Path(path).exists():
            raise CommandError("Program content JSON file not found.")
        return Path(path)

    def _load_payload(self, source_path):
        try:
            with source_path.open(encoding="utf-8") as handle:
                payload = json.load(handle)
        except (OSError, ValueError) as exc:
            raise CommandError(f"Invalid JSON file: {exc}") from exc

        if not isinstance(payload, dict):
            raise CommandError("JSON root must be an object.")
        return payload

    def _parse_approved_at(self, value):
        if not value:
            return None
        if isinstance(value, datetime):
            dt = value
        else:
            dt = parse_datetime(str(value))
            if not dt:
                date_value = parse_date(str(value))
                if not date_value:
                    return None
                dt = datetime.combine(date_value, datetime.min.time())

        if timezone.is_naive(dt):
            return timezone.make_aware(dt, timezone.get_current_timezone())
        return dt
