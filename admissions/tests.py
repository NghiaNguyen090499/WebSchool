import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import AdmissionDocument, AdmissionInfo


class AdmissionDownloadTests(TestCase):
    def setUp(self):
        super().setUp()
        self.temp_media = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.temp_media, ignore_errors=True)
        self.override_media = override_settings(MEDIA_ROOT=self.temp_media)
        self.override_media.enable()
        self.addCleanup(self.override_media.disable)

    def test_document_download_increments_count(self):
        admission = AdmissionInfo.objects.create(
            level="mam_non",
            title="Preschool",
            description="Description",
            requirements="Requirements",
            tuition_info="Tuition",
            process="Process",
        )
        upload = SimpleUploadedFile(
            "doc.pdf",
            b"%PDF-1.4 test",
            content_type="application/pdf",
        )
        document = AdmissionDocument.objects.create(
            admission=admission,
            title="Document",
            file=upload,
        )
        url = reverse("admissions:document_download", args=[document.pk])

        response = self.client.get(url, HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 302)
        document.refresh_from_db()
        self.assertEqual(document.download_count, 1)

        response = self.client.get(url, HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 302)
        document.refresh_from_db()
        self.assertEqual(document.download_count, 2)


class AdmissionInlineErrorMarkupTests(TestCase):
    def test_admission_form_has_inline_error_markup(self):
        admission = AdmissionInfo.objects.create(
            level="mam_non",
            title="Preschool",
            description="Description",
            requirements="Requirements",
            tuition_info="Tuition",
            process="Process",
        )
        url = reverse("admissions:detail", kwargs={"level": admission.level})

        response = self.client.post(url, data={"parent_name": ""}, HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'x-text="errors.parent_name"')
        self.assertContains(response, 'x-text="errors.parent_phone"')
        self.assertContains(response, 'x-text="errors.student_name"')
        self.assertContains(response, 'x-text="errors.student_dob"')
        self.assertContains(response, 'x-text="errors.student_gender"')
        self.assertContains(response, 'x-text="errors.address"')
        self.assertContains(response, 'x-show="formError"')
        self.assertNotContains(response, "alert(")


class AdmissionRegistrationValidationTests(TestCase):
    def setUp(self):
        super().setUp()
        self.admission = AdmissionInfo.objects.create(
            level="mam_non",
            title="Preschool",
            description="Description",
            requirements="Requirements",
            tuition_info="Tuition",
            process="Process",
        )

    def test_invalid_email_rejected(self):
        payload = {
            "level": self.admission.level,
            "parent_name": "Parent",
            "parent_phone": "0912345678",
            "parent_email": "invalid-email",
            "student_name": "Student",
            "student_dob": "2015-01-01",
            "student_gender": "male",
            "address": "Address",
        }
        response = self.client.post(
            reverse("admissions:submit"),
            data=payload,
            HTTP_HOST="localhost",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Email không hợp lệ", response.json().get("message", ""))

    def test_invalid_gender_rejected(self):
        payload = {
            "level": self.admission.level,
            "parent_name": "Parent",
            "parent_phone": "0912345678",
            "parent_email": "parent@example.com",
            "student_name": "Student",
            "student_dob": "2015-01-01",
            "student_gender": "unknown",
            "address": "Address",
        }
        response = self.client.post(
            reverse("admissions:submit"),
            data=payload,
            HTTP_HOST="localhost",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Giới tính không hợp lệ", response.json().get("message", ""))
