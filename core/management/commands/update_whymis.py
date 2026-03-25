import re
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.urls import reverse

from about.models import AboutPage, AboutSection


SOURCE_URL = "https://misvn.edu.vn/tai-sao-chon-mis/"


def _extract_content():
    req = Request(SOURCE_URL, headers={"User-Agent": "Mozilla/5.0"})
    html = urlopen(req).read().decode("utf-8", errors="ignore")
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find(class_="entry-content") or soup.find("article")
    if not content:
        return [], [], []

    paragraphs = []
    lists = []
    images = []

    for el in content.find_all(["p", "ul", "img"], recursive=True):
        if el.name == "p":
            text = el.get_text(" ", strip=True)
            if text:
                paragraphs.append(text)
        elif el.name == "ul":
            items = [
                li.get_text(" ", strip=True)
                for li in el.find_all("li")
                if li.get_text(strip=True)
            ]
            if items:
                lists.append(items)
        elif el.name == "img":
            src = el.get("src")
            if src:
                images.append(src)

    return paragraphs, lists, images


def _normalize_image_url(url):
    return re.sub(r"-\\d+x\\d+(?=\\.(?:jpg|jpeg|png|webp)$)", "", url, flags=re.I)


def _download_image(url):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urlopen(req).read()


def _safe_download(urls):
    for url in urls:
        try:
            return _download_image(url), url
        except Exception:
            continue
    return None, None


def _first_sentences(text, max_len=240):
    if len(text) <= max_len:
        return text
    parts = re.split(r"(?<=[.!?])\\s+", text)
    output = ""
    for part in parts:
        candidate = f"{output} {part}".strip()
        if len(candidate) > max_len and output:
            break
        output = candidate
    if not output:
        output = text[:max_len].rsplit(" ", 1)[0] + "..."
    return output


class Command(BaseCommand):
    help = "Update 'Tại sao chọn MIS?' page content and images from misvn.edu.vn."

    def handle(self, *args, **options):
        paragraphs, lists, images = _extract_content()
        if not paragraphs:
            self.stdout.write("No content found. Aborting.")
            return

        images = [_normalize_image_url(url) for url in images]

        page, _ = AboutPage.objects.get_or_create(
            page_type="whymis",
            defaults={"title": "Tại sao chọn MIS?"},
        )
        page.title = "Tại sao chọn MIS?"
        page.content = ""
        page.save()

        page.sections.all().delete()

        cta_primary = reverse("admissions:list")
        cta_secondary = reverse("contact:contact")

        hero = AboutSection.objects.create(
            page=page,
            order=0,
            layout="hero",
            background="gradient",
            eyebrow="Tại sao chọn MIS",
            title="Tại sao chọn MIS?",
            subtitle=_first_sentences(paragraphs[0]),
            cta_text="Đăng ký tư vấn",
            cta_url=cta_primary,
            cta_secondary_text="Đặt lịch tham quan",
            cta_secondary_url=cta_secondary,
        )

        intro_section = AboutSection.objects.create(
            page=page,
            order=1,
            layout="text_left",
            background="white",
            title="Tôn trọng khác biệt – Khơi mở tiềm năng",
            content=paragraphs[0],
        )

        philosophy_section = AboutSection.objects.create(
            page=page,
            order=2,
            layout="text_right",
            background="light",
            title="Triết lý giáo dục đa trí tuệ",
            content=paragraphs[1],
        )

        if lists:
            highlights = []
            for block in lists[:2]:
                highlights.extend(block)
            highlights_text = "\n".join([f"• {item}" for item in highlights])
        else:
            highlights_text = ""

        program_section = AboutSection.objects.create(
            page=page,
            order=3,
            layout="full_text",
            background="white",
            title="Nội dung chương trình cốt lõi",
            content=highlights_text,
        )

        if len(lists) >= 3:
            experiences_text = "\n".join([f"• {item}" for item in lists[2]])
        else:
            experiences_text = ""

        experience_section = AboutSection.objects.create(
            page=page,
            order=4,
            layout="text_left",
            background="light",
            title="Trải nghiệm – Nghệ thuật – Thể thao – Kỹ năng sống",
            content=experiences_text,
        )

        # Download and attach images in order: hero, intro, philosophy, experience
        image_targets = [
            (hero, images[3:4] or images[1:2] or images[:1]),
            (intro_section, images[1:2] or images[:1]),
            (philosophy_section, images[2:3] or images[:1]),
            (experience_section, images[:1]),
        ]

        for section, candidates in image_targets:
            if not candidates:
                continue
            url_candidates = [candidates[0]]
            normalized = _normalize_image_url(candidates[0])
            if normalized != candidates[0]:
                url_candidates.insert(0, normalized)
            data, used_url = _safe_download(url_candidates)
            if not data:
                continue
            filename = used_url.split("/")[-1].split("?")[0]
            section.image.save(filename, ContentFile(data), save=True)

        # Use hero image as page image fallback
        if hero.image and not page.image:
            page.image = hero.image
            page.save(update_fields=["image"])

        self.stdout.write("Updated 'whymis' page sections and images.")
