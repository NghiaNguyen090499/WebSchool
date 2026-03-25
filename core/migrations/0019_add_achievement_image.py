from django.db import migrations, models


def seed_achievement_awards(apps, schema_editor):
    Achievement = apps.get_model("core", "Achievement")
    awards = [
        {
            "title": "TOP 10",
            "description": "Thương hiệu tiêu biểu Châu Á - Thái Bình Dương 2025 (Trung Quốc)",
            "icon": "fas fa-award",
            "tags": "2025",
            "category": "competition",
            "color": "red",
            "stat_value": "",
            "stat_label": "",
            "is_stat": False,
            "is_card": True,
            "is_active": True,
            "year": 2025,
            "order": 1,
            "image": "achiement/cup1.png",
        },
        {
            "title": "TOP 50",
            "description": "Thương hiệu nổi tiếng ASEAN 2025 (Singapore)",
            "icon": "fas fa-globe",
            "tags": "2025",
            "category": "competition",
            "color": "amber",
            "stat_value": "",
            "stat_label": "",
            "is_stat": False,
            "is_card": True,
            "is_active": True,
            "year": 2025,
            "order": 2,
            "image": "achiement/cup2.png",
        },
        {
            "title": "TOP 20",
            "description": "Thương hiệu sản phẩm dịch vụ chất lượng vàng vì quyền lợi người tiêu dùng Việt Nam 2025",
            "icon": "fas fa-medal",
            "tags": "2025",
            "category": "competition",
            "color": "red",
            "stat_value": "",
            "stat_label": "",
            "is_stat": False,
            "is_card": True,
            "is_active": True,
            "year": 2025,
            "order": 3,
            "image": "achiement/cup3.png",
        },
    ]

    for item in awards:
        Achievement.objects.update_or_create(
            title=item["title"],
            defaults=item,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0018_alter_corevalue_options_achievement_year_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="achievement",
            name="image",
            field=models.ImageField(
                blank=True,
                help_text="Optional image for achievement card",
                null=True,
                upload_to="achiement/",
                verbose_name="Image",
            ),
        ),
        migrations.RunPython(seed_achievement_awards, migrations.RunPython.noop),
    ]
