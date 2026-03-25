from django.core.management.base import BaseCommand

from core.models import Pillar


class Command(BaseCommand):
    help = "Update education pillars content (idempotent)."

    def handle(self, *args, **options):
        pillars_data = [
            {
                "title": "Học Làm Người",
                "short_description": (
                    "Nuôi dưỡng nhân cách – Tình yêu đất nước – Giá trị bản thân qua Giữ gìn Nhân tính - "
                    "Bảo tồn Quốc tính - Khẳng định Cá tính. “Giáo dục con tim” thông qua phát triển Năng lực "
                    "Cảm xúc Xã hội và Giá trị sống theo mô thức GRACE – Hoa Kỳ."
                ),
                "icon": "fas fa-heart",
                "order": 1,
            },
            {
                "title": "Vững Vàng Tri Thức",
                "short_description": (
                    "Giảng dạy chuyên sâu các môn Văn hóa – Công nghệ mới – Ngoại ngữ – Toán tư duy, "
                    "từ nền tảng đến chuyên biệt. Phát triển năng lực xử lý thông tin, sử dụng Công nghệ, "
                    "Trí tuệ nhân tạo (AI), Internet of Things, Big Data…"
                ),
                "icon": "fas fa-book",
                "order": 2,
            },
            {
                "title": "Phát triển Kỹ Năng Thế Kỷ 21",
                "short_description": (
                    "Trang bị năng lực 5Cs: Giao tiếp – Tư duy phản biện – Hợp tác – Giải quyết vấn đề sáng tạo – "
                    "Tư duy máy tính. Thực hiện học tập hợp tác, giáo dục công nghệ mới và các hoạt động trải nghiệm "
                    "sáng tạo, sự kiện, ngoại khoá, giáo dục kết nối với môi trường, xã hội…"
                ),
                "icon": "fas fa-users",
                "order": 3,
            },
            {
                "title": "Chăm Sóc Sức Khỏe Thể Chất và Tinh thần",
                "short_description": (
                    "Lồng ghép EQ, rèn luyện thân thể, nuôi dưỡng cảm xúc lành mạnh, hướng tới học sinh hạnh phúc."
                ),
                "icon": "fas fa-heartbeat",
                "order": 4,
            },
            {
                "title": "Học Gắn Với Hành với Thực Tiễn Cuộc Sống",
                "short_description": (
                    "Kết nối kiến thức và đời sống thông qua trải nghiệm, hoạt động thực hành, "
                    "hướng nghiệp – khởi nghiệp."
                ),
                "icon": "fas fa-hands-helping",
                "order": 5,
            },
            {
                "title": "Tăng cường Năng lực Công Nghệ - AI",
                "short_description": (
                    "Liên tục đào tạo cán bộ, giáo viên để ứng dụng hiệu quả công nghệ và trí tuệ nhân tạo "
                    "trong dạy học, đánh giá và quản lý giáo dục."
                ),
                "icon": "fas fa-robot",
                "order": 6,
            },
            {
                "title": "Xây Dựng Trường Học Thông Minh – Xanh vì cuộc sống bền vững",
                "short_description": (
                    "Đầu tư cơ sở vật chất xanh – công nghệ cao – năng lượng tái tạo vì một tương lai bền vững."
                ),
                "icon": "fas fa-leaf",
                "order": 7,
            },
            {
                "title": "Cộng Đồng Kết Nối - Chia Sẻ",
                "short_description": (
                    "Gắn kết Nhà trường – Phụ huynh – Học sinh tạo nên văn hóa học đường nhân văn và lan tỏa, "
                    "hướng tới mục tiêu: Mỗi thành viên đều thấm nhuần giá trị chung của trường - "
                    "“Đa Trí Tuệ - Một Nhân Cách”."
                ),
                "icon": "fas fa-users",
                "order": 8,
            },
        ]

        created_count = 0
        updated_count = 0

        for data in pillars_data:
            pillar, created = Pillar.objects.update_or_create(
                title=data["title"],
                defaults={
                    "short_description": data["short_description"],
                    "icon": data["icon"],
                    "order": data["order"],
                    "is_active": True,
                },
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\nPillars processed: {created_count} created, {updated_count} updated."
            )
        )
