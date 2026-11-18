(function () {
  'use strict';
  var CONFIG = {
    whatsappNumber: '918431336991',
    formEndpoint: ''
  };

  var RU = (document.documentElement.lang || '').indexOf('ru') === 0;
  var L = RU ? {
    hello: 'Здравствуйте, Luno Health. Хочу получить план лечения в Индии.',
    required: 'Обязательное поле.', enquiry: 'Новая заявка: Luno Health', fallback: 'Пожалуйста, напишите нам в WhatsApp.',
    fields: { name: 'Имя', phone: 'WhatsApp', country: 'Страна', need: 'Интересует', message: 'Комментарий' }
  } : {
    hello: 'Hello Luno Health. I would like a treatment plan in India.',
    required: 'Required.', enquiry: 'New enquiry: Luno Health', fallback: 'Please message us on WhatsApp.',
    fields: { name: 'Name', phone: 'WhatsApp', country: 'Country', need: 'Need', message: 'Note' }
  };

  var wrapper = document.querySelector('.navbar_wrapper');
  var hamburger = document.querySelector('.navbar_hamburger');
  var menu = document.querySelector('.navbar_menu');
  var overlay = document.querySelector('.navbar_overlay');
  if (wrapper) {
    var onScroll = function () {
      wrapper.classList.toggle('is-scrolled', window.scrollY > 50);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    onScroll();
  }
  function closeMenu() {
    if (menu) menu.classList.remove('is-open');
    if (overlay) overlay.classList.remove('is-visible');
    document.documentElement.removeAttribute('data-modal-lock');
  }
  if (hamburger && menu) {
    hamburger.addEventListener('click', function () {
      menu.classList.add('is-open');
      if (overlay) overlay.classList.add('is-visible');
      document.documentElement.setAttribute('data-modal-lock', '1');
    });
  }
  if (overlay) overlay.addEventListener('click', closeMenu);
  if (menu) {
    var closeBtn = menu.querySelector('.navbar_menu-close');
    if (closeBtn) closeBtn.addEventListener('click', closeMenu);
  }
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeMenu(); });

  document.querySelectorAll('[data-whatsapp]').forEach(function (el) {
    var text = el.getAttribute('data-whatsapp') || L.hello;
    el.setAttribute('href', 'https://wa.me/' + CONFIG.whatsappNumber + '?text=' + encodeURIComponent(text));
    el.setAttribute('target', '_blank');
    el.setAttribute('rel', 'noopener');
  });

  document.querySelectorAll('[data-drag-slider]').forEach(function (wrap) {
    var track = wrap.querySelector('.slider_track');
    var prev = wrap.querySelector('[data-slider-prev]');
    var next = wrap.querySelector('[data-slider-next]');
    if (!track) return;
    var down = false, x0 = 0, s0 = 0;
    track.addEventListener('mousedown', function (e) { down = true; x0 = e.pageX; s0 = track.scrollLeft; });
    window.addEventListener('mousemove', function (e) { if (down) track.scrollLeft = s0 - (e.pageX - x0); });
    window.addEventListener('mouseup', function () { down = false; });
    function w() {
      var c = track.querySelector('.slider_card');
      return c ? c.getBoundingClientRect().width + 18 : 300;
    }
    if (prev) prev.addEventListener('click', function () { track.scrollBy({ left: -w(), behavior: 'smooth' }); });
    if (next) next.addEventListener('click', function () { track.scrollBy({ left: w(), behavior: 'smooth' }); });
  });

  document.querySelectorAll('.buybox_faq-q').forEach(function (q) {
    q.addEventListener('click', function () { q.parentElement.classList.toggle('is-open'); });
  });

  var buyMain = document.querySelector('[data-buybox-main]');
  if (buyMain) {
    document.querySelectorAll('[data-buybox-src]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        buyMain.src = btn.getAttribute('data-buybox-src');
        document.querySelectorAll('[data-buybox-src]').forEach(function (b) { b.classList.remove('is-active'); });
        btn.classList.add('is-active');
      });
    });
  }

  function setError(field, msg) {
    var wrap = field.closest('.field');
    if (!wrap) return;
    var err = wrap.querySelector('.field_error');
    wrap.classList.toggle('field--error', !!msg);
    if (err) err.textContent = msg || '';
  }
  document.querySelectorAll('form[data-enquiry]').forEach(function (form) {
    form.setAttribute('novalidate', '');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true;
      form.querySelectorAll('[required]').forEach(function (field) {
        if (!field.value.trim()) { setError(field, L.required); ok = false; }
        else setError(field, '');
      });
      if (!ok) return;
      var lines = [L.enquiry];
      new FormData(form).forEach(function (v, k) { if (v && k !== '_gotcha') lines.push((L.fields[k] || k) + ': ' + v); });
      if (CONFIG.formEndpoint) {
        fetch(CONFIG.formEndpoint, { method: 'POST', headers: { Accept: 'application/json' }, body: new FormData(form) })
          .then(function (r) { if (!r.ok) throw new Error(); form.classList.add('is-sent'); })
          .catch(function () { alert(L.fallback); });
      } else {
        window.open('https://wa.me/' + CONFIG.whatsappNumber + '?text=' + encodeURIComponent(lines.join('\n')), '_blank', 'noopener');
        form.classList.add('is-sent');
      }
    });
  });

  var banner = document.querySelector('.cookie_banner');
  if (banner) {
    try { if (!localStorage.getItem('luno_cookie_consent')) setTimeout(function () { banner.classList.add('is-visible'); }, 800); } catch (e) {}
    banner.querySelectorAll('[data-cookie]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        try { localStorage.setItem('luno_cookie_consent', '1'); } catch (e) {}
        banner.classList.remove('is-visible');
      });
    });
  }
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Rooms & suites tabs
  document.querySelectorAll('[data-tabs]').forEach(function (root) {
    var tabs = root.querySelectorAll('[data-tab]');
    var panels = root.querySelectorAll('[data-panel]');
    tabs.forEach(function (tab) {
      tab.setAttribute('aria-selected', tab.classList.contains('is-active') ? 'true' : 'false');
      tab.addEventListener('click', function () {
        var id = tab.getAttribute('data-tab');
        tabs.forEach(function (t) { var on = t === tab; t.classList.toggle('is-active', on); t.setAttribute('aria-selected', on ? 'true' : 'false'); });
        panels.forEach(function (p) { p.classList.toggle('is-active', p.getAttribute('data-panel') === id); });
      });
    });
  });

  // Hospital city filter
  document.querySelectorAll('[data-city-tabs]').forEach(function (bar) {
    var section = bar.closest('section') || document;
    var cards = section.querySelectorAll('.hospital_card');
    bar.querySelectorAll('[data-city]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var city = btn.getAttribute('data-city');
        bar.querySelectorAll('[data-city]').forEach(function (b) { b.classList.toggle('is-active', b === btn); });
        cards.forEach(function (card, i) {
          var show = city === 'all' || card.getAttribute('data-city') === city;
          card.classList.toggle('is-hidden', !show);
          if (show && !reduceMotion) {
            card.classList.add('is-entering');
            window.setTimeout(function () { card.classList.remove('is-entering'); }, 30 + (i % 6) * 50);
          }
        });
      });
    });
  });

  // Count-up numbers
  function countUp(el) {
    var target = parseFloat(el.getAttribute('data-count')) || 0;
    if (reduceMotion || target === 0) { el.textContent = target; return; }
    var start = null, dur = 1400;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
      if (p < 1) window.requestAnimationFrame(step);
    }
    el.textContent = '0';
    window.requestAnimationFrame(step);
  }
  if ('IntersectionObserver' in window) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { countUp(e.target); cio.unobserve(e.target); } });
    }, { threshold: 0.6 });
    document.querySelectorAll('[data-count]').forEach(function (el) { cio.observe(el); });
  }

  var revealables = document.querySelectorAll('.title_row, .why_card, .reveal-img, .timeline, .bars, .bento_item, .hospital_grid, .rooms, .trust, .stat, .tx_card, .buybox_faqs, .market_card, .case_card, .check_item, .member_photo, .member_copy, .visual_tile, .slider_card, .tx, .phase, .split, .form_card, .value_card, .contact_item, .compare_scroll, .buybox_stage, .buybox_right, .cta_component, .hero_content > *');
  if (reduceMotion || !('IntersectionObserver' in window)) {
    revealables.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    revealables.forEach(function (el) { el.setAttribute('data-reveal', ''); });
    var heroBits = document.querySelectorAll('.hero_content > *');
    heroBits.forEach(function (el, i) {
      window.setTimeout(function () { el.classList.add('is-in'); }, 140 + i * 90);
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        io.unobserve(entry.target);
      });
    }, { threshold: 0.14, rootMargin: '0px 0px -8% 0px' });
    revealables.forEach(function (el, i) {
      if (el.closest('.hero_content')) return;
      el.style.transitionDelay = ((i % 5) * 0.07) + 's';
      io.observe(el);
    });
  }
})();
