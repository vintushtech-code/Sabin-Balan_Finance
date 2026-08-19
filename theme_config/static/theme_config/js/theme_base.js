/**
 * GuardianTree FP — Master Base Theme & Accessibility Engine
 * Handles toast notifications, dynamic theme states, blind mode speech narration,
 * and floating accessibility console controls.
 */

// 1. Toast Notification Management
document.addEventListener('DOMContentLoaded', function () {
  const toasts = document.querySelectorAll('.toast-message-item');
  toasts.forEach(function (toast) {
    setTimeout(function () {
      dismissToast(toast);
    }, 3000);
  });

  // Restore saved accessibility preferences on load
  initAccessibilityModes();
});

function dismissToast(toastEl) {
  if (!toastEl || toastEl.classList.contains('dismissing')) return;
  toastEl.classList.add('dismissing');
  toastEl.style.animation = 'toastSlideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards';
  setTimeout(function () {
    if (toastEl.parentElement) {
      toastEl.remove();
    }
  }, 400);
}

function showToast(message, type = 'info') {
  const container = document.getElementById('toast-messages-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast-message-item alert-${type}`;
  toast.setAttribute('role', 'alert');

  let icon = 'ℹ';
  if (type === 'success') icon = '✓';
  else if (type === 'error' || type === 'danger') icon = '✕';

  toast.innerHTML = `
    <div class="toast-message-content">
      <span class="toast-icon">${icon}</span>
      <span class="toast-text">${message}</span>
    </div>
    <button type="button" class="toast-close-btn" onclick="dismissToast(this.parentElement)" aria-label="Close notification">&times;</button>
    <div class="toast-progress-bar"></div>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    dismissToast(toast);
  }, 3200);
}

// 2. Blind Mode Audio Speech Synthesis Engine
let speechEnabled = false;
let speechThrottleTimeout = null;

function speakText(text, priority = false) {
  if (!('speechSynthesis' in window)) return;
  if (!speechEnabled && !priority) return;

  try {
    window.speechSynthesis.cancel(); // Stop prior narration immediately
    const cleanText = text.trim();
    if (!cleanText) return;

    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    utterance.volume = 1.0;
    window.speechSynthesis.speak(utterance);
  } catch (e) {
    console.error('Speech synthesis error:', e);
  }
}

function setupBlindModeListeners() {
  const narratableSelectors = 'a, button, input, select, textarea, h1, h2, h3, h4, h5, h6, p, img, li, .utility-item, .admin-metric-card, .admin-sidebar-link';
  
  document.removeEventListener('focusin', handleElementNarration);
  document.removeEventListener('mouseover', handleElementNarration);

  if (speechEnabled) {
    document.addEventListener('focusin', handleElementNarration, true);
    document.addEventListener('mouseover', handleElementNarration, true);
  }
}

function handleElementNarration(e) {
  if (!speechEnabled) return;
  const target = e.target.closest('a, button, input, select, textarea, h1, h2, h3, h4, p, img, li');
  if (!target) return;

  clearTimeout(speechThrottleTimeout);
  speechThrottleTimeout = setTimeout(() => {
    let narration = '';
    const tagName = target.tagName.toLowerCase();

    if (tagName === 'a') {
      narration = `Link: ${target.innerText || target.getAttribute('aria-label') || target.title || 'Navigation link'}`;
    } else if (tagName === 'button') {
      narration = `Button: ${target.innerText || target.getAttribute('aria-label') || target.title || 'Action button'}`;
    } else if (tagName === 'img') {
      narration = `Image: ${target.alt || target.title || 'Graphic visual'}`;
    } else if (tagName === 'input') {
      narration = `Input field: ${target.placeholder || target.getAttribute('aria-label') || target.name || 'Text input'}`;
    } else if (['h1', 'h2', 'h3', 'h4'].includes(tagName)) {
      narration = `Heading: ${target.innerText}`;
    } else {
      narration = target.innerText || target.textContent || '';
    }

    if (narration && narration.length < 150) {
      speakText(narration);
    }
  }, 120);
}

// 3. Floating Accessibility Control Console
const ACCESS_MODES = [
  { id: 'access-btn-blind', class: 'access-blind-mode', label: 'Blind / Speech Assist' },
  { id: 'access-btn-contrast', class: 'access-high-contrast', label: 'High Contrast' },
  { id: 'access-btn-text', class: 'access-large-text', label: 'Larger Text' },
  { id: 'access-btn-font', class: 'access-readable-font', label: 'Readable Font' },
  { id: 'access-btn-links', class: 'access-highlight-links', label: 'Highlight Links' },
  { id: 'access-btn-motion', class: 'access-reduced-motion', label: 'Reduced Motion' }
];

function toggleAccessibilityPanel() {
  const panel = document.getElementById('accessibility-panel');
  if (panel) {
    panel.classList.toggle('active');
  }
}

function closeAccessibilityPanel() {
  const panel = document.getElementById('accessibility-panel');
  if (panel) {
    panel.classList.remove('active');
  }
}

function toggleAccessMode(modeClass, modeLabel) {
  const html = document.documentElement;
  const isEnabled = html.classList.toggle(modeClass);

  // Handle Blind Speech Mode specifically
  if (modeClass === 'access-blind-mode') {
    speechEnabled = isEnabled;
    setupBlindModeListeners();
    if (isEnabled) {
      speakText("Blind accessibility mode enabled. Hover or navigate through elements to listen.", true);
    } else {
      if ('speechSynthesis' in window) window.speechSynthesis.cancel();
      speakText("Blind mode disabled.", true);
    }
  }

  // Save to localStorage
  try {
    const saved = JSON.parse(localStorage.getItem('gtfp-access-modes') || '{}');
    saved[modeClass] = isEnabled;
    localStorage.setItem('gtfp-access-modes', JSON.stringify(saved));
  } catch (e) {
    console.error('Failed to save accessibility preference:', e);
  }

  // Update button active states and badge count in UI
  syncAccessibilityButtons();

  if (isEnabled) {
    showToast(`${modeLabel} activated.`, 'success');
  } else {
    showToast(`${modeLabel} turned off (reset).`, 'info');
  }
}

function resetAccessibilityModes() {
  const html = document.documentElement;
  ACCESS_MODES.forEach(mode => {
    html.classList.remove(mode.class);
  });

  speechEnabled = false;
  if ('speechSynthesis' in window) window.speechSynthesis.cancel();
  setupBlindModeListeners();

  try {
    localStorage.removeItem('gtfp-access-modes');
  } catch (e) {}

  syncAccessibilityButtons();
  showToast('All accessibility modes reset to default.', 'info');
  speakText("All accessibility modes have been reset to default.", true);
}

function syncAccessibilityButtons() {
  const html = document.documentElement;
  let activeCount = 0;

  ACCESS_MODES.forEach(mode => {
    const btn = document.getElementById(mode.id);
    const isModeActive = html.classList.contains(mode.class);

    if (isModeActive) activeCount++;

    if (btn) {
      const statusText = btn.querySelector('.accessibility-status-text');
      if (isModeActive) {
        btn.classList.add('active');
        if (statusText) statusText.textContent = 'ON';
      } else {
        btn.classList.remove('active');
        if (statusText) statusText.textContent = 'OFF';
      }
    }
  });

  // Update active count badge on the floating button
  const badge = document.getElementById('accessibility-active-badge');
  if (badge) {
    if (activeCount > 0) {
      badge.textContent = activeCount;
      badge.style.display = 'flex';
    } else {
      badge.style.display = 'none';
    }
  }
}

function initAccessibilityModes() {
  try {
    const saved = JSON.parse(localStorage.getItem('gtfp-access-modes') || '{}');
    const html = document.documentElement;
    ACCESS_MODES.forEach(mode => {
      if (saved[mode.class]) {
        html.classList.add(mode.class);
        if (mode.class === 'access-blind-mode') {
          speechEnabled = true;
          setupBlindModeListeners();
        }
      }
    });
    syncAccessibilityButtons();
  } catch (e) {
    console.error('Failed to restore accessibility preferences:', e);
  }
}

// Close panel when clicking outside
document.addEventListener('click', function (e) {
  const widget = document.getElementById('accessibility-widget');
  const panel = document.getElementById('accessibility-panel');
  if (widget && panel && panel.classList.contains('active')) {
    if (!widget.contains(e.target)) {
      closeAccessibilityPanel();
    }
  }
});
