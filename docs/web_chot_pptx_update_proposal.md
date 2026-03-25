# Đề xuất update từ `WEB chốt.pptx`

## 1. Phạm vi nội dung lấy từ file

PowerPoint này không phải brief redesign toàn site. Nội dung tập trung vào 3 nhóm:

1. `Trang chủ - Trách nhiệm xã hội`
   - Nhiều chiến dịch CSR giai đoạn 2008-2025.
   - Nguồn minh chứng là Facebook post/album/reel, bài trên site MIS, Google Drive.
2. `Chương trình Kỹ năng sống & Giá trị sống`
   - Thêm minh chứng triển khai SEL/GRACE/Kymviet/Seroto.
   - Có link video, bài viết, album hoạt động.
3. `Lịch sử hình thành trường`
   - Có 1 tài liệu Google Docs làm nguồn gốc nội dung.

## 2. Hiện trạng hệ thống

### 2.1. Điểm đã có sẵn

- Trang chủ đã có teaser CSR ở `templates/core/home.html`.
- Module CSR đã có route riêng `/csr/` với model `CSRProject` và `CSRImage`.
- Trang `lifeskills` đã có layout hoàn chỉnh và chất lượng tốt hơn nội dung PPT.
- Route `about:principal` đã tồn tại để hiển thị trang có ý nghĩa "Lịch sử hình thành".

### 2.2. Khoảng cách chính

- CSR trên homepage đang hardcode nội dung và ảnh đơn lẻ, chưa lấy từ dữ liệu quản trị.
- Model CSR hiện chưa đủ để lưu:
  - giai đoạn năm,
  - địa điểm,
  - loại chiến dịch,
  - link minh chứng ngoài site,
  - cờ `featured_on_home`.
- `lifeskills` chưa có block "minh chứng thực tế" để gắn các bài viết/video/album từ PPT.
- `principal` đang lệch nghiệp vụ:
  - code định danh page này là `Lịch sử hình thành`,
  - nhưng dữ liệu DB hiện vẫn là `Thông điệp Tổng Giám đốc`.
- Portal hiện chưa có CRUD cho CSR hoặc evidence links.

## 3. Đề xuất cập nhật theo module

### 3.1. Homepage

Giữ section CSR trên trang chủ nhưng đổi thành block dữ liệu động:

- Tiêu đề ngắn + 2-3 chỉ dấu tác động.
- 3 chiến dịch nổi bật dạng card/timeline.
- CTA sang `/csr/`.
- Ảnh hero lấy từ project được gắn `featured_on_home=True`, không hardcode đường dẫn media.

Nội dung phù hợp nhất để đưa lên home:

- Mái ấm Thánh Tâm.
- Mang yêu thương về vùng lũ.
- Hỗ trợ sửa trường học / Đường Hy Vọng.

### 3.2. Trang CSR `/csr/`

Nên nâng từ "gallery dự án" thành "timeline CSR có minh chứng".

Đề xuất mở rộng model:

- `CSRProject`
  - `summary`
  - `start_year`
  - `end_year`
  - `location`
  - `project_type`
  - `is_featured_home`
  - `is_featured_timeline`
- `CSRProofLink`
  - `project`
  - `label`
  - `url`
  - `source_type` (`facebook_post`, `facebook_album`, `video`, `article`, `drive`)
  - `order`

UI nên thêm:

- Filter theo năm/chủ đề.
- Card "minh chứng" dạng chip/button.
- Timeline các chiến dịch dài hạn 2008-2025.

### 3.3. Trang `lifeskills`

Không cần làm lại layout chính.

Chỉ nên thêm 1 section mới:

- `Minh chứng triển khai SEL`
  - GRACE tại Hawaii.
  - Hoạt động với Kymviet.
  - Chuỗi hoạt động SEL tại trường.
  - Đào tạo Trí tuệ cảm xúc cùng Seroto.

Đề xuất model dùng lại theo hướng generic:

- `EvidenceLink`
  - `page_type`
  - `group`
  - `title`
  - `url`
  - `source_type`
  - `year`
  - `order`

Nếu cần đi nhanh, có thể chưa tạo model mới mà render tạm từ JSON/data file. Nhưng về lâu dài nên có model quản trị.

### 3.4. Trang `principal`

Nên chuẩn hóa page này thành `Lịch sử hình thành trường` đúng nghĩa.

Đề xuất:

- Giữ URL cũ `/about/principal/` để tránh ảnh hưởng SEO và menu.
- Đổi nội dung page:
  - timeline mốc 2008, 2013, các giai đoạn phát triển,
  - câu chuyện hình thành MIS,
  - CTA xem tài liệu chi tiết từ Google Docs hoặc bản nội bộ hóa.
- Không dùng page này cho "Thông điệp Tổng Giám đốc" nữa vì homepage đã có `FounderMessage`.

## 4. Ưu tiên triển khai

### P1 - Nên làm ngay

- Chuẩn hóa `principal` thành trang lịch sử.
- Bổ sung section minh chứng cho `lifeskills`.
- Biến block CSR trên home thành dữ liệu động.

### P2 - Nên làm trong cùng đợt

- Mở rộng model CSR để lưu proof links và timeline.
- Import toàn bộ chiến dịch từ PPT vào DB.

### P3 - Nâng cấp quản trị

- Thêm portal/admin flow để content team tự quản lý:
  - CSR project,
  - proof links,
  - featured home flags.

## 5. Cách triển khai khuyến nghị

### Phương án nhanh, ít migration

- `principal`: cập nhật lại `AboutPage` + `AboutSection`.
- `lifeskills`: thêm section "minh chứng" bằng data tĩnh/JSON.
- `home`: đọc 3 project CSR đầu tiên từ DB thay cho hardcode.

### Phương án chuẩn, quản trị được

- Thêm `CSRProofLink`.
- Thêm generic `EvidenceLink` cho các page chương trình.
- Mở rộng template và admin/portal tương ứng.

## 6. Lưu ý nội dung

- Các link trong PPT hiện mới được trích ra từ file, chưa xác minh trạng thái sống/chết.
- Không nên nhúng nguyên danh sách URL dài vào body HTML.
- Nên chuyển thành:
  - tiêu đề chiến dịch,
  - mô tả ngắn,
  - 3-6 link minh chứng có nhãn rõ ràng.

## 7. Kết luận

Update từ `WEB chốt.pptx` phù hợp với hệ thống hiện tại, vì các module đích đã tồn tại. Phần cần làm là:

- chuẩn hóa nghiệp vụ trang `principal`,
- nâng cấp cấu trúc dữ liệu CSR,
- thêm lớp "minh chứng thực tế" cho `lifeskills`,
- đổi homepage CSR từ hardcode sang data-driven.
