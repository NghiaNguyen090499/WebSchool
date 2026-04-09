from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "portal"

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="portal:dashboard"), name="home"),
    path("dashboard/", views.PortalDashboardView.as_view(), name="dashboard"),
    path("login/", views.PortalLoginView.as_view(), name="login"),
    path("logout/", views.PortalLogoutView.as_view(), name="logout"),
    path("news/", views.NewsListView.as_view(), name="news_list"),
    path("news/import/", views.NewsImportView.as_view(), name="news_import"),
    path("news/create/", views.NewsCreateView.as_view(), name="news_create"),
    path("news/<int:pk>/edit/", views.NewsUpdateView.as_view(), name="news_edit"),
    path("news/<int:pk>/delete/", views.NewsDeleteView.as_view(), name="news_delete"),
    path("events/", views.EventListView.as_view(), name="event_list"),
    path("events/create/", views.EventCreateView.as_view(), name="event_create"),
    path("events/<int:pk>/edit/", views.EventUpdateView.as_view(), name="event_edit"),
    path("events/<int:pk>/delete/", views.EventDeleteView.as_view(), name="event_delete"),
    path("admissions/", views.AdmissionInfoListView.as_view(), name="admissions_list"),
    path("admissions/create/", views.AdmissionInfoCreateView.as_view(), name="admissions_create"),
    path("admissions/<int:pk>/edit/", views.AdmissionInfoUpdateView.as_view(), name="admissions_edit"),
    path("admissions/<int:pk>/delete/", views.AdmissionInfoDeleteView.as_view(), name="admissions_delete"),
    path(
        "admissions/registrations/",
        views.AdmissionRegistrationListView.as_view(),
        name="admissions_registrations_list",
    ),
    path(
        "admissions/registrations/<int:pk>/edit/",
        views.AdmissionRegistrationUpdateView.as_view(),
        name="admissions_registrations_edit",
    ),
    path(
        "admissions/registrations/<int:pk>/delete/",
        views.AdmissionRegistrationDeleteView.as_view(),
        name="admissions_registrations_delete",
    ),
    path(
        "admissions/registrations/export/",
        views.AdmissionRegistrationExportView.as_view(),
        name="admissions_registrations_export",
    ),
    path("pages/", views.PortalPageListView.as_view(), name="pages_list"),
    path("pages/create/", views.PortalPageCreateView.as_view(), name="pages_create"),
    path("pages/<int:pk>/edit/", views.PortalPageUpdateView.as_view(), name="pages_edit"),
    path("pages/<int:pk>/delete/", views.PortalPageDeleteView.as_view(), name="pages_delete"),
    path("pages/<int:pk>/preview/", views.PortalPagePreviewView.as_view(), name="pages_preview"),
    path("pages/<int:pk>/publish/", views.PortalPagePublishView.as_view(), name="pages_publish"),
    path("pages/<int:pk>/unpublish/", views.PortalPageUnpublishView.as_view(), name="pages_unpublish"),
    path("media/", views.PortalMediaListView.as_view(), name="media_list"),
    path("media/upload/", views.PortalMediaCreateView.as_view(), name="media_upload"),
]
