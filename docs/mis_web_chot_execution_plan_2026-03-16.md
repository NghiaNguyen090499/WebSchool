# Plan sửa cụ thể theo file/model

## Mục tiêu đợt 1

Ưu tiên xử lý những gì MIS nhìn thấy ngay trên website public:

1. sửa text bị vỡ dấu;
2. sửa label/menu chương trình học;
3. loại bỏ placeholder public;
4. chuẩn bị sẵn danh sách file/model cho các đợt sửa dữ liệu tiếp theo.

## Phase 1. Public UI P0

### 1.1. Template public bị mojibake

| File | Vấn đề | Việc cần làm | Trạng thái |
| --- | --- | --- | --- |
| [templates/core/student_spotlight_list.html](/d:/NGHIA/WebsiteSchool/templates/core/student_spotlight_list.html) | Meta/title/button/pagination vỡ dấu | Chuẩn hóa toàn bộ text literal về UTF-8 đúng | Đang làm |
| [templates/core/training_programs.html](/d:/NGHIA/WebsiteSchool/templates/core/training_programs.html) | Hero/meta/CTA vỡ dấu | Chuẩn hóa text literal, bỏ wording dễ lệch như số lượng hệ | Đang làm |
| [templates/contact/contact.html](/d:/NGHIA/WebsiteSchool/templates/contact/contact.html) | Toàn bộ heading/label/form/map vỡ dấu | Chuẩn hóa text literal về UTF-8 đúng | Đang làm |
| [templates/about/whymis.html](/d:/NGHIA/WebsiteSchool/templates/about/whymis.html) | Meta/default labels/CTA/fallback copy vỡ dấu | Chuẩn hóa text literal và fallback copy | Đang làm |
| [templates/core/home.html](/d:/NGHIA/WebsiteSchool/templates/core/home.html) | Block GRACE/CSR và tab news còn sót text lỗi | Sửa các literal public còn lỗi | Đang làm |
| [templates/core/includes/navbar.html](/d:/NGHIA/WebsiteSchool/templates/core/includes/navbar.html) | Một phần submenu bị vỡ dấu | Chuẩn hóa text ở cả desktop/mobile menu | Đang làm |

### 1.2. Menu chương trình học

| File | Vấn đề | Việc cần làm | Trạng thái |
| --- | --- | --- | --- |
| [templates/core/includes/navbar.html](/d:/NGHIA/WebsiteSchool/templates/core/includes/navbar.html) | `Toán`, `steeam`, `Nội dung tôi sẽ thêm sau` | Đổi thành nhãn MIS chốt, bỏ placeholder public | Đang làm |

## Phase 2. Dữ liệu chương trình học

| File / Model | Vấn đề | Việc cần làm | Trạng thái |
| --- | --- | --- | --- |
| [core/models.py](/d:/NGHIA/WebsiteSchool/core/models.py) `TrainingProgram` | Hiện logic và wording còn bám bộ 3 hệ/4 record | Rà lại tên hệ, group, choice label và copy hiển thị | Chưa làm |
| [core/views.py](/d:/NGHIA/WebsiteSchool/core/views.py) `training_programs_list` | Trang listing lấy toàn bộ record active theo `order` | Sau khi chuẩn hóa DB, kiểm tra lại thứ tự hiển thị 5 hệ | Chưa làm |
| DB `TrainingProgram` | Thiếu đủ 5 hệ MIS chốt | Tạo/điều chỉnh record: STEAM, Chất lượng cao Công nghệ, Tiếng Anh tài năng, Tiếng Trung tài năng, Toán tài năng | Chưa làm |

## Phase 3. Dữ liệu campus / contact

| File / Model | Vấn đề | Việc cần làm | Trạng thái |
| --- | --- | --- | --- |
| [core/models.py](/d:/NGHIA/WebsiteSchool/core/models.py) `Campus` | Dữ liệu đang trùng logic và chưa thống nhất tên | Chuẩn hóa record campus theo tên MIS chốt | Chưa làm |
| [contact/views.py](/d:/NGHIA/WebsiteSchool/contact/views.py) | View lấy campus active hiện có | Sau khi dọn DB, kiểm tra campus chính/map/cách sắp xếp | Chưa làm |
| DB `Campus` | `Campus chính`, `Cơ sở Cầu Giấy`, `MIS Pandora Landscape` đang lẫn | Gộp/chỉnh tên/địa chỉ và cờ `is_primary` | Chưa làm |

## Phase 4. About / History / Founder message

| File / Model | Vấn đề | Việc cần làm | Trạng thái |
| --- | --- | --- | --- |
| [about/models.py](/d:/NGHIA/WebsiteSchool/about/models.py) `AboutPage`, `AboutSection` | `principal` đúng choice nhưng DB title còn lệch | Chuẩn hóa nội dung page `principal` thành lịch sử hình thành | Chưa làm |
| [about/views.py](/d:/NGHIA/WebsiteSchool/about/views.py) | `principal` render đúng template nhưng phụ thuộc content DB | Kiểm tra lại data source `principal_history` và fallback | Chưa làm |
| [templates/about/principal.html](/d:/NGHIA/WebsiteSchool/templates/about/principal.html) | Cần QA sau khi đổi data | Kiểm tra title/subtitle/CTA theo tài liệu MIS | Chưa làm |
| [core/models.py](/d:/NGHIA/WebsiteSchool/core/models.py) `FounderMessage` | Cần thay copy MIS mới | Cập nhật bản ghi active theo nội dung slide 8 | Chưa làm |

## Phase 5. Why MIS / Đối tác / GRACE

| File / Model | Vấn đề | Việc cần làm | Trạng thái |
| --- | --- | --- | --- |
| [templates/about/whymis.html](/d:/NGHIA/WebsiteSchool/templates/about/whymis.html) | Đã có layout nhưng text lỗi và asset cũ | Sửa text trước, sau đó thay bài/ảnh MIS mới | Đang làm |
| [about/models.py](/d:/NGHIA/WebsiteSchool/about/models.py) `AboutSection` | Data section đã có nhưng cần refresh nội dung | Cập nhật section `features`, `text_left`, `stats` theo docs MIS | Chưa làm |
| DB `AboutSection` page `whymis` | Nội dung cũ và ảnh chưa final | Nhập bài viết/ảnh chuẩn MIS | Chưa làm |

## Phase 6. CSR

| File / Model | Vấn đề | Việc cần làm | Trạng thái |
| --- | --- | --- | --- |
| [csr/models.py](/d:/NGHIA/WebsiteSchool/csr/models.py) `CSRProject`, `CSRImage` | Chưa đủ cấu trúc cho proof links/timeline dài | Thiết kế thêm model link minh chứng nếu triển khai data-driven | Chưa làm |
| [csr/views.py](/d:/NGHIA/WebsiteSchool/csr/views.py) | Đang mix DB với template hardcode | Sau khi có data chuẩn, chuyển dần sang render từ DB | Chưa làm |
| [csr/templates/csr/list.html](/d:/NGHIA/WebsiteSchool/csr/templates/csr/list.html) | Hardcode nhiều link và campaign | Giảm hardcode, map campaign theo record thật | Chưa làm |
| [templates/core/home.html](/d:/NGHIA/WebsiteSchool/templates/core/home.html) | CSR teaser còn tĩnh | Sau đợt P0, chuyển block này sang data-driven | Chưa làm |

## Thứ tự triển khai khuyến nghị

1. Fix template public và navbar.
2. QA nhanh lại render public.
3. Chuẩn hóa DB `TrainingProgram` và `Campus`.
4. Chuẩn hóa `principal`, `FounderMessage`, `whymis`.
5. Làm sạch CSR theo hướng data-driven.

