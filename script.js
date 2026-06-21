// ── NAV TOGGLE ──
const navToggle = document.getElementById('navToggle');
const navbar = document.getElementById('navbar');
navToggle?.addEventListener('click', () => navbar.classList.toggle('open'));
navbar?.querySelectorAll('.nav-link').forEach(link => {
  link.addEventListener('click', () => navbar.classList.remove('open'));
});

// ── HEADER SCROLL ──
const header = document.getElementById('header');
window.addEventListener('scroll', () => {
  header?.classList.toggle('scrolled', window.scrollY > 50);
});

// ── ACTIVE NAV ON SCROLL ──
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-link');
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      navLinks.forEach(link => {
        link.classList.toggle('active', link.getAttribute('href') === '#' + entry.target.id);
      });
    }
  });
}, { rootMargin: '-40% 0px -55% 0px' });
sections.forEach(s => observer.observe(s));

// ── PARTICLES ──
function createParticles() {
  const container = document.getElementById('particles');
  if (!container) return;
  for (let i = 0; i < 30; i++) {
    const p = document.createElement('div');
    const size = Math.random() * 3 + 1;
    p.style.cssText = `
      position: absolute;
      width: ${size}px;
      height: ${size}px;
      border-radius: 50%;
      background: ${Math.random() > 0.5 ? '#38bdf8' : '#f97316'};
      opacity: ${Math.random() * 0.4 + 0.05};
      left: ${Math.random() * 100}%;
      top: ${Math.random() * 100}%;
      animation: floatParticle ${Math.random() * 10 + 8}s ease-in-out infinite;
      animation-delay: ${Math.random() * 5}s;
    `;
    container.appendChild(p);
  }
}
const style = document.createElement('style');
style.textContent = `
  @keyframes floatParticle {
    0%, 100% { transform: translateY(0) translateX(0); opacity: 0.1; }
    33% { transform: translateY(-30px) translateX(15px); opacity: 0.4; }
    66% { transform: translateY(15px) translateX(-20px); opacity: 0.2; }
  }
`;
document.head.appendChild(style);
createParticles();

// ── STATS COUNTER ──
function animateCounter(el) {
  const target = parseInt(el.getAttribute('data-target'));
  const duration = 1800;
  const step = target / (duration / 16);
  let current = 0;
  const timer = setInterval(() => {
    current = Math.min(current + step, target);
    el.textContent = Math.floor(current);
    if (current >= target) clearInterval(timer);
  }, 16);
}

const statsObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const counters = entry.target.querySelectorAll('.stat-number');
      counters.forEach(c => animateCounter(c));
      statsObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.3 });

const statsSection = document.querySelector('.stats-section');
if (statsSection) statsObserver.observe(statsSection);

// ── LINA DEMO ──
const cmdBtns = document.querySelectorAll('.cmd-btn');
const userMsg = document.getElementById('demoUserMsg');
const linaMsg = document.getElementById('demoLinaMsg');
const linaStatus = document.getElementById('linaStatus');
let demoTimeout;

cmdBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    clearTimeout(demoTimeout);
    const cmd = btn.getAttribute('data-cmd');
    const res = btn.getAttribute('data-res');

    // Reset
    userMsg.classList.remove('visible');
    linaMsg.classList.remove('visible');
    linaStatus.textContent = 'Listening...';
    linaStatus.style.color = '#facc15';

    setTimeout(() => {
      userMsg.textContent = '🗣️ ' + cmd;
      userMsg.classList.add('visible');
      linaStatus.textContent = 'Processing...';
      linaStatus.style.color = '#f97316';
    }, 200);

    setTimeout(() => {
      linaMsg.textContent = '🤖 Lina™: ' + res;
      linaMsg.classList.add('visible');
      linaStatus.textContent = 'Ready';
      linaStatus.style.color = '#22c55e';
    }, 1200);
  });
});

// ── KIT SELECTOR QUIZ ──
const quizAnswers = {};
document.querySelectorAll('.quiz-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const step = parseInt(btn.getAttribute('data-step'));
    const val = btn.getAttribute('data-val');
    quizAnswers[step] = val;

    if (step === 1) {
      document.getElementById('qStep1').classList.remove('active');
      document.getElementById('qStep2').classList.add('active');
    } else if (step === 2) {
      document.getElementById('qStep2').classList.remove('active');
      document.getElementById('qStep3').classList.add('active');
    } else if (step === 3) {
      document.getElementById('qStep3').classList.remove('active');
      showQuizResult();
    }
  });
});

function showQuizResult() {
  const result = document.getElementById('quizResult');
  const kitName = document.getElementById('resultKit');
  const kitDesc = document.getElementById('resultDesc');

  // Always recommend Elite as flagship
  kitName.textContent = 'Horizon Link Elite';
  kitDesc.textContent = 'The Flagship Edition — complete automation for any home or business with advanced Lina™ voice control and up to 18 devices.';

  result.classList.add('active');
}

document.getElementById('quizRestart')?.addEventListener('click', () => {
  document.getElementById('quizResult').classList.remove('active');
  document.getElementById('qStep1').classList.add('active');
  Object.keys(quizAnswers).forEach(k => delete quizAnswers[k]);
});

// ── BACK TO TOP ──
const backTopBtn = document.getElementById('backToTop');
window.addEventListener('scroll', () => {
  backTopBtn?.classList.toggle('visible', window.scrollY > 400);
});
backTopBtn?.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

// ── FLOATING DEMO BUTTON ──
const floatingDemo = document.getElementById('floatingDemo');
window.addEventListener('scroll', () => {
  floatingDemo?.classList.toggle('visible', window.scrollY > 300);
});

// ── CHATBOT POPUP ──
const chatbotBtn = document.getElementById('chatbotBtn');
const popupOverlay = document.getElementById('popupOverlay');
const popupClose = document.getElementById('popupClose');

chatbotBtn?.addEventListener('click', () => popupOverlay.classList.add('open'));
popupClose?.addEventListener('click', () => popupOverlay.classList.remove('open'));
popupOverlay?.addEventListener('click', (e) => {
  if (e.target === popupOverlay) popupOverlay.classList.remove('open');
});

// ── SMOOTH SCROLL ──
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', (e) => {
    const target = document.querySelector(anchor.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// ── SCROLL REVEAL ──
const revealEls = document.querySelectorAll('.product-card, .team-card, .benefit-card, .about-item, .scene-card, .flow-step, .stat-item');
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = entry.target.style.transform?.includes('translateY(-') 
        ? entry.target.style.transform 
        : 'translateY(0)';
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });

revealEls.forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(20px)';
  el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
  revealObserver.observe(el);
});
