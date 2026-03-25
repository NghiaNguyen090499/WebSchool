"""EPIC 1 — Expand program_content_2026_2027.json with docx data."""
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

JSON_PATH = r"d:\NGHIA\WebsiteSchool\core\data\program_content_2026_2027.json"

with open(JSON_PATH, encoding="utf-8") as f:
    data = json.load(f)

# ── T1: training_systems (Table 16) ──
data["training_systems"] = [
    {
        "key": "steam",
        "title": "Hệ STEAM Chuẩn / CLC",
        "icon": "fas fa-cogs",
        "description": "Chương trình STEAM theo chuẩn Bộ GD&ĐT, tích hợp công nghệ AI vào giảng dạy.",
        "levels": {
            "tieu_hoc": {"english_hours": "7-9", "chinese_hours": "1-2",
                         "english_target": "Cambridge Movers / CEFR Pre A2",
                         "chinese_target": "Chắc phát âm, giao tiếp cơ bản"},
            "thcs": {"english_hours": "6-7", "chinese_hours": "2",
                     "english_target": "CEFR A2+ / B1",
                     "chinese_target": "YCT2-3 (HSK1-2)"},
            "thpt": {"english_hours": "6-7", "chinese_hours": "3",
                     "english_target": "IELTS 4.0-6.0+ / CEFR B1-B2",
                     "chinese_target": "HSK 2-4"},
        },
    },
    {
        "key": "math_tech",
        "title": "Hệ Tài năng Toán – Công nghệ mới",
        "icon": "fas fa-calculator",
        "description": "Chương trình mũi nhọn bồi dưỡng học sinh năng lực vượt trội về Toán và STEM.",
        "levels": {
            "tieu_hoc": {"english_hours": "11", "chinese_hours": "1-2",
                         "english_target": "Cambridge Movers / CEFR Pre A2",
                         "chinese_target": "Chắc phát âm, giao tiếp cơ bản"},
            "thcs": {"english_hours": "8", "chinese_hours": "2",
                     "english_target": "CEFR A2+ / B1",
                     "chinese_target": "YCT2-3 (HSK1-2)"},
            "thpt": {"english_hours": "7", "chinese_hours": "3",
                     "english_target": "IELTS 4.0-6.0+ / CEFR B1-B2",
                     "chinese_target": "HSK 2-4"},
        },
    },
    {
        "key": "language",
        "title": "Hệ Tài năng Ngôn ngữ",
        "icon": "fas fa-globe",
        "description": "Chương trình mũi nhọn đào tạo song hành Tiếng Anh (IELTS) và Tiếng Trung (HSK).",
        "sub_tracks": ["Tiếng Anh tài năng", "Tiếng Trung tài năng"],
        "levels": {
            "tieu_hoc": {"english_hours": "14", "chinese_hours": "1-3",
                         "english_target": "Cambridge Flyers / KET / PET / CEFR A2+",
                         "chinese_target": "YCT 1-3 (HSK1-2)"},
            "thcs": {"english_hours": "10", "chinese_hours": "5",
                     "english_target": "IELTS 4.0-6.0+ / CEFR B1-B2",
                     "chinese_target": "YCT4 (HSK3-4)"},
            "thpt": {"english_hours": "10", "chinese_hours": "5-8",
                     "english_target": "IELTS 6.5-8.0+ / CEFR B2-C1",
                     "chinese_target": "HSK 4-6"},
        },
        "privileges": [
            "Cường độ tiếp xúc tối đa: 10-18 tiết ngoại ngữ/tuần.",
            "Hệ sinh thái Giáo viên Bản ngữ & AI: tương tác trực tiếp + trợ lý ảo 24/7.",
            "Hệ thống giáo trình May đo: IELTS Master, Focus Plus, HSK Standard Course.",
            "Học tập qua dự án (PBL): Video tranh biện, Infographic chuyên sâu.",
        ],
    },
]

# ── T2: curriculum (Tables 14, 15) ──
data["blocks"]["overview_english"]["curriculum"] = {
    "tieu_hoc": {
        "textbooks": ["Super Minds", "Phonics", "Cambridge YLE Test",
                       "Cambridge Primary Science", "Cambridge Primary Maths",
                       "Grammar", "MIS Extra Practice"],
        "target": "CEFR PreA2 / A2",
    },
    "thcs": {
        "textbooks": ["Global Success", "Speak Now", "Macmillan Science",
                       "Pre-IELTS", "MIS supplementary exercises"],
        "target": "CEFR A2+ / B1",
    },
    "thpt": {
        "textbooks": ["Global Success", "Speak Now", "Reading Explorer",
                       "Pre-IELTS", "Complete IELTS", "IELTS Focus Plus",
                       "MIS supplementary exercises"],
        "target": "CEFR B1 / C1",
    },
}

data["blocks"]["overview_chinese"]["curriculum"] = {
    "tieu_hoc": {
        "textbooks": ["YCT Standard Course 1-3", "Thẻ học từ vựng & AI Doubao"],
        "target": "YCT 1-3 / Giao tiếp tình huống",
    },
    "thcs": {
        "textbooks": ["HSK Standard Course 1-3 (3.0)", "Tiếng Trung nhập môn",
                       "Tiếng Trung tiêu chuẩn", "Chuyên đề luyện thi"],
        "target": "HSK 1-3 (YCT 3-4) / Đọc hiểu & thảo luận",
    },
    "thpt": {
        "textbooks": ["HSK Standard Course 4-6 (3.0)", "Tiếng Trung nhập môn",
                       "Tiếng Trung tổng hợp", "Chuyên đề luyện thi"],
        "target": "HSK 4-6 / Học thuật & du học",
    },
}

# ── T3: sample_lesson (Tables 1, 4, 7) ──
data["blocks"]["math"]["sample_lesson"] = {
    "tieu_hoc": {
        "duration": "35 phút",
        "steps": [
            {"time": "5 phút", "activity": "Khởi động – Đặt vấn đề qua trò chơi", "tool": "Gamification"},
            {"time": "10 phút", "activity": "Hình thành kiến thức", "tool": "AI mô phỏng trực quan"},
            {"time": "15 phút", "activity": "Luyện tập cá nhân/nhóm", "tool": "AI Virtual Tutor"},
            {"time": "5 phút", "activity": "Giao bài & Tổng kết", "tool": "AI sơ đồ tư duy & bài tập cá nhân hóa"},
        ],
    },
    "thcs": {
        "duration": "40 phút",
        "steps": [
            {"time": "5 phút", "activity": "Khởi động – Đặt vấn đề thực tế", "tool": "AI tóm tắt và mô hình hóa"},
            {"time": "10 phút", "activity": "Hình thành kiến thức", "tool": "AI mô phỏng (khử Gauss, đồ thị động)"},
            {"time": "15 phút", "activity": "Luyện tập", "tool": "AI Virtual Tutor"},
            {"time": "5 phút", "activity": "Củng cố & Mở rộng liên môn", "tool": "AI tạo bài toán Vật lý/Kinh tế"},
            {"time": "5 phút", "activity": "Giao bài", "tool": "AI sơ đồ tư duy & bài tập cá nhân hóa"},
        ],
    },
    "thpt": {
        "duration": "40 phút",
        "steps": [
            {"time": "5 phút", "activity": "Khởi động", "tool": "AI tóm tắt, chuyển sang mô hình toán học"},
            {"time": "10 phút", "activity": "Hình thành kiến thức", "tool": "AI mô phỏng trực quan"},
            {"time": "15 phút", "activity": "Luyện tập", "tool": "AI Virtual Tutor"},
            {"time": "10 phút", "activity": "Giao bài & Tổng kết", "tool": "AI sơ đồ tư duy & bài tập cá nhân hóa"},
        ],
    },
}

# ── T4: Detailed per-grade targets (Tables 2, 5, 8) ──
data["blocks"]["math"]["grade_roadmap"] = {
    "K1": {"focus": "Số học: Nhận diện số, phép tính phạm vi 100. Hình phẳng đơn giản.",
            "ai_tools": "Nexta Tablet, Scratch Junior, Gamification",
            "output": "Làm quen thao tác toán học trên thiết bị số."},
    "K2": {"focus": "Phép nhân, chia cơ bản. Đo lường: Thời gian, độ dài.",
            "ai_tools": "Nexta Tablet, AI Voice",
            "output": "Mô hình hóa toán học vào tình huống thực tế."},
    "K3": {"focus": "Số 4-5 chữ số. Chu vi, diện tích hình vuông/chữ nhật.",
            "ai_tools": "Scratch, GeoGebra cơ bản, DeepSeek Math",
            "output": "Tư duy thuật toán: dùng lập trình giải bài toán logic."},
    "K4": {"focus": "Phân số, TBC. Góc, đường thẳng, diện tích hình bình hành.",
            "ai_tools": "ChatGPT, Gemini, GeoGebra AI, PhET Interactive",
            "output": "CEO bộ óc: biết Prompt AI tìm cách giải đa dạng."},
    "K5": {"focus": "Số thập phân, tỉ số %. Hình hộp, hình lập phương, hình trụ.",
            "ai_tools": "Excel AI, Canva AI, Azota AI",
            "output": "Xử lý dữ liệu thực tế, hoàn thiện Portfolio."},
    "K6": {"focus": "Tập hợp số tự nhiên, Chia hết, Số nguyên, Phân số & Số thập phân, Hình học phẳng & Đối xứng.",
            "ai_tools": "DeepSeek Math, Math AI, GeoGebra AI, Scratch",
            "output": "Thành thạo phép toán cơ bản. Sổ tay toán học & Sơ đồ tư duy."},
    "K7": {"focus": "Số hữu tỉ, Số thực, Tỉ lệ thức, Đa thức một biến, Tam giác, Hình khối 3D.",
            "ai_tools": "Excel AI Simulations, Python căn bản",
            "output": "Làm chủ đa thức & tỉ lệ thức. Infographic ứng dụng thực tế."},
    "K8": {"focus": "Đa thức đa biến, Hằng đẳng thức, Định lý Thales, PT bậc nhất, Xác suất thực nghiệm.",
            "ai_tools": "Monte Carlo, Wolfram Alpha, Teachable Machine",
            "output": "Bài toán kinh tế đời sống qua hàm số. Video minh họa."},
    "K9": {"focus": "Hệ PT, PT bậc hai, Căn bậc hai/ba, Đường tròn, Thống kê tần số.",
            "ai_tools": "AI Tutor, Prompt Engineering nâng cao, Python API",
            "output": "Tối ưu kỳ thi vào 10. Portfolio Toán-AI cá nhân."},
    "K10": {"focus": "Mệnh đề, Hệ PT 3 ẩn, Vectơ, Ba đường Conic, Đại số tổ hợp.",
             "ai_tools": "DeepSeek Math khử Gauss, GeoGebra AI Conic",
             "output": "Tư duy logic chặt chẽ. Sổ tay toán học lớp 10."},
    "K11": {"focus": "Hàm số lượng giác, Dãy số, Đạo hàm, Xác suất cổ điển.",
             "ai_tools": "AI mô phỏng dao động, AR/VR bóc tách khối đa diện",
             "output": "Mô hình hóa toán học. Dự báo lãi suất & tài chính."},
    "K12": {"focus": "Khảo sát hàm số, Vectơ Oxyz, Tích phân, Xác suất Bayes.",
             "ai_tools": "Pandas/Python Big Data, AI Tutor ôn thi",
             "output": "Portfolio AI & KHDL xét tuyển ĐH."},
}

# ── T5: edtech_ecosystem (Chapter 3) ──
data["blocks"]["edtech_ecosystem"] = {
    "key": "edtech_ecosystem",
    "year": "2026-2027",
    "title": "Hệ sinh thái phần mềm hỗ trợ đào tạo 4.0",
    "subtitle": "Công nghệ tiên phong – Nâng tầm tri thức",
    "intro": "Tại MIS, chúng tôi không chỉ giảng dạy về công nghệ mà còn trực tiếp ứng dụng những giải pháp EdTech hàng đầu.",
    "platforms": [
        {"key": "azota", "name": "AZOTA",
         "tagline": "Nền tảng quản lý & đánh giá giáo dục thông minh hàng đầu Việt Nam",
         "award": "Giải Vàng Made in Viet Nam 2021",
         "features": ["Hệ sinh thái số toàn diện", "Ngân hàng đề thi thông minh",
                       "Chấm phiếu tô tự động bằng AI", "Cá nhân hóa lộ trình",
                       "Kết nối Phụ huynh 24/7"]},
        {"key": "icorrect", "name": "iCorrect",
         "tagline": "Trợ lý ảo luyện nói tiếng Anh 24/7",
         "features": ["Luyện tập cá nhân hóa", "Phản hồi tức thì bằng AI",
                       "Bám sát chương trình học", "Thi mô phỏng IELTS"]},
        {"key": "vr_ar", "name": "Công nghệ VR/AR",
         "tagline": "Trải nghiệm học tập đa chiều",
         "features": ["Mô hình 3D Toán, Hình học, Robot",
                       "Trải nghiệm nhập vai: thực địa số hóa",
                       "Phòng thí nghiệm ảo an toàn",
                       "Học vui - Hiểu sâu"]},
        {"key": "nexta", "name": "Lớp học thông minh Nexta",
         "tagline": "Trợ lý cho hành trình cá nhân hóa",
         "features": ["Tương tác 1:1 thời gian thực",
                       "Học liệu số sinh động & Gamification",
                       "AI-Track phân tích điểm mạnh/yếu",
                       "Khiên chắn an toàn Internet sạch"]},
        {"key": "genai", "name": "Generative AI trong học thuật",
         "tagline": "Hỗ trợ nghiên cứu và sáng tạo",
         "features": ["Gemini, ChatGPT, DeepSeek Math, MathAI, GeoGebra AI",
                       "Canva AI & biên tập video chuyên nghiệp",
                       "Scratch (Tiểu học), Python (THCS & THPT)",
                       "Microsoft Ecosystem cộng tác trực tuyến"]},
    ],
}

# ── T6: Expand future_ai outcomes (6 items per docx) ──
data["blocks"]["future_ai"]["outcomes"] = [
    "Tư duy kiến tạo vững chắc: Làm chủ Python, tạo Website, Game, ứng dụng, Robot.",
    "Năng lực khoa học dữ liệu (Data Science): Từ thu thập đến Machine Learning.",
    "Kỹ năng AI Literacy toàn diện: Sử dụng AI như Co-pilot trong mọi môn học.",
    "Tư duy phản biện & Đạo đức số: Phát hiện Bias, Deepfake, tin giả.",
    "Tự học và tự nghiên cứu: Thành thạo Prompt Engineering nâng cao.",
    "Digital Portfolio: Bộ sưu tập dự án AI tạo lợi thế xét tuyển đại học.",
]

# ── T7: Math articulation + talent_pillars ──
data["blocks"]["math"]["articulation"] = [
    "Tiểu học (K1-K5): Khơi gợi niềm yêu thích; tư duy logic và thuật toán trực quan qua Scratch.",
    "THCS (K6-K9): Rèn chứng minh – phân tích – tổng hợp; Python căn bản và thống kê.",
    "THPT (K10-K12): Chuyên sâu Python nâng cao, AI và Khoa học dữ liệu; HSG quốc gia.",
]

data["blocks"]["math"]["talent_pillars"] = [
    {"title": "Toán học cốt lõi & Giải quyết vấn đề",
     "content": "Toán tư duy, Toán mở và Olympiad. Phát hiện và bồi dưỡng mũi nhọn."},
    {"title": "Tư duy thuật toán – Lập trình – AI",
     "content": "Từ Scratch đến Python, AI, KHDL. Tư duy mô hình hóa từ Tiểu học."},
    {"title": "Ứng dụng Toán – STEM & Định hướng nghề",
     "content": "Học qua dự án, CLB Toán-STEM-AI. Định hướng KHDL, Tài chính, Kỹ thuật."},
]

# ── T8: Literature articulation roadmap (Table 19) ──
data["blocks"]["literature"]["articulation"] = [
    {"level": "Tiểu học",
     "focus": "Khơi gợi cảm xúc: ngôn ngữ kể chuyện, thơ ca, kịch nghệ.",
     "output": "Podcast kể chuyện; Sách tranh tự sáng tác (AI minh họa)."},
    {"level": "THCS",
     "focus": "Tư duy hệ thống: thành thạo các dạng văn, phân tích tâm lý nhân vật.",
     "output": "Tạp chí nội bộ; Kịch bản video ngắn; Tranh biện nhân văn."},
    {"level": "THPT",
     "focus": "Kiến tạo bản sắc: viết luận chuyên sâu, phê bình văn học so sánh.",
     "output": "Dự án nghiên cứu văn hóa. Điểm cao kỳ thi Tốt nghiệp & ĐH."},
]

# ── Navigation: restructure to 3 systems ──
data["navigation"]["specialized_programs"] = [
    {"key": "steam", "title": "Hệ STEAM Chuẩn / CLC",
     "icon": "fas fa-cogs", "url_name": "about:steam"},
    {"key": "math_tech", "title": "Hệ Tài năng Toán – Công nghệ mới",
     "icon": "fas fa-calculator", "url_name": "about:overview_math"},
    {"key": "language", "title": "Hệ Tài năng Ngôn ngữ",
     "icon": "fas fa-globe", "url_name": "about:overview_english",
     "sub_items": [
         {"key": "english_talent", "title": "Tiếng Anh tài năng",
          "icon": "fas fa-language", "url_name": "about:overview_english"},
         {"key": "chinese_talent", "title": "Tiếng Trung tài năng",
          "icon": "fas fa-yen-sign", "url_name": "about:overview_chinese"},
     ]},
]

# ── Update version ──
data["version"] = "2026.2"

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

ts_count = len(data.get("training_systems", []))
blocks = list(data.get("blocks", {}).keys())
print(f"JSON updated successfully! Version: {data['version']}")
print(f"training_systems: {ts_count} systems")
print(f"blocks: {blocks}")
print(f"grade_roadmap grades: {list(data['blocks']['math']['grade_roadmap'].keys())}")
print(f"edtech platforms: {len(data['blocks']['edtech_ecosystem']['platforms'])}")
