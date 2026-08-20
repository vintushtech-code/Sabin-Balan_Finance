/**
 * GuardianTree FP — Real-Time Live Financial Market Streaming Ticker (24/7 Engine)
 * ================================================================================
 * Features:
 * - Dual Streaming: Server-Sent Events (SSE) + High-Frequency Adaptive Polling Fallback
 * - 100% Dynamic 24/7 Rates for Indices, Forex, Commodities, Cryptocurrencies, and Equities
 * - In-place non-disruptive DOM updates without resetting CSS marquee scroll
 * - Micro-tick animations: Emerald Green Flash (Up) / Crimson Red Flash (Down)
 * - Live Market Clock (HH:MM:SS) updated every second
 * - Interactive Filter Pills & Detail Tooltip Popups
 */

(function () {
  'use strict';

  // Configuration
  const CONFIG = {
    streamEndpoint: '/api/market-stream/',
    ratesEndpoint: '/api/market-rates/',
    pollIntervalMs: 3000,
    maxReconnectAttempts: 10,
    reconnectDelayMs: 2000,
  };

  // State
  let eventSource = null;
  let pollTimer = null;
  let clockTimer = null;
  let activeCategory = 'all';
  let cachedRates = [];
  let isStreamActive = false;

  // DOM Elements
  const container = document.getElementById('market-ticker-container');
  const trackPrimary = document.getElementById('ticker-track-primary');
  const trackSecondary = document.getElementById('ticker-track-secondary');
  const liveDot = document.getElementById('ticker-live-dot');
  const liveClock = document.getElementById('ticker-live-clock');
  const filterButtons = document.querySelectorAll('.ticker-filter-btn');
  const tooltipModal = document.getElementById('ticker-detail-tooltip');

  if (!container || !trackPrimary) {
    return;
  }

  /**
   * Format numbers with commas and locale-aware precision
   */
  function formatNumber(num, precision = 2) {
    if (num === null || num === undefined || isNaN(num)) return '0.00';
    return Number(num).toLocaleString('en-US', {
      minimumFractionDigits: precision,
      maximumFractionDigits: precision,
    });
  }

  /**
   * Update the live market clock every second
   */
  function startLiveClock() {
    function updateClock() {
      if (liveClock) {
        const now = new Date();
        const timeStr = now.toLocaleTimeString('en-US', {
          hour12: false,
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
        });
        liveClock.textContent = `${timeStr} LIVE`;
      }
    }
    updateClock();
    if (clockTimer) clearInterval(clockTimer);
    clockTimer = setInterval(updateClock, 1000);
  }

  /**
   * Create HTML markup for a single ticker item
   */
  function createTickerItemHTML(item) {
    const isUp = item.direction === 'up' || (item.raw_change >= 0);
    const dirClass = isUp ? 'up' : 'down';
    const arrow = isUp ? '▲' : '▼';
    const changePct = item.formatted_change_pct || `${arrow} ${item.raw_change_pct >= 0 ? '+' : ''}${item.raw_change_pct}%`;
    const priceText = item.formatted_price || formatNumber(item.raw_price);

    return `
      <div class="ticker-item" data-id="${item.id}" data-category="${item.category}" title="Click for details on ${item.name || item.symbol}">
        <span class="ticker-cat-tag">${item.category ? item.category.toUpperCase().slice(0, 3) : 'MKT'}</span>
        <span class="ticker-symbol">${item.symbol}</span>
        <span class="ticker-price" data-price-for="${item.id}">${priceText}</span>
        <span class="ticker-change ${dirClass}" data-change-for="${item.id}">
          <span class="ticker-arrow">${arrow}</span> ${item.raw_change_pct >= 0 ? '+' : ''}${Math.abs(item.raw_change_pct || 0).toFixed(2)}%
        </span>
      </div>
    `;
  }

  /**
   * Render the complete list of rates into both primary and duplicate tracks
   */
  function renderAllRates(rates) {
    if (!rates || rates.length === 0) return;

    const filtered = activeCategory === 'all' 
      ? rates 
      : rates.filter(r => r.category && r.category.toLowerCase() === activeCategory.toLowerCase());

    const itemsHTML = (filtered.length > 0 ? filtered : rates).map(createTickerItemHTML).join('');

    trackPrimary.innerHTML = itemsHTML;
    if (trackSecondary) {
      trackSecondary.innerHTML = itemsHTML;
    }

    // Attach click listener for detail tooltip
    container.querySelectorAll('.ticker-item').forEach(el => {
      el.addEventListener('click', (e) => {
        e.stopPropagation();
        const itemId = el.getAttribute('data-id');
        showItemTooltip(itemId, el);
      });
    });
  }

  /**
   * Smooth in-place update of prices without resetting marquee scroll position
   */
  function updateRatesInPlace(rates) {
    if (!rates || rates.length === 0) return;
    cachedRates = rates;

    rates.forEach(item => {
      const priceEls = container.querySelectorAll(`[data-price-for="${item.id}"]`);
      const changeEls = container.querySelectorAll(`[data-change-for="${item.id}"]`);

      const isUp = item.direction === 'up' || (item.raw_change >= 0);
      const dirClass = isUp ? 'up' : 'down';
      const arrow = isUp ? '▲' : '▼';
      const newPriceText = item.formatted_price || formatNumber(item.raw_price);
      const newPctText = `<span class="ticker-arrow">${arrow}</span> ${item.raw_change_pct >= 0 ? '+' : ''}${Math.abs(item.raw_change_pct || 0).toFixed(2)}%`;

      priceEls.forEach(priceEl => {
        const oldText = priceEl.textContent.trim();
        if (oldText !== newPriceText) {
          priceEl.textContent = newPriceText;
          
          // Trigger visual flash
          const flashClass = isUp ? 'tick-flash-up' : 'tick-flash-down';
          priceEl.classList.remove('tick-flash-up', 'tick-flash-down');
          void priceEl.offsetWidth; // Force reflow
          priceEl.classList.add(flashClass);
          setTimeout(() => priceEl.classList.remove(flashClass), 900);
        }
      });

      changeEls.forEach(changeEl => {
        changeEl.className = `ticker-change ${dirClass}`;
        changeEl.innerHTML = newPctText;
      });
    });
  }

  /**
   * Display detailed popover/tooltip for clicked instrument
   */
  function showItemTooltip(itemId, targetElement) {
    const item = cachedRates.find(r => r.id === itemId);
    if (!item || !tooltipModal) return;

    const isUp = item.direction === 'up' || (item.raw_change >= 0);
    const color = isUp ? '#10B981' : '#EF4444';

    tooltipModal.innerHTML = `
      <div class="ticker-modal-card">
        <div class="ticker-modal-header">
          <div>
            <span class="ticker-modal-symbol">${item.symbol}</span>
            <span class="ticker-modal-name">${item.name || item.symbol}</span>
          </div>
          <button type="button" class="ticker-modal-close" id="ticker-modal-close-btn">&times;</button>
        </div>
        <div class="ticker-modal-body">
          <div class="ticker-modal-price-row">
            <span class="ticker-modal-price" style="color: ${color};">${item.formatted_price}</span>
            <span class="ticker-modal-badge ${isUp ? 'up' : 'down'}">${item.formatted_change_pct} (${item.formatted_change})</span>
          </div>
          <div class="ticker-modal-stats-grid">
            <div class="ticker-modal-stat">
              <span class="stat-label">Category</span>
              <span class="stat-val">${(item.category || 'Index').toUpperCase()}</span>
            </div>
            <div class="ticker-modal-stat">
              <span class="stat-label">Market State</span>
              <span class="stat-val" style="color: #10B981;">● ${item.market_state || 'REGULAR'}</span>
            </div>
            <div class="ticker-modal-stat">
              <span class="stat-label">24h Day High</span>
              <span class="stat-val">${item.high ? formatNumber(item.high) : '—'}</span>
            </div>
            <div class="ticker-modal-stat">
              <span class="stat-label">24h Day Low</span>
              <span class="stat-val">${item.low ? formatNumber(item.low) : '—'}</span>
            </div>
          </div>
          <div class="ticker-modal-footer">
            <span>Updated: ${item.updated_at || 'Just now'} (24/7 Live Stream)</span>
          </div>
        </div>
      </div>
    `;

    tooltipModal.style.display = 'flex';
    tooltipModal.setAttribute('aria-hidden', 'false');

    const closeBtn = document.getElementById('ticker-modal-close-btn');
    if (closeBtn) {
      closeBtn.onclick = () => {
        tooltipModal.style.display = 'none';
        tooltipModal.setAttribute('aria-hidden', 'true');
      };
    }
  }

  // Close tooltip when clicking outside
  if (tooltipModal) {
    tooltipModal.addEventListener('click', (e) => {
      if (e.target === tooltipModal) {
        tooltipModal.style.display = 'none';
        tooltipModal.setAttribute('aria-hidden', 'true');
      }
    });
  }

  /**
   * Connect to Server-Sent Events (SSE) Live Stream
   */
  function initSSEStream() {
    if (window.EventSource) {
      try {
        if (eventSource) {
          eventSource.close();
        }

        eventSource = new EventSource(CONFIG.streamEndpoint);

        eventSource.addEventListener('market_update', (e) => {
          try {
            const data = JSON.parse(e.data);
            if (data && data.rates) {
              isStreamActive = true;
              if (liveDot) liveDot.classList.add('active');
              
              if (trackPrimary.children.length === 0) {
                cachedRates = data.rates;
                renderAllRates(data.rates);
              } else {
                updateRatesInPlace(data.rates);
              }
            }
          } catch (err) {
            console.debug('Error parsing SSE market frame:', err);
          }
        });

        eventSource.onopen = () => {
          isStreamActive = true;
          if (liveDot) liveDot.classList.add('active');
          if (pollTimer) {
            clearInterval(pollTimer);
            pollTimer = null;
          }
        };

        eventSource.onerror = () => {
          isStreamActive = false;
          if (liveDot) liveDot.classList.remove('active');
          eventSource.close();
          // Fall back immediately to adaptive fast polling
          startPollingFallback();
        };
      } catch (err) {
        startPollingFallback();
      }
    } else {
      startPollingFallback();
    }
  }

  /**
   * Fallback: High-Frequency Polling
   */
  function fetchRatesViaHTTP() {
    const url = `${CONFIG.ratesEndpoint}?tick=1&_t=${Date.now()}`;
    fetch(url, { cache: 'no-store' })
      .then(res => res.json())
      .then(data => {
        if (data && data.rates) {
          if (liveDot) liveDot.classList.add('active');
          if (trackPrimary.children.length === 0) {
            cachedRates = data.rates;
            renderAllRates(data.rates);
          } else {
            updateRatesInPlace(data.rates);
          }
        }
      })
      .catch(err => {
        console.debug('Market rates polling error:', err);
        if (liveDot) liveDot.classList.remove('active');
      });
  }

  function startPollingFallback() {
    if (pollTimer) return;
    fetchRatesViaHTTP();
    pollTimer = setInterval(fetchRatesViaHTTP, CONFIG.pollIntervalMs);
  }

  /**
   * Initialize Category Filtering
   */
  function initFilterButtons() {
    filterButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        filterButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activeCategory = btn.getAttribute('data-cat') || 'all';
        renderAllRates(cachedRates);
      });
    });
  }

  /**
   * Bootstrap Ticker Component
   */
  function init() {
    startLiveClock();
    initFilterButtons();

    // Initial fetch to paint data immediately
    fetchRatesViaHTTP();

    // Launch SSE stream for continuous sub-second updates
    setTimeout(initSSEStream, 500);

    // Visibility change handler: pause when tab hidden, refresh immediately when focused
    document.addEventListener('visibilitychange', () => {
      if (!document.hidden) {
        fetchRatesViaHTTP();
        if (!isStreamActive) {
          initSSEStream();
        }
      }
    });
  }

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
