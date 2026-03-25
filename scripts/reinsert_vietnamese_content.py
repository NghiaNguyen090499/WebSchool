import sqlite3
import sys

sys.stdout.reconfigure(encoding="utf-8")

CAM_KET = (
    "Học thật: học sinh hiểu bản chất và biết vận dụng, không học vẹt.\n"
    "Chất lượng thật: kết quả đo được qua tiến bộ từng kỳ và chuẩn đầu ra rõ ràng.\n"
    "Tiến bộ thật: mỗi học sinh có lộ trình cá nhân hóa, được theo dõi bằng dữ liệu.\n"
    "Cam kết minh bạch với phụ huynh qua mục tiêu và báo cáo định kỳ."
)

FUTURE_AI = (
    "Future with AI là định hướng tích hợp AI và dữ liệu vào mọi môn học.\n"
    "Học sinh rèn tư duy số, biết dùng AI đúng cách và có đạo đức số.\n"
    "Giáo viên dùng AI để cá nhân hóa học tập và theo dõi tiến bộ.\n"
    "Mục tiêu là năng lực học tập suốt đời, không chỉ điểm số."
)

VISION_PILLARS = {
    0: "Foreign Languages: thành thạo Anh–Trung, giao tiếp học thuật, tư duy đa văn hóa",
    1: "Heart: phát triển nhân cách, GRACE, bền vững cảm xúc & đạo đức",
    2: "AI: năng lực dữ liệu, công nghệ, ứng dụng AI an toàn trong học tập",
}

MATH_SUMMARY = (
    "Mục tiêu: phát triển tư duy logic và năng lực công dân số.\n"
    "Phương pháp: Smart Math tích hợp AI, trực quan hóa qua GeoGebra/Desmos, học qua mô phỏng và dự án.\n"
    "Đầu ra: học sinh hiểu bản chất, vận dụng Toán vào thực tiễn."
)

MATH_DEEPSEEK = (
    "DeepSeek dùng để giải thích đa bước, phân tích lỗi sai, gợi ý cách giải.\n"
    "Giáo viên kiểm soát ngữ cảnh.\n"
    "Học sinh phải giải thích lại bằng lời.\n"
    "Không lệ thuộc công cụ."
)

LIT_SUMMARY = (
    "Mục tiêu: bồi dưỡng tư duy phản biện, năng lực ngôn ngữ và cảm thụ văn học.\n"
    "Phương pháp: kết hợp đọc – viết – thảo luận, ứng dụng AI để tối ưu dàn ý và phân tích ngôn ngữ.\n"
    "Đầu ra: học sinh biết trình bày quan điểm, tạo sản phẩm nội dung số và giữ chuẩn mực đạo đức số."
)

ENG_SUMMARY = (
    "Mục tiêu: thành thạo tiếng Anh học thuật và giao tiếp tự tin.\n"
    "Phương pháp: immersion, chuẩn Cambridge, tăng cường thực hành với giáo viên chuyên môn.\n"
    "Đầu ra: đạt chuẩn đầu ra phù hợp từng cấp, sẵn sàng IELTS/ứng dụng học tập quốc tế."
)

LEVEL_CONTENT = {
    "preschool": (
        1,
        "Mục tiêu: phát triển toàn diện thể chất, trí tuệ, cảm xúc và nền nếp tự lập.\n"
        "Phương pháp: Hands on learning, chơi – học, trải nghiệm đa giác quan; song ngữ cân bằng.\n"
        "Đầu ra: trẻ tự tin giao tiếp, biết hợp tác, hình thành thói quen học tập tích cực.\n\n"
        "• Ngôn ngữ và giao tiếp\n"
        "• Tư duy logic\n"
        "• Kỹ năng tự lập\n"
        "• Cảm xúc – xã hội"
    ),
    "primary": (
        1,
        "Mục tiêu: nền tảng kiến thức vững, năng lực số và tư duy phản biện.\n"
        "Phương pháp: bám chuẩn Bộ GD&ĐT, tích hợp STEM/STEAM, học qua dự án.\n"
        "Đầu ra: học sinh đọc – viết – toán vững, giao tiếp tiếng Anh cơ bản, tự tin khám phá.\n\n"
        "• Rèn luyện tư duy phản biện và sáng tạo\n"
        "• Phát triển năng lực số và công nghệ\n"
        "• Tăng cường kỹ năng học tập"
    ),
    "middle": (
        1,
        "Mục tiêu: định hình tư duy, định hướng nghề nghiệp, phát triển kỹ năng sống.\n"
        "Phương pháp: học qua trải nghiệm kết hợp STEAM, dự án liên môn, câu lạc bộ học thuật.\n"
        "Đầu ra: biết tự học, làm việc nhóm, có định hướng năng lực và lộ trình chứng chỉ.\n\n"
        "• Tăng cường giáo dục định hướng nghề nghiệp\n"
        "• Phát triển kỹ năng sống và giá trị sống\n"
        "• Rèn luyện tư duy phản biện"
    ),
    "high": (
        1,
        "Mục tiêu: bứt phá học thuật và năng lực nghề nghiệp, chuẩn bị đại học/du học.\n"
        "Phương pháp: lộ trình phân hóa (Công nghệ quốc tế/HSK5+/tài năng), hướng nghiệp thực tế.\n"
        "Đầu ra: hồ sơ học thuật rõ ràng, chứng chỉ IELTS/HSK phù hợp, năng lực số sẵn sàng.\n\n"
        "• Công nghệ quốc tế: liên kết Aptech, chứng chỉ toàn cầu\n"
        "• HSK5+: tăng cường năng lực tiếng Trung\n"
        "• Tài năng Toán học & Tiếng Anh"
    ),
}


def main():
    conn = sqlite3.connect("db.sqlite3")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # core_heroslide
    cur.execute("SELECT id FROM core_heroslide ORDER BY id LIMIT 1")
    row = cur.fetchone()
    if row:
        slide_id = row["id"]
        description = CAM_KET + "\n\n" + FUTURE_AI
        cur.execute(
            "UPDATE core_heroslide SET slogan=?, subtitle=?, description=? WHERE id=?",
            (
                "Học thật – Chất lượng thật – Tiến bộ thật",
                "Future with AI là định hướng tích hợp AI và dữ liệu vào mọi môn học.",
                description,
                slide_id,
            ),
        )

    # mission section order=0
    cur.execute("SELECT id FROM about_aboutpage WHERE page_type='mission'")
    mission = cur.fetchone()
    if mission:
        cur.execute(
            "SELECT id FROM about_aboutsection WHERE page_id=? AND `order`=0",
            (mission["id"],),
        )
        sec = cur.fetchone()
        if sec:
            cur.execute(
                "UPDATE about_aboutsection SET content=? WHERE id=?",
                (CAM_KET, sec["id"]),
            )

    # vision sections order 0-2
    cur.execute("SELECT id FROM about_aboutpage WHERE page_type='vision'")
    vision = cur.fetchone()
    if vision:
        cur.execute(
            "SELECT id, `order` FROM about_aboutsection WHERE page_id=? ORDER BY `order`",
            (vision["id"],),
        )
        for sec in cur.fetchall():
            if sec["order"] in VISION_PILLARS:
                cur.execute(
                    "UPDATE about_aboutsection SET content=? WHERE id=?",
                    (VISION_PILLARS[sec["order"]], sec["id"]),
                )

    # overview_math sections
    cur.execute("SELECT id FROM about_aboutpage WHERE page_type='overview_math'")
    math = cur.fetchone()
    if math:
        cur.execute(
            "SELECT id, `order` FROM about_aboutsection WHERE page_id=? ORDER BY `order`",
            (math["id"],),
        )
        rows = cur.fetchall()
        if len(rows) >= 1:
            cur.execute(
                "UPDATE about_aboutsection SET title=?, content=? WHERE id=?",
                ("Tóm tắt chương trình Smart Math", MATH_SUMMARY, rows[0]["id"]),
            )
        if len(rows) >= 2:
            cur.execute(
                "UPDATE about_aboutsection SET title=?, content=? WHERE id=?",
                ("Smart Math – DeepSeek", MATH_DEEPSEEK, rows[1]["id"]),
            )

    # overview_literature sections
    cur.execute("SELECT id FROM about_aboutpage WHERE page_type='overview_literature'")
    lit = cur.fetchone()
    if lit:
        cur.execute(
            "SELECT id, `order` FROM about_aboutsection WHERE page_id=? ORDER BY `order`",
            (lit["id"],),
        )
        rows = cur.fetchall()
        if len(rows) >= 1:
            cur.execute(
                "UPDATE about_aboutsection SET title=?, content=? WHERE id=?",
                ("Tóm tắt chương trình Ngữ văn thế hệ mới", LIT_SUMMARY, rows[0]["id"]),
            )
        if len(rows) >= 2:
            cur.execute(
                "UPDATE about_aboutsection SET title=?, content=? WHERE id=?",
                ("Trụ cột nội dung", "Phản biện – Sáng tạo nội dung số – Đạo đức số.", rows[1]["id"]),
            )

    # overview_english section (order 0)
    cur.execute("SELECT id FROM about_aboutpage WHERE page_type='overview_english'")
    eng = cur.fetchone()
    if eng:
        cur.execute(
            "SELECT id FROM about_aboutsection WHERE page_id=? ORDER BY `order` LIMIT 1",
            (eng["id"],),
        )
        sec = cur.fetchone()
        if sec:
            cur.execute(
                "UPDATE about_aboutsection SET eyebrow=?, title=?, content=? WHERE id=?",
                ("Tổng quan", "Tóm tắt chương trình Tiếng Anh", ENG_SUMMARY, sec["id"]),
            )

    # academics levels (order 1)
    for ptype, (order_target, content) in LEVEL_CONTENT.items():
        cur.execute("SELECT id FROM about_aboutpage WHERE page_type=?", (ptype,))
        page = cur.fetchone()
        if not page:
            continue
        cur.execute(
            "SELECT id FROM about_aboutsection WHERE page_id=? AND `order`=?",
            (page["id"], order_target),
        )
        sec = cur.fetchone()
        if sec:
            cur.execute(
                "UPDATE about_aboutsection SET content=? WHERE id=?",
                (content, sec["id"]),
            )

    # core_statistic label (id=13)
    cur.execute(
        "UPDATE core_statistic SET label=? WHERE id=?",
        ("Diện tích campus (m²)", 13),
    )

    # about_aboutpdfdocument subtitle
    cur.execute(
        "UPDATE about_aboutpdfdocument SET subtitle=?",
        ("Tài liệu chương trình (PDF)",),
    )

    conn.commit()
    conn.close()
    print("Reinserted correct Vietnamese content.")


if __name__ == "__main__":
    main()
