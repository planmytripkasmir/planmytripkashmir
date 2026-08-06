# Plan My Trip Kashmir — Website

A 38-page static website for a Srinagar-based Kashmir tour & travel business, ready to host on GitHub Pages now and move to premium hosting later with zero code changes.

## What's inside
- **Home, About, Contact** pages
- **10 package pages** (+ listing page) — full itinerary, inclusions/exclusions, pricing, FAQs
- **6 destination pages** (+ listing page) — Srinagar, Gulmarg, Pahalgam, Sonmarg/offbeat, Leh-Ladakh
- **12 blog posts** (+ listing page) — SEO articles targeting your keyword list
- **Gallery, FAQ (30+ Qs), Testimonials, Privacy Policy, Terms & Conditions, 404**
- `sitemap.xml` and `robots.txt` for Google/Bing indexing
- SEO meta titles/descriptions, Open Graph tags, and JSON-LD schema (TravelAgency, TouristTrip, FAQPage, BlogPosting) on every relevant page

## 1. Hosting on GitHub Pages (free, for now)
1. Create a new **public** GitHub repository, e.g. `plan-my-trip-kashmir`.
2. Upload the entire contents of this folder (not the folder itself — the `index.html` should sit at the repo root) — either drag-and-drop on github.com or via git:
   ```
   git init
   git add .
   git commit -m "Launch website"
   git branch -M main
   git remote add origin https://github.com/<your-username>/plan-my-trip-kashmir.git
   git push -u origin main
   ```
3. In the repo, go to **Settings → Pages**, set Source = `main` branch, folder = `/ (root)`, and save.
4. Your site goes live at `https://<your-username>.github.io/plan-my-trip-kashmir/`.

### Important — fix internal links for your GitHub Pages URL
This site uses **relative links** (e.g. `packages/index.html`, `../assets/css/style.css`), so it will work correctly at a project URL like `https://<username>.github.io/plan-my-trip-kashmir/` out of the box. No changes needed for GitHub Pages itself.

### Before moving to premium hosting / a custom domain
Once you buy hosting and a domain (e.g. `planmytripkashmir.com`):
1. Open `build.py` (or just find-and-replace across all `.html` files) and update `SITE_URL` from the placeholder `https://www.planmytripkashmir.com` to your real domain.
2. Re-run `python3 assemble.py && python3 _full_build.py` to regenerate every page with the correct canonical URLs, sitemap and Open Graph tags — OR simply find-and-replace the domain string across all HTML files and `sitemap.xml` if you don't want to touch Python.
3. Re-upload/redeploy.

## 2. Submitting to Google & Bing after going live
1. **Google Search Console** (search.google.com/search-console): add your property (domain or URL prefix), verify ownership, then submit `sitemap.xml`.
2. **Bing Webmaster Tools** (bing.com/webmasters): same process — you can also import directly from Google Search Console.
3. Indexing typically takes a few days to a few weeks. Publishing new blog posts regularly and getting a few backlinks (local directories, Google Business Profile, social media) speeds this up.
4. Set up a **Google Business Profile** for "Plan My Trip Kashmir" at your Srinagar address — this matters as much as the website for local search ("kashmir tour package srinagar").

## 3. Replacing images with your own HD photos
Every image currently loads from Wikimedia Commons (free, Creative-Commons-licensed, no copyright issue) via URLs defined at the top of `build.py` in the `IMG` dictionary. To swap in your own photography:
- **Easiest:** rename your photo files to match, e.g. replace the `src` in the relevant `.html` files directly with `assets/img/yourphoto.jpg`, and add your own images into `assets/img/`.
- **Recommended (keeps everything consistent):** add your photos to `assets/img/`, update the `IMG` dictionary in `build.py` to point to local paths instead of Wikimedia URLs, then re-run `python3 assemble.py && python3 _full_build.py` to regenerate the whole site in one go.
- Keep images under ~300KB each (export as JPG, 1600px wide max) for fast page loads — large unoptimised photos are one of the most common reasons a travel site ranks poorly.

## 4. Editing content (packages, prices, blog posts)
All content lives in plain Python data files, not scattered across 38 HTML files:
- `build_data_packages.py` — all 10 tour packages (price, itinerary, inclusions, FAQs)
- `build_data_destinations.py` — the 6 destination pages
- `build_data_blog.py` — the 12 blog posts
- `build_data_faq.py` — the FAQ page and testimonials

To change a price, fix a typo, or add a new package/blog post: edit the relevant data file, then run:
```
python3 assemble.py && python3 _full_build.py
```
This regenerates every HTML page from scratch in a few seconds — you never hand-edit the HTML files directly (any manual HTML edits will be overwritten next time you rebuild).

## 5. The booking form (currently WhatsApp-based)
Since GitHub Pages can't run server code, the Contact page form and every "Get Exact Quote" button opens a **pre-filled WhatsApp message** to +91 70060 83281 instead of submitting to a server — this works immediately with zero setup. When you move to premium hosting later, ask us (or any developer) to wire the form to a real backend (email service like Formspree, or a PHP/Node handler) for a traditional inbox-based enquiry system — the form's HTML structure in `contact.html` is already built and ready to point at a new endpoint.

## 6. Business details used across the site
- Name: Plan My Trip Kashmir
- Phone/WhatsApp: +91 70060 83281
- Email: planmy.trip.to.sxr@gmail.com
- Address: Check Pora Kalan, Srinagar, Jammu & Kashmir 190015

To change any of these, edit the constants near the top of `build.py` (`PHONE_DISPLAY`, `PHONE_TEL`, `PHONE_WA`, `EMAIL`, `ADDRESS`) and rebuild.

## 7. Design notes
- Palette: ivory/parchment background, deep Dal-Lake teal, saffron gold, chinar brick red
- Type: Cormorant Garamond (headings) + Jost (body), loaded from Google Fonts
- Signature motif: Mughal ogee-arch image frames + gold jaali (lattice) dividers, echoing Kashmir's Mughal garden pavilions
- Fully responsive (mobile menu, responsive grids), keyboard-focus states, and `prefers-reduced-motion` support built in

## Folder structure
```
index.html, about.html, contact.html, gallery.html, faq.html, testimonials.html,
privacy-policy.html, terms-conditions.html, 404.html, sitemap.xml, robots.txt
packages/        (index.html + 10 package pages)
destinations/    (index.html + 5 destination pages)
blog/            (index.html + 12 blog posts)
assets/css/style.css
assets/js/main.js
assets/img/logo.svg, icon.svg
build.py, build_data_*.py, build_pages_*.py, assemble.py, _full_build.py   ← the generator (see section 4)
```

Questions or want help wiring a real backend, custom domain, or booking system later — just ask.
