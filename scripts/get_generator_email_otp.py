#!/usr/bin/env python3
"""
Fetch an OTP code from a generator.email inbox page.

Usage:
  python scripts/get_generator_email_otp.py
  python scripts/get_generator_email_otp.py --url "https://generator.email/your@domain"
"""
from __future__ import annotations

import argparse
import re
import sys
from html import unescape

import requests


DEFAULT_URL = "https://generator.email/ayofuc@nqe.sgbteam.co"
PATTERNS = [
    re.compile(r"Your\s+ChatGPT\s+code\s+is\s+([0-9]{4,8})", re.IGNORECASE),
    re.compile(r"verification\s+code[^0-9]{0,20}([0-9]{4,8})", re.IGNORECASE),
    re.compile(r"\bOTP\b[^0-9]{0,20}([0-9]{4,8})", re.IGNORECASE),
    re.compile(r"\bcode\b[^0-9]{0,20}([0-9]{4,8})", re.IGNORECASE),
]


def extract_code(text: str) -> str | None:
    if not text:
        return None
    for pattern in PATTERNS:
        match = pattern.search(text)
        if match:
            return match.group(1)
    return None


def fetch_html(url: str, timeout: int) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; OTPFetcher/1.0)",
        "Accept": "text/html,application/xhtml+xml",
    }
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response.text


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch OTP code from generator.email inbox page.")
    parser.add_argument("--url", default=DEFAULT_URL, help="Inbox URL to fetch.")
    parser.add_argument("--timeout", type=int, default=15, help="Request timeout in seconds.")
    args = parser.parse_args()

    try:
        html = fetch_html(args.url, args.timeout)
    except requests.RequestException as exc:
        print(f"[error] Failed to fetch inbox: {exc}", file=sys.stderr)
        return 1

    title_match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if title_match:
        title_text = unescape(title_match.group(1))
        title_text = re.sub(r"\s+", " ", title_text).strip()
        code = extract_code(title_text)
        if code:
            print(code)
            return 0

    code = extract_code(html)
    if code:
        print(code)
        return 0

    print("[error] OTP code not found in inbox page.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
