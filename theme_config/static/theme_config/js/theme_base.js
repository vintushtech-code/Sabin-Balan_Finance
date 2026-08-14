/**
 * GuardianTree FP — Master Base Theme & Utility Script
 * Handles toast notifications, dynamic theme states, and live chat assistant.
 */

// 1. Toast Notification Management
document.addEventListener('DOMContentLoaded', function () {
  const toasts = document.querySelectorAll('.toast-message-item');
  toasts.forEach(function (toast) {
    setTimeout(function () {
      dismissToast(toast);
    }, 3000);
  });
});

function dismissToast(toastEl) {
  if (!toastEl || toastEl.classList.contains('dismissing')) return;
  toastEl.classList.add('dismissing');
  toastEl.style.animation = 'toastSlideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards';
  setTimeout(function () {
    if (toastEl.parentElement && toastEl.parentElement.querySelectorAll('.toast-message-item').length === 1) {
      toastEl.remove();
    } else {
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
  }, 3000);
}

// 2. Interactive Live Chat Assistant
function toggleChatPanel() {
  const panel = document.getElementById('chat-panel');
  if (panel) {
    panel.classList.toggle('active');
  }
}

function closeChatPanel() {
  const panel = document.getElementById('chat-panel');
  if (panel) {
    panel.classList.remove('active');
  }
}

function sendChatMessage() {
  const input = document.getElementById('chat-input-field');
  const body = document.getElementById('chat-body');
  if (!input || !body) return;

  const text = input.value.trim();
  if (!text) return;

  const userMsg = document.createElement('div');
  userMsg.className = 'chat-message user';
  userMsg.textContent = text;
  body.appendChild(userMsg);

  input.value = '';
  body.scrollTop = body.scrollHeight;

  const typingInd = document.createElement('div');
  typingInd.className = 'typing-indicator';
  typingInd.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';
  body.appendChild(typingInd);
  body.scrollTop = body.scrollHeight;

  setTimeout(() => {
    if (body.contains(typingInd)) body.removeChild(typingInd);

    const botMsg = document.createElement('div');
    botMsg.className = 'chat-message bot';

    const lowerText = text.toLowerCase();
    let reply = "Thank you for your message. An advisor will be with you shortly.";
    if (lowerText.includes('hello') || lowerText.includes('hi')) {
      reply = "Hello! How can we assist you with our wealth management services?";
    } else if (lowerText.includes('pricing') || lowerText.includes('cost') || lowerText.includes('fee')) {
      reply = "Our advisory fees are structured transparently based on AUM. We'd love to schedule a consultation to discuss this in detail.";
    } else if (lowerText.includes('help')) {
      reply = "Sure! You can navigate to 'Services' in the menu or book a consultation below.";
    }

    botMsg.textContent = reply;
    body.appendChild(botMsg);
    body.scrollTop = body.scrollHeight;
  }, 1500);
}
