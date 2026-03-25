from django.test import TestCase

from .models import News, Category


class NewsRichTextSanitizerTests(TestCase):
    def test_news_detail_sanitizes_html(self):
        category = Category.objects.create(name="General")
        news = News.objects.create(
            title="Hello",
            content="<script>alert(1)</script><p>Hello</p>",
            category=category,
        )

        response = self.client.get(news.get_absolute_url(), HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "<script>alert(1)</script>")
        self.assertContains(response, "<p>Hello</p>", html=True)
