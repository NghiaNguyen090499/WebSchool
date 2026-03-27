from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('thanh-tich-noi-bat/', views.achievement_list, name='achievements'),
    path('prototype/mis/', views.mis_lowfi_page, name='mis_lowfi_home'),
    path('prototype/mis/<slug:page_key>/', views.mis_lowfi_page, name='mis_lowfi_page'),
    path('he-dao-tao/', views.training_programs_list, name='training_programs'),
    path('he-dao-tao/<slug:slug>/', views.training_program_detail, name='training_program_detail'),
    path(
        'chuong-trinh-tong-quan-mon-toan/',
        views.program_overview_detail,
        {'slug': 'chuong-trinh-tong-quan-mon-toan'},
        name='program_overview_math',
    ),
    path(
        'tong-quan-chuong-trinh-ngu-van-tai-mis/',
        views.program_overview_detail,
        {'slug': 'tong-quan-chuong-trinh-ngu-van-tai-mis'},
        name='program_overview_literature',
    ),
    path(
        'tong-quan-chuong-trinh-tieng-anh/',
        views.program_overview_detail,
        {'slug': 'tong-quan-chuong-trinh-tieng-anh'},
        name='program_overview_english',
    ),
    path(
        'chuong-trinh-tong-quan-trai-nghiem-sang-tao-tnst/',
        views.program_overview_detail,
        {'slug': 'chuong-trinh-tong-quan-trai-nghiem-sang-tao-tnst'},
        name='program_overview_tnst',
    ),
    path(
        'chuong-trinh-steam-voi-cong-nghe-sang-tao/',
        views.program_overview_detail,
        {'slug': 'chuong-trinh-steam-voi-cong-nghe-sang-tao'},
        name='program_overview_steam',
    ),
    path(
        'tong-quan-chuong-trinh-tieng-trung-2/',
        views.program_overview_detail,
        {'slug': 'tong-quan-chuong-trinh-tieng-trung-2'},
        name='program_overview_chinese',
    ),
    path(
        'chuong-trinh-ky-nang-song-nam-hoc-2026-2027/',
        views.program_overview_detail,
        {'slug': 'chuong-trinh-ky-nang-song-nam-hoc-2026-2027'},
        name='program_overview_lifeskills',
    ),
    path(
        'chuong-trinh-ky-nang-song-nam-hoc-2022-2023/',
        views.program_overview_detail,
        {'slug': 'chuong-trinh-ky-nang-song-nam-hoc-2022-2023'},
        name='program_overview_lifeskills_legacy',
    ),
    path('doi-song-hoc-sinh/', views.student_life, name='student_life'),
    path('guong-mat-misers/', views.student_spotlight_list, name='student_spotlight'),
    path('triet-ly-giao-duc/', views.pillar_list, name='pillars'),
    path('gia-tri-cot-loi/', views.core_values, name='core_values'),
    path('co-so-vat-chat/', views.facility_list, name='facilities'),
    path('tieng-noi-misers/', views.podcast_list, name='podcasts'),
    path('healthz/', views.healthz, name='healthz'),
    path('readyz/', views.readyz, name='readyz'),
    path('cap-nhat-tkb/', views.upload_timetable, name='upload_timetable'),
]
