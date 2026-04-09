import json

from django import forms
from django.core.exceptions import ValidationError

from core.validators import (
    validate_vietnam_phone,
    get_phone_validation_error_message,
    normalize_phone_number,
)
from .models import (
    AdmissionRegistration,
    RegistrationSibling,
    AdmissionConsultation,
    TRAINING_PROGRAM_CHOICES,
    ADMISSION_METHOD_CHOICES,
    TARGET_GRADE_CHOICES,
    CONTACT_RELATIONSHIP_CHOICES,
    SCHOOL_YEAR_CHOICES,
    validate_transcript_extension,
    validate_transcript_file_size,
)


# ─── Form đăng ký dự tuyển (Tab 1) ───────────────────────────────────────

class AdmissionRegistrationForm(forms.Form):
    """Form đăng ký dự tuyển đầy đủ — multi-step wizard."""

    # ── Bước 1: Thông tin học sinh ────────────────────────────────────────
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
    address = forms.CharField(
        required=True,
        error_messages={"required": "Nơi cư trú là bắt buộc."},
    )
    current_school = forms.CharField(max_length=200, required=False)
    current_grade = forms.CharField(max_length=50, required=False)

    # ── Bước 2: Chương trình & hệ đào tạo ────────────────────────────────
    target_grade = forms.ChoiceField(
        choices=[('', '--- Lựa chọn ---')] + list(TARGET_GRADE_CHOICES),
        required=True,
        error_messages={
            "required": "Vui lòng chọn khối lớp dự tuyển.",
            "invalid_choice": "Khối lớp không hợp lệ.",
        },
    )
    training_program = forms.ChoiceField(
        choices=[('', '--- Lựa chọn ---')] + list(TRAINING_PROGRAM_CHOICES),
        required=True,
        error_messages={
            "required": "Vui lòng chọn hệ đào tạo.",
            "invalid_choice": "Hệ đào tạo không hợp lệ.",
        },
    )
    registration_school_year = forms.ChoiceField(
        choices=SCHOOL_YEAR_CHOICES,
        required=True,
        error_messages={"required": "Vui lòng chọn năm học."},
    )
    admission_method = forms.ChoiceField(
        choices=[('', '--- Lựa chọn ---')] + list(ADMISSION_METHOD_CHOICES),
        required=True,
        error_messages={
            "required": "Vui lòng chọn phương thức tuyển sinh.",
            "invalid_choice": "Phương thức tuyển sinh không hợp lệ.",
        },
    )
    transcript_file = forms.FileField(
        required=False,
        help_text="Học bạ / Phiếu điểm HK1, HK2 — scan PDF hoặc ảnh, tối đa 2 MB",
    )

    # ── Bước 3: Thông tin bổ sung ─────────────────────────────────────────
    study_abroad_plan = forms.ChoiceField(
        choices=[('false', 'Không'), ('true', 'Có')],
        required=False,
        initial='false',
    )
    siblings_json = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
        help_text="JSON array of siblings",
    )
    favorite_subjects = forms.CharField(required=False, max_length=500)
    best_subject = forms.CharField(required=False, max_length=100)
    achievements = forms.CharField(required=False)
    talent_subjects = forms.CharField(required=False, max_length=500)

    # ── Bước 4: Dịch vụ & thông tin liên hệ ──────────────────────────────
    register_shuttle = forms.BooleanField(required=False)
    register_dayboarding = forms.BooleanField(required=False)
    register_boarding = forms.BooleanField(required=False)

    parent_name = forms.CharField(
        max_length=100,
        required=True,
        error_messages={"required": "Họ tên người liên hệ là bắt buộc."},
    )
    contact_relationship = forms.ChoiceField(
        choices=[('', '--- Lựa chọn ---')] + list(CONTACT_RELATIONSHIP_CHOICES),
        required=True,
        error_messages={"required": "Vui lòng chọn quan hệ với học sinh."},
    )
    parent_email = forms.EmailField(
        required=True,
        error_messages={
            "required": "Email là bắt buộc.",
            "invalid": "Email không hợp lệ.",
        },
    )
    parent_email_confirm = forms.EmailField(
        required=True,
        error_messages={
            "required": "Vui lòng nhập lại email.",
            "invalid": "Email xác nhận không hợp lệ.",
        },
    )
    parent_phone = forms.CharField(
        max_length=20,
        required=True,
        error_messages={"required": "Số điện thoại là bắt buộc."},
    )
    referrer = forms.CharField(max_length=200, required=False)
    note = forms.CharField(required=False)

    # Giữ tương thích backward — ẩn trong form mới
    district = forms.CharField(max_length=100, required=False)
    city = forms.CharField(max_length=100, required=False)
    how_did_you_know = forms.CharField(max_length=200, required=False)
    interest_visit = forms.BooleanField(required=False)
    interest_curriculum = forms.BooleanField(required=False)
    interest_admission_process = forms.BooleanField(required=False)

    # ── Validation ────────────────────────────────────────────────────────

    def clean_parent_phone(self):
        phone = self.cleaned_data.get("parent_phone", "")
        if not validate_vietnam_phone(phone):
            raise forms.ValidationError(get_phone_validation_error_message(phone))
        return normalize_phone_number(phone)

    def clean_parent_email_confirm(self):
        email = self.cleaned_data.get("parent_email", "")
        email_confirm = self.cleaned_data.get("parent_email_confirm", "")
        if email and email_confirm and email.lower() != email_confirm.lower():
            raise forms.ValidationError("Email xác nhận không khớp.")
        return email_confirm

    def clean_transcript_file(self):
        f = self.cleaned_data.get("transcript_file")
        if f:
            validate_transcript_extension(f)
            validate_transcript_file_size(f)
        return f

    def clean_siblings_json(self):
        raw = self.cleaned_data.get("siblings_json", "").strip()
        if not raw:
            return []
        try:
            siblings = json.loads(raw)
        except json.JSONDecodeError:
            raise forms.ValidationError("Dữ liệu anh chị em không hợp lệ.")
        if not isinstance(siblings, list):
            raise forms.ValidationError("Dữ liệu anh chị em không hợp lệ.")
        if len(siblings) > 5:
            raise forms.ValidationError("Tối đa 5 anh chị em ruột.")
        for idx, sib in enumerate(siblings):
            if not isinstance(sib, dict):
                raise forms.ValidationError(f"Anh chị em #{idx+1}: dữ liệu không hợp lệ.")
            for key in ('full_name', 'date_of_birth', 'gender', 'current_school'):
                if not sib.get(key, '').strip():
                    raise forms.ValidationError(f"Anh chị em #{idx+1}: thiếu thông tin '{key}'.")
        return siblings


# ─── Form đăng ký tư vấn (Tab 2) ─────────────────────────────────────────

class AdmissionConsultationForm(forms.Form):
    """Form đăng ký tư vấn tuyển sinh — form ngắn gọn."""

    target_grade = forms.ChoiceField(
        choices=[('', '--- Lựa chọn ---')] + list(TARGET_GRADE_CHOICES),
        required=True,
        error_messages={
            "required": "Vui lòng chọn lớp tìm hiểu.",
            "invalid_choice": "Lớp không hợp lệ.",
        },
    )
    training_program = forms.ChoiceField(
        choices=[('', '--- Lựa chọn ---')] + list(TRAINING_PROGRAM_CHOICES),
        required=True,
        error_messages={
            "required": "Vui lòng chọn hệ đào tạo.",
            "invalid_choice": "Hệ đào tạo không hợp lệ.",
        },
    )
    details = forms.CharField(
        required=True,
        error_messages={"required": "Vui lòng cho biết thông tin mong muốn."},
    )
    interest_visit = forms.BooleanField(required=False)
    interest_curriculum = forms.BooleanField(required=False)
    interest_admission_process = forms.BooleanField(required=False)
    parent_name = forms.CharField(
        max_length=100,
        required=True,
        error_messages={"required": "Họ tên Phụ huynh là bắt buộc."},
    )
    phone = forms.CharField(
        max_length=20,
        required=True,
        error_messages={"required": "Số điện thoại là bắt buộc."},
    )
    email = forms.EmailField(
        required=True,
        error_messages={
            "required": "Email là bắt buộc.",
            "invalid": "Email không hợp lệ.",
        },
    )
    email_confirm = forms.EmailField(
        required=True,
        error_messages={
            "required": "Vui lòng nhập lại email.",
            "invalid": "Email xác nhận không hợp lệ.",
        },
    )

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "")
        if not validate_vietnam_phone(phone):
            raise forms.ValidationError(get_phone_validation_error_message(phone))
        return normalize_phone_number(phone)

    def clean_email_confirm(self):
        email = self.cleaned_data.get("email", "")
        email_confirm = self.cleaned_data.get("email_confirm", "")
        if email and email_confirm and email.lower() != email_confirm.lower():
            raise forms.ValidationError("Email xác nhận không khớp.")
        return email_confirm
