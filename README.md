# Website Trường MIS – Đa Trí Tuệ

Hệ thống website trường học xây dựng bằng Django, tập trung vào quản trị nội dung,
giới thiệu chương trình đào tạo, tuyển sinh và truyền thông. Hệ thống hỗ trợ đa
ngôn ngữ (VI/EN), quản lý media, và cung cấp các module nội dung chuyên biệt
cho nhu cầu của trường.

## Tổng quan chức năng
- Trang chủ: hero slider, giá trị cốt lõi, thống kê, chương trình đào tạo, thành tích,
  chia sẻ phụ huynh, đối tác, podcast, gương mặt học sinh, cơ sở vật chất.
- Tuyển sinh: thông tin theo cấp học, điểm nổi bật, form đăng ký và quản lý hồ sơ.
- Tin tức & Sự kiện: bài viết, danh mục, bài nổi bật, lịch sự kiện.
- Thư viện ảnh: album, ảnh theo sự kiện/chủ đề.
- Giới thiệu/Academics: nội dung dạng section, hỗ trợ tài liệu PDF.
- Liên hệ: form liên hệ, đăng ký tư vấn, lead từ chatbot.
- CSR & Hoạt động ngoại khóa: dự án CSR, hoạt động ngoại khóa.
- Đội ngũ: danh sách nhân sự/giáo viên.
- Portal nội bộ: CRUD cho tin tức, sự kiện, tuyển sinh và hồ sơ đăng ký.

## Công nghệ & hạ tầng
- Python 3.10+
- Django 5.2 (Template-based)
- Django REST Framework, django-cors-headers
- SQLite (development) / PostgreSQL (production)
- Pillow (xử lý ảnh), WhiteNoise (static), Gunicorn (production)

## Đa ngôn ngữ
- Hỗ trợ EN/VI với `LocaleMiddleware` và `i18n_patterns`.
- URL mặc định không có prefix ngôn ngữ (`prefix_default_language=False`).

## Cấu trúc thư mục chính
```
WebsiteSchool/
├── school_website/        # Django settings/urls/wsgi
├── core/                  # Trang chủ, menu, chương trình đào tạo, nội dung nền
├── admissions/            # Tuyển sinh & đăng ký
├── news/                  # Tin tức
├── events/                # Sự kiện
├── gallery/               # Thư viện ảnh
├── about/                 # Giới thiệu, Academics, PDF
├── contact/               # Liên hệ, tư vấn, lead
├── staff/                 # Đội ngũ
├── csr/                   # Trách nhiệm xã hội
├── activities/            # Hoạt động ngoại khóa
├── portal/                # Portal quản trị nội dung
├── templates/             # HTML templates
├── static/                # CSS/JS/Images
├── media/                 # Uploads
└── scripts/               # Script seeding/cập nhật dữ liệu
```

## Cài đặt nhanh (Development)
```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Dữ liệu mẫu
```bash
python manage.py create_admission_data
```

## Cấu hình môi trường
Tham khảo `.env.example` cho các biến cấu hình phổ biến (SECRET_KEY, DATABASE_URL,
EMAIL_*, STATIC_*, MEDIA_*). Dự án hiện đọc cấu hình trực tiếp trong
`school_website/settings.py`, nên khi triển khai production cần đồng bộ lại việc
đọc biến môi trường hoặc cập nhật settings theo hạ tầng.

## Quản trị
- Admin: `http://localhost:8000/admin/`
- Portal nội bộ: `http://localhost:8000/portal/`

## Tài liệu liên quan
- `SETUP.md` – Hướng dẫn triển khai chi tiết
- `CRAWL_GUIDE.md`, `DATA_UPDATE_SUMMARY.md` – Tài liệu dữ liệu/crawl (nếu dùng)
