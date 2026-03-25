from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from core.validators import (
    validate_upload_extension,
    validate_upload_file_size,
    validate_upload_file_type,
)
from events.models import Event
from news.models import News

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
        fields = ["title", "slug", "thumbnail", "content", "excerpt", "category", "is_featured"]


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
