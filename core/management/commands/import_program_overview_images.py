import os
import re
from urllib.parse import urlparse, urljoin

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from core.models import ProgramOverviewPage, ProgramOverviewImage

try:
    from bs4 import BeautifulSoup
except Exception:  # pragma: no cover - optional dependency
    BeautifulSoup = None


class Command(BaseCommand):
    help = "Download ProgramOverview images into media/ and attach to models."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Redownload even if local images already exist.",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=0,
            help="Limit number of images per page (0 = all).",
        )
        parser.add_argument(
            "--pages",
            nargs="*",
            help="Optional list of page slugs to process.",
        )
        parser.add_argument(
            "--refresh",
            action="store_true",
            help="Refresh image_url list by crawling source_url before downloading.",
        )
        parser.add_argument(
            "--insecure",
            action="store_true",
            help="Disable SSL verification when downloading.",
        )
        parser.add_argument(
            "--timeout",
            type=int,
            default=25,
            help="Request timeout in seconds (default: 25).",
        )

    def _download(self, session, url, timeout, verify):
        response = session.get(url, timeout=timeout, verify=verify)
        response.raise_for_status()
        content_type = response.headers.get("content-type", "")
        if not content_type.startswith("image/"):
            return None, content_type
        return response.content, content_type

    def _guess_ext(self, url, content_type=""):
        path = urlparse(url).path
        ext = os.path.splitext(path)[1].lower()
        if ext in {".jpg", ".jpeg", ".png", ".webp"}:
            return ext
        if "png" in content_type:
            return ".png"
        if "webp" in content_type:
            return ".webp"
        return ".jpg"

    def _normalize_url(self, base_url, raw_url):
        if not raw_url:
            return None
        raw_url = raw_url.strip()
        if raw_url.startswith("//"):
            return f"https:{raw_url}"
        if raw_url.startswith("http://") or raw_url.startswith("https://"):
            return raw_url
        return urljoin(base_url, raw_url)

    def _extract_src_from_srcset(self, srcset):
        if not srcset:
            return None
        first = srcset.split(",")[0].strip()
        return first.split(" ")[0].strip() if first else None

    def _is_candidate_image(self, url):
        if not url:
            return False
        lower = url.lower()
        if "/wp-content/uploads/" in lower or "/uploads/" in lower:
            if lower.endswith(".svg"):
                return False
            return True
        return False

    def _discover_image_urls(self, session, page):
        if not page.source_url:
            return []
        response = session.get(page.source_url, timeout=25, verify=self._verify)
        response.raise_for_status()
        html = response.text

        candidates = []
        if BeautifulSoup:
            soup = BeautifulSoup(html, "html.parser")
            for tag in soup.find_all(["img", "source"]):
                raw_urls = []
                for attr in ("data-src", "data-lazy-src", "data-original", "src"):
                    value = tag.get(attr)
                    if value:
                        raw_urls.append(value)
                srcset = tag.get("data-srcset") or tag.get("srcset")
                src_from_set = self._extract_src_from_srcset(srcset)
                if src_from_set:
                    raw_urls.append(src_from_set)

                for raw in raw_urls:
                    normalized = self._normalize_url(page.source_url, raw)
                    if normalized:
                        candidates.append(normalized)
        else:
            for match in re.findall(r'src=["\']([^"\']+)["\']', html, flags=re.IGNORECASE):
                normalized = self._normalize_url(page.source_url, match)
                if normalized:
                    candidates.append(normalized)

        # Keep order, unique, and filter to uploads only
        seen = set()
        ordered = []
        for url in candidates:
            if url in seen:
                continue
            if not self._is_candidate_image(url):
                continue
            seen.add(url)
            ordered.append(url)
        return ordered

    def handle(self, *args, **options):
        queryset = ProgramOverviewPage.objects.prefetch_related("images").order_by("order", "title")
        slugs = options.get("pages") or []
        if slugs:
            queryset = queryset.filter(slug__in=slugs)

        force = options.get("force")
        limit = options.get("limit", 0)
        refresh = options.get("refresh")
        timeout = options.get("timeout", 25)
        insecure = options.get("insecure")

        self._verify = not insecure
        if insecure:
            try:
                import urllib3
                from urllib3.exceptions import InsecureRequestWarning
                urllib3.disable_warnings(InsecureRequestWarning)
            except Exception:
                pass

        session = requests.Session()
        session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "https://misvn.edu.vn/",
            }
        )

        total_downloaded = 0

        for page in queryset:
            self.stdout.write(self.style.MIGRATE_HEADING(f"Processing: {page.title}"))

            if refresh:
                try:
                    discovered = self._discover_image_urls(session, page)
                    if discovered:
                        page.hero_image_url = discovered[0]
                        page.save(update_fields=["hero_image_url"])
                        ProgramOverviewImage.objects.filter(page=page).delete()
                        ProgramOverviewImage.objects.bulk_create(
                            [
                                ProgramOverviewImage(
                                    page=page,
                                    image_url=image_url,
                                    alt_text=f"{page.title} - {order + 1}",
                                    order=order,
                                )
                                for order, image_url in enumerate(discovered)
                            ]
                        )
                        self.stdout.write(self.style.SUCCESS(f"  ✓ Refreshed {len(discovered)} image URLs"))
                    else:
                        self.stdout.write(self.style.WARNING("  ! No images discovered from source_url"))
                except Exception as exc:
                    self.stdout.write(self.style.WARNING(f"  ! Refresh failed: {exc}"))

            if page.hero_image_url and (force or not page.hero_image):
                try:
                    content, content_type = self._download(
                        session, page.hero_image_url, timeout, self._verify
                    )
                    if content:
                        ext = self._guess_ext(page.hero_image_url, content_type)
                        filename = f"{page.slug}-hero{ext}"
                        page.hero_image.save(filename, ContentFile(content), save=False)
                        page.save(update_fields=["hero_image"])
                        total_downloaded += 1
                        self.stdout.write(self.style.SUCCESS("  ✓ Hero image saved"))
                except Exception as exc:
                    self.stdout.write(self.style.WARNING(f"  ! Hero image failed: {exc}"))

            images = list(page.images.all().order_by("order"))
            if limit and limit > 0:
                images = images[:limit]

            for image in images:
                if not image.image_url:
                    continue
                if image.image and not force:
                    continue
                try:
                    content, content_type = self._download(
                        session, image.image_url, timeout, self._verify
                    )
                    if not content:
                        continue
                    ext = self._guess_ext(image.image_url, content_type)
                    filename = f"{page.slug}-{image.order + 1}{ext}"
                    image.image.save(filename, ContentFile(content), save=False)
                    image.save(update_fields=["image"])
                    total_downloaded += 1
                except Exception as exc:
                    self.stdout.write(self.style.WARNING(f"  ! Image {image.order + 1} failed: {exc}"))

        self.stdout.write(self.style.SUCCESS(f"Done. Downloaded {total_downloaded} images."))
