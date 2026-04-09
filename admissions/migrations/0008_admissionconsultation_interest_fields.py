from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admissions", "0007_admissionconsultation_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="admissionconsultation",
            name="interest_admission_process",
            field=models.BooleanField(default=False, verbose_name="Tư vấn quy trình tuyển sinh"),
        ),
        migrations.AddField(
            model_name="admissionconsultation",
            name="interest_curriculum",
            field=models.BooleanField(default=False, verbose_name="Tư vấn chương trình học"),
        ),
        migrations.AddField(
            model_name="admissionconsultation",
            name="interest_visit",
            field=models.BooleanField(default=False, verbose_name="Hẹn lịch tham quan trường"),
        ),
    ]
