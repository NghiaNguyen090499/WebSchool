from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0022_seed_program_overview_pages"),
    ]

    operations = [
        migrations.AddField(
            model_name="programoverviewpage",
            name="hero_image",
            field=models.ImageField(blank=True, null=True, upload_to="program_overview/hero/"),
        ),
        migrations.AddField(
            model_name="programoverviewimage",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="program_overview/pages/"),
        ),
    ]
