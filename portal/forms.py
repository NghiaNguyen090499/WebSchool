from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from core.validators import (
    validate_upload_extension,
    validate_upload_file_size,
    validate_upload_file_type,
)
from events.models import Event
from news.models import Category, News

from .models import PortalPage, PortalMediaAsset


class PortalPageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["slug"].required = False

    class Meta:
        model = PortalPage
        fields = [
            "title",
            "slug",
            "page_type",
            "status",
            "content",
            "seo_title",
            "seo_description",
            "og_image",
        ]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 14, "class": "js-richtext"}),
            "seo_description": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get("slug", "").strip() or slugify(
            self.cleaned_data.get("title", "")
        )
        if PortalPage.objects.exclude(pk=self.instance.pk).filter(slug=slug).exists():
            raise forms.ValidationError("Slug already exists. Please choose another.")
        return slug


class PortalMediaAssetForm(forms.ModelForm):
    class Meta:
        model = PortalMediaAsset
        fields = ["file", "file_type", "alt_text"]

    def clean(self):
        cleaned = super().clean()
        uploaded_file = cleaned.get("file")
        file_type = cleaned.get("file_type")
        if not uploaded_file or not file_type:
            return cleaned

        validators = (
            lambda: validate_upload_extension(uploaded_file),
            lambda: validate_upload_file_type(uploaded_file, file_type),
            lambda: validate_upload_file_size(uploaded_file),
        )
        for run_validator in validators:
            try:
                run_validator()
            except ValidationError as exc:
                self.add_error("file", exc)

        return cleaned


class NewsForm(forms.ModelForm):
    def clean_slug(self):
        slug = self.cleaned_data.get("slug", "").strip() or slugify(
            self.cleaned_data.get("title", "")
        )
        if News.objects.exclude(pk=self.instance.pk).filter(slug=slug).exists():
            raise forms.ValidationError("Slug đã tồn tại. Vui lòng chọn slug khác.")
        return slug

    class Meta:
        model = News
        fields = ["title", "slug", "thumbnail", "source_document", "content", "excerpt", "category", "is_featured"]


class NewsImportForm(forms.Form):
    source_file = forms.FileField(
        label="File bài viết (.docx)",
        help_text="Dòng đầu tiên trong file sẽ được dùng làm tiêu đề nếu bạn không nhập tiêu đề thay thế. File Word gốc cũng sẽ được lưu lại trong bài tin.",
    )
    extra_images_zip = forms.FileField(
        label="Ảnh phụ (.zip)",
        required=False,
        help_text="Tuỳ chọn. Dùng khi bài có thêm ảnh ngoài file Word.",
    )
    title_override = forms.CharField(
        label="Tiêu đề thay thế",
        required=False,
        help_text="Tuỳ chọn. Nếu để trống, portal sẽ lấy tiêu đề từ dòng đầu tiên của file Word.",
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        label="Danh mục",
        empty_label=None,
    )
    is_featured = forms.BooleanField(
        label="Đánh dấu nổi bật",
        required=False,
    )
    overwrite_existing = forms.BooleanField(
        label="Ghi đè nếu bài đã tồn tại",
        required=False,
        initial=True,
        help_text="Portal sẽ tìm bài theo tiêu đề hoặc slug và cập nhật lại nội dung thay vì tạo bản sao.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.order_by("name")

    def clean_source_file(self):
        uploaded_file = self.cleaned_data.get("source_file")
        if not uploaded_file:
            return uploaded_file
        validate_upload_file_size(uploaded_file)
        ext = uploaded_file.name.rsplit(".", 1)[-1].lower() if "." in uploaded_file.name else ""
        if ext != "docx":
            raise forms.ValidationError("Chỉ hỗ trợ import file .docx.")
        return uploaded_file

    def clean_extra_images_zip(self):
        uploaded_file = self.cleaned_data.get("extra_images_zip")
        if not uploaded_file:
            return uploaded_file
        validate_upload_file_size(uploaded_file)
        ext = uploaded_file.name.rsplit(".", 1)[-1].lower() if "." in uploaded_file.name else ""
        if ext != "zip":
            raise forms.ValidationError("Ảnh phụ phải là file .zip.")
        return uploaded_file


class EventForm(forms.ModelForm):
    def clean_slug(self):
        slug = self.cleaned_data.get("slug", "").strip() or slugify(
            self.cleaned_data.get("title", "")
        )
        if Event.objects.exclude(pk=self.instance.pk).filter(slug=slug).exists():
            raise forms.ValidationError("Slug đã tồn tại. Vui lòng chọn slug khác.")
        return slug

    class Meta:
        model = Event
        fields = ["title", "slug", "date", "time", "location", "description", "image", "is_featured"]
