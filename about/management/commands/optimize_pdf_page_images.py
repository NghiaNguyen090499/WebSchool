from django.core.management.base import BaseCommand

from about.models import AboutPdfPageImage


class Command(BaseCommand):
    help = "Backfill width/height metadata and AVIF/WebP assets for About PDF page images."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Regenerate AVIF/WebP files even if they already exist.",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=0,
            help="Process only the first N records (0 means all).",
        )

    def handle(self, *args, **options):
        force = options["force"]
        limit = options["limit"]

        queryset = AboutPdfPageImage.objects.select_related("document").order_by("document_id", "order")
        if limit and limit > 0:
            queryset = queryset[:limit]

        total = queryset.count()
        self.stdout.write(f"Processing {total} PDF page image(s)...")

        updated_count = 0
        for page_image in queryset.iterator():
            changed = page_image.refresh_optimized_assets(force=force, save=True)
            if changed:
                updated_count += 1
                self.stdout.write(
                    f"UPDATED: {page_image.document.page_type} #{page_image.order}"
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Completed. Updated {updated_count}/{total} image record(s)."
            )
        )
