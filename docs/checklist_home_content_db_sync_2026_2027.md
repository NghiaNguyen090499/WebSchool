# Checklist Sync Nội Dung Trang Chủ MIS (2026-2027)

## Mục tiêu
- Đồng bộ nội dung trang chủ với brochure MIS 53 trang.
- Đưa dữ liệu vào DB để có thể quản trị qua admin, giảm hardcode.

## Checklist triển khai
- [x] Chuẩn hoá `Achievement` theo số liệu brochure:
  - [x] Stats: `50%`, `15`, `98%`.
  - [x] Cards: STEAMCUP/ASMO và các chỉ dấu hội nhập.
- [x] Chuẩn hoá `Pillar` về đúng 6 trụ cột cốt lõi.
- [x] Chuẩn hoá `FounderMessage` theo ngữ liệu brochure.
- [x] Tạo `ParentTestimonial` trong DB (3 mục) + gắn ảnh từ `static/images/testimonials/`.
- [x] Refactor section Testimonials trong `templates/core/home.html` để đọc từ DB (`testimonials`) với fallback.
- [x] Bổ sung script đồng bộ để chạy lại: `scripts/sync_home_content_db.py`.

## Cách chạy lại đồng bộ
```bash
# PowerShell (Windows)
python manage.py shell -c "exec(open('scripts/sync_home_content_db.py', encoding='utf-8').read())"

# Bash / Zsh
python manage.py shell < scripts/sync_home_content_db.py
```

## Ghi chú
- Phần Testimonials hiện là nội dung marketing nội bộ; chưa thấy xuất hiện trong brochure 53 trang, cần xác nhận SoT nếu muốn audit tuyệt đối theo brochure.
- Các block đang nằm trong `{% comment %}` sẽ không render ra frontend dù đã có dữ liệu DB.
