# -*- coding: utf-8 -*-
"""
Render a.pdf into images and store them in AboutPdfDocument/AboutPdfPageImage.
Run with: python scripts/update_future_ai_pdf.py
"""
import os
import sys
from pathlib import Path

import django


def render_pdf_page_to_png_bytes(pdf_path: Path, page_index: int, zoom: float = 2.0) -> bytes:
    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError("PyMuPDF is required. Install with: pip install PyMuPDF") from exc

    with fitz.open(str(pdf_path)) as doc:
        if page_index < 0 or page_index >= doc.page_count:
            raise ValueError(f"PDF page index out of range: {page_index}")
        page = doc.load_page(page_index)
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
        return pix.tobytes("png")


def main() -> None:
    base_dir = Path(__file__).resolve().parent.parent
    pdf_path = base_dir / "a.pdf"
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    sys.path.insert(0, str(base_dir))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_website.settings")
    django.setup()

    from about.models import AboutPage, AboutPdfDocument, AboutPdfPageImage
    from django.core.files.base import ContentFile
    from django.core.files.storage import default_storage

    page, _ = AboutPage.objects.get_or_create(
        page_type="future_ai",
        defaults={
            "title": "Future With AI",
            "content": "",
        },
    )
    if not page.title:
        page.title = "Future With AI"
        page.save()

    document, _ = AboutPdfDocument.objects.get_or_create(
        page_type="future_ai",
        defaults={
            "title": page.title or "Future With AI",
            "subtitle": "",
        },
    )
    if not document.title:
        document.title = page.title or "Future With AI"

    pdf_storage_name = "about/pdfs/future-ai.pdf"
    if document.pdf_file and default_storage.exists(document.pdf_file.name):
        try:
            default_storage.delete(document.pdf_file.name)
        except PermissionError:
            pass
    document.pdf_file.save(pdf_storage_name, ContentFile(pdf_path.read_bytes()), save=False)
    document.save()

    for page_image in document.pages.all():
        if page_image.image:
            page_image.image.delete(save=False)
    document.pages.all().delete()

    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError("PyMuPDF is required. Install with: pip install PyMuPDF") from exc

    with fitz.open(str(pdf_path)) as pdf_doc:
        for page_index in range(pdf_doc.page_count):
            png_bytes = render_pdf_page_to_png_bytes(pdf_path, page_index, zoom=2.0)
            image_name = f"about/pdfs/pages/future-ai-page-{page_index + 1:02d}.png"
            page_image = AboutPdfPageImage(
                document=document,
                order=page_index,
                alt_text=f"Future With AI - page {page_index + 1}",
            )
            page_image.image.save(image_name, ContentFile(png_bytes), save=False)
            page_image.save()


if __name__ == "__main__":
    main()
