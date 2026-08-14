/**
 * GuardianTree FP — Master Navbar & Mobile Navigation Drawer Scripts
 */

(function () {
  const saved = localStorage.getItem('bf-theme');
  if (saved === 'dark') {
    document.documentElement.setAttribute('data-theme', 'dark');
    window.addEventListener('DOMContentLoaded', () => {
      const dropdownIcon = document.getElementById('theme-icon-dropdown');
      if (dropdownIcon) dropdownIcon.textContent = '☀️';
    });
  }
})();

function handleNavbarScroll() {
  const wrapper = document.querySelector('.finance-navbar-wrapper');
  if (wrapper) {
    if (window.scrollY > 20) {
      wrapper.classList.add('scrolled');
    } else {
      wrapper.classList.remove('scrolled');
    }
  }
}
window.addEventListener('scroll', handleNavbarScroll);
window.addEventListener('DOMContentLoaded', handleNavbarScroll);

function toggleTheme() {
  const html = document.documentElement;
  const isDark = html.getAttribute('data-theme') === 'dark';
  const nextTheme = isDark ? 'light' : 'dark';
  const nextIcon = isDark ? '🌙' : '☀️';

  if (isDark) {
    html.removeAttribute('data-theme');
  } else {
    html.setAttribute('data-theme', 'dark');
  }
  localStorage.setItem('bf-theme', nextTheme);

  const dropdownIcon = document.getElementById('theme-icon-dropdown');
  if (dropdownIcon) dropdownIcon.textContent = nextIcon;

  const mobileIcon = document.getElementById('mobile-theme-icon');
  if (mobileIcon) mobileIcon.textContent = nextIcon;
}

function toggleUserDropdown(event) {
  if (event) event.stopPropagation();
  const dropdown = document.getElementById('user-dropdown-menu');
  if (dropdown) {
    dropdown.classList.toggle('show');
  }
}

function toggleMobileDrawer(event) {
  if (event) event.stopPropagation();
  const drawer = document.getElementById('finance-mobile-drawer');
  const toggle = document.getElementById('finance-hamburger-toggle');
  const overlay = document.getElementById('finance-mobile-drawer-overlay');

  if (drawer) drawer.classList.toggle('open');
  if (toggle) toggle.classList.toggle('active');

  if (overlay) {
    if (drawer && drawer.classList.contains('open')) {
      overlay.style.display = 'block';
      document.body.style.overflow = 'hidden';
    } else {
      overlay.style.display = 'none';
      document.body.style.overflow = '';
    }
  }
}

document.addEventListener('click', function (event) {
  const dropdown = document.getElementById('user-dropdown-menu');
  const trigger = document.getElementById('settings-dropdown-trigger');
  if (dropdown && dropdown.classList.contains('show')) {
    if (!dropdown.contains(event.target) && (!trigger || !trigger.contains(event.target))) {
      dropdown.classList.remove('show');
    }
  }
});
