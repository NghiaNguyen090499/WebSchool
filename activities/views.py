from collections import defaultdict

from django.db.models import Q
from django.shortcuts import render

from .models import Activity


def activity_list(request):
    activities = Activity.objects.filter(is_active=True).order_by("start_date")
    query = request.GET.get("q", "").strip()
    if query:
        activities = activities.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    type_filter = request.GET.get("type", "").strip()
    if type_filter:
        activities = activities.filter(type=type_filter)
    grouped = defaultdict(list)
    for item in activities:
        grouped[item.type].append(item)

    activity_groups = [
        {"value": value, "label": label, "items": grouped.get(value, [])}
        for value, label in Activity.TYPE_CHOICES
    ]

    context = {
        "activities": activities,
        "activity_groups": activity_groups,
        "query": query,
        "selected_type": type_filter,
        "has_results": activities.exists(),
    }
    return render(request, "activities/list.html", context)
