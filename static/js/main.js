/* Portfolio — main.js */
'use strict';

// ── Mobile nav toggle ────────────────────────────────────────
const toggle = document.querySelector('.nav-toggle');
const nav    = document.querySelector('.site-nav');
if (toggle && nav) {
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', open);
  });
  // Close on outside click
  document.addEventListener('click', e => {
    if (!nav.contains(e.target) && !toggle.contains(e.target)) {
      nav.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
    }
  });
  // Close on Escape
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      nav.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
    }
  });
}

// ── Dismiss flash messages ───────────────────────────────────
document.querySelectorAll('.message-close').forEach(btn => {
  btn.addEventListener('click', () => {
    const msg = btn.closest('.message');
    msg.style.opacity = '0';
    msg.style.transform = 'translateX(20px)';
    msg.style.transition = 'all 0.25s ease';
    setTimeout(() => msg.remove(), 260);
  });
});
// Auto-dismiss after 6s
setTimeout(() => {
  document.querySelectorAll('.message').forEach(msg => {
    msg.style.opacity = '0';
    msg.style.transform = 'translateX(20px)';
    msg.style.transition = 'all 0.4s ease';
    setTimeout(() => msg.remove(), 420);
  });
}, 6000);

// ── Scroll-reveal animation ──────────────────────────────────
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll(
    '.post-card, .project-card, .subject-card, .subject-detail-card, .stat'
  ).forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.45s ease, transform 0.45s ease';
    observer.observe(el);
  });

  document.addEventListener('animationend', () => {}, {once:true});
}

// Add visible class styles via JS
const style = document.createElement('style');
style.textContent = '.visible { opacity: 1 !important; transform: translateY(0) !important; }';
document.head.appendChild(style);

// ── Active nav link on scroll (single-page sections) ─────────
// (Only applies to pages with anchor sections)
const navLinks = document.querySelectorAll('.site-nav a[href^="#"]');
if (navLinks.length) {
  const sections = Array.from(navLinks).map(a => document.querySelector(a.getAttribute('href'))).filter(Boolean);
  window.addEventListener('scroll', () => {
    const scrollY = window.scrollY + 120;
    sections.forEach((section, i) => {
      if (section.offsetTop <= scrollY && section.offsetTop + section.offsetHeight > scrollY) {
        navLinks.forEach(l => l.classList.remove('active'));
        navLinks[i].classList.add('active');
      }
    });
  }, { passive: true });
}

// ── Copy code blocks ─────────────────────────────────────────
document.querySelectorAll('.prose pre').forEach(pre => {
  const btn = document.createElement('button');
  btn.textContent = 'Copy';
  btn.style.cssText = 'position:absolute;top:.6rem;right:.6rem;font-size:.75rem;padding:.25rem .6rem;border:1px solid rgba(255,255,255,.3);border-radius:4px;background:rgba(255,255,255,.1);color:rgba(255,255,255,.8);cursor:pointer;transition:all .2s;';
  btn.addEventListener('click', () => {
    navigator.clipboard.writeText(pre.querySelector('code')?.textContent || pre.textContent)
      .then(() => { btn.textContent = 'Copied!'; setTimeout(() => btn.textContent = 'Copy', 2000); });
  });
  pre.style.position = 'relative';
  pre.appendChild(btn);
});
