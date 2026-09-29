"""Builds the static site from tools/content/.

    python3 tools/build.py

Each file in tools/content/ (and tools/content/blog/) is one page: a JSON
header between two lines of '---', then the page body as HTML. This script
wraps every body in the shared head, header, footer and schema, and writes
plain HTML to the repo (e.g. /about/index.html). GitHub Pages serves those
files as-is; nothing runs on the server. Commit the output along with the
content.

Body shortcuts:
    {{photo:slug|sizes|class}}   responsive <img> (WebP srcset, width/height)
    {{photo!:slug|sizes|class}}  same, loaded eagerly (use for the top image)
    {{rates}}                    the four price cards
    {{faq}}                      FAQ list from the page's "faq" field
    {{cta}}                      booking call-to-action block
    {{services}}                 links to the three service pages (minus this one)
    {{posts}}                    blog post list
    {{grid}}                     Work page photo grid
    {{slideshow}}                Home page slideshow (first 10 photos)
    {{mark}}                     the logo mark (inline SVG, animated)
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
ALT["joshua-albert-philadelphia-food-photographer"] = "Black and white portrait of Joshua Albert, food photographer in Philadelphia"

RATES = [
    # name, price, unit, photos line, detail, url anchor
    ("Menu shoot, half day", 500, "", "20 finished photos", "A new menu, or the dishes that sell the most.", "menu-shoot-half-day"),
    ("Menu shoot, full day", 950, "", "45 finished photos", "The whole menu, the room, the bar and the team.", "menu-shoot-full-day"),
    ("Dish drop", 250, "", "1 hour, 6 photos", "New specials and one-offs.", "dish-drop"),
    ("Monthly content", 600, "/mo", "1 visit a month, 10 photos", "Fresh photos for social, every month.", "monthly-content"),
]

SERVICES = [
    ("/restaurant-photography/", "Restaurant photography", "Menu shoots, openings, dish drops and monthly content."),
    ("/food-photography/", "Food photography", "For restaurants, bakeries and cafés. Menus, websites, delivery apps."),
    ("/drink-photography/", "Cocktail and drink photography", "Cocktail lists, pours, coffee and the bar itself."),
]

NAV = [("/work/", "Work"), ("/pricing/", "Pricing"), ("/about/", "About"), ("/contact/", "Book")]

FOOT_NAV = [
    ("/work/", "Work"),
    ("/restaurant-photography/", "Restaurant photography"),
    ("/food-photography/", "Food photography"),
    ("/drink-photography/", "Cocktail and drink photography"),
    ("/pricing/", "Pricing"),
    ("/blog/", "Guides"),
    ("/about/", "About"),
    ("/contact/", "Book a shoot"),
]

MARK = (TOOLS / "mark.svg").read_text().strip()


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


def photo(slug, sizes="100vw", cls="", eager=False, alt=None):
    w, h = jpeg_size(ROOT / "photos" / f"{slug}.jpg")
    ss, ws = srcset(slug)
    mid = [x for x in ws if x <= 1200][-1]
    alt = ALT[slug] if alt is None else alt
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/photos/{slug}-{mid}.webp" srcset="{ss}" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{html.escape(alt)}" {load}>')


def preload(slug, sizes):
    ss, ws = srcset(slug)
    mid = [x for x in ws if x <= 1200][-1]
    return (f'<link rel="preload" as="image" href="/photos/{slug}-{mid}.webp" '
            f'imagesrcset="{ss}" imagesizes="{sizes}" fetchpriority="high">')


# ---------- blocks ----------

def mark(cls=""):
    return f'<svg class="mark {cls}" viewBox="0 0 240 240" aria-hidden="true" focusable="false">{MARK}</svg>'


def money(n):
    return f"${n:,}"


def rates_html():
    cards = "".join(
        f'<div class="rate" id="{a}"><h3>{html.escape(n)}</h3>'
        f'<div class="p">{money(p)}<small>{u}</small></div><p class="ph">{ph}</p><p>{d}</p></div>'
        for n, p, u, ph, d, a in RATES)
    return f'<div class="rates">{cards}</div>'


def faq_html(faq):
    items = "".join(f'<details><summary>{html.escape(q)}</summary><div>{a}</div></details>' for q, a in faq)
    return f'<section class="faq" aria-labelledby="faq-h"><h2 id="faq-h">Questions people ask</h2>{items}</section>'


def cta_html():
    return ('<section class="cta"><h2>Have a menu, a menu change or an opening coming up?</h2>'
            '<p>Tell me what you&rsquo;re working on and when. Prices are on the <a href="/pricing/">pricing page</a>.</p>'
            '<a class="btn" href="/contact/">Book a shoot</a></section>')


def services_html(path):
    items = "".join(
        f'<a class="svc" href="{u}"><span class="svc-t">{t}</span><span class="svc-d">{d}</span></a>'
        for u, t, d in SERVICES if u != path)
    return f'<nav class="svcs" aria-label="Services">{items}</nav>'


def grid_html():
    tiles = []
    for i, (slug, alt) in enumerate(PHOTOS):
        tiles.append(
            f'<button class="tile" type="button" data-i="{i}" data-full="/photos/{slug}-1800.webp" '
            f'aria-label="Open photo: {html.escape(alt)}">'
            + photo(slug, "(max-width: 760px) 50vw, 400px", eager=i < 3) + "</button>")
    return f'<div class="grid" id="grid">{"".join(tiles)}</div>'


SHOW_SIZES = "(max-width: 900px) 100vw, 900px"


def slideshow_html():
    imgs = []
    for i, (slug, alt) in enumerate(PHOTOS[:10]):
        if i == 0:
            imgs.append(photo(slug, SHOW_SIZES, "on", eager=True))
            continue
        ss, _ = srcset(slug)
        w, h = jpeg_size(ROOT / "photos" / f"{slug}.jpg")
        imgs.append(f'<img data-src="/photos/{slug}-1200.webp" data-srcset="{ss}" sizes="{SHOW_SIZES}" '
                    f'width="{w}" height="{h}" alt="{html.escape(alt)}" decoding="async">')
    return (f'<button class="show" id="show" type="button" aria-label="Next photo">{"".join(imgs)}</button>')


def posts_html(posts):
    items = "".join(
        f'<li><a href="{p["path"]}"><span class="pt">{html.escape(p["h1"])}</span></a>'
        f'<p>{html.escape(p["excerpt"])}</p></li>'
        for p in posts)
    return f'<ul class="posts">{items}</ul>'


# ---------- schema ----------

BUSINESS_ID = SITE + "/#business"
PERSON_ID = SITE + "/about/#joshua"


def business():
    return {
        "@type": ["LocalBusiness", "ProfessionalService"],
        "@id": BUSINESS_ID,
        "name": BRAND,
        "description": "Food and drink photography for restaurants, bars, bakeries and cafés in Philadelphia. Menu shoots, dish drops and monthly content.",
        "url": SITE + "/",
        "logo": SITE + "/icon-512.png",
        "image": SITE + "/og-image.jpg",
        "priceRange": "$250 - $950",
        "address": {"@type": "PostalAddress", "addressLocality": "Philadelphia", "addressRegion": "PA", "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": 39.9259, "longitude": -75.1662},
        "areaServed": [{"@type": "City", "name": "Philadelphia"}] + [
            {"@type": "Place", "name": f"{n}, Philadelphia"} for n in
            ("South Philadelphia", "East Passyunk", "Fishtown", "Center City", "Old City", "Northern Liberties")
        ] + [{"@type": "Place", "name": "Main Line, Pennsylvania"}],
        "founder": {"@id": PERSON_ID},
        "knowsAbout": ["Food photography", "Restaurant photography", "Menu photography", "Cocktail photography", "Drink photography", "Bakery photography"],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Food and drink photography",
            "itemListElement": [
                {"@type": "Offer", "name": n, "price": str(p), "priceCurrency": "USD", "url": f"{SITE}/pricing/#{a}",
                 "itemOffered": {"@id": f"{SITE}/pricing/#{a}-service"}}
                for n, p, u, ph, d, a in RATES],
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
                     {"@type": "Organization", "name": "Cowdog Studio", "url": "https://www.cowdog.studio/"}],
    }


def service_nodes():
    out = []
    for n, p, u, ph, d, a in RATES:
        out.append({
            "@type": "Service",
            "@id": f"{SITE}/pricing/#{a}-service",
            "name": n,
            "serviceType": "Food photography",
            "description": f"{ph}. {d}",
            "provider": {"@id": BUSINESS_ID},
            "areaServed": {"@type": "City", "name": "Philadelphia"},
            "offers": {"@type": "Offer", "price": str(p), "priceCurrency": "USD",
                       "url": f"{SITE}/pricing/#{a}"},
        })
    return out


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
        graph.append({"@type": "Service", "@id": url + "#service", "name": s["name"], "serviceType": s["type"],
                      "description": s["description"], "provider": {"@id": BUSINESS_ID}, "url": url,
                      "areaServed": {"@type": "City", "name": "Philadelphia"},
                      "offers": {"@type": "AggregateOffer", "lowPrice": "250", "highPrice": "950", "priceCurrency": "USD"}})
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

FONTS = "https://fonts.googleapis.com/css2?family=Caveat+Brush&family=Fraunces:opsz,wght@9..144,400;9..144,500&family=Inter+Tight:wght@400;500;600&display=swap"

FILTER = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><filter id="marker" x="-5%" y="-5%" '
          'width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency=".8" numOctaves="1" seed="4"/>'
          '<feDisplacementMap in="SourceGraphic" scale="1.8"/></filter></defs></svg>')


def header(path):
    links = "".join(
        f'<a href="{u}"{" aria-current=\"page\"" if path.startswith(u) else ""}>{t}</a>' for u, t in NAV)
    mini = "" if path == "/" else (
        f'<a class="mini" href="/" aria-label="{BRAND}, home">{mark()}<span class="nm">{BRAND}</span></a>')
    return f'<header class="top">{mini}<nav class="nav" aria-label="Main">{links}</nav></header>'


def footer():
    nav = "".join(f'<a href="{u}">{t}</a>' for u, t in FOOT_NAV)
    return (
        '<footer class="foot"><div class="foot-in">'
        f'<div class="foot-brand"><a class="foot-logo" href="/" aria-label="{BRAND}, home">{mark()}'
        f'<span class="nm">{BRAND}</span></a>'
        '<p>Food and drink photography in Philadelphia.</p>'
        '<p>Restaurants, bars, bakeries and cafés. Based in South Philly.</p></div>'
        f'<nav class="foot-nav" aria-label="Footer">{nav}</nav>'
        '<div class="foot-more">'
        '<p>A sister company of <a href="https://www.cowdog.studio/">Cowdog Studio</a>, family and engagement portraits in Philadelphia.</p>'
        '<p><a class="btn btn-sm" href="/contact/">Book a shoot</a></p>'
        '</div></div>'
        f'<div class="foot-legal">&copy; {YEAR} {BRAND}</div></footer>')


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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="{FONTS}"></noscript>
<style>{CSS}</style>
<script type="application/ld+json">{schema(page, crumbs)}</script>
<script defer src="/js/sg-track.js"></script>
<script defer src="/js/site.js"></script>
</head>
<body class="pg-{page.get('slug', 'page')}">
{FILTER}
<a class="skip" href="#main">Skip to content</a>
{header(path)}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>
"""


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
        return photo(parts[0], parts[1] if len(parts) > 1 and parts[1] else "100vw",
                     parts[2] if len(parts) > 2 else "", eager)
    body = re.sub(r"\{\{photo(!?):([^}]+)\}\}", ph, body)
    body = body.replace("{{rates}}", rates_html())
    body = body.replace("{{faq}}", faq_html(page.get("faq", [])))
    body = body.replace("{{cta}}", cta_html())
    body = body.replace("{{services}}", services_html(page["path"]))
    body = body.replace("{{posts}}", posts_html(posts))
    body = body.replace("{{grid}}", grid_html())
    body = body.replace("{{slideshow}}", slideshow_html())
    body = body.replace("{{mark}}", mark("big"))
    left = re.findall(r"\{\{[^}]*\}\}", body)
    if left:
        raise SystemExit(f"{page['src']}: unknown shortcut {left}")
    return body


def wrap_post(page, body):
    d = date.fromisoformat(page["date"])
    return (f'<article class="post"><header class="post-h"><p class="kicker"><a href="/blog/">Guides</a> · '
            f'<time datetime="{page["date"]}">{d:%B} {d.day}, {d.year}</time></p>'
            f'<h1>{html.escape(page["h1"])}</h1></header>'
            f'<figure class="post-img">{photo(page["image"], "(max-width: 900px) 100vw, 860px", eager=True)}</figure>'
            f'<div class="prose">{body}</div></article>{cta_html()}'
            f'<section class="more"><h2>What I shoot</h2>{services_html("")}</section>')


def main():
    content = TOOLS / "content"
    pages = [load(p) for p in sorted(content.glob("*.html"))]
    posts = [load(p) for p in sorted((content / "blog").glob("*.html"))]
    for p in posts:
        p["type"] = "post"
        p["path"] = f"/blog/{p['src'].stem}/"
        p["preload"] = [p["image"], "(max-width: 900px) 100vw, 860px"]
    posts.sort(key=lambda p: (p["date"], p.get("order", 0)), reverse=True)

    problems = []
    urls = []
    for page in pages + posts:
        d = page["description"]
        if len(d) > 160:
            problems.append(f"{page['path']}: description is {len(d)} chars")
        body = expand(page, posts)
        crumbs = [("Home", "/")]
        if page.get("type") == "post":
            crumbs.append(("Guides", "/blog/"))
        if page["path"] != "/":
            crumbs.append((page.get("crumb", page.get("h1", page["title"])), page["path"]))
        if page.get("type") == "post":
            body = wrap_post(page, body)
        out = render(page, body, crumbs)
        dest = ROOT / ("404.html" if page["path"] == "/404.html" else page["path"].strip("/") + "/index.html")
        if page["path"] == "/":
            dest = ROOT / "index.html"
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
