from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'about'

urlpatterns = [
    # Legacy URLs (keep for backwards compatibility)
    path('mission/', views.mission, name='mission'),
    path('vision/', views.vision, name='vision'),
    path('principal/', views.principal_message, name='principal'),
    
    # New content pages
    path('strengths/', views.page_detail, {'page_type': 'strengths'}, name='strengths'),
    path('strategy/', views.page_detail, {'page_type': 'strategy'}, name='strategy'),
    path(
        'strategy-2025-2028/',
        views.page_detail,
        {'page_type': 'strategy_2025_2028'},
        name='strategy_2025_2028',
    ),
    path('structure/', views.page_detail, {'page_type': 'structure'}, name='structure'),
    path('culture/', views.page_detail, {'page_type': 'culture'}, name='culture'),
    path('boarding/', views.page_detail, {'page_type': 'boarding'}, name='boarding'),
    path('happiness/', views.page_detail, {'page_type': 'happiness'}, name='happiness'),
    path('liberal/', views.page_detail, {'page_type': 'liberal'}, name='liberal'),
    path(
        'vision-2033/',
        views.page_detail,
        {'page_type': 'vision_2033'},
        name='vision_2033',
    ),
    path(
        'future-ai/',
        views.page_detail,
        {'page_type': 'future_ai'},
        name='future_ai',
    ),
    path('whymis/', views.page_detail, {'page_type': 'whymis'}, name='whymis'),
    path('partners/', views.page_detail, {'page_type': 'partners'}, name='partners'),
    path('history/', views.history, name='history'),
    
    # Academics - redirect to MIS prototype pages
    path(
        'academics/',
        RedirectView.as_view(pattern_name='core:mis_lowfi_home', permanent=True),
        name='academics',
    ),
    path(
        'academics/preschool/',
        RedirectView.as_view(pattern_name='core:mis_lowfi_page', permanent=True),
        {'page_key': 'preparation'},
        name='preschool',
    ),
    path(
        'academics/primary/',
        RedirectView.as_view(pattern_name='core:mis_lowfi_page', permanent=True),
        {'page_key': 'primary'},
        name='primary',
    ),
    path(
        'academics/middle/',
        RedirectView.as_view(pattern_name='core:mis_lowfi_page', permanent=True),
        {'page_key': 'thcs'},
        name='middle',
    ),
    path(
        'academics/high/',
        RedirectView.as_view(pattern_name='core:mis_lowfi_page', permanent=True),
        {'page_key': 'thpt'},
        name='high',
    ),
    
    # Curriculum overview pages
    path('curriculum/math/', views.page_detail, {'page_type': 'overview_math'}, name='overview_math'),
    path('curriculum/literature/', views.page_detail, {'page_type': 'overview_literature'}, name='overview_literature'),
    path('curriculum/english/', views.page_detail, {'page_type': 'overview_english'}, name='overview_english'),
    path('curriculum/chinese/', views.page_detail, {'page_type': 'overview_chinese'}, name='overview_chinese'),

    # Specialized programs
    path('curriculum/tnst/', views.page_detail, {'page_type': 'tnst'}, name='tnst'),
    path('curriculum/steam/', views.page_detail, {'page_type': 'steam'}, name='steam'),
    path('curriculum/robotics/', views.page_detail, {'page_type': 'robotics'}, name='robotics'),
    path('curriculum/lifeskills/', views.page_detail, {'page_type': 'lifeskills'}, name='lifeskills'),
    path('curriculum/creative-movement/', views.page_detail, {'page_type': 'creative_movement'}, name='creative_movement'),
    path('edtech/', views.page_detail, {'page_type': 'edtech'}, name='edtech'),

    # Schedule pages
    path('schedule/2026-2027/', views.page_detail, {'page_type': 'schedule_2026'}, name='schedule_2026'),
    path('schedule/hd-2026-2027/', views.page_detail, {'page_type': 'schedule_hd'}, name='schedule_hd_2026'),
    path('schedule/2026-2027/', views.page_detail, {'page_type': 'schedule_2026'}, name='schedule_2025'),
    path('schedule/hd-2026-2027/', views.page_detail, {'page_type': 'schedule_hd'}, name='schedule_hd'),
    path(
        'schedule/2025-2026/',
        RedirectView.as_view(pattern_name='about:schedule_2026', permanent=True),
        name='schedule_2025_legacy',
    ),
    path(
        'schedule/hd-2025-2026/',
        RedirectView.as_view(pattern_name='about:schedule_hd_2026', permanent=True),
        name='schedule_hd_legacy',
    ),
]
