import csv

from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.utils import timezone

from admissions.models import AdmissionInfo, AdmissionRegistration
from events.models import Event
from news.models import News, Category

from .forms import PortalPageForm, PortalMediaAssetForm, NewsForm, EventForm
from .models import PortalPage, PortalPageRevision, PortalMediaAsset, PortalAuditLog
from .mixins import (
    PortalEditorRequiredMixin,
    PortalAdminRequiredMixin,
    PortalListContextMixin,
    PortalFormLayoutMixin,
)


class NewsListView(PortalEditorRequiredMixin, PortalListContextMixin, ListView):
    model = News
    template_name = "portal/news/list.html"
    paginate_by = 20
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = News.all_objects.all().order_by("-created_at")
        query = self.request.GET.get("q", "").strip()
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(excerpt__icontains=query)
                | Q(content__icontains=query)
            )
        category = self.request.GET.get("category", "").strip()
        if category:
            queryset = queryset.filter(category__slug=category)
        featured = self.request.GET.get("featured", "")
        if featured == "yes":
            queryset = queryset.filter(is_featured=True)
        elif featured == "no":
            queryset = queryset.filter(is_featured=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.order_by("name")
        context["selected_category"] = self.request.GET.get("category", "").strip()
        context["selected_featured"] = self.request.GET.get("featured", "")
        context["search_query"] = self.request.GET.get("q", "").strip()
        return context


class NewsCreateView(SuccessMessageMixin, PortalEditorRequiredMixin, PortalFormLayoutMixin, CreateView):
    model = News
    form_class = NewsForm
    template_name = "portal/news/form.html"
    success_url = reverse_lazy("portal:news_list")
    success_message = "News item has been created."
    full_width_fields = ("thumbnail", "content", "excerpt")

    def form_valid(self, form):
        response = super().form_valid(form)
        _portal_log(
            self.request.user,
            "create",
            None,
            f"Created news: {self.object.title}",
            target=self.object,
        )
        return response


class NewsUpdateView(SuccessMessageMixin, PortalEditorRequiredMixin, PortalFormLayoutMixin, UpdateView):
    model = News
    form_class = NewsForm
    template_name = "portal/news/form.html"
    success_url = reverse_lazy("portal:news_list")
    success_message = "News item has been updated."
    full_width_fields = ("thumbnail", "content", "excerpt")

    def form_valid(self, form):
        response = super().form_valid(form)
        _portal_log(
            self.request.user,
            "update",
            None,
            f"Updated news: {self.object.title}",
            target=self.object,
        )
        return response


class NewsDeleteView(PortalAdminRequiredMixin, DeleteView):
    model = News
    template_name = "portal/news/confirm_delete.html"
    success_url = reverse_lazy("portal:news_list")

    def form_valid(self, form):
        self.object = self.get_object()
        _portal_log(
            self.request.user,
            "delete",
            None,
            f'Deleted news: {self.object.title}',
            target=self.object,
        )
        messages.success(self.request, f'News "{self.object.title}" has been deleted.')
        return super().form_valid(form)


class EventListView(PortalEditorRequiredMixin, PortalListContextMixin, ListView):
    model = Event
    template_name = "portal/events/list.html"
    paginate_by = 20
    ordering = ["-date"]

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q", "").strip()
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(location__icontains=query)
                | Q(description__icontains=query)
            )
        when = self.request.GET.get("when", "")
        today = timezone.now().date()
        if when == "upcoming":
            queryset = queryset.filter(date__gte=today)
        elif when == "past":
            queryset = queryset.filter(date__lt=today)
        featured = self.request.GET.get("featured", "")
        if featured == "yes":
            queryset = queryset.filter(is_featured=True)
        elif featured == "no":
            queryset = queryset.filter(is_featured=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected_when"] = self.request.GET.get("when", "")
        context["selected_featured"] = self.request.GET.get("featured", "")
        context["search_query"] = self.request.GET.get("q", "").strip()
        return context


class EventCreateView(SuccessMessageMixin, PortalEditorRequiredMixin, PortalFormLayoutMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "portal/events/form.html"
    success_url = reverse_lazy("portal:event_list")
    success_message = "Event has been created."
    full_width_fields = ("description", "image")

    def form_valid(self, form):
        response = super().form_valid(form)
        _portal_log(
            self.request.user,
            "create",
            None,
            f"Created event: {self.object.title}",
            target=self.object,
        )
        return response


class EventUpdateView(SuccessMessageMixin, PortalEditorRequiredMixin, PortalFormLayoutMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = "portal/events/form.html"
    success_url = reverse_lazy("portal:event_list")
    success_message = "Event has been updated."
    full_width_fields = ("description", "image")

    def form_valid(self, form):
        response = super().form_valid(form)
        _portal_log(
            self.request.user,
            "update",
            None,
            f"Updated event: {self.object.title}",
            target=self.object,
        )
        return response


class EventDeleteView(PortalAdminRequiredMixin, DeleteView):
    model = Event
    template_name = "portal/events/confirm_delete.html"
    success_url = reverse_lazy("portal:event_list")

    def form_valid(self, form):
        self.object = self.get_object()
        _portal_log(
            self.request.user,
            "delete",
            None,
            f'Deleted event: {self.object.title}',
            target=self.object,
        )
        messages.success(self.request, f'Event "{self.object.title}" has been deleted.')
        return super().form_valid(form)


class AdmissionInfoListView(PortalEditorRequiredMixin, PortalListContextMixin, ListView):
    model = AdmissionInfo
    template_name = "portal/admissions/list.html"
    paginate_by = 20
    ordering = ["order", "level"]

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q", "").strip()
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(subtitle__icontains=query)
                | Q(school_year__icontains=query)
            )
        level = self.request.GET.get("level", "").strip()
        if level:
            queryset = queryset.filter(level=level)
        active = self.request.GET.get("active", "")
        if active == "yes":
            queryset = queryset.filter(is_active=True)
        elif active == "no":
            queryset = queryset.filter(is_active=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["level_choices"] = AdmissionInfo.LEVEL_CHOICES
        context["selected_level"] = self.request.GET.get("level", "").strip()
        context["selected_active"] = self.request.GET.get("active", "")
        context["search_query"] = self.request.GET.get("q", "").strip()
        return context


class AdmissionInfoCreateView(SuccessMessageMixin, PortalEditorRequiredMixin, PortalFormLayoutMixin, CreateView):
    model = AdmissionInfo
    fields = [
        "level",
        "title",
        "school_year",
        "subtitle",
        "description",
        "age_range",
        "requirements",
        "tuition_info",
        "process",
        "benefits",
        "facilities",
        "curriculum",
        "deadline",
        "image",
        "banner_image",
        "icon",
        "color",
        "is_active",
        "is_featured",
        "order",
    ]
    template_name = "portal/admissions/form.html"
    success_url = reverse_lazy("portal:admissions_list")
    success_message = "Admission info has been created."
    full_width_fields = (
        "subtitle",
        "description",
        "requirements",
        "tuition_info",
        "process",
        "benefits",
        "facilities",
        "curriculum",
        "image",
        "banner_image",
    )

    def form_valid(self, form):
        response = super().form_valid(form)
        _portal_log(
            self.request.user,
            "create",
            None,
            f"Created admission info: {self.object.title}",
            target=self.object,
        )
        return response


class AdmissionInfoUpdateView(SuccessMessageMixin, PortalEditorRequiredMixin, PortalFormLayoutMixin, UpdateView):
    model = AdmissionInfo
    fields = [
        "level",
        "title",
        "school_year",
        "subtitle",
        "description",
        "age_range",
        "requirements",
        "tuition_info",
        "process",
        "benefits",
        "facilities",
        "curriculum",
        "deadline",
        "image",
        "banner_image",
        "icon",
        "color",
        "is_active",
        "is_featured",
        "order",
    ]
    template_name = "portal/admissions/form.html"
    success_url = reverse_lazy("portal:admissions_list")
    success_message = "Admission info has been updated."
    full_width_fields = (
        "subtitle",
        "description",
        "requirements",
        "tuition_info",
        "process",
        "benefits",
        "facilities",
        "curriculum",
        "image",
        "banner_image",
    )

    def form_valid(self, form):
        response = super().form_valid(form)
        _portal_log(
            self.request.user,
            "update",
            None,
            f"Updated admission info: {self.object.title}",
            target=self.object,
        )
        return response


class AdmissionInfoDeleteView(PortalAdminRequiredMixin, DeleteView):
    model = AdmissionInfo
    template_name = "portal/admissions/confirm_delete.html"
    success_url = reverse_lazy("portal:admissions_list")

    def form_valid(self, form):
        self.object = self.get_object()
        _portal_log(
            self.request.user,
            "delete",
            None,
            f'Deleted admission info: {self.object.title}',
            target=self.object,
        )
        messages.success(self.request, f'Admission "{self.object.title}" has been deleted.')
        return super().form_valid(form)


def _get_registration_queryset(request):
    queryset = AdmissionRegistration.objects.select_related("admission").order_by("-created_at")
    query = request.GET.get("q", "").strip()
    if query:
        queryset = queryset.filter(
            Q(parent_name__icontains=query)
            | Q(parent_phone__icontains=query)
            | Q(student_name__icontains=query)
        )
    status = request.GET.get("status", "").strip()
    if status:
        queryset = queryset.filter(status=status)
    level = request.GET.get("level", "").strip()
    if level:
        queryset = queryset.filter(admission__level=level)
    return queryset


class AdmissionRegistrationListView(PortalEditorRequiredMixin, PortalListContextMixin, ListView):
    model = AdmissionRegistration
    template_name = "portal/admissions/registrations_list.html"
    paginate_by = 20
    ordering = ["-created_at"]

    def get_queryset(self):
        return _get_registration_queryset(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_choices"] = AdmissionRegistration.STATUS_CHOICES
        context["level_choices"] = AdmissionInfo.LEVEL_CHOICES
        context["selected_status"] = self.request.GET.get("status", "").strip()
        context["selected_level"] = self.request.GET.get("level", "").strip()
        context["search_query"] = self.request.GET.get("q", "").strip()
        return context


class AdmissionRegistrationUpdateView(SuccessMessageMixin, PortalEditorRequiredMixin, PortalFormLayoutMixin, UpdateView):
    model = AdmissionRegistration
    fields = ["status", "admin_notes"]
    template_name = "portal/admissions/registrations_form.html"
    success_url = reverse_lazy("portal:admissions_registrations_list")
    success_message = "Registration status has been updated."
    full_width_fields = ("admin_notes",)

    def form_valid(self, form):
        response = super().form_valid(form)
        _portal_log(
            self.request.user,
            "update",
            None,
            f"Updated registration: {self.object.student_name}",
            target=self.object,
        )
        return response


class AdmissionRegistrationDeleteView(PortalAdminRequiredMixin, DeleteView):
    model = AdmissionRegistration
    template_name = "portal/admissions/registrations_confirm_delete.html"
    success_url = reverse_lazy("portal:admissions_registrations_list")

    def form_valid(self, form):
        self.object = self.get_object()
        _portal_log(
            self.request.user,
            "delete",
            None,
            f'Deleted registration: {self.object.student_name}',
            target=self.object,
        )
        messages.success(
            self.request,
            f'Registration for "{self.object.student_name}" has been deleted.',
        )
        return super().form_valid(form)


class AdmissionRegistrationExportView(PortalEditorRequiredMixin, View):
    @staticmethod
    def _escape_csv_value(value):
        if value is None:
            return ""
        text = str(value)
        if text.startswith(("=", "+", "-", "@")):
            return f"'{text}"
        return text

    def get(self, request, *args, **kwargs):
        queryset = _get_registration_queryset(request)
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = "attachment; filename=admissions_registrations.csv"
        response.write("\ufeff")

        writer = csv.writer(response)
        writer.writerow([
            "Parent Name",
            "Parent Phone",
            "Parent Email",
            "Student Name",
            "Student DOB",
            "Student Gender",
            "Level",
            "Status",
            "Created At",
            "Address",
            "District",
            "City",
            "Notes",
        ])

        for item in queryset:
            row = [
                item.parent_name,
                item.parent_phone,
                item.parent_email,
                item.student_name,
                item.student_dob,
                item.get_student_gender_display(),
                item.admission.get_level_display(),
                item.get_status_display(),
                item.created_at.strftime("%Y-%m-%d %H:%M"),
                item.address,
                item.district,
                item.city,
                item.note,
            ]
            writer.writerow([self._escape_csv_value(value) for value in row])

        return response


class PortalLoginView(LoginView):
    template_name = "portal/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        redirect_url = self.get_redirect_url()
        if redirect_url:
            return redirect_url
        return reverse_lazy("portal:dashboard")


class PortalLogoutView(LogoutView):
    next_page = reverse_lazy("portal:login")


class PortalDashboardView(PortalEditorRequiredMixin, TemplateView):
    template_name = "portal/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["news_count"] = News.all_objects.count()
        context["events_count"] = Event.objects.count()
        context["admissions_count"] = AdmissionInfo.objects.count()
        context["registrations_count"] = AdmissionRegistration.objects.count()
        context["pages_count"] = PortalPage.objects.count()
        context["recent_news"] = News.all_objects.order_by("-created_at")[:5]
        context["recent_events"] = Event.objects.order_by("-date")[:5]
        context["recent_registrations"] = AdmissionRegistration.objects.order_by("-created_at")[:5]
        context["recent_pages"] = PortalPage.objects.order_by("-updated_at")[:5]
        return context


class PortalPageListView(PortalEditorRequiredMixin, PortalListContextMixin, ListView):
    model = PortalPage
    template_name = "portal/pages/list.html"
    paginate_by = 20
    ordering = ["-updated_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q", "").strip()
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(slug__icontains=query))
        status = self.request.GET.get("status", "").strip()
        if status:
            queryset = queryset.filter(status=status)
        page_type = self.request.GET.get("page_type", "").strip()
        if page_type:
            queryset = queryset.filter(page_type=page_type)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "").strip()
        context["selected_status"] = self.request.GET.get("status", "").strip()
        context["selected_type"] = self.request.GET.get("page_type", "").strip()
        context["type_choices"] = PortalPage.TYPE_CHOICES
        return context


class PortalPageCreateView(SuccessMessageMixin, PortalEditorRequiredMixin, PortalFormLayoutMixin, CreateView):
    model = PortalPage
    form_class = PortalPageForm
    template_name = "portal/pages/form.html"
    success_url = reverse_lazy("portal:pages_list")
    success_message = "Page has been created."
    full_width_fields = ("content", "seo_description", "og_image")

    def form_valid(self, form):
        page = form.save(commit=False)
        page.created_by = self.request.user
        page.updated_by = self.request.user
        response = super().form_valid(form)
        PortalPageRevision.objects.create(
            page=page,
            snapshot=_portal_page_snapshot(page),
            created_by=self.request.user,
            note="Create",
        )
        _portal_log(self.request.user, "create", page, "Created page")
        return response


class PortalPageUpdateView(SuccessMessageMixin, PortalEditorRequiredMixin, PortalFormLayoutMixin, UpdateView):
    model = PortalPage
    form_class = PortalPageForm
    template_name = "portal/pages/form.html"
    success_url = reverse_lazy("portal:pages_list")
    success_message = "Page has been updated."
    full_width_fields = ("content", "seo_description", "og_image")

    def form_valid(self, form):
        page = form.save(commit=False)
        page.updated_by = self.request.user
        response = super().form_valid(form)
        PortalPageRevision.objects.create(
            page=page,
            snapshot=_portal_page_snapshot(page),
            created_by=self.request.user,
            note="Update",
        )
        _portal_log(self.request.user, "update", page, "Updated page")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["audit_logs"] = self.object.audit_logs.select_related("user")[:10]
        context["revisions"] = self.object.revisions.select_related("created_by")[:5]
        return context


class PortalPageDeleteView(PortalAdminRequiredMixin, DeleteView):
    model = PortalPage
    template_name = "portal/pages/confirm_delete.html"
    success_url = reverse_lazy("portal:pages_list")

    def form_valid(self, form):
        page = self.get_object()
        _portal_log(self.request.user, "delete", page, "Deleted page")
        messages.success(self.request, f'Page "{page.title}" has been deleted.')
        return super().form_valid(form)


class PortalPagePreviewView(PortalEditorRequiredMixin, TemplateView):
    template_name = "portal/pages/preview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = get_object_or_404(PortalPage, pk=self.kwargs["pk"])
        context["page"] = page
        _portal_log(self.request.user, "preview", page, "Preview page")
        return context


class PortalPagePublishView(PortalEditorRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        page = get_object_or_404(PortalPage, pk=kwargs["pk"])
        page.status = "published"
        page.published_at = timezone.now()
        page.updated_by = request.user
        page.save()
        PortalPageRevision.objects.create(
            page=page,
            snapshot=_portal_page_snapshot(page),
            created_by=request.user,
            note="Publish",
        )
        _portal_log(request.user, "publish", page, "Published page")
        messages.success(request, f'Page "{page.title}" has been published.')
        return HttpResponseRedirect(reverse_lazy("portal:pages_list"))


class PortalPageUnpublishView(PortalEditorRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        page = get_object_or_404(PortalPage, pk=kwargs["pk"])
        page.status = "draft"
        page.updated_by = request.user
        page.save()
        PortalPageRevision.objects.create(
            page=page,
            snapshot=_portal_page_snapshot(page),
            created_by=request.user,
            note="Unpublish",
        )
        _portal_log(request.user, "unpublish", page, "Unpublished page")
        messages.success(request, f'Page "{page.title}" has been moved to draft.')
        return HttpResponseRedirect(reverse_lazy("portal:pages_list"))


class PortalMediaListView(PortalEditorRequiredMixin, PortalListContextMixin, ListView):
    model = PortalMediaAsset
    template_name = "portal/media/list.html"
    paginate_by = 24
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        file_type = self.request.GET.get("file_type", "").strip()
        if file_type:
            queryset = queryset.filter(file_type=file_type)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["file_type_choices"] = PortalMediaAsset.FILE_TYPE_CHOICES
        context["selected_type"] = self.request.GET.get("file_type", "").strip()
        return context


class PortalMediaCreateView(SuccessMessageMixin, PortalEditorRequiredMixin, CreateView):
    model = PortalMediaAsset
    form_class = PortalMediaAssetForm
    template_name = "portal/media/form.html"
    success_url = reverse_lazy("portal:media_list")
    success_message = "Media uploaded successfully."

    def form_valid(self, form):
        asset = form.save(commit=False)
        asset.created_by = self.request.user
        response = super().form_valid(form)
        _portal_log(
            self.request.user,
            "upload",
            None,
            f"Uploaded media: {asset.file.name}",
            target=asset,
        )
        return response


def _portal_page_snapshot(page):
    return {
        "title": page.title,
        "slug": page.slug,
        "page_type": page.page_type,
        "status": page.status,
        "content": page.content,
        "seo_title": page.seo_title,
        "seo_description": page.seo_description,
        "og_image": page.og_image.url if page.og_image else "",
        "updated_at": page.updated_at.isoformat() if page.updated_at else "",
    }


def _portal_log(user, action, page, details, target=None):
    target_model = ""
    target_object_id = ""
    if target is not None:
        target_model = target._meta.label_lower
        target_object_id = str(target.pk)
    elif page is not None:
        target_model = page._meta.label_lower
        target_object_id = str(page.pk)

    PortalAuditLog.objects.create(
        action=action,
        page=page,
        user=user,
        details=details or "",
        target_model=target_model,
        target_object_id=target_object_id,
    )
