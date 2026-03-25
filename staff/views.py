from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator

from .models import Staff


def staff_list(request):
    role = request.GET.get("role", "").strip()
    staff_qs = Staff.objects.filter(is_active=True)
    role_values = {value for value, _ in Staff.ROLE_CHOICES}

    if role in role_values:
        staff_qs = staff_qs.filter(role=role)
    else:
        role = ""

    paginator = Paginator(staff_qs, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "staff_list": page_obj,
        "page_obj": page_obj,
        "role_selected": role,
        "roles": Staff.ROLE_CHOICES,
    }
    return render(request, "staff/list.html", context)


def staff_detail(request, slug):
    staff = get_object_or_404(Staff, slug=slug, is_active=True)
    return render(request, "staff/detail.html", {"staff": staff})
