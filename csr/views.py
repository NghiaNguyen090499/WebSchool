import re

from django.shortcuts import render

from .models import CSRProject, JourneyProgram


def _clean_description(text: str, title: str = "") -> str:
    """Remove scraped artifacts from CSR project descriptions."""
    if not text:
        return ""

    cleaned = text

    # Remove social-media share labels
    cleaned = re.sub(r"Share\s*on\s*(Twitter|Facebook|LinkedIn)", "", cleaned, flags=re.I)
    cleaned = re.sub(r"ShareTweet", "", cleaned, flags=re.I)
    cleaned = re.sub(r"Share\s*Tweet", "", cleaned, flags=re.I)

    # Remove the title if it appears at the very beginning of the description
    # (common when content is scraped from web pages)
    if title:
        # Normalise whitespace in both title and cleaned text for comparison
        norm_title = re.sub(r"\s+", "", title).upper()
        norm_start = re.sub(r"\s+", "", cleaned[:len(title) * 2]).upper()
        if norm_start.startswith(norm_title):
            # Find actual end position in original text
            chars_matched = 0
            end_pos = 0
            for i, ch in enumerate(cleaned):
                if ch in (" ", "\n", "\r", "\t"):
                    continue
                if chars_matched < len(norm_title) and ch.upper() == norm_title[chars_matched]:
                    chars_matched += 1
                    end_pos = i + 1
                else:
                    break
            if chars_matched == len(norm_title):
                cleaned = cleaned[end_pos:]

    # Truncate at "Related Posts" section (Vietnamese)
    idx = cleaned.find("Bài Cùng Chuyên Mục")
    if idx > 0:
        cleaned = cleaned[:idx]

    # Remove inline JS variable blocks
    cleaned = re.sub(r"var\s+jnews_module[\w_]*\s*=\s*\{[\s\S]*?\};", "", cleaned)
    cleaned = re.sub(r"var\s+[\w_]+\s*=\s*\{[^}]*\};", "", cleaned)

    # Remove footer / charity boilerplate
    cleaned = re.sub(r"MIS CHARITY FOUNDATION[\s\S]*$", "", cleaned, flags=re.I)
    cleaned = re.sub(r"Quỹ Thiện Nguyện MIS[\s\S]*$", "", cleaned, flags=re.I)
    cleaned = re.sub(r"Website:\s*misvn\.edu\.vn[\s\S]*$", "", cleaned, flags=re.I)
    cleaned = re.sub(r"Lô TH2 khu ĐTM[\s\S]*$", "", cleaned, flags=re.I)

    # Remove MIS slogans that frequently leak into content
    cleaned = re.sub(r"Học để tự do[\s\S]*$", "", cleaned, flags=re.I)
    cleaned = re.sub(r"CÓ MỘT THỨ TUYỆT VỜI HƠN CẢ[\s\S]*$", "", cleaned, flags=re.I)
    cleaned = re.sub(r"Thông minh để Hạnh phúc[\s\S]*$", "", cleaned, flags=re.I)

    # Remove decorative separators
    cleaned = re.sub(r"—{2,}", "", cleaned)
    cleaned = re.sub(r"-{3,}", "", cleaned)
    cleaned = re.sub(r"_{3,}", "", cleaned)

    # Remove phone numbers & YouTube links
    cleaned = re.sub(r"\d{3}\s*\d{4}\s*\d{3}", "", cleaned)
    cleaned = re.sub(r"Youtube:\s*https?://\S+", "", cleaned, flags=re.I)

    # Insert paragraph breaks at sentence boundaries
    # Period followed by uppercase Vietnamese/Latin letter
    vn_upper = (
        r"A-ZÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬĐÈÉẺẼẸÊẾỀỂỄỆ"
        r"ÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴ"
    )
    cleaned = re.sub(
        r"\.(\s*)([" + vn_upper + r"])",
        r".\n\n\2",
        cleaned
    )

    # Collapse excessive whitespace (keep paragraph breaks)
    cleaned = re.sub(r"[ \t]{2,}", " ", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    return cleaned.strip()


def csr_list(request):
    projects_qs = (
        CSRProject.objects.filter(is_active=True)
        .prefetch_related("images")
        .order_by("order", "title")
    )
    projects = []
    total_images = 0
    hero_image = None
    for project in projects_qs:
        active_images = [img for img in project.images.all() if img.is_active]
        project.active_images = active_images
        project.primary_image = active_images[0] if active_images else None
        total_images += len(active_images)
        if hero_image is None and project.primary_image:
            hero_image = project.primary_image

        # Clean description server-side so both card & modal get clean data
        project.description = _clean_description(project.description, project.title)

        projects.append(project)

    # ── Journey Programs ──
    journey_qs = (
        JourneyProgram.objects
        .filter(is_active=True)
        .prefetch_related("gallery_images")
        .order_by("order")
    )
    for jp in journey_qs:
        jp.active_gallery = [img for img in jp.gallery_images.all() if img.is_active]

    journey_featured = [jp for jp in journey_qs if jp.is_featured]
    journey_more = [jp for jp in journey_qs if not jp.is_featured]

    context = {
        "projects": projects,
        "hero_image": hero_image,
        "total_projects": len(projects),
        "total_images": total_images,
        "journey_featured": journey_featured,
        "journey_more": journey_more,
        "journey_more_count": len(journey_more),
    }
    return render(request, "csr/list.html", context)
