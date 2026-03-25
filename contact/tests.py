from django.test import TestCase
from django.urls import reverse


class ContactFormPlaceholderTests(TestCase):
    def test_contact_form_placeholders_in_vietnamese(self):
        response = self.client.get(reverse("contact:contact"), HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)
        # Verify placeholders match current forms.py widgets
        self.assertContains(response, 'placeholder="Nguyễn Văn A"')
        self.assertContains(response, 'placeholder="email@example.com"')
        self.assertContains(response, 'placeholder="Nhập nội dung bạn muốn liên hệ..."')
