# Sunday Gravy Studio: off-site SEO checklist

Things that happen outside the website. Do them roughly in this order. Tick them off as you go.

## 1. Google Search Console (do this first)
- [ ] Go to https://search.google.com/search-console and click **Add property**.
- [ ] Choose **Domain** and type `sundaygravystudio.com`.
- [ ] Google gives you a TXT record (starts with `google-site-verification=`). In GoDaddy: Domain Portfolio > sundaygravystudio.com > DNS > **Add New Record** > Type **TXT**, Name `@`, Value = the text Google gave you. Save.
- [ ] Back in Search Console, click **Verify**. It can take a few minutes to an hour.
- [ ] Left menu > **Sitemaps** > enter `https://www.sundaygravystudio.com/sitemap.xml` > Submit.
- [ ] Left menu > **URL inspection** > paste `https://www.sundaygravystudio.com/` > **Request indexing**. Do the same for `/restaurant-photography/` and `/food-photography/`.

## 2. Google Analytics (GA4)
- [ ] Go to https://analytics.google.com > Admin > **Create property**. Name it "Sunday Gravy Studio". Keep it separate from the Cowdog property.
- [ ] Add a **Web** data stream for `https://www.sundaygravystudio.com`.
- [ ] Copy the **Measurement ID** (looks like `G-XXXXXXXXXX`) and send it to Claude. Claude pastes it into `js/sg-track.js` and the site starts reporting.
- [ ] After a few days of data: Admin > Events > mark **generate_lead** as a key event (conversion). That's the one that fires when someone sends the contact form. `contact_click` and `pricing_click` are tracked too.

## 3. Google Business Profile
- [ ] Go to https://business.google.com and create a profile for **Sunday Gravy Studio**.
- [ ] Set it up as a **service-area business** (you go to clients, they don't come to you). Choose **not** to show an address.
- [ ] Service area: Philadelphia, plus the nearby places you'll actually travel to (for example the Main Line towns).
- [ ] Primary category: **Photographer**. Add **Commercial photographer** as a secondary category. If Google offers a food photography category, add that too.
- [ ] Website: `https://www.sundaygravystudio.com/`. Booking link: `https://www.sundaygravystudio.com/contact/`.
- [ ] Add services with prices (menu shoot half day $500, full day $950, dish drop $250, monthly content $600/mo).
- [ ] Upload 10+ photos from the portfolio, plus the logo (`icon-512.png` in the repo) and a cover photo.
- [ ] Verify it (Google will choose video, postcard or phone).
- [ ] Once verified, send Claude the profile's share link so it can go in the site's schema `sameAs`.
- [ ] Ask your first clients for a Google review. Reviews on this profile are what make stars show up in Google. Review schema on your own site won't.

## 4. Point foodphotographyphilly.com at the food photography page
- [ ] GoDaddy > Domain Portfolio > foodphotographyphilly.com > **Forwarding** > Add forwarding.
- [ ] Forward to: `https://www.sundaygravystudio.com/food-photography/`
- [ ] Redirect type: **Permanent (301)**. Forward settings: **Forward only** (no masking). Save.
- [ ] Tell Claude when it's done so it can check that the redirect works.

## 5. Link from Cowdog to Sunday Gravy
- [ ] Ask Claude (in the Cowdog project) to add a line to the cowdog.studio footer or About page: "Sister company: Sunday Gravy Studio, food and drink photography" linked to `https://www.sundaygravystudio.com/`.

## 6. Instagram
- [ ] Claim **@sundaygravystudio** if you haven't. Tell Claude once it's yours. Then Claude adds it to the footer and the schema.
- [ ] Bio link: `https://www.sundaygravystudio.com/`.

## 7. Directories and listings
Use the exact same name everywhere: **Sunday Gravy Studio**. Same website. Same description.
- [ ] **Bing Places** (https://www.bingplaces.com): you can import straight from Google Business Profile once that's verified.
- [ ] **Apple Business Connect** (https://businessconnect.apple.com): shows you in Apple Maps.
- [ ] **Yelp for Business** (https://biz.yelp.com): category Photographers > Commercial Photography if available.
- [ ] **Wonderful Machine** (https://www.wonderfulmachine.com): a paid directory of commercial photographers. Check the price before you sign up.
- [ ] Philly food and restaurant groups: local restaurant owner groups on Facebook, restaurant industry newsletters, the neighborhood business associations (East Passyunk Avenue BID, Fishtown District, Old City District). A link from any of these helps.

## 8. Ongoing
- [ ] Every real client: ask for a Google review and permission to use one or two photos plus a short quote on the site. Send the quote to Claude. There are marked spots on the About and Restaurant photography pages for real testimonials.
- [ ] New shoot, new photos: send Claude your favorites for the Work page.
- [ ] Once a month, check Search Console > **Performance** to see what people searched to find you.
