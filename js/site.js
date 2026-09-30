/* Sunday Gravy Studio: home slideshow, Work photo viewer, contact form. */
(function () {
  'use strict';

  // Old one-page links (/#work etc.) go to the real pages.
  var old = { '#work': '/work/', '#about': '/about/', '#contact': '/contact/', '#rates': '/pricing/' };
  if (location.pathname === '/' && old[location.hash]) location.replace(old[location.hash]);

  // Home slideshow. Crossfades every 4s. With Reduce Motion on it still advances,
  // it just swaps instantly (the fade is turned off in CSS).
  // Click the left third for the previous photo, anywhere else for the next.
  // Only the first photo loads up front; each next one loads just before it shows.
  var stage = document.getElementById('stage');
  if (stage) {
    var imgs = [].slice.call(stage.querySelectorAll('img'));
    var k = 0, timer = null;
    var ready = function (img) {
      if (img.dataset.srcset) { img.srcset = img.dataset.srcset; img.removeAttribute('data-srcset'); }
      if (img.dataset.src) { img.src = img.dataset.src; img.removeAttribute('data-src'); }
    };
    var show = function (i) {
      imgs[k].classList.remove('on');
      k = (i + imgs.length) % imgs.length;
      ready(imgs[k]);
      imgs[k].classList.add('on');
      ready(imgs[(k + 1) % imgs.length]);
    };
    var start = function () {
      clearInterval(timer);
      timer = setInterval(function () { if (!document.hidden) show(k + 1); }, 4000);
    };
    stage.addEventListener('click', function (e) {
      var r = stage.getBoundingClientRect();
      show(e.clientX < r.left + r.width / 3 ? k - 1 : k + 1);
      start();
    });
    stage.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') { show(k - 1); start(); }
      if (e.key === 'ArrowRight' || e.key === 'Enter' || e.key === ' ') { e.preventDefault(); show(k + 1); start(); }
    });
    var go = function () { ready(imgs[1]); start(); };
    if (document.readyState === 'complete') go(); else window.addEventListener('load', go);
  }

  // Work: click a photo to open it full screen on white, click again to close.
  var grid = document.getElementById('wgrid');
  if (grid) {
    var links = [].slice.call(grid.querySelectorAll('a'));
    var box = null, opener = null, at = 0;
    var close = function () {
      if (!box) return;
      box.remove(); box = null;
      if (opener) opener.focus();
    };
    var open = function (i) {
      at = (i + links.length) % links.length;
      var a = links[at];
      if (!box) {
        box = document.createElement('div');
        box.className = 'lb';
        box.setAttribute('role', 'dialog');
        box.setAttribute('aria-modal', 'true');
        box.setAttribute('aria-label', 'Photo');
        box.innerHTML = '<button class="x u" type="button" style="background:none;border:0;padding:0;cursor:pointer;color:inherit">Close</button><img alt="">';
        box.addEventListener('click', close);
        document.body.appendChild(box);
        box.querySelector('.x').focus();
      }
      var img = box.querySelector('img');
      img.src = a.getAttribute('href');
      img.alt = a.querySelector('img').alt;
    };
    grid.addEventListener('click', function (e) {
      var a = e.target.closest('a');
      if (!a) return;
      e.preventDefault();
      opener = a;
      open(links.indexOf(a));
    });
    addEventListener('keydown', function (e) {
      if (!box) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowRight') open(at + 1);
      if (e.key === 'ArrowLeft') open(at - 1);
    });
  }

  // Contact form. Posts to Formspree (same service as the Cowdog form), which emails it on.
  var form = document.getElementById('inquiry');
  if (form) {
    var note = document.getElementById('f-note');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      note.textContent = '';
      var name = form.elements.name.value.trim(), email = form.elements.email.value.trim();
      var biz = form.elements.business.value.trim();
      if (!name || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
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
          note.textContent = "That didn't go through. Give it another try in a minute.";
        });
    });
  }
})();
