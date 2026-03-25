from django.test import TestCase
from django.urls import reverse

from about.models import AboutPage
from core.models import ProgramContentSource
from core.utils.program_content import clear_program_content_cache


class PrincipalHistoryPageTests(TestCase):
    def setUp(self):
        super().setUp()
        clear_program_content_cache()

    def tearDown(self):
        clear_program_content_cache()
        super().tearDown()

    def test_principal_route_renders_history_page(self):
        AboutPage.objects.create(page_type="principal", title="Thong diep cu")

        response = self.client.get(reverse("about:principal"), HTTP_HOST="localhost")

        self.assertEqual(response.status_code, 200)
        # Principal page now shows founder message, not history
        self.assertContains(response, "Thông điệp từ ban lãnh đạo")
        self.assertContains(response, "Triết lý điều hành")

    def test_principal_route_falls_back_when_db_content_is_partial(self):
        AboutPage.objects.create(page_type="principal", title="Thong diep cu")
        ProgramContentSource.objects.create(
            year="2026-2027",
            is_active=True,
            version="test",
            content={
                "program_year": "2026-2027",
                "blocks": {
                    "lifeskills": {
                        "key": "lifeskills",
                        "title": "Future with Heart",
                    }
                },
            },
        )

        response = self.client.get(reverse("about:principal"), HTTP_HOST="localhost")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Thông điệp từ ban lãnh đạo")
        self.assertContains(response, "Hệ thống Giáo dục Đa Trí Tuệ MIS")
