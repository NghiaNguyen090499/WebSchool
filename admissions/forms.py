from django import forms

from core.validators import (
    validate_vietnam_phone,
    get_phone_validation_error_message,
    normalize_phone_number,
)
from .models import AdmissionRegistration


class AdmissionRegistrationForm(forms.Form):
    parent_name = forms.CharField(
        max_length=100,
        required=True,
        error_messages={"required": "Họ tên phụ huynh là bắt buộc."},
    )
    parent_phone = forms.CharField(
        max_length=20,
        required=True,
        error_messages={"required": "Số điện thoại là bắt buộc."},
    )
    parent_email = forms.EmailField(
        required=False,
        error_messages={"invalid": "Email không hợp lệ. Vui lòng kiểm tra lại."},
    )

    student_name = forms.CharField(
        max_length=100,
        required=True,
        error_messages={"required": "Họ tên học sinh là bắt buộc."},
    )
    student_dob = forms.DateField(
        input_formats=["%Y-%m-%d"],
        required=True,
        error_messages={
            "required": "Ngày sinh là bắt buộc.",
            "invalid": "Ngày sinh không hợp lệ. Vui lòng nhập đúng định dạng.",
        },
    )
    student_gender = forms.ChoiceField(
        choices=AdmissionRegistration.GENDER_CHOICES,
        required=True,
        error_messages={
            "required": "Vui lòng chọn giới tính.",
            "invalid_choice": "Giới tính không hợp lệ.",
        },
    )

    current_school = forms.CharField(max_length=200, required=False)
    current_grade = forms.CharField(max_length=50, required=False)

    address = forms.CharField(
        required=True,
        error_messages={"required": "Địa chỉ là bắt buộc."},
    )
    district = forms.CharField(max_length=100, required=False)
    city = forms.CharField(max_length=100, required=False)

    # Chương trình Phụ huynh quan tâm
    interest_visit = forms.BooleanField(required=False, label="Hẹn lịch tham quan trường")
    interest_curriculum = forms.BooleanField(required=False, label="Tư vấn chương trình học")
    interest_admission_process = forms.BooleanField(required=False, label="Tư vấn quy trình tuyển sinh")

    how_did_you_know = forms.CharField(max_length=200, required=False)
    note = forms.CharField(required=False)

    def clean_parent_phone(self):
        phone = self.cleaned_data.get("parent_phone", "")
        if not validate_vietnam_phone(phone):
            raise forms.ValidationError(get_phone_validation_error_message(phone))
        return normalize_phone_number(phone)
