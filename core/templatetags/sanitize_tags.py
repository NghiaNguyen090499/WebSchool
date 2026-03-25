from django import template

from core.utils.html_sanitizer import sanitize_html, contains_html


register = template.Library()


@register.filter(name="sanitize_html")
def sanitize_html_filter(value):
    return sanitize_html(value)


@register.filter(name="contains_html")
def contains_html_filter(value):
    return contains_html(value)
