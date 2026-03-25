import json
import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

STAT_PATTERN = re.compile(r"^\s*([0-9]+(?:[.,][0-9]+)?(?:\+|%)?)\s*(.*)$")
FEATURE_SEPARATORS = (" - ", " – ", ": ", " | ")


def _normalize_line(text):
    value = str(text or "").strip()
    if not value:
        return ""
    value = value.lstrip("•").lstrip("-").strip()
    return value


def _split_feature_text(text):
    clean = _normalize_line(text)
    if not clean:
        return "", ""
    for sep in FEATURE_SEPARATORS:
        if sep in clean:
            title, body = clean.split(sep, 1)
            return title.strip(), body.strip()
    return clean, ""


@register.filter
def split_lines(value):
    if not value:
        return []
    output = []
    for line in str(value).splitlines():
        cleaned = _normalize_line(line)
        if cleaned:
            output.append(cleaned)
    return output


@register.filter
def stat_number(value):
    text = str(value or "").strip()
    if not text:
        return ""
    match = STAT_PATTERN.match(text)
    if match:
        return match.group(1)
    return text.split(" ", 1)[0]


@register.filter
def stat_label(value):
    text = str(value or "").strip()
    if not text:
        return ""
    match = STAT_PATTERN.match(text)
    if match:
        label = match.group(2).strip()
        return label or text
    parts = text.split(" ", 1)
    if len(parts) == 2:
        return parts[1].strip()
    return text


@register.filter
def feature_title(value):
    title, _ = _split_feature_text(value)
    return title


@register.filter
def feature_body(value):
    _, body = _split_feature_text(value)
    return body


@register.filter
def feature_image_for(section, index):
    if not section:
        return None
    try:
        position = int(index)
    except (TypeError, ValueError):
        return None
    if position < 1:
        return None

    image_fields = [
        getattr(section, "feature_image_1", None),
        getattr(section, "feature_image_2", None),
        getattr(section, "feature_image_3", None),
        getattr(section, "feature_image_4", None),
        getattr(section, "feature_image_5", None),
        getattr(section, "feature_image_6", None),
    ]
    images = [image for image in image_fields if image]
    if not images:
        return None

    return images[(position - 1) % len(images)]


@register.filter
def feature_details_json(section):
    """Return JSON array of feature detail objects for modal display."""
    if not section or not hasattr(section, "content") or not section.content:
        return mark_safe("[]")
    try:
        data = json.loads(section.content)
        if isinstance(data, list):
            return mark_safe(json.dumps(data, ensure_ascii=False))
    except (TypeError, ValueError, json.JSONDecodeError):
        pass
    return mark_safe("[]")
