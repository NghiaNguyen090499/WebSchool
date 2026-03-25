from __future__ import annotations

import csv
import fnmatch
import hashlib
import json
import logging
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

from django.conf import settings
from django.utils.text import slugify
from PIL import Image, ImageOps

logger = logging.getLogger(__name__)

SUPPORTED_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
SUPPORTED_VIDEO_EXTS = {".mp4", ".mov", ".webm", ".mkv", ".avi"}
SUPPORTED_DOC_EXTS = {".pdf", ".doc", ".docx"}

PRESETS = {
    "HERO_16_9": {"size": (1920, 1080), "webp_q": 78, "jpeg_q": 82, "crop": True},
    "PORTRAIT_4_5": {"size": (1200, 1500), "webp_q": 80, "jpeg_q": 82, "crop": True},
    "SQUARE_1_1": {"size": (1200, 1200), "webp_q": 80, "jpeg_q": 82, "crop": True},
    "THUMB": {"long_edge": 480, "webp_q": 78, "jpeg_q": 82, "crop": False},
}


@dataclass
class MediaMapEntry:
    pattern: str
    page_template: str = ""
    block_key: str = ""
    purpose: str = ""
    notes: str = ""
    preset: str = ""
    category: str = ""
    caption: str = ""
    alt_text: str = ""


def normalize_text(value: Optional[str]) -> str:
    if value is None:
        return ""
    return str(value).strip()


def build_map_entry(row: dict) -> Optional[MediaMapEntry]:
    pattern = normalize_text(
        row.get("file_name")
        or row.get("pattern")
        or row.get("file")
        or row.get("filename")
    )
    if not pattern:
        return None
    return MediaMapEntry(
        pattern=pattern,
        page_template=normalize_text(row.get("page_template") or row.get("page")),
        block_key=normalize_text(row.get("block_key") or row.get("block")),
        purpose=normalize_text(row.get("purpose")),
        notes=normalize_text(row.get("notes")),
        preset=normalize_text(row.get("preset")),
        category=normalize_text(row.get("category")),
        caption=normalize_text(row.get("caption")),
        alt_text=normalize_text(row.get("alt_text")),
    )


def load_media_map(map_path: Optional[Path]) -> list[MediaMapEntry]:
    if not map_path:
        return []
    if not map_path.exists():
        raise FileNotFoundError(f"Media map not found: {map_path}")

    suffix = map_path.suffix.lower()
    entries: list[MediaMapEntry] = []

    if suffix in {".json"}:
        data = json.loads(map_path.read_text(encoding="utf-8"))
        items = data.get("items", data) if isinstance(data, dict) else data
        if not isinstance(items, list):
            raise ValueError("JSON media map must be a list or {items: [...]} object")
        for row in items:
            if not isinstance(row, dict):
                continue
            entry = build_map_entry(row)
            if entry:
                entries.append(entry)
    elif suffix in {".yaml", ".yml"}:
        try:
            import yaml  # type: ignore
        except Exception as exc:
            raise RuntimeError("PyYAML is required to read YAML media map files") from exc
        data = yaml.safe_load(map_path.read_text(encoding="utf-8"))
        items = data.get("items", data) if isinstance(data, dict) else data
        if not isinstance(items, list):
            raise ValueError("YAML media map must be a list or {items: [...]} object")
        for row in items:
            if not isinstance(row, dict):
                continue
            entry = build_map_entry(row)
            if entry:
                entries.append(entry)
    elif suffix in {".csv"}:
        with map_path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                entry = build_map_entry(row)
                if entry:
                    entries.append(entry)
    else:
        raise ValueError("Unsupported media map format. Use CSV, JSON, or YAML.")

    return entries


def match_map_entry(rel_path: Path, entries: Iterable[MediaMapEntry]) -> Optional[MediaMapEntry]:
    rel_str = rel_path.as_posix().lower()
    base_name = rel_path.name.lower()
    for entry in entries:
        pattern = entry.pattern.lower()
        if fnmatch.fnmatch(rel_str, pattern) or fnmatch.fnmatch(base_name, pattern):
            return entry
    return None


def heuristic_map_for_path(rel_path: Path) -> Optional[MediaMapEntry]:
    name = rel_path.name.lower()
    parts = [p.lower() for p in rel_path.parts]

    if "cover" in name:
        return MediaMapEntry(
            pattern=rel_path.name,
            page_template="home.html",
            block_key="hero_video",
            purpose="branding",
            preset="HERO_16_9",
            category="home",
        )
    if "pvph" in name or "phhs" in name or "testimonials" in parts:
        return MediaMapEntry(
            pattern=rel_path.name,
            page_template="admission_list.html",
            block_key="testimonial_slider",
            purpose="admissions",
            preset="PORTRAIT_4_5",
            category="admissions",
        )
    if "asmo" in name or "v1" in name or "thcs" in name or "thpt" in name or name == "th.png":
        return MediaMapEntry(
            pattern=rel_path.name,
            page_template="home.html",
            block_key="achievements",
            purpose="academics",
            preset="SQUARE_1_1",
            category="awards",
        )
    if "mis01560" in name:
        return MediaMapEntry(
            pattern=rel_path.name,
            page_template="page.html",
            block_key="campus_gallery",
            purpose="branding",
            preset="HERO_16_9",
            category="about",
        )
    return None


def derive_category(page_template: str, fallback: str = "unmapped") -> str:
    value = page_template.lower()
    if "home" in value:
        return "home"
    if "about" in value or value == "page.html":
        return "about"
    if "admission" in value:
        return "admissions"
    if "academic" in value:
        return "academics"
    if "student_life" in value:
        return "student_life"
    if "news" in value:
        return "news"
    if "event" in value:
        return "events"
    if "csr" in value:
        return "csr"
    return fallback


def choose_preset(block_key: str, default: str = "THUMB") -> str:
    value = block_key.lower()
    if "hero" in value or "banner" in value:
        return "HERO_16_9"
    if "testimonial" in value or "portrait" in value:
        return "PORTRAIT_4_5"
    if "achievement" in value or "award" in value or "vinh_danh" in value:
        return "SQUARE_1_1"
    if "gallery" in value or "campus" in value:
        return "HERO_16_9"
    return default


def detect_file_type(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in SUPPORTED_IMAGE_EXTS:
        return "image"
    if ext in SUPPORTED_VIDEO_EXTS:
        return "video"
    if ext in SUPPORTED_DOC_EXTS:
        return "doc"
    return "other"


def compute_checksum(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def make_slug(stem: str, checksum: str) -> str:
    base = slugify(stem) or "media"
    return f"{base}-{checksum[:8]}"


def humanize_filename(path: Path) -> str:
    name = path.stem.replace("_", " ").replace("-", " ").strip()
    name = " ".join(part for part in name.split() if part)
    return name.title() if name else "Media asset"


def detect_people_flags(rel_path: Path, block_key: str = "", purpose: str = "") -> tuple[bool, bool]:
    name = rel_path.name.lower()
    parts = [p.lower() for p in rel_path.parts]
    contains_parent = False
    contains_student = False

    safe_award_names = {"th.png", "thcs.png", "thpt.png", "v1.png"}
    if name in safe_award_names:
        return False, False

    if "testimonials" in parts or "pvph" in name or "phhs" in name:
        contains_parent = True
    if "vinh danh" in parts or "asmo" in name:
        contains_student = True

    if "testimonial" in block_key.lower():
        contains_parent = True
    if "student" in block_key.lower():
        contains_student = True
    if "student" in purpose.lower():
        contains_student = True

    return contains_student, contains_parent


def build_tags(category: str, purpose: str, contains_student: bool, contains_parent: bool) -> list[str]:
    tags: list[str] = []
    if category and category != "unmapped":
        tags.append(f"category:{category}")
    if purpose:
        tags.append(f"purpose:{purpose}")
    if contains_student:
        tags.append("student")
    if contains_parent:
        tags.append("parent")
    return tags


def ensure_dir(path: Path, dry_run: bool) -> None:
    if dry_run:
        return
    path.mkdir(parents=True, exist_ok=True)


def copy_or_move_file(source: Path, dest: Path, move: bool, dry_run: bool) -> str:
    if dest.exists():
        return "exists"
    if dry_run:
        return "dry_run"
    ensure_dir(dest.parent, dry_run=False)
    if move:
        shutil.move(str(source), str(dest))
        return "moved"
    shutil.copy2(str(source), str(dest))
    return "copied"


def flatten_image(image: Image.Image) -> Image.Image:
    image = ImageOps.exif_transpose(image)
    if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
        background = Image.new("RGB", image.size, (255, 255, 255))
        alpha = image.split()[-1]
        background.paste(image, mask=alpha)
        return background
    return image.convert("RGB")


def resize_cover(image: Image.Image, target_size: tuple[int, int]) -> Image.Image:
    target_w, target_h = target_size
    src_w, src_h = image.size
    scale = max(target_w / src_w, target_h / src_h)
    new_w, new_h = int(src_w * scale), int(src_h * scale)
    resized = image.resize((new_w, new_h), Image.LANCZOS)
    left = max((new_w - target_w) // 2, 0)
    top = max((new_h - target_h) // 2, 0)
    return resized.crop((left, top, left + target_w, top + target_h))


def resize_long_edge(image: Image.Image, long_edge: int) -> Image.Image:
    src_w, src_h = image.size
    if max(src_w, src_h) <= long_edge:
        return image
    if src_w >= src_h:
        new_w = long_edge
        new_h = int(src_h * (long_edge / src_w))
    else:
        new_h = long_edge
        new_w = int(src_w * (long_edge / src_h))
    return image.resize((new_w, new_h), Image.LANCZOS)


def process_image(
    source_path: Path,
    dest_dir: Path,
    slug: str,
    preset_name: str,
    dry_run: bool,
) -> dict:
    preset = PRESETS.get(preset_name, PRESETS["THUMB"])
    with Image.open(source_path) as img:
        img = flatten_image(img)

        if "long_edge" in preset:
            processed = resize_long_edge(img, preset["long_edge"])
        else:
            processed = resize_cover(img, preset["size"])

        width, height = processed.size

        webp_path = dest_dir / f"{slug}.webp"
        jpeg_path = dest_dir / f"{slug}.jpg"

        if not dry_run:
            ensure_dir(dest_dir, dry_run=False)
            processed.save(
                webp_path,
                format="WEBP",
                quality=preset["webp_q"],
                method=6,
            )
            processed.save(
                jpeg_path,
                format="JPEG",
                quality=preset["jpeg_q"],
                optimize=True,
                progressive=True,
            )

    return {
        "webp_path": webp_path,
        "jpeg_path": jpeg_path,
        "width": width,
        "height": height,
    }


def ffmpeg_available() -> bool:
    return shutil.which("ffmpeg") is not None


def ffprobe_available() -> bool:
    return shutil.which("ffprobe") is not None


def extract_video_poster(source_path: Path, dest_path: Path, dry_run: bool) -> Optional[Path]:
    if not ffmpeg_available():
        return None
    if dry_run:
        return dest_path
    ensure_dir(dest_path.parent, dry_run=False)
    command = [
        "ffmpeg",
        "-y",
        "-ss",
        "00:00:01",
        "-i",
        str(source_path),
        "-frames:v",
        "1",
        "-q:v",
        "2",
        str(dest_path),
    ]
    subprocess.run(command, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return dest_path if dest_path.exists() else None


def probe_duration(source_path: Path) -> Optional[float]:
    if not ffprobe_available():
        return None
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(source_path),
    ]
    try:
        result = subprocess.run(command, check=False, capture_output=True, text=True)
        value = result.stdout.strip()
        return float(value) if value else None
    except Exception:
        return None


def media_root() -> Path:
    return Path(settings.MEDIA_ROOT)


def to_media_relative(path: Path) -> str:
    return path.relative_to(media_root()).as_posix()
