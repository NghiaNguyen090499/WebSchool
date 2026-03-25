import copy
import json
from functools import lru_cache
from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.db.utils import OperationalError, ProgrammingError
from django.urls import NoReverseMatch, reverse


DATA_DIR = Path(settings.BASE_DIR) / "core" / "data"
DEFAULT_PROGRAM_YEAR = "2026-2027"


def _resolve_content_file(year=None):
    """Return Path for the JSON file matching *year* (e.g. '2026-2027')."""
    year = year or getattr(settings, "MIS_PROGRAM_YEAR", DEFAULT_PROGRAM_YEAR)
    candidate = DATA_DIR / f"program_content_{year.replace('-', '_')}.json"
    if candidate.exists():
        return candidate
    # Fallback to the default year
    fallback = DATA_DIR / f"program_content_{DEFAULT_PROGRAM_YEAR.replace('-', '_')}.json"
    return fallback if fallback.exists() else None


@lru_cache(maxsize=4)
def load_program_content(year=None):
    file_payload = _load_program_content_from_file(year)
    db_payload = _load_program_content_from_db(year)
    if db_payload and file_payload:
        return _deep_merge_content(file_payload, db_payload)
    if db_payload:
        return db_payload

    return file_payload


def _load_program_content_from_file(year=None):
    path = _resolve_content_file(year)
    if not path:
        return {}
    try:
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return {}


def _deep_merge_content(base, override):
    if not isinstance(base, dict) or not isinstance(override, dict):
        return copy.deepcopy(override)

    merged = copy.deepcopy(base)
    for key, value in override.items():
        current = merged.get(key)
        if isinstance(current, dict) and isinstance(value, dict):
            merged[key] = _deep_merge_content(current, value)
        else:
            merged[key] = copy.deepcopy(value)
    return merged


def clear_program_content_cache():
    load_program_content.cache_clear()


def get_program_year():
    content = load_program_content()
    return content.get("program_year") or getattr(settings, "MIS_PROGRAM_YEAR", DEFAULT_PROGRAM_YEAR)


def get_program_block(key):
    content = load_program_content()
    blocks = content.get("blocks", {})
    block = blocks.get(key)
    if not isinstance(block, dict):
        return {}

    payload = copy.deepcopy(block)
    payload.setdefault("key", key)
    payload.setdefault("year", get_program_year())
    payload["metadata"] = _merge_block_metadata(payload, content)
    return payload


def get_program_metadata(key):
    return load_program_content().get(key, {})


def get_training_systems():
    """Return the ``training_systems`` array from the JSON (EPIC-1 addition)."""
    return load_program_content().get("training_systems", [])


def get_edtech_ecosystem():
    """Return the ``edtech_ecosystem`` block from the JSON (EPIC-1 addition)."""
    content = load_program_content()
    block = content.get("blocks", {}).get("edtech_ecosystem")
    if isinstance(block, dict):
        payload = copy.deepcopy(block)
        payload.setdefault("key", "edtech_ecosystem")
        payload.setdefault("year", get_program_year())
        return payload
    return {}


def resolve_navigation(section):
    navigation = load_program_content().get("navigation", {})
    items = navigation.get(section, [])
    if not isinstance(items, list):
        return []

    resolved = []
    for item in items:
        if not isinstance(item, dict):
            continue
        payload = dict(item)
        url_name = payload.get("url_name")
        if url_name:
            try:
                payload["href"] = reverse(url_name)
            except NoReverseMatch:
                payload["href"] = "#"
        else:
            payload["href"] = payload.get("href", "#")
        resolved.append(payload)
    return resolved


def get_program_overview_entry(entry_key):
    entries = get_program_metadata("program_overview_pages").get("entries", {})
    entry = entries.get(entry_key)
    return dict(entry) if isinstance(entry, dict) else {}


def build_program_overview_redirects():
    entries = get_program_metadata("program_overview_pages").get("entries", {})
    if not isinstance(entries, dict):
        return {}

    url_name_lookup = _navigation_url_name_lookup("program_overview")
    redirects = {}

    for entry_key, entry in entries.items():
        if not isinstance(entry, dict):
            continue
        target = entry.get("url_name") or url_name_lookup.get(entry_key)
        if not target:
            continue
        slug = entry.get("slug")
        if slug:
            redirects[slug] = target
        for legacy_slug in entry.get("legacy_slugs", []):
            if isinstance(legacy_slug, str) and legacy_slug:
                redirects[legacy_slug] = target
    return redirects


def _navigation_url_name_lookup(section):
    navigation = load_program_content().get("navigation", {})
    items = navigation.get(section, [])
    if not isinstance(items, list):
        return {}

    lookup = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        key = item.get("key")
        url_name = item.get("url_name")
        if key and url_name:
            lookup[key] = url_name
    return lookup


def _merge_block_metadata(block, content):
    metadata = {}
    root_metadata = {
        "source_doc": content.get("source_doc"),
        "approved_at": content.get("approved_at"),
        "version": content.get("version"),
    }
    metadata.update({k: v for k, v in root_metadata.items() if v})
    block_metadata = block.get("metadata")
    if isinstance(block_metadata, dict):
        metadata.update({k: v for k, v in block_metadata.items() if v})
    return metadata


def _load_program_content_from_db(year=None):
    """Return program content from DB (active records), or {} when unavailable."""
    try:
        model = apps.get_model("core", "ProgramContentSource")
    except LookupError:
        return {}

    try:
        qs = model.objects.filter(is_active=True)
        requested_year = year or getattr(settings, "MIS_PROGRAM_YEAR", DEFAULT_PROGRAM_YEAR)

        record = qs.filter(year=requested_year).first()
        if not record:
            record = qs.order_by("-year").first()
        if not record or not isinstance(record.content, dict):
            return {}

        payload = copy.deepcopy(record.content)
        payload.setdefault("program_year", record.year)
        return payload
    except (OperationalError, ProgrammingError):
        return {}
