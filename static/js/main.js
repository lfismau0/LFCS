// ── Back to Top ──
const backToTop = document.getElementById('backToTop');
window.addEventListener('scroll', () => {
  if (backToTop) {
    if (window.scrollY > 300) backToTop.classList.add('visible');
    else backToTop.classList.remove('visible');
  }
});
if (backToTop) {
  backToTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
}

// ── Navbar scroll shrink / shadow ──
window.addEventListener('scroll', () => {
  const nav = document.getElementById('mainNav');
  if (nav) {
    nav.classList.toggle('scrolled', window.scrollY > 40);
    nav.classList.toggle('shadow', window.scrollY > 60);
  }
});

// ── Popup (once per session) ──
// Wait until Bootstrap is FULLY ready before showing the popup modal.
// This prevents the modal backdrop from blocking the page if Bootstrap JS
// hasn't finished initialising its event listeners on first load.
function showPopup() {
  const popupEl = document.getElementById('popupModal');
  if (!popupEl) return;
  if (sessionStorage.getItem('popupShown')) return;

  try {
    const modal = new bootstrap.Modal(popupEl, { keyboard: true, backdrop: true });
    modal.show();
    sessionStorage.setItem('popupShown', '1');

    // Extra safety: if the modal doesn't hide within 30s, force-remove it
    const safetyTimer = setTimeout(() => {
      try { modal.hide(); } catch (_) { }
      popupEl.remove();
    }, 30000);

    popupEl.addEventListener('hidden.bs.modal', () => {
      clearTimeout(safetyTimer);
    }, { once: true });
  } catch (e) {
    // Bootstrap not available yet – skip popup
    console.warn('Popup skipped: Bootstrap not ready', e);
  }
}

// Delay popup until after page is fully interactive (all scripts loaded)
window.addEventListener('load', () => {
  setTimeout(showPopup, 1800);   // 1.8s after full page load (not just DOMContentLoaded)
});

// ── Staff department filter ──
function filterDept(dept) {
  document.querySelectorAll('.staff-card-wrap').forEach(card => {
    const d = card.dataset.dept;
    card.style.display = (!dept || d === dept) ? '' : 'none';
  });
  document.querySelectorAll('.dept-tab').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.dept === dept);
  });
}

// ── Alumni batch filter ──
function filterBatch(batch) {
  document.querySelectorAll('.alumni-card-wrap').forEach(card => {
    const b = card.dataset.batch;
    card.style.display = (!batch || b === batch) ? '' : 'none';
  });
}

// ── Lightbox for gallery ──
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.gallery-item').forEach(item => {
    item.addEventListener('click', () => {
      const imgEl = item.querySelector('img');
      if (!imgEl) return;
      const src = imgEl.src;
      const overlay = document.createElement('div');
      overlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,.92);z-index:9999;display:flex;align-items:center;justify-content:center;cursor:pointer;';
      overlay.innerHTML = `<img src="${src}" style="max-width:90vw;max-height:90vh;border-radius:8px;box-shadow:0 0 60px rgba(0,0,0,.8);">`;
      overlay.addEventListener('click', () => overlay.remove());
      document.body.appendChild(overlay);
    });
  });
});

// ── Animated counter for stat numbers ──
function animateCounter(el, target, duration = 1800) {
  let start = 0;
  const step = target / (duration / 16);
  const suffix = el.textContent.replace(/[0-9]/g, '').trim();
  const timer = setInterval(() => {
    start = Math.min(start + step, target);
    el.textContent = Math.floor(start) + suffix;
    if (start >= target) clearInterval(timer);
  }, 16);
}

// ── Intersection Observer for counters & fade-ins ──
document.addEventListener('DOMContentLoaded', () => {
  // Animate stat counts when visible
  const statNums = document.querySelectorAll('.stat-num, [data-count]');
  if (statNums.length) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const raw = el.textContent.replace(/[^0-9]/g, '');
          if (raw) animateCounter(el, parseInt(raw));
          observer.unobserve(el);
        }
      });
    }, { threshold: 0.5 });
    statNums.forEach(el => observer.observe(el));
  }

  // ── Section fade-in on scroll ──
  // IMPORTANT: sections above the fold (already visible) are revealed
  // immediately via the 'immediate' class to avoid the first-load blank issue.
  const sections = document.querySelectorAll('section');
  const viewportH = window.innerHeight;

  sections.forEach(s => {
    const rect = s.getBoundingClientRect();
    // If section is already in the viewport on page load, show it immediately
    if (rect.top < viewportH) {
      s.style.opacity = '1';
      s.style.transform = 'translateY(0)';
      s.style.transition = 'none';
    } else {
      s.style.opacity = '0';
      s.style.transform = 'translateY(28px)';
      s.style.transition = 'opacity .6s ease, transform .6s ease';
    }
  });

  const fadeObs = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        fadeObs.unobserve(entry.target);
      }
    });
  }, { threshold: 0.05, rootMargin: '0px 0px -20px 0px' });

  sections.forEach(s => {
    if (s.style.opacity !== '1') fadeObs.observe(s);
  });

  // Safety fallback: reveal ALL sections after 2s regardless
  setTimeout(() => {
    sections.forEach(s => {
      s.style.opacity = '1';
      s.style.transform = 'translateY(0)';
    });
  }, 2000);

  // Re-animate banner captions on slide change
  const carousel = document.getElementById('bannerCarousel');
  if (carousel) {
    carousel.addEventListener('slide.bs.carousel', () => {
      const caps = carousel.querySelectorAll('.carousel-caption > *');
      caps.forEach(el => { el.style.opacity = '0'; el.style.animation = 'none'; });
    });
    carousel.addEventListener('slid.bs.carousel', () => {
      const active = carousel.querySelector('.carousel-item.active .carousel-caption');
      if (!active) return;
      active.querySelectorAll('.caption-eyebrow').forEach((el, i) => {
        el.style.animation = `fadeInUp .7s ${0.3 + i * 0.2}s forwards`;
      });
      active.querySelectorAll('h5').forEach(el => { el.style.animation = 'fadeInUp .7s .5s forwards'; });
      active.querySelectorAll('p').forEach(el => { el.style.animation = 'fadeInUp .7s .7s forwards'; });
      active.querySelectorAll('.hero-cta').forEach(el => { el.style.animation = 'fadeInUp .7s .9s forwards'; });
    });
  }
});
