from django import forms
from .models import TimetableUpload

class TimetableUploadForm(forms.ModelForm):
    class Meta:
        model = TimetableUpload
        fields = ['title', 'zip_file']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-neutral-300 focus:outline-none focus:ring-2 focus:ring-red-500',
                'placeholder': 'VD: TKB Mới Nhất 30/04/2026'
            }),
            'zip_file': forms.ClearableFileInput(attrs={
                'class': 'w-full text-sm text-neutral-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-red-50 file:text-red-700 hover:file:bg-red-100',
                'accept': '.zip'
            })
        }
