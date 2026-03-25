"""
Custom validators for MIS Website.
Includes phone number and file upload validation.
"""
import re
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from core.utils.youtube import extract_youtube_id


# Vietnamese phone number patterns
# Valid prefixes: 03, 05, 07, 08, 09 (10 digits total)
# Or with country code: +84 followed by 3, 5, 7, 8, 9 (12 digits with +84)
VIETNAM_PHONE_REGEX = re.compile(
    r'^(?:'
    r'(?:\+84|84|0)'  # Country code +84, 84, or leading 0
    r'(?:3[2-9]|5[2689]|7[06-9]|8[1-9]|9[0-46-9])'  # Valid network prefixes
    r'\d{7}'  # 7 remaining digits
    r')$'
)

# Alternative simpler pattern for basic validation
VIETNAM_PHONE_SIMPLE_REGEX = re.compile(
    r'^(?:\+84|84|0)[35789]\d{8}$'
)


def normalize_phone_number(phone: str) -> str:
    """
    Normalize Vietnamese phone number by removing spaces, dashes, dots.
    
    Args:
        phone: Raw phone number string
        
    Returns:
        Cleaned phone number string
        
    Examples:
        >>> normalize_phone_number("0912 345 678")
        "0912345678"
        >>> normalize_phone_number("091-234-5678")
        "0912345678"
        >>> normalize_phone_number("+84.912.345.678")
        "+84912345678"
    """
    if not phone:
        return ""
    
    # Remove spaces, dashes, dots, parentheses
    cleaned = re.sub(r'[\s\-\.\(\)]+', '', phone.strip())
    return cleaned


def validate_vietnam_phone(phone: str) -> bool:
    """
    Validate if the phone number is a valid Vietnamese mobile number.
    
    Args:
        phone: Phone number string (can include spaces, dashes)
        
    Returns:
        True if valid Vietnamese phone number, False otherwise
        
    Valid formats:
        - 0912345678 (10 digits, starts with 0)
        - +84912345678 (12 chars with +84)
        - 84912345678 (11 digits with 84)
        
    Valid prefixes (after 0 or 84):
        - 3x: Viettel (32-39)
        - 5x: Vietnamobile (52, 56, 58, 59)
        - 7x: Mobifone (70, 76-79)
        - 8x: Vinaphone (81-89)
        - 9x: Various (90-94, 96-99)
    """
    cleaned = normalize_phone_number(phone)
    
    if not cleaned:
        return False
    
    return bool(VIETNAM_PHONE_SIMPLE_REGEX.match(cleaned))


def validate_vietnam_phone_strict(phone: str) -> bool:
    """
    Strictly validate Vietnamese phone number with exact carrier prefixes.
    
    This is more restrictive and validates against actual carrier prefixes
    used in Vietnam.
    """
    cleaned = normalize_phone_number(phone)
    
    if not cleaned:
        return False
    
    return bool(VIETNAM_PHONE_REGEX.match(cleaned))


class VietnamPhoneValidator:
    """
    Django validator class for Vietnamese phone numbers.
    Can be used in model fields or forms.
    
    Usage in models:
        phone = models.CharField(
            max_length=20,
            validators=[VietnamPhoneValidator()]
        )
        
    Usage in forms:
        phone = forms.CharField(
            validators=[VietnamPhoneValidator(message="SĐT không hợp lệ")]
        )
    """
    
    message = _("Số điện thoại không hợp lệ. Vui lòng nhập SĐT Việt Nam (VD: 0912345678)")
    code = "invalid_phone"
    
    def __init__(self, message=None, code=None, strict=False):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        self.strict = strict
    
    def __call__(self, value):
        if not value:
            return  # Let required validation handle empty values
        
        if self.strict:
            is_valid = validate_vietnam_phone_strict(value)
        else:
            is_valid = validate_vietnam_phone(value)
        
        if not is_valid:
            raise ValidationError(self.message, code=self.code)
    
    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.message == other.message and
            self.code == other.code and
            self.strict == other.strict
        )


def get_phone_validation_error_message(phone: str) -> str:
    """
    Get a specific error message based on what's wrong with the phone number.
    
    Args:
        phone: The invalid phone number
        
    Returns:
        Specific error message in Vietnamese
    """
    cleaned = normalize_phone_number(phone)
    
    if not cleaned:
        return "Vui lòng nhập số điện thoại"
    
    # Check if contains non-digit characters (except leading +)
    if cleaned.startswith('+'):
        check_str = cleaned[1:]
    else:
        check_str = cleaned
    
    if not check_str.isdigit():
        return "Số điện thoại chỉ được chứa các chữ số"
    
    # Check length
    if cleaned.startswith('+84') or cleaned.startswith('84'):
        expected_len = 12 if cleaned.startswith('+84') else 11
        if len(cleaned) != expected_len:
            return f"Số điện thoại phải có {expected_len} ký tự (bao gồm mã quốc gia)"
    elif cleaned.startswith('0'):
        if len(cleaned) != 10:
            return "Số điện thoại phải có 10 chữ số"
    else:
        return "Số điện thoại phải bắt đầu bằng 0 hoặc +84"
    
    # Check prefix
    valid_prefixes = ['03', '05', '07', '08', '09']
    normalized = cleaned
    if normalized.startswith('+84'):
        normalized = '0' + normalized[3:]
    elif normalized.startswith('84'):
        normalized = '0' + normalized[2:]
    
    if not any(normalized.startswith(prefix) for prefix in valid_prefixes):
        return "Đầu số điện thoại không hợp lệ (phải bắt đầu bằng 03, 05, 07, 08 hoặc 09)"
    
    return "Số điện thoại không hợp lệ"


def validate_upload_extension(uploaded_file):
    """
    Validate uploaded file extension against settings.ALLOWED_UPLOAD_EXTENSIONS.
    """
    if not uploaded_file:
        return
    allowed_set = get_allowed_upload_extensions()
    if not allowed_set:
        return
    ext = Path(uploaded_file.name).suffix.lower()
    if not ext or ext not in allowed_set:
        allowed_display = ", ".join(sorted(allowed_set))
        raise ValidationError(
            _(f"Định dạng tệp không được hỗ trợ. Cho phép: {allowed_display}")
        )


DEFAULT_UPLOAD_EXTENSIONS_BY_TYPE = {
    "image": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"},
    "document": {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"},
}


def _normalize_extensions(extensions):
    normalized = set()
    for item in extensions or []:
        text = str(item).strip().lower()
        if not text:
            continue
        if not text.startswith("."):
            text = f".{text}"
        normalized.add(text)
    return normalized


def get_allowed_upload_extensions():
    configured = getattr(settings, "ALLOWED_UPLOAD_EXTENSIONS", None)
    if configured:
        return _normalize_extensions(configured)

    merged = set()
    for values in DEFAULT_UPLOAD_EXTENSIONS_BY_TYPE.values():
        merged.update(values)
    return merged


def get_allowed_extensions_for_type(file_type):
    configured_map = getattr(settings, "UPLOAD_ALLOWED_EXTENSIONS_BY_TYPE", None) or {}
    configured = configured_map.get(file_type)
    if configured:
        return _normalize_extensions(configured)
    return set(DEFAULT_UPLOAD_EXTENSIONS_BY_TYPE.get(file_type, set()))


def get_upload_max_file_size():
    max_size = getattr(settings, "UPLOAD_MAX_FILE_SIZE", None)
    if max_size is None:
        max_size = getattr(settings, "FILE_UPLOAD_MAX_MEMORY_SIZE", None)
    return max_size


def validate_upload_file_size(uploaded_file):
    if not uploaded_file:
        return
    max_size = get_upload_max_file_size()
    if max_size and uploaded_file.size > max_size:
        max_mb = max_size / (1024 * 1024)
        raise ValidationError(
            _("Dung lượng tệp vượt quá giới hạn %(max_mb).0fMB."),
            params={"max_mb": max_mb},
        )


def validate_upload_file_type(uploaded_file, file_type):
    if not uploaded_file or not file_type:
        return
    expected = get_allowed_extensions_for_type(file_type)
    if not expected:
        return
    ext = Path(uploaded_file.name).suffix.lower()
    if ext not in expected:
        allowed_display = ", ".join(sorted(expected))
        raise ValidationError(
            _("Định dạng tệp không phù hợp với loại đã chọn. Cho phép: %(allowed)s"),
            params={"allowed": allowed_display},
        )


def validate_youtube_url(value: str):
    if value and not extract_youtube_id(value):
        raise ValidationError(_("Liên kết YouTube không hợp lệ."))
