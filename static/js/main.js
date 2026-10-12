(function () {
  const $ = (sel, root) => (root || document).querySelector(sel);
  const $$ = (sel, root) => Array.from((root || document).querySelectorAll(sel));
  const root = document.documentElement;

  // ----- Dark mode (remembered) -----
  const themeBtn = $('#theme-toggle');
  function paintThemeBtn() {
    if (themeBtn) themeBtn.textContent = root.classList.contains('dark') ? 'Light' : 'Dark';
  }
  paintThemeBtn();
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      root.classList.toggle('dark');
      try { localStorage.setItem('theme', root.classList.contains('dark') ? 'dark' : 'light'); } catch (e) {}
      paintThemeBtn();
    });
  }

  // ----- Mobile menu -----
  const menuBtn = $('#menu-btn');
  const navLinks = $('#nav-links');
  if (menuBtn && navLinks) {
    menuBtn.addEventListener('click', function () { navLinks.classList.toggle('open'); });
  }

  // ----- Toast messages fade out -----
  $$('.toast').forEach(function (t) {
    setTimeout(function () { t.style.opacity = '0'; }, 4000);
    setTimeout(function () { t.remove(); }, 4500);
  });

  // ----- Typing effect on the public profile tagline -----
  const typing = $('#typing');
  if (typing && typing.dataset.text) {
    const text = typing.dataset.text;
    let i = 0;
    typing.textContent = '';
    (function type() {
      typing.textContent = text.slice(0, i++);
      if (i <= text.length) setTimeout(type, 60);
    })();
  }

  // ----- Skill bars fill when they scroll into view -----
  const fills = $$('.fill[data-level]');
  if (fills.length) {
    if ('IntersectionObserver' in window) {
      const obs = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            e.target.style.width = e.target.dataset.level + '%';
            obs.unobserve(e.target);
          }
        });
      });
      fills.forEach(function (f) { obs.observe(f); });
    } else {
      fills.forEach(function (f) { f.style.width = f.dataset.level + '%'; });
    }
  }

  // ----- Gallery lightbox -----
  const lightbox = $('#lightbox');
  if (lightbox) {
    const big = $('#lightbox-img');
    $$('.photo img').forEach(function (img) {
      img.addEventListener('click', function () {
        big.src = img.src;
        lightbox.hidden = false;
      });
    });
    lightbox.addEventListener('click', function () { lightbox.hidden = true; });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') lightbox.hidden = true;
    });
  }

  // ----- Copy link buttons -----
  $$('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const original = btn.textContent;
      const done = function () {
        btn.textContent = 'Copied!';
        setTimeout(function () { btn.textContent = original; }, 1500);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(btn.dataset.copy).then(done, function () { window.prompt('Copy this link:', btn.dataset.copy); });
      } else {
        window.prompt('Copy this link:', btn.dataset.copy);
      }
    });
  });

  // ----- Range sliders show their value -----
  $$('input[type="range"]').forEach(function (input) {
    const out = document.createElement('span');
    out.className = 'range-out';
    out.textContent = input.value + '%';
    input.insertAdjacentElement('afterend', out);
    input.addEventListener('input', function () { out.textContent = input.value + '%'; });
  });

  // ----- Theme color swatches: live preview on the edit page -----
  const swatches = $$('.swatch input');
  if (swatches.length) {
    const apply = function (input) { root.style.setProperty('--primary', input.value); };
    swatches.forEach(function (input) {
      input.addEventListener('change', function () { apply(input); });
      if (input.checked) apply(input);
    });
  }

  // ----- Profile photo preview before saving -----
  const fileInput = $('#id_avatar');
  const preview = $('#avatar-preview');
  if (fileInput && preview) {
    fileInput.addEventListener('change', function () {
      const file = fileInput.files && fileInput.files[0];
      if (!file) return;
      preview.src = URL.createObjectURL(file);
      preview.hidden = false;
      const ph = $('#avatar-ph');
      if (ph) ph.hidden = true;
    });
  }
    // ----- Print and download the profile -----
  function prepareForCapture() {
    $$('.fill[data-level]').forEach(function (f) { f.style.width = f.dataset.level + '%'; });
    const t = $('#typing');
    if (t && t.dataset.text) t.textContent = t.dataset.text;
  }

  const printBtn = $('#print-btn');
  if (printBtn) {
    printBtn.addEventListener('click', function () {
      prepareForCapture();
      window.print();
    });
  }

  const downloadBtn = $('#download-btn');
  if (downloadBtn) {
    const loadLib = function () {
      return new Promise(function (resolve, reject) {
        if (window.html2canvas) return resolve();
        const s = document.createElement('script');
        s.src = 'https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js';
        s.onload = resolve;
        s.onerror = reject;
        document.head.appendChild(s);
      });
    };
    downloadBtn.addEventListener('click', function () {
      const target = $('.profile-theme');
      if (!target) return;
      const original = downloadBtn.textContent;
      downloadBtn.textContent = 'Preparing...';
      downloadBtn.disabled = true;
      prepareForCapture();
      loadLib().then(function () {
        return html2canvas(target, {
          scale: 2,
          useCORS: true,
          backgroundColor: getComputedStyle(document.body).backgroundColor,
          ignoreElements: function (el) { return el.classList && el.classList.contains('no-print'); }
        });
      }).then(function (canvas) {
        const a = document.createElement('a');
        a.download = (downloadBtn.dataset.filename || 'my-profile') + '.png';
        a.href = canvas.toDataURL('image/png');
        a.click();
      }).catch(function () {
        alert('Could not create the image. Check your internet connection, or use Print / Save as PDF instead.');
      }).finally(function () {
        downloadBtn.textContent = original;
        downloadBtn.disabled = false;
      });
    });
  }
})();
