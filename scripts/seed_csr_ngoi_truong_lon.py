"""
Seed script: Thêm dự án CSR "HÀNH ĐỘNG NHỎ - NGÔI TRƯỜNG LỚN" vào CSDL.
Dự án này sẽ hiển thị nổi bật ở vị trí đầu tiên (order=0).
"""
import os
import sys
import glob

import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_website.settings")
django.setup()

from csr.models import CSRImage, CSRProject

# ──────────────────────────────────────────────
# 1) Tạo hoặc cập nhật dự án CSR
# ──────────────────────────────────────────────
TITLE = "HÀNH ĐỘNG NHỎ - NGÔI TRƯỜNG LỚN"
SLUG = "hanh-dong-nho-ngoi-truong-lon"

DESCRIPTION = """\
🏫 KHÁNH THÀNH "NGÔI TRƯỜNG LỚN"

Giữa núi rừng, một mái ấm nở hoa — Ngôi trường lớn của tình yêu chan hoà.

Điểm trường Háng Phừ Loa, Mù Cang Chải — nơi từng chỉ có bốn bức tường đất cũ kỹ, nay đã khoác lên mình một diện mạo hoàn toàn mới. Mái đỏ rực rỡ, tường màu sắc tươi tắn, sân trường rộn ràng tiếng cười trẻ thơ.

Hành trình kéo dài trong 1 năm với sự đồng hành của trường Đa Trí Tuệ MIS và Quỹ MCF, dự án "Hành Động Nhỏ - Ngôi Trường Lớn" đã biến ước mơ về một ngôi trường khang trang thành hiện thực cho các em nhỏ vùng cao.

Mỗi viên gạch được đặt xuống không chỉ xây nên một ngôi trường, mà còn xây nên hy vọng, niềm tin và tương lai cho hàng trăm em nhỏ nơi đây. Sự e dè đã được thay thế bằng nụ cười rạng rỡ, bằng ánh mắt háo hức mỗi ngày đến trường.

Trường MIS tin rằng: Giáo dục không chỉ dừng lại trong lớp học — mà còn lan toả đến mọi nơi cần đến.\
"""

IMPACT_METRICS = """\
01 ngôi trường mới khang trang tại Háng Phừ Loa, Mù Cang Chải
Hành trình 1 năm đồng hành xây dựng
Hàng trăm em nhỏ vùng cao có nơi học tập ấm áp, an toàn
Phối hợp cùng Quỹ MCF (MIS Community Fund)
79 bức ảnh ghi lại khoảnh khắc khánh thành đáng nhớ\
"""

project, created = CSRProject.objects.update_or_create(
    slug=SLUG,
    defaults={
        "title": TITLE,
        "description": DESCRIPTION,
        "impact_metrics": IMPACT_METRICS,
        "is_active": True,
        "order": 0,  # Hiển thị trên cùng
    },
)

action = "Created" if created else "Updated"
print(f"{action} CSRProject: {project.title} (id={project.id}, order={project.order})")

# ──────────────────────────────────────────────
# 2) Thêm ảnh từ thư mục đã tải
# ──────────────────────────────────────────────
IMAGE_DIR = os.path.join("media", "csr", "ngoi-truong-lon")
image_files = sorted(glob.glob(os.path.join(IMAGE_DIR, "*.jpg")))

if not image_files:
    print(f"WARNING: No images found in {IMAGE_DIR}")
else:
    # Xoá ảnh cũ của project (nếu re-run)
    old_count = CSRImage.objects.filter(project=project).count()
    if old_count:
        CSRImage.objects.filter(project=project).delete()
        print(f"  Deleted {old_count} old images")

    for idx, filepath in enumerate(image_files):
        # Đường dẫn relative từ MEDIA_ROOT
        relative_path = os.path.relpath(filepath, "media").replace("\\", "/")
        basename = os.path.splitext(os.path.basename(filepath))[0]

        CSRImage.objects.create(
            project=project,
            image=relative_path,
            caption=f"Ngôi Trường Lớn - {basename}",
            order=idx,
            is_active=True,
        )

    print(f"  Added {len(image_files)} images")

# ──────────────────────────────────────────────
# 3) Kiểm tra kết quả
# ──────────────────────────────────────────────
print("\n--- Current CSR Projects ---")
for p in CSRProject.objects.all():
    img_count = CSRImage.objects.filter(project=p).count()
    print(f"  order={p.order} | {p.title} | {img_count} images | active={p.is_active}")

print("\nDone!")
