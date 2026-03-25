import calendar
from datetime import date

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator

from .models import Event


def events_list(request):
    """List all upcoming events"""
    today = timezone.now().date()
    view_mode = request.GET.get("view", "list")

    if view_mode == "calendar":
        year_param = request.GET.get("year")
        month_param = request.GET.get("month")

        def _parse_int(value, default, min_value, max_value):
            try:
                parsed = int(value)
            except (TypeError, ValueError):
                return default
            return parsed if min_value <= parsed <= max_value else default

        year = _parse_int(year_param, today.year, 2000, 2100)
        month = _parse_int(month_param, today.month, 1, 12)
        first_day = date(year, month, 1)

        month_events = Event.objects.filter(date__year=year, date__month=month).order_by("date")
        events_by_day = {}
        for item in month_events:
            events_by_day.setdefault(item.date, []).append(item)

        calendar_weeks = []
        for week in calendar.Calendar(firstweekday=0).monthdatescalendar(year, month):
            week_days = []
            for day in week:
                week_days.append(
                    {
                        "date": day,
                        "in_month": day.month == month,
                        "is_today": day == today,
                        "is_weekend": day.weekday() >= 5,
                        "events": events_by_day.get(day, []),
                    }
                )
            calendar_weeks.append(week_days)

        prev_month_year = year - 1 if month == 1 else year
        prev_month_value = 12 if month == 1 else month - 1
        next_month_year = year + 1 if month == 12 else year
        next_month_value = 1 if month == 12 else month + 1

        # Monthly themes from school activity plan
        month_themes = {
            3: {"theme": "Non sông gấm vóc", "icon": "fas fa-flag", "color": "red"},
            4: {"theme": "Con Rồng cháu Tiên", "icon": "fas fa-dragon", "color": "amber"},
            5: {"theme": "Chắp cánh ước mơ", "icon": "fas fa-graduation-cap", "color": "blue"},
        }
        current_theme = month_themes.get(month, {})

        context = {
            "view_mode": "calendar",
            "calendar_weeks": calendar_weeks,
            "calendar_month": month,
            "calendar_year": year,
            "month_label": f"Tháng {month}/{year}",
            "prev_month": {"year": prev_month_year, "month": prev_month_value},
            "next_month": {"year": next_month_year, "month": next_month_value},
            "has_events": month_events.exists(),
            "event_count": month_events.count(),
            "today": today,
            "month_theme": current_theme.get("theme", ""),
            "month_theme_icon": current_theme.get("icon", "fas fa-calendar-alt"),
        }
        return render(request, "events/list.html", context)

    upcoming_events = Event.objects.filter(date__gte=today).order_by("date")
    past_events = Event.objects.filter(date__lt=today).order_by("-date")

    paginator = Paginator(past_events, 6)
    page_number = request.GET.get("page")
    past_page_obj = paginator.get_page(page_number)

    context = {
        "view_mode": "list",
        "upcoming_events": upcoming_events,
        "past_events": past_page_obj,
        "past_page_obj": past_page_obj,
    }
    return render(request, "events/list.html", context)


def event_detail(request, slug):
    """Event detail page"""
    event = get_object_or_404(Event, slug=slug)
    related_events = Event.objects.exclude(id=event.id).order_by('date')[:3]
    
    context = {
        'event': event,
        'related_events': related_events,
    }
    return render(request, 'events/detail.html', context)







