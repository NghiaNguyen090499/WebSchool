from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Event


def events_list(request):
    """List all upcoming events"""
    today = timezone.now().date()
    upcoming_events = Event.objects.filter(date__gte=today).order_by('date')
    past_events = Event.objects.filter(date__lt=today).order_by('-date')
    
    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }
    return render(request, 'events/list.html', context)


def event_detail(request, slug):
    """Event detail page"""
    event = get_object_or_404(Event, slug=slug)
    related_events = Event.objects.exclude(id=event.id).order_by('date')[:3]
    
    context = {
        'event': event,
        'related_events': related_events,
    }
    return render(request, 'events/detail.html', context)



