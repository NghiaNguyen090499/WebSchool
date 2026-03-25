from django.test import TestCase
from django.urls import reverse


class LandingPageTests(TestCase):
    def test_mis_innovation_day_page_renders(self):
        response = self.client.get(
            reverse("landing:detail", kwargs={"slug": "mis-innovation-day-2026"})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "landing/mis-innovation-day-2026.html")
        self.assertContains(response, "MIS Innovation Day 2026")

    def test_open_day_page_renders(self):
        response = self.client.get(reverse("landing:detail", kwargs={"slug": "open-day-2026"}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "landing/open_day_2026.html")
        self.assertContains(response, "Open Day 2026")

    def test_unknown_slug_returns_404(self):
        response = self.client.get(reverse("landing:detail", kwargs={"slug": "khong-ton-tai"}))

        self.assertEqual(response.status_code, 404)
