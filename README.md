# Sunday Gravy Studio website

Static site for https://www.sundaygravystudio.com, hosted on GitHub Pages from `main` (repo root). No server code. Push to `main` and it deploys.

## How it's put together
- **Edit pages in `tools/content/`**, not the generated HTML. Each file is one page: a JSON header between `---` lines (title, description, FAQ, etc.), then the page body.
- Guides (blog posts) live in `tools/content/blog/`. The file name becomes the URL: `blog/<name>/`.
- Run `python3 tools/build.py` to regenerate every page, plus `sitemap.xml`. Commit the content and the generated files together.
- Shared header, footer, schema (LocalBusiness, Service, FAQPage, BlogPosting, breadcrumbs) and prices (`RATES`) live in `tools/build.py`. Styles are in `tools/site.css`, which gets inlined into every page.
- Logo mark (grouped for the animation): `tools/mark.svg`. Favicon: `favicon.svg`. Icons and `og-image.jpg` were rendered from the mark.

## Photos
- `tools/photos.py` lists every portfolio photo (SEO file name + alt text), in Work page order.
- To add one: save the 1800px JPG as `photos/<descriptive-name>.jpg`, add a line to `PHOTOS`, then run `python3 tools/photos.py` (makes the 600/1200/1800 WebP copies and a 900px JPG; needs `pip3 install --user pillow`) and `python3 tools/build.py`.
- Originals: `~/Desktop/forsundaygravy`.

## Scripts
- `js/site.js`: slideshow, photo viewer, contact form (posts to Formspree, same as the Cowdog form).
- `js/sg-track.js`: GA4 and event tracking. Set `GA_ID` once the GA4 property exists.
