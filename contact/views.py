from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from .forms import ContactForm
from .models import ConsultationRequest


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            
            # Send email notification
            try:
                send_mail(
                    subject=f'New Contact Form: {contact_message.subject}',
                    message=f'From: {contact_message.name} ({contact_message.email})\n\n{contact_message.message}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=False,
                )
            except Exception as e:
                # Log error but don't fail the form submission
                pass
            
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact:contact')
    else:
        form = ContactForm()
    
    return render(request, 'contact/contact.html', {'form': form})


@require_POST
@csrf_protect
def submit_consultation(request):
    """Handle AJAX consultation form submission"""
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
        
        # Create consultation request
        consultation = ConsultationRequest.objects.create(
            name=name,
            phone=phone,
            email=email,
            grade_level=grade_level,
            message=message
        )
        
        # Send email notification (optional)
        try:
            send_mail(
                subject=f'[MIS] Đăng ký tư vấn mới: {name}',
                message=f'''
Có đăng ký tư vấn mới:

Họ tên: {name}
Số điện thoại: {phone}
Email: {email or 'Không có'}
Cấp học: {consultation.get_grade_level_display()}
Nội dung: {message or 'Không có'}

Thời gian: {consultation.created_at}
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['c123mis@hanoiedu.vn'],
                fail_silently=True,
            )
        except:
            pass
        
        return JsonResponse({
            'success': True,
            'message': 'Cảm ơn bạn đã đăng ký! Chúng tôi sẽ liên hệ trong thời gian sớm nhất.'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Có lỗi xảy ra. Vui lòng thử lại sau.'
        }, status=500)

