from django.db import migrations


def seed_program_overview_pages(apps, schema_editor):
    ProgramOverviewPage = apps.get_model("core", "ProgramOverviewPage")
    ProgramOverviewImage = apps.get_model("core", "ProgramOverviewImage")

    pages = [
        {
            "slug": "chuong-trinh-tong-quan-mon-toan",
            "title": "CHƯƠNG TRÌNH TỔNG QUAN MÔN TOÁN",
            "source_url": "https://misvn.edu.vn/chuong-trinh-tong-quan-mon-toan/",
            "images": [],
        },
        {
            "slug": "tong-quan-chuong-trinh-ngu-van-tai-mis",
            "title": "TỔNG QUAN CHƯƠNG TRÌNH NGỮ VĂN",
            "source_url": "https://misvn.edu.vn/tong-quan-chuong-trinh-ngu-van-tai-mis/",
            "images": [],
        },
        {
            "slug": "tong-quan-chuong-trinh-tieng-anh",
            "title": "TỔNG QUAN CHƯƠNG TRÌNH TIẾNG ANH",
            "source_url": "https://misvn.edu.vn/tong-quan-chuong-trinh-tieng-anh/",
            "images": [],
        },
        {
            "slug": "chuong-trinh-tong-quan-trai-nghiem-sang-tao-tnst",
            "title": "CHƯƠNG TRÌNH TỔNG QUAN TRẢI NGHIỆM SÁNG TẠO TNST",
            "source_url": "https://misvn.edu.vn/chuong-trinh-tong-quan-trai-nghiem-sang-tao-tnst/",
            "images": [],
        },
        {
            "slug": "chuong-trinh-steam-voi-cong-nghe-sang-tao",
            "title": "CHƯƠNG TRÌNH STEAM VỚI CÔNG NGHỆ SÁNG TẠO",
            "source_url": "https://misvn.edu.vn/chuong-trinh-steam-voi-cong-nghe-sang-tao/",
            "images": [],
        },
        {
            "slug": "tong-quan-chuong-trinh-tieng-trung-2",
            "title": "TỔNG QUAN CHƯƠNG TRÌNH TIẾNG TRUNG",
            "source_url": "https://misvn.edu.vn/tong-quan-chuong-trinh-tieng-trung-2/",
            "images": [],
        },
        {
            "slug": "chuong-trinh-ky-nang-song-nam-hoc-2026-2027",
            "title": "CHƯƠNG TRÌNH KỸ NĂNG SỐNG NĂM HỌC 2026-2027",
            "source_url": "https://misvn.edu.vn/chuong-trinh-ky-nang-song-nam-hoc-2026-2027/",
            "images": [],
        },
    ]

    for index, payload in enumerate(pages):
        page, _ = ProgramOverviewPage.objects.get_or_create(
            slug=payload["slug"],
            defaults={
                "title": payload["title"],
                "subtitle": "",
                "description": "",
                "source_url": payload["source_url"],
                "hero_image_url": "",
                "order": index,
                "is_active": True,
            },
        )

        page.title = payload["title"]
        page.subtitle = ""
        page.description = ""
        page.source_url = payload["source_url"]
        page.order = index
        page.is_active = True
        if payload["images"]:
            page.hero_image_url = payload["images"][0]
        elif "2022" in (page.hero_image_url or "") or "2023" in (page.hero_image_url or ""):
            # Clear legacy remote URLs so 2022-2023 assets are not carried into 2026-2027 seed data.
            page.hero_image_url = ""
        page.save()

        # Never recreate old batch URLs when there is no 2026-2027 source image list.
        if not payload["images"]:
            ProgramOverviewImage.objects.filter(page=page, image_url__contains="2022").delete()
            ProgramOverviewImage.objects.filter(page=page, image_url__contains="2023").delete()

        # Do not overwrite imported images for newer school-year batches.
        if payload["images"] and not ProgramOverviewImage.objects.filter(page=page).exists():
            ProgramOverviewImage.objects.bulk_create(
                [
                    ProgramOverviewImage(
                        page=page,
                        image_url=image_url,
                        alt_text=f"{page.title} - {order + 1}",
                        order=order,
                    )
                    for order, image_url in enumerate(payload["images"])
                ]
            )


def unseed_program_overview_pages(apps, schema_editor):
    ProgramOverviewPage = apps.get_model("core", "ProgramOverviewPage")
    slugs = [
        "chuong-trinh-tong-quan-mon-toan",
        "tong-quan-chuong-trinh-ngu-van-tai-mis",
        "tong-quan-chuong-trinh-tieng-anh",
        "chuong-trinh-tong-quan-trai-nghiem-sang-tao-tnst",
        "chuong-trinh-steam-voi-cong-nghe-sang-tao",
        "tong-quan-chuong-trinh-tieng-trung-2",
        "chuong-trinh-ky-nang-song-nam-hoc-2026-2027",
        "chuong-trinh-ky-nang-song-nam-hoc-2022-2023",
    ]
    ProgramOverviewPage.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0021_program_overview_pages"),
    ]

    operations = [
        migrations.RunPython(seed_program_overview_pages, unseed_program_overview_pages),
    ]
