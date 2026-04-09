import shutil
import tempfile
from datetime import timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from core.models import StudentLifePage, StudentSpotlight, Podcast
from events.models import Event
from gallery.models import Album, Photo
from news.models import Category, News
from staff.models import Staff


SMALL_GIF = (
    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00"
    b"!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01"
    b"\x00\x00\x02\x02D\x01\x00;"
)


class PublicRoutesTests(TestCase):
    def test_sitemap_returns_200(self):
        response = self.client.get("/sitemap.xml", HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)

    def test_robots_returns_200(self):
        response = self.client.get("/robots.txt", HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)

    def test_home_footer_uses_unified_admissions_cta_instead_of_old_form(self):
        response = self.client.get(reverse("core:home"), HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="/tuyen-sinh/#tu-van"')
        self.assertContains(response, 'href="/tuyen-sinh/#du-tuyen"')
        self.assertNotContains(response, 'id="consultationForm"')


class NewsSearchTests(TestCase):
    def test_news_search_filters_by_query(self):
        category = Category.objects.create(name="General")
        news_match = News.objects.create(
            title="Alpha story",
            content="Hello world",
            category=category,
        )
        news_other = News.objects.create(
            title="Beta story",
            content="Other content",
            category=category,
        )

        response = self.client.get("/news/?q=Alpha", HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)
        # Search should find 1 result (Alpha), not 2
        self.assertEqual(response.context["total_news"], 1)
        self.assertContains(response, "Alpha story")
        self.assertNotContains(response, "Beta story")


class GalleryAnnotationTests(TestCase):
    def setUp(self):
        super().setUp()
        self.temp_media = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.temp_media, ignore_errors=True)
        self.override_media = override_settings(MEDIA_ROOT=self.temp_media)
        self.override_media.enable()
        self.addCleanup(self.override_media.disable)

    def test_gallery_context_has_photo_count(self):
        cover = SimpleUploadedFile("cover.gif", SMALL_GIF, content_type="image/gif")
        album = Album.objects.create(name="Album 1", cover_image=cover)
        photo_1 = SimpleUploadedFile("photo1.gif", SMALL_GIF, content_type="image/gif")
        photo_2 = SimpleUploadedFile("photo2.gif", SMALL_GIF, content_type="image/gif")
        Photo.objects.create(album=album, image=photo_1)
        Photo.objects.create(album=album, image=photo_2)

        response = self.client.get("/gallery/", HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)
        albums = list(response.context["albums"])
        self.assertTrue(albums)
        self.assertTrue(hasattr(albums[0], "photo_count"))
        self.assertEqual(albums[0].photo_count, 2)


class EventsPaginationTests(TestCase):
    def test_events_pagination_page_2(self):
        today = timezone.now().date()
        for i in range(7):
            Event.objects.create(
                title=f"Past {i}",
                date=today - timedelta(days=i + 1),
                time=timezone.now().time(),
                location="Hanoi",
                description="Description",
            )

        response = self.client.get("/events/?page=2", HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)
        page_obj = response.context["past_page_obj"]
        self.assertEqual(page_obj.number, 2)


class StaffPaginationTests(TestCase):
    def test_staff_pagination_page_2(self):
        for i in range(13):
            Staff.objects.create(name=f"Staff {i}", role="teacher", is_active=True)

        response = self.client.get("/doi-ngu/?page=2", HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)
        page_obj = response.context["page_obj"]
        self.assertEqual(page_obj.number, 2)


class StudentLifeNoCreateTests(TestCase):
    def test_student_life_get_does_not_create_record(self):
        self.assertEqual(StudentLifePage.objects.count(), 0)
        response = self.client.get("/doi-song-hoc-sinh/", HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(StudentLifePage.objects.count(), 0)


class StudentSpotlightCtaTests(TestCase):
    def test_spotlight_cta_points_to_admissions_list(self):
        spotlight_url = reverse("core:student_spotlight")
        admissions_url = reverse("admissions:list")

        response = self.client.get(spotlight_url, HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'href="{admissions_url}#tu-van"')
        self.assertNotContains(response, 'action="/tuyen-sinh/dang-ky/"')


class StudentSpotlightPaginationTests(TestCase):
    def setUp(self):
        super().setUp()
        self.temp_media = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.temp_media, ignore_errors=True)
        self.override_media = override_settings(MEDIA_ROOT=self.temp_media)
        self.override_media.enable()
        self.addCleanup(self.override_media.disable)

    def test_spotlight_pagination_preserves_category(self):
        for i in range(13):
            photo = SimpleUploadedFile(f"spotlight{i}.gif", SMALL_GIF, content_type="image/gif")
            StudentSpotlight.objects.create(
                student_name=f"Student {i}",
                photo=photo,
                title="Achievement",
                achievement="Details",
                category="academic",
                is_active=True,
            )

        response = self.client.get("/guong-mat-misers/?category=academic&page=2", HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page_obj"].number, 2)
        self.assertContains(response, "page=1&category=academic")


class PodcastInvalidUrlTests(TestCase):
    def test_invalid_podcast_url_renders(self):
        Podcast.objects.create(
            title="Invalid Podcast",
            description="Desc",
            youtube_url="https://example.com/video",
            episode_number=1,
            is_featured=True,
        )

        response = self.client.get("/tieng-noi-misers/", HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Liên kết không hợp lệ")


class HealthEndpointTests(TestCase):
    def test_healthz_ok(self):
        response = self.client.get("/healthz/", HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("utf-8").strip(), "ok")

    def test_readyz_ok(self):
        response = self.client.get("/readyz/", HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)
