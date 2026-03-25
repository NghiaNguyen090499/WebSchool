# WebsiteSchool - Cau truc va giao dien he thong

## 1) Muc tieu tai lieu
Tai lieu nay mo ta:
- Cau truc he thong Django cua WebsiteSchool.
- Cach to chuc module va route public/portal.
- Kien truc giao dien (template, CSS, JS) de dong bo UI khi phat trien.

Pham vi tai lieu dua tren source code hien co trong repo.

## 2) Tong quan kien truc
He thong su dung monolithic Django (template-based):

```text
Browser
  -> Django URL Router (school_website/urls.py + i18n_patterns)
  -> App Views (core/news/events/...)
  -> Templates (templates/<app>/*.html)
  -> Static Assets (static/css, static/js, static/images)
  -> Database (SQLite dev, PostgreSQL production)
  -> Media Storage (media/)
```

## 3) App va trach nhiem chinh
| App | Vai tro |
|---|---|
| `core` | Home, training programs, program overview, student life, pillars, facilities, podcasts, health checks |
| `admissions` | Noi dung tuyen sinh, highlights, form dang ky, documents |
| `news` | Danh muc tin tuc, list/detail bai viet |
| `events` | Danh sach su kien, detail theo slug |
| `gallery` | Album anh, list/detail |
| `about` | Gioi thieu hoc thuat, mission/vision, cac trang curriculum |
| `contact` | Form lien he, form tu van, chatbot lead |
| `staff` | Danh sach va chi tiet doi ngu |
| `csr` | Trang trach nhiem xa hoi |
| `activities` | Hoat dong ngoai khoa |
| `portal` | Khu vuc noi bo (auth + CRUD cho news/events/admissions/pages/media) |

## 4) Cau truc thu muc du an
```text
WebsiteSchool/
|- school_website/        # settings.py, urls.py, wsgi/asgi
|- core/
|- admissions/
|- news/
|- events/
|- gallery/
|- about/
|- contact/
|- staff/
|- csr/
|- activities/
|- portal/
|- templates/             # HTML theo app + includes
|- static/
|  |- css/                # output.css, design-tokens.css, custom.css, portal.css, ...
|  |- js/                 # main.js
|  |- images/
|- media/                 # Uploaded files
|- scripts/               # Import/seed/update scripts
`- docs/                  # Tai lieu ky thuat/van hanh
```

## 5) URL map chinh
### 5.1 Root router (`school_website/urls.py`)
- Global: `favicon.ico`, `robots.txt`, `sitemap.xml`, `admin/`, `i18n/`.
- Public va portal duoc khai bao trong `i18n_patterns(..., prefix_default_language=False)`.

### 5.2 Prefix route theo module
- `/` -> `core.urls`
- `/news/` -> `news.urls`
- `/events/` -> `events.urls`
- `/gallery/` -> `gallery.urls`
- `/about/` -> `about.urls`
- `/contact/` -> `contact.urls`
- `/trach-nhiem-xa-hoi/` -> `csr.urls`
- `/tuyen-sinh/` -> `admissions.urls`
- `/doi-ngu/` -> `staff.urls`
- `/hoat-dong-ngoai-khoa/` -> `activities.urls`
- `/portal/` -> `portal.urls`

### 5.3 Endpoint he thong
- `/healthz/` (core)
- `/readyz/` (core)

## 6) Cau truc giao dien (UI Architecture)
### 6.1 Base layout
Public pages dung `templates/base.html`:
- Includes:
  - `core/includes/navbar.html`
  - `core/includes/floating_contact.html`
  - `core/includes/footer.html`
- Main region:
  - `<main id="main-content"> ... {% block content %}`
- Co `skip-link` cho accessibility.

Portal dung bo template rieng trong `templates/portal/`:
- `layout.html`, `base.html`, `dashboard.html`, `login.html`.
- Cac module con: `portal/news/*`, `portal/events/*`, `portal/admissions/*`, `portal/pages/*`, `portal/media/*`.

### 6.2 CSS layering
Thu tu tai CSS trong `base.html`:
1. `static/css/output.css` (Tailwind compiled)
2. `static/css/design-tokens.css` (design token)
3. `static/css/custom.css` (component/utility/global style)

Them theo nhu cau trang:
- `static/css/pdf-images.css` (trang program overview/PDF image flow)
- `static/css/portal.css` (portal UI)
- `static/css/csr.css` (module CSR)

### 6.3 JS layering
- `static/js/main.js`:
  - Khoi tao dark mode.
  - Smooth scroll cho anchor links.
  - Lazy load video.
- Inline scripts tai `base.html`:
  - Lazy load image/iframe.
  - Date display helper.

### 6.4 Pattern giao dien chung
- Utility class theo section:
  - `.section`, `.section-tight`, `.section-compact`, `.section-slim`
- Hero pattern:
  - Nen gradient (`.hero-gradient-bg`)
  - Heading lon (`.hero-title`)
  - CTA va animation (`.animate-fadeInUp`)
- Card pattern:
  - Radius lon (`rounded-2xl/3xl`)
  - Shadow + hover-lift
  - Border mau nhe de tach khoi nen

### 6.5 Responsive strategy
- Mobile-first qua Tailwind utility classes.
- Breakpoint chinh:
  - `sm`, `md`, `lg`, `xl`
- Luon uu tien:
  - Dam bao text line-length vua phai (`max-w-*`)
  - Grid 1 cot tren mobile, nhieu cot tren desktop
  - Touch-friendly spacing cho button/form.

## 7) Luong du lieu giao dien quan trong
### 7.1 Public content flow
1. Request vao route module.
2. View query model.
3. Render template theo app (`templates/<app>/...`).
4. Lay static/media cho anh/video/document.

### 7.2 Form flow
- Admissions:
  - GET list/detail
  - POST `/tuyen-sinh/dang-ky/` tao `AdmissionRegistration`
- Contact:
  - GET/POST `/contact/`
  - POST consultation/chatbot lead endpoints
  - Co chong spam/rate-limit co ban trong view.

### 7.3 Portal flow
1. User login (`/portal/login/`).
2. Truy cap dashboard.
3. CRUD content theo module.
4. Quan ly page publishing va media upload.
5. Ghi log qua model audit (portal).

## 8) i18n, static, media
- i18n:
  - `LocaleMiddleware` bat buoc.
  - `LANGUAGES = en, vi`.
  - `prefix_default_language=False` (URL default khong co language prefix).
- Static:
  - `STATIC_URL=/static/`
  - `STATIC_ROOT=staticfiles/`
  - Source static trong `static/`
- Media:
  - `MEDIA_URL=/media/`
  - `MEDIA_ROOT=media/`

## 9) Huong dan mo rong giao dien
Khi them trang/module moi:
1. Khai bao route o app `urls.py`.
2. Tao view tra ve template.
3. Dat template theo dung namespace (`templates/<app>/...`).
4. Tai su dung pattern chung (`hero`, `section`, `card`, `btn`).
5. Neu co CSS rieng, tach file trong `static/css/` va include qua `{% block extra_head %}`.
6. Kiem tra mobile + desktop + dark mode + lazy loading media.

## 10) Checklist cap nhat tai lieu
Cap nhat file nay khi co thay doi:
- Them app moi hoac doi prefix URL.
- Doi base layout/includes.
- Doi design token/CSS stack.
- Doi flow portal hoac form business-critical.
