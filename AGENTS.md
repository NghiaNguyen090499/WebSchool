# Agent Instructions for WebsiteSchool

## 1) Mục tiêu kiểm tra

Xác nhận hệ thống build/run ổn định trên môi trường giống production (Postgres, Gunicorn, static/media thật).

Bắt lỗi bảo mật cấu hình Django trước khi deploy.

Kiểm tra đúng nghiệp vụ theo module (tuyển sinh, tin tức/sự kiện, gallery, contact, portal).

Xác nhận độ ổn định/hiệu năng (truy vấn DB, cache, tải trang, upload).

Chuẩn hoá đồng bộ cấu hình: env vars, migrations, static/media, i18n.

## 2) “Bộ lệnh” kiểm tra nhanh (chạy ngay trên repo)

Mục tiêu: trong 10–20 phút có kết quả ban đầu “GO/NO-GO” về kỹ thuật.

### 2.1. Kiểm tra Django + cấu hình deploy

```
python manage.py check
python manage.py check --deploy
```

`check --deploy` rất quan trọng để bắt các cấu hình hay sai ở production (DEBUG, SECRET_KEY, ALLOWED_HOSTS, HTTPS, cookies…).

### 2.2. Kiểm tra migrations và đồng bộ schema

```
python manage.py makemigrations --check --dry-run
python manage.py showmigrations --plan
```

Nếu `makemigrations --check` báo còn thay đổi chưa commit → blocker (deploy dễ lệch schema).

### 2.3. Kiểm tra static & i18n

```
python manage.py collectstatic --noinput
django-admin compilemessages
```

`collectstatic` giúp phát hiện lỗi static path, WhiteNoise config, thiếu file.

`compilemessages` giúp phát hiện lỗi file dịch.

### 2.4. Chạy test (nếu đã có)

```
pytest -q
# hoặc
python manage.py test
```

## 3) Giải pháp kiểm tra đầy đủ theo 3 tầng (khuyến nghị triển khai)

### Tầng A — “Code Quality & Security Gate” (tự động trong CI)

Mục tiêu: PR nào cũng bị chặn nếu vi phạm chuẩn hoặc có lỗ hổng hiển nhiên.

**A1) Lint/Format/Type (chất lượng code)**

ruff (lint), black (format), isort (import), mypy (type – tuỳ mức áp dụng)

**A2) Security/Supply chain**

bandit (quét lỗi bảo mật Python)

pip-audit (lỗ hổng dependencies)

kiểm tra secrets: detect-secrets hoặc gitleaks

**A3) Django deploy checks**

bắt buộc chạy: `python manage.py check --deploy`

chạy `makemigrations --check --dry-run` để chặn lệch migrations

Output mong muốn: CI trả về report rõ ràng, fail nhanh nếu có Critical/High.

### Tầng B — “Staging giống Production” (bắt các lỗi chỉ lộ khi deploy)

Mục tiêu: staging phải “giống prod” để test đúng.

**B1) Dùng Postgres trên staging (không dùng SQLite)**

Vì README nêu prod là Postgres → mọi test tích hợp nên chạy trên Postgres.

**B2) Deploy đúng kiểu production**

Gunicorn + (Nginx hoặc reverse proxy)

WhiteNoise static (hoặc Nginx/CDN serve static)

Media uploads: thư mục mount volume / object storage

**B3) Checklist staging phải chạy**

migrate

collectstatic

compilemessages

smoke test endpoints (xem mục 6)

### Tầng C — “Production Readiness” (quan sát & vận hành)

Mục tiêu: deploy xong là biết ngay có ổn hay không, và có đường rollback.

Logging: log structured / log level

Error monitoring: Sentry (khuyến nghị)

Health checks: `/healthz` & `/readyz`

Backup/restore Postgres + media

Rollback plan: code rollback + migration strategy (ít nhất: migration backwards hoặc forward-fix)

## 4) Ma trận test theo module (bám đúng mô tả README)

Dựa trên các module bạn mô tả README, đây là bộ test case nên có (ưu tiên theo rủi ro):

### 4.1. Public site (Template pages)

- Trang chủ: render đủ block (slider/section), không lỗi query, ảnh hiển thị ok
- Tin tức: list + detail + category + featured; pagination
- Sự kiện: list + detail + calendar view (nếu có)
- Gallery: album list + album detail; ảnh tải đúng; lazyload (nếu có)
- About/Academics + PDF: download PDF đúng quyền truy cập, correct content-type
- Staff: danh sách hiển thị đúng, SEO-friendly
- CSR/Activities: list/detail đúng ngôn ngữ

### 4.2. Form flows (nguy cơ cao)

- Admissions form: validation, required fields, anti-spam, lưu DB, email notify (nếu có)
- Contact / tư vấn / lead chatbot: validation, rate limit, lưu lead

2 form này nên có integration test + manual test vì liên quan dữ liệu thật.

### 4.3. Portal nội bộ (nguy cơ bảo mật cao)

- Auth bắt buộc (không lộ CRUD)
- Role/permission: ai được sửa gì
- Upload media trong portal: kiểm tra loại file, kích thước, path traversal
- Audit log (khuyến nghị): ai sửa nội dung, lúc nào

## 5) Kiểm tra đồng bộ hệ thống (những chỗ hay lệch khi deploy)

README có nhắc `.env.example` nhưng hiện “đọc cấu hình trực tiếp trong settings.py” và cần đồng bộ lại khi lên production. Đây là nhóm kiểm tra cực quan trọng:

### 5.1. Đồng bộ cấu hình môi trường

- `.env.example` khớp với các biến thật sự đang dùng trong `settings.py`
- Không hardcode: `SECRET_KEY`, DB credentials, email password, API keys
- `DEBUG=False` production
- `ALLOWED_HOSTS` đúng domain
- CORS: chỉ whitelist domain cần thiết (đang dùng django-cors-headers)

### 5.2. Đồng bộ DB

- Migrations luôn chạy trước khi serve traffic
- Không có “migrations pending”
- Kiểm tra dữ liệu seed/script trong `scripts/` có an toàn khi chạy lại (idempotent)

### 5.3. Đồng bộ static/media

- `collectstatic` chạy và WhiteNoise serve đúng
- Media upload: URL + storage path đúng (production thường tách ra khỏi static)
- Permissions thư mục upload đúng, không public list directory

### 5.4. Đồng bộ i18n (VI/EN)

- URL default không prefix language (`prefix_default_language=False`)
- Test routing: `/` và `/en/` hoạt động đúng, canonical/SEO không bị duplicate content
- Kiểm tra fallback khi thiếu bản dịch

## 6) Smoke test sau deploy (script gợi ý)

Bạn nên có một “smoke suite” chạy bằng curl hoặc pytest sau mỗi deploy.

### 6.1. Danh sách endpoint tối thiểu

- `/` (home)
- `/en/` (home EN)
- Trang list tin tức + 1 trang detail mẫu
- Trang list sự kiện + 1 detail mẫu
- Gallery list + 1 album detail
- Admissions form GET + POST (POST dùng dữ liệu giả)
- Contact form GET + POST
- `/portal/` phải redirect login hoặc 403 nếu chưa login
- `/admin/` tương tự

### 6.2. Điều kiện pass/fail

- HTTP 200 cho trang public
- Form POST: trả status hợp lý + record được tạo trong DB
- Không có 500/traceback
- Thời gian phản hồi P95 (tuỳ mục tiêu) nhưng ít nhất không “đơ” khi tải

## 7) Kiểm tra hiệu năng & ổn định (đủ cho website trường)

### 7.1. Kiểm tra query N+1

Dùng django-debug-toolbar trên dev.

Trên staging có thể dùng django-silk (nếu chấp nhận).

Mục tiêu: các trang list (news/events/gallery) không bị query tăng tuyến tính theo số item.

### 7.2. Load test “vừa đủ”

Dùng Locust hoặc k6:

- 50–100 users đồng thời truy cập home/news/gallery
- 5–10% request là submit admissions/contact

Quan sát: CPU, RAM, DB connections, latency.

## 8) Bộ “tiêu chí GO/NO-GO” trước khi triển khai production

**NO-GO nếu có bất kỳ điểm nào sau:**

- `manage.py check --deploy` báo lỗi nghiêm trọng chưa xử lý
- Pending migrations hoặc mismatch schema
- Portal CRUD truy cập được khi chưa auth / sai permission
- Form admissions/contact không có validation/rate limit tối thiểu
- Secrets hardcode hoặc lộ trong repo/logs

**GO WITH RISKS nếu:**

- Thiếu test tự động nhưng staging smoke test pass và có monitoring cơ bản

**GO nếu:**

- CI gate pass + staging pass + có smoke test + có backup/rollback plan
