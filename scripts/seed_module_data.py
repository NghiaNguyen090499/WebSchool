from datetime import date, timedelta
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.test import Client

from csr.models import CSRProject, CSRImage
from activities.models import Activity
from core.models import Pillar, Facility
from about.models import AboutPage, AboutSection


def get_first_media_image():
    media_root = Path(settings.MEDIA_ROOT)
    if not media_root.exists():
        return None
    candidates = list(media_root.rglob("*.jpg"))
    if not candidates:
        candidates = list(media_root.rglob("*.png")) + list(media_root.rglob("*.jpeg"))
    return candidates[0] if candidates else None


image_path = get_first_media_image()
print(f"Image source: {image_path}" if image_path else "No image found in media; CSRImage will be skipped.")

# -----------------------------
# CSR Projects + Images
# -----------------------------
csr_projects = [
    {
        "title": "CSR Community Robotics",
        "description": "Community robotics labs and mentorship for middle school students.",
        "impact_metrics": "500+ students reached\n25+ hands-on workshops\n12 community partners",
        "order": 1,
    },
    {
        "title": "CSR Green Campus",
        "description": "Sustainability initiatives focused on energy, water, and waste reduction.",
        "impact_metrics": "30% energy reduction\n3 green labs launched\n1500+ trees planted",
        "order": 2,
    },
]

for data in csr_projects:
    project, created = CSRProject.objects.get_or_create(
        title=data["title"],
        defaults={
            "description": data["description"],
            "impact_metrics": data["impact_metrics"],
            "order": data["order"],
            "is_active": True,
        },
    )
    if not created:
        if not project.description:
            project.description = data["description"]
        if not project.impact_metrics:
            project.impact_metrics = data["impact_metrics"]
        project.order = project.order or data["order"]
        project.is_active = True
        project.save()

    if image_path and not CSRImage.objects.filter(project=project).exists():
        with image_path.open("rb") as handle:
            image = CSRImage(project=project, caption="CSR activity", order=1, is_active=True)
            image.image.save(f"csr-{project.slug}-01{image_path.suffix}", File(handle), save=True)

# -----------------------------
# Activities
# -----------------------------
base_date = date.today()
activities = [
    {
        "title": "STEM Maker Week",
        "type": "extracurricular",
        "start_date": base_date + timedelta(days=7),
        "end_date": base_date + timedelta(days=10),
        "description": "A week of design challenges, robotics builds, and student showcases.",
    },
    {
        "title": "Summer Camp Innovation",
        "type": "summer_camp",
        "start_date": base_date + timedelta(days=30),
        "end_date": base_date + timedelta(days=45),
        "description": "Project-based summer camp with AI, art, and entrepreneurship modules.",
    },
    {
        "title": "International Exchange 2030",
        "type": "international",
        "start_date": base_date + timedelta(days=90),
        "end_date": base_date + timedelta(days=100),
        "description": "Partner school exchange program with cross-cultural learning.",
    },
]

for data in activities:
    activity, created = Activity.objects.get_or_create(
        title=data["title"],
        type=data["type"],
        start_date=data["start_date"],
        defaults={
            "end_date": data["end_date"],
            "description": data["description"],
            "is_active": True,
        },
    )
    if not created:
        if not activity.description:
            activity.description = data["description"]
        activity.end_date = activity.end_date or data["end_date"]
        activity.is_active = True
        activity.save()

# -----------------------------
# Pillars (6 items)
# -----------------------------
pillars = [
    ("Character", "fas fa-heart", "Build integrity, empathy, and leadership through real projects.", 1),
    ("Academic Excellence", "fas fa-graduation-cap", "Rigorous, student-centered learning paths.", 2),
    ("Innovation", "fas fa-lightbulb", "Apply AI and design thinking to real challenges.", 3),
    ("Global Mindset", "fas fa-globe", "Cross-cultural experiences and language mastery.", 4),
    ("Wellbeing", "fas fa-leaf", "Balanced growth across mind, body, and character.", 5),
    ("Future Skills", "fas fa-rocket", "Digital literacy, collaboration, and entrepreneurship.", 6),
]

for title, icon, desc, order in pillars:
    pillar, created = Pillar.objects.get_or_create(
        title=title,
        defaults={
            "icon": icon,
            "short_description": desc,
            "order": order,
            "is_active": True,
        },
    )
    if not created:
        if not pillar.short_description:
            pillar.short_description = desc
        pillar.icon = pillar.icon or icon
        pillar.order = pillar.order or order
        pillar.is_active = True
        pillar.save()

# -----------------------------
# Facilities
# -----------------------------
facilities = [
    {
        "name": "Smart Classroom",
        "category": "classroom",
        "description": "Interactive boards, AI-assisted learning stations, and flexible seating.",
        "map_embed": "",
        "order": 1,
    },
    {
        "name": "STEM Innovation Lab",
        "category": "lab",
        "description": "Robotics kits, 3D printing, electronics, and prototyping tools.",
        "map_embed": "",
        "order": 1,
    },
    {
        "name": "Community Hub",
        "category": "utility",
        "description": "Library, counseling, and parent engagement spaces.",
        "map_embed": "<iframe src=\"https://www.google.com/maps?q=Hanoi\u0026output=embed\" width=\"100%\" height=\"220\" style=\"border:0;\" loading=\"lazy\"></iframe>",
        "order": 1,
    },
]

for data in facilities:
    facility, created = Facility.objects.get_or_create(
        name=data["name"],
        category=data["category"],
        defaults={
            "description": data["description"],
            "map_embed": data["map_embed"],
            "order": data["order"],
            "is_active": True,
        },
    )
    if not created:
        if not facility.description:
            facility.description = data["description"]
        if not facility.map_embed:
            facility.map_embed = data["map_embed"]
        facility.order = facility.order or data["order"]
        facility.is_active = True
        facility.save()

    if image_path and not facility.image:
        with image_path.open("rb") as handle:
            facility.image.save(f"facility-{facility.pk}{image_path.suffix}", File(handle), save=True)

# -----------------------------
# About Pages + Sections (Strategy/Vision)
# -----------------------------
about_pages = [
    {
        "page_type": "strategy_2025_2028",
        "title": "Strategy 2025-2028",
        "content": "Roadmap for growth, quality, and digital transformation.",
        "sections": [
            {
                "order": 0,
                "layout": "hero",
                "background": "gradient",
                "eyebrow": "Strategy",
                "title": "Strategy 2025-2028",
                "subtitle": "A focused roadmap for learning innovation and community impact.",
                "cta_text": "Explore programs",
                "cta_url": "/triet-ly-giao-duc/",
            },
            {
                "order": 1,
                "layout": "text_left",
                "background": "white",
                "eyebrow": "Key initiatives",
                "title": "Four strategic pillars",
                "content": "Focus on AI literacy, bilingual excellence, wellbeing, and global partnerships.",
                "timeline": "2025: Launch AI labs\n2026: Expand STEM programs\n2027: Global partnerships\n2028: New campus phase",
                "kpi": "90% satisfaction\n30% international programs\n100% digital literacy",
            },
        ],
    },
    {
        "page_type": "vision_2033",
        "title": "Vision 2033",
        "content": "Long-term vision for a future-ready learning ecosystem.",
        "sections": [
            {
                "order": 0,
                "layout": "hero",
                "background": "navy",
                "eyebrow": "Vision",
                "title": "Vision 2033",
                "subtitle": "A learning ecosystem that prepares students for global challenges.",
                "cta_text": "View facilities",
                "cta_url": "/co-so-vat-chat/",
            },
            {
                "order": 1,
                "layout": "text_right",
                "background": "light",
                "eyebrow": "Milestones",
                "title": "Growing with purpose",
                "content": "Sustainable growth, inclusive culture, and high-impact outcomes.",
                "timeline": "2029: International accreditation\n2031: Expansion of partnerships\n2033: Regional leadership",
                "kpi": "Top 5 regional ranking\n50+ partner schools\n95% graduate success",
            },
        ],
    },
]

for page_data in about_pages:
    page, created = AboutPage.objects.get_or_create(
        page_type=page_data["page_type"],
        defaults={
            "title": page_data["title"],
            "content": page_data["content"],
        },
    )
    if not created:
        if not page.title:
            page.title = page_data["title"]
        if not page.content:
            page.content = page_data["content"]
        page.save()

    if not AboutSection.objects.filter(page=page).exists():
        for section_data in page_data["sections"]:
            timeline = section_data.pop("timeline", "")
            kpi = section_data.pop("kpi", "")
            section = AboutSection.objects.create(page=page, timeline=timeline, kpi=kpi, **section_data)
            if image_path and section.layout == "hero":
                with image_path.open("rb") as handle:
                    section.image.save(
                        f"about-{page.page_type}-hero{image_path.suffix}",
                        File(handle),
                        save=True,
                    )

# -----------------------------
# UI checks
# -----------------------------
client = Client()
urls = [
    "/trach-nhiem-xa-hoi/",
    "/triet-ly-giao-duc/",
    "/co-so-vat-chat/",
    "/hoat-dong-ngoai-khoa/",
    "/about/strategy-2025-2028/",
    "/about/vision-2033/",
]
print("\nURL status checks:")
for url in urls:
    response = client.get(url)
    print(f"{url} -> {response.status_code}")
