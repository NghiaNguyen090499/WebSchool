css = """
/* ============================================
   NEWS DETAIL PAGE
   ============================================ */
/* Reading Progress */
.news-progress-container {
    position: fixed;
    top: 72px;
    left: 0;
    width: 100%;
    height: 4px;
    background: transparent;
    z-index: 1000;
}
.news-progress-bar {
    height: 100%;
    background: var(--brand-primary-500);
    width: 0%;
    transition: width 0.1s ease-out;
}

/* Detail Header */
.news-detail-header {
    position: relative;
    padding: 5rem 1.5rem 8rem;
    overflow: visible;
    background: var(--surface-muted);
}
.dark .news-detail-header {
    background: #1e293b;
}

.news-detail-header-bg {
    position: absolute;
    inset: 0;
    background: var(--gradient-hero);
    opacity: 0.05;
    z-index: 0;
}
.dark .news-detail-header-bg {
    opacity: 0.15;
}

.news-detail-header-content {
    position: relative;
    z-index: 10;
    max-width: 900px;
    margin: 0 auto;
    text-align: center;
}

.news-detail-title {
    font-size: clamp(2rem, 4.5vw, 3.5rem);
    font-weight: 800;
    line-height: 1.25;
    color: var(--content-strong);
    margin: 1.25rem 0 2rem;
    letter-spacing: -0.02em;
}

.news-detail-meta {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    gap: 1.5rem;
    font-size: 0.95rem;
    color: var(--content-muted);
    margin-bottom: 2.5rem;
}

.news-meta-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 500;
}
.news-meta-item i {
    color: var(--brand-primary-500);
}

.news-detail-hero-image {
    position: relative;
    border-radius: 1.5rem;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0,0,0,0.15);
    margin: 0 auto -6rem; /* overlaps into body */
    aspect-ratio: 16/9;
    max-width: 1000px;
    z-index: 15;
    background: var(--surface);
}
@media (max-width: 768px) {
    .news-detail-hero-image {
        margin: 0 auto -4rem;
        border-radius: 1rem;
    }
}
.news-detail-hero-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

/* Body & Layout */
.news-detail-body {
    max-width: 1100px;
    margin: 8rem auto 4rem; /* 8rem top margin to clear hero overlap */
    padding: 0 1.5rem;
    position: relative;
    display: grid;
    grid-template-columns: 80px 1fr;
    gap: 3rem;
    align-items: start;
}

@media (max-width: 1024px) {
    .news-detail-body {
        grid-template-columns: 1fr;
        margin-top: 6rem;
    }
}

/* Social Share Sticky */
.news-detail-share {
    position: relative;
}
.news-share-sticky {
    position: sticky;
    top: 120px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    z-index: 20;
}
@media (max-width: 1024px) {
    .news-share-sticky {
        position: relative;
        top: 0;
        flex-direction: row;
        justify-content: center;
        margin-bottom: 2rem;
        flex-wrap: wrap;
    }
}

.news-share-label {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    color: var(--content-muted);
    letter-spacing: 0.05em;
    writing-mode: vertical-rl;
    transform: rotate(180deg);
    margin-bottom: 0.5rem;
}
@media (max-width: 1024px) {
    .news-share-label {
        writing-mode: horizontal-tb;
        transform: none;
        margin-bottom: 0;
        margin-right: 0.5rem;
    }
}

.news-share-btn {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--surface);
    color: var(--content-muted);
    border: 1px solid var(--border);
    font-size: 1.1rem;
    text-decoration: none;
    transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03);
}

.news-share-btn:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.1);
}
.news-share-btn.fb:hover { color: #fff; background: #1877F2; border-color: #1877F2; }
.news-share-btn.tw:hover { color: #fff; background: #1DA1F2; border-color: #1DA1F2; }
.news-share-btn.cp:hover { color: #fff; background: var(--content-strong); border-color: var(--content-strong); }

/* Typography Prose Premium */
.news-detail-content {
    background: var(--surface);
    border-radius: 2rem;
    padding: 5rem 6rem;
    box-shadow: 0 10px 40px rgba(0,0,0,0.03);
    border: 1px solid var(--border);
    position: relative;
    z-index: 20;
    max-width: 100%;
    overflow-x: hidden;
}
@media (max-width: 768px) {
    .news-detail-content {
        padding: 2.5rem 1.5rem;
        border-radius: 1.25rem;
    }
}

.prose-premium {
    font-size: 1.15rem;
    line-height: 1.8;
    color: var(--content-strong);
    font-family: inherit;
}

.prose-premium p {
    margin-bottom: 1.75rem;
}

.prose-premium h2, .prose-premium h3, .prose-premium h4, .prose-premium h5, .prose-premium h6 {
    color: var(--content-strong);
    font-weight: 700;
    line-height: 1.3;
    margin: 2.5rem 0 1.25rem;
}

.prose-premium h2 { font-size: 1.85rem; font-weight: 800; }
.prose-premium h3 { font-size: 1.5rem; }
.prose-premium h4 { font-size: 1.25rem; }

.prose-premium a {
    color: var(--brand-primary-500);
    text-decoration: none;
    border-bottom: 1px solid rgba(220, 38, 38, 0.3);
    transition: all 0.2s;
    font-weight: 500;
}
.prose-premium a:hover {
    border-bottom-color: var(--brand-primary-500);
    border-bottom-width: 2px;
}

.prose-premium img {
    max-width: 100%;
    height: auto;
    border-radius: 1rem;
    margin: 2.5rem auto;
    display: block;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}
.prose-premium img[class*="wp-image"] {
    width: auto;
}

.prose-premium figure {
    margin: 2.5rem 0;
    text-align: center;
}
.prose-premium figcaption {
    font-size: 0.9rem;
    color: var(--content-muted);
    margin-top: 1rem;
    font-style: italic;
}

.prose-premium blockquote {
    margin: 2.5rem 0;
    padding: 1.5rem 2.5rem;
    background: rgba(220, 38, 38, 0.04);
    border-left: 4px solid var(--brand-primary-500);
    border-radius: 0 1rem 1rem 0;
    font-size: 1.25rem;
    font-style: italic;
    color: var(--brand-primary-700);
    line-height: 1.6;
}
.dark .prose-premium blockquote {
    background: rgba(220, 38, 38, 0.1);
    color: var(--brand-primary-500);
}

.prose-premium ul, .prose-premium ol {
    margin-bottom: 2rem;
    padding-left: 1.5rem;
}
.prose-premium li {
    margin-bottom: 0.75rem;
}
.prose-premium li::marker {
    color: var(--brand-primary-500);
    font-weight: bold;
}

/* Content specific fixes for wordpress */
.prose-premium .aligncenter { text-align: center; margin: 0 auto; clear: both; display: block; }
.prose-premium .alignright { float: right; margin: 0 0 1rem 1rem; }
.prose-premium .alignleft { float: left; margin: 0 1rem 1rem 0; }

/* First paragraph dropcap */
.prose-premium > p:first-of-type::first-letter {
    font-size: 4rem;
    font-weight: 900;
    float: left;
    line-height: 0.85;
    margin: 0.1em 0.15em 0 0;
    color: var(--brand-primary-500);
}

/* Related section */
.news-detail-related {
    background: var(--surface-muted);
    padding: 5rem 1.5rem;
    border-top: 1px solid var(--border);
}
.dark .news-detail-related { background: #1e293b; }

.news-detail-related-inner {
    max-width: 1280px;
    margin: 0 auto;
}
"""

with open('d:/NGHIA/WebsiteSchool/static/css/news.css', 'a', encoding='utf-8') as f:
    f.write('\n' + css)
