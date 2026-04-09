from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admissions", "0008_admissionconsultation_interest_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="admissionregistration",
            name="study_abroad_country",
            field=models.CharField(
                blank=True,
                max_length=100,
                verbose_name="Quốc gia dự định du học",
            ),
        ),
    ]
