/* Sunday Gravy Studio: slideshow, photo viewer, contact form. */
(function () {
  'use strict';
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Old one-page links (/#work etc.) go to the real pages.
  var old = { '#work': '/work/', '#about': '/about/', '#contact': '/contact/' };
  if (location.pathname === '/' && old[location.hash]) location.replace(old[location.hash]);

  // Home slideshow. Only the first photo loads up front; each next one loads just before it shows.
  var show = document.getElementById('show');
  if (show) {
    var imgs = [].slice.call(show.querySelectorAll('img'));
    var count = document.getElementById('count');
    var k = 0, timer;
    var ready = function (img) {
      if (img.dataset.srcset) { img.srcset = img.dataset.srcset; img.removeAttribute('data-srcset'); }
      if (img.dataset.src) { img.src = img.dataset.src; img.removeAttribute('data-src'); }
    };
    var step = function () {
      imgs[k].classList.remove('on');
      k = (k + 1) % imgs.length;
      ready(imgs[k]);
      imgs[k].classList.add('on');
      ready(imgs[(k + 1) % imgs.length]);
      count.textContent = (k + 1) + ' / ' + imgs.length;
    };
    var start = function () { clearInterval(timer); if (!reduce) timer = setInterval(step, 3500); };
    show.addEventListener('click', function () { step(); start(); });
    window.addEventListener('load', function () { ready(imgs[1]); start(); });
  }

  // Work page photo viewer.
  var grid = document.getElementById('grid');
  var lb = document.getElementById('lb');
  if (grid && lb) {
    var tiles = [].slice.call(grid.querySelectorAll('.tile'));
    var li = document.getElementById('lb-img'), lc = document.getElementById('lb-c');
    var at = 0, opener = null;
    var openAt = function (i) {
      at = (i + tiles.length) % tiles.length;
      var t = tiles[at];
      li.src = t.dataset.full;
      li.alt = t.querySelector('img').alt;
      lc.textContent = (at + 1) + ' / ' + tiles.length;
      lb.hidden = false;
    };
    var closeLb = function () { lb.hidden = true; if (opener) opener.focus(); };
    grid.addEventListener('click', function (e) {
      var b = e.target.closest('.tile');
      if (!b) return;
      opener = b; openAt(+b.dataset.i);
      document.getElementById('lb-x').focus();
    });
    document.getElementById('lb-x').onclick = closeLb;
    document.getElementById('lb-p').onclick = function () { openAt(at - 1); };
    document.getElementById('lb-n').onclick = function () { openAt(at + 1); };
    lb.addEventListener('click', function (e) { if (e.target === lb) closeLb(); });
    addEventListener('keydown', function (e) {
      if (lb.hidden) return;
      if (e.key === 'Escape') closeLb();
      if (e.key === 'ArrowRight') openAt(at + 1);
      if (e.key === 'ArrowLeft') openAt(at - 1);
    });
  }

  // Contact form. Posts to Formspree (same service as the Cowdog form), which emails it on.
  var form = document.getElementById('inquiry');
  if (form) {
    var note = document.getElementById('f-note');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      note.className = 'note'; note.textContent = '';
      var name = form.elements.name.value.trim(), email = form.elements.email.value.trim();
      var biz = form.elements.business.value.trim();
      if (!name || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        note.className = 'note err';
        note.textContent = 'Please add your name and a working email.';
        return;
      }
      form.elements._subject.value = 'Sunday Gravy inquiry: ' + name + (biz ? ' / ' + biz : '');
      var btn = form.querySelector('button[type=submit]');
      btn.disabled = true; btn.textContent = 'Sending…';
      fetch(form.action, { method: 'POST', body: new FormData(form), headers: { 'Accept': 'application/json' } })
        .then(function (res) {
          if (!res.ok) throw new Error('send failed');
          form.hidden = true;
          document.getElementById('f-sent').hidden = false;
          if (window.sgTrack) window.sgTrack('generate_lead', { form_source: 'contact-page' });
        })
        .catch(function () {
          btn.disabled = false; btn.textContent = 'Send';
          note.className = 'note err';
          note.textContent = "That didn't go through. Give it another try in a minute.";
        });
    });
  }
})();
