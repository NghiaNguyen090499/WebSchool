from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy


class PortalRoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy("portal:login")
    raise_exception = True
    allowed_groups = ()

    def handle_no_permission(self):
        # Unauthenticated → redirect to login (not 403)
        if not self.request.user.is_authenticated:
            return redirect(f"{self.login_url}?next={self.request.path}")
        # Authenticated but wrong role → 403 (keep raise_exception behavior)
        return super().handle_no_permission()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        is_admin = user.is_superuser or user.groups.filter(name="Admin").exists()
        is_editor = is_admin or user.groups.filter(name="Editor").exists()
        context["portal_is_admin"] = is_admin
        context["portal_is_editor"] = is_editor
        return context

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        if not self.allowed_groups:
            return False
        return user.groups.filter(name__in=self.allowed_groups).exists()


class PortalListContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        query_params.pop("page", None)
        context["querystring"] = query_params.urlencode()
        return context


class PortalFormLayoutMixin:
    full_width_fields = ()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["portal_full_width_fields"] = list(self.full_width_fields)
        return context


class PortalEditorRequiredMixin(PortalRoleRequiredMixin):
    allowed_groups = ("Admin", "Editor")


class PortalAdminRequiredMixin(PortalRoleRequiredMixin):
    allowed_groups = ("Admin",)
