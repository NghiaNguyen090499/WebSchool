from django.shortcuts import render
from django.urls import NoReverseMatch, reverse


def _resolve_url(name, fallback):
    try:
        return reverse(name)
    except NoReverseMatch:
        return fallback


def _portal_cta(request):
    user = getattr(request, "user", None)
    if user and user.is_authenticated:
        return _resolve_url("portal:dashboard", "/portal/dashboard/"), "Về Dashboard"
    return _resolve_url("portal:login", "/portal/login/"), "Đăng nhập Portal"


def _error_context(request):
    primary_url, primary_label = _portal_cta(request)
    return {
        "primary_cta_url": primary_url,
        "primary_cta_label": primary_label,
        "home_url": _resolve_url("core:home", "/"),
    }


def permission_denied_view(request, exception=None):
    context = _error_context(request)
    return render(request, "403.html", context=context, status=403)


def page_not_found_view(request, exception):
    context = _error_context(request)
    return render(request, "404.html", context=context, status=404)


def server_error_view(request):
    context = _error_context(request)
    return render(request, "500.html", context=context, status=500)
