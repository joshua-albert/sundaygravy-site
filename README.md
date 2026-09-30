# Sunday Gravy Studio website

Static site for https://www.sundaygravystudio.com, hosted on GitHub Pages from `main` (repo root). No server code. Push to `main` and it deploys.

## How it's put together
- **Edit pages in `tools/content/`**, not the generated HTML. Each file is one page: a JSON header between `---` lines (title, description, FAQ, etc.), then the page body.
- Guides (blog posts) live in `tools/content/blog/`. The file name becomes the URL: `blog/<name>/`.
- Run `python3 tools/build.py` to regenerate every page, plus `sitemap.xml`. Commit the content and the generated files together.
- Shared corner nav, butter footer, schema (LocalBusiness, Service, FAQPage, BlogPosting, breadcrumbs), GA4 tag, rates table (`RATES`), usage note and shoot steps live in `tools/build.py`. Styles are in `tools/site.css`, which gets inlined into every page.
- Fonts: Hoss Round Slab from the Adobe Fonts kit `cur5uhh` (big text and body), Helvetica for small caps UI. The kit only serves allowed domains, so preview locally at `http://localhost:8765` (`python3 -m http.server 8765`), not 127.0.0.1.
- Logo (brush redraw): `tools/mark.svg` (inline, grouped for the lift animation) and `mark.svg` (footer image). Favicon: `favicon.svg`. Icons and `og-image.jpg` were rendered from the mark.
- `design/` holds the redesign brief and preview. It's gitignored, so it never goes live.

## Photos
- `tools/photos.py` lists every portfolio photo (SEO file name + alt text), in Work page order.
- To add one: save the 1800px JPG as `photos/<descriptive-name>.jpg`, add a line to `PHOTOS`, then run `python3 tools/photos.py` (makes the 600/1200/1800 WebP copies and a 900px JPG; needs `pip3 install --user pillow`) and `python3 tools/build.py`.
- Originals: `~/Desktop/forsundaygravy`.

## Scripts
- `js/site.js`: home slideshow (keeps running with Reduce Motion, just no fade), Work photo viewer, contact form (posts to Formspree, same as the Cowdog form; sends GA4 `generate_lead` on success).
- `js/sg-track.js`: click and scroll events on top of GA4 (`G-H66S7RM0XF`, tag is in each page's head).
