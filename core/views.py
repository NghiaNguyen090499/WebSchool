from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse
from django.db import OperationalError, connection
from django.urls import reverse
from news.models import News, Category
from events.models import Event
from gallery.models import Album, Photo
from about.models import AboutPage
from core.utils.program_content import (
    build_program_overview_redirects,
    get_program_year,
)
from .models import (
    CoreValue, CoreValuesPage, Statistic, TrainingProgram, TrainingProgramGroup, StudentLifePage,
    HeroSlide, Achievement, ParentTestimonial, Partner, FounderMessage,
    StudentSpotlight, Pillar, Facility, Podcast, ProgramOverviewPage, MediaAsset,
    MISPrototypeSiteContent, MISPrototypePage,
)


def home(request):
    """Homepage view with all sections including tabbed news"""
    program_year = get_program_year()

    tab_slugs = ['tieu-hoc', 'thcs', 'thpt', 'tuyen-sinh']
    news_by_category = {slug: [] for slug in tab_slugs}
    tab_news_qs = (
        News.objects.filter(category__slug__in=tab_slugs)
        .select_related('category')
        .order_by('-created_at')
    )
    for item in tab_news_qs:
        if not item.category:
            continue
        slug = item.category.slug
        if slug in news_by_category and len(news_by_category[slug]) < 4:
            news_by_category[slug].append(item)
        if all(len(items) >= 4 for items in news_by_category.values()):
            break
    
    # Get dynamic content from database
    hero_slides = HeroSlide.objects.filter(is_active=True)
    
    # Achievement data (home keeps only top 3 cards, others go to subpage)
    achievement_cards = Achievement.objects.filter(is_active=True, is_card=True).order_by('order', 'id')
    featured_achievement_cards = list(achievement_cards[:3])
    
    # Parent testimonials
    testimonials = ParentTestimonial.objects.filter(is_active=True)[:6]
    
    # Partners for marquee
    partners = Partner.objects.filter(is_active=True, show_in_marquee=True).order_by('order', 'name')
    
    # Founder message
    founder_message = FounderMessage.get_active()
    
    # Fallback to static partner logos if no partners in database
    if not partners.exists():
        partner_logos = [
            {"name": "Aptech Vietnam", "logo": "images/partners/aptechvietnam-com-vn.webp", "url": "https://aptechvietnam.com.vn/"},
            {"name": "MathExpress", "logo": "images/partners/mathexpress.svg", "url": "https://mathexpress.vn/"},
            {"name": "Jaxtina", "logo": "images/partners/jaxtina.svg", "url": "https://jaxtina.com/"},
            {"name": "Du học Quốc tế Thời Đại", "logo": "images/partners/duhocthoidai-com.jpg", "url": "http://duhocthoidai.com/"},
            {"name": "STEAM Academy", "logo": "images/partners/steamacademy-edu-vn.png", "url": "https://steamacademy.edu.vn/"},
            {"name": "RoboHub", "logo": "images/partners/robohub-vn.jpg", "url": "https://robohub.vn/"},
            {"name": "Robotanan", "logo": "images/partners/robotanan-com.jpg", "url": "https://www.robotanan.com/"},
            {"name": "Umbalena", "logo": "images/partners/umbalena-vn.jpg", "url": "https://umbalena.vn/"},
            {"name": "Seroto", "logo": "images/partners/seroto-vn.jpg", "url": "https://www.seroto.vn/"},
            {"name": "Rice-INS", "logo": "images/partners/rice-ins-com.png", "url": "https://www.rice-ins.com/"},
        ]
    else:
        partner_logos = None  # Will use partners from database

    training_program_group = TrainingProgramGroup.objects.filter(
        is_active=True,
        slug='he-dao-tao-chuyen-sau',
    ).first()
    if training_program_group:
        training_programs = training_program_group.programs.filter(is_active=True).order_by('order')
    else:
        training_programs = TrainingProgram.objects.filter(is_active=True).order_by('order')

    vision_page = AboutPage.objects.prefetch_related('sections').filter(page_type='vision').first()
    vision_sections = list(vision_page.sections.all().order_by('order')) if vision_page else []
    vision_header = next((section for section in vision_sections if section.order == 0), None) if vision_sections else None

    why_mis_page = AboutPage.objects.prefetch_related('sections').filter(page_type='whymis').first()
    why_mis_sections = list(why_mis_page.sections.all().order_by('order')) if why_mis_page else []
    why_mis_header = next((section for section in why_mis_sections if section.order == 0), None) if why_mis_sections else None
    why_mis_cards = [
        section for section in why_mis_sections
        if section.content and section.order not in {0, 6}
    ][:4]

    context = {
        'core_values': CoreValue.objects.all().order_by('order')[:8],
        'pillars': Pillar.objects.filter(is_active=True).order_by('order', 'title')[:6],
        'statistics': Statistic.objects.all()[:4],
        'featured_news': News.objects.filter(is_featured=True).select_related('category').first(),
        'recent_news': News.objects.filter(is_featured=False).select_related('category')[:6],
        'upcoming_events': Event.objects.filter(date__gte=timezone.now().date()).order_by('date')[:3],
        'albums': Album.objects.all()[:6],
        # Tabbed news by education level
        'news_tieu_hoc': news_by_category['tieu-hoc'],
        'news_thcs': news_by_category['thcs'],
        'news_thpt': news_by_category['thpt'],
        'news_tuyen_sinh': news_by_category['tuyen-sinh'],
        'news_categories': Category.objects.all()[:6],
        # Training programs for homepage
        'training_program_group': training_program_group,
        'training_programs': training_programs,
        # NEW: Dynamic content from database
        'hero_slides': hero_slides,
        'featured_achievement_cards': featured_achievement_cards,
        'testimonials': testimonials,
        'partners': partners,
        'founder_message': founder_message,
        # Fallback for partners
        'partner_logos': partner_logos,
        # Student Spotlight
        'student_spotlights': StudentSpotlight.objects.filter(is_active=True, is_featured=True)[:6],
        'vision_header': vision_header,
        'why_mis_header': why_mis_header,
        'why_mis_cards': why_mis_cards,
        'program_year': program_year,
    }
    return render(request, 'core/home.html', context)


def achievement_list(request):
    """All achievements page (everything except top 3 home cards)."""
    program_year = get_program_year()

    achievement_stats = Achievement.objects.filter(is_active=True, is_stat=True).order_by('order', 'id')
    achievement_cards = Achievement.objects.filter(is_active=True, is_card=True).order_by('order', 'id')
    featured_achievement_cards = list(achievement_cards[:3])
    featured_achievement_ids = [item.id for item in featured_achievement_cards]
    other_achievement_cards = achievement_cards.exclude(id__in=featured_achievement_ids)

    achievement_media = MediaAsset.objects.filter(
        is_approved=True,
        page_target='home.html',
        block_target='achievements',
        file_type='image',
    ).order_by('id')

    context = {
        'program_year': program_year,
        'achievement_stats': achievement_stats,
        'featured_achievement_cards': featured_achievement_cards,
        'other_achievement_cards': other_achievement_cards,
        'achievement_media': achievement_media,
    }
    return render(request, 'core/achievements.html', context)


def training_programs_list(request):
    """List all training programs"""
    training_program_group = TrainingProgramGroup.objects.filter(
        is_active=True,
        slug='he-dao-tao-chuyen-sau',
    ).first()
    if training_program_group:
        programs = training_program_group.programs.filter(is_active=True).order_by('order')
    else:
        programs = TrainingProgram.objects.filter(is_active=True).order_by('order')
    context = {
        'programs': programs,
        'training_program_group': training_program_group,
        'program_year': get_program_year(),
    }
    return render(request, 'core/training_programs.html', context)


def training_program_detail(request, slug):
    """Detail view for a single training program"""
    program = get_object_or_404(TrainingProgram, slug=slug, is_active=True)
    other_programs = TrainingProgram.objects.filter(is_active=True).exclude(slug=slug)[:3]
    context = {
        'program': program,
        'other_programs': other_programs,
    }
    return render(request, 'core/training_program_detail.html', context)


def program_overview_detail(request, slug):
    """Detail page for legacy MIS program overview content."""
    about_redirects = build_program_overview_redirects()
    if not about_redirects:
        about_redirects = {
            "chuong-trinh-tong-quan-mon-toan": "about:overview_math",
            "tong-quan-chuong-trinh-ngu-van-tai-mis": "about:overview_literature",
            "tong-quan-chuong-trinh-tieng-anh": "about:overview_english",
            "tong-quan-chuong-trinh-tieng-trung-2": "about:overview_chinese",
            "chuong-trinh-tong-quan-trai-nghiem-sang-tao-tnst": "about:tnst",
            "chuong-trinh-steam-voi-cong-nghe-sang-tao": "about:steam",
            "chuong-trinh-ky-nang-song-nam-hoc-2026-2027": "about:lifeskills",
        }

    target = about_redirects.get(slug)
    if target:
        return redirect(reverse(target), permanent=True)

    page = get_object_or_404(ProgramOverviewPage, slug=slug, is_active=True)
    context = {
        'page': page,
        'images': page.images.all(),
        'program_year': get_program_year(),
    }
    return render(request, 'core/program_overview_detail.html', context)


def student_life(request):
    """Trang Đời sống học sinh"""
    student_life_page = StudentLifePage.objects.filter(is_active=True).first()
    if not student_life_page:
        # Nếu chưa có dữ liệu, tạo trang mặc định
        student_life_page = StudentLifePage(
            title="Đời sống học sinh",
            slug="doi-song-hoc-sinh",
            description="Khám phá cuộc sống học tập và sinh hoạt tại MIS",
            is_active=True
        )
    
    has_content = any([
        (student_life_page.content or '').strip(),
        (student_life_page.activities or '').strip(),
        (student_life_page.clubs or '').strip(),
        (student_life_page.events or '').strip(),
        (student_life_page.facilities or '').strip(),
    ])

    context = {
        'page': student_life_page,
        'has_content': has_content,
    }
    return render(request, 'core/student_life.html', context)


def student_spotlight_list(request):
    """Trang Gương mặt MISers - hiển thị tất cả học sinh nổi bật"""
    category = request.GET.get('category', '')
    
    # Get all active spotlights
    spotlights = StudentSpotlight.objects.filter(is_active=True)

    # Filter by category if provided
    if category:
        spotlights = spotlights.filter(category=category)

    # Get unique categories for filter
    categories = StudentSpotlight.CATEGORY_CHOICES

    paginator = Paginator(spotlights, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    query_params = request.GET.copy()
    query_params.pop('page', None)
    querystring = query_params.urlencode()
    
    context = {
        'spotlights': page_obj,
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category,
        'total_count': StudentSpotlight.objects.filter(is_active=True).count(),
        'querystring': querystring,
    }
    return render(request, 'core/student_spotlight_list.html', context)


def pillar_list(request):
    """Trang trụ cột giáo dục"""
    pillars = Pillar.objects.filter(is_active=True).order_by("order", "title")
    context = {
        "pillars": pillars,
    }
    return render(request, "core/pillars.html", context)


def facility_list(request):
    """Trang cơ sở vật chất"""
    facilities = list(Facility.objects.filter(is_active=True).order_by("order", "name"))
    groups = {value: {"label": label, "items": []} for value, label in Facility.CATEGORY_CHOICES}
    for facility in facilities:
        groups[facility.category]["items"].append(facility)
    context = {
        "facility_groups": groups,
    }
    return render(request, "core/facilities.html", context)


def podcast_list(request):
    """Trang Tiếng nói MISERs - Podcasts"""
    podcasts = Podcast.objects.filter(is_active=True)
    featured = podcasts.filter(is_featured=True).first()
    
    context = {
        'podcasts': podcasts,
        'featured': featured,
        'total_count': podcasts.count(),
    }
    return render(request, 'core/podcasts.html', context)

def core_values(request):
    """Core values page"""
    page = CoreValuesPage.objects.filter(is_active=True).first()
    grace_values = CoreValue.objects.filter(group='grace').order_by('order')
    context = {
        'page': page,
        'grace_values': grace_values,
    }
    return render(request, 'core/core_values.html', context)


DEFAULT_LOWFI_TITLE = "MIS Prototype"
DEFAULT_LOWFI_META = "Prototype MIS 2026-2027: giáo dục AI-tích hợp, tư duy sáng tạo và phát triển toàn diện."
LEGACY_LOWFI_PAGES = {
    "home": {
        "template": "core/lowfi/mis_home.html",
        "title": "MIS - Trang chủ",
        "nav_label": "Trang chủ",
        "order": 0,
    },
    "preparation": {
        "template": "core/lowfi/mis_preparation.html",
        "title": "MIS - Mầm non & Tiền tiểu học",
        "nav_label": "Mầm non",
        "order": 1,
    },
    "primary": {
        "template": "core/lowfi/mis_primary.html",
        "title": "MIS - Cấp Tiểu học",
        "nav_label": "Tiểu học",
        "order": 2,
    },
    "thcs": {
        "template": "core/lowfi/mis_thcs.html",
        "title": "MIS - Cấp THCS",
        "nav_label": "THCS",
        "order": 3,
    },
    "thpt": {
        "template": "core/lowfi/mis_thpt.html",
        "title": "MIS - Cấp THPT",
        "nav_label": "THPT",
        "order": 4,
    },
    "edtech": {
        "template": "core/lowfi/mis_edtech.html",
        "title": "MIS - Hệ sinh thái EdTech",
        "nav_label": "EdTech",
        "order": 5,
    },
    "parent-portal": {
        "template": "core/lowfi/mis_parent_portal.html",
        "title": "MIS - Cổng phụ huynh",
        "nav_label": "Phụ huynh",
        "order": 6,
    },
}

LOWFI_HERO_IMAGE_BY_PAGE_KEY = {
    "preparation": "images/cap_hoc/mam_non.png",
    "primary": "images/cap_hoc/tieu_hoc.png",
    "thcs": "images/cap_hoc/thcs.png",
    "thpt": "images/cap_hoc/thpt.png",
}


def _get_lowfi_site_content(program_year):
    try:
        site = MISPrototypeSiteContent.objects.filter(year=program_year, is_active=True).first()
        if site:
            return site
        return MISPrototypeSiteContent.objects.filter(is_active=True).order_by("-year").first()
    except OperationalError:
        return None


def _get_lowfi_pages(program_year):
    try:
        pages = list(
            MISPrototypePage.objects.filter(year=program_year, is_active=True).order_by("order", "page_key")
        )
        if pages:
            return pages
        return list(MISPrototypePage.objects.filter(is_active=True).order_by("-year", "order", "page_key"))
    except OperationalError:
        return []


def _render_legacy_lowfi_page(request, page_key, program_year, lowfi_site):
    if page_key == "home":
        page_config = LEGACY_LOWFI_PAGES["home"]
    else:
        page_config = LEGACY_LOWFI_PAGES.get(page_key)
        if not page_config:
            raise Http404("Prototype page not found.")

    nav_items = []
    ordered_pages = sorted(LEGACY_LOWFI_PAGES.items(), key=lambda item: item[1]["order"])
    for nav_key, config in ordered_pages:
        if nav_key == "home":
            href = reverse("core:mis_lowfi_home")
        else:
            href = reverse("core:mis_lowfi_page", kwargs={"page_key": nav_key})
        nav_items.append(
            {
                "key": nav_key,
                "label": config["nav_label"],
                "href": href,
            }
        )

    context = {
        "program_year": program_year,
        "lowfi_page_key": page_key if page_key != "home" else "home",
        "lowfi_nav": nav_items,
        "lowfi_title": page_config["title"],
        "lowfi_meta_description": lowfi_site.meta_description if lowfi_site else DEFAULT_LOWFI_META,
        "lowfi_site": lowfi_site,
        "lowfi_hero_image": LOWFI_HERO_IMAGE_BY_PAGE_KEY.get(page_key),
    }
    return render(request, page_config["template"], context)


def mis_lowfi_page(request, page_key='home'):
    program_year = get_program_year()
    lowfi_site = _get_lowfi_site_content(program_year)
    pages = _get_lowfi_pages(program_year)
    if not pages:
        return _render_legacy_lowfi_page(request, page_key, program_year, lowfi_site)

    pages_by_key = {page.page_key: page for page in pages}
    if page_key == "home":
        lowfi_page = pages_by_key.get("home") or pages[0]
    else:
        lowfi_page = pages_by_key.get(page_key)
        if not lowfi_page:
            raise Http404("Prototype page not found.")

    nav_items = []
    for page in pages:
        if page.page_key == 'home':
            href = reverse('core:mis_lowfi_home')
        else:
            href = reverse('core:mis_lowfi_page', kwargs={'page_key': page.page_key})
        nav_items.append(
            {
                'key': page.page_key,
                'label': page.nav_label,
                'href': href,
            }
        )

    blocks = lowfi_page.blocks if isinstance(lowfi_page.blocks, list) else []
    lowfi_title = lowfi_page.browser_title or lowfi_page.title or DEFAULT_LOWFI_TITLE
    lowfi_meta_description = lowfi_page.meta_description or (
        lowfi_site.meta_description if lowfi_site else DEFAULT_LOWFI_META
    )

    context = {
        'program_year': program_year,
        'lowfi_page_key': lowfi_page.page_key,
        'lowfi_nav': nav_items,
        'lowfi_title': lowfi_title,
        'lowfi_meta_description': lowfi_meta_description,
        'lowfi_site': lowfi_site,
        'lowfi_hero_image': LOWFI_HERO_IMAGE_BY_PAGE_KEY.get(lowfi_page.page_key),
        'lowfi_page': lowfi_page,
        'lowfi_blocks': blocks,
    }
    return render(request, "core/lowfi/mis_page.html", context)



def healthz(request):
    return HttpResponse("ok", content_type="text/plain")


def readyz(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except OperationalError:
        return HttpResponse("db unavailable", status=503, content_type="text/plain")
    return HttpResponse("ok", content_type="text/plain")
