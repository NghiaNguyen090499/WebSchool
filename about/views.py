from django.shortcuts import render
from .models import AboutPage, AboutPdfDocument


from core.models import CoreValue, Achievement, Facility, FounderMessage, Partner
from core.utils.program_content import (
    get_program_block,
    get_program_metadata,
    get_program_year,
    get_training_systems,
    get_edtech_ecosystem,
)


def _as_list(payload):
    return payload if isinstance(payload, list) else []


def _unique_values(values):
    seen = set()
    output = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            output.append(value)
    return output


def page_detail(request, page_type):
    """Dynamic view for all About pages."""
    program_year = get_program_year()
    legacy_page_types = {
        'overview_math': 'math',
        'overview_literature': 'literature',
        'overview_english': 'english',
        'overview_chinese': 'chinese',
        'tnst': 'creative',
        'schedule_2026': 'schedule_2025',
    }

    # Prefetch sections for efficient loading
    page = AboutPage.objects.prefetch_related('sections').filter(page_type=page_type).first()
    if not page:
        legacy_type = legacy_page_types.get(page_type)
        if legacy_type:
            page = AboutPage.objects.prefetch_related('sections').filter(page_type=legacy_type).first()

    if not page:
        labels = dict(AboutPage.PAGE_CHOICES)
        page_label = labels.get(page_type)
        if not page_label and legacy_type:
            page_label = labels.get(legacy_type)
        return render(
            request,
            "about/page_missing.html",
            {
                "page_label": page_label or "Thông tin",
                "page_type": page_type,
            },
        )

    reverse_legacy = {value: key for key, value in legacy_page_types.items()}
    pdf_page_type_candidates = _unique_values([
        page.page_type,
        page_type,
        legacy_page_types.get(page.page_type),
        legacy_page_types.get(page_type),
        reverse_legacy.get(page.page_type),
        reverse_legacy.get(page_type),
    ])
    pdf_candidates = AboutPdfDocument.objects.filter(
        page_type__in=pdf_page_type_candidates
    ).prefetch_related('pages')
    pdf_by_page_type = {item.page_type: item for item in pdf_candidates}
    pdf_document = next(
        (pdf_by_page_type[candidate] for candidate in pdf_page_type_candidates if candidate in pdf_by_page_type),
        None,
    )
    pdf_pages = list(pdf_document.pages.all()) if pdf_document else []

    sections = list(page.sections.all().order_by('order'))

    # Fetch extra data for specific pages
    extra_context = {
        'program_year': program_year,
    }
    if page.page_type == 'mission':
        hero_section = next((section for section in sections if section.layout == 'hero'), None)
        if not hero_section and sections:
            hero_section = sections[0]

        panel_sections = [
            section for section in sections
            if section != hero_section
        ]

        extra_context['grace_values'] = CoreValue.objects.filter(group='grace')
        extra_context['hero_section'] = hero_section
        extra_context['panel_sections'] = panel_sections
    elif page.page_type == 'future_ai':
        hero_section = next((section for section in sections if section.layout == 'hero'), None)
        if not hero_section and sections:
            hero_section = sections[0]

        ai_section = next((section for section in sections if section.layout == 'future_ai'), None)
        ai_tags = ai_section.get_kpi_list() if ai_section else []
        ai_features = []
        if ai_section:
            for item in ai_section.get_timeline_list():
                title, _, description = item.partition('|')
                ai_features.append(
                    {
                        'title': title.strip(),
                        'description': description.strip(),
                    }
                )

        info_sections = [
            section for section in sections
            if section not in {hero_section, ai_section}
        ]

        extra_context['hero_section'] = hero_section
        extra_context['ai_section'] = ai_section
        extra_context['ai_tags'] = ai_tags
        extra_context['ai_features'] = ai_features
        extra_context['info_sections'] = info_sections
        future_ai_block = get_program_block('future_ai')
        future_ai_metadata = future_ai_block.get('metadata', {})
        extra_context['future_ai_block'] = future_ai_block
        extra_context['future_ai_copy'] = future_ai_block.get('copy', {})
        extra_context['future_ai_domains'] = _as_list(future_ai_metadata.get('domains'))
        extra_context['future_ai_roadmap'] = _as_list(future_ai_metadata.get('roadmap_levels'))
        extra_context['future_ai_core_pillars'] = _as_list(future_ai_block.get('core_pillars'))
        extra_context['future_ai_tools'] = _as_list(future_ai_block.get('tools'))
        extra_context['future_ai_outcomes'] = _as_list(future_ai_block.get('outcomes'))
    
    elif page.page_type == 'lifeskills':
        extra_context['values_5xin'] = CoreValue.objects.filter(group='5xin')
        extra_context['values_5biet'] = CoreValue.objects.filter(group='5biet')
        extra_context['values_5khong'] = CoreValue.objects.filter(group='5khong')
        extra_context['lifeskills_block'] = get_program_block('lifeskills')
        extra_context['lifeskills_overview'] = get_program_metadata('program_overview_pages')
    elif page.page_type == 'principal':
        extra_context['founder_message'] = FounderMessage.get_active()
        
    elif page.page_type == 'strengths':
        extra_context['achievements'] = Achievement.objects.filter(year=2025)
        extra_context['facilities'] = Facility.objects.filter(is_active=True)
        extra_context['grace_values'] = CoreValue.objects.filter(group='grace')
        extra_context['values_5xin'] = CoreValue.objects.filter(group='5xin')
        extra_context['values_5biet'] = CoreValue.objects.filter(group='5biet')
        extra_context['values_5khong'] = CoreValue.objects.filter(group='5khong')
    elif page.page_type == 'creative_movement':
        # Keep fallback empty until a verified 2026-2027 asset batch is approved/imported.
        extra_context['pdf_fallback_images'] = []
    elif page.page_type == 'partners':
        active_partners = Partner.objects.filter(is_active=True)
        extra_context['all_partners'] = active_partners
        extra_context['partners_tech'] = active_partners.filter(partner_type='technology')
        extra_context['partners_lang'] = active_partners.filter(partner_type='language')
        extra_context['partners_edu'] = active_partners.filter(partner_type='education')
        extra_context['partners_community'] = active_partners.filter(partner_type='community')

    if page.page_type in {'overview_english', 'english'}:
        english_block = get_program_block('overview_english')
        extra_context['program_block'] = english_block
        extra_context['program_targets'] = english_block.get('targets', {})
        extra_context['program_labels'] = english_block.get('labels', {})
        extra_context['program_curriculum'] = english_block.get('curriculum', {})
        extra_context['training_systems'] = get_training_systems()

    if page.page_type in {'overview_chinese', 'chinese'}:
        chinese_block = get_program_block('overview_chinese')
        extra_context['program_block'] = chinese_block
        extra_context['program_targets'] = chinese_block.get('targets', {})
        extra_context['program_labels'] = chinese_block.get('labels', {})
        extra_context['program_curriculum'] = chinese_block.get('curriculum', {})
        extra_context['training_systems'] = get_training_systems()

    if page.page_type == 'high':
        english_block = get_program_block('overview_english')
        extra_context['program_targets'] = english_block.get('targets', {})
        extra_context['program_labels'] = english_block.get('labels', {})

    if page.page_type in {'overview_math', 'math'}:
        math_block = get_program_block('math')
        extra_context['math_block'] = math_block
        extra_context['grade_roadmap'] = math_block.get('grade_roadmap', {})
        extra_context['sample_lesson'] = math_block.get('sample_lesson', {})
        extra_context['talent_pillars'] = _as_list(math_block.get('talent_pillars'))

    if page.page_type in {'overview_literature', 'literature'}:
        lit_block = get_program_block('literature')
        extra_context['literature_block'] = lit_block
        extra_context['lit_articulation'] = _as_list(lit_block.get('articulation'))

    if page.page_type == 'edtech':
        extra_context['edtech'] = get_edtech_ecosystem()
        extra_context['training_systems'] = get_training_systems()

    if page.page_type == 'vision':
        extra_context['vision_2035_block'] = get_program_block('vision_2035')

    if page.page_type in {'schedule_2025', 'schedule_2026', 'schedule_hd'}:
        extra_context['schedule_config'] = get_program_metadata('schedule')

    # Use dedicated templates for specific page types
    template_map = {
        'strengths': 'about/strengths.html',
        'robotics': 'about/robotics.html',
        'steam': 'about/steam.html',
        'overview_math': 'about/math.html',
        'math': 'about/math.html',
        'overview_literature': 'about/literature.html',
        'literature': 'about/literature.html',
        'overview_english': 'about/english.html',
        'english': 'about/english.html',
        'overview_chinese': 'about/foreign_languages.html',
        'chinese': 'about/foreign_languages.html',
        'tnst': 'about/tnst.html',
        'creative': 'about/tnst.html',  # Legacy mapping
        'lifeskills': 'about/lifeskills.html',
        'creative_movement': 'about/creative_movement.html',
        'mission': 'about/mission.html',
        'vision': 'about/vision.html',
        'principal': 'about/principal.html',
        'whymis': 'about/whymis.html',
        'future_ai': 'about/future_ai.html',
        'edtech': 'about/edtech.html',
        'partners': 'about/partners.html',
    }
    
    if page.page_type in template_map:
        context = {
            'page': page,
            'pdf_document': pdf_document,
            'pdf_pages': pdf_pages,
            'sections': sections,
        }
        context.update(extra_context)
        return render(
            request,
            template_map[page.page_type],
            context,
        )

    context = {
        'page': page,
        'pdf_document': pdf_document,
        'pdf_pages': pdf_pages,
        'sections': sections,
        'contact_url': 'contact:contact',
        'admissions_url': 'admissions:list',
    }
    context.update(extra_context)
    return render(
        request,
        'about/page.html',
        context,
    )



# Legacy views for backwards compatibility
def mission(request):
    return page_detail(request, 'mission')


def vision(request):
    return page_detail(request, 'vision')


def principal_message(request):
    return page_detail(request, 'principal')


def history(request):
    """Standalone view for the MIS History page."""
    return render(request, 'about/history.html')

