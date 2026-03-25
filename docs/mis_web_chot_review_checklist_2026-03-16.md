# Review `WEB chốt.pptx` và checklist triển khai

## 1. Kết luận nhanh

PPT của MIS không phải brief làm lại toàn bộ website. Phần lớn yêu cầu rơi vào 5 nhóm:

1. Bổ sung và chuẩn hóa nội dung `Trách nhiệm xã hội` và `SEL/GRACE`.
2. Cập nhật lại nội dung các trang `Thông điệp`, `Tại sao chọn MIS?`, `Đối tác chiến lược`, `Lịch sử hình thành`.
3. Sửa nhãn/menu/hệ đào tạo theo cách gọi mới của MIS.
4. Chỉnh lại dữ liệu `Các cơ sở`.
5. Xử lý lỗi hiển thị tiếng Việt bị vỡ dấu trên một số template public đang dùng thật.

Đánh giá tổng thể:

- Có thể triển khai trên nền hiện tại, không cần đập đi làm lại.
- Nhưng trước khi nhập thêm nội dung từ MIS, cần xử lý nhóm lỗi hiển thị/mã hóa và dọn dữ liệu gốc, nếu không nội dung mới vẫn ra sai.
- Một phần yêu cầu trong PPT đã được đưa vào code ở mức template cứng, nhưng chưa được chuẩn hóa thành dữ liệu quản trị.

## 2. Những gì đã có sẵn

- `/csr/` đã có trang riêng và đã hardcode khá nhiều hoạt động CSR từ PPT.
- `lifeskills.html` đã có section GRACE/SEL, gồm Hawaii, Kymviet, Seroto.
- Route và template cho `Lịch sử hình thành` đã tồn tại.
- Trang `Tại sao chọn MIS?` và `Các hệ đào tạo chuyên sâu` đã có cấu trúc sẵn.
- Dữ liệu `FounderMessage`, `TrainingProgram`, `Campus`, `StudentSpotlight` đều đã có model.

## 3. Phát hiện quan trọng cần ưu tiên

### P0. Lỗi hiển thị tiếng Việt / mojibake trên template public

Đây là blocker kỹ thuật vì MIS đang yêu cầu cập nhật nội dung, nhưng một số template active vẫn đang chứa text sai mã hóa.

Đã xác nhận trong các file:

- `templates/core/home.html`
- `templates/about/whymis.html`
- `templates/core/training_programs.html`
- `templates/core/student_spotlight_list.html`
- `templates/contact/contact.html`

Biểu hiện thực tế đã khớp với screenshot trong PPT:

- `Học sinh nổi bật ca»§a MIS`
- `Tin má»›i`
- nhiều chữ tiếng Việt vỡ dấu trong `Why MIS`, `Training Programs`, `Contact`, `Home`.

### P0. Dữ liệu và giao diện đang lệch nhau

- `CSRProject` trong DB hiện chỉ có 3 bản ghi, nhưng trang `/csr/` đã hardcode nhiều chiến dịch hơn trong template.
- số đếm dự án đang theo DB, nên chưa thể hiện đúng tinh thần `15+ dự án`.
- `AboutPage(page_type='principal')` hiện vẫn mang title `Thông điệp Tổng Giám đốc`, trong khi MIS muốn page này là `Lịch sử hình thành`.
- `TrainingProgram` hiện mới có 4 bản ghi, chưa khớp bộ 5 hệ MIS chốt.
- `Campus` đang có dữ liệu trùng/ngang cấp lẫn lộn giữa `Campus chính`, `Cơ sở Cầu Giấy`, `Cơ sở Láng Hòa Lạc`, `MIS Pandora Landscape`.

### P0. Menu chương trình học còn placeholder

Đã xác nhận trong `templates/core/includes/navbar.html`:

- còn nhãn `Toán`
- còn nhãn `Nội dung tôi sẽ thêm sau`
- tên các hệ chưa khớp đúng cách MIS yêu cầu

## 4. Đánh giá theo từng nhóm yêu cầu trong PPT

### Nhóm A. Trang chủ và trang CSR

Nguồn từ slide 1-5, 9.

Thực tế hiện tại:

- homepage có block `GRACE & Trách nhiệm xã hội`, nhưng đang viết tĩnh và còn lỗi mã hóa.
- `/csr/` đã nhúng khá nhiều campaign/link đúng tinh thần PPT, nhưng phần lớn đang hardcode trong template.
- DB mới có 3 project, nên số liệu và khả năng quản trị không khớp.

Việc cần chỉnh:

- đưa toàn bộ campaign MIS chốt thành dữ liệu quản trị thay vì hardcode template.
- cập nhật thống kê thành `15+ dự án`.
- đổi tên dự án theo slide 9:
  - `Mang trung thu lên vùng biên giới`
  - thêm `Hành động nhỏ - Ngôi trường lớn` vào nhóm nổi bật
- đồng bộ số liệu `dự án`, `hình ảnh`, `tình nguyện viên`, `người thụ hưởng` với nguồn MIS.
- thống nhất hero/home CSR với dữ liệu thật thay vì ảnh + caption tĩnh.

Khuyến nghị:

- thêm model/link con cho minh chứng ngoài site như Facebook/Drive/YouTube.
- tránh tiếp tục hardcode URL dài vào template.

### Nhóm B. Kỹ năng sống, SEL, GRACE

Nguồn từ slide 6.

Thực tế hiện tại:

- phần này đã được làm một phần trong `templates/about/lifeskills.html`.
- đã có block riêng cho Hawaii, Kymviet, Seroto.

Việc cần chỉnh:

- rà lại toàn bộ link và ảnh theo bộ MIS mới gửi.
- xác nhận MIS có gửi ảnh thay thế hay chỉ dùng ảnh hiện có.
- nếu MIS muốn tự cập nhật về sau, nên chuyển nhóm evidence này từ template cứng sang dữ liệu DB/admin.

Đánh giá:

- đây không phải hạng mục phải viết lại từ đầu.
- chủ yếu là QA nội dung, asset và khả năng quản trị lâu dài.

### Nhóm C. Về chúng tôi / Thông điệp / Lịch sử hình thành

Nguồn từ slide 7, 8, 14.

Thực tế hiện tại:

- `FounderMessage` đang lấy dữ liệu động từ DB.
- page `principal` đã tồn tại nhưng dữ liệu đang mang nghĩa `Thông điệp Tổng Giám đốc`.
- `mission/about` đã có bố cục hero + ảnh.

Việc cần chỉnh:

- slide 8: thay nội dung `Thông điệp` bằng đoạn MIS chốt.
- slide 7: chuẩn hóa lại page `principal` thành `Lịch sử hình thành trường`, dùng nội dung từ Google Docs MIS cung cấp.
- slide 14: thay ảnh hero/ảnh minh họa theo file Drive MIS gửi.

Đánh giá:

- phần này chủ yếu là cập nhật content và ảnh.
- riêng `principal` là chỉnh nghiệp vụ nội dung, không nên để lẫn với trang thông điệp như hiện nay.

### Nhóm D. Tại sao chọn MIS? / Tại sao phụ huynh tin tưởng MIS? / Đối tác chiến lược

Nguồn từ slide 11, 12, 13.

Thực tế hiện tại:

- cấu trúc trang đã có sẵn.
- section `Tại Sao Phụ Huynh Tin Tưởng MIS?` và `Đối Tác Chiến Lược` đã có trong DB.
- nhưng template active `templates/about/whymis.html` đang lỗi mã hóa text.

Việc cần chỉnh:

- cập nhật bài viết theo Word/Docs MIS gửi.
- thay bộ ảnh chuẩn MIS gửi.
- cập nhật lại bộ 6 điểm mạnh theo wording mới:
  - Gratitude – Biết ơn
  - Respect – Tôn trọng
  - Accountability – Trách nhiệm
  - Courage – Dũng cảm
  - Engagement – Kết nối
  - các line mô tả Howard Gardner, đa ngôn ngữ, công nghệ số, GRACE, nghệ thuật, nội trú
- thay nội dung `Đối tác chiến lược` theo tài liệu mới.

Đánh giá:

- đây là hạng mục vừa sửa content vừa sửa template.
- phải fix encoding trước, rồi mới nhập bài và thay ảnh.

### Nhóm E. Hệ đào tạo và menu chương trình

Nguồn từ slide 10, 15.

Thực tế hiện tại:

- menu navbar đang hardcode một phần label.
- trang `Các hệ đào tạo chuyên sâu` render động theo `TrainingProgram`.
- DB hiện có 4 record, chưa khớp bộ 5 hệ MIS chốt.

MIS chốt tên cần hiển thị:

- Hệ STEAM
- Hệ Chất lượng cao Công nghệ
- Hệ Tiếng Anh tài năng
- Hệ Tiếng Trung tài năng
- Hệ Toán tài năng

Việc cần chỉnh:

- sửa menu desktop và mobile trong navbar.
- bỏ placeholder `Nội dung tôi sẽ thêm sau`.
- đổi `Toán` thành `Toán tài năng`.
- tách lại các record chương trình để đủ 5 card.
- rà lại ảnh từng card khi MIS gửi.

Đánh giá:

- đây là hạng mục vừa có sửa DB vừa có sửa template.
- nếu chỉ sửa text trong navbar mà không sửa dữ liệu `TrainingProgram`, trang listing vẫn lệch.

### Nhóm F. Học sinh nổi bật

Nguồn từ slide 16.

Thực tế hiện tại:

- dữ liệu `StudentSpotlight` trong DB nhìn ổn.
- nhưng template list page đang vỡ dấu tiếng Việt.

Việc cần chỉnh:

- sửa lại `templates/core/student_spotlight_list.html` về UTF-8 đúng.
- kiểm tra thêm meta/title/labels trên trang này vì file đang bị nhiễm mojibake nhiều chỗ.

Đánh giá:

- đây là lỗi template, không phải lỗi dữ liệu.

### Nhóm G. Các cơ sở / contact

Nguồn từ slide 17.

Thực tế hiện tại:

- DB đang có 4 campus:
  - `Campus chính – Cầu Giấy`
  - `Co so Cau Giay`
  - `Co so Lang Hoa Lac`
  - `MIS Pandora Landscape – Láng – Hòa Lạc`
- dữ liệu bị trùng logic và không thống nhất dấu/tên gọi.
- contact template cũng đang có lỗi mã hóa text.

Việc cần chỉnh:

- giữ `37 Hoàng Quán Chi` là đúng.
- đổi `MIS Pandora Landscape: Láng Hoà Lạc`, bỏ cụm `Làng Đại học`.
- rà lại xem có cần giữ riêng `Cơ sở Cầu Giấy` và `Campus chính` hay gộp.
- chuẩn hóa toàn bộ tên cơ sở có dấu tiếng Việt đồng nhất.

Đánh giá:

- đây là hạng mục dọn dữ liệu + sửa hiển thị.

## 5. Checklist triển khai đề xuất

### Phase 1. Blocker kỹ thuật

- [ ] Fix toàn bộ template public đang mojibake về UTF-8 đúng.
- [ ] Rà lại các page active sau fix: home, whymis, training programs, student spotlight, contact.
- [ ] Xóa các placeholder public như `Nội dung tôi sẽ thêm sau`.

### Phase 2. Dọn dữ liệu nền

- [ ] Chuẩn hóa `AboutPage(principal)` thành `Lịch sử hình thành`.
- [ ] Cập nhật `FounderMessage` theo đoạn MIS chốt.
- [ ] Chuẩn hóa `Campus` theo tên chính thức MIS.
- [ ] Chuẩn hóa `TrainingProgram` thành đúng 5 hệ.
- [ ] Kiểm kê lại `CSRProject` để không còn lệch giữa DB và template.

### Phase 3. Cập nhật nội dung theo tài liệu MIS

- [ ] Nhập nội dung `Lịch sử hình thành` từ Google Docs.
- [ ] Nhập bài viết mới cho `Tại sao chọn MIS?`.
- [ ] Nhập bài viết `Tại sao phụ huynh tin tưởng MIS?`.
- [ ] Nhập bài viết `Đối tác chiến lược`.
- [ ] Cập nhật wording GRACE theo slide 12.
- [ ] Cập nhật tên dự án CSR theo slide 9.

### Phase 4. Cập nhật asset

- [ ] Thay ảnh chuẩn cho `Why MIS`.
- [ ] Thay ảnh `Đối tác chiến lược`.
- [ ] Thay ảnh hero/about theo slide 14.
- [ ] Nhận và gắn ảnh từng hệ đào tạo theo slide 15.
- [ ] Rà alt text cho toàn bộ ảnh mới.

### Phase 5. Chuẩn hóa quản trị nội dung

- [ ] Tách link minh chứng CSR khỏi template hardcode.
- [ ] Tạo cấu trúc quản trị cho proof links/evidence links nếu MIS còn bổ sung dài hạn.
- [ ] Cho phép đánh dấu project nổi bật trên home.
- [ ] Cho phép chỉnh stats CSR từ admin hoặc data source rõ ràng.

### Phase 6. QA trước khi bàn giao MIS

- [ ] Soát chính tả và dấu tiếng Việt trên toàn bộ page bị ảnh hưởng.
- [ ] Kiểm tra desktop + mobile cho navbar chương trình học.
- [ ] Kiểm tra số card hệ đào tạo hiển thị đúng 5 mục.
- [ ] Kiểm tra `/csr/` hiển thị đúng số liệu, đúng tên dự án nổi bật.
- [ ] Kiểm tra `student spotlight` không còn lỗi font/dấu.
- [ ] Kiểm tra `contact` hiển thị đúng tên cơ sở, địa chỉ, map.
- [ ] Kiểm tra toàn bộ link ngoài site từ PPT không bị 404 hoặc private.

## 6. Mức ưu tiên khuyến nghị

### Phải làm ngay

- Fix mojibake trên template public.
- Chỉnh lại menu chương trình học.
- Dọn dữ liệu campus.
- Chuẩn hóa `principal` thành lịch sử hình thành.

### Nên làm trong cùng đợt

- Cập nhật toàn bộ content/ảnh theo Docs và Drive MIS.
- Chuẩn hóa 5 hệ đào tạo trong DB.
- Đồng bộ CSR count và danh sách project.

### Có thể làm sau nhưng nên có

- Chuyển CSR evidence và SEL evidence sang dữ liệu quản trị.
- Giảm hardcode trong template `csr/list.html`.

## 7. Ước lượng effort tương đối

- `Fix encoding + cleanup template`: trung bình đến cao, vì đang chạm nhiều page public.
- `Update content + images`: trung bình.
- `Chuẩn hóa CSR sang data-driven`: trung bình đến cao.
- `Dọn training programs + campus`: thấp đến trung bình.

## 8. Khuyến nghị làm việc với MIS

- Chốt lại một bộ master content cuối cùng bằng Word/Doc, không vừa Docs vừa link rời nếu tránh được.
- Yêu cầu MIS gửi một thư mục ảnh final theo từng page:
  - `whymis`
  - `training-programs`
  - `about`
  - `csr`
- Với CSR, nên chốt mỗi chiến dịch theo format:
  - tên chiến dịch
  - năm
  - mô tả ngắn
  - 1 ảnh cover
  - 2-5 link minh chứng

