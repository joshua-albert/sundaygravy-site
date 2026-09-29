/* Sunday Gravy Studio analytics: GA4 plus click and form tracking.
   Same approach as cowdog-track.js. Every event carries source_page.
   GA stays off until GA_ID is filled in with the Sunday Gravy GA4 measurement ID. */
(function () {
  'use strict';

  var GA_ID = ''; // e.g. 'G-XXXXXXXXXX' from GA4 > Admin > Data streams

  if (GA_ID) {
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', GA_ID);
  }

  var page = location.pathname;

  function send(name, extra) {
    var params = { source_page: page };
    if (extra) for (var k in extra) if (Object.prototype.hasOwnProperty.call(extra, k)) params[k] = extra[k];
    try { if (typeof window.gtag === 'function') window.gtag('event', name, params); } catch (e) {}
  }
  window.sgTrack = send;

  function eventFor(href) {
    var h = href.toLowerCase();
    if (h.indexOf('/contact') !== -1) return 'contact_click';
    if (h.indexOf('/pricing') !== -1) return 'pricing_click';
    if (h.indexOf('cowdog.studio') !== -1) return 'cowdog_click';
    if (h.indexOf('instagram.com') !== -1) return 'instagram_click';
    return null;
  }

  function onClick(e) {
    try {
      var el = e.target.closest && e.target.closest('a');
      if (!el) return;
      var href = el.getAttribute('href');
      var name = href && eventFor(href);
      if (!name) return;
      send(name, { link_url: href, link_text: (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 100) });
    } catch (err) {}
  }

  function scrollDepth() {
    if (page.indexOf('/blog/') !== 0 || page === '/blog/') return;
    var marks = [25, 50, 75, 100], fired = {}, ticking = false;
    function check() {
      ticking = false;
      var doc = document.documentElement;
      var total = doc.scrollHeight - window.innerHeight;
      if (total <= 0) return;
      var pct = Math.round((window.pageYOffset / total) * 100);
      for (var i = 0; i < marks.length; i++) if (pct >= marks[i] && !fired[marks[i]]) { fired[marks[i]] = true; send('scroll_depth', { percent: marks[i] }); }
    }
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(check); } }, { passive: true });
  }

  try {
    document.addEventListener('click', onClick, true);
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', scrollDepth); else scrollDepth();
  } catch (err) {}
})();
