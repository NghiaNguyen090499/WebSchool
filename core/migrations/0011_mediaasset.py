from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0010_facility_pillar"),
    ]

    operations = [
        migrations.CreateModel(
            name="MediaAsset",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("file", models.FileField(blank=True, null=True, upload_to="mis/2026/")),
                ("file_webp", models.ImageField(blank=True, null=True, upload_to="mis/2026/")),
                ("file_jpeg", models.ImageField(blank=True, null=True, upload_to="mis/2026/")),
                ("poster", models.ImageField(blank=True, null=True, upload_to="mis/2026/")),
                ("file_type", models.CharField(choices=[("image", "Image"), ("video", "Video"), ("doc", "Document"), ("other", "Other")], default="image", max_length=20)),
                ("original_name", models.CharField(max_length=255)),
                ("slug", models.SlugField(max_length=255)),
                ("category", models.CharField(choices=[("home", "Home"), ("about", "About"), ("admissions", "Admissions"), ("academics", "Academics"), ("student_life", "Student Life"), ("news", "News"), ("awards", "Awards"), ("events", "Events"), ("csr", "CSR"), ("gallery", "Gallery"), ("unmapped", "Unmapped")], default="unmapped", max_length=50)),
                ("tags", models.JSONField(blank=True, default=list)),
                ("page_target", models.CharField(blank=True, max_length=200)),
                ("block_target", models.CharField(blank=True, max_length=200)),
                ("caption", models.CharField(blank=True, max_length=300)),
                ("alt_text", models.CharField(blank=True, max_length=300)),
                ("notes", models.TextField(blank=True)),
                ("width", models.IntegerField(blank=True, null=True)),
                ("height", models.IntegerField(blank=True, null=True)),
                ("duration", models.FloatField(blank=True, null=True)),
                ("is_approved", models.BooleanField(default=False)),
                ("needs_consent", models.BooleanField(default=False)),
                ("contains_student", models.BooleanField(default=False)),
                ("contains_parent", models.BooleanField(default=False)),
                ("source", models.CharField(default="drive_2026", max_length=100)),
                ("usage_rights_status", models.CharField(choices=[("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")], default="pending", max_length=20)),
                ("checksum", models.CharField(max_length=64)),
                ("file_size", models.PositiveBigIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "indexes": [
                    models.Index(fields=["slug"], name="mediaasset_slug_idx"),
                    models.Index(fields=["checksum", "file_size"], name="mediaasset_checksum_size_idx"),
                ],
            },
        ),
        migrations.AddConstraint(
            model_name="mediaasset",
            constraint=models.UniqueConstraint(fields=("checksum", "file_size"), name="mediaasset_unique_checksum_size"),
        ),
    ]
