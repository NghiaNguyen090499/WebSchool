# Portal MIS UI/UX Testing Checklist

## 🚀 Server
- Django Server: `http://127.0.0.1:8000`
- Portal URL: `http://127.0.0.1:8000/portal/`
- Login URL: `http://127.0.0.1:8000/portal/login/`

## 📱 Mobile Responsive Testing (375px width)

### Sidebar
- [ ] Hamburger menu visible on mobile
- [ ] Click hamburger → sidebar slides in from left
- [ ] Overlay visible behind sidebar
- [ ] Click overlay → sidebar closes
- [ ] Press ESC → sidebar closes
- [ ] Navigation links work properly

### Tables
- [ ] Tables scroll horizontally on mobile
- [ ] Headers visible (sticky if scrolling)
- [ ] Action dropdown accessible

### Forms
- [ ] Form fields are full width
- [ ] Labels above inputs
- [ ] Error messages visible
- [ ] Submit button full width or appropriate size

---

## 🎨 Design System Verification

### Colors (should see these tokens)
- Primary: Navy blue (`hsl(222, 47%, 11%)`)
- Accent: Brand red (`hsl(348, 83%, 47%)`)
- Success: Green (`#16a34a`)
- Warning: Yellow/Orange (`#f59e0b`)
- Danger: Red (`#dc2626`)

### Typography
- Font: Inter (or system fallback)
- Vietnamese text readable with proper line height

### Components

#### Buttons
- [ ] `.btn-primary` - Navy blue background
- [ ] `.btn-secondary` - Light background
- [ ] `.btn-ghost` - Transparent, visible on hover
- [ ] `.btn-danger` - Red for destructive actions
- [ ] `.btn-success` - Green for positive actions
- [ ] Hover states visible
- [ ] Focus rings visible (Tab navigation)

#### Cards
- [ ] `.portal-card` - White background, shadow
- [ ] Header, body, footer sections
- [ ] Rounded corners

#### Badges
- [ ] `.badge-success` - Green
- [ ] `.badge-warning` - Yellow
- [ ] `.badge-danger` - Red
- [ ] `.badge-info` - Blue
- [ ] `.badge-neutral` - Gray

#### Dropdowns
- [ ] Click trigger → menu appears
- [ ] Menu has shadow and border
- [ ] Arrow up/down navigates items
- [ ] ESC closes menu
- [ ] Click outside closes menu
- [ ] Danger items are red

#### Tooltips
- [ ] Hover element → tooltip shows above
- [ ] Smooth animation
- [ ] Dark background, light text

---

## 🔧 Functionality Testing

### Login Page (`/portal/login/`)
- [ ] Form displays correctly
- [ ] Labels visible
- [ ] Submit button works
- [ ] Error messages show for invalid login

### Dashboard (`/portal/` - requires login)
- [ ] Stats grid with icons
- [ ] Recent content lists
- [ ] Navigation links work
- [ ] Cards have proper styling

### News List (`/portal/news/`)
- [ ] Filter form works
- [ ] Table displays correctly
- [ ] Dropdown actions work
- [ ] Empty state shown when no data

### News Form (`/portal/news/create/`)
- [ ] Sticky action bar
- [ ] Unsaved badge appears on change
- [ ] Ctrl+S triggers save
- [ ] TinyMCE editor loads

### Events List (`/portal/events/`)
- [ ] Similar to News list
- [ ] Date column formatted correctly

### Admissions (`/portal/admissions/`)
- [ ] Level badges displayed
- [ ] Active/Inactive status visible

### Registrations (`/portal/admissions/registrations/`)
- [ ] Phone link clickable
- [ ] Status badges color-coded
- [ ] Dropdown actions work

### Pages List (`/portal/pages/`)
- [ ] Status badges (Draft/Published)
- [ ] Search and filter work
- [ ] Dropdown actions work

### Page Editor (`/portal/pages/{id}/edit/`)
- [ ] Sticky action bar
- [ ] Publish/Unpublish buttons
- [ ] Preview button opens new tab
- [ ] Unsaved changes detection
- [ ] Ctrl+S save shortcut

### Page Preview (`/portal/pages/{id}/preview/`)
- [ ] Content renders with .prose styles
- [ ] SEO metadata displayed
- [ ] Edit button works

### Delete Confirmations
- [ ] Warning icon and message
- [ ] Alert box visible
- [ ] Danger button for confirm
- [ ] Cancel button works

---

## ♿ Accessibility Testing

### Keyboard Navigation
- [ ] Tab through all interactive elements
- [ ] Focus rings visible
- [ ] Modal trap works (Tab stays in modal)
- [ ] ESC closes modals/sidebar/dropdown

### Screen Reader
- [ ] Aria-labels on buttons
- [ ] Role attributes correct
- [ ] Live regions announce toasts
- [ ] Headings properly structured (h1 → h2 → h3)

### Motion
- [ ] Animations respect `prefers-reduced-motion`

---

## 📊 Performance

### CSS Size
- portal.css: ~49KB (unminified)

### JS Size  
- portal.js: ~31KB (unminified)

### Loading
- [ ] No console errors
- [ ] Static files load correctly
- [ ] Page renders without layout shift

---

## 🐛 Known Issues

1. **Vietnamese encoding in PowerShell**: Characters display garbled in terminal but render correctly in browser.

2. **TinyMCE API Key**: Uses "no-api-key" - needs real API key for production.

3. **Font Inter**: Should be loaded via Google Fonts or locally for optimal display.

---

## ✅ Test Complete

Date: _______________
Tester: ______________
Browser: _____________
Resolution: ___________
Notes:


