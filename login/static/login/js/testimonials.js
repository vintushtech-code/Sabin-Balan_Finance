/**
 * GuardianTree FP — Client Testimonials Interactive Controller
 * Handles modal popups, review details, submission form modal, keyword search and leader grid filters.
 */

var activeCategory = 'all';

function openReviewModal(name, role, location, quote, rating, avatar, highlight) {
  const mName = document.getElementById('mName');
  const mRole = document.getElementById('mRole');
  const mLocation = document.getElementById('mLocation');
  const mQuote = document.getElementById('mQuote');
  const mStars = document.getElementById('mStars');
  const mHighlight = document.getElementById('mHighlight');

  if (mName) mName.textContent = name;
  if (mRole) mRole.textContent = role;
  if (mLocation) mLocation.textContent = '📍 ' + location;
  if (mQuote) mQuote.textContent = '"' + quote + '"';
  if (mStars) mStars.textContent = rating;
  if (mHighlight) mHighlight.textContent = highlight || 'Verified Fiduciary Account';

  const avatarWrapper = document.getElementById('mAvatarWrapper');
  if (avatarWrapper) {
    if (avatar && avatar !== '') {
      avatarWrapper.innerHTML = `<img id="mAvatar" src="${avatar}" alt="${name}" style="width: 64px; height: 64px; border-radius: 50%; object-fit: cover; border: 2px solid var(--color-gold); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);">`;
    } else {
      const firstLetter = (name && name.length > 0) ? name.charAt(0).toUpperCase() : 'U';
      avatarWrapper.innerHTML = `
        <div style="width: 64px; height: 64px; border-radius: 50%; background: linear-gradient(135deg, #FFD700 0%, #F59E0B 100%); color: #0A0D14; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.6rem; border: 2px solid var(--color-gold); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);">
          ${firstLetter}
        </div>
      `;
    }
  }

  const modal = document.getElementById('detailModal');
  if (modal) modal.classList.add('active');
}

function closeReviewModal(e) {
  const detailModal = document.getElementById('detailModal');
  if (e && e.target !== detailModal && !e.target.classList.contains('modal-close-btn')) {
    return;
  }
  if (detailModal) detailModal.classList.remove('active');
}

function openWriteModal() {
  const modal = document.getElementById('writeModal');
  if (modal) modal.classList.add('active');
}

function closeWriteModal(e) {
  const writeModal = document.getElementById('writeModal');
  if (e && e.target !== writeModal && !e.target.classList.contains('modal-close-btn')) {
    return;
  }
  if (writeModal) writeModal.classList.remove('active');
}

function filterCategory(btn) {
  const btns = document.querySelectorAll('.dock-filter-btn');
  btns.forEach(b => b.classList.remove('active'));
  if (btn) {
    btn.classList.add('active');
    activeCategory = btn.getAttribute('data-category');
  }
  applyCombinedFilters();
}

function filterLeadersGrid() {
  applyCombinedFilters();
}

function applyCombinedFilters() {
  const dockInput = document.getElementById('dockSearchInput');
  const query = dockInput ? dockInput.value.toLowerCase().trim() : '';
  const portraitCards = document.querySelectorAll('.leader-portrait-card');

  portraitCards.forEach(card => {
    const cardOnclick = card.getAttribute('onclick') || '';
    const lowerOnclick = cardOnclick.toLowerCase();

    // Category Match
    let categoryMatch = false;
    if (activeCategory === 'all') {
      categoryMatch = true;
    } else if (activeCategory === 'entrepreneur' && lowerOnclick.includes('entrepreneur')) {
      categoryMatch = true;
    } else if (activeCategory === 'portfolio_manager' && lowerOnclick.includes('portfolio manager')) {
      categoryMatch = true;
    } else if (activeCategory === 'saver' && lowerOnclick.includes('saver')) {
      categoryMatch = true;
    } else if (activeCategory === 'institutional' && (lowerOnclick.includes('trustee') || lowerOnclick.includes('executive') || lowerOnclick.includes('institutional'))) {
      categoryMatch = true;
    }

    // Keyword Match
    let keywordMatch = false;
    if (!query || lowerOnclick.includes(query)) {
      keywordMatch = true;
    }

    const colElement = card.parentElement;
    if (categoryMatch && keywordMatch) {
      if (colElement) colElement.style.display = 'flex';
      card.style.opacity = '1';
      card.style.transform = 'scale(1)';
      card.style.pointerEvents = 'auto';
    } else {
      card.style.opacity = '0.15';
      card.style.transform = 'scale(0.85)';
      card.style.pointerEvents = 'none';
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  const heroSearch = document.getElementById('testimonialSearchInput');
  if (heroSearch) {
    heroSearch.addEventListener('keyup', () => {
      const query = heroSearch.value;
      const dockInput = document.getElementById('dockSearchInput');
      if (dockInput) dockInput.value = query;
      applyCombinedFilters();
    });
  }
});
