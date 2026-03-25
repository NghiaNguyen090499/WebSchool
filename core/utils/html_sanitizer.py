from html import escape
from html.parser import HTMLParser
import re
from typing import Iterable, Optional
from urllib.parse import urlparse


ALLOWED_TAGS = {
    "p",
    "br",
    "ul",
    "ol",
    "li",
    "strong",
    "em",
    "b",
    "i",
    "u",
    "a",
    "h2",
    "h3",
    "h4",
    "blockquote",
    "img",
    "table",
    "thead",
    "tbody",
    "tfoot",
    "tr",
    "th",
    "td",
    "span",
    "div",
    "figure",
    "figcaption",
}

VOID_TAGS = {"br", "img"}
BLOCKED_TAGS = {"script", "style", "iframe"}

GLOBAL_ATTRS = {"class"}
ALLOWED_ATTRS = {
    "a": {"href", "title", "target", "rel"},
    "img": {"src", "alt", "title", "width", "height"},
    "th": {"colspan", "rowspan", "scope"},
    "td": {"colspan", "rowspan"},
}

SAFE_URL_SCHEMES = {"", "http", "https", "mailto", "tel"}

HTML_TAG_RE = re.compile(r"<[a-z][\s\S]*?>", re.IGNORECASE)


def contains_html(value: Optional[str]) -> bool:
    if not value:
        return False
    return bool(HTML_TAG_RE.search(value))


def _is_safe_url(value: str) -> bool:
    if not value:
        return False
    lowered = value.strip().lower()
    if lowered.startswith(("javascript:", "data:", "vbscript:")):
        return False
    parsed = urlparse(value)
    return parsed.scheme in SAFE_URL_SCHEMES


class _HtmlSanitizer(HTMLParser):
    def __init__(self, allowed_tags: Iterable[str]) -> None:
        super().__init__()
        self.allowed_tags = set(allowed_tags)
        self.result: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in BLOCKED_TAGS:
            self._skip_depth += 1
            return
        if tag not in self.allowed_tags:
            return
        attr_allowed = set(ALLOWED_ATTRS.get(tag, set())) | GLOBAL_ATTRS
        cleaned_attrs = []
        for name, value in attrs:
            if not name:
                continue
            attr_name = name.lower()
            if attr_name not in attr_allowed:
                continue
            if attr_name in {"href", "src"} and (not value or not _is_safe_url(value)):
                continue
            if attr_name == "target" and value not in {"_blank", "_self", "_parent", "_top"}:
                continue
            cleaned_attrs.append(
                f' {attr_name}="{escape(value or "", quote=True)}"'
            )
        attrs_str = "".join(cleaned_attrs)
        self.result.append(f"<{tag}{attrs_str}>")

    def handle_startendtag(self, tag, attrs):
        tag = tag.lower()
        if tag in BLOCKED_TAGS or tag not in self.allowed_tags:
            return
        attr_allowed = set(ALLOWED_ATTRS.get(tag, set())) | GLOBAL_ATTRS
        cleaned_attrs = []
        for name, value in attrs:
            if not name:
                continue
            attr_name = name.lower()
            if attr_name not in attr_allowed:
                continue
            if attr_name in {"href", "src"} and (not value or not _is_safe_url(value)):
                continue
            cleaned_attrs.append(
                f' {attr_name}="{escape(value or "", quote=True)}"'
            )
        attrs_str = "".join(cleaned_attrs)
        self.result.append(f"<{tag}{attrs_str}>")

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in BLOCKED_TAGS and self._skip_depth > 0:
            self._skip_depth -= 1
            return
        if tag in self.allowed_tags and tag not in VOID_TAGS:
            self.result.append(f"</{tag}>")

    def handle_data(self, data):
        if self._skip_depth > 0:
            return
        self.result.append(escape(data))

    def handle_entityref(self, name):
        if self._skip_depth > 0:
            return
        self.result.append(f"&{name};")

    def handle_charref(self, name):
        if self._skip_depth > 0:
            return
        self.result.append(f"&#{name};")


def sanitize_html(value: Optional[str]) -> str:
    if not value:
        return ""
    sanitizer = _HtmlSanitizer(ALLOWED_TAGS)
    sanitizer.feed(value)
    sanitizer.close()
    return "".join(sanitizer.result)
