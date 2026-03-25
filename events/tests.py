from datetime import date, time

from django.test import TestCase

from .models import Event


class EventsCalendarViewTests(TestCase):
    def test_calendar_view_renders_event_in_month(self):
        event = Event.objects.create(
            title="Calendar Event",
            date=date(2026, 2, 15),
            time=time(9, 0),
            location="Hanoi",
            description="Event description",
        )

        response = self.client.get(
            "/events/?view=calendar&year=2026&month=2",
            HTTP_HOST="localhost",
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, event.title)
