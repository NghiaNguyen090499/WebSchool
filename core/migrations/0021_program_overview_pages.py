from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0020_corevaluespage"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProgramOverviewPage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("slug", models.SlugField(max_length=200, unique=True)),
                ("title", models.CharField(max_length=255)),
                ("subtitle", models.CharField(blank=True, max_length=300)),
                ("description", models.TextField(blank=True)),
                ("source_url", models.URLField(blank=True)),
                ("hero_image_url", models.URLField(blank=True)),
                ("order", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Trang chương trình tổng quan",
                "verbose_name_plural": "Trang chương trình tổng quan",
                "ordering": ["order", "title"],
            },
        ),
        migrations.CreateModel(
            name="ProgramOverviewImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image_url", models.URLField()),
                ("alt_text", models.CharField(blank=True, max_length=300)),
                ("caption", models.CharField(blank=True, max_length=300)),
                ("order", models.PositiveIntegerField(default=0)),
                ("page", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="images", to="core.programoverviewpage")),
            ],
            options={
                "verbose_name": "Ảnh chương trình tổng quan",
                "verbose_name_plural": "Ảnh chương trình tổng quan",
                "ordering": ["order"],
            },
        ),
    ]
