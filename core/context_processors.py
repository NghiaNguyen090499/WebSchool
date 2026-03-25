from django.db.models import Prefetch
from .models import MenuItem, SchoolInfo, Campus
from core.utils.program_content import (
    get_program_metadata,
    get_program_year,
    resolve_navigation,
)

def global_menus(request):
    """
    Make database-driven menus and school info available in all templates.
    """
    school_info = SchoolInfo.get_active()
    campuses = Campus.objects.filter(is_active=True).order_by('order', 'name')
    if school_info:
        campuses = campuses.filter(school=school_info)
    primary_campus = campuses.filter(is_primary=True).first() or campuses.first()
    contact_email = ''
    contact_hotline = ''
    fallback_address = ''
    if school_info:
        contact_email = school_info.admissions_email or school_info.general_email or ''
        contact_hotline = school_info.hotline or ''
        fallback_address = school_info.address or ''
    if not contact_hotline:
        contact_hotline = '024 60 278 666'
    if not contact_email:
        contact_email = 'c123mis@hanoiedu.vn'
    campus_items = [
        {
            'name': campus.name,
            'address': campus.address,
            'phone': campus.phone,
            'email': campus.email,
        }
        for campus in campuses
    ]
    active_grandchildren = Prefetch(
        'children',
        queryset=MenuItem.objects.filter(is_active=True).order_by('order'),
        to_attr='prefetched_children',
    )
    active_children = Prefetch(
        'children',
        queryset=MenuItem.objects.filter(is_active=True).order_by('order').prefetch_related(active_grandchildren),
        to_attr='prefetched_children',
    )
    return {
        'header_menu': MenuItem.objects.filter(
            position='header',
            is_active=True,
            parent=None
        ).prefetch_related(active_children),

        'footer_menu': MenuItem.objects.filter(
            position='footer',
            is_active=True,
            parent=None
        ).prefetch_related(active_children),

        'school_info': school_info,
        'campuses': campuses,
        'primary_campus': primary_campus,
        'contact_email': contact_email,
        'contact_hotline': contact_hotline,
        'contact_info': {
            'email': contact_email,
            'hotline': contact_hotline,
            'campuses': campus_items,
            'fallback_address': fallback_address,
        },
        'program_year': get_program_year(),
        'about_links': resolve_navigation('about'),
        'program_overview_links': resolve_navigation('program_overview'),
        'specialized_program_links': resolve_navigation('specialized_programs'),
        'program_schedule_config': get_program_metadata('schedule'),
    }
