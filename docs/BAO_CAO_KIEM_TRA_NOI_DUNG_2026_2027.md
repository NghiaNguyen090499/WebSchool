# 📋 BÁO CÁO KIỂM TRA NỘI DUNG WEBSITE MIS 2026–2027
> **Ngày tạo:** 2026-02-15
> **Nguồn chuẩn (Source of Truth):** `Tổng quan chương trình GD MIS 2026-2027.docx`
> **Phạm vi:** Toàn bộ Django codebase (repo `WebsiteSchool/`)

---

## PHẦN 1: TRUTH DATA 2026–2027 (Trích xuất từ docx)

### 1.1 Tổng quan cấu trúc chương trình

| # | Chủ đề | Cấp học | Trạng thái trích |
|---|--------|---------|-------------------|
| 1 | **Toán học tích hợp AI** | Tiểu học (K1-K5), THCS (K6-K9), THPT (K10-K12) | EXACT_QUOTE |
| 2 | **Hệ Toán Tài năng & Công nghệ mới (AI)** | Liên thông TH → THCS → THPT | EXACT_QUOTE |
| 3 | **Chương trình Phát triển Ngoại ngữ Thế hệ mới** – Đa ngoại ngữ (Anh + Trung) | Liên thông TH → THCS → THPT | EXACT_QUOTE |
| 4 | **Hệ Tiếng Anh Tài năng** – Lộ trình IELTS 8.0+ | THCS → THPT | EXACT_QUOTE |
| 5 | **Hệ Tiếng Trung Tài năng** – Lộ trình HSK 5-6 | TH → THCS → THPT | EXACT_QUOTE |
| 6 | **Ngữ văn Thế hệ mới** – Từ cảm thụ đến sáng tạo số | TH → THCS → THPT | EXACT_QUOTE |
| 7 | **Công nghệ mới & AI** – Làm chủ công cụ, kiến tạo tương lai | K-12 (Lớp 1 → 12) | EXACT_QUOTE |
| 8 | **Hệ sinh thái Phần mềm hỗ trợ đào tạo 4.0** (EdTech) | Toàn trường | EXACT_QUOTE |

### 1.2 Hệ đào tạo chuyên biệt (PROGRAM_CHOICES)

| Hệ | Docx gọi tên | Website hiện tại (model) | Sai lệch? |
|----|--------------|--------------------------|-----------|
| 1 | **Hệ STEAM Chuẩn / CLC** | `steam` = "Hệ STEAM", `steam_clc` = "Hệ STEAM Chất lượng cao" | ✅ Khớp |
| 2 | **Hệ Tài năng Toán – Công nghệ mới** | `math` = "Hệ Tài năng Toán và Công nghệ mới" | ✅ Khớp |
| 3 | **Hệ Tài năng Ngôn ngữ** (bao gồm Anh + Trung) | `english` = "Hệ Tài năng Tiếng Anh", `chinese` = "Hệ Tài năng Tiếng Trung" | ⚠️ **SAI LỆCH** — Docx gọi chung "Hệ Tài năng Ngôn ngữ", website tách thành 2 hệ riêng |

### 1.3 Chuẩn đầu ra theo Hệ & Cấp (EXACT_QUOTE từ Table 16)

| Cấp | Hệ | TA (tiết/tuần) | Trung (tiết/tuần) | Chuẩn đầu ra TA | Chuẩn đầu ra Trung |
|-----|-----|----------------|--------------------|-----------------|--------------------|
| TH (1-5) | STEAM Chuẩn/CLC | 7-9 | 1-2 | Cambridge Movers / CEFR Pre A2 | Phát âm, giao tiếp cơ bản |
| TH (1-5) | Tài năng Toán-CN | 11 | 1-2 | Cambridge Movers / CEFR Pre A2 | Phát âm, giao tiếp cơ bản |
| TH (1-5) | **Tài năng Ngôn ngữ** | **14** | **1-3** | Cambridge Flyers/KET/PET, CEFR A2/A2+ | **YCT 1-3** (≈ HSK1-2) |
| THCS (6-9) | STEAM Chuẩn/CLC | 6-7 | 2 | CEFR A2+ / B1 | YCT2-3 (≈ HSK1-2) |
| THCS (6-9) | Tài năng Toán-CN | 8 | 2 | CEFR A2+ / B1 | YCT2-3 (≈ HSK1-2) |
| THCS (6-9) | **Tài năng Ngôn ngữ** | **10** | **5** | **IELTS 4.0-6.0+ / CEFR B1-B2** | **YCT4** (≈ HSK3-4) |
| THPT (10-12) | STEAM Chuẩn/CLC | 6-7 | 3 | IELTS 4.0-6.0+ / CEFR B1-B2 | HSK 2-4 |
| THPT (10-12) | Tài năng Toán-CN | 7 | 3 | IELTS 4.0-6.0+ / CEFR B1-B2 | HSK 2-4 |
| THPT (10-12) | **Tài năng Ngôn ngữ** | **10** | **5-8** | **IELTS 6.5-8.0+ / CEFR B2-C1** | **HSK 4-6** |

### 1.4 Bộ công cụ AI & EdTech (EXACT_QUOTE từ Chương 3)

| Nền tảng | Vai trò | Nguồn |
|----------|---------|-------|
| **Azota** | Quản lý & đánh giá giáo dục, ngân hàng đề thi, chấm phiếu tô AI | Chương 3, line 353-360 |
| **iCorrect** | Trợ lý ảo luyện nói Tiếng Anh 24/7, chấm điểm IELTS Speaking | Chương 3, line 362-367 |
| **VR/AR** | Trải nghiệm học tập đa chiều, mô phỏng 3D, phòng thí nghiệm ảo | Chương 3, line 369-374 |
| **Nexta** | Lớp học thông minh, tương tác 1:1, cá nhân hóa AI-Track | Chương 3, line 375-381 |
| **Generative AI** | ChatGPT, Gemini, DeepSeek, GeoGebra AI, Math AI, Azota AI | Chương 3, line 382-385 |
| **Phần mềm lập trình** | Scratch (TH), Python (THCS/THPT), Tuxpaint, Microsoft Ecosystem | Chương 3, line 386-390 |
| **DeepSeek / Doubao** | Trợ lý Tiếng Trung ảo, giải nghĩa từ vựng, luyện hội thoại | Chương 2, line 237-238 |

### 1.5 Giáo trình & Đối tác (EXACT_QUOTE từ Table 14, 15)

| Cấp | Tiếng Anh | Chuẩn đầu ra TA | Tiếng Trung | Chuẩn đầu ra Trung |
|-----|-----------|-----------------|-------------|---------------------|
| TH | Super Minds, Phonics, Cambridge YLE, Cambridge Primary Science/Maths | CEFR Pre A2/A2 | YCT Standard Course 1-3 & AI Doubao | YCT 1-3 |
| THCS | Global Success, Speak Now, Macmillan Science, Pre-IELTS | CEFR A2+/B1 | HSK Standard Course 1-3 (3.0 mới nhất) | HSK 1-3 (≈ YCT 3-4) |
| THPT | Global Success, Speak Now, Reading Explorer, Pre-IELTS, IELTS Focus Plus | CEFR B1/C1 | HSK Standard Course 4-6 (3.0 mới nhất) | HSK 4-6 |

### 1.6 Đối tác đào tạo ngoại ngữ
- **Hệ Tài năng Ngôn ngữ** kết hợp với **Jaxtina English** và **Tiếng Trung Quốc tế Thời đại** (EXACT_QUOTE line 249)

### 1.7 Thông tin chưa có trong docx → NEED_CONFIRM

| Mục | Trạng thái |
|-----|-----------|
| Học phí / Chính sách ưu đãi | **NEED_CONFIRM** – Docx không đề cập |
| Tuyển sinh: deadline, quy trình, hồ sơ cụ thể | **NEED_CONFIRM** – Docx không đề cập |
| Mầm non / Tiền tiểu học | **NEED_CONFIRM** – Docx không mô tả chương trình Mầm non |
| Địa chỉ, Hotline, Email, Giờ làm việc | **NEED_CONFIRM** – Không nằm trong docx |
| Kỹ năng sống & Giá trị sống | **NEED_CONFIRM** – Docx không có chương chi tiết cho KNS |
| Chương trình Trải nghiệm sáng tạo (TNST) | **NEED_CONFIRM** – Docx không mô tả TNST |
| Chương trình Robotics | **NEED_CONFIRM** – Có file riêng `ROBOTICS 2026-2027.pdf`, không nằm trong docx |
| Creative Movement (Tâm vận động) | **NEED_CONFIRM** – Docx không đề cập |

---

## PHẦN 2: INVENTORY ĐIỂM NỘI DUNG TRÊN WEBSITE

### 2.1 Template & Content Points Map

| # | Trang/Feature | URL Pattern | Template | Content Source | Loại nội dung |
|---|--------------|-------------|----------|----------------|---------------|
| 1 | **Trang chủ** | `/` | `core/home.html` | DB: HeroSlide, TrainingProgram, Achievement, Statistics, Partners | Hero, giới thiệu hệ đào tạo, tuyển sinh |
| 2 | **Hệ đào tạo (list)** | `/he-dao-tao/` | `core/training_programs.html` | DB: TrainingProgram, TrainingProgramGroup | 5 hệ chuyên biệt, thông tin đối tác |
| 3 | **Hệ đào tạo (detail)** | `/he-dao-tao/<slug>/` | `core/training_program_detail.html` | DB: TrainingProgram | Chi tiết từng hệ |
| 4 | **Chương trình Toán** | `/about/curriculum/math/` | `about/math.html` | JSON: `program_content_2026_2027.json` → blocks.math | Triết lý, AI tools, roadmap |
| 5 | **Chương trình Ngữ văn** | `/about/curriculum/literature/` | `about/literature.html` | JSON: blocks.literature | Trụ cột, quy trình 4S, đánh giá |
| 6 | **Chương trình Tiếng Anh** | `/about/curriculum/english/` | View `page_detail` | JSON: blocks.overview_english | Lộ trình IELTS, giáo trình |
| 7 | **Chương trình Tiếng Trung** | `/about/curriculum/chinese/` | View `page_detail` | JSON: blocks.overview_chinese | Lộ trình HSK, giáo trình |
| 8 | **Future with AI** | `/about/future-ai/` | `about/future_ai.html` | JSON: blocks.future_ai | CNTT & AI, EdTech, năng lực số |
| 9 | **Tại sao chọn MIS** | `/about/whymis/` | `about/whymis.html` | DB: AboutPage(whymis) + AboutSections | Tuyển sinh, USPs |
| 10 | **Prototype/Lowfi pages** | `/prototype/mis/<key>/` | `core/lowfi/mis_*.html` | Static HTML / MISPrototypeSiteContent | Home, cấp học, EdTech, Parent Portal |
| 11 | **Sức mạnh MIS** | `/about/strengths/` | `about/strengths.html` | DB: AboutPage(strengths) + Sections | 8 điểm mạnh |
| 12 | **Tầm nhìn** | `/about/vision/` | View `page_detail` | DB: AboutPage(vision) | Giá trị cốt lõi |
| 13 | **Tuyển sinh** | `/tuyen-sinh/` | `admissions/` | DB: AdmissionInfo, AdmissionDocument | Cấp học, form ĐK |
| 14 | **Navbar/Footer** | (global) | `core/includes/navbar.html`, `base.html` | JSON navigation + DB MenuItem | Menu, links |
| 15 | **Cơ sở vật chất** | `/co-so-vat-chat/` | `core/facilities.html` | DB: Facility | Phòng lab, STEAM room |

### 2.2 Nguồn cung cấp nội dung (Data Sources)

| Source | File/Module | Vai trò |
|--------|------------|---------|
| **JSON Data File** | `core/data/program_content_2026_2027.json` (593 dòng) | Nội dung chương trình chính, phân theo blocks |
| **Django Models** | `core/models.py` → TrainingProgram, TrainingProgramGroup, SchoolInfo | Hệ đào tạo, thông tin trường |
| **About Models** | `about/models.py` → AboutPage, AboutSection | Trang giới thiệu, tuyển sinh |
| **Admissions Models** | `admissions/models.py` → AdmissionInfo, AdmissionRegistration | Tuyển sinh/đăng ký |
| **Views Logic** | `about/views.py` → `page_detail()` | Routing nội dung theo page_type |
| **Program Utility** | `core/utils/program_content.py` | Load JSON, resolve navigation |
| **Context Processor** | `core/context_processors.py` | School info global |

---

## PHẦN 3: BẢNG THAY THẾ NỘI DUNG (MAPPING P0/P1/P2)

### Ký hiệu: 
- **P0** = Phải sửa trước khi publish (nội dung sai so với docx)
- **P1** = Cần sửa sớm (thiếu nội dung quan trọng hoặc cấu trúc chưa đúng)
- **P2** = Cải thiện (UX, SEO, data-driven)

### 3.1 P0 — Nội dung sai / cũ so với docx

| # | Page/Feature | Where in code | Current content | New content (theo docx) | Change type | Risk | Owner | Acceptance Criteria |
|---|-------------|---------------|-----------------|-------------------------|-------------|------|-------|---------------------|
| P0-1 | **Hệ đào tạo (model)** | `core/models.py` L126-130: `PROGRAM_CHOICES` | 5 hệ riêng biệt: steam, steam_clc, math, english, chinese | Docx nêu **3 hệ chính**: (1) Hệ STEAM Chuẩn/CLC, (2) Hệ Tài năng Toán – CN mới, (3) **Hệ Tài năng Ngôn ngữ** (gộp Anh + Trung) | **Restructure** | **High** — ảnh hưởng toàn bộ menu, URL, admin, DB | BE | Model khớp 3 hệ + 2 sub-track; Admin + migration không lỗi |
| P0-2 | **training_programs.html** hero text | `templates/core/training_programs.html` L43-48 | "MIS mang đến 5 hệ đào tạo chuyên biệt... Công nghệ 4.0, Ngoại ngữ Anh - Trung và tư duy Toán học vượt trội" | Text mới theo docx: "MIS mang đến 3 hệ đào tạo chuyên biệt... tích hợp AI trong thời đại trí tuệ nhân tạo, mô hình Hợp tác – Sáng tạo – Giải quyết vấn đề" | **Replace** | Med | FE/Content | Text = docx paraphrase, không hard-code |
| P0-3 | **Tiếng Anh – Chuẩn đầu ra** | `core/data/program_content_2026_2027.json` L190-202: targets | standard.ielts = "4.0-6.0+", talent.ielts = "6.5-8.0+" | Phải bổ sung chi tiết **theo cấp**: TH = Cambridge Movers/CEFR Pre A2, THCS = CEFR A2+/B1, THPT standard = CEFR B1-B2, talent = CEFR B2-C1 | **Replace** | Med | BE | JSON targets match Table 16 |
| P0-4 | **Tiếng Trung – Chuẩn đầu ra** | `core/data/program_content_2026_2027.json` L235-247: targets | standard.hsk = "2-4", talent.hsk = "4-6" | Phải chi tiết: TH talent = YCT 1-3, THCS talent = YCT4 (HSK3-4), THPT talent = HSK 4-6 | **Replace** | Med | BE | JSON match Table 16 |
| P0-5 | **Giáo trình tiêu biểu** | Không tìm thấy trong JSON/templates | Website chưa liệt kê giáo trình cụ thể | Bổ sung Table 14 + 15 từ docx: Super Minds, Global Success, Reading Explorer, YCT/HSK Standard Course... | **Add** | Low | BE/Content | Danh sách giáo trình hiển thị đúng per cấp |
| P0-6 | **Đối tác ngôn ngữ** | `core/data/...json` và TrainingProgram.partner_name | Chưa rõ | Docx nêu: **Jaxtina English** và **Tiếng Trung Quốc tế Thời đại** | **Add/Replace** | Low | Content | Partner section đúng tên docx |
| P0-7 | **Thời lượng đào tạo ngoại ngữ** | Không thấy trên website | Chưa hiển thị | Phải hiện bảng thời lượng: Hệ TN Ngôn ngữ TH=14 tiết TA + 1-3 tiết Trung/tuần, THCS=10+5, THPT=10+5-8 (Table 16) | **Add** | Med | FE/BE | Bảng thời lượng match docx |
| P0-8 | **Toán – Lộ trình chi tiết K1-K12** | JSON blocks.math has articulation 3 items | Chỉ có 3 bullet tóm tắt | Docx có Tables 2, 5, 8 (30+ rows) chi tiết theo từng khối lớp | **Add** | Med | BE/Content | Bảng roadmap per grade = docx |
| P0-9 | **EdTech ecosystem – chưa có trang riêng** | Chỉ có prototype `core/lowfi/mis_edtech.html` | Lowfi prototype, không publish | Docx Chương 3 mô tả chi tiết 6 nền tảng EdTech | **Add** | Med | FE/BE | Trang EdTech live, nội dung = Chương 3 |

### 3.2 P1 — Thiếu nội dung quan trọng

| # | Page/Feature | Where in code | Current | New (theo docx) | Change | Risk | Owner | AC |
|---|-------------|---------------|---------|-----------------|--------|------|-------|---------|
| P1-1 | **Ngữ văn – Quy trình 4S** | `about/literature.html` L120-133 | Template render `process_4s` từ JSON | JSON có 4 items đúng docx ✅ nhưng **chưa có phần "Chuyển đổi tư duy"** (Prompting, Phản biện, Liêm chính số) | **Add** | Low | BE | 3 chuyển đổi tư duy bổ sung |
| P1-2 | **Ngữ văn – Lộ trình liên thông** | `about/literature.html` | Chưa có | Docx Table 19: TH = Thơ ca/kịch nghệ, THCS = Tư duy hệ thống, THPT = Kiến tạo bản sắc | **Add** | Low | BE | Table roadmap per cấp |
| P1-3 | **Future AI – Mục tiêu đầu ra chi tiết** | `about/future_ai.html` + JSON blocks.future_ai.outcomes | 4 bullet outcomes | Docx mục "MỤC TIÊU ĐẦU RA KỲ VỌNG" có 6 chi tiết hơn: Tư duy kiến tạo, Data Science, AI Literacy, Tư duy phản biện, Tự học, Digital Portfolio | **Replace** | Low | Content | 6 outcomes đầy đủ = docx |
| P1-4 | **Future AI – Hệ sinh thái hỗ trợ** | JSON + template | Chưa chi tiết | Docx: Lớp học Nexta, VR/AR lab – nên mô tả rõ hơn | **Add** | Low | FE | Section hệ sinh thái hiển thị |
| P1-5 | **Toán – Mô hình lớp học thông minh** | `about/math.html` | Chỉ list tools | Docx mô tả "AI-READY CLASSROOM" chi tiết per cấp (Tables 0, 3, 6) | **Add** | Med | FE/Content | Section AI Classroom per cấp |
| P1-6 | **Toán – Quy trình tiết học mẫu** | `about/math.html` | Chưa có | Docx: TH=35 phút (5+10+15+5), THCS/THPT=40 phút (5+10+15+5+5) – Tables 1, 4, 7 | **Add** | Low | FE | Bảng quy trình tiết mẫu |
| P1-7 | **SEO meta description** | `templates/core/training_programs.html` L5-6 | "Hệ Tài năng Tiếng Anh, Hệ Tài năng Tiếng Trung" | Đổi thành "Hệ Tài năng Ngôn ngữ" để khớp docx | **Replace** | Low | FE | Meta desc = cấu trúc docx |
| P1-8 | **Trang cấp học (Academics)** | `about/views.py` page_detail → 'academics' | Trang tổng quan chương trình (DB-driven) | Cần cập nhật subtitle/content theo docx: "MIS & Lộ trình bước vào kỷ nguyên sáng tạo" | **Replace** | Low | Content |
| P1-9 | **Tầm nhìn 2035 (Chương 1 docx)** | JSON blocks.vision_2035 | Đã có 4 chapters trong JSON ✅ | Kiểm tra template render → `about/vision.html` hoặc `about/future_ai.html` – nội dung chưa rõ hiển thị đầy đủ hay không | **Verify** | Low | FE | Đảm bảo Chương 1 lên web |

### 3.3 P2 — Cải thiện kiến trúc & UX

| # | Page/Feature | Where | Current | Proposed | Change | Risk | Owner |
|---|-------------|-------|---------|----------|--------|------|-------|
| P2-1 | **Hard-coded fallback text** | `core/home.html`, `about/whymis.html` (L726-727), training_programs.html (L38-48) | Nhiều fallback text tĩnh | Chuyển sang DB/JSON driven, không hard-code | **Restructure** | Med | BE |
| P2-2 | **Training system gộp Tài năng Ngôn ngữ** | `core/models.py` TrainingProgram | `english` và `chinese` là 2 program riêng | Thêm concept "SubTrack" để Hệ TN Ngôn ngữ có 2 track: TA + Trung | **Restructure** | High | BE |
| P2-3 | **Version year trong URL** | `about/urls.py` L62-63 | `schedule/2026-2027/` hard-code | Sử dụng dynamic year từ JSON config | **Restructure** | Low | BE |
| P2-4 | **Program Year versioning** | `program_content.py` L10-11 | Hard-code file name "2026_2027" | Support multiple year files, fallback mechanism | **Restructure** | Med | BE |
| P2-5 | **Trang EdTech chính thức** | `core/lowfi/mis_edtech.html` (prototype chỉ) | Prototype only | Tạo trang chính thức `/about/edtech/` với nội dung Chương 3 | **Add** | Low | FE/BE |

---

## PHẦN 4: GIẢI PHÁP KIẾN TRÚC NỘI DUNG ĐỀ XUẤT

### 4.1 Đánh giá hiện trạng

Website MIS hiện đang dùng **mô hình hybrid**:
- **JSON file** (`program_content_2026_2027.json`) cho nội dung chương trình chính
- **Django Models + Admin** cho data "sống" (hệ đào tạo, tuyển sinh, sections)
- **AboutPage + AboutSection** (CMS-like) cho các trang giới thiệu
- **Hard-coded HTML** trong templates cho một số nội dung

### 4.2 Hướng đề xuất: **Hướng 3 – JSON Data Fixtures + Loader (Ưu tiên)**

#### Lý do chọn:

| Tiêu chí | Hướng 1 (DB Models) | Hướng 2 (CMS) | **Hướng 3 (JSON + Loader)** ✅ |
|----------|---------------------|---------------|-------------------------------|
| Tốc độ triển khai | Chậm (migration) | Rất chậm (Wagtail setup) | **Nhanh nhất** |
| Version theo năm học | Khó (cần snapshot DB) | Phức tạp | **Trivial** (file per year) |
| Team content cập nhật | Cần Admin | UI tốt | Cần dev hoặc admin tool |
| Không sai lệch docx | Risk cao (manual entry) | Risk trung (WYSIWYG) | **Risk thấp** (review PR) |
| Phù hợp hiện trạng | Trung bình | Thấp (phải rebuild) | **Cao** (đã dùng sẵn) |
| Scale 2027-2028+ | Tốt | Tốt | **Tốt** (copy + edit) |

#### Kiến trúc đề xuất:

```
core/data/
├── program_content_2026_2027.json  ← (đã có - mở rộng)
├── program_content_2027_2028.json  ← (tương lai)
└── schema.json                     ← (validation schema)
```

#### 4.3 Schema mở rộng cho JSON

```json
{
  "program_year": "2026-2027",
  "source_doc": "Tổng quan chương trình GD MIS 2026-2027.docx",
  "approved_at": "2026-02-15",
  "version": "2026.2",
  
  "training_systems": {
    "steam_standard": {
      "name": "Hệ STEAM Chuẩn / CLC",
      "grade_levels": "Tiểu học – THCS – THPT",
      "foreign_lang_hours": {
        "primary": {"english": "7-9", "chinese": "1-2"},
        "middle": {"english": "6-7", "chinese": "2"},
        "high": {"english": "6-7", "chinese": "3"}
      },
      "output_standards": { "...per cấp theo Table 16..." }
    },
    "math_tech_talent": {
      "name": "Hệ Tài năng Toán – Công nghệ mới",
      "foreign_lang_hours": { "..." },
      "output_standards": { "..." }
    },
    "language_talent": {
      "name": "Hệ Tài năng Ngôn ngữ",
      "sub_tracks": ["Tiếng Anh Tài năng", "Tiếng Trung Tài năng"],
      "partners": ["Jaxtina English", "Tiếng Trung Quốc tế Thời đại"],
      "foreign_lang_hours": {
        "primary": {"english": "14", "chinese": "1-3"},
        "middle": {"english": "10", "chinese": "5"},
        "high": {"english": "10", "chinese": "5-8"}
      },
      "output_standards": { "..." }
    }
  },
  
  "blocks": {
    "math": { "...giữ nguyên cấu trúc hiện tại + bổ sung roadmap per grade..." },
    "literature": { "...bổ sung lộ trình liên thông Table 19..." },
    "overview_english": { "...bổ sung giáo trình Table 14..." },
    "overview_chinese": { "...bổ sung giáo trình Table 15..." },
    "future_ai": { "...bổ sung outcomes chi tiết 6 mục..." },
    "edtech_ecosystem": {
      "platforms": [
        {"name": "Azota", "role": "Quản lý & Đánh giá", "..."},
        {"name": "iCorrect", "role": "Luyện nói TA 24/7", "..."},
        {"name": "VR/AR", "role": "Trải nghiệm đa chiều", "..."},
        {"name": "Nexta", "role": "Lớp học thông minh", "..."},
        {"name": "Generative AI", "role": "Hỗ trợ học tập & nghiên cứu", "..."},
        {"name": "Phần mềm lập trình", "role": "Scratch/Python/MS Ecosystem", "..."}
      ]
    }
  },

  "curriculum": {
    "textbooks_english": { "...Table 14..." },
    "textbooks_chinese": { "...Table 15..." }
  },
  
  "sample_lesson": {
    "primary_35min": { "...Table 1..." },
    "secondary_40min": { "...Table 4/7..." }
  }
}
```

#### 4.4 Cách version theo năm học

```python
# core/utils/program_content.py - Sửa đổi
PROGRAM_CONTENT_DIR = Path(settings.BASE_DIR) / "core" / "data"

def get_content_file(year=None):
    year = year or getattr(settings, "MIS_PROGRAM_YEAR", "2026-2027")
    filename = f"program_content_{year.replace('-', '_')}.json"
    return PROGRAM_CONTENT_DIR / filename
```

#### 4.5 Content Governance (Quy trình đảm bảo không sai lệch docx)

1. **Quy trình cập nhật:** Docx → Review meeting → JSON PR → Code review → Staging → Approve → Production
2. **Mỗi field trong JSON có `source_ref`** trỏ ngược về dòng/bảng trong docx
3. **CI check:** Script validate JSON against schema + check NEED_CONFIRM flags
4. **Lock production:** Chỉ deploy khi tất cả NEED_CONFIRM đã được resolve

---

## PHẦN 5: KẾ HOẠCH TRIỂN KHAI & CHECKLIST QA

### 5.1 Epic Breakdown

#### EPIC 1: Cập nhật JSON Data (3-5 ngày)
| Task | File | Estimate | Assignee |
|------|------|----------|----------|
| E1-T1: Mở rộng JSON schema với `training_systems` | `core/data/program_content_2026_2027.json` | 1d | BE |
| E1-T2: Bổ sung `curriculum` (giáo trình Table 14, 15) | JSON | 0.5d | Content/BE |
| E1-T3: Bổ sung `sample_lesson` (quy trình tiết học Table 1, 4, 7) | JSON | 0.5d | Content/BE |
| E1-T4: Cập nhật targets chi tiết theo Table 16 | JSON | 0.5d | BE |
| E1-T5: Bổ sung `edtech_ecosystem` block từ Chương 3 | JSON | 1d | Content/BE |
| E1-T6: Bổ sung outcomes chi tiết cho `future_ai` | JSON | 0.5d | BE |
| E1-T7: Bổ sung `math` roadmap per grade (Tables 2, 5, 8) | JSON | 1d | Content/BE |
| E1-T8: Bổ sung `literature` lộ trình liên thông (Table 19) | JSON | 0.5d | Content |

#### EPIC 2: Cập nhật Models & Backend (2-3 ngày)
| Task | File | Estimate | Assignee |
|------|------|----------|----------|
| E2-T1: Không sửa model TrainingProgram (giữ 5 choices) nhưng thêm field `system_group` để nhóm english+chinese thành "Tài năng Ngôn ngữ" | `core/models.py` | 1d | BE |
| E2-T2: Migration | `core/migrations/` | 0.5d | BE |
| E2-T3: Cập nhật `program_content.py` hỗ trợ multi-year | `core/utils/program_content.py` | 0.5d | BE |
| E2-T4: Cập nhật views load new blocks | `about/views.py`, `core/views.py` | 0.5d | BE |
| E2-T5: Admin cập nhật partner_name cho Ngôn ngữ | Django Admin | 0.5d | Content |

#### EPIC 3: Cập nhật Templates & Frontend (3-5 ngày)
| Task | File | Estimate | Assignee |
|------|------|----------|----------|
| E3-T1: Training programs hero text (P0-2) | `templates/core/training_programs.html` | 0.5d | FE |
| E3-T2: SEO meta descriptions (P1-7) | Multiple templates | 0.5d | FE |
| E3-T3: Trang Tiếng Anh – bổ sung giáo trình, thời lượng | About English template | 1d | FE |
| E3-T4: Trang Tiếng Trung – bổ sung giáo trình, thời lượng | About Chinese template | 1d | FE |
| E3-T5: Trang Toán – bổ sung roadmap per grade, tiết học mẫu | `templates/about/math.html` | 1d | FE |
| E3-T6: Trang Ngữ văn – bổ sung chuyển đổi tư duy, lộ trình | `templates/about/literature.html` | 0.5d | FE |
| E3-T7: Trang Future AI – cập nhật outcomes, hệ sinh thái | `templates/about/future_ai.html` | 0.5d | FE |
| E3-T8: Tạo trang EdTech chính thức | New: `templates/about/edtech.html` + URL + View | 1d | FE |
| E3-T9: Loại bỏ hard-coded fallback chuyển sang data-driven | Multiple templates | 1d | FE/BE |

#### EPIC 4: QA & Content Review (2 ngày)
| Task | Estimate | Assignee |
|------|----------|----------|
| E4-T1: Cross-check JSON vs docx (100% fields) | 1d | Content Lead |
| E4-T2: Responsive testing (Mobile/Tablet/Desktop) | 0.5d | QA |
| E4-T3: Link/CTA testing (no broken links) | 0.5d | QA |
| E4-T4: SEO audit (meta, title, og tags) | 0.5d | QA |

### 5.2 Danh sách File/Module cần sửa

```
📁 Cần sửa:
├── core/data/program_content_2026_2027.json     ← MỞ RỘNG (P0-3,4,5,6,7,8,9)
├── core/models.py                                ← THÊM field system_group (P0-1, P2-2)
├── core/migrations/00XX_*.py                     ← AUTO-GENERATE
├── core/utils/program_content.py                 ← MULTI-YEAR support (P2-4)
├── core/views.py                                 ← Load new blocks (E2-T4)
├── about/views.py                                ← Load edtech block (E2-T4)
├── about/urls.py                                 ← Thêm /about/edtech/ (P2-5)
├── templates/core/training_programs.html          ← Text update (P0-2)
├── templates/about/math.html                      ← Bổ sung roadmap (P0-8, P1-5,6)
├── templates/about/literature.html                ← Bổ sung lộ trình (P1-1,2)
├── templates/about/future_ai.html                 ← Outcomes update (P1-3,4)
├── templates/about/edtech.html                    ← MỚI (P0-9)
└── templates cho english, chinese                 ← Giáo trình + thời lượng

📁 Không cần sửa (đã đúng):
├── core/data/ schema đã support blocks chuẩn
├── about/models.py (AboutPage CHOICES đã đúng)
├── admissions/ (không liên quan docx này)
└── templates/about/whymis.html (CMS-driven, chỉ edit DB)
```

### 5.3 Checklist QA

#### ✅ Content Correctness
- [ ] Mọi tên hệ đào tạo trên web = tên trong docx
- [ ] Chuẩn đầu ra (IELTS/HSK/CEFR/Cambridge) khớp 100% Table 16
- [ ] Giáo trình tiêu biểu khớp Table 14, 15
- [ ] Thời lượng (tiết/tuần) khớp Table 16
- [ ] 6 nền tảng EdTech (Azota, iCorrect, VR/AR, Nexta, GenAI, Lập trình) đầy đủ
- [ ] Đối tác: Jaxtina English, Tiếng Trung Quốc tế Thời đại
- [ ] Không có nội dung "nói quá" so với docx
- [ ] Tất cả NEED_CONFIRM đã được đánh dấu rõ hoặc resolve

#### ✅ Responsive & UI
- [ ] Desktop (1440px+): bảng hiển thị đúng cột
- [ ] Tablet (768px - 1024px): grid responsive
- [ ] Mobile (375px): readable, không overflow
- [ ] Dark mode: contrast đủ

#### ✅ Navigation & Links
- [ ] Menu navbar liệt kê đúng hệ đào tạo
- [ ] Breadcrumb đường dẫn không gãy
- [ ] CTA buttons link đúng
- [ ] Footer links cập nhật

#### ✅ SEO
- [ ] `<title>` cập nhật 2026-2027
- [ ] `<meta description>` khớp nội dung docx
- [ ] `<h1>` duy nhất per page
- [ ] Sitemap cập nhật trang EdTech mới

#### ✅ Technical
- [ ] No broken migrations
- [ ] JSON load không lỗi (encoding, structure)
- [ ] NEED_CONFIRM values highlighted, không published như fact
- [ ] Existing URLs không bị redirect loop

### 5.4 Quy trình duyệt nội dung

```
┌─────────────┐    ┌──────────────┐    ┌──────────────┐    ┌───────────┐
│ Content team │───▶│ JSON/DB edit │───▶│ Dev review   │───▶│ Staging   │
│ (docx xác   │    │ (PR trên Git)│    │ (code + text)│    │ QA check  │
│  nhận)       │    └──────────────┘    └──────────────┘    └─────┬─────┘
└─────────────┘                                                   │
                    ┌──────────────┐    ┌──────────────┐         │
                    │ Production   │◀───│ Content Lead │◀────────┘
                    │ Deploy       │    │ Approve      │
                    └──────────────┘    └──────────────┘
```

### 5.5 Timeline ước tính (10-15 ngày dev)

| Tuần | Epic | Phạm vi | Milestone |
|------|------|---------|-----------|
| W1 (D1-D5) | EPIC 1 + EPIC 2 | JSON mở rộng + Model + Backend | ✅ All data correctness P0 resolved |
| W2 (D6-D10) | EPIC 3 | Templates + Frontend | ✅ All pages render đúng nội dung mới |
| W3 (D11-D13) | EPIC 4 | QA + Content review | ✅ Sign-off from Content Lead |
| W3 (D14-D15) | Deploy | Staging → Production | ✅ Live |

### 5.6 Rủi ro & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| Restructure 5→3 hệ đào tạo gây mất dữ liệu DB | **High** | Không xóa model, thêm `system_group` field, giữ backward compat |
| NEED_CONFIRM items chưa resolve khi deploy | **Med** | CI script check, chặn deploy nếu còn NEED_CONFIRM |
| JSON file lớn khó maintain | **Low** | Tách thành multi-file per block nếu > 1000 dòng |
| Content team edit nhầm năm cũ | **Low** | Lock file 2025-2026 (read-only) |
| SEO ranking giảm do đổi URL | **Med** | Giữ nguyên URLs, chỉ đổi content; redirect nếu cần |

---

> **Tóm tắt:** Website MIS đã có cơ sở kiến trúc tốt (JSON data file + AboutSection CMS + TrainingProgram models). Sai lệch chính là **cấu trúc 5 hệ vs 3 hệ** trong docx, **thiếu chi tiết giáo trình/thời lượng/chuẩn đầu ra theo cấp**, và **chưa có trang EdTech chính thức**. Giải pháp ưu tiên: mở rộng JSON data file hiện tại + thêm nhóm logic cho hệ đào tạo, không cần rebuild từ đầu.
