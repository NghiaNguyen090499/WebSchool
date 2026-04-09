import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import AdmissionConsultation, AdmissionDocument, AdmissionInfo, AdmissionRegistration


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


class AdmissionEntryPointTests(TestCase):
    def setUp(self):
        super().setUp()
        admission = AdmissionInfo.objects.create(
            level="mam_non",
            title="Preschool",
            description="Description",
            requirements="Requirements",
            tuition_info="Tuition",
            process="Process",
        )
        self.detail_url = reverse("admissions:detail", kwargs={"level": admission.level})
        self.list_url = reverse("admissions:list")
        self.registration_url = reverse("admissions:registration")
        self.consultation_url = f"{self.list_url}#tu-van"
        self.application_url = f"{self.list_url}#du-tuyen"
        self.contact_url = reverse("contact:contact")

    def test_admission_detail_routes_consultation_to_new_registration_page(self):
        response = self.client.get(self.detail_url, HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'href="{self.consultation_url}"')
        self.assertNotContains(response, 'x-text="errors.parent_name"')
        self.assertNotContains(response, 'x-text="errors.parent_phone"')
        self.assertNotContains(response, 'x-text="errors.student_name"')
        self.assertNotContains(response, 'x-text="errors.student_dob"')
        self.assertNotContains(response, 'x-text="errors.student_gender"')
        self.assertNotContains(response, 'x-text="errors.address"')

    def test_admission_list_routes_consultation_to_new_registration_page(self):
        response = self.client.get(self.list_url, HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'href="{self.consultation_url}"')
        self.assertContains(response, self.application_url)
        self.assertContains(response, '@submit.prevent="submitRegistration($event)"')
        self.assertContains(response, 'id="du-tuyen"')
        self.assertContains(response, 'id="tu-van"')
        self.assertContains(response, "Quy trình tuyển sinh")
        self.assertNotContains(response, "Đăng ký tuyển sinh theo từng bước")


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
            "parent_email_confirm": "parent@example.com",
            "contact_relationship": "me",
            "student_name": "Student",
            "student_dob": "2015-01-01",
            "student_gender": "male",
            "address": "Address",
            "target_grade": "mam_non",
            "training_program": "steam_chuan",
            "registration_school_year": "2026-2027",
            "admission_method": "xet_tuyen_thang",
        }
        response = self.client.post(
            reverse("admissions:submit"),
            data=payload,
            HTTP_HOST="localhost",
            REMOTE_ADDR="127.0.0.11",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Email không hợp lệ", response.json().get("message", ""))

    def test_invalid_gender_rejected(self):
        payload = {
            "level": self.admission.level,
            "parent_name": "Parent",
            "parent_phone": "0912345678",
            "parent_email": "parent@example.com",
            "parent_email_confirm": "parent@example.com",
            "contact_relationship": "me",
            "student_name": "Student",
            "student_dob": "2015-01-01",
            "student_gender": "unknown",
            "address": "Address",
            "target_grade": "mam_non",
            "training_program": "steam_chuan",
            "registration_school_year": "2026-2027",
            "admission_method": "xet_tuyen_thang",
        }
        response = self.client.post(
            reverse("admissions:submit"),
            data=payload,
            HTTP_HOST="localhost",
            REMOTE_ADDR="127.0.0.12",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Giới tính không hợp lệ", response.json().get("message", ""))

    def test_study_abroad_country_required_when_plan_is_true(self):
        payload = {
            "level": self.admission.level,
            "parent_name": "Parent",
            "parent_phone": "0912345678",
            "parent_email": "parent@example.com",
            "parent_email_confirm": "parent@example.com",
            "contact_relationship": "me",
            "student_name": "Student",
            "student_dob": "2015-01-01",
            "student_gender": "male",
            "address": "Address",
            "target_grade": "mam_non",
            "training_program": "steam_chuan",
            "registration_school_year": "2026-2027",
            "admission_method": "xet_tuyen_thang",
            "study_abroad_plan": "true",
            "study_abroad_country": "",
        }
        response = self.client.post(
            reverse("admissions:submit"),
            data=payload,
            HTTP_HOST="localhost",
            REMOTE_ADDR="127.0.0.13",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Vui lòng nhập quốc gia dự định du học", response.json().get("message", ""))

    def test_study_abroad_country_saved_when_plan_is_true(self):
        payload = {
            "level": self.admission.level,
            "parent_name": "Parent",
            "parent_phone": "0912345678",
            "parent_email": "parent@example.com",
            "parent_email_confirm": "parent@example.com",
            "contact_relationship": "me",
            "student_name": "Student",
            "student_dob": "2015-01-01",
            "student_gender": "male",
            "address": "Address",
            "target_grade": "mam_non",
            "training_program": "steam_chuan",
            "registration_school_year": "2026-2027",
            "admission_method": "xet_tuyen_thang",
            "study_abroad_plan": "true",
            "study_abroad_country": "Singapore",
        }
        response = self.client.post(
            reverse("admissions:submit"),
            data=payload,
            HTTP_HOST="localhost",
            REMOTE_ADDR="127.0.0.14",
        )
        self.assertEqual(response.status_code, 200)
        registration = AdmissionRegistration.objects.latest("id")
        self.assertTrue(registration.study_abroad_plan)
        self.assertEqual(registration.study_abroad_country, "Singapore")


class AdmissionRegistrationPageTests(TestCase):
    def test_admission_list_renders_single_form_without_step_wizard(self):
        response = self.client.get(
            reverse("admissions:list"),
            HTTP_HOST="localhost",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '@submit.prevent="submitRegistration($event)"')
        self.assertContains(response, "Học bạ - Phiếu điểm HK1, HK2")
        self.assertContains(response, "Quốc gia dự định du học")
        self.assertNotContains(response, "nextStep()")
        self.assertNotContains(response, 'step === 1')
        self.assertNotContains(response, "step: 1")

    def test_legacy_registration_page_redirects_to_admissions_list(self):
        response = self.client.get(
            reverse("admissions:registration"),
            HTTP_HOST="localhost",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="legacy-registration-link"')
        self.assertContains(response, reverse("admissions:list"))
        self.assertContains(response, "window.location.replace(destination);")
        self.assertNotContains(response, '@submit.prevent="submitRegistration($event)"')


class AdmissionConsultationTests(TestCase):
    def test_consultation_submission_persists_interest_checkboxes(self):
        payload = {
            "target_grade": "lop_1",
            "training_program": "steam_chuan",
            "details": "Muon tim hieu chi tiet.",
            "interest_visit": "true",
            "interest_curriculum": "false",
            "interest_admission_process": "true",
            "parent_name": "Parent",
            "phone": "0912345678",
            "email": "parent@example.com",
            "email_confirm": "parent@example.com",
        }

        response = self.client.post(
            reverse("admissions:submit_consultation"),
            data=payload,
            HTTP_HOST="localhost",
        )

        self.assertEqual(response.status_code, 200)
        consultation = AdmissionConsultation.objects.get()
        self.assertTrue(consultation.interest_visit)
        self.assertFalse(consultation.interest_curriculum)
        self.assertTrue(consultation.interest_admission_process)
