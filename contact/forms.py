from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = [
            'name', 'phone', 'email',
            'grade_level', 'message',
            'interest_visit', 'interest_curriculum', 'interest_admission_process',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nguyễn Văn A'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '0912 345 678'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'email@example.com'
            }),
            'grade_level': forms.Select(attrs={
                'class': 'form-select',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-textarea resize-none',
                'rows': 3,
                'placeholder': 'Nhập nội dung bạn muốn liên hệ...'
            }),
            'interest_visit': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 rounded border-neutral-300 text-red-600 focus:ring-red-500 cursor-pointer',
            }),
            'interest_curriculum': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 rounded border-neutral-300 text-red-600 focus:ring-red-500 cursor-pointer',
            }),
            'interest_admission_process': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 rounded border-neutral-300 text-red-600 focus:ring-red-500 cursor-pointer',
            }),
        }
