import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from .models import Album, Photo


SMALL_GIF = (
    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00"
    b"!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01"
    b"\x00\x00\x02\x02D\x01\x00;"
)


class GalleryPaginationTests(TestCase):
    def setUp(self):
        super().setUp()
        self.temp_media = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.temp_media, ignore_errors=True)
        self.override_media = override_settings(MEDIA_ROOT=self.temp_media)
        self.override_media.enable()
        self.addCleanup(self.override_media.disable)

    def test_album_detail_shows_page_count_and_total(self):
        cover = SimpleUploadedFile("cover.gif", SMALL_GIF, content_type="image/gif")
        album = Album.objects.create(name="Album 1", cover_image=cover)
        for i in range(25):
            photo = SimpleUploadedFile(f"photo{i}.gif", SMALL_GIF, content_type="image/gif")
            Photo.objects.create(album=album, image=photo, caption=f"Photo {i}")

        response = self.client.get(album.get_absolute_url(), HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "20 / 25 ảnh")
        self.assertEqual(len(response.context["page_obj"].object_list), 20)

        response = self.client.get(f"{album.get_absolute_url()}?page=2", HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "5 / 25 ảnh")
        self.assertEqual(len(response.context["page_obj"].object_list), 5)
