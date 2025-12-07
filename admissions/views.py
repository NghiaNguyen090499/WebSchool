from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from .models import AdmissionInfo, AdmissionRegistration


def admission_list(request):
    """Trang tổng quan tuyển sinh - hiển thị tất cả các cấp học"""
    admissions = AdmissionInfo.objects.filter(is_active=True)
    featured = admissions.filter(is_featured=True).first()
    
    context = {
        'admissions': admissions,
        'featured': featured,
        'page_title': 'Tuyển sinh',
        'page_subtitle': 'Thông tin tuyển sinh các cấp học năm 2025-2026',
    }
    return render(request, 'admissions/admission_list.html', context)


def admission_detail(request, level):
    """Trang chi tiết tuyển sinh từng cấp học"""
    admission = get_object_or_404(AdmissionInfo, level=level, is_active=True)
    other_admissions = AdmissionInfo.objects.filter(is_active=True).exclude(level=level)[:3]
    
    context = {
        'admission': admission,
        'highlights': admission.highlights.all(),
        'other_admissions': other_admissions,
    }
    return render(request, 'admissions/admission_detail.html', context)


@require_POST
@csrf_protect
def submit_registration(request):
    """API xử lý đăng ký tuyển sinh qua AJAX"""
    try:
        # Lấy admission
        level = request.POST.get('level')
        admission = get_object_or_404(AdmissionInfo, level=level, is_active=True)
        
        # Parse ngày sinh
        dob_str = request.POST.get('student_dob')
        try:
            student_dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return JsonResponse({
                'success': False,
                'message': 'Ngày sinh không hợp lệ. Vui lòng nhập đúng định dạng.'
            })
        
        # Validate required fields
        required_fields = ['parent_name', 'parent_phone', 'student_name', 'student_gender', 'address']
        for field in required_fields:
            if not request.POST.get(field):
                return JsonResponse({
                    'success': False,
                    'message': f'Vui lòng điền đầy đủ thông tin bắt buộc.'
                })
        
        # Tạo đơn đăng ký
        registration = AdmissionRegistration.objects.create(
            admission=admission,
            parent_name=request.POST.get('parent_name', '').strip(),
            parent_phone=request.POST.get('parent_phone', '').strip(),
            parent_email=request.POST.get('parent_email', '').strip(),
            student_name=request.POST.get('student_name', '').strip(),
            student_dob=student_dob,
            student_gender=request.POST.get('student_gender'),
            current_school=request.POST.get('current_school', '').strip(),
            current_grade=request.POST.get('current_grade', '').strip(),
            address=request.POST.get('address', '').strip(),
            district=request.POST.get('district', '').strip(),
            city=request.POST.get('city', 'Hà Nội').strip(),
            how_did_you_know=request.POST.get('how_did_you_know', '').strip(),
            note=request.POST.get('note', '').strip(),
        )
        
        return JsonResponse({
            'success': True,
            'message': f'Cảm ơn bạn đã đăng ký! Chúng tôi sẽ liên hệ trong thời gian sớm nhất.',
            'registration_id': registration.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Có lỗi xảy ra. Vui lòng thử lại sau hoặc liên hệ hotline 024 60 278 666.'
        })
