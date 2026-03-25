# Overnight Worklog (MIS Website)

Start: 2026-02-02 (local)
Goal: Optimize frontend/backend/db per checklist (security/chatbot excluded).

## A) Baseline Quick Checks
- Command: `python manage.py check`
  Result: PASS (System check identified no issues)
- Command: `python manage.py makemigrations --check --dry-run`
  Result: PASS (No changes detected)
- Command: `python manage.py showmigrations --plan`
  Result: PASS (All applied)
- Command: `python manage.py collectstatic --noinput`
  Result: PASS (0 copied, 236 unmodified)
- Smoke (runserver + curl):
  - `/` -> FAIL (500)
  - `/sitemap.xml` -> FAIL (500)
  - `/robots.txt` -> FAIL (500)

Notes: runserver started/stopped for baseline. Errors expected before fixes.

---

## B) ?? GO-LIVE FIXES (1-3)

### B1) Fix sitemap.xml l?i FieldError/NoReverseMatch (sitemaps.py)
1) V?n d? (trích report): "Fix sitemap.xml l?i FieldError/NoReverseMatch (sitemaps.py)"
2) File ch?nh: `core/sitemaps.py`, `school_website/settings.py`
3) Thay d?i:
   - Lo?i b? filter `is_published`/`is_published` không t?n t?i.
   - Ch? l?y b?n ghi có slug h?p l?.
   - C?p nh?t danh sách URL about cho dúng tên route th?c t?.
   - Thêm `django.contrib.sitemaps` vào `INSTALLED_APPS` d? có template sitemap m?c d?nh.
4) L?nh test/smoke: runserver + curl `/sitemap.xml`
5) K?t qu?: FAIL (500 do l?i sitemap template tru?c khi thêm app; c?n re-test sau B2/B3)

### B2) Thêm robots.txt (thi?u)
1) V?n d? (trích report): "Thêm robots.txt (thi?u)"
2) File ch?nh: `templates/robots.txt`
3) Thay d?i:
   - Thêm robots v?i Disallow `/admin/`, `/portal/` và tr? Sitemap.
4) L?nh test/smoke: runserver + curl `/robots.txt`
5) K?t qu?: FAIL (curl batch b? d?ng b?i 500 t? sitemap; c?n re-test riêng)

### B3) S?a CTA Student Spotlight tr? sai POST endpoint
1) V?n d? (trích report): "S?a CTA Student Spotlight tr? sai POST endpoint"
2) File ch?nh: `templates/core/student_spotlight_list.html`
3) Thay d?i:
   - Ð?i CTA t? `admissions:submit` -> `admissions:list`.
4) Lenh test/smoke: `python manage.py test core.tests.StudentSpotlightCtaTests`
5) Ket qua: PASS (CTA -> /tuyen-sinh/, no submit action)

---

## Quick Checks (sau 3 m?c B1-B3)
- `python manage.py check` -> PASS
- `python manage.py makemigrations --check --dry-run` -> PASS
- `python manage.py showmigrations --plan` -> PASS
- `python manage.py collectstatic --noinput` -> PASS
- Smoke (runserver + curl): FAIL (500 do sitemap; c?n re-test sau khi hoàn t?t fix)

---

## C) ?? Backend Functional + Data Correctness (1-3)

### C1) News search q chua implement
1) V?n d? (trích report): "News search q chua implement"
2) File ch?nh: `news/views.py`
3) Thay d?i:
   - Thêm query param `q` (icontains title/content/excerpt).
   - Gi? category filter + pagination.
4) L?nh test/smoke: `/news/?q=test`
5) K?t qu?: PASS (200)

### C2) download_count tài li?u tuy?n sinh không tang
1) V?n d? (trích report): "download_count tài li?u tuy?n sinh không tang"
2) File ch?nh: `admissions/views.py`, `admissions/urls.py`, `templates/admissions/admission_detail.html`
3) Thay d?i:
   - Thêm view `download_document` tang `download_count` b?ng F().
   - Thêm route `/tuyen-sinh/documents/<id>/download/`.
   - Update link download di qua view m?i.
4) Lenh test/smoke: `python manage.py test` (AdmissionDownloadTests)
5) Ket qua: PASS (download_count increments)

### C3) Portal: export CSV registrations
1) V?n d? (trích report): "Portal: export CSV registrations (n?u có th?i gian)"
2) File ch?nh: `portal/views.py`, `portal/urls.py`, `templates/portal/admissions/registrations_list.html`
3) Thay d?i:
   - Thêm export CSV v?i filter q/status/level.
   - Thêm nút Xu?t CSV trong toolbar.
4) Lenh test/smoke: `python manage.py test portal.tests.PortalAdmissionsExportTests`
5) Ket qua: PASS (200 + CSV header)

---

## Quick Checks (sau 3 m?c C1-C3)
- `python manage.py check` -> PASS
- `python manage.py makemigrations --check --dry-run` -> PASS
- `python manage.py showmigrations --plan` -> PASS
- `python manage.py collectstatic --noinput` -> PASS
- Smoke (runserver + curl):
  - `/` -> 200
  - `/sitemap.xml` -> 200
  - `/robots.txt` -> 200
  - `/news/?q=test` -> 200

---

## D) ?? Performance / N+1 / Pagination

### D1) Gallery list N+1 album.photos.count
1) V?n d? (trích report): "Gallery list N+1 album.photos.count"
2) File ch?nh: `gallery/views.py`, `templates/gallery/list.html`
3) Thay d?i:
   - Annotate `photo_count=Count('photos')`.
   - Template dùng `album.photo_count`.
4) L?nh test/smoke: `/gallery/`
5) K?t qu?: PASS (200)

### D2) Trang ch? nhi?u query (news/categories/events/menus/sections)
1) V?n d? (trích report): "Trang ch? nhi?u query (news/categories/events/menus/sections)"
2) File ch?nh: `core/views.py`
3) Thay d?i:
   - G?p query news theo category tabs (1 query + grouping).
   - `select_related('category')` cho featured/recent news.
4) L?nh test/smoke: `/` 
5) K?t qu?: PASS (200)

### D3) Events list không pagination
1) V?n d? (trích report): "Events list không pagination"
2) File ch?nh: `events/views.py`, `templates/events/list.html`
3) Thay d?i:
   - Paginate past events (page param `?page=`) + UI pagination.
4) L?nh test/smoke: `/events/?page=2`
5) K?t qu?: PASS (200)

---

## Quick Checks (sau 3 m?c D1-D3)
- `python manage.py check` -> PASS
- `python manage.py makemigrations --check --dry-run` -> PASS
- `python manage.py showmigrations --plan` -> PASS
- `python manage.py collectstatic --noinput` -> PASS
- Smoke (runserver + curl):
  - `/` -> 200
  - `/gallery/` -> 200
  - `/events/?page=2` -> 200
  - `/doi-ngu/?page=2` -> 200

---

### D4) Staff list không pagination
1) V?n d? (trích report): "Staff list không pagination"
2) File ch?nh: `staff/views.py`, `staff/templates/staff/list.html`
3) Thay d?i:
   - Thêm Paginator (12/item) + UI pagination (gi? filter role).
4) L?nh test/smoke: `/doi-ngu/?page=2`
5) K?t qu?: PASS (200)

---

## E) UI/UX Frontend

### E1) Admissions detail: l?i hi?n th? b?ng alert
1) V?n d? (trích report): "Admissions detail: l?i hi?n th? b?ng alert"
2) File chinh: `templates/admissions/admission_detail.html`, `templates/core/includes/footer.html`
3) Thay d?i:
   - Thay alert b?ng formError inline + l?i required theo t?ng field.
   - Loai bo alert() trong form tu van footer, thay bang formError inline.
   - Gi? loading state, reset l?i khi success.
4) Lenh test/smoke: `python manage.py test admissions.tests.AdmissionInlineErrorMarkupTests`
5) Ket qua: PASS (inline errors; no alert())

### E2) Podcasts thumbnail youtube maxres có th? 404
1) V?n d? (trích report): "Podcasts thumbnail youtube maxres có th? 404"
2) File ch?nh: `templates/core/podcasts.html`
3) Thay d?i:
   - onerror fallback: maxres -> hqdefault -> mqdefault.
4) L?nh test/smoke: `/tieng-noi-misers/`
5) K?t qu?: PASS (200)

---

## Quick Checks (sau 3 m?c D4 + E1 + E2)
- `python manage.py check` -> PASS
- `python manage.py makemigrations --check --dry-run` -> PASS
- `python manage.py showmigrations --plan` -> PASS
- `python manage.py collectstatic --noinput` -> PASS (1 file copied)
- Smoke (runserver + curl):
  - `/tuyen-sinh/` -> 200
  - `/tieng-noi-misers/` -> 200
  - `/en/` -> 301 (redirect)

---

### E3) CSR: CSS inline r?t l?n
1) V?n d? (trích report): "CSR: CSS inline r?t l?n"
2) File ch?nh: `csr/templates/csr/list.html`, `static/css/csr.css`
3) Thay d?i:
   - Tách toàn b? CSS ra `static/css/csr.css` và include b?ng `<link>`.
4) L?nh test/smoke: `python manage.py shell -c "from django.test import Client; print(Client(HTTP_HOST='localhost').get('/trach-nhiem-xa-hoi/').status_code)"`
5) K?t qu?: PASS (200; runserver+curl bi chan theo policy, dung Django test client)

### E4) /en duplicate content do i18n chua có d?ch
1) V?n d? (trích report): "/en duplicate content do i18n chua có d?ch"
2) File ch?nh: `school_website/urls.py`
3) Thay d?i:
   - Redirect /en và /en/* -> / (301).
4) L?nh test/smoke: `/en/`
5) K?t qu?: PASS (301)

---


## F) Database & Repo Hygiene

### F1) Xu ly db.sqlite3/.bak trong repo
1) Van de (trich report): "Xu ly db.sqlite3/.bak trong repo"
2) File chinh: `.gitignore`
3) Thay doi:
   - Them `db.sqlite3.bak` vao gitignore.
4) Lenh test/smoke: (none)
5) Ket qua: PASS

### F2) Seed idempotent (Student Life GET khong tao record)
1) Van de (trich report): "Seed idempotent (Student life GET tao record)"
2) File chinh: `core/views.py`, `core/management/commands/seed_pages.py`
3) Thay doi:
   - Bo tao record trong GET, thay bang seed command idempotent.
4) Lenh test/smoke: `python manage.py test` (test StudentLife)
5) Ket qua: PASS

---

## Quick Checks (sau 3 muc E3 + F1 + F2)
- `python manage.py check` -> PASS
- `python manage.py makemigrations --check --dry-run` -> PASS
- `python manage.py showmigrations --plan` -> PASS
- `python manage.py collectstatic --noinput` -> PASS (0 copied, 237 unmodified)

---

## G) Test toi thieu

### G1) Tao 8 Django TestCase theo checklist
1) Van de (trich report): "Tao toi thieu 8-12 Django TestCase"
2) File chinh: `core/tests.py`, `admissions/tests.py`
3) Thay doi:
   - Them tests cho sitemap/robots/news search/download count/gallery annotate/events pagination/staff pagination/student life no create.
4) Lenh test/smoke:
   - `python manage.py test`
   - `python manage.py check`
   - `python manage.py collectstatic --noinput`
5) Ket qua: PASS (8 tests, check ok, collectstatic ok)

---

## Quick Checks (final)
- `python manage.py test` -> PASS (11 tests)
- `python manage.py check` -> PASS
- `python manage.py collectstatic --noinput` -> PASS (0 copied, 237 unmodified)
- `python manage.py makemigrations --check --dry-run` -> PASS
- `python manage.py showmigrations --plan` -> PASS

---


## H) Reporting

### H1) Readiness report
1) Van de (trich report): "Stakeholder-ready readiness report"
2) File chinh: `docs/readiness_report.md`
3) Thay doi:
   - Tong hop diem so frontend/backend/db, muc do san sang go-live, rui ro con lai.
4) Lenh test/smoke: (none)
5) Ket qua: PASS

---


## I) Seed pages command fix

### I1) Fix seed_pages encoding error
1) Van de (trich report): "python manage.py seed_pages bi loi Unicode/SyntaxError"
2) File chinh: `core/management/commands/seed_pages.py`
3) Thay doi:
   - Ghi lai file voi chuoi Unicode escape de dam bao UTF-8 hop le.
4) Lenh test/smoke: `python manage.py seed_pages`
5) Ket qua: PASS (StudentLifePage already exists. No changes made.)

---
