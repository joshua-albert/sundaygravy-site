"""Builds the static site from tools/content/.

    python3 tools/build.py

Each file in tools/content/ (and tools/content/blog/) is one page: a JSON
header between two lines of '---', then the page body as HTML. This script
wraps every body in the shared head, corner nav, butter footer and schema, and
writes plain HTML to the repo (e.g. /about/index.html). GitHub Pages serves
those files as-is. Commit the output along with the content.

Layouts ("layout" in the header):
    rows   (default) sections in the right-hand content column, no left labels.
           The page's "h1" opens the first section; every <h2> in the body
           starts a new section and shows as a small caps subhead. FAQ, related
           links and a booking line are added at the end ({{tail}}...{{/tail}}
           does the same on plain pages). Blog posts always use this.
    plain  body is used as written.

Body shortcuts:
    {{photo:slug|sizes|class}}   responsive <img> (WebP srcset, width/height)
    {{photo!:slug|sizes|class}}  same, loaded eagerly (use for the top image)
    {{rates}}  rates table     {{steps}}  the three shoot steps
    {{usage}}  usage note      {{faq}}    FAQ list from the page's "faq" field
    {{grid}}   Work page grid  {{slideshow}} / {{sig}}  home page pieces
    {{posts}}  journal list
"""
import html
import json
import re
import struct
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
from photos import PHOTOS  # noqa: E402

SITE = "https://www.sundaygravystudio.com"
BRAND = "Sunday Gravy Studio"
YEAR = date.today().year
ALT = dict(PHOTOS)
ALT["joshua-albert-philadelphia-food-photographer"] = "Black and white portrait of Joshua Albert, food photographer in the Philadelphia area"
INSTAGRAM = "https://www.instagram.com/sundaygravystudio/"
COWDOG = "https://www.cowdog.studio/"
GA_ID = "G-H66S7RM0XF"

RATES = [
    # name, price, unit, detail, anchor
    ("Dish drop", 175, "", "1 hour · 6 photos", "dish-drop"),
    ("Menu shoot, half day", 400, "", "20 photos", "menu-shoot-half-day"),
    ("Menu shoot, full day", 750, "", "45 photos, dishes and the room", "menu-shoot-full-day"),
    ("Monthly content", 300, "/mo", "1 visit · 10 photos", "monthly-content"),
]
USAGE = "Use the photos on your menu, website, social, Google and the delivery apps. Ads and packaging are quoted separately."
STEPS = [
    "Send me the menu. We pick the dishes and a time that works for the kitchen.",
    "I set up in a corner of the dining room. The kitchen fires one plate at a time. If something needs another try, we fire it again.",
    "I edit everything and send it sized for your menu, website, Instagram and the delivery apps.",
]

SERVICES = [
    ("/restaurant-photography/", "Restaurant photography"),
    ("/food-photography/", "Food photography"),
    ("/drink-photography/", "Drink photography"),
    ("/pricing/", "Rates"),
    ("/work/", "Work"),
    ("/blog/", "Journal"),
]

NAV_L = [("/work/", "Work"), ("/pricing/", "Rates")]
NAV_R = [("/about/", "About"), ("/contact/", "Contact")]
FOOT_L = [("/restaurant-photography/", "Restaurant photography"), ("/food-photography/", "Food photography"),
          ("/drink-photography/", "Drink photography"), ("/blog/", "Journal")]

MARK = (TOOLS / "mark.svg").read_text().strip()
MARK_VB = (TOOLS / "mark-viewbox.txt").read_text().strip()
_vb = [float(x) for x in MARK_VB.split()]
MARK_RATIO = _vb[3] / _vb[2]

# Home slideshow order (1-based positions in PHOTOS), from the design preview.
HERO = [5, 7, 3, 8, 1, 13, 9, 18, 2, 4, 12, 10, 20]


# ---------- images ----------

def jpeg_size(path):
    with open(path, "rb") as f:
        data = f.read()
    i = 2
    while i < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        i += 2 + struct.unpack(">H", data[i + 2:i + 4])[0]
    raise ValueError(path)


def srcset(slug):
    ws = sorted(int(p.stem.rsplit("-", 1)[1]) for p in (ROOT / "photos").glob(f"{slug}-*.webp"))
    return ", ".join(f"/photos/{slug}-{w}.webp {w}w" for w in ws), ws


def mid(ws):
    return [x for x in ws if x <= 1200][-1]


def photo(slug, sizes="100vw", cls="", eager=False, alt=None, lazy=True):
    w, h = jpeg_size(ROOT / "photos" / f"{slug}.jpg")
    ss, ws = srcset(slug)
    alt = ALT[slug] if alt is None else alt
    load = 'fetchpriority="high"' if eager else ('loading="lazy" decoding="async"' if lazy else 'decoding="async"')
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/photos/{slug}-{mid(ws)}.webp" srcset="{ss}" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{html.escape(alt)}" {load}>')


def preload(slug, sizes):
    ss, ws = srcset(slug)
    return (f'<link rel="preload" as="image" href="/photos/{slug}-{mid(ws)}.webp" '
            f'imagesrcset="{ss}" imagesizes="{sizes}" fetchpriority="high">')


# ---------- blocks ----------

BODY_SIZES = "(max-width: 760px) calc(100vw - 40px), 72vw"


def mark_inline(cls=""):
    return f'<svg class="mark {cls}" viewBox="{MARK_VB}" aria-hidden="true" focusable="false">{MARK}</svg>'


def mark_img(width=None, height=None):
    if height:
        width = round(height / MARK_RATIO)
    return f'<img src="/mark.svg" width="{width}" height="{height or round(width * MARK_RATIO)}" alt="">'


def money(n):
    return f"${n:,}"


def rates_html():
    rows = "".join(
        f'<tr id="{a}"><td class="n mute u">{i + 1:02d}</td><td>{html.escape(n)}<span class="dm mute u">{d}</span></td>'
        f'<td class="d mute u">{d}</td><td>{money(p)}{u}</td></tr>'
        for i, (n, p, u, d, a) in enumerate(RATES))
    return f'<table class="rates"><caption class="sr">Rates</caption>{rows}</table>'


def steps_html():
    return '<ol class="steps">' + "".join(f"<li>{s}</li>" for s in STEPS) + "</ol>"


def faq_html(faq):
    items = "".join(f'<details><summary>{html.escape(q)}</summary><div>{a}</div></details>' for q, a in faq)
    return f'<div class="faq">{items}</div>'


def links_html(path, extra=()):
    items = "".join(f'<li><a href="{u}"><span>{t}</span><span class="mute">&rarr;</span></a></li>'
                    for u, t in list(extra) + SERVICES if u != path)
    return f'<ul class="links u">{items}</ul>'


def grid_html():
    out = []
    for i, (slug, alt) in enumerate(PHOTOS):
        out.append(f'<a href="/photos/{slug}-1800.webp" data-i="{i}">'
                   + photo(slug, "(max-width: 760px) 50vw, 33vw", eager=i < 3, lazy=i >= 9) + "</a>")
    return f'<div class="wgrid" id="wgrid">{"".join(out)}</div>'


SHOW_SIZES = "(max-width: 1140px) 100vw, 1100px"


def slideshow_html():
    imgs = []
    for i, n in enumerate(HERO):
        slug, alt = PHOTOS[n - 1]
        if i == 0:
            imgs.append(photo(slug, SHOW_SIZES, "on", eager=True))
            continue
        ss, ws = srcset(slug)
        w, h = jpeg_size(ROOT / "photos" / f"{slug}.jpg")
        imgs.append(f'<img data-src="/photos/{slug}-{mid(ws)}.webp" data-srcset="{ss}" sizes="{SHOW_SIZES}" '
                    f'width="{w}" height="{h}" alt="{html.escape(alt)}" decoding="async">')
    return (f'<div class="stage" id="stage" role="button" tabindex="0" '
            f'aria-label="Recent work. Click for the next photo.">{"".join(imgs)}</div>')


def sig_html():
    return (f'<a class="sig" href="/work/" aria-label="{BRAND}, see the work">{mark_inline()}'
            f'<span class="nm">{BRAND}</span>'
            '<span class="u tag">Food and drink photography · Philadelphia area</span></a>')


def posts_html(posts):
    items = "".join(
        f'<li><a href="{p["path"]}"><span>{html.escape(p["h1"])}</span>'
        f'<span class="mute u">{date.fromisoformat(p["date"]):%b %Y}</span></a></li>'
        for p in posts)
    return f'<ul class="links one">{items}</ul>'


# ---------- schema ----------

BUSINESS_ID = SITE + "/#business"
PERSON_ID = SITE + "/about/#joshua"


def business():
    return {
        "@type": ["LocalBusiness", "ProfessionalService"],
        "@id": BUSINESS_ID,
        "name": BRAND,
        "description": "Food and drink photography for restaurants, bars, bakeries and cafés in the Philadelphia area. Menu shoots, dish drops and monthly content.",
        "url": SITE + "/",
        "logo": SITE + "/icon-512.png",
        "image": SITE + "/og-image.jpg",
        "priceRange": "$175 - $750",
        "address": {"@type": "PostalAddress", "addressLocality": "Philadelphia", "addressRegion": "PA", "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": 39.9259, "longitude": -75.1662},
        "areaServed": [{"@type": "City", "name": "Philadelphia"},
                       {"@type": "AdministrativeArea", "name": "Greater Philadelphia"}] + [
            {"@type": "Place", "name": f"{n}, Philadelphia"} for n in
            ("South Philadelphia", "East Passyunk", "Fishtown", "Center City", "Old City", "Northern Liberties")
        ] + [{"@type": "Place", "name": "Main Line, Pennsylvania"}],
        "sameAs": [INSTAGRAM],
        "founder": {"@id": PERSON_ID},
        "knowsAbout": ["Food photography", "Restaurant photography", "Menu photography", "Cocktail photography", "Drink photography", "Bakery photography"],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Food and drink photography",
            "itemListElement": [
                {"@type": "Offer", "name": n, "price": str(p), "priceCurrency": "USD", "url": f"{SITE}/pricing/#{a}",
                 "itemOffered": {"@id": f"{SITE}/pricing/#{a}-service"}}
                for n, p, u, d, a in RATES],
        },
    }


def person():
    return {
        "@type": "Person",
        "@id": PERSON_ID,
        "name": "Joshua Albert",
        "jobTitle": "Food photographer",
        "url": SITE + "/about/",
        "image": SITE + "/photos/joshua-albert-philadelphia-food-photographer.jpg",
        "worksFor": [{"@id": BUSINESS_ID},
                     {"@type": "Organization", "name": "Cowdog Studio", "url": COWDOG}],
    }


def service_nodes():
    return [{
        "@type": "Service",
        "@id": f"{SITE}/pricing/#{a}-service",
        "name": n,
        "serviceType": "Food photography",
        "description": d.replace(" · ", ", ") + ".",
        "provider": {"@id": BUSINESS_ID},
        "areaServed": {"@type": "AdministrativeArea", "name": "Greater Philadelphia"},
        "offers": {"@type": "Offer", "price": str(p), "priceCurrency": "USD", "url": f"{SITE}/pricing/#{a}"},
    } for n, p, u, d, a in RATES]


def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def schema(page, crumbs):
    url = SITE + page["path"]
    graph = [business(), person(),
             {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": BRAND, "publisher": {"@id": BUSINESS_ID}},
             {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": page["title"],
              "description": page["description"], "isPartOf": {"@id": SITE + "/#website"},
              "about": {"@id": BUSINESS_ID}}]
    if len(crumbs) > 1:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(crumbs)]})
    if page.get("faq"):
        graph.append({"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}}
            for q, a in page["faq"]]})
    if page.get("service"):
        s = page["service"]
        prices = [p for _, p, _, _, _ in RATES]
        graph.append({"@type": "Service", "@id": url + "#service", "name": s["name"], "serviceType": s["type"],
                      "description": s["description"], "provider": {"@id": BUSINESS_ID}, "url": url,
                      "areaServed": {"@type": "AdministrativeArea", "name": "Greater Philadelphia"},
                      "offers": {"@type": "AggregateOffer", "lowPrice": str(min(prices)), "highPrice": str(max(prices)), "priceCurrency": "USD"}})
    if page["path"] == "/pricing/":
        graph += service_nodes()
    if page.get("type") == "post":
        graph.append({"@type": "BlogPosting", "@id": url + "#post", "headline": page["h1"],
                      "description": page["description"], "datePublished": page["date"],
                      "dateModified": page.get("updated", page["date"]), "mainEntityOfPage": url,
                      "image": f"{SITE}/photos/{page['image']}.jpg",
                      "author": {"@id": PERSON_ID}, "publisher": {"@id": BUSINESS_ID}})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))


# ---------- layout ----------

CSS = (TOOLS / "site.css").read_text()
CSS = re.sub(r"/\*.*?\*/", "", CSS, flags=re.S)
CSS = re.sub(r"\s*\n\s*", "", CSS)


def nav(path):
    def a(u, t):
        cur = ' class="cur" aria-current="page"' if path.startswith(u) else ""
        return f'<a href="{u}"{cur}>{t}</a>'
    # Every page but Home gets the small logo top-center as the way home.
    home = "" if path == "/" else f'<a class="home" href="/" aria-label="{BRAND} home">{mark_img(height=26)}</a>'
    return (f'<nav class="nav u" aria-label="Main"><span class="g">{"".join(a(u, t) for u, t in NAV_L)}</span>'
            f'{home}<span class="g">{"".join(a(u, t) for u, t in NAV_R)}</span></nav>')


def footer():
    fl = "".join(f'<a href="{u}">{t}</a>' for u, t in FOOT_L)
    return (f'<footer class="foot u"><a class="fm" href="/" aria-label="{BRAND} home">{mark_img(26)}'
            f'<span>&copy; {YEAR} {BRAND}</span></a>'
            f'<nav class="fl" aria-label="Services">{fl}</nav>'
            f'<span class="fr"><a href="{COWDOG}">Sister studio of Cowdog Studio</a>'
            f'<a href="{INSTAGRAM}">Instagram</a></span></footer>')


def render(page, body, crumbs):
    path = page["path"]
    url = SITE + path
    title = page["title"] if page.get("raw_title") else f'{page["title"]} | {BRAND}'
    og = f'{SITE}/og-image.jpg'
    ogw, ogh = 1200, 630
    if page.get("og"):
        og = f'{SITE}/photos/{page["og"]}.jpg'
        ogw, ogh = jpeg_size(ROOT / "photos" / f'{page["og"]}.jpg')
    pre = preload(*page["preload"]) if page.get("preload") else ""
    robots = '<meta name="robots" content="noindex">' if page.get("noindex") else ""
    canon = "" if page.get("noindex") else f'<link rel="canonical" href="{url}">'
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(page['description'])}">
{canon}{robots}
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-48.png" sizes="48x48" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#FFFFFF">
<meta property="og:type" content="{'article' if page.get('type') == 'post' else 'website'}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{html.escape(page.get('og_title', page['title']))}">
<meta property="og:description" content="{html.escape(page['description'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="{ogw}">
<meta property="og:image:height" content="{ogh}">
<meta name="twitter:card" content="summary_large_image">
{pre}
<link rel="preconnect" href="https://use.typekit.net" crossorigin>
<link rel="preconnect" href="https://p.typekit.net" crossorigin>
<link rel="stylesheet" href="https://use.typekit.net/cur5uhh.css">
<style>{CSS}</style>
<script type="application/ld+json">{schema(page, crumbs)}</script>
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>
<script defer src="/js/sg-track.js"></script>
<script defer src="/js/site.js"></script>
</head>
<body class="pg-{page.get('slug', 'page')}">
<a class="skip" href="#main">Skip to content</a>
{nav(path)}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>
"""


# ---------- rows layout ----------

def rows(page, body):
    """First section: H1 + intro. Each <h2> starts a new section with the h2 as a small caps subhead."""
    parts = re.split(r"<h2>(.*?)</h2>", body.strip(), flags=re.S)
    intro, rest = parts[0], parts[1:]
    top = ""
    if page.get("type") == "post":
        d = date.fromisoformat(page["date"])
        top = (f'<p class="kicker u mute"><a href="/blog/">Journal</a> · '
               f'<time datetime="{page["date"]}">{d:%B} {d.day}, {d.year}</time></p>')
    top += f'<h1 class="lede">{html.escape(page["h1"])}</h1>'
    if page.get("type") == "post":
        top += f'<figure>{photo(page["image"], BODY_SIZES, eager=True)}</figure>'
    out = [f'<section class="row"><div class="body">{top}{intro}</div></section>']
    for i in range(0, len(rest), 2):
        out.append(f'<section class="row"><div class="body"><h2 class="sh u">{rest[i]}</h2>{rest[i + 1].strip()}</div></section>')
    out += tail_rows(page)
    return f'<div class="page">{"".join(out)}</div>'


def tail_rows(page, more=None):
    """FAQ, related links and the booking line. No visible labels; the h2s are for screen readers."""
    out = []
    if page.get("faq"):
        out.append(f'<section class="row" id="faq"><div class="body"><h2 class="sr">Questions</h2>{faq_html(page["faq"])}</div></section>')
    if not page.get("no_more"):
        out.append(f'<section class="row"><div class="body"><h2 class="sr">More</h2>{more or links_html(page["path"])}</div></section>')
        out.append('<section class="row"><div class="body"><h2 class="sr">Book</h2>'
                   '<p>Tell me what you&rsquo;re working on and when.</p>'
                   '<p class="u"><a href="/contact/">Book a shoot</a></p></div></section>')
    return out


# ---------- build ----------

def load(path):
    text = path.read_text()
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    if not m:
        raise SystemExit(f"{path}: missing --- header")
    meta = json.loads(m.group(1))
    meta["body"] = m.group(2)
    meta["src"] = path
    return meta


def expand(page, posts):
    body = page["body"]

    def ph(m):
        eager = m.group(1) == "!"
        parts = m.group(2).split("|")
        return photo(parts[0], parts[1] if len(parts) > 1 and parts[1] else BODY_SIZES,
                     parts[2] if len(parts) > 2 else "", eager)
    body = re.sub(r"\{\{photo(!?):([^}]+)\}\}", ph, body)
    for k, v in {"rates": rates_html, "steps": steps_html, "grid": grid_html,
                 "slideshow": slideshow_html, "sig": sig_html}.items():
        if "{{" + k + "}}" in body:
            body = body.replace("{{" + k + "}}", v())
    body = body.replace("{{usage}}", USAGE)
    body = body.replace("{{faq}}", faq_html(page.get("faq", [])))
    body = body.replace("{{posts}}", posts_html(posts))
    if "{{tail}}" in body:
        m = re.search(r"\{\{tail\}\}(.*?)\{\{/tail\}\}", body, re.S)
        body = body.replace(m.group(0), "".join(tail_rows(page, m.group(1).strip())))
    left = re.findall(r"\{\{[^}]*\}\}", body)
    if left:
        raise SystemExit(f"{page['src']}: unknown shortcut {left}")
    return body


def main():
    content = TOOLS / "content"
    pages = [load(p) for p in sorted(content.glob("*.html"))]
    posts = [load(p) for p in sorted((content / "blog").glob("*.html"))]
    for p in posts:
        p["type"] = "post"
        p["path"] = f"/blog/{p['src'].stem}/"
        p["preload"] = [p["image"], BODY_SIZES]
    posts.sort(key=lambda p: (p["date"], p.get("order", 0)), reverse=True)

    problems = []
    urls = []
    for page in pages + posts:
        d = page["description"]
        if len(d) > 160:
            problems.append(f"{page['path']}: description is {len(d)} chars")
        body = expand(page, posts)
        if page.get("type") == "post" or page.get("layout", "rows") == "rows":
            body = rows(page, body)
        crumbs = [("Home", "/")]
        if page.get("type") == "post":
            crumbs.append(("Journal", "/blog/"))
        if page["path"] != "/":
            crumbs.append((page.get("crumb", page.get("h1", page["title"])), page["path"]))
        out = render(page, body, crumbs)
        if page["path"] == "/":
            dest = ROOT / "index.html"
        elif page["path"] == "/404.html":
            dest = ROOT / "404.html"
        else:
            dest = ROOT / page["path"].strip("/") / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(out)
        if not page.get("noindex"):
            urls.append((page["path"], page.get("updated", page.get("date", str(date.today())))))

    order = {"/": 0}
    urls.sort(key=lambda u: (order.get(u[0], 1), u[0].startswith("/blog/"), u[0]))
    sm = "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{m}</lastmod></url>\n" for u, m in urls)
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}</urlset>\n')
    print(f"built {len(pages)} pages, {len(posts)} posts, {len(urls)} urls in sitemap")
    for p in problems:
        print("WARNING", p)


if __name__ == "__main__":
    main()
