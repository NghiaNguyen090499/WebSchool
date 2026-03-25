from django import template


register = template.Library()


def _normalize_path(path):
    if not path:
        return ""
    normalized = path.strip()
    if not normalized.startswith("/"):
        return normalized
    return normalized.rstrip("/") or "/"


@register.simple_tag
def path_is_active(current_path, target_path, exact=False):
    """Return True if target_path matches current_path for active nav state."""
    if not current_path or not target_path:
        return False

    target_path = target_path.strip()
    if target_path.startswith(("http://", "https://", "mailto:", "tel:", "#")):
        return False

    current = _normalize_path(current_path)
    target = _normalize_path(target_path)
    if not current or not target:
        return False

    if exact:
        return current == target
    if current == target:
        return True
    if target == "/":
        return False
    return current.startswith(f"{target}/")
