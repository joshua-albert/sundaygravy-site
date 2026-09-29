# Sunday Gravy Studio: round 2 (tweaks + SEO overhaul)

Joshua asked for all of this on Sep 29 2026. Do it all in one pass with your own judgment, no approval gates. Follow CLAUDE.md for voice and brand. Show him a summary at the end with anything he still has to do himself.

## 1. Rates: cut everything except monthly by about a third
- Menu shoot, half day: $750 -> $500 (20 photos)
- Menu shoot, full day: $1,400 -> $950 (45 photos)
- Dish drop: $350 -> $250 (1 hour, 6 photos)
- Monthly content: stays $600/mo (1 visit, 10 photos)
Rounded to clean numbers. If he wants exact thirds instead ($467 / $933 / $233), change them.

## 2. Animate the logo, slightly
- Subtle only. Ideas: the steam lines drift/wave, the fork lifts the meatball a few px and settles. Loop slowly (3-5s) or play once on load plus on hover.
- Respect prefers-reduced-motion (no animation). No layout shift. Keep it CSS/SVG, no libraries.

## 3. About page
- Photo: replace the flan with a photo of Joshua. There's a portrait in his Cowdog repo: ~/cowdogwebsite/cowdog-main/img/joshua-philadelphia-photographer-cowdog-studio.jpg. Copy it in (rename for SEO, e.g. joshua-albert-philadelphia-food-photographer.jpg), resize to about 1400px, good alt text. If that file is missing, or he says it's the wrong shot, ask him for one.
- Copy: add that he's a photographer with 22 years of restaurant experience. State it as a plain fact, the reason he knows how a kitchen and a menu actually work. Don't make it warm or nostalgic, and don't use his photojournalism background as a credential.
- Add: Sunday Gravy is a sister company of Cowdog Studio, linked to https://www.cowdog.studio (Cowdog does family and engagement portraits). Put it in the About copy and the footer.
- Keep the copy short, spoken, no cheese. Example direction (rewrite as needed):
  "I'm Joshua Albert. I'm a photographer, and I spent 22 years working in restaurants. I know what a menu shoot has to do and how to get it done without getting in the kitchen's way."
  "Sunday Gravy is the sister company of Cowdog Studio."

## 4. Footer redesign
Current footer problems: the butter band reads like a leftover strip, the left text sits flush against the screen edge, and it says almost nothing.
New footer: keep butter as the brand accent, but make it a proper section with real padding and alignment:
- Small logo mark + "Sunday Gravy Studio"
- "Food and drink photography in Philadelphia"
- Nav links (Work, About, Contact/Book)
- Instagram @sundaygravystudio (confirm with him that the handle is claimed before linking it)
- "A sister company of Cowdog Studio" linked to cowdog.studio
- Email once it exists (hello@sundaygravystudio.com isn't set up yet, see below)
- © year Sunday Gravy Studio LLC (confirm the exact legal name with him before publishing; if unsure, use "Sunday Gravy Studio")
Must look right on phone and desktop.

## 5. SEO overhaul
Goal: rank on page 1, as high as possible, for:
- food photography philadelphia / philadelphia food photographer / food photographer philly
- restaurant photography philadelphia / restaurant photographer philly
- also: menu photography philadelphia, cocktail/drink photography philadelphia, bakery photography
Use the Cowdog SEO work as the model (see ~/cowdogwebsite/cowdog-main and the Cowdog lessons below).

### Structure (biggest win)
- Replace the hash-routed single page with real pages, each with its own title, meta description (under 160 chars), H1, canonical, OG tags:
  - / (Home): H1 includes "Food & Restaurant Photography in Philadelphia"
  - /work/ (portfolio)
  - /restaurant-photography/ : main money page for "restaurant photography philadelphia" (menu shoots, openings, dish drops, monthly content, what a shoot day looks like, FAQ)
  - /food-photography/ : money page for "philadelphia food photographer"
  - /drink-photography/ or cocktails section (bars)
  - /pricing/ (the 4 packages)
  - /about/
  - /contact/ (the form)
- Keep the look: same header, same footer, same photos.
- Every page links to the money pages and to /contact/. Descriptive internal link text.

### Technical
- LocalBusiness/ProfessionalService JSON-LD (name, url, logo, image, priceRange, areaServed Philadelphia + neighborhoods/suburbs, geo coordinates, sameAs: Instagram once confirmed, cowdog.studio as related). No street address in schema, same decision as Cowdog. Add parentOrganization or "sameAs" link logic for the Cowdog sister relationship only if schema.org supports it cleanly; otherwise just link it.
- FAQPage schema on the money pages, Service schema per package.
- sitemap.xml with every page, robots.txt, 404.
- Images: WebP + srcset, width/height, lazy loading below the fold, descriptive file names (e.g. birria-tacos-restaurant-photography-philadelphia.jpg) and alt text. Keep the originals.
- Performance: aim for Lighthouse 95+ on mobile. Preload the hero image, font-display swap.
- Favicon set + apple-touch-icon + OG image (1200x630, logo + a hero photo).

### Content
- Write 8-12 blog posts / guides targeting long-tail searches, in his voice (spoken, short sentences). Examples: "How much does restaurant photography cost in Philadelphia", "What to prep before a menu shoot", "Photos for a new restaurant opening: a checklist", "Food photos for Instagram vs. for your menu", "Cocktail photography tips for bars", "Why your delivery app photos matter". Don't future-date them all at once like the Cowdog blog did; date them honestly or spread them realistically.
- Don't invent clients, testimonials, stats or awards. Leave clearly marked placeholders for real testimonials.
- Neighborhood/area mentions where natural (South Philly, East Passyunk, Fishtown, Center City, Old City, Northern Liberties, Main Line) without keyword stuffing.

### Off-site (write a checklist for Joshua in SEO_OFFSITE_CHECKLIST.md; he or Cowork will do these)
- Google Search Console: add https://www.sundaygravystudio.com, verify (DNS TXT in GoDaddy), submit sitemap.
- GA4 property + conversion event on form submit (same pattern as Cowdog: see the cowdog-track.js approach).
- Google Business Profile for Sunday Gravy Studio (service-area business, category Photographer / Commercial photographer / Food photographer if available).
- He owns foodphotographyphilly.com at GoDaddy: 301 it to https://www.sundaygravystudio.com/food-photography/ (Permanent, https, forward only).
- Link from cowdog.studio (footer or About) to sundaygravystudio.com as the sister company.
- Directories: Yelp, Bing Places, Apple Business Connect, Wonderful Machine, Philly food/restaurant groups.

## 6. Contact form + email (needed for the site to actually get leads)
- Wire the contact form the same way the Cowdog /contact/ form is wired (check that repo), with a honeypot. Tell him where submissions will land.
- hello@sundaygravystudio.com will forward to joshua@cowdog.studio (Claude in Cowork is setting this up in GoDaddy/Google Workspace on Sep 29 2026). Show hello@sundaygravystudio.com on the site as the contact email. Form submissions should also land at joshua@cowdog.studio.

## Cowdog lessons to carry over
- Meta descriptions under 160 characters.
- Brand suffix on page titles (" | Sunday Gravy Studio").
- Don't date posts into the future or out of season.
- Self-serving review schema won't show stars (Google policy), so don't rely on it.
- Add analytics from day one; measurement was the weakest part of the Cowdog audit.

## When done
Commit, push to main, verify the live site, and update CLAUDE.md with what changed.
