/**
 * GuardianTree FP — About Us Page Interactive Scripts
 * Handles Team Accordion Expansion, Slider Carousel Controls, Dots, and Mobile Touch Swipe.
 */

document.addEventListener("DOMContentLoaded", function () {
  const cards = document.querySelectorAll(".team-member-card");
  const controls = document.getElementById("team-controls");
  const dotsContainer = document.getElementById("team-dots");
  const prevBtn = document.getElementById("team-prev-btn");
  const nextBtn = document.getElementById("team-next-btn");

  if (!cards || cards.length === 0) return;

  let currentIdx = 0;
  const visibleCount = 4;
  const totalCount = cards.length;

  function updateSlider() {
    // 1. Update the visibility of the cards
    cards.forEach((card, idx) => {
      if (totalCount > visibleCount) {
        if (idx >= currentIdx && idx < currentIdx + visibleCount) {
          card.classList.remove("team-member-hidden");
        } else {
          card.classList.add("team-member-hidden");
        }
      } else {
        card.classList.remove("team-member-hidden");
      }

      // Remove active-first from all cards
      card.classList.remove("active-first");
    });

    // 2. Set the first visible card as active-first (expanded when accordion is not hovered)
    const firstVisibleCard = cards[currentIdx];
    if (firstVisibleCard) {
      firstVisibleCard.classList.add("active-first");
    }

    // 3. Update the dot active states
    if (totalCount > visibleCount && dotsContainer) {
      const dots = dotsContainer.querySelectorAll(".team-slider-dot");
      dots.forEach((dot, idx) => {
        dot.classList.toggle("active", idx === currentIdx);
      });

      // 4. Update disabled state of navigation buttons
      if (prevBtn) prevBtn.disabled = (currentIdx === 0);
      if (nextBtn) nextBtn.disabled = (currentIdx === totalCount - visibleCount);
    }
  }

  if (totalCount > visibleCount && controls && dotsContainer && prevBtn && nextBtn) {
    // Show controls
    controls.style.display = "flex";

    // Generate navigation dots (totalCount - visibleCount + 1 dots)
    const dotCount = totalCount - visibleCount + 1;
    for (let i = 0; i < dotCount; i++) {
      const dot = document.createElement("button");
      dot.className = "team-slider-dot";
      dot.setAttribute("aria-label", `Go to team members starting from ${i + 1}`);
      dot.addEventListener("click", function () {
        currentIdx = i;
        updateSlider();
      });
      dotsContainer.appendChild(dot);
    }

    // Prev and Next Button Listeners
    prevBtn.addEventListener("click", function () {
      if (currentIdx > 0) {
        currentIdx--;
        updateSlider();
      }
    });

    nextBtn.addEventListener("click", function () {
      if (currentIdx < totalCount - visibleCount) {
        currentIdx++;
        updateSlider();
      }
    });

    // Mobile touch swipe support
    const accordion = document.querySelector(".team-members-accordion");
    if (accordion) {
      let touchStartX = 0;
      let touchEndX = 0;

      accordion.addEventListener("touchstart", function (e) {
        touchStartX = e.changedTouches[0].screenX;
      }, { passive: true });

      accordion.addEventListener("touchend", function (e) {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
      }, { passive: true });

      function handleSwipe() {
        const swipeThreshold = 50; // pixels
        if (touchStartX - touchEndX > swipeThreshold) {
          // Swiped left -> Next
          if (currentIdx < totalCount - visibleCount) {
            currentIdx++;
            updateSlider();
          }
        } else if (touchEndX - touchStartX > swipeThreshold) {
          // Swiped right -> Prev
          if (currentIdx > 0) {
            currentIdx--;
            updateSlider();
          }
        }
      }
    }
  }

  // Initialize slider state
  updateSlider();
});
