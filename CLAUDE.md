# Sunday Gravy Studio: project brief for Claude Code

## Who and what
- Owner: Joshua Albert (GitHub: joshua-albert, git email joshuascottalbert@gmail.com). Not very technical. He directs and reviews; you build. Make reasonable calls and show results instead of asking first. Explain anything he has to do himself in plain steps.
- Business: Sunday Gravy Studio, a food and drink photography studio in South Philadelphia, its own LLC, separate from his other business Cowdog Studio (cowdog.studio). Clients: restaurants, bars, bakeries, cafés. No product photography for now.
- Domains he owns: sundaygravystudio.com (primary; site lives at https://www.sundaygravystudio.com) and sundaygravy.studio (should 301 redirect to the primary). Both are registered at GoDaddy (confirmed by Joshua Sep 29 2026), same as his ~30 Cowdog domains. For Cowdog he set up 301 forwarding in GoDaddy (Permanent 301, https, no masking), so use that same pattern for sundaygravy.studio.
- Instagram handle planned: @sundaygravystudio (not yet confirmed as claimed).

## Stack (same approach as his Cowdog site at ~/cowdogwebsite/cowdog-main)
- Hand-written static HTML/CSS/JS, no framework, no build step. GitHub Pages serves the `main` branch from the repo root. `CNAME` file = www.sundaygravystudio.com. `.nojekyll` present.
- Keep it that way unless there's a strong reason. Look at the Cowdog repo for patterns (SEO meta, schema, contact form, sitemap) and reuse what works.

## Brand
- Logo: D4.3 "Meatball Lift" (a fork lifting a meatball out of a bowl of spaghetti with two meatballs left, steam), a loose one-color red marker doodle. It's inline SVG in index.html; favicon.svg is the same mark on butter. The final logo will eventually be redrawn by hand and scanned; when he supplies a scan, swap it in.
- Colors: tomato red #D52B1E, ink #1A1918, white page background, butter #F8E7A4 as accent (footer, favicon, social, print).
- Type: Caveat Brush (marker lettering for the name), Fraunces (headlines), Inter Tight (body/UI). All from Google Fonts.
- Layout reference: rlga.photo (minimal, big rotating homepage photo, mark with name under it).

## Copy rules (his voice)
- Sound spoken, not writerly. Short sentences. No cheesy lines, no forced keyword openers, no repeated setup-pivot-punchline, sparing em dashes.
- Don't lean on his photojournalism background as a credential.
- Verify facts before stating them. If you can't verify something, say so.

## Current content
- Pages (hash-routed views in index.html): Home (10-photo slideshow + lockup), Work (21-photo grid + lightbox), About, Contact (prices + inquiry form).
- Prices on the page are PROPOSED, not final: menu shoot half day $750 (20 photos), full day $1,400 (45 photos), dish drop $350 (1 hr, 6 photos), monthly content $600/mo (1 visit, 10 photos). Confirm with him before treating as final.
- Photo source: ~/Desktop/forsundaygravy (originals) and ~/Desktop/forsundaygravy/web (1800px copies).

## First session: get it live
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

## Next up (after it's live)
- Split the hash views into real pages (/work/, /about/, /contact/) for SEO, with titles, meta descriptions, LocalBusiness schema (no street address in schema; geo + areaServed only, same decision as Cowdog), sitemap.
- Wire the contact form the same way the Cowdog /contact/ form is wired (it works), plus a honeypot.
- Email: hello@sundaygravystudio.com isn't set up yet. The page flags it in red. Help him choose forwarding vs Google Workspace.
- Google Search Console + GA4, Google Business Profile.
- Image optimization (WebP + srcset), alt text is already written.
