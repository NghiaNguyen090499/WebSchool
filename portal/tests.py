import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from admissions.models import AdmissionInfo, AdmissionRegistration
from events.models import Event
from news.models import Category, News

from .forms import EventForm, NewsForm, PortalMediaAssetForm
from .models import PortalAuditLog, PortalMediaAsset


class PortalAdmissionsExportTests(TestCase):
    def test_export_csv_returns_header(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="portal_admin",
            password="password123",
            is_staff=True,
            is_superuser=True,
        )
        self.client.force_login(user)

        admission = AdmissionInfo.objects.create(
            level="mam_non",
            title="Preschool",
            description="Description",
            requirements="Requirements",
            tuition_info="Tuition",
            process="Process",
        )
        AdmissionRegistration.objects.create(
            admission=admission,
            parent_name="Parent",
            parent_phone="0912345678",
            parent_email="parent@example.com",
            student_name="Student",
            student_dob=timezone.now().date(),
            student_gender="male",
            address="Hanoi",
        )

        url = reverse("portal:admissions_registrations_export")
        response = self.client.get(url, HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/csv", response["Content-Type"])

        content = response.content.decode("utf-8-sig")
        first_line = content.splitlines()[0]
        self.assertIn("Parent Name", first_line)
        self.assertIn("Parent Phone", first_line)
        self.assertIn("Student Name", first_line)
        self.assertIn("Status", first_line)


class PortalAdmissionsExportSanitizeTests(TestCase):
    def test_export_csv_escapes_formula(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="portal_admin",
            password="password123",
            is_staff=True,
            is_superuser=True,
        )
        self.client.force_login(user)

        admission = AdmissionInfo.objects.create(
            level="mam_non",
            title="Preschool",
            description="Description",
            requirements="Requirements",
            tuition_info="Tuition",
            process="Process",
        )
        AdmissionRegistration.objects.create(
            admission=admission,
            parent_name="=HYPERLINK(\"https://example.com\",\"click\")",
            parent_phone="0912345678",
            parent_email="parent@example.com",
            student_name="Student",
            student_dob=timezone.now().date(),
            student_gender="male",
            address="Hanoi",
        )

        url = reverse("portal:admissions_registrations_export")
        response = self.client.get(url, HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8-sig")
        self.assertIn("'=HYPERLINK", content)


class PortalSlugValidationTests(TestCase):
    def test_news_form_duplicate_slug(self):
        News.objects.create(title="News 1", slug="duplicate", content="Content")
        form = NewsForm(
            data={
                "title": "News 2",
                "slug": "duplicate",
                "content": "Content",
                "excerpt": "",
                "is_featured": False,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("slug", form.errors)

    def test_event_form_duplicate_slug(self):
        Event.objects.create(
            title="Event 1",
            slug="duplicate",
            date=timezone.now().date(),
            location="Hanoi",
            description="Desc",
        )
        form = EventForm(
            data={
                "title": "Event 2",
                "slug": "duplicate",
                "date": timezone.now().date(),
                "location": "Hanoi",
                "description": "Desc",
                "is_featured": False,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("slug", form.errors)


class PortalMediaValidationTests(TestCase):
    def setUp(self):
        super().setUp()
        self.temp_media = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.temp_media, ignore_errors=True)
        self.override_media = override_settings(MEDIA_ROOT=self.temp_media)
        self.override_media.enable()
        self.addCleanup(self.override_media.disable)

    def test_disallowed_extension_rejected(self):
        upload = SimpleUploadedFile("malware.exe", b"data", content_type="application/octet-stream")
        form = PortalMediaAssetForm(
            data={"file_type": "image", "alt_text": "Test"},
            files={"file": upload},
        )
        self.assertFalse(form.is_valid())
        self.assertIn("file", form.errors)

    def test_mismatched_file_type_rejected(self):
        upload = SimpleUploadedFile("document.pdf", b"%PDF-1.4", content_type="application/pdf")
        form = PortalMediaAssetForm(
            data={"file_type": "image", "alt_text": "PDF pretending to be image"},
            files={"file": upload},
        )
        self.assertFalse(form.is_valid())
        self.assertIn("file", form.errors)

    @override_settings(UPLOAD_MAX_FILE_SIZE=5, FILE_UPLOAD_MAX_MEMORY_SIZE=5)
    def test_oversize_file_rejected(self):
        upload = SimpleUploadedFile("image.png", b"123456", content_type="image/png")
        form = PortalMediaAssetForm(
            data={"file_type": "image", "alt_text": "Too large"},
            files={"file": upload},
        )
        self.assertFalse(form.is_valid())
        self.assertIn("file", form.errors)


class PortalAuditLogCrudTests(TestCase):
    def setUp(self):
        super().setUp()
        User = get_user_model()
        self.user = User.objects.create_user(
            username="portal_superuser",
            password="password123",
            is_staff=True,
            is_superuser=True,
        )
        self.client.force_login(self.user)
        self.category = Category.objects.create(name="General")

    def test_news_event_admission_crud_creates_audit_logs(self):
        news_create = self.client.post(
            reverse("portal:news_create"),
            data={
                "title": "Portal News",
                "slug": "portal-news",
                "content": "News body",
                "excerpt": "Short",
                "category": self.category.pk,
                "is_featured": "on",
            },
            HTTP_HOST="localhost",
        )
        self.assertEqual(news_create.status_code, 302)
        news = News.objects.get(slug="portal-news")

        news_update = self.client.post(
            reverse("portal:news_edit", args=[news.pk]),
            data={
                "title": "Portal News Updated",
                "slug": "portal-news",
                "content": "Updated body",
                "excerpt": "Updated short",
                "category": self.category.pk,
                "is_featured": "",
            },
            HTTP_HOST="localhost",
        )
        self.assertEqual(news_update.status_code, 302)

        news_delete = self.client.post(
            reverse("portal:news_delete", args=[news.pk]),
            HTTP_HOST="localhost",
        )
        self.assertEqual(news_delete.status_code, 302)

        event_create = self.client.post(
            reverse("portal:event_create"),
            data={
                "title": "Portal Event",
                "slug": "portal-event",
                "date": "2026-02-01",
                "time": "09:30",
                "location": "Hanoi",
                "description": "Event body",
                "is_featured": "on",
            },
            HTTP_HOST="localhost",
        )
        self.assertEqual(event_create.status_code, 302)
        event = Event.objects.get(slug="portal-event")

        event_update = self.client.post(
            reverse("portal:event_edit", args=[event.pk]),
            data={
                "title": "Portal Event Updated",
                "slug": "portal-event",
                "date": "2026-02-03",
                "time": "10:00",
                "location": "Hanoi",
                "description": "Event updated",
                "is_featured": "",
            },
            HTTP_HOST="localhost",
        )
        self.assertEqual(event_update.status_code, 302)

        event_delete = self.client.post(
            reverse("portal:event_delete", args=[event.pk]),
            HTTP_HOST="localhost",
        )
        self.assertEqual(event_delete.status_code, 302)

        admission_create = self.client.post(
            reverse("portal:admissions_create"),
            data={
                "level": "thcs",
                "title": "THCS Program",
                "school_year": "2026-2027",
                "subtitle": "Subtitle",
                "description": "Description",
                "requirements": "Requirements",
                "tuition_info": "Tuition",
                "process": "Process",
                "benefits": "Benefits",
                "facilities": "Facilities",
                "curriculum": "Curriculum",
                "icon": "fas fa-graduation-cap",
                "color": "red",
                "is_active": "on",
                "order": 1,
            },
            HTTP_HOST="localhost",
        )
        self.assertEqual(admission_create.status_code, 302)
        admission = AdmissionInfo.objects.get(level="thcs")

        admission_update = self.client.post(
            reverse("portal:admissions_edit", args=[admission.pk]),
            data={
                "level": "thcs",
                "title": "THCS Program Updated",
                "school_year": "2026-2027",
                "subtitle": "Subtitle",
                "description": "Description",
                "requirements": "Requirements",
                "tuition_info": "Tuition",
                "process": "Process",
                "benefits": "Benefits",
                "facilities": "Facilities",
                "curriculum": "Curriculum",
                "icon": "fas fa-graduation-cap",
                "color": "red",
                "is_active": "on",
                "order": 2,
            },
            HTTP_HOST="localhost",
        )
        self.assertEqual(admission_update.status_code, 302)

        admission_delete = self.client.post(
            reverse("portal:admissions_delete", args=[admission.pk]),
            HTTP_HOST="localhost",
        )
        self.assertEqual(admission_delete.status_code, 302)

        self.assertTrue(
            PortalAuditLog.objects.filter(action="create", target_model="news.news").exists()
        )
        self.assertTrue(
            PortalAuditLog.objects.filter(action="update", target_model="news.news").exists()
        )
        self.assertTrue(
            PortalAuditLog.objects.filter(action="delete", target_model="news.news").exists()
        )

        self.assertTrue(
            PortalAuditLog.objects.filter(action="create", target_model="events.event").exists()
        )
        self.assertTrue(
            PortalAuditLog.objects.filter(action="update", target_model="events.event").exists()
        )
        self.assertTrue(
            PortalAuditLog.objects.filter(action="delete", target_model="events.event").exists()
        )

        self.assertTrue(
            PortalAuditLog.objects.filter(action="create", target_model="admissions.admissioninfo").exists()
        )
        self.assertTrue(
            PortalAuditLog.objects.filter(action="update", target_model="admissions.admissioninfo").exists()
        )
        self.assertTrue(
            PortalAuditLog.objects.filter(action="delete", target_model="admissions.admissioninfo").exists()
        )


class PortalAuditLogMediaUploadTests(TestCase):
    def setUp(self):
        super().setUp()
        self.temp_media = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.temp_media, ignore_errors=True)
        self.override_media = override_settings(MEDIA_ROOT=self.temp_media)
        self.override_media.enable()
        self.addCleanup(self.override_media.disable)

        User = get_user_model()
        self.user = User.objects.create_user(
            username="portal_media_admin",
            password="password123",
            is_staff=True,
            is_superuser=True,
        )
        self.client.force_login(self.user)

    def test_media_upload_creates_audit_log(self):
        upload = SimpleUploadedFile("hero.png", b"pngdata", content_type="image/png")
        response = self.client.post(
            reverse("portal:media_upload"),
            data={"file_type": "image", "alt_text": "Hero image", "file": upload},
            HTTP_HOST="localhost",
        )
        self.assertEqual(response.status_code, 302)

        asset = PortalMediaAsset.objects.latest("id")
        self.assertTrue(
            PortalAuditLog.objects.filter(
                action="upload",
                target_model="portal.portalmediaasset",
                target_object_id=str(asset.pk),
            ).exists()
        )
