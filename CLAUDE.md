# Sunday Gravy Studio: project brief for Claude Code

## Who and what
- Owner: Joshua Albert (GitHub: joshua-albert, git email joshuascottalbert@gmail.com). Not very technical. He directs and reviews; you build. Make reasonable calls and show results instead of asking first. Explain anything he has to do himself in plain steps.
- Business: Sunday Gravy Studio, a food and drink photography studio in South Philadelphia, its own LLC, separate from his other business Cowdog Studio (cowdog.studio). Clients: restaurants, bars, bakeries, cafés. No product photography for now.
- Domains he owns: sundaygravystudio.com (primary; site lives at https://www.sundaygravystudio.com) and sundaygravy.studio (should 301 redirect to the primary). Both are registered at GoDaddy (confirmed by Joshua Sep 29 2026), same as his ~30 Cowdog domains. For Cowdog he set up 301 forwarding in GoDaddy (Permanent 301, https, no masking), so use that same pattern for sundaygravy.studio.
- Instagram handle planned: @sundaygravystudio (not yet confirmed as claimed).

## Stack (same approach as his Cowdog site at ~/cowdogwebsite/cowdog-main)
- Static HTML/CSS/JS, no framework. GitHub Pages serves the `main` branch from the repo root. `CNAME` file = www.sundaygravystudio.com. `.nojekyll` present.
- Since Sep 29 2026 the pages are GENERATED: edit `tools/content/*.html` (and `tools/content/blog/`), `tools/build.py` (layout, schema, prices in RATES), `tools/site.css`, then run `python3 tools/build.py` and commit the content and output together. Never hand-edit the generated `*/index.html`; the next build overwrites them. See README.md.
- Photos: `tools/photos.py` (slug + alt, Work page order); `python3 tools/photos.py` makes the WebP sizes (needs Pillow).
- The local ~/cowdogwebsite/cowdog-main checkout is behind origin/main. For current Cowdog code use `git show origin/main:<path>` there (after `git fetch`), or the live site.

## Brand
- Logo: D4.3 "Meatball Lift" (a fork lifting a meatball out of a bowl of spaghetti with two meatballs left, steam), a loose one-color red marker doodle. It's inline SVG, stored grouped (bowl / steam / lift) in tools/mark.svg and animated in site.css: the fork lifts and the steam drifts, looping on the home lockup and on hover in the header and footer, off under prefers-reduced-motion. favicon.svg is the same mark on butter. The final logo will eventually be redrawn by hand and scanned; when he supplies a scan, swap it in.
- Colors: tomato red #D52B1E, ink #1A1918, white page background, butter #F8E7A4 as accent (footer, favicon, social, print).
- Type: Caveat Brush (marker lettering for the name), Fraunces (headlines), Inter Tight (body/UI). All from Google Fonts.
- Layout reference: rlga.photo (minimal, big rotating homepage photo, mark with name under it).

## Copy rules (his voice)
- Sound spoken, not writerly. Short sentences. No cheesy lines, no forced keyword openers, no repeated setup-pivot-punchline, sparing em dashes.
- Don't lean on his photojournalism background as a credential.
- Verify facts before stating them. If you can't verify something, say so.

## Current content (Sep 29 2026, round 2 from NEXT-BRIEF.md)
- Real pages: / (slideshow + lockup + H1 "Food & Restaurant Photography in Philadelphia"), /work/, /restaurant-photography/, /food-photography/, /drink-photography/, /pricing/, /about/, /contact/, /blog/ (10 guides, all dated 2026-09-29, the day they were written), 404.html. Old /#work etc. links redirect via js/site.js.
- Prices (Joshua cut them Sep 29 2026): menu shoot half day $500 (20 photos), full day $950 (45 photos), dish drop $250 (1 hr, 6 photos), monthly content $600/mo (1 visit, 10 photos). He may prefer exact thirds ($467 / $933 / $233).
- About: Joshua photo (from Cowdog), "22 years working in restaurants" as plain fact, sister company of Cowdog Studio (linked, also in footer).
- Contact form posts to the Cowdog Formspree form (xdeoekqz) with subject "Sunday Gravy inquiry: <name> / <business>", honeypot `_gotcha`. Delivers wherever that Formspree form sends (Joshua wants joshua@cowdog.studio). No email address shown on the site.
- GA4: js/sg-track.js has GA_ID = '' until Joshua creates the Sunday Gravy GA4 property. Event generate_lead fires on successful form send.
- Not yet on the site, waiting on Joshua: Instagram handle (unconfirmed), exact LLC legal name (footer says "© Sunday Gravy Studio"), real testimonials (HTML comment placeholders on /about/ and /restaurant-photography/), Google Business Profile link for schema sameAs.
- Copy with assumptions to confirm: he travels to the Main Line and close suburbs; usage covers menu/web/social/delivery apps/Google/press and goes in writing before the shoot; the kitchen plates and he tidies on set; shoots usually before service.
- Off-site SEO to-dos for Joshua: SEO_OFFSITE_CHECKLIST.md.
- Photo source: ~/Desktop/forsundaygravy (originals) and ~/Desktop/forsundaygravy/web (1800px copies).

## First session: get it live
Status Sep 29 2026: first session DONE. DNS verified; HTTPS certificate issued (Let's Encrypt, auto-renews) and Enforce HTTPS on. All of http/https, apex/www and sundaygravy.studio end at https://www.sundaygravystudio.com. Mobile Lighthouse on live: home 100/100/100/100, restaurant page 100s, work 97 perf. Lesson: the cert never started until the custom domain was removed, left off ~2 min, then re-added (instant remove/re-add did nothing). Removing/re-adding via API makes GitHub commit to CNAME on origin, so pull before pushing.

0. Permissions: move `claude-settings.json` to `.claude/settings.json` (mkdir .claude first) and tell Joshua to restart Claude Code so it loads. It pre-approves git, gh, file edits, dig/curl and similar, and blocks force-push and rm -rf.
1. Create a GitHub repo `joshua-albert/sundaygravy-site` (public, so Pages is free) with `gh repo create`, and push `main`. If `gh` isn't installed or logged in, walk him through `brew install gh` and `gh auth login`.
2. Turn on GitHub Pages (Deploy from branch: main, / root) via `gh api`, and set the custom domain to www.sundaygravystudio.com.
3. DNS in GoDaddy (Domain Portfolio > sundaygravystudio.com > DNS). Remove GoDaddy's default parked A record for @ and any default www CNAME first. GitHub Pages' documented records:
   - apex sundaygravystudio.com: A records 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
   - www: CNAME to joshua-albert.github.io
   - Re-check these against docs.github.com before giving them to him.
   - sundaygravy.studio: GoDaddy Forwarding > Permanent (301) to https://www.sundaygravystudio.com, forward only (no masking).
4. After DNS resolves, turn on "Enforce HTTPS". Verify with `dig` and `curl -I`.
5. Tell him exactly what's done and what he still has to click.

## Page background (decided Sep 29 2026)
- White pages so the colorful photos carry the site. Butter #F8E7A4 is the brand accent only: footer band, favicon tile, Instagram, print.

## Next up
- Plug in the GA4 ID, Instagram, GBP link and LLC name when he sends them.
- Confirm the Formspree form delivers to joshua@cowdog.studio; if not, have him make a separate Sunday Gravy form in Formspree and swap the ID in tools/content/contact.html.
- Email: no hello@sundaygravystudio.com yet; the form is the only contact method. Help him choose forwarding vs Google Workspace if he wants an address.
- Work through SEO_OFFSITE_CHECKLIST.md with him.
