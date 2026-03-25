# UI Audit Report - MIS Django Project
Generated: 2026-03-21

## Summary
- Total files scanned: 121
- Total issues found: 25
  - Red Critical: 3
  - Yellow Warning: 21
  - Blue Info: 1
- Auto-fixed findings: 16

## Files Scanned

### static/css + first-party portal CSS
- `static/css/about/edtech.css`
- `static/css/about/future_ai.css`
- `static/css/about/mission.css`
- `static/css/about/principal.css`
- `static/css/about/whymis.css`
- `static/css/csr.css`
- `static/css/curriculum-components.css`
- `static/css/custom.css`
- `static/css/design-tokens.css`
- `static/css/history.css`
- `static/css/input.css`
- `static/css/mis-future-ui.css`
- `static/css/news.css`
- `static/css/output.css`
- `static/css/pdf-images.css`
- `static/css/portal.css`
- `static/css/typography.css`
- `static/portal/portal.css`

### templates
- `templates/403.html`
- `templates/404.html`
- `templates/500.html`
- `templates/about/creative_movement.html`
- `templates/about/edtech.html`
- `templates/about/english.html`
- `templates/about/foreign_languages.html`
- `templates/about/future_ai.html`
- `templates/about/history.html`
- `templates/about/lifeskills.html`
- `templates/about/literature.html`
- `templates/about/math.html`
- `templates/about/mission.html`
- `templates/about/page.html`
- `templates/about/page_1.html`
- `templates/about/page_backup_original.html`
- `templates/about/page_missing.html`
- `templates/about/page_refactored.html`
- `templates/about/partials/_academics_page.html`
- `templates/about/partials/_cta.html`
- `templates/about/partials/_hero.html`
- `templates/about/partials/_pdf_images_section.html`
- `templates/about/partials/_section_header.html`
- `templates/about/partials/curriculum/_academic_pillar_card.html`
- `templates/about/partials/curriculum/_assessment_rubric.html`
- `templates/about/partials/curriculum/_brochure_drawer.html`
- `templates/about/partials/curriculum/_curriculum_hero.html`
- `templates/about/partials/curriculum/_differentiation_matrix.html`
- `templates/about/partials/curriculum/_final_cta_cluster.html`
- `templates/about/partials/curriculum/_learning_card.html`
- `templates/about/partials/curriculum/_outcome_badge.html`
- `templates/about/partials/curriculum/_roadmap_tabs_accordion.html`
- `templates/about/partials/curriculum/_trust_signal_strip.html`
- `templates/about/partners.html`
- `templates/about/principal.html`
- `templates/about/robotics.html`
- `templates/about/steam.html`
- `templates/about/strengths.html`
- `templates/about/tnst.html`
- `templates/about/vision.html`
- `templates/about/whymis.html`
- `templates/admissions/admission_detail.html`
- `templates/admissions/admission_list.html`
- `templates/base.html`
- `templates/contact/contact.html`
- `templates/core/achievements.html`
- `templates/core/core_values.html`
- `templates/core/facilities.html`
- `templates/core/home copy.html`
- `templates/core/home.html`
- `templates/core/home_1.html`
- `templates/core/includes/floating_contact.html`
- `templates/core/includes/footer.html`
- `templates/core/includes/navbar.html`
- `templates/core/includes/popup_form.html`
- `templates/core/lowfi/base.html`
- `templates/core/lowfi/mis_edtech.html`
- `templates/core/lowfi/mis_home.html`
- `templates/core/lowfi/mis_page.html`
- `templates/core/lowfi/mis_parent_portal.html`
- `templates/core/lowfi/mis_preparation.html`
- `templates/core/lowfi/mis_primary.html`
- `templates/core/lowfi/mis_thcs.html`
- `templates/core/lowfi/mis_thpt.html`
- `templates/core/lowfi/partials/panel.html`
- `templates/core/pillars.html`
- `templates/core/podcasts.html`
- `templates/core/program_overview_detail.html`
- `templates/core/student_life.html`
- `templates/core/student_spotlight_list.html`
- `templates/core/training_program_detail.html`
- `templates/core/training_programs.html`
- `templates/events/detail.html`
- `templates/events/list.html`
- `templates/gallery/album_detail.html`
- `templates/gallery/list.html`
- `templates/news/detail.html`
- `templates/news/list.html`
- `templates/portal/admissions/confirm_delete.html`
- `templates/portal/admissions/form.html`
- `templates/portal/admissions/list.html`
- `templates/portal/admissions/registrations_confirm_delete.html`
- `templates/portal/admissions/registrations_form.html`
- `templates/portal/admissions/registrations_list.html`
- `templates/portal/base.html`
- `templates/portal/dashboard.html`
- `templates/portal/events/confirm_delete.html`
- `templates/portal/events/form.html`
- `templates/portal/events/list.html`
- `templates/portal/includes/breadcrumb.html`
- `templates/portal/includes/form_fields.html`
- `templates/portal/includes/pagination.html`
- `templates/portal/layout.html`
- `templates/portal/login.html`
- `templates/portal/media/form.html`
- `templates/portal/media/list.html`
- `templates/portal/news/confirm_delete.html`
- `templates/portal/news/form.html`
- `templates/portal/news/list.html`
- `templates/portal/pages/confirm_delete.html`
- `templates/portal/pages/form.html`
- `templates/portal/pages/list.html`
- `templates/portal/pages/preview.html`

## Color Issues
| File | Line | Current Value | Issue | Suggested Fix |
|------|------|---------------|-------|---------------|
| static/css/portal.css | 110 | `color: #94a3b8` | Low contrast on white card/list surfaces (approximately 2.79:1 against white). | Use `#64748b` or `var(--color-text-muted)` for empty-state copy. |
| templates/portal/login.html | 150 | `color: #94a3b8` | Low contrast subtitle on white login panel (approximately 2.79:1). | Darken to `#64748b` or a stronger muted token. |
| templates/portal/login.html | 228 | `color: #94a3b8` | Low contrast footer text on white login panel (approximately 2.79:1). | Darken to `#64748b` or a stronger muted token. |
| static/css/custom.css | 114 | `#0E2A5C` | Hard-coded secondary/navy text color bypasses the existing token system. | Replace with a named secondary token or a semantic text token fallback. |
| static/css/custom.css | 154 | `#1B5DD0` | CTA blue sits outside the declared brand token palette and is repeated as a raw hex. | Tokenize as a secondary action color rather than hard-coding it in `.btn-primary`. |
| static/css/custom.css | 163 | `#164AA6` | Secondary hover blue duplicates the CTA palette with a slightly different shade. | Centralize both blue shades behind variables. |
| static/portal/portal.css | 18 | `--p-primary: #0d9488` | Portal palette is intentionally separate from the public red palette, but the split was not documented consistently and raw teal values reappear outside the token block. | Keep a dedicated portal namespace and reference `--p-*` everywhere else. |
| static/css/about/edtech.css | 31 | `linear-gradient(90deg, #4f46e5, #818cf8)` | Five unrelated accent gradients (indigo, green, purple, orange, red) create an inconsistent accent system on a single page. | Reduce to a smaller semantic accent set or document the page as intentionally multi-themed. |
| templates/portal/dashboard.html | 44 | `style="color:#8b5cf6"` | Dashboard stat icons use inline hard-coded accent colors instead of shared tokens. | Reference portal or global accent variables inline. |
| templates/about/partners.html | 507 | `rgba(239,68,68,0.15) / #ef4444` | Repeated inline accent pairs make the partner cards hard to retheme and duplicate the public palette manually. | Use semantic CSS variables with fallbacks for each accent pair. |
| templates/about/lifeskills.html | 193 | `#b71c1c` | The page contains a large set of inline maroon, purple, indigo, teal, and social-media colors outside any token system. | Move the repeated action/badge colors behind alias variables. |
| templates/about/history.html | 423 | `linear-gradient(135deg,#1e3a5f,#0d47a1)` | Closing CTA introduces a one-off blue gradient that is not defined anywhere in the token layer. | Use secondary/CTA variables instead of embedding a custom gradient inline. |
| static/css/output.css | 1 | `compiled Tailwind palette` | Generated utility bundle contains many hard-coded palette values by design. | Adjust the source tokens and utility config rather than editing `output.css` directly. |

## Typography Issues
| File | Line | Current Value | Issue | Suggested Fix |
|------|------|---------------|-------|---------------|
| static/css/custom.css | 83 | `font-family: 'Inter', system-ui, -apple-system, sans-serif` | Body typography in `custom.css` overrides the shared typography system and diverges from `typography.css`. | Use `var(--font-sans)` from the shared token layer. |
| static/css/custom.css | 84 | `line-height: 1.7` | Body line-height diverges from the shared `--lh-body` token. | Use `var(--lh-body)` to keep text rhythm consistent. |
| static/css/custom.css | 111 | `font-size: 2.5rem` | Section titles use a local ad-hoc scale instead of the typography tokens. | Adopt `--fs-h1` or a shared clamp token. |
| static/css/portal.css | 7 | `font-size: 1.75rem` | Portal title sizes are hand-authored and not tied to the shared or portal type scale. | Map them to a tokenized heading size. |
| static/portal/portal.css | 107 | `--p-font: 'Inter', system-ui, -apple-system, sans-serif` | Portal uses a separate font-family stack without documenting whether the mismatch from the public site is intentional. | Keep a dedicated admin font token or align with `--font-sans` explicitly. |
| templates/portal/login.html | 179 | `font-family: 'Inter', sans-serif` | The login page repeats local font-family overrides instead of consuming a UI font variable. | Reference a named UI font variable with fallback. |

## Layout/Alignment Issues
| File | Line | Current Value | Issue | Suggested Fix |
|------|------|---------------|-------|---------------|
| templates/portal/base.html | 21 | `style="color:#94a3b8;background:none;border:none;cursor:pointer;font-size:1.2rem"` | Inline control styling bypasses portal CSS and makes theme updates harder. | Use the portal token namespace even when inline styling is unavoidable. |
| templates/portal/dashboard.html | 14 | `style="display:flex;gap:8px"` | Inline flex layout overrides are repeated across portal templates instead of being expressed once in CSS. | Extract a shared portal action-row utility in CSS. |
| templates/about/lifeskills.html | 119 | `large inline card style block` | Card presentation, spacing, and color are heavily defined inline, which overrides the page stylesheet and makes reuse difficult. | Move card presentation into a reusable CSS component class. |
| templates/core/home.html | 1570 | `inline gradient block` | Home page sections repeat inline theme gradients instead of referencing shared hero/background tokens. | Extract the repeated gradients into CSS classes or variables. |
| templates/core/home_1.html | 1489 | `inline gradient block` | Alternate home template duplicates the same inline gradient logic as `home.html`. | Point both templates at the same shared CSS token or component class. |
| templates/core/home copy.html | 1460 | `inline gradient block` | Legacy home copy duplicates the same inline background overrides again. | Delete or refactor the duplicate template so the gradient system lives in one place. |

## Recommended CSS Variables (Design Tokens)
Create a `static/css/variables.css` with:
```css
:root {
  --color-primary: var(--color-brand-primary, #dc2626);
  --color-secondary: var(--color-brand-secondary, #1e40af);
  --color-text: var(--color-text-primary, #171717);
  --color-bg: var(--color-surface-light, #ffffff);
  --color-danger: var(--color-error, #ef4444);
  --font-family-base: var(--font-sans, 'Montserrat', ui-sans-serif, system-ui);
  --font-size-base: var(--fs-300, 16px);
  --font-size-sm: var(--fs-200, 14px);
  --font-size-lg: var(--fs-400, 18px);
}
```

## Auto-fix Scope
- High-confidence fixes were written to `.fixed` files only.
- Generated CSS (`static/css/output.css`) was audited but not patched directly.
- Theme-specific gradients in `home.html`, `home_1.html`, `home copy.html`, and the multicolor parts of `about/edtech.css` remain warnings because a safe semantic remap was not obvious.
