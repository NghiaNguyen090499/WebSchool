from django.core.management.base import BaseCommand

from about.models import AboutPage
from core.models import StudentLifePage


class Command(BaseCommand):
    help = "Seed default content pages if missing."

    def handle(self, *args, **options):
        if StudentLifePage.objects.exists():
            self.stdout.write("StudentLifePage already exists. No changes made.")
        else:
            StudentLifePage.objects.create(
                title="Đời sống học sinh",
                slug="doi-song-hoc-sinh",
                description="Khám phá cuộc sống học tập và sinh hoạt tại MIS",
                is_active=True,
            )
            self.stdout.write(self.style.SUCCESS("Seeded StudentLifePage."))

        required_about_pages = [
            "mission",
            "vision",
            "principal",
            "strengths",
            "strategy",
            "strategy_2025_2028",
            "structure",
            "culture",
            "boarding",
            "happiness",
            "liberal",
            "vision_2033",
            "whymis",
            "academics",
            "preschool",
            "primary",
            "middle",
            "high",
            "overview_math",
            "overview_literature",
            "overview_english",
            "overview_chinese",
            "tnst",
            "steam",
            "robotics",
            "lifeskills",
            "creative_movement",
            "schedule_2025",
            "schedule_hd",
        ]
        labels = dict(AboutPage.PAGE_CHOICES)
        created_count = 0
        for page_type in required_about_pages:
            title = labels.get(page_type, page_type.replace("_", " ").title())
            _, created = AboutPage.objects.get_or_create(
                page_type=page_type,
                defaults={"title": title},
            )
            if created:
                created_count += 1
        self.stdout.write(
            self.style.SUCCESS(f"Seeded About Pages: {created_count} created.")
        )
