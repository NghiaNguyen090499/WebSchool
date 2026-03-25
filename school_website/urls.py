"""
URL configuration for school_website project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView, TemplateView
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import sitemaps
from django.templatetags.static import static as static_url
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=static_url('images/favicon.svg'), permanent=False)),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]


handler403 = "core.error_views.permission_denied_view"
handler404 = "core.error_views.page_not_found_view"
handler500 = "core.error_views.server_error_view"

urlpatterns += i18n_patterns(
    path('', include('core.urls')),
    path('su-kien/', include('landing.urls')),
    path('news/', include('news.urls')),
    path('events/', include('events.urls')),
    path('gallery/', include('gallery.urls')),
    path('about/', include('about.urls')),
    path('contact/', include('contact.urls')),
    path('trach-nhiem-xa-hoi/', include('csr.urls')),
    path('tuyen-sinh/', include('admissions.urls')),
    path('doi-ngu/', include('staff.urls')),
    path('hoat-dong-ngoai-khoa/', include('activities.urls')),
    path('portal/', include('portal.urls')),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


