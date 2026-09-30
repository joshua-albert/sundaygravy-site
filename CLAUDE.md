# Sunday Gravy Studio: project brief for Claude Code

## Who and what
- Owner: Joshua Albert (GitHub: joshua-albert, git email joshuascottalbert@gmail.com). Not very technical. He directs and reviews; you build. Make reasonable calls and show results instead of asking first. Explain anything he has to do himself in plain steps.
- Business: Sunday Gravy Studio, a food and drink photography studio in South Philadelphia, its own LLC, separate from his other business Cowdog Studio (cowdog.studio). Clients: restaurants, bars, bakeries, cafés. No product photography for now.
- Domains he owns: sundaygravystudio.com (primary; site lives at https://www.sundaygravystudio.com) and sundaygravy.studio (should 301 redirect to the primary). Both are registered at GoDaddy (confirmed by Joshua Sep 29 2026), same as his ~30 Cowdog domains. For Cowdog he set up 301 forwarding in GoDaddy (Permanent 301, https, no masking), so use that same pattern for sundaygravy.studio.
- Instagram: @sundaygravystudio (confirmed his, Sep 30 2026). Linked in the footer, on /contact/ and in schema sameAs.

## Stack (same approach as his Cowdog site at ~/cowdogwebsite/cowdog-main)
- Static HTML/CSS/JS, no framework. GitHub Pages serves the `main` branch from the repo root. `CNAME` file = www.sundaygravystudio.com. `.nojekyll` present.
- Since Sep 29 2026 the pages are GENERATED: edit `tools/content/*.html` (and `tools/content/blog/`), `tools/build.py` (layout, schema, prices in RATES), `tools/site.css`, then run `python3 tools/build.py` and commit the content and output together. Never hand-edit the generated `*/index.html`; the next build overwrites them. See README.md.
- Photos: `tools/photos.py` (slug + alt, Work page order); `python3 tools/photos.py` makes the WebP sizes (needs Pillow).
- The local ~/cowdogwebsite/cowdog-main checkout is behind origin/main. For current Cowdog code use `git show origin/main:<path>` there (after `git fetch`), or the live site.

## Brand (round 3 redesign, Sep 30 2026; brief and preview in design/, which is gitignored)
- Logo: brush-pen redraw of D4.3 "Meatball Lift" (design/mark-brush.svg), one color #D52B1E. Inline on Home (tools/mark.svg, grouped still / lift) with a slow ~1.5px lift of the fork and meatball, off under prefers-reduced-motion. Footer uses /mark.svg as an <img>. favicon.svg = mark on a butter tile; icons and og-image.jpg rendered from it.
- Colors: #fff background, #111 text, #8a8a8a secondary, #e6e6e6 hairlines, #D52B1E only in the logo, butter #F8E7A4 only for the footer bar and favicon.
- Type: Hoss Round Slab via Adobe Fonts kit cur5uhh (<link> to use.typekit.net/cur5uhh.css in every head; kit allows sundaygravystudio.com, www, joshua-albert.github.io, localhost, so preview locally at http://localhost:8765, not 127.0.0.1). Hoss for H1s (clamp 32-64px, -0.02em, lh 1.02), the studio name under the logo (24px/500), rate names and prices (20px), subheads (20px) and body (17px, max 34em). Helvetica stack only for small UI: 11px caps, .04em (nav, footer, labels, form labels, buttons). No bold anywhere.
- Layout: RLGA-style (rlga.photo). Fixed corner nav (Work, Rates left; About, Contact right; current page underlined), plus the small red brush logo (26px tall) top-center on every page except Home, linking to / (aria-label "Sunday Gravy Studio home"). Footer logo + "© 2026 Sunday Gravy Studio" is also one link to /. Content sits in the right-hand 9 of 12 columns with NO left-column labels (Joshua removed them Sep 30 2026); h2 subheads show as small caps inside the content column; generated Questions/More/Book sections have screen-reader-only h2s. Slim butter footer.

## Copy rules (his voice)
- Sound spoken, not writerly. Short sentences. No cheesy lines, no forced keyword openers, no repeated setup-pivot-punchline, sparing em dashes.
- Don't lean on his photojournalism background as a credential.
- Verify facts before stating them. If you can't verify something, say so.

## Current content (Sep 30 2026, round 3)
- Pages: / (slideshow of 13 photos, crossfade every 4s, left third = previous, rest = next; with Reduce Motion it still advances but swaps instantly; hidden H1 "Food & Restaurant Photography in the Philadelphia Area"), /work/ (3-col masonry, 2 on mobile, tap to open full screen, tap to close; hidden H1), /pricing/ (nav label "Rates"; H1 "Launch rates for restaurants, bars and cafés in the Philadelphia area."), /about/ (split screen, sticky B&W photo), /contact/, /restaurant-photography/, /food-photography/, /drink-photography/, /blog/ ("Journal", 10 guides dated 2026-09-29), 404.html. Old /#work, #rates etc. redirect via js/site.js.
- Copy says "Philadelphia area" (titles, meta, copy); schema keeps address Philadelphia, PA and adds areaServed Greater Philadelphia.
- Prices (Sep 30 2026, "launch rates"): dish drop $175 (1 hr, 6 photos), menu shoot half day $400 (20 photos), full day $750 (45 photos, dishes and the room), monthly content $300/mo (1 visit, 10 photos). Source of truth: RATES in tools/build.py; prose mentions are in the service pages and 3 guides.
- Usage note (his words): menu, website, social, Google and delivery apps; ads and packaging quoted separately.
- No turnaround promises anywhere (Joshua, Sep 30 2026). No email address on the site; the form is the contact method.
- Contact form posts to the Cowdog Formspree form (xdeoekqz) with subject "Sunday Gravy inquiry: <name> / <business>", honeypot `_gotcha`. Delivers wherever that Formspree form sends (Joshua wants joshua@cowdog.studio).
- GA4 G-H66S7RM0XF: gtag in every <head> (same pattern as Cowdog); js/sg-track.js adds click/scroll events; js/site.js fires generate_lead after a successful form send.
- Still waiting on Joshua: exact LLC legal name (footer says "© Sunday Gravy Studio"), real testimonials (HTML comment placeholders on /about/ and /restaurant-photography/), Google Business Profile link for schema sameAs.
- Copy with assumptions to confirm: he travels to the Main Line and close suburbs; the kitchen plates and he tidies on set; shoots usually before service.
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


## Next up
- Plug in the GBP link and LLC name when he sends them. In GA4, mark generate_lead as a key event.
- Confirm the Formspree form delivers to joshua@cowdog.studio; if not, have him make a separate Sunday Gravy form in Formspree and swap the ID in tools/content/contact.html.
- Email: no hello@sundaygravystudio.com yet; the form is the only contact method. Help him choose forwarding vs Google Workspace if he wants an address.
- Work through SEO_OFFSITE_CHECKLIST.md with him.
