import logging

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import F
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django_ratelimit.decorators import ratelimit

from .models import (
    AdmissionInfo,
    AdmissionRegistration,
    RegistrationSibling,
    AdmissionConsultation,
    AdmissionDocument,
    TRAINING_PROGRAM_CHOICES,
    ADMISSION_METHOD_CHOICES,
    TARGET_GRADE_CHOICES,
    CONTACT_RELATIONSHIP_CHOICES,
    SCHOOL_YEAR_CHOICES,
)
from .forms import AdmissionRegistrationForm, AdmissionConsultationForm
from core.utils.program_content import get_program_metadata, get_program_year

# Configure logging
logger = logging.getLogger(__name__)
PROGRAM_YEAR = get_program_year()
ADMISSIONS_META = get_program_metadata('admissions')
ADMISSIONS_POLICY_STATUS = ADMISSIONS_META.get('policy_status', 'NEED_CONFIRM')
ADMISSIONS_NOTICE_STATUS = ADMISSIONS_META.get('official_notice_status', 'NEED_CONFIRM')
ADMISSIONS_NOTICE_URLS = ADMISSIONS_META.get('official_notice_urls', {})


def _notice_url(key):
    if not isinstance(ADMISSIONS_NOTICE_URLS, dict):
        return None
    candidate = ADMISSIONS_NOTICE_URLS.get(key)
    if isinstance(candidate, str):
        candidate = candidate.strip()
    return candidate or None

# Official admission announcement sources (MISVN)
OFFICIAL_ADMISSION_NOTICES = {
    'mam_non': {
        'level': 'mam_non',
        'title': f'Thông tin tuyển sinh Mầm non - Tiền tiểu học năm học {PROGRAM_YEAR}',
        'year': PROGRAM_YEAR,
        'url': _notice_url('mam_non'),
        'status': ADMISSIONS_NOTICE_STATUS,
        'image_urls': [
            'images/admissions/misvn/mam_non/TTTSMN-25-26_001-2.jpg',
            'images/admissions/misvn/mam_non/TTTSMN-25-26_002-2.jpg',
            'images/admissions/misvn/mam_non/TTTSMN-25-26_003-2.jpg',
            'images/admissions/misvn/mam_non/TTTSMN-25-26_004-2.jpg',
            'images/admissions/misvn/mam_non/TTTSMN-25-26_005-2.jpg',
        ],
        'image_url': 'images/admissions/notices/mam-non.png',
    },
    'tieu_hoc': {
        'level': 'tieu_hoc',
        'title': f'Thông tin tuyển sinh Tiểu học năm học {PROGRAM_YEAR}',
        'year': PROGRAM_YEAR,
        'url': _notice_url('tieu_hoc'),
        'status': ADMISSIONS_NOTICE_STATUS,
        'image_urls': [
            'images/admissions/misvn/tieu_hoc/TTTSTH2025-2026-ngay22-04_001.jpg',
            'images/admissions/misvn/tieu_hoc/TTTSTH2025-2026-ngay-7-5_001.jpg',
            'images/admissions/misvn/tieu_hoc/TTTSTH2025-2026-ngay-7-5_002.jpg',
            'images/admissions/misvn/tieu_hoc/TTTSTH2025-2026-ngay-7-5_003.jpg',
            'images/admissions/misvn/tieu_hoc/TTTSTH2025-2026-ngay-7-5_004.jpg',
            'images/admissions/misvn/tieu_hoc/TTTSTH2025-2026-ngay-7-5_005.jpg',
            'images/admissions/misvn/tieu_hoc/TTTSTH2025-2026-ngay-7-5_006.jpg',
            'images/admissions/misvn/tieu_hoc/TTTSTH2025-2026-ngay-7-5_007.jpg',
            'images/admissions/misvn/tieu_hoc/TTTSTH2025-2026-ngay-7-5_008.jpg',
            'images/admissions/misvn/tieu_hoc/TTTSTH2025-2026-ngay-7-5_009.jpg',
            'images/admissions/misvn/tieu_hoc/TTTSTH2025-2026-ngay-7-5_010.jpg',
            'images/admissions/misvn/tieu_hoc/TTTSTH2025-2026-ngay-7-5_011.jpg',
            'images/admissions/misvn/tieu_hoc/TTTSTH2025-2026-ngay-7-5_012.jpg',
        ],
        'image_url': 'images/admissions/notices/tieu-hoc.png',
    },
    'thcs': {
        'level': 'thcs',
        'title': f'Thông tin tuyển sinh Trung học cơ sở năm học {PROGRAM_YEAR}',
        'year': PROGRAM_YEAR,
        'url': _notice_url('thcs'),
        'status': ADMISSIONS_NOTICE_STATUS,
        'image_urls': [
            'images/admissions/misvn/thcs/TTthcs.png',
            'images/admissions/misvn/thcs/Artboard-1@2x-9.png',
            'images/admissions/misvn/thcs/Artboard-2@2x-8.png',
            'images/admissions/misvn/thcs/Artboard-3@2x-6.png',
            'images/admissions/misvn/thcs/Artboard-4@2x-6.png',
            'images/admissions/misvn/thcs/Artboard-5@2x-6.png',
            'images/admissions/misvn/thcs/Artboard-6@2x-6.png',
            'images/admissions/misvn/thcs/Artboard-7@2x-6.png',
            'images/admissions/misvn/thcs/Artboard-8@2x-6.png',
            'images/admissions/misvn/thcs/Artboard-9@2x-6.png',
            'images/admissions/misvn/thcs/Artboard-14@2x-4.png',
            'images/admissions/misvn/thcs/Artboard-15@2x-5.png',
            'images/admissions/misvn/thcs/Artboard-17@2x-2.png',
            'images/admissions/misvn/thcs/Artboard-18@2x-2.png',
            'images/admissions/misvn/thcs/Artboard-18-copy@2x-1.png',
        ],
        'image_url': 'images/admissions/notices/thcs.png',
    },
    'thpt': {
        'level': 'thpt',
        'title': f'Thông tin tuyển sinh Trung học phổ thông năm học {PROGRAM_YEAR}',
        'year': PROGRAM_YEAR,
        'url': _notice_url('thpt'),
        'status': ADMISSIONS_NOTICE_STATUS,
        'image_urls': [
            'images/admissions/misvn/thpt/Asset-2.png',
            'images/admissions/misvn/thpt/Artboard-1@2x-8.png',
            'images/admissions/misvn/thpt/Artboard-2@2x-7.png',
            'images/admissions/misvn/thpt/Artboard-3@2x-5.png',
            'images/admissions/misvn/thpt/Artboard-4@2x-5.png',
            'images/admissions/misvn/thpt/Artboard-5@2x-5.png',
            'images/admissions/misvn/thpt/Artboard-6@2x-5.png',
            'images/admissions/misvn/thpt/Artboard-7@2x-5.png',
            'images/admissions/misvn/thpt/Artboard-8@2x-5.png',
            'images/admissions/misvn/thpt/Artboard-9@2x-5.png',
            'images/admissions/misvn/thpt/Artboard-14@2x-3.png',
            'images/admissions/misvn/thpt/Artboard-15@2x-4.png',
            'images/admissions/misvn/thpt/Artboard-16@2x.png',
            'images/admissions/misvn/thpt/Artboard-17@2x-1.png',
            'images/admissions/misvn/thpt/Artboard-17-copy@2x.png',
            'images/admissions/misvn/thpt/Artboard-18@2x-1.png',
        ],
        'image_url': 'images/admissions/notices/thpt.png',
    },
    'policy': {
        'level': 'policy',
        'title': f'Chính sách tuyển sinh bổ sung năm học {PROGRAM_YEAR}',
        'year': PROGRAM_YEAR,
        'url': _notice_url('policy'),
        'status': ADMISSIONS_POLICY_STATUS,
        'image_urls': [
            'images/admissions/misvn/policy/Asset-1.png',
            'images/admissions/misvn/policy/Artboard-1@2x-11.png',
            'images/admissions/misvn/policy/Artboard-2@2x-10.png',
        ],
        'image_url': 'images/admissions/notices/policy.png',
    },
}


def _registration_context():
    return {
        'training_programs': TRAINING_PROGRAM_CHOICES,
        'admission_methods': ADMISSION_METHOD_CHOICES,
        'target_grades': TARGET_GRADE_CHOICES,
        'contact_relationships': CONTACT_RELATIONSHIP_CHOICES,
        'school_years': SCHOOL_YEAR_CHOICES,
        'gender_choices': AdmissionRegistration.GENDER_CHOICES,
    }


def admission_list(request):
    """Trang tổng quan tuyển sinh - hiển thị tất cả các cấp học"""
    admissions = AdmissionInfo.objects.filter(is_active=True)
    featured = admissions.filter(is_featured=True).first()
    first_admission = admissions.first()
    active_level = featured.level if featured else (first_admission.level if first_admission else "")

    official_policy_notice = OFFICIAL_ADMISSION_NOTICES['policy']
    official_level_notices = [
        OFFICIAL_ADMISSION_NOTICES['mam_non'],
        OFFICIAL_ADMISSION_NOTICES['tieu_hoc'],
        OFFICIAL_ADMISSION_NOTICES['thcs'],
        OFFICIAL_ADMISSION_NOTICES['thpt'],
    ]

    context = {
        'admissions': admissions,
        'featured': featured,
        'active_level': active_level,
        'page_title': 'Tuyển sinh',
        'page_subtitle': 'Thông tin tuyển sinh các cấp học theo thông báo mới nhất',
        'official_policy_notice': official_policy_notice,
        'official_level_notices': official_level_notices,
        'admissions_policy_status': ADMISSIONS_POLICY_STATUS,
        'admissions_notice_status': ADMISSIONS_NOTICE_STATUS,
    }
    context.update(_registration_context())
    return render(request, 'admissions/admission_list.html', context)


def admission_detail(request, level):
    """Trang chi tiết tuyển sinh từng cấp học"""
    admission = get_object_or_404(AdmissionInfo, level=level, is_active=True)
    other_admissions = AdmissionInfo.objects.filter(is_active=True).exclude(level=level)[:3]

    # Lấy danh sách tài liệu tuyển sinh của cấp học này
    documents = AdmissionDocument.objects.filter(
        admission=admission,
        is_active=True
    ).order_by('order', '-created_at')

    highlights = [
        h for h in admission.highlights.all()
        if '{{' not in (h.title or '') and '{{' not in (h.description or '')
    ]

    context = {
        'admission': admission,
        'highlights': highlights,
        'documents': documents,
        'other_admissions': other_admissions,
        'official_notice': OFFICIAL_ADMISSION_NOTICES.get(admission.level),
    }
    return render(request, 'admissions/admission_detail.html', context)


def registration_page(request):
    """Legacy route for the unified admissions form."""
    return render(request, 'admissions/registration_page.html')


def download_document(request, pk):
    """Tăng download_count và chuyển hướng đến file tài liệu."""
    document = get_object_or_404(AdmissionDocument, pk=pk, is_active=True)
    if not document.file:
        raise Http404("Document file not found")
    AdmissionDocument.objects.filter(pk=document.pk).update(
        download_count=F('download_count') + 1
    )
    return redirect(document.file.url)


@require_POST
@csrf_protect
@ratelimit(key='ip', rate='3/m', method='POST', block=False)
def submit_registration(request):
    """
    API xử lý đăng ký dự tuyển qua AJAX — hỗ trợ file upload + siblings.
    Limit: 3 submissions per minute per IP.
    """
    if getattr(request, 'limited', False):
        return JsonResponse({
            'success': False,
            'message': 'Bạn đã gửi quá nhiều yêu cầu. Vui lòng thử lại sau 1 phút.'
        }, status=429)

    try:
        # Lấy admission (dựa trên target_grade → map sang cấp học)
        level = request.POST.get('level', '')
        if not level:
            # Auto-detect level from target_grade
            target_grade = request.POST.get('target_grade', '')
            level = _grade_to_level(target_grade)

        admission = get_object_or_404(AdmissionInfo, level=level, is_active=True)

        form = AdmissionRegistrationForm(request.POST, request.FILES)
        if not form.is_valid():
            error_message = ""
            for field_name, errors in form.errors.items():
                if errors:
                    error_message = errors[0]
                    break
            if not error_message:
                error_message = 'Vui lòng điền đầy đủ thông tin bắt buộc.'
            return JsonResponse({
                'success': False,
                'message': error_message,
                'errors': form.errors,
            }, status=400)

        cleaned = form.cleaned_data

        registration = AdmissionRegistration.objects.create(
            admission=admission,
            # 1. Thông tin học sinh
            student_name=cleaned.get('student_name', '').strip(),
            student_dob=cleaned.get('student_dob'),
            student_gender=cleaned.get('student_gender'),
            address=cleaned.get('address', '').strip(),
            current_school=cleaned.get('current_school', '').strip(),
            current_grade=cleaned.get('current_grade', '').strip(),
            # 2. Chương trình & hệ đào tạo
            target_grade=cleaned.get('target_grade', ''),
            training_program=cleaned.get('training_program', ''),
            registration_school_year=cleaned.get('registration_school_year', ''),
            admission_method=cleaned.get('admission_method', ''),
            transcript_file=cleaned.get('transcript_file'),
            # 3. Thông tin bổ sung
            study_abroad_plan=cleaned.get('study_abroad_plan', 'false') == 'true',
            favorite_subjects=cleaned.get('favorite_subjects', '').strip(),
            best_subject=cleaned.get('best_subject', '').strip(),
            achievements=cleaned.get('achievements', '').strip(),
            talent_subjects=cleaned.get('talent_subjects', '').strip(),
            # 4. Dịch vụ
            register_shuttle=cleaned.get('register_shuttle', False),
            register_dayboarding=cleaned.get('register_dayboarding', False),
            register_boarding=cleaned.get('register_boarding', False),
            # 5. Người liên hệ
            parent_name=cleaned.get('parent_name', '').strip(),
            contact_relationship=cleaned.get('contact_relationship', ''),
            parent_phone=cleaned.get('parent_phone', '').strip(),
            parent_email=cleaned.get('parent_email', '').strip(),
            referrer=cleaned.get('referrer', '').strip(),
            # 6. Giữ tương thích
            district=cleaned.get('district', '').strip(),
            city=(cleaned.get('city') or 'Hà Nội').strip(),
            how_did_you_know=cleaned.get('how_did_you_know', '').strip(),
            note=cleaned.get('note', '').strip(),
            interest_visit=cleaned.get('interest_visit', False),
            interest_curriculum=cleaned.get('interest_curriculum', False),
            interest_admission_process=cleaned.get('interest_admission_process', False),
        )

        # Lưu siblings
        siblings_data = cleaned.get('siblings_json', [])
        for sib in siblings_data:
            RegistrationSibling.objects.create(
                registration=registration,
                full_name=sib['full_name'].strip(),
                date_of_birth=sib['date_of_birth'],
                gender=sib['gender'],
                current_school=sib['current_school'].strip(),
            )

        logger.info(f"New admission registration: {registration.id} - {registration.student_name}")

        return JsonResponse({
            'success': True,
            'message': 'Cảm ơn bạn đã đăng ký! Chúng tôi sẽ liên hệ trong thời gian sớm nhất.',
            'registration_id': registration.id,
        })

    except Exception as e:
        logger.error(f"Error in submit_registration: {e}", exc_info=True)
        return JsonResponse({
            'success': False,
            'message': 'Có lỗi xảy ra. Vui lòng thử lại sau hoặc liên hệ hotline 024 60 278 666.'
        }, status=500)


@require_POST
@csrf_protect
@ratelimit(key='ip', rate='5/m', method='POST', block=False)
def submit_consultation(request):
    """
    API xử lý đăng ký tư vấn qua AJAX.
    Limit: 5 submissions per minute per IP.
    """
    if getattr(request, 'limited', False):
        return JsonResponse({
            'success': False,
            'message': 'Bạn đã gửi quá nhiều yêu cầu. Vui lòng thử lại sau 1 phút.'
        }, status=429)

    try:
        form = AdmissionConsultationForm(request.POST)
        if not form.is_valid():
            error_message = ""
            for errors in form.errors.values():
                if errors:
                    error_message = errors[0]
                    break
            if not error_message:
                error_message = 'Vui lòng điền đầy đủ thông tin bắt buộc.'
            return JsonResponse({
                'success': False,
                'message': error_message,
                'errors': form.errors,
            }, status=400)

        cleaned = form.cleaned_data

        consultation = AdmissionConsultation.objects.create(
            target_grade=cleaned.get('target_grade', ''),
            training_program=cleaned.get('training_program', ''),
            details=cleaned.get('details', '').strip(),
            interest_visit=cleaned.get('interest_visit', False),
            interest_curriculum=cleaned.get('interest_curriculum', False),
            interest_admission_process=cleaned.get('interest_admission_process', False),
            parent_name=cleaned.get('parent_name', '').strip(),
            phone=cleaned.get('phone', '').strip(),
            email=cleaned.get('email', '').strip(),
        )

        logger.info(f"New admission consultation: {consultation.id} - {consultation.parent_name}")

        return JsonResponse({
            'success': True,
            'message': 'Cảm ơn bạn đã đăng ký tư vấn! Bộ phận tuyển sinh sẽ liên hệ trong thời gian sớm nhất.',
            'consultation_id': consultation.id,
        })

    except Exception as e:
        logger.error(f"Error in submit_consultation: {e}", exc_info=True)
        return JsonResponse({
            'success': False,
            'message': 'Có lỗi xảy ra. Vui lòng thử lại sau hoặc liên hệ hotline 024 60 278 666.'
        }, status=500)


def _grade_to_level(target_grade):
    """Map target_grade choice → AdmissionInfo.level."""
    mapping = {
        'mam_non': 'mam_non',
        'tien_tieu_hoc': 'mam_non',
        'lop_1': 'tieu_hoc',
        'lop_2': 'tieu_hoc',
        'lop_3': 'tieu_hoc',
        'lop_4': 'tieu_hoc',
        'lop_5': 'tieu_hoc',
        'lop_6': 'thcs',
        'lop_7': 'thcs',
        'lop_8': 'thcs',
        'lop_9': 'thcs',
        'lop_10': 'thpt',
        'lop_11': 'thpt',
        'lop_12': 'thpt',
    }
    return mapping.get(target_grade, 'tieu_hoc')
