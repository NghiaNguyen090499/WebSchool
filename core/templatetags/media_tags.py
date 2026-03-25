from django import template

from core.models import MediaAsset

register = template.Library()


@register.simple_tag
def get_media(page=None, block=None, category=None, file_type=None, limit=None):
    qs = MediaAsset.objects.filter(is_approved=True)
    if page:
        qs = qs.filter(page_target=page)
    if block:
        qs = qs.filter(block_target=block)
    if category:
        qs = qs.filter(category=category)
    if file_type:
        qs = qs.filter(file_type=file_type)
    if limit:
        qs = qs[: int(limit)]
    return qs
