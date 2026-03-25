/**
 * Portal MIS - Core JavaScript Module v2.0
 * Features: Sidebar, Tabs, Modal, Toast, Unsaved Changes, Keyboard Shortcuts, A11y
 */

const Portal = (function () {
    'use strict';

    // =========================================
    // STATE
    // =========================================
    const state = {
        isDirty: false,
        isSaving: false,
        toastQueue: [],
        activeModal: null,
        focusTrap: null,
    };

    // =========================================
    // UTILITIES
    // =========================================

    /**
     * Debounce function calls
     */
    function debounce(fn, delay = 300) {
        let timer;
        return function (...args) {
            clearTimeout(timer);
            timer = setTimeout(() => fn.apply(this, args), delay);
        };
    }

    /**
     * Generate unique ID
     */
    function generateId() {
        return 'p-' + Math.random().toString(36).substr(2, 9);
    }

    /**
     * Get focusable elements within a container
     */
    function getFocusableElements(container) {
        const selectors = [
            'a[href]',
            'button:not([disabled])',
            'input:not([disabled])',
            'select:not([disabled])',
            'textarea:not([disabled])',
            '[tabindex]:not([tabindex="-1"])',
        ];
        return Array.from(container.querySelectorAll(selectors.join(', ')));
    }

    // =========================================
    // TOAST SYSTEM
    // =========================================

    /**
     * Show a toast notification
     * @param {string} message - Toast message
     * @param {string} type - 'info' | 'success' | 'error' | 'warning'
     * @param {number} duration - Auto dismiss time in ms (0 = no auto dismiss)
     */
    function showToast(message, type = 'info', duration = 5000) {
        let container = document.querySelector('.portal-toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'portal-toast-container';
            container.setAttribute('aria-live', 'polite');
            container.setAttribute('aria-atomic', 'true');
            document.body.appendChild(container);
        }

        // Create live region announcement for screen readers
        let liveRegion = container.querySelector('.portal-toast-live');
        if (!liveRegion) {
            liveRegion = document.createElement('div');
            liveRegion.className = 'portal-toast-live sr-only';
            liveRegion.setAttribute('aria-live', 'assertive');
            container.appendChild(liveRegion);
        }

        const icons = {
            info: 'ℹ️',
            success: '✅',
            error: '❌',
            warning: '⚠️',
        };

        const toast = document.createElement('div');
        toast.className = 'portal-toast';
        toast.setAttribute('role', 'alert');
        toast.setAttribute('data-type', type);
        toast.id = generateId();

        toast.innerHTML = `
            <span class="portal-toast-icon" aria-hidden="true">${icons[type] || icons.info}</span>
            <span class="portal-toast-content">${escapeHtml(message)}</span>
            <button class="portal-toast-close" aria-label="Đóng thông báo" type="button">✕</button>
        `;

        // Announce to screen readers
        liveRegion.textContent = message;

        // Add close handler
        const closeBtn = toast.querySelector('.portal-toast-close');
        closeBtn.addEventListener('click', () => dismissToast(toast));

        container.appendChild(toast);
        state.toastQueue.push(toast);

        // Auto dismiss
        if (duration > 0) {
            setTimeout(() => dismissToast(toast), duration);
        }

        // Limit queue to 5 toasts
        if (state.toastQueue.length > 5) {
            dismissToast(state.toastQueue[0]);
        }

        return toast;
    }

    /**
     * Dismiss a toast with animation
     */
    function dismissToast(toast) {
        if (!toast || !toast.parentElement) return;

        toast.classList.add('is-exiting');
        toast.addEventListener('animationend', () => {
            toast.remove();
            state.toastQueue = state.toastQueue.filter((t) => t !== toast);
        });
    }

    /**
     * Escape HTML to prevent XSS
     */
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // =========================================
    // SIDEBAR
    // =========================================

    function initSidebar() {
        const toggleBtn = document.getElementById('portal-sidebar-toggle');
        const sidebar = document.getElementById('portal-sidebar');
        const overlay = document.querySelector('.portal-sidebar-overlay');

        if (!toggleBtn || !sidebar) return;

        toggleBtn.addEventListener('click', () => {
            const isOpen = document.body.classList.toggle('portal-sidebar-open');
            toggleBtn.setAttribute('aria-expanded', isOpen);

            if (isOpen) {
                // Focus first nav item when opening
                const firstLink = sidebar.querySelector('a');
                if (firstLink) firstLink.focus();
            }
        });

        // Close on overlay click
        if (overlay) {
            overlay.addEventListener('click', closeSidebar);
        }

        // Close on ESC
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && document.body.classList.contains('portal-sidebar-open')) {
                closeSidebar();
                toggleBtn.focus();
            }
        });

        // Close sidebar on resize to desktop
        const mediaQuery = window.matchMedia('(min-width: 768px)');
        mediaQuery.addEventListener('change', (e) => {
            if (e.matches) {
                document.body.classList.remove('portal-sidebar-open');
            }
        });
    }

    function closeSidebar() {
        document.body.classList.remove('portal-sidebar-open');
        const toggleBtn = document.getElementById('portal-sidebar-toggle');
        if (toggleBtn) toggleBtn.setAttribute('aria-expanded', 'false');
    }

    // =========================================
    // TABS
    // =========================================

    function initTabs() {
        const tabContainers = document.querySelectorAll('[data-tabs]');

        tabContainers.forEach((container) => {
            const tabs = container.querySelectorAll('[data-tab]');
            const panels = container.querySelectorAll('[data-tab-panel]');

            if (tabs.length === 0) return;

            // Set up ARIA
            tabs.forEach((tab, index) => {
                tab.setAttribute('role', 'tab');
                tab.setAttribute('aria-selected', 'false');
                tab.id = tab.id || `tab-${generateId()}`;

                const panel = panels[index];
                if (panel) {
                    panel.setAttribute('role', 'tabpanel');
                    panel.setAttribute('aria-labelledby', tab.id);
                    panel.setAttribute('aria-hidden', 'true');
                    panel.classList.remove('active');
                }
            });

            // Restore from URL hash or localStorage
            const savedTab = getTabFromStorage(container) || tabs[0].dataset.tab;
            activateTab(container, savedTab);

            // Click handlers
            tabs.forEach((tab) => {
                tab.addEventListener('click', (e) => {
                    e.preventDefault();
                    activateTab(container, tab.dataset.tab);
                });

                // Keyboard navigation
                tab.addEventListener('keydown', (e) => {
                    const tabsArray = Array.from(tabs);
                    const currentIndex = tabsArray.indexOf(tab);

                    let newIndex;
                    if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
                        newIndex = (currentIndex + 1) % tabsArray.length;
                    } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
                        newIndex = (currentIndex - 1 + tabsArray.length) % tabsArray.length;
                    } else if (e.key === 'Home') {
                        newIndex = 0;
                    } else if (e.key === 'End') {
                        newIndex = tabsArray.length - 1;
                    }

                    if (newIndex !== undefined) {
                        e.preventDefault();
                        tabsArray[newIndex].focus();
                        activateTab(container, tabsArray[newIndex].dataset.tab);
                    }
                });
            });
        });
    }

    function activateTab(container, tabId) {
        const tabs = container.querySelectorAll('[data-tab]');
        const panels = container.querySelectorAll('[data-tab-panel]');

        tabs.forEach((tab) => {
            const isActive = tab.dataset.tab === tabId;
            tab.classList.toggle('active', isActive);
            tab.setAttribute('aria-selected', isActive);
            tab.setAttribute('tabindex', isActive ? '0' : '-1');
        });

        panels.forEach((panel) => {
            const isActive = panel.dataset.tabPanel === tabId;
            panel.classList.toggle('active', isActive);
            panel.setAttribute('aria-hidden', !isActive);
        });

        // Save to storage
        saveTabToStorage(container, tabId);
    }

    function getTabFromStorage(container) {
        const key = container.dataset.tabs || 'default-tabs';
        // Check URL hash first
        const hash = window.location.hash.replace('#', '');
        if (hash && container.querySelector(`[data-tab="${hash}"]`)) {
            return hash;
        }
        // Fall back to localStorage
        try {
            return localStorage.getItem(`portal-tab-${key}`);
        } catch (e) {
            return null;
        }
    }

    function saveTabToStorage(container, tabId) {
        const key = container.dataset.tabs || 'default-tabs';
        try {
            localStorage.setItem(`portal-tab-${key}`, tabId);
            // Update URL hash without scrolling
            if (history.replaceState) {
                history.replaceState(null, null, `#${tabId}`);
            }
        } catch (e) {
            // localStorage not available
        }
    }

    // =========================================
    // MODAL SYSTEM
    // =========================================

    function initModals() {
        // Handle [data-modal-trigger] buttons
        document.querySelectorAll('[data-modal-trigger]').forEach((trigger) => {
            trigger.addEventListener('click', (e) => {
                e.preventDefault();
                const modalId = trigger.dataset.modalTrigger;
                const modal = document.getElementById(modalId);
                if (modal) openModal(modal);
            });
        });

        // Handle close buttons
        document.querySelectorAll('[data-modal-close]').forEach((closeBtn) => {
            closeBtn.addEventListener('click', () => {
                const modal = closeBtn.closest('.portal-modal-backdrop');
                if (modal) closeModal(modal);
            });
        });

        // Handle backdrop click
        document.querySelectorAll('.portal-modal-backdrop').forEach((backdrop) => {
            backdrop.addEventListener('click', (e) => {
                if (e.target === backdrop && !backdrop.dataset.modalPersistent) {
                    closeModal(backdrop);
                }
            });
        });

        // ESC to close
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && state.activeModal) {
                closeModal(state.activeModal);
            }
        });
    }

    function openModal(modal) {
        if (!modal) return;

        state.activeModal = modal;
        modal.classList.add('is-open');
        modal.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';

        // Focus trap setup
        const focusableElements = getFocusableElements(modal);
        if (focusableElements.length > 0) {
            focusableElements[0].focus();
            setupFocusTrap(modal, focusableElements);
        }

        // Announce to screen readers
        const title = modal.querySelector('.portal-modal-title');
        if (title) {
            modal.setAttribute('aria-labelledby', title.id || generateId());
        }
    }

    function closeModal(modal) {
        if (!modal) return;

        modal.classList.remove('is-open');
        modal.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';

        // Remove focus trap
        if (state.focusTrap) {
            document.removeEventListener('keydown', state.focusTrap);
            state.focusTrap = null;
        }

        state.activeModal = null;

        // Return focus to trigger
        const trigger = document.querySelector(`[data-modal-trigger="${modal.id}"]`);
        if (trigger) trigger.focus();
    }

    function setupFocusTrap(modal, focusableElements) {
        state.focusTrap = function (e) {
            if (e.key !== 'Tab') return;

            const firstEl = focusableElements[0];
            const lastEl = focusableElements[focusableElements.length - 1];

            if (e.shiftKey && document.activeElement === firstEl) {
                e.preventDefault();
                lastEl.focus();
            } else if (!e.shiftKey && document.activeElement === lastEl) {
                e.preventDefault();
                firstEl.focus();
            }
        };
        document.addEventListener('keydown', state.focusTrap);
    }

    /**
     * Programmatically create and show a confirm modal
     */
    function confirmModal(options = {}) {
        return new Promise((resolve) => {
            const {
                title = 'Xác nhận',
                message = 'Bạn có chắc chắn muốn thực hiện hành động này?',
                confirmText = 'Xác nhận',
                cancelText = 'Hủy',
                type = 'danger', // 'danger' | 'warning' | 'info'
            } = options;

            // Create modal
            const backdrop = document.createElement('div');
            backdrop.className = 'portal-modal-backdrop';
            backdrop.innerHTML = `
                <div class="portal-modal" role="dialog" aria-modal="true">
                    <div class="portal-modal-header">
                        <h3 class="portal-modal-title">${escapeHtml(title)}</h3>
                        <button class="portal-modal-close" aria-label="Đóng" type="button">✕</button>
                    </div>
                    <div class="portal-modal-body">
                        <p>${escapeHtml(message)}</p>
                    </div>
                    <div class="portal-modal-footer">
                        <button type="button" class="btn btn-secondary btn-md" data-action="cancel">${escapeHtml(cancelText)}</button>
                        <button type="button" class="btn btn-${type} btn-md" data-action="confirm">${escapeHtml(confirmText)}</button>
                    </div>
                </div>
            `;

            document.body.appendChild(backdrop);

            // Handle actions
            const handleAction = (result) => {
                closeModal(backdrop);
                backdrop.addEventListener('transitionend', () => backdrop.remove());
                resolve(result);
            };

            backdrop.querySelector('[data-action="confirm"]').addEventListener('click', () => handleAction(true));
            backdrop.querySelector('[data-action="cancel"]').addEventListener('click', () => handleAction(false));
            backdrop.querySelector('.portal-modal-close').addEventListener('click', () => handleAction(false));

            // Click outside
            backdrop.addEventListener('click', (e) => {
                if (e.target === backdrop) handleAction(false);
            });

            openModal(backdrop);
        });
    }

    // =========================================
    // UNSAVED CHANGES GUARD
    // =========================================

    function initUnsavedChanges() {
        const form = document.querySelector('form.portal-form');
        if (!form) return;

        // Track original form data
        const originalData = new FormData(form);
        const originalValues = {};
        for (const [key, value] of originalData.entries()) {
            originalValues[key] = value;
        }

        // Detect changes
        const checkDirty = debounce(() => {
            const currentData = new FormData(form);
            let isDirty = false;

            for (const [key, value] of currentData.entries()) {
                if (originalValues[key] !== value) {
                    isDirty = true;
                    break;
                }
            }

            if (isDirty !== state.isDirty) {
                state.isDirty = isDirty;
                updateDirtyUI();
            }
        }, 100);

        // Listen for input changes
        form.addEventListener('input', checkDirty);
        form.addEventListener('change', checkDirty);

        // Warn before leaving
        window.addEventListener('beforeunload', (e) => {
            if (state.isDirty && !state.isSaving) {
                e.preventDefault();
                e.returnValue = 'Bạn có thay đổi chưa lưu!';
            }
        });

        // Reset dirty on successful submit
        form.addEventListener('submit', () => {
            state.isDirty = false;
            state.isSaving = true;
        });
    }

    function updateDirtyUI() {
        const saveBtn = document.querySelector('.btn-save-trigger');
        const unsavedBadge = document.querySelector('.badge-unsaved-indicator');

        if (saveBtn) {
            const btnText = saveBtn.querySelector('.btn-text') || saveBtn;
            if (state.isDirty) {
                btnText.textContent = 'Lưu thay đổi *';
                saveBtn.classList.add('btn-primary');
                saveBtn.classList.remove('btn-secondary');
            } else {
                btnText.textContent = 'Đã lưu';
                saveBtn.classList.remove('btn-primary');
                saveBtn.classList.add('btn-secondary');
            }
        }

        // Show/hide unsaved badge
        if (unsavedBadge) {
            unsavedBadge.classList.toggle('is-hidden', !state.isDirty);
        }
    }

    // =========================================
    // SAVE FUNCTIONALITY
    // =========================================

    function initSaveShortcut() {
        document.addEventListener('keydown', (e) => {
            // Ctrl+S or Cmd+S
            if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 's') {
                e.preventDefault();

                const form = document.querySelector('form.portal-form');
                if (!form) return;

                triggerSave(form);
            }
        });
    }

    async function triggerSave(form) {
        if (state.isSaving) return;

        const submitBtn = form.querySelector('.btn-save-trigger');
        if (!submitBtn) {
            form.submit();
            return;
        }

        // Set loading state
        state.isSaving = true;
        submitBtn.classList.add('is-loading');
        submitBtn.disabled = true;

        showToast('Đang lưu...', 'info', 2000);

        // Trigger form submit
        submitBtn.click();
    }

    // =========================================
    // CONFIRMATIONS
    // =========================================

    function initConfirmations() {
        document.addEventListener('click', async (e) => {
            const target = e.target.closest('[data-confirm]');
            if (!target) return;

            e.preventDefault();
            e.stopPropagation();

            const message = target.dataset.confirm;
            const confirmed = await confirmModal({
                title: 'Xác nhận hành động',
                message: message,
                confirmText: 'Đồng ý',
                cancelText: 'Hủy',
                type: target.classList.contains('btn-danger') ? 'danger' : 'warning',
            });

            if (confirmed) {
                // If it's a form button, submit the form
                const form = target.closest('form');
                if (form) {
                    // Remove data-confirm temporarily to prevent loop
                    target.removeAttribute('data-confirm');
                    target.click();
                } else if (target.href) {
                    // If it's a link, navigate
                    window.location.href = target.href;
                }
            }
        });
    }

    // =========================================
    // SEARCH WITH DEBOUNCE
    // =========================================

    function initSearch() {
        const searchInputs = document.querySelectorAll('.portal-search input, input[type="search"]');

        searchInputs.forEach((input) => {
            const form = input.closest('form');
            if (!form) return;

            // Live search debounce (optional - only if form has data-live-search)
            if (form.dataset.liveSearch !== undefined) {
                input.addEventListener('input', debounce(() => {
                    form.submit();
                }, 500));
            }
        });
    }

    // =========================================
    // SELECT ALL CHECKBOX
    // =========================================

    function initSelectAll() {
        const selectAllCheckboxes = document.querySelectorAll('[data-select-all]');

        selectAllCheckboxes.forEach((selectAll) => {
            const targetName = selectAll.dataset.selectAll;
            const container = selectAll.closest('table') || document;
            const checkboxes = container.querySelectorAll(`input[name="${targetName}"]`);

            selectAll.addEventListener('change', () => {
                checkboxes.forEach((cb) => {
                    cb.checked = selectAll.checked;
                });
                updateSelectAllState(selectAll, checkboxes);
            });

            checkboxes.forEach((cb) => {
                cb.addEventListener('change', () => {
                    updateSelectAllState(selectAll, checkboxes);
                });
            });
        });
    }

    function updateSelectAllState(selectAll, checkboxes) {
        const checked = Array.from(checkboxes).filter((cb) => cb.checked);
        selectAll.checked = checked.length === checkboxes.length;
        selectAll.indeterminate = checked.length > 0 && checked.length < checkboxes.length;
    }

    // =========================================
    // FORM VALIDATION STYLING
    // =========================================

    function initFormValidation() {
        const forms = document.querySelectorAll('form.portal-form');

        forms.forEach((form) => {
            form.addEventListener('submit', (e) => {
                // Clear previous errors
                form.querySelectorAll('.is-invalid').forEach((el) => el.classList.remove('is-invalid'));

                // Check validity
                const invalidInputs = form.querySelectorAll(':invalid');
                if (invalidInputs.length > 0) {
                    e.preventDefault();
                    invalidInputs.forEach((input) => {
                        input.classList.add('is-invalid');
                    });
                    // Focus first invalid input
                    invalidInputs[0].focus();
                    showToast('Vui lòng kiểm tra lại thông tin.', 'error');
                }
            });

            // Remove invalid class on input
            form.addEventListener('input', (e) => {
                if (e.target.classList.contains('is-invalid')) {
                    e.target.classList.remove('is-invalid');
                }
            });
        });
    }

    // =========================================
    // RICH TEXT EDITOR INTEGRATION
    // =========================================

    function initRichTextSync() {
        // Sync TinyMCE changes to dirty state
        if (window.tinymce) {
            // Wait for TinyMCE to initialize
            setTimeout(() => {
                window.tinymce.get().forEach((editor) => {
                    editor.on('change keyup', () => {
                        const form = document.querySelector('form.portal-form');
                        if (form) {
                            form.dispatchEvent(new Event('input', { bubbles: true }));
                        }
                    });
                });
            }, 1000);
        }
    }

    // =========================================
    // DROPDOWNS
    // =========================================

    function initDropdowns() {
        const dropdowns = document.querySelectorAll('[data-dropdown]');

        dropdowns.forEach((dropdown) => {
            const trigger = dropdown.querySelector('[data-dropdown-trigger]');
            const menu = dropdown.querySelector('.portal-dropdown-menu');

            if (!trigger || !menu) return;

            // Toggle on click
            trigger.addEventListener('click', (e) => {
                e.stopPropagation();
                const isOpen = dropdown.classList.contains('is-open');

                // Close all other dropdowns
                closeAllDropdowns();

                if (!isOpen) {
                    dropdown.classList.add('is-open');
                    trigger.setAttribute('aria-expanded', 'true');

                    // Focus first item
                    const firstItem = menu.querySelector('.portal-dropdown-item');
                    if (firstItem) firstItem.focus();
                }
            });

            // Keyboard navigation
            menu.addEventListener('keydown', (e) => {
                const items = Array.from(menu.querySelectorAll('.portal-dropdown-item:not([disabled])'));
                const currentIndex = items.indexOf(document.activeElement);

                switch (e.key) {
                    case 'ArrowDown':
                        e.preventDefault();
                        const nextIndex = currentIndex < items.length - 1 ? currentIndex + 1 : 0;
                        items[nextIndex]?.focus();
                        break;
                    case 'ArrowUp':
                        e.preventDefault();
                        const prevIndex = currentIndex > 0 ? currentIndex - 1 : items.length - 1;
                        items[prevIndex]?.focus();
                        break;
                    case 'Escape':
                        e.preventDefault();
                        closeDropdown(dropdown);
                        trigger.focus();
                        break;
                    case 'Tab':
                        closeDropdown(dropdown);
                        break;
                }
            });
        });

        // Close on outside click
        document.addEventListener('click', (e) => {
            if (!e.target.closest('[data-dropdown]')) {
                closeAllDropdowns();
            }
        });

        // Close on ESC globally
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                closeAllDropdowns();
            }
        });
    }

    function closeDropdown(dropdown) {
        dropdown.classList.remove('is-open');
        const trigger = dropdown.querySelector('[data-dropdown-trigger]');
        if (trigger) trigger.setAttribute('aria-expanded', 'false');
    }

    function closeAllDropdowns() {
        document.querySelectorAll('[data-dropdown].is-open').forEach(closeDropdown);
    }

    // =========================================
    // ACCESSIBILITY ENHANCEMENTS
    // =========================================

    function initA11y() {
        // Add aria-labels to icon-only buttons
        document.querySelectorAll('.btn-icon:not([aria-label])').forEach((btn) => {
            const svg = btn.querySelector('svg');
            const title = svg?.querySelector('title')?.textContent;
            if (title) {
                btn.setAttribute('aria-label', title);
            }
        });

        // Ensure skip link exists
        const skipLink = document.querySelector('.skip-link');
        if (!skipLink) {
            const link = document.createElement('a');
            link.href = '#main-content';
            link.className = 'skip-link sr-only';
            link.textContent = 'Chuyển đến nội dung chính';
            link.addEventListener('focus', () => link.classList.remove('sr-only'));
            link.addEventListener('blur', () => link.classList.add('sr-only'));
            document.body.insertBefore(link, document.body.firstChild);
        }
    }

    // =========================================
    // INITIALIZATION
    // =========================================

    function init() {
        // Core features
        initSidebar();
        initTabs();
        initModals();
        initDropdowns();
        initUnsavedChanges();
        initSaveShortcut();
        initConfirmations();

        // Enhancements
        initSearch();
        initSelectAll();
        initFormValidation();
        initRichTextSync();
        initA11y();

        // Log initialization
        console.log('🚀 Portal MIS v2.0 initialized');
    }

    // =========================================
    // PUBLIC API
    // =========================================
    return {
        init,
        showToast,
        confirmModal,
        openModal,
        closeModal,
        closeSidebar,
        state,
    };
})();

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', Portal.init);

// Also expose globally for inline handlers
window.Portal = Portal;
