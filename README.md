# Website Trường MIS - Đa Trí Tuệ

Website trường học hiện đại được xây dựng với Django 5.2 và Tailwind CSS.

## 🚀 Tính năng

- **Trang chủ**: Hero slider, Giá trị cốt lõi, Giới thiệu, Video, Thống kê, Chương trình học, Tin tức, Sự kiện, Thư viện ảnh
- **Tuyển sinh**: Thông tin tuyển sinh theo cấp học, Form đăng ký trực tuyến
- **Tin tức**: Danh sách tin tức, chi tiết bài viết
- **Sự kiện**: Lịch sự kiện, chi tiết sự kiện
- **Thư viện ảnh**: Album ảnh, hiển thị gallery
- **Liên hệ**: Form liên hệ, thông tin trường

## 📋 Yêu cầu hệ thống

- Python 3.10+
- Django 5.2+
- SQLite (development) / PostgreSQL (production)

## 🛠️ Cài đặt Development

```bash
# Clone repository
git clone <repository-url>
cd WebsiteSchool

# Tạo virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy migrations
python manage.py migrate

# Tạo dữ liệu mẫu tuyển sinh
python manage.py create_admission_data

# Tạo superuser
python manage.py createsuperuser

# Chạy development server
python manage.py runserver
```

## 🚢 Triển khai Production (Linux)

### 1. Clone và cài đặt

```bash
# Clone repository
git clone <repository-url> /var/www/mis-website
cd /var/www/mis-website

# Tạo virtual environment
python3 -m venv venv
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

### 2. Cấu hình environment

```bash
# Tạo file .env
cp .env.example .env

# Chỉnh sửa cấu hình
nano .env
```

### 3. Cấu hình Database (PostgreSQL)

```sql
CREATE DATABASE mis_website;
CREATE USER mis_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE mis_website TO mis_user;
```

### 4. Chạy migrations

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 5. Cấu hình Gunicorn

```bash
# Chạy với Gunicorn
gunicorn school_website.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

### 6. Cấu hình Nginx

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /static/ {
        alias /var/www/mis-website/staticfiles/;
    }

    location /media/ {
        alias /var/www/mis-website/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📁 Cấu trúc dự án

```
WebsiteSchool/
├── school_website/     # Django settings
├── core/               # Trang chủ, Core Values, Statistics
├── admissions/         # Tuyển sinh
├── news/               # Tin tức
├── events/             # Sự kiện
├── gallery/            # Thư viện ảnh
├── about/              # Giới thiệu
├── contact/            # Liên hệ
├── templates/          # HTML templates
├── static/             # CSS, JS, Images
└── media/              # User uploads
```

## 🔑 Admin Panel

Truy cập: `http://localhost:8000/admin/`

## 📝 License

© 2024 MIS Đa Trí Tuệ. All rights reserved.
