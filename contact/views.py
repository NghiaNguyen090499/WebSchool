import json
import logging

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django_ratelimit.decorators import ratelimit
from .forms import ContactForm
from .models import ConsultationRequest, ChatbotLead
from core.validators import validate_vietnam_phone, get_phone_validation_error_message

# Configure logging
logger = logging.getLogger(__name__)


def ratelimited_error_json(request, exception):
    """Custom handler for rate-limited AJAX requests."""
    return JsonResponse({
        'success': False,
        'ok': False,
        'error': 'Bạn đã gửi quá nhiều yêu cầu. Vui lòng thử lại sau 1 phút.',
        'message': 'Bạn đã gửi quá nhiều yêu cầu. Vui lòng thử lại sau 1 phút.',
    }, status=429)


@ratelimit(key='ip', rate='10/m', method='POST', block=False)
def contact(request):
    """
    Contact form view with rate limiting.
    Limit: 10 submissions per minute per IP.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if getattr(request, "limited", False):
            messages.error(
                request,
                "Bạn thao tác quá nhanh. Vui lòng thử lại sau ít phút.",
            )
            return render(request, 'contact/contact.html', {'form': form}, status=429)
        if form.is_valid():
            contact_message = form.save()
            
            # Build interest summary
            interests = []
            if contact_message.interest_visit:
                interests.append('Hẹn lịch tham quan trường')
            if contact_message.interest_curriculum:
                interests.append('Tư vấn chương trình học')
            if contact_message.interest_admission_process:
                interests.append('Tư vấn quy trình tuyển sinh')
            interest_text = ', '.join(interests) if interests else 'Không chọn'
            
            # Send email notification
            try:
                grade_display = contact_message.get_grade_level_display() if contact_message.grade_level else 'Không chọn'
                send_mail(
                    subject=f'[MIS] Liên hệ mới: {contact_message.subject}',
                    message=f'''Có liên hệ mới từ website:

Họ tên: {contact_message.name}
Số điện thoại: {contact_message.phone or 'Không có'}
Email: {contact_message.email}
Chủ đề: {contact_message.subject}
Cấp học quan tâm: {grade_display}
Quan tâm: {interest_text}

Nội dung:
{contact_message.message}

Thời gian: {contact_message.created_at}
''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=False,
                )
            except Exception as e:
                # Log error but don't fail the form submission
                logger.warning(f"Failed to send contact email: {e}")
            
            messages.success(request, 'Cảm ơn bạn đã liên hệ! Chúng tôi sẽ phản hồi trong thời gian sớm nhất.')
            return redirect('contact:contact')
    else:
        form = ContactForm()
    
    return render(request, 'contact/contact.html', {'form': form})


@require_POST
@csrf_protect
@ratelimit(key='ip', rate='5/m', method='POST', block=False)
def submit_consultation(request):
    """
    Handle AJAX consultation form submission with rate limiting and phone validation.
    Limit: 5 submissions per minute per IP.
    """
    # Check if rate limited
    if getattr(request, 'limited', False):
        return JsonResponse({
            'success': False,
            'message': 'Bạn đã gửi quá nhiều yêu cầu. Vui lòng thử lại sau 1 phút.'
        }, status=429)
    
    try:
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip() or None
        grade_level = request.POST.get('grade_level', '').strip()
        message = request.POST.get('message', '').strip()
        
        # Validate required fields
        if not name or not phone or not grade_level:
            return JsonResponse({
                'success': False,
                'message': 'Vui lòng điền đầy đủ thông tin bắt buộc.'
            }, status=400)
        
        # Validate Vietnamese phone number
        if not validate_vietnam_phone(phone):
            error_msg = get_phone_validation_error_message(phone)
            return JsonResponse({
                'success': False,
                'message': error_msg
            }, status=400)
        
        # Validate grade level
        valid_grades = {choice[0] for choice in ConsultationRequest.GRADE_CHOICES}
        if grade_level not in valid_grades:
            return JsonResponse({
                'success': False,
                'message': 'Cấp học chọn không hợp lệ.'
            }, status=400)
        
        # Create consultation request with interest fields
        consultation = ConsultationRequest.objects.create(
            name=name,
            phone=phone,
            email=email,
            grade_level=grade_level,
            message=message,
            interest_visit=bool(request.POST.get('interest_visit')),
            interest_curriculum=bool(request.POST.get('interest_curriculum')),
            interest_admission_process=bool(request.POST.get('interest_admission_process')),
        )
        
        # Build interest summary for email
        interests = []
        if consultation.interest_visit:
            interests.append('Hẹn lịch tham quan trường')
        if consultation.interest_curriculum:
            interests.append('Tư vấn chương trình học')
        if consultation.interest_admission_process:
            interests.append('Tư vấn quy trình tuyển sinh')
        interest_text = ', '.join(interests) if interests else 'Không chọn'
        
        # Send email notification (optional)
        try:
            send_mail(
                subject=f'[MIS] Đăng ký tư vấn mới: {name}',
                message=f'''Có đăng ký tư vấn mới:

Họ tên: {name}
Số điện thoại: {phone}
Email: {email or 'Không có'}
Cấp học: {consultation.get_grade_level_display()}
Quan tâm: {interest_text}
Nội dung: {message or 'Không có'}

Thời gian: {consultation.created_at}
''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['c123mis@hanoiedu.vn'],
                fail_silently=True,
            )
        except Exception as e:
            logger.warning(f"Failed to send consultation email: {e}")
        
        return JsonResponse({
            'success': True,
            'message': 'Cảm ơn bạn đã đăng ký! Chúng tôi sẽ liên hệ trong thời gian sớm nhất.'
        })
        
    except Exception as e:
        logger.error(f"Error in submit_consultation: {e}")
        return JsonResponse({
            'success': False,
            'message': 'Có lỗi xảy ra. Vui lòng thử lại sau.'
        }, status=500)


@require_POST
@csrf_protect
@ratelimit(key='ip', rate='5/m', method='POST', block=False)
def submit_chatbot_lead(request):
    """
    Handle chatbot contact submissions with rate limiting and phone validation.
    Limit: 5 submissions per minute per IP.
    """
    # Check if rate limited
    if getattr(request, 'limited', False):
        return JsonResponse({
            'ok': False,
            'error': 'Bạn đã gửi quá nhiều yêu cầu. Vui lòng thử lại sau 1 phút.'
        }, status=429)
    
    try:
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body.decode('utf-8'))
            except (json.JSONDecodeError, UnicodeDecodeError):
                data = {}
        else:
            data = request.POST

        name = str(data.get('name', '')).strip()
        phone = str(data.get('phone', '')).strip()
        email = str(data.get('email', '')).strip()
        message = str(data.get('message', '')).strip()
        grade_level = str(data.get('grade_level', '')).strip()

        if not name or not phone or not grade_level:
            return JsonResponse({
                'ok': False,
                'error': 'Vui lòng nhập đầy đủ họ tên, số điện thoại và cấp học quan tâm.'
            }, status=400)

        # Validate Vietnamese phone number
        if not validate_vietnam_phone(phone):
            error_msg = get_phone_validation_error_message(phone)
            return JsonResponse({
                'ok': False,
                'error': error_msg
            }, status=400)

        valid_grades = {choice[0] for choice in ConsultationRequest.GRADE_CHOICES}
        if grade_level not in valid_grades:
            return JsonResponse({
                'ok': False,
                'error': 'Cấp học chọn không hợp lệ.'
            }, status=400)

        if email and '@' not in email:
            return JsonResponse({
                'ok': False,
                'error': 'Email không hợp lệ. Vui lòng kiểm tra lại.'
            }, status=400)

        ConsultationRequest.objects.create(
            name=name,
            phone=phone,
            email=email or None,
            grade_level=grade_level,
            message=message,
        )

        return JsonResponse({
            'ok': True,
            'message': 'Cảm ơn bạn đã đăng ký! Chúng tôi sẽ liên hệ trong thời gian sớm nhất.'
        })
    except Exception as e:
        logger.error(f"Error in submit_chatbot_lead: {e}")
        return JsonResponse({
            'ok': False,
            'error': 'Có lỗi xảy ra. Vui lòng thử lại sau.'
        }, status=500)


@require_POST
@csrf_protect
@ratelimit(key='ip', rate='10/m', method='POST', block=False)
def submit_chatbot_lead_info(request):
    """
    Capture lead name and phone before the conversation.
    Limit: 10 submissions per minute per IP (higher for chatbot interaction).
    """
    # Check if rate limited
    if getattr(request, 'limited', False):
        return JsonResponse({
            'ok': False,
            'error': 'Bạn đã gửi quá nhiều yêu cầu. Vui lòng thử lại sau 1 phút.'
        }, status=429)
    
    try:
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body.decode('utf-8'))
            except (json.JSONDecodeError, UnicodeDecodeError):
                data = {}
        else:
            data = request.POST

        name = str(data.get('name', '')).strip()
        phone = str(data.get('phone', '')).strip()
        email = str(data.get('email', '')).strip()

        if not name or not phone:
            return JsonResponse({
                'ok': False,
                'error': 'Vui lòng nhập đầy đủ tên và số điện thoại trước.'
            }, status=400)

        # Validate Vietnamese phone number
        if not validate_vietnam_phone(phone):
            error_msg = get_phone_validation_error_message(phone)
            return JsonResponse({
                'ok': False,
                'error': error_msg
            }, status=400)

        ChatbotLead.objects.create(
            name=name,
            phone=phone,
            email=email or None,
        )

        return JsonResponse({
            'ok': True,
            'message': 'Cảm ơn! Thông tin đã được lưu, tiếp tục gửi câu hỏi nếu cần.'
        })
    except Exception as e:
        logger.error(f"Error in submit_chatbot_lead_info: {e}")
        return JsonResponse({
            'ok': False,
            'error': 'Có lỗi xảy ra. Vui lòng thử lại sau.'
        }, status=500)
