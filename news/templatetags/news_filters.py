import re
from django import template
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='clean_excerpt')
def clean_excerpt(value):
    """Remove social share junk and HTML from excerpt text."""
    if not value:
        return ""
    # Strip HTML tags first
    text = strip_tags(value)
    # Remove "Share on Facebook", "Share on Twitter" etc.
    text = re.sub(r'Share on (Facebook|Twitter|LinkedIn|Pinterest|Email)\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(Share|Tweet)\b\s*', '', text)
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


@register.filter(name='strip_first_image')
def strip_first_image(value):
    """Remove the first <figure> or standalone <img> from content HTML.

    This avoids showing a duplicate image when the detail template
    already renders the thumbnail as a featured image above the content.
    """
    if not value:
        return ""
    # Try removing the first <figure>...</figure> block
    result, count = re.subn(
        r'<figure[^>]*>.*?</figure>\s*',
        '',
        value,
        count=1,
        flags=re.DOTALL,
    )
    if count:
        return mark_safe(result)
    # Fallback: remove the first standalone <img> tag
    result, count = re.subn(
        r'<img[^>]*>\s*',
        '',
        value,
        count=1,
    )
    if count:
        return mark_safe(result)
    return value

