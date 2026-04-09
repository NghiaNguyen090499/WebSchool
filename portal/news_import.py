from __future__ import annotations

import hashlib
import re
import unicodedata
from dataclasses import dataclass
from html import escape
from io import BytesIO
from pathlib import Path
from zipfile import BadZipFile, ZipFile

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.utils import timezone
from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

from news.models import News


NS_A = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
URL_RE = re.compile(r"(https?://[^\s<]+)")
ALLOWED_EXTRA_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


@dataclass
class ImportedNewsResult:
    news: News
    action: str
    image_count: int


def import_news_from_upload(
    source_file,
    *,
    category,
    is_featured=False,
    overwrite_existing=True,
    title_override="",
    extra_images_zip=None,
):
    document = _open_docx(source_file)
    title = _extract_title(document, fallback_name=getattr(source_file, "name", "news.docx"))
    if title_override.strip():
        title = _clean_text(title_override)
    slug = _make_slug(title)
    if not slug:
        raise ValidationError("Không thể tạo slug từ tiêu đề bài viết.")

    existing = News.all_objects.filter(title=title).first()
    if not existing:
        existing = News.all_objects.filter(slug=slug).first()
    if existing and not overwrite_existing:
        raise ValidationError("Bài viết đã tồn tại. Bật ghi đè để cập nhật bài hiện có.")

    media_dir = "news/imported/{month}/{slug}".format(
        month=timezone.localtime(timezone.now()).strftime("%Y-%m"),
        slug=slug[:80],
    )
    content, image_paths = _build_content(document, title=title, media_dir=media_dir)
    if extra_images_zip:
        extra_image_paths = _save_zip_images(
            extra_images_zip,
            media_dir=media_dir,
            start_index=len(image_paths) + 1,
        )
        image_paths.extend(extra_image_paths)
        content = _append_images_to_content(content, extra_image_paths, title)

    if not content.strip():
        raise ValidationError("Không trích xuất được nội dung từ file .docx.")

    excerpt = _build_excerpt(content)
    action = "update" if existing else "create"
    news = existing or News()
    news.title = title
    news.slug = slug
    news.content = content
    news.excerpt = excerpt
    news.category = category
    news.is_featured = bool(is_featured)
    news.is_archived = False
    if image_paths:
        news.thumbnail.name = image_paths[0]
    news.save()
    _assign_source_document(news, source_file, slug=slug)
    if news.source_document:
        news.save(update_fields=["source_document"])

    return ImportedNewsResult(news=news, action=action, image_count=len(image_paths))


def _open_docx(uploaded_file):
    try:
        if hasattr(uploaded_file, "seek"):
            uploaded_file.seek(0)
        payload = uploaded_file.read()
        if hasattr(uploaded_file, "seek"):
            uploaded_file.seek(0)
        return Document(BytesIO(payload))
    except Exception as exc:
        raise ValidationError("Không đọc được file .docx. Vui lòng kiểm tra lại tệp nguồn.") from exc


def _extract_title(document, fallback_name):
    for paragraph in document.paragraphs:
        text = _clean_text(paragraph.text)
        if text:
            return text
    return _clean_text(Path(fallback_name).stem)


def _iter_block_items(document):
    parent = document.element.body
    for child in parent.iterchildren():
        if child.tag == qn("w:p"):
            yield Paragraph(child, document)
        elif child.tag == qn("w:tbl"):
            yield Table(child, document)


def _paragraph_lines(paragraph):
    text = _clean_text(paragraph.text)
    if not text:
        return []
    return [line for line in text.split("\n") if line]


def _paragraph_images(paragraph, document):
    images = []
    seen_ids = set()
    for run in paragraph.runs:
        for blip in run.element.findall(".//a:blip", namespaces=NS_A):
            embed_id = blip.get(qn("r:embed"))
            if not embed_id or embed_id in seen_ids:
                continue
            part = document.part.related_parts.get(embed_id)
            if not part:
                continue
            content_type = getattr(part, "content_type", "")
            if not content_type.startswith("image/"):
                continue
            ext = content_type.split("/")[-1].replace("jpeg", "jpg")
            images.append((ext, part.blob))
            seen_ids.add(embed_id)
    return images


def _build_content(document, *, title, media_dir):
    body_lines = []
    image_paths = []
    seen_hashes = set()
    image_counter = 1
    skip_first_title = True

    for block in _iter_block_items(document):
        if isinstance(block, Table):
            continue

        lines = _paragraph_lines(block)
        if lines:
            if skip_first_title and lines[0] == title:
                lines = lines[1:]
                skip_first_title = False
            else:
                skip_first_title = False
            body_lines.extend(lines)

        for ext, payload in _paragraph_images(block, document):
            payload_hash = hashlib.sha1(payload).hexdigest()
            if payload_hash in seen_hashes:
                continue
            relative_path = _write_media(
                "{media_dir}/image_{index:02d}.{ext}".format(
                    media_dir=media_dir,
                    index=image_counter,
                    ext=ext,
                ),
                payload,
            )
            image_paths.append(relative_path)
            seen_hashes.add(payload_hash)
            image_counter += 1

    html_blocks = _render_text_blocks(body_lines)
    html_blocks.extend(_image_blocks(image_paths, title))
    return "\n".join(html_blocks), image_paths


def _save_zip_images(uploaded_zip, *, media_dir, start_index):
    try:
        if hasattr(uploaded_zip, "seek"):
            uploaded_zip.seek(0)
        archive = ZipFile(uploaded_zip)
    except BadZipFile as exc:
        raise ValidationError("File ảnh phụ phải là .zip hợp lệ.") from exc

    image_paths = []
    try:
        index = start_index
        for info in archive.infolist():
            if info.is_dir():
                continue
            filename = Path(info.filename).name
            if not filename:
                continue
            ext = Path(filename).suffix.lower()
            if ext not in ALLOWED_EXTRA_IMAGE_EXTENSIONS:
                continue
            payload = archive.read(info.filename)
            if not payload:
                continue
            image_paths.append(
                _write_media(
                    "{media_dir}/image_{index:02d}{ext}".format(
                        media_dir=media_dir,
                        index=index,
                        ext=ext,
                    ),
                    payload,
                )
            )
            index += 1
    finally:
        archive.close()
        if hasattr(uploaded_zip, "seek"):
            uploaded_zip.seek(0)

    return image_paths

def _append_images_to_content(content, image_paths, title):
    if not image_paths:
        return content
    blocks = [content] if content else []
    blocks.extend(_image_blocks(image_paths, title))
    return "\n".join(blocks)


def _image_blocks(image_paths, title):
    return [
        '<figure><img src="{src}" alt="{alt}"></figure>'.format(
            src=_html_url(path),
            alt=escape(title, quote=True),
        )
        for path in image_paths
    ]


def _write_media(relative_path, payload):
    normalized = relative_path.replace("\\", "/")
    absolute_path = Path(settings.MEDIA_ROOT) / Path(normalized)
    absolute_path.parent.mkdir(parents=True, exist_ok=True)
    absolute_path.write_bytes(payload)
    return normalized


def _html_url(relative_media_path):
    media_url = settings.MEDIA_URL.rstrip("/")
    return "{}/{}".format(media_url, relative_media_path).replace("//", "/").replace(":/", "://")


def _assign_source_document(news, uploaded_file, *, slug):
    payload = _read_uploaded_payload(uploaded_file)
    if not payload:
        return

    ext = Path(getattr(uploaded_file, "name", "")).suffix.lower() or ".docx"
    relative_path = "{month}/{slug}{ext}".format(
        month=timezone.localtime(timezone.now()).strftime("%Y-%m"),
        slug=slug[:120],
        ext=ext,
    )

    if news.source_document:
        news.source_document.delete(save=False)
    news.source_document.save(relative_path, ContentFile(payload), save=False)


def _read_uploaded_payload(uploaded_file):
    if not uploaded_file:
        return b""
    if hasattr(uploaded_file, "seek"):
        uploaded_file.seek(0)
    payload = uploaded_file.read()
    if hasattr(uploaded_file, "seek"):
        uploaded_file.seek(0)
    return payload


def _build_excerpt(content):
    text = re.sub(r"<[^>]+>", " ", content or "")
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= 300:
        return text
    return "{}...".format(text[:297].rstrip())


def _render_text_blocks(lines):
    blocks = []
    index = 0
    while index < len(lines):
        current = lines[index]
        next_lines = lines[index + 1 :]
        if current.endswith(":"):
            list_items = []
            for item in next_lines:
                if _looks_like_short_item(item):
                    list_items.append(item)
                else:
                    break
            if list_items:
                blocks.append("<p><strong>{}</strong></p>".format(_linkify_text(current)))
                blocks.append(
                    "<ul>{}</ul>".format(
                        "".join("<li>{}</li>".format(_linkify_text(item)) for item in list_items)
                    )
                )
                index += 1 + len(list_items)
                continue
        blocks.append("<p>{}</p>".format(_linkify_text(current)))
        index += 1
    return blocks


def _looks_like_short_item(text):
    if len(text) > 120:
        return False
    if re.search(r"\bGiải\b", text, flags=re.IGNORECASE):
        return True
    if " – " in text:
        return True
    if ":" in text and len(text) < 100:
        return True
    return text.endswith(".") and len(text) < 90


def _linkify_text(text):
    escaped = escape(text, quote=False)

    def replace(match):
        url = match.group(1)
        safe_url = escape(url, quote=True)
        label = escape(url, quote=False)
        return '<a href="{url}" target="_blank" rel="noopener">{label}</a>'.format(
            url=safe_url,
            label=label,
        )

    return URL_RE.sub(replace, escaped)


def _clean_text(value):
    value = (value or "").replace("\xa0", " ")
    value = value.replace("\u2028", " ").replace("\u2029", " ")
    value = value.replace("\u200b", "")
    value = value.replace("\r", "\n")
    lines = [re.sub(r"\s+", " ", line).strip() for line in value.split("\n")]
    return "\n".join(line for line in lines if line)


def _make_slug(value):
    value = _clean_text(value)
    value = unicodedata.normalize("NFKC", value)
    value = value.replace("Đ", "D").replace("đ", "d")
    value = unicodedata.normalize("NFD", value)
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = re.sub(r"[^A-Za-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value)
    return value.strip("-").lower()
