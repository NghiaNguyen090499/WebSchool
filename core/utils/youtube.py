from typing import Optional
from urllib.parse import parse_qs, urlparse


def _is_youtube_host(netloc: str) -> bool:
    if not netloc:
        return False
    host = netloc.lower()
    return host == "youtube.com" or host.endswith(".youtube.com")


def _is_youtu_be_host(netloc: str) -> bool:
    if not netloc:
        return False
    host = netloc.lower()
    return host == "youtu.be" or host.endswith(".youtu.be")


def extract_youtube_id(url: str) -> Optional[str]:
    if not url:
        return None

    parsed = urlparse(url)
    netloc = parsed.netloc

    if _is_youtu_be_host(netloc):
        video_id = parsed.path.lstrip("/").split("/")[0]
        return video_id or None

    if _is_youtube_host(netloc):
        if parsed.path == "/watch":
            return parse_qs(parsed.query).get("v", [None])[0]
        if parsed.path.startswith("/embed/"):
            parts = parsed.path.split("/")
            return parts[2] if len(parts) > 2 and parts[2] else None
        if parsed.path.startswith("/shorts/"):
            parts = parsed.path.split("/")
            return parts[2] if len(parts) > 2 and parts[2] else None

    return None
