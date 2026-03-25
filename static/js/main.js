// Main JavaScript file for custom functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize dark mode from localStorage
    const darkMode = localStorage.getItem('darkMode') === 'true';
    if (darkMode) {
        document.documentElement.classList.add('dark');
    }
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (!href || href === '#' || href === '#0') {
                return;
            }
            let target;
            try {
                target = document.querySelector(href);
            } catch (err) {
                return;
            }
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Lazy-load heavy videos to avoid eager downloads
    const lazyVideos = document.querySelectorAll('video[data-lazy-video]');
    if (lazyVideos.length) {
        const loadVideo = (video) => {
            if (!video || video.dataset.loaded === 'true') {
                return;
            }
            const sources = video.querySelectorAll('source[data-src]');
            sources.forEach((source) => {
                source.src = source.dataset.src;
                source.removeAttribute('data-src');
            });
            video.load();
            video.dataset.loaded = 'true';
        };

        lazyVideos.forEach((video) => {
            video.addEventListener('play', () => loadVideo(video), { once: true });
        });

        if ('IntersectionObserver' in window) {
            const observer = new IntersectionObserver((entries, obs) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        loadVideo(entry.target);
                        obs.unobserve(entry.target);
                    }
                });
            }, { rootMargin: '200px 0px' });

            lazyVideos.forEach((video) => observer.observe(video));
        } else {
            lazyVideos.forEach((video) => loadVideo(video));
        }
    }

    // Curriculum tabs: accessible tablist controls
    document.querySelectorAll('[data-curriculum-tabs]').forEach((tabsRoot) => {
        const tabs = Array.from(tabsRoot.querySelectorAll('[role="tab"]'));
        const panels = Array.from(tabsRoot.querySelectorAll('.curriculum-tab-panel'));
        if (!tabs.length || !panels.length) {
            return;
        }

        const activate = (nextTab) => {
            tabs.forEach((tab) => {
                const selected = tab === nextTab;
                tab.classList.toggle('is-active', selected);
                tab.setAttribute('aria-selected', selected ? 'true' : 'false');
                tab.tabIndex = selected ? 0 : -1;
                const panelId = tab.getAttribute('aria-controls');
                const panel = panelId ? tabsRoot.querySelector(`#${panelId}`) : null;
                if (panel) {
                    panel.classList.toggle('is-active', selected);
                    panel.hidden = !selected;
                }
            });
        };

        tabs.forEach((tab, index) => {
            tab.addEventListener('click', () => activate(tab));
            tab.addEventListener('keydown', (event) => {
                let nextIndex = null;
                if (event.key === 'ArrowRight') {
                    nextIndex = (index + 1) % tabs.length;
                } else if (event.key === 'ArrowLeft') {
                    nextIndex = (index - 1 + tabs.length) % tabs.length;
                } else if (event.key === 'Home') {
                    nextIndex = 0;
                } else if (event.key === 'End') {
                    nextIndex = tabs.length - 1;
                }
                if (nextIndex !== null) {
                    event.preventDefault();
                    activate(tabs[nextIndex]);
                    tabs[nextIndex].focus();
                }
            });
        });
    });

    // Curriculum accordion: one-open behavior
    document.querySelectorAll('[data-curriculum-accordion]').forEach((accordionRoot) => {
        const triggers = Array.from(accordionRoot.querySelectorAll('.curriculum-accordion-trigger'));
        if (!triggers.length) {
            return;
        }

        const toggle = (trigger) => {
            triggers.forEach((btn) => {
                const controlsId = btn.getAttribute('aria-controls');
                const panel = controlsId ? accordionRoot.querySelector(`#${controlsId}`) : null;
                const expanded = btn === trigger ? btn.getAttribute('aria-expanded') !== 'true' : false;
                btn.setAttribute('aria-expanded', expanded ? 'true' : 'false');
                if (panel) {
                    panel.hidden = !expanded;
                    panel.classList.toggle('is-open', expanded);
                }
            });
        };

        triggers.forEach((trigger) => {
            trigger.addEventListener('click', () => toggle(trigger));
        });
    });

    // Brochure dialog: native dialog with lightweight fallback
    const openDialog = (dialog) => {
        if (!dialog) return;
        if (typeof dialog.showModal === 'function') {
            if (!dialog.open) dialog.showModal();
        } else {
            dialog.setAttribute('open', 'open');
        }
    };

    const closeDialog = (dialog) => {
        if (!dialog) return;
        if (typeof dialog.close === 'function') {
            if (dialog.open) dialog.close();
        } else {
            dialog.removeAttribute('open');
        }
    };

    document.querySelectorAll('[data-open-dialog]').forEach((opener) => {
        opener.addEventListener('click', () => {
            const targetId = opener.getAttribute('data-open-dialog');
            if (!targetId) return;
            const dialog = document.getElementById(targetId);
            openDialog(dialog);
        });
    });

    document.querySelectorAll('[data-brochure-dialog]').forEach((dialog) => {
        dialog.querySelectorAll('[data-close-dialog]').forEach((closer) => {
            closer.addEventListener('click', () => closeDialog(dialog));
        });
        dialog.addEventListener('cancel', (event) => {
            event.preventDefault();
            closeDialog(dialog);
        });
        dialog.addEventListener('click', (event) => {
            if (event.target === dialog) {
                closeDialog(dialog);
            }
        });
    });

    // Curriculum motion: reveal on scroll + subtle hero parallax
    const curriculumRoot = document.querySelector('.curriculum');
    const reducedMotionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    const prefersReducedMotion = reducedMotionQuery.matches;

    if (curriculumRoot && !prefersReducedMotion) {
        document.documentElement.classList.add('has-curriculum-motion');

        const revealTargets = Array.from(new Set([
            ...curriculumRoot.querySelectorAll('[data-reveal]'),
            ...curriculumRoot.querySelectorAll(
                '.curriculum-section, .curriculum-card, .curriculum-rubric-row, .curriculum-trust-item, .curriculum-table-wrap, .curriculum-brochure'
            ),
        ]));

        revealTargets.forEach((element, index) => {
            if (!element.hasAttribute('data-reveal')) {
                element.setAttribute('data-reveal', '');
            }

            // Keep explicit delay configured in template; only add stagger when absent.
            if (!element.style.getPropertyValue('--reveal-delay')) {
                const staggerIndex = index % 8;
                element.style.setProperty('--reveal-delay', `${staggerIndex * 36}ms`);
            }
        });

        if ('IntersectionObserver' in window) {
            const revealObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('is-visible');
                        observer.unobserve(entry.target);
                    }
                });
            }, {
                threshold: 0.14,
                rootMargin: '0px 0px -8% 0px',
            });

            revealTargets.forEach((element) => revealObserver.observe(element));
        } else {
            revealTargets.forEach((element) => element.classList.add('is-visible'));
        }

        const heroes = Array.from(curriculumRoot.querySelectorAll('.curriculum-hero'));
        if (heroes.length) {
            let ticking = false;

            const updateHeroParallax = () => {
                heroes.forEach((hero) => {
                    const rect = hero.getBoundingClientRect();
                    const viewportHeight = window.innerHeight || 1;
                    const progress = (viewportHeight - rect.top) / (viewportHeight + rect.height);
                    const clamped = Math.max(0, Math.min(1, progress));
                    const offset = (clamped - 0.5) * 14;
                    hero.style.setProperty('--hero-parallax-offset', `${offset.toFixed(2)}px`);
                });
                ticking = false;
            };

            updateHeroParallax();
            window.addEventListener('scroll', () => {
                if (!ticking) {
                    window.requestAnimationFrame(updateHeroParallax);
                    ticking = true;
                }
            }, { passive: true });

            window.addEventListener('resize', updateHeroParallax, { passive: true });
        }
    }
});







