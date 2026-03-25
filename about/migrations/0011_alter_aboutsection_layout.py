from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("about", "0010_aboutsection_feature_image_1_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="aboutsection",
            name="layout",
            field=models.CharField(
                choices=[
                    ("hero", "Hero Section"),
                    ("text_left", "Text Left, Image Right"),
                    ("text_right", "Text Right, Image Left"),
                    ("full_text", "Full Width Text"),
                    ("stats", "Statistics/Numbers"),
                    ("quote", "Quote/Testimonial"),
                    ("cta", "Call to Action"),
                    ("features", "Feature Grid"),
                    ("future_ai", "Future With AI"),
                ],
                default="full_text",
                max_length=20,
            ),
        ),
    ]
