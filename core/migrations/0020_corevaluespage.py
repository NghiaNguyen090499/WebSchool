from django.db import migrations, models


def seed_core_values_page(apps, schema_editor):
    CoreValuesPage = apps.get_model("core", "CoreValuesPage")
    if CoreValuesPage.objects.filter(is_active=True).exists():
        return

    CoreValuesPage.objects.create(
        title="Giá trị cốt lõi",
        subtitle="Đa trí tuệ - đa phương pháp - đa trải nghiệm & một nhân cách",
        grace_title="GRACE",
        social_title="Trách nhiệm xã hội",
        social_content=(
            "Quỹ thiện nguyện MIS trong hơn 10 năm hoạt động đã không ngừng lan tỏa yêu thương qua các dự án\n"
            "cộng đồng giá trị với những hoạt động thiết thực như xây trường, mở đường, sửa sang cơ sở vật chất\n"
            "cho các trường học vùng khó khăn.\n\n"
            "Không dừng lại ở đó, Quỹ còn trao tặng học bổng, trang thiết bị học tập, giúp các em vững bước đến\n"
            "trường và nuôi dưỡng ước mơ hướng tới cuộc sống tốt đẹp hơn. Và nhiều các dự án cứu trợ khác trên\n"
            "khắp mọi miền Tổ quốc."
        ),
        image="gallery/photos/mis_ho_tro_xay_truong.jpg",
        image_heading="MIS hỗ trợ xây mới",
        image_title="Trường Mầm non Háng Phù Loa",
        image_location="Mồ Dề - Mù Cang Chải - Yên Bái",
        is_active=True,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0019_add_achievement_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="CoreValuesPage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(default="Giá trị cốt lõi", max_length=200)),
                ("subtitle", models.CharField(blank=True, default="Đa trí tuệ - đa phương pháp - đa trải nghiệm & một nhân cách", max_length=300)),
                ("grace_title", models.CharField(default="GRACE", max_length=100)),
                ("social_title", models.CharField(default="Trách nhiệm xã hội", max_length=200)),
                ("social_content", models.TextField(blank=True)),
                ("image", models.ImageField(blank=True, null=True, upload_to="core_values/")),
                ("image_heading", models.CharField(blank=True, default="MIS hỗ trợ xây mới", max_length=200)),
                ("image_title", models.CharField(blank=True, default="Trường Mầm non Háng Phù Loa", max_length=200)),
                ("image_location", models.CharField(blank=True, default="Mồ Dề - Mù Cang Chải - Yên Bái", max_length=200)),
                ("is_active", models.BooleanField(default=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Giá trị cốt lõi",
                "verbose_name_plural": "Giá trị cốt lõi",
            },
        ),
        migrations.RunPython(seed_core_values_page, migrations.RunPython.noop),
    ]
