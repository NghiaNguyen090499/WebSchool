# Hướng dẫn Crawl và Đồng bộ dữ liệu từ misvn.edu.vn

## Tổng quan

Script này sẽ crawl dữ liệu từ website [misvn.edu.vn](https://misvn.edu.vn/) và đồng bộ vào database Django của bạn.

## Cài đặt Dependencies

Trước tiên, cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

Các thư viện cần thiết:
- `requests` - Để fetch HTML từ website
- `beautifulsoup4` - Để parse HTML
- `lxml` - Parser cho BeautifulSoup

## Cách sử dụng

### 1. Crawl tất cả dữ liệu

```bash
python manage.py crawl_mis --all
```

Lệnh này sẽ crawl:
- ✅ Tin tức (News)
- ✅ Sự kiện (Events)  
- ✅ Trang giới thiệu (About pages)

### 2. Crawl từng loại riêng lẻ

**Chỉ crawl tin tức:**
```bash
python manage.py crawl_mis --news
```

**Chỉ crawl sự kiện:**
```bash
python manage.py crawl_mis --events
```

**Chỉ crawl trang giới thiệu:**
```bash
python manage.py crawl_mis --about
```

## Dữ liệu được crawl

### 1. Tin tức (News)
- **Nguồn**: `/tin-tuc/`
- **Dữ liệu crawl**:
  - Tiêu đề
  - Nội dung
  - Hình ảnh thumbnail
  - Ngày đăng
  - Danh mục (Thông báo, Tin tức, Văn bản...)
- **Lưu vào**: Model `News` trong app `news`

### 2. Sự kiện (Events)
- **Nguồn**: `/tin-tuc/tin-tuc-su-kien/`
- **Dữ liệu crawl**:
  - Tiêu đề
  - Ngày diễn ra
  - Địa điểm
  - Mô tả
  - Hình ảnh
- **Lưu vào**: Model `Event` trong app `events`

### 3. Trang giới thiệu (About)
- **Nguồn**: `/gioi-thieu/`
- **Các trang được crawl**:
  - **Mission**: Giới thiệu chung về MIS
  - **Vision**: Hệ thống giáo dục MIS – Đổi mới để đột phá
  - **Principal's Message**: Thông điệp của Tổng Giám đốc điều hành MIS
- **Lưu vào**: Model `AboutPage` trong app `about`

## Tính năng

### ✅ Tự động xử lý
- Tự động tạo slug từ tiêu đề
- Tải và lưu hình ảnh vào media folder
- Parse ngày tháng từ tiếng Việt
- Tránh trùng lặp (kiểm tra slug trước khi tạo)

### ✅ Xử lý lỗi
- Retry khi fetch page thất bại
- Bỏ qua item lỗi, tiếp tục crawl các item khác
- Log chi tiết quá trình crawl

### ✅ Tôn trọng server
- Delay 1 giây giữa các request
- User-Agent hợp lệ
- Timeout 30 giây

## Ví dụ Output

```
Starting news crawl...
✓ Crawled: Thông báo tuyển sinh năm học 2025-2026...
✓ Crawled: Lễ khai giảng năm học mới...
✓ Crawled: Hội thảo giáo dục đa trí tuệ...
Successfully crawled 25 news articles

Starting events crawl...
✓ Crawled event: Ngày hội thể thao học sinh...
✓ Crawled event: Cuộc thi khoa học kỹ thuật...
Successfully crawled 12 events

Starting about pages crawl...
✓ Crawled mission: Giới thiệu chung về MIS...
✓ Crawled vision: Hệ thống giáo dục MIS...
✓ Crawled principal: Thông điệp của Tổng Giám đốc...
Successfully crawled about pages
```

## Lưu ý

### 1. Cấu trúc website có thể thay đổi
Nếu website misvn.edu.vn thay đổi cấu trúc HTML, bạn cần cập nhật các selector trong file `crawl_mis.py`:
- `news_items = soup.find_all(...)` - Selector cho danh sách tin tức
- `content_elem = soup.find(...)` - Selector cho nội dung bài viết
- `date_elem = soup.find(...)` - Selector cho ngày tháng

### 2. Hình ảnh
- Hình ảnh được tải về và lưu vào `media/news/thumbnails/` và `media/events/`
- Nếu không tải được hình ảnh, bài viết vẫn được tạo (không có thumbnail)

### 3. Ngày tháng
- Script cố gắng parse ngày tháng từ nhiều format khác nhau
- Nếu không parse được, sẽ dùng ngày hiện tại

### 4. Chạy lại
- Script tự động bỏ qua các bài viết đã tồn tại (dựa trên slug)
- Có thể chạy lại nhiều lần mà không lo trùng lặp

## Tùy chỉnh

### Thay đổi số lượng crawl
Trong file `crawl_mis.py`, tìm và sửa:
```python
for item in news_items[:50]:  # Thay đổi 50 thành số bạn muốn
```

### Thay đổi delay
```python
time.sleep(1)  # Thay đổi 1 thành số giây bạn muốn
```

### Thêm category mới
Trong hàm `crawl_news()`, thêm vào `categories_map`:
```python
categories_map = {
    'Tên category': 'slug-category',
    # ...
}
```

## Troubleshooting

### Lỗi: "Could not fetch page"
- Kiểm tra kết nối internet
- Kiểm tra website có đang hoạt động không
- Thử tăng số lần retry

### Lỗi: "No news items found"
- Website có thể đã thay đổi cấu trúc HTML
- Cần cập nhật selector trong code

### Lỗi: "Image download failed"
- Không ảnh hưởng đến việc tạo bài viết
- Bài viết sẽ được tạo nhưng không có thumbnail

## Kiểm tra kết quả

Sau khi crawl xong, kiểm tra trong Django Admin:
1. Truy cập: http://127.0.0.1:8000/admin/
2. Xem:
   - **News → News**: Danh sách tin tức đã crawl
   - **Events → Events**: Danh sách sự kiện đã crawl
   - **About → About Pages**: Các trang giới thiệu đã crawl

## Lịch chạy tự động (Optional)

Để crawl tự động hàng ngày, có thể setup cron job:

**Linux/Mac:**
```bash
# Chạy mỗi ngày lúc 2 giờ sáng
0 2 * * * cd /path/to/project && python manage.py crawl_mis --all
```

**Windows (Task Scheduler):**
Tạo task chạy lệnh:
```
python manage.py crawl_mis --all
```

## Hỗ trợ

Nếu gặp vấn đề, kiểm tra:
1. Log output trong terminal
2. Django admin để xem dữ liệu đã crawl
3. Media folder để xem hình ảnh đã tải







