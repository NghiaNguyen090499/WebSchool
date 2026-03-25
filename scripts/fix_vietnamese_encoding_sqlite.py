import argparse
import sqlite3
import sys


VIET_CHARS = (
    "àáảãạâầấẩẫậăằắẳẵặ"
    "èéẻẽẹêềếểễệ"
    "ìíỉĩị"
    "òóỏõọôồốổỗộơờớởỡợ"
    "ùúủũụưừứửữự"
    "ỳýỷỹỵ"
    "đ"
    "ÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶ"
    "ÈÉẺẼẸÊỀẾỂỄỆ"
    "ÌÍỈĨỊ"
    "ÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢ"
    "ÙÚỦŨỤƯỪỨỬỮỰ"
    "ỲÝỶỸỴ"
    "Đ"
)


def count_viet_chars(text: str) -> int:
    return sum(1 for ch in text if ch in VIET_CHARS)


def count_question_marks(text: str) -> int:
    return text.count("?")


def is_mojibake(text: str) -> bool:
    patterns = ("Ã", "Â", "Ä", "Æ", "á»", "ª", "º")
    return any(p in text for p in patterns)


def score(text: str) -> int:
    return count_viet_chars(text) * 2 - count_question_marks(text)


def fix_text(text: str):
    if not text or not is_mojibake(text):
        return None
    candidates = []
    for enc in ("latin1", "cp1252"):
        try:
            candidate = text.encode(enc, errors="ignore").decode("utf-8", errors="ignore")
            candidates.append(candidate)
        except Exception:
            continue
    if not candidates:
        return None
    best = max(candidates, key=score)
    if score(best) > score(text) and count_question_marks(best) <= count_question_marks(text):
        return best
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="db.sqlite3")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    tables = {
        "core_heroslide": [
            "title",
            "title_highlight",
            "subtitle",
            "slogan",
            "description",
            "badge_text",
        ],
        "about_aboutsection": [
            "eyebrow",
            "title",
            "subtitle",
            "content",
            "highlight_text",
            "stat_number",
            "stat_label",
            "cta_text",
            "cta_secondary_text",
        ],
        "core_statistic": ["label"],
        "about_aboutpdfdocument": ["title", "subtitle"],
    }

    updates = 0
    for table, cols in tables.items():
        col_expr = ", ".join([f'"{c}"' for c in cols])
        cur.execute(f"SELECT rowid, {col_expr} FROM {table}")
        rows = cur.fetchall()
        for row in rows:
            for col in cols:
                value = row[col]
                if not value or not isinstance(value, str):
                    continue
                fixed = fix_text(value)
                if fixed and fixed != value:
                    before = value[:80].replace("\n", " ")
                    after = fixed[:80].replace("\n", " ")
                    print(f"{table}.{col} rowid={row['rowid']} | {before} -> {after}")
                    if args.apply:
                        cur.execute(
                            f'UPDATE {table} SET "{col}"=? WHERE rowid=?',
                            (fixed, row["rowid"]),
                        )
                        updates += 1

    if args.apply:
        conn.commit()
    conn.close()
    print(f"Done. Updated rows: {updates}" if args.apply else "Dry run complete.")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
