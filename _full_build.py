# -*- coding: utf-8 -*-
"""
Static site generator for Plan My Trip Kashmir
Outputs a full multi-page HTML site into /home/claude/site (this folder).
Run: python3 build.py
"""
import os, re
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "https://www.planmytripkashmir.com"  # placeholder — update after custom domain / note GH Pages URL in README
BIZ_NAME = "Plan My Trip Kashmir"
PHONE_DISPLAY = "+91 70060 83281"
PHONE_TEL = "+917006083281"
PHONE_WA = "917006083281"
EMAIL = "planmy.trip.to.sxr@gmail.com"
ADDRESS = "Check Pora Kalan, Srinagar, Jammu & Kashmir 190015"

# ---------------------------------------------------------------
# Free-to-use image bank (Wikimedia Commons, CC-licensed) served
# via the stable Special:FilePath redirect. Swap any of these for
# your own HD photos later — see README "Replacing Images".
# ---------------------------------------------------------------
def wimg(filename, width=1600):
    return f"https://commons.wikimedia.org/wiki/Special:FilePath/{quote(filename)}?width={width}"

IMG = {
    "dal_sunset":      wimg("Houseboat- Dal Lake, srinagar Kashmir.JPG"),
    "dal_wide":        wimg("Srinagar - Dal lake and around 42.JPG"),
    "houseboat":       wimg("Houseboat at Dal Lake.JPG"),
    "shikara":         wimg("Shikara & house boat in Dal Lake.JPG"),
    "gulmarg_gondola": wimg("Gulmarg Gondola.JPG"),
    "gulmarg_gondola2":wimg("Gulmarg gondola.JPG"),
    "gulmarg_meadow":  wimg("Gulmarg.JPG"),
    "gulmarg_station": wimg("Gulmarg Kungdoor gondola station.JPG"),
    "gulmarg_cable":   wimg("Gulmarg Gondola, Cable Car.JPG"),
    "betaab1":         wimg("Betaab Valley Pahalgam.jpg"),
    "aru_valley":      wimg("Aru Valley Pehalgam Jammu and Kashmir.jpg"),
    "pahalgam_valley": wimg("Pahalgam Valley.jpg"),
    "betaab2":         wimg("Betaab Valley, Pehalgam, Kashmir.jpg"),
    "pahalgam_autumn": wimg("Autumn weather in pahalgam kashmir valley.jpg"),
    "pahalgam_peaks":  wimg("Himalayan peaks visible from pahalgam valley.jpg"),
    "nishat_bagh":     wimg("Nishat Bagh, A Mughal Garden in Srinagar.jpg"),
    "shalimar_arch":   wimg("Mughal era architecture inside of the Shalimar Bagh, Srinagar.jpg"),
    "shalimar_pav":    wimg("Pavillion inside Shalimar Bagh.jpg"),
    "pangong1":        wimg("Lake Pangong (Pangong Tso) in Ladakh.jpg"),
    "pangong2":        wimg("Pangong Lake, Ladakh, India 06.jpg"),
    "leh1":            wimg("Leh, Ladakh, India.jpg"),
    "leh2":            wimg("Leh Ladakh.jpg"),
    "vaishno1":        wimg("A Hindu temple on hilltop at Katra, Jammu & Kashmir.jpg"),
    "vaishno2":        wimg("SHRI MATA VAISHNO DEVI SHRINE BOARD.jpg"),
    "pangong3":        wimg("A panoramic view of the Pangong Tso lake, in Ladakh.jpg"),
}

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def slugify(s):
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")

# ---------------------------------------------------------------
# Nav structure (used everywhere)
# ---------------------------------------------------------------
NAV_LINKS = [
    ("index.html", "Home"),
    ("packages/index.html", "Packages"),
    ("destinations/index.html", "Destinations"),
    ("gallery.html", "Gallery"),
    ("blog/index.html", "Blog"),
    ("faq.html", "FAQs"),
    ("testimonials.html", "Reviews"),
    ("about.html", "About Us"),
    ("contact.html", "Contact"),
]

def head(prefix, title, desc, canonical_path, og_image=None, extra_schema="", noindex=False):
    og_image = og_image or IMG["dal_sunset"]
    robots = "noindex,follow" if noindex else "index,follow"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{SITE_URL}/{canonical_path}">
<link rel="icon" type="image/svg+xml" href="{prefix}assets/img/icon.svg">
<meta name="theme-color" content="#123240">

<meta property="og:type" content="website">
<meta property="og:site_name" content="{BIZ_NAME}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{og_image}">
<meta property="og:url" content="{SITE_URL}/{canonical_path}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{og_image}">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Jost:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}assets/css/style.css">
{extra_schema}
</head>
"""

def local_business_schema():
    return f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "TravelAgency",
  "name": "{BIZ_NAME}",
  "image": "{IMG['dal_sunset']}",
  "url": "{SITE_URL}",
  "telephone": "{PHONE_TEL}",
  "email": "{EMAIL}",
  "priceRange": "₹₹",
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "Check Pora Kalan",
    "addressLocality": "Srinagar",
    "addressRegion": "Jammu and Kashmir",
    "postalCode": "190015",
    "addressCountry": "IN"
  }},
  "areaServed": "Jammu and Kashmir",
  "sameAs": []
}}
</script>"""

def header_html(prefix, active):
    links = ""
    for href, label in NAV_LINKS:
        cls = " active" if href == active else ""
        links += f'<a href="{prefix}{href}" class="link{cls}">{label}</a>\n'
    return f"""<header class="site-header">
  <div class="nav-wrap">
    <a href="{prefix}index.html" class="brand" aria-label="{BIZ_NAME} home">
      <img src="{prefix}assets/img/logo.svg" alt="{BIZ_NAME} logo" width="180" height="52">
    </a>
    <nav class="main-nav" id="mainNav">
      {links}
      <a href="{prefix}contact.html" class="btn btn-gold" style="margin-top:10px;">Get a Free Quote</a>
    </nav>
    <div class="nav-cta">
      <a href="tel:{PHONE_TEL}" class="nav-call"><span aria-hidden="true">📞</span><span class="label">{PHONE_DISPLAY}</span></a>
      <button class="menu-toggle" id="menuToggle" aria-label="Toggle menu" aria-expanded="false">☰</button>
    </div>
  </div>
</header>
"""

def footer_html(prefix):
    pkg_links = "".join(f'<a href="{prefix}packages/{p["slug"]}.html">{p["title"]}</a>\n' for p in PACKAGES_SHORT_FOR_FOOTER)
    dest_links = "".join(f'<a href="{prefix}destinations/{d["slug"]}.html">{d["title"]}</a>\n' for d in DESTINATIONS_SHORT_FOR_FOOTER)
    return f"""<footer>
  <div class="container footer-grid">
    <div>
      <img src="{prefix}assets/img/logo.svg" alt="{BIZ_NAME}" width="180" height="52" style="margin-bottom:16px;filter:brightness(0) invert(1) opacity(0.92);">
      <p style="color:#B9C6C9;max-width:320px;">Locally owned tour and travel company based in Srinagar, Jammu &amp; Kashmir, crafting private and group Kashmir holiday packages — houseboats, Gulmarg, Pahalgam, Sonmarg, Ladakh and Vaishno Devi — at prices built to beat the standard market rate.</p>
      <div class="social-row">
        <a href="#" aria-label="Facebook">f</a>
        <a href="#" aria-label="Instagram">ig</a>
        <a href="#" aria-label="YouTube">yt</a>
      </div>
    </div>
    <div>
      <h4>Packages</h4>
      {pkg_links}
      <a href="{prefix}packages/index.html">View All Packages →</a>
    </div>
    <div>
      <h4>Destinations</h4>
      {dest_links}
      <a href="{prefix}destinations/index.html">All Destinations →</a>
    </div>
    <div>
      <h4>Contact</h4>
      <a href="tel:{PHONE_TEL}">📞 {PHONE_DISPLAY}</a>
      <a href="https://wa.me/{PHONE_WA}">💬 WhatsApp Us</a>
      <a href="mailto:{EMAIL}">✉️ {EMAIL}</a>
      <a href="{prefix}contact.html">📍 {ADDRESS}</a>
    </div>
  </div>
  <div class="container footer-bottom">
    <span>© <span id="yr"></span> {BIZ_NAME}. All rights reserved.</span>
    <span><a href="{prefix}privacy-policy.html">Privacy Policy</a> &nbsp;·&nbsp; <a href="{prefix}terms-conditions.html">Terms &amp; Conditions</a></span>
  </div>
</footer>
<a href="https://wa.me/{PHONE_WA}" class="wa-float" aria-label="Chat on WhatsApp">💬</a>
<script>document.getElementById('yr').textContent = new Date().getFullYear();</script>
<script src="{prefix}assets/js/main.js"></script>
</body>
</html>"""

def page(prefix, active, title, desc, canonical_path, body, og_image=None, extra_schema="", noindex=False):
    return head(prefix, title, desc, canonical_path, og_image, extra_schema, noindex) + "<body>\n" + header_html(prefix, active) + body + footer_html(prefix)

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


# Package data — imported into build.py
PACKAGES = [
{
    "slug": "kashmir-paradise-getaway-5n-6d",
    "title": "Kashmir Paradise Getaway",
    "duration": "5 Nights / 6 Days",
    "route": "Srinagar – Gulmarg – Pahalgam – Sonmarg",
    "category": "Best Seller",
    "price": 24999, "old_price": 27999,
    "hero": IMG["dal_sunset"], "gallery": [IMG["gulmarg_gondola"], IMG["betaab1"], IMG["nishat_bagh"]],
    "meta_title": "Kashmir Tour Package 5 Nights 6 Days | Srinagar Gulmarg Pahalgam | Plan My Trip Kashmir",
    "meta_desc": "Book our best-selling Kashmir tour package (5N/6D) covering Srinagar, Gulmarg, Pahalgam & Sonmarg with houseboat stay, shikara ride & transfers. Prices up to 10% below the standard market rate.",
    "intro": "Our most-booked Kashmir trip package, built for first-time travellers who want to see the valley's four icons — Dal Lake, Gulmarg, Pahalgam and Sonmarg — without rushing. You spend a night aboard a traditional houseboat, ride the Gulmarg Gondola toward the Apharwat slopes, walk through the pine-lined meadows of Betaab and Aru, and end the day in Sonmarg beside the Sindh River, all on a fixed departure or private itinerary that our Srinagar-based team runs from arrival to airport drop.",
    "highlights": [
        "1 night aboard a deluxe houseboat on Dal Lake with a private shikara ride",
        "Gulmarg Gondola (Phase 1) cable-car ride toward Kongdoori",
        "Pahalgam sightseeing: Betaab Valley, Aru Valley and the Lidder riverside",
        "Half-day excursion to Sonmarg — Thajiwas Glacier viewpoint",
        "Srinagar Mughal Gardens: Nishat Bagh and Shalimar Bagh",
        "All airport/railway station transfers by private AC vehicle",
    ],
    "itinerary": [
        ("Day 1 — Arrival in Srinagar & Houseboat Check-in", "Land at Srinagar Airport, where our representative greets you and transfers you to your houseboat on Dal Lake. Spend the afternoon at leisure or take an optional shikara ride past the floating vegetable market. Evening tea is served on the houseboat deck as the sun sets over the Zabarwan hills. Overnight on the houseboat."),
        ("Day 2 — Srinagar Local Sightseeing & Mughal Gardens", "After breakfast, visit Nishat Bagh and Shalimar Bagh, the terraced Mughal gardens built on Dal Lake's eastern shore, followed by Chashme Shahi and a stop at Shankaracharya Hill for a panoramic view of the city. Return for a one-hour shikara ride through the lake's quieter channels in the evening. Overnight in Srinagar."),
        ("Day 3 — Srinagar to Gulmarg Day Excursion", "Drive roughly 50 km (about 1.5 hours) to Gulmarg, the 'meadow of flowers'. Take the Gulmarg Gondola cable car up to Kongdoori for views of the Apharwat range (Phase 2 ropeway to Apharwat is optional and paid directly at the counter, subject to weather). Explore the golf course and pine forest before returning to Srinagar by evening."),
        ("Day 4 — Srinagar to Pahalgam", "Drive to Pahalgam (about 90 km, 2.5–3 hours), stopping at the saffron fields of Pampore and the Awantipora ruins en route. Check in to your hotel and spend the evening walking along the Lidder River. Overnight in Pahalgam."),
        ("Day 5 — Pahalgam Valley Sightseeing & Sonmarg Transfer", "Visit Betaab Valley and Aru Valley by local taxi (included) before driving to Sonmarg via Srinagar. Sonmarg sits at the base of the Thajiwas Glacier and the road to Ladakh via Zoji La. Overnight in Sonmarg or Srinagar depending on hotel availability."),
        ("Day 6 — Departure", "After breakfast, transfer to Srinagar Airport or railway station for your onward journey, with fond memories of the valley and a printed photo voucher from our team."),
    ],
    "inclusions": [
        "5 nights accommodation (1 houseboat + 4 hotel) on double/twin sharing",
        "Daily breakfast and dinner (MAP plan)",
        "All transfers and sightseeing by private AC vehicle (Innova/Sumo/similar)",
        "1 hour shikara ride on Dal Lake",
        "Gulmarg Gondola Phase 1 ticket",
        "All applicable tolls, parking and driver allowance",
        "Dedicated trip coordinator on WhatsApp throughout your stay",
    ],
    "exclusions": [
        "Airfare/train fare to and from Srinagar",
        "Gulmarg Gondola Phase 2 (Apharwat) ticket — paid on the spot, weather dependent",
        "Pony/horse rides, sledging and other optional adventure activities",
        "Lunch and any meals not mentioned in inclusions",
        "Personal expenses, tips and travel insurance",
        "GST and anything not specifically mentioned as included",
    ],
    "faqs": [
        ("Is 5 nights 6 days enough to cover Kashmir?", "Yes — this is the most popular duration for a first Kashmir trip. It comfortably covers Srinagar, Gulmarg, Pahalgam and a Sonmarg excursion without feeling rushed. If you also want Ladakh or Vaishno Devi, ask us about our extended packages."),
        ("Can this package be customised?", "Yes. Every itinerary on this page is a starting template — we adjust the number of days in each destination, upgrade hotel categories, or add Ladakh, Doodhpathri or Vaishno Devi on request at no planning fee."),
        ("Is the houseboat safe and comfortable?", "We work only with registered houseboat owners on Dal Lake who meet Jammu & Kashmir Tourism's safety and hygiene standards. Rooms include attached bathrooms, running hot water and heating on request."),
    ],
},
{
    "slug": "kashmir-express-4n-5d",
    "title": "Kashmir Express",
    "duration": "4 Nights / 5 Days",
    "route": "Srinagar – Gulmarg – Pahalgam",
    "category": "Budget Friendly",
    "price": 17999, "old_price": 19999,
    "hero": IMG["gulmarg_meadow"], "gallery": [IMG["dal_wide"], IMG["pahalgam_valley"], IMG["shikara"]],
    "meta_title": "Kashmir Tour Package 4 Nights 5 Days | Budget Srinagar Gulmarg Pahalgam Trip",
    "meta_desc": "A compact, affordable Kashmir holiday package covering Srinagar, Gulmarg and Pahalgam in 4 nights 5 days. Ideal short trip to Kashmir with hotel, transfers and sightseeing included.",
    "intro": "Short on leave but long on wanderlust? Kashmir Express is a tightly-planned 4N/5D itinerary for travellers who want the highlights — Dal Lake, Gulmarg's meadows and Pahalgam's valleys — without a long trip. It's our most affordable full-circuit package and a favourite with working professionals and college friend groups looking for a quick Kashmir tour package from Srinagar airport back to Srinagar airport.",
    "highlights": [
        "Covers all 3 core destinations in just 4 nights",
        "1 night houseboat stay with shikara ride included",
        "Gulmarg Gondola Phase 1 cable car ride",
        "Pahalgam's Betaab Valley by local sightseeing cab",
        "Compact pricing — our lowest full-circuit package",
        "Private transfers throughout, no shared coaches",
    ],
    "itinerary": [
        ("Day 1 — Arrival & Srinagar Houseboat", "Airport pickup and transfer to your Dal Lake houseboat. Evening shikara ride included. Overnight on the houseboat."),
        ("Day 2 — Srinagar to Gulmarg", "Morning drive to Gulmarg, gondola ride to Kongdoori, a walk through the meadow and golf course, then return to Srinagar for the night."),
        ("Day 3 — Srinagar to Pahalgam", "Drive to Pahalgam via the saffron town of Pampore. Evening free to explore the Lidder riverside market. Overnight in Pahalgam."),
        ("Day 4 — Pahalgam Sightseeing & Return to Srinagar", "Local sightseeing cab to Betaab Valley and Aru Valley, then drive back to Srinagar for a final evening at the Boulevard promenade beside Dal Lake."),
        ("Day 5 — Departure", "Transfer to Srinagar Airport for your flight home."),
    ],
    "inclusions": [
        "4 nights accommodation (1 houseboat + 3 hotel), double sharing",
        "Daily breakfast and dinner",
        "All transfers and sightseeing in a private AC vehicle",
        "Shikara ride and Gulmarg Gondola Phase 1 ticket",
        "Driver allowance, parking and tolls",
    ],
    "exclusions": [
        "Airfare/train fare",
        "Gondola Phase 2, pony rides and adventure activities",
        "Lunches, personal expenses and tips",
        "GST and anything not listed under inclusions",
    ],
    "faqs": [
        ("Is 4 nights too short for Kashmir?", "It's the leanest version of our full-circuit itinerary — enough to see Srinagar, Gulmarg and Pahalgam, though each stop is a little brisker than our 5N/6D package. Great for a long weekend trip."),
        ("Can I add Sonmarg to this package?", "Yes, we can extend this to 5N/6D with a Sonmarg day trip for a small supplement — message us on WhatsApp and we'll requote instantly."),
    ],
},
{
    "slug": "kashmir-honeymoon-bliss-6n-7d",
    "title": "Kashmir Honeymoon Bliss",
    "duration": "6 Nights / 7 Days",
    "route": "Srinagar – Gulmarg – Pahalgam – Sonmarg",
    "category": "For Couples",
    "price": 31499, "old_price": 34999,
    "hero": IMG["shalimar_pav"], "gallery": [IMG["dal_sunset"], IMG["gulmarg_gondola2"], IMG["betaab2"]],
    "meta_title": "Kashmir Honeymoon Package | Romantic Kashmir Trip for Couples | Plan My Trip Kashmir",
    "meta_desc": "Kashmir honeymoon package with candlelight houseboat dinner, private shikara ride and couple-friendly hotels across Srinagar, Gulmarg, Pahalgam and Sonmarg. Best Kashmir tour packages for couples.",
    "intro": "Kashmir has been called Paradise on Earth by Mughal emperors who built entire gardens for the people they loved — it remains one of India's most romantic honeymoon destinations. This package is paced for couples: candlelight dinner on your houseboat, a private sunset shikara ride, quieter viewpoints away from the crowds, and couple-friendly rooms with lake or mountain views across all 4 destinations.",
    "highlights": [
        "2 nights luxury houseboat with candlelight dinner on Dal Lake",
        "Private sunset shikara ride for two",
        "Couple-friendly hotel rooms with valley or lake views",
        "Gulmarg Gondola ride with photo stop at Kongdoori",
        "Romantic riverside evening in Pahalgam by the Lidder",
        "Flexible pacing — no early-morning rush days",
    ],
    "itinerary": [
        ("Day 1 — Arrival & Welcome to Dal Lake", "Airport pickup, transfer to your deluxe houseboat, welcome drink and a relaxed first evening with a candlelight dinner served on the private deck."),
        ("Day 2 — Sunrise Shikara & Srinagar Gardens", "An easy morning shikara ride through the floating gardens, followed by a visit to Nishat Bagh and Shalimar Bagh. Free evening to stroll the Boulevard."),
        ("Day 3 — Gulmarg Day Trip", "Drive to Gulmarg for the gondola ride to Kongdoori. Couples can pause at the meadow for photographs before returning to Srinagar for a second night on the houseboat."),
        ("Day 4 — Srinagar to Pahalgam", "Scenic drive to Pahalgam through the saffron fields of Pampore. Check in to a valley-facing hotel and spend the evening beside the Lidder River."),
        ("Day 5 — Pahalgam Valleys", "Visit Betaab Valley and Aru Valley by local cab — both are popular film locations and offer quiet picnic spots for couples."),
        ("Day 6 — Sonmarg Excursion", "Half-day trip to Sonmarg for glacier and river views, then return to Srinagar for a final relaxed evening."),
        ("Day 7 — Departure", "Transfer to Srinagar Airport with our compliments and a printed trip memento."),
    ],
    "inclusions": [
        "6 nights accommodation (2 houseboat + 4 hotel), couple room",
        "Daily breakfast and dinner, including 1 candlelight dinner",
        "Private sunset shikara ride",
        "All transfers and sightseeing by private AC vehicle",
        "Gulmarg Gondola Phase 1 ticket",
        "Room décor on the houseboat for the first night",
    ],
    "exclusions": [
        "Airfare/train fare", "Gondola Phase 2 and adventure activities",
        "Lunches, personal expenses, spa/salon services",
        "GST and anything not mentioned under inclusions",
    ],
    "faqs": [
        ("Do you offer room décor for the honeymoon night?", "Yes, basic room décor (flowers and a welcome setup) is included on your first houseboat night. Premium décor and cake can be added for an extra charge."),
        ("Are the hotels couple-friendly for unmarried couples?", "We work with hotels that accept couples with a valid ID proof for both guests. Let us know your preference while booking and we'll confirm the right property."),
    ],
},
{
    "slug": "kashmir-family-wonders-6n-7d",
    "title": "Kashmir Family Wonders",
    "duration": "6 Nights / 7 Days",
    "route": "Srinagar – Gulmarg – Pahalgam – Sonmarg",
    "category": "Family Friendly",
    "price": 30499, "old_price": 33999,
    "hero": IMG["nishat_bagh"], "gallery": [IMG["dal_wide"], IMG["gulmarg_station"], IMG["aru_valley"]],
    "meta_title": "Kashmir Tour Packages for Family | Kids & Senior Friendly Kashmir Trip",
    "meta_desc": "Family-friendly Kashmir holiday package with relaxed pacing, comfortable hotels and easy sightseeing suited to kids and grandparents. Covers Srinagar, Gulmarg, Pahalgam and Sonmarg.",
    "intro": "Travelling with children or elderly parents needs a different rhythm — fewer early starts, easier walking distances and hotels with family rooms. Kashmir Family Wonders is designed exactly for that: a full 6-night circuit with buffer time built into each day, wheelchair/senior-friendly gondola access at Gulmarg, and a private vehicle throughout so nobody has to rush between stops.",
    "highlights": [
        "Relaxed daily pace with built-in rest time",
        "Family/triple rooms available across all hotels",
        "Kid-friendly shikara ride and pony rides in Pahalgam (optional)",
        "Gulmarg Gondola with easy boarding assistance",
        "Doctor-on-call support arranged if required",
        "Private vehicle with extra luggage space",
    ],
    "itinerary": [
        ("Day 1 — Arrival in Srinagar", "Airport pickup, houseboat check-in, and a gentle first evening — no sightseeing planned so the family can settle in after travel."),
        ("Day 2 — Srinagar Sightseeing", "Visit Nishat Bagh, Shalimar Bagh and Chashme Shahi at an easy pace, with plenty of photo stops and open lawns for children to run around."),
        ("Day 3 — Gulmarg Day Trip", "Gondola ride to Kongdoori (assistance provided for seniors), meadow walk, and an early return to Srinagar for rest."),
        ("Day 4 — Srinagar to Pahalgam", "Comfortable drive to Pahalgam with a stop at Pampore's saffron fields. Family hotel check-in with river-view rooms where available."),
        ("Day 5 — Pahalgam Valley Sightseeing", "Betaab Valley and Aru Valley by local cab, with time for pony rides and riverside picnics — a favourite day for children."),
        ("Day 6 — Sonmarg Excursion", "Half-day Sonmarg trip for glacier views, then an early return to Srinagar for packing and a relaxed final dinner."),
        ("Day 7 — Departure", "Timed airport transfer with buffer for check-in."),
    ],
    "inclusions": [
        "6 nights accommodation (2 houseboat + 4 hotel), family/triple rooms available",
        "Daily breakfast and dinner",
        "Private AC vehicle with extra boot space",
        "Shikara ride and Gulmarg Gondola Phase 1",
        "Assistance for elderly travellers at sightseeing points",
    ],
    "exclusions": [
        "Airfare/train fare", "Pony rides and adventure activities",
        "Lunches, personal expenses",
        "GST and anything not mentioned under inclusions",
    ],
    "faqs": [
        ("Is this package suitable for toddlers and grandparents together?", "Yes — this is exactly the itinerary we recommend for multi-generational family trips. We keep driving distances shorter per day and avoid back-to-back long drives."),
        ("Can you arrange a wheelchair or extra assistance?", "Yes, let us know in advance and we'll arrange wheelchair assistance at the airport and gondola stations, plus a driver briefed on any specific needs."),
    ],
},
{
    "slug": "srinagar-short-break-3n-4d",
    "title": "Srinagar City & Gardens Short Break",
    "duration": "3 Nights / 4 Days",
    "route": "Srinagar Only",
    "category": "Short Trip",
    "price": 14299, "old_price": 15999,
    "hero": IMG["dal_wide"], "gallery": [IMG["shalimar_arch"], IMG["shikara"], IMG["houseboat"]],
    "meta_title": "Srinagar Tour Package 3 Nights 4 Days | Srinagar Holiday Package with Houseboat",
    "meta_desc": "Srinagar-only holiday package with houseboat stay, shikara ride and Mughal Garden sightseeing. A quick srinagar trip package ideal for weekend travellers and business add-on trips.",
    "intro": "Not everyone has a week to spare. This Srinagar-focused package is built for travellers extending a business trip, a weekend getaway, or a first taste of Kashmir before deciding to come back for the full circuit. It covers the city's essential experiences — Dal Lake, the Mughal Gardens and the old city — from a comfortable houseboat or hotel base.",
    "highlights": [
        "2 nights houseboat + 1 night hotel in Srinagar",
        "Shikara ride through Dal Lake's floating gardens",
        "Nishat Bagh, Shalimar Bagh and Chashme Shahi",
        "Old city walk past Jamia Masjid and the riverside markets",
        "Optional half-day add-on to Gulmarg or Pahalgam",
    ],
    "itinerary": [
        ("Day 1 — Arrival & Houseboat Check-in", "Airport pickup and houseboat check-in on Dal Lake. Evening shikara ride to watch the sunset over the Zabarwan range."),
        ("Day 2 — Mughal Gardens & Shankaracharya Hill", "Full day covering Nishat Bagh, Shalimar Bagh, Chashme Shahi and the viewpoint at Shankaracharya Temple."),
        ("Day 3 — Old City & Local Markets", "Visit the old city's wooden architecture, Jamia Masjid and Hazratbal Shrine, followed by free time for shopping Pashmina shawls and papier-mâché souvenirs."),
        ("Day 4 — Departure", "Transfer to Srinagar Airport or railway station."),
    ],
    "inclusions": [
        "3 nights accommodation (2 houseboat + 1 hotel)",
        "Daily breakfast", "Airport transfers and city sightseeing by private vehicle",
        "1 hour shikara ride",
    ],
    "exclusions": [
        "Airfare/train fare", "Lunch and dinner (available on request at extra cost)",
        "Entry tickets to gardens (nominal, paid on the spot)",
        "GST and anything not mentioned under inclusions",
    ],
    "faqs": [
        ("Can I extend this into a Gulmarg or Pahalgam day trip?", "Yes, we offer this as an optional add-on for a day-trip supplement — just mention it while booking."),
        ("Is 3 nights enough to see Srinagar properly?", "It's enough to comfortably cover the Mughal Gardens, Dal Lake and the old city at a relaxed pace, without feeling rushed."),
    ],
},
{
    "slug": "gulmarg-snow-special-5n-6d",
    "title": "Gulmarg Snow Special",
    "duration": "5 Nights / 6 Days",
    "route": "Srinagar – Gulmarg (Winter)",
    "category": "Winter / December",
    "price": 25999, "old_price": 28999,
    "hero": IMG["gulmarg_cable"], "gallery": [IMG["gulmarg_gondola"], IMG["dal_sunset"], IMG["gulmarg_station"]],
    "meta_title": "Kashmir in December | Gulmarg Snow Package | Winter Kashmir Tour",
    "meta_desc": "Plan your Kashmir trip in December with our Gulmarg Snow Special package — snowfall, gondola rides and skiing at Asia's highest ski resort, plus Srinagar houseboat stay.",
    "intro": "December to February turns Gulmarg into one of Asia's premier snow destinations, with the Gondola climbing above snow-laden pine forests toward Apharwat Peak. This package is built around that season — extra nights in Gulmarg, warm-clothing guidance, and a flexible itinerary that adjusts to road and weather conditions, which is standard practice for any responsible Kashmir tour operator in winter.",
    "highlights": [
        "2 nights in Gulmarg during peak snow season",
        "Gulmarg Gondola Phase 1 (and Phase 2 optional, weather permitting)",
        "Skiing and snowboarding lessons available (paid add-on)",
        "Sledging in the snow meadows",
        "Srinagar houseboat stay with in-room heating",
        "Winter clothing and boot rental guidance provided",
    ],
    "itinerary": [
        ("Day 1 — Arrival in Srinagar", "Airport pickup and houseboat check-in with heated rooms. Evening at leisure."),
        ("Day 2 — Srinagar Sightseeing", "Visit Nishat Bagh, Shalimar Bagh and Chashme Shahi (some gardens have shorter winter hours)."),
        ("Day 3 — Drive to Gulmarg", "Transfer to Gulmarg, check in to a heated hotel and spend the afternoon walking through the snow-covered meadow."),
        ("Day 4 — Gondola & Snow Activities", "Full day for the Gondola ride, optional skiing lesson at the ski school, and sledging with local guides."),
        ("Day 5 — Gulmarg to Srinagar", "Morning at leisure in Gulmarg before returning to Srinagar for a final houseboat night."),
        ("Day 6 — Departure", "Transfer to Srinagar Airport."),
    ],
    "inclusions": [
        "5 nights accommodation (2 houseboat + 3 hotel) with heating",
        "Daily breakfast and dinner", "Private AC/heated vehicle for all transfers",
        "Gulmarg Gondola Phase 1 ticket",
    ],
    "exclusions": [
        "Airfare/train fare", "Ski/snowboard equipment and lessons",
        "Gondola Phase 2 ticket (subject to weather closures)",
        "Winter clothing rental, GST and anything not listed under inclusions",
    ],
    "faqs": [
        ("Does it always snow in Gulmarg in December?", "Snowfall in early December varies year to year — the heaviest, most reliable snow is usually late December through February. We'll advise honestly on current conditions when you enquire."),
        ("Is the road to Gulmarg safe in winter?", "Yes, the Tangmarg–Gulmarg road is regularly cleared by the authorities. Our drivers carry snow chains and we adjust timings around road advisories."),
    ],
},
{
    "slug": "jammu-kashmir-grand-tour-vaishno-devi-8n-9d",
    "title": "Jammu & Kashmir Grand Tour with Vaishno Devi",
    "duration": "8 Nights / 9 Days",
    "route": "Jammu – Katra (Vaishno Devi) – Srinagar – Gulmarg – Pahalgam – Sonmarg",
    "category": "Pilgrimage + Leisure",
    "price": 38499, "old_price": 42999,
    "hero": IMG["vaishno1"], "gallery": [IMG["vaishno2"], IMG["dal_sunset"], IMG["gulmarg_meadow"]],
    "meta_title": "Jammu and Kashmir Tour Package with Vaishno Devi | 8N/9D Grand Tour",
    "meta_desc": "Complete Jammu and Kashmir trip package combining Mata Vaishno Devi darshan at Katra with a full Kashmir valley circuit — Srinagar, Gulmarg, Pahalgam and Sonmarg. 8 nights 9 days.",
    "intro": "This is our most complete Jammu and Kashmir tour package — pairing the Mata Vaishno Devi pilgrimage at Katra with a full Kashmir valley holiday. It suits travellers who want both the spiritual significance of the shrine and the scenic circuit of Srinagar, Gulmarg, Pahalgam and Sonmarg in a single, well-sequenced trip.",
    "highlights": [
        "Mata Vaishno Devi darshan from Katra (trek or pony/palki at own cost)",
        "Full Kashmir circuit: Srinagar, Gulmarg, Pahalgam and Sonmarg",
        "Houseboat stay on Dal Lake with shikara ride",
        "Gulmarg Gondola Phase 1 ride",
        "Comfortable overnight halts, no same-day long-haul drives",
        "Single point of contact from Jammu arrival to Srinagar departure",
    ],
    "itinerary": [
        ("Day 1 — Arrival in Jammu, Transfer to Katra", "Pickup from Jammu Airport/Railway Station and drive to Katra, the base town for the Vaishno Devi shrine. Overnight in Katra."),
        ("Day 2 — Vaishno Devi Darshan", "Early trek (or optional pony/palki/helicopter at your own cost) to the shrine for darshan, returning to Katra by evening. Overnight in Katra."),
        ("Day 3 — Katra to Srinagar", "Scenic drive through the Jawahar Tunnel into the Kashmir Valley, arriving in Srinagar by evening. Houseboat check-in."),
        ("Day 4 — Srinagar Sightseeing", "Nishat Bagh, Shalimar Bagh, Chashme Shahi and a shikara ride on Dal Lake."),
        ("Day 5 — Srinagar to Gulmarg", "Day trip to Gulmarg for the Gondola ride and meadow walk, returning to Srinagar for the night."),
        ("Day 6 — Srinagar to Pahalgam", "Drive to Pahalgam via Pampore's saffron fields. Overnight in Pahalgam."),
        ("Day 7 — Pahalgam Valleys & Sonmarg", "Betaab and Aru Valley sightseeing, then a transfer toward Sonmarg for glacier views."),
        ("Day 8 — Return to Srinagar", "Free morning, last-minute shopping for Pashmina and saffron, and a farewell dinner."),
        ("Day 9 — Departure", "Transfer to Srinagar Airport."),
    ],
    "inclusions": [
        "8 nights accommodation (Katra hotel + Srinagar houseboat/hotel)",
        "Daily breakfast and dinner",
        "All ground transfers by private AC vehicle across Jammu and Kashmir",
        "Shikara ride and Gulmarg Gondola Phase 1",
    ],
    "exclusions": [
        "Airfare/train fare to Jammu and from Srinagar",
        "Vaishno Devi pony, palki or helicopter charges (paid directly)",
        "Lunches, personal expenses",
        "GST and anything not mentioned under inclusions",
    ],
    "faqs": [
        ("How difficult is the Vaishno Devi trek?", "The trek from Katra to the shrine is about 12–13 km on a well-paved path. It's a moderate climb — pony, palki (palanquin) and battery car options are available at your own cost for those who prefer not to walk the full distance."),
        ("How many days should be kept for Vaishno Devi alone?", "We recommend 2 full days in Katra — one for the ascent and darshan, one buffer for descent and rest, which this itinerary already includes."),
    ],
},
{
    "slug": "kashmir-ladakh-explorer-9n-10d",
    "title": "Kashmir with Ladakh Explorer",
    "duration": "9 Nights / 10 Days",
    "route": "Srinagar – Sonmarg – Kargil – Leh – Pangong – Gulmarg – Pahalgam",
    "category": "Adventure",
    "price": 49499, "old_price": 54999,
    "hero": IMG["pangong1"], "gallery": [IMG["leh1"], IMG["pangong3"], IMG["dal_wide"]],
    "meta_title": "Kashmir Ladakh Tour Package | Srinagar to Leh Trip | 9N/10D",
    "meta_desc": "Combined Kashmir and Ladakh tour package — Srinagar, Sonmarg, Kargil, Leh and Pangong Lake, plus Gulmarg and Pahalgam. A complete Jammu and Kashmir travel and tourism circuit for adventure travellers.",
    "intro": "For travellers who want both the green valleys of Kashmir and the high-altitude desert of Ladakh in one trip, this is our flagship long-format package. You cross the dramatic Zoji La pass overland from Sonmarg into Kargil, spend days acclimatising and exploring around Leh, drive out to the turquoise expanse of Pangong Lake, then loop back through Kashmir's Gulmarg and Pahalgam before flying out of Srinagar.",
    "highlights": [
        "Overland crossing via Zoji La from Kashmir into Ladakh",
        "2 nights at Pangong Tso, one of the world's highest saline lakes",
        "Leh local sightseeing with built-in acclimatisation day",
        "Gulmarg and Pahalgam covered on the return leg",
        "Srinagar houseboat stay with shikara ride",
        "Experienced high-altitude drivers and oxygen support on request",
    ],
    "itinerary": [
        ("Day 1 — Arrival in Srinagar", "Airport pickup, houseboat check-in, evening shikara ride."),
        ("Day 2 — Srinagar Sightseeing", "Mughal Gardens and Dal Lake, preparing for the Ladakh leg ahead."),
        ("Day 3 — Srinagar to Kargil via Sonmarg & Zoji La", "Long scenic drive over the Zoji La pass into Ladakh's high-altitude terrain, overnight in Kargil."),
        ("Day 4 — Kargil to Leh", "Drive through Lamayuru's moonland landscape and the confluence of the Indus and Zanskar rivers, arriving in Leh. Rest evening for acclimatisation."),
        ("Day 5 — Leh Acclimatisation & Local Sightseeing", "Easy day covering Shanti Stupa, Leh Palace and the main market at a gentle pace to help the body adjust to altitude."),
        ("Day 6 — Leh to Pangong Lake", "Drive via Chang La pass to Pangong Tso. Overnight by the lake in a camp or guesthouse."),
        ("Day 7 — Pangong to Leh", "Morning by the lake before the return drive to Leh."),
        ("Day 8 — Leh to Srinagar (fly or overland by arrangement)", "Return toward Kashmir, with an overnight halt planned around road conditions."),
        ("Day 9 — Gulmarg or Pahalgam Day Trip", "A final Kashmir valley day — Gulmarg Gondola or Pahalgam sightseeing, based on your arrival time."),
        ("Day 10 — Departure", "Transfer to Srinagar Airport."),
    ],
    "inclusions": [
        "9 nights accommodation across Srinagar, Kargil, Leh, Pangong and Gulmarg/Pahalgam",
        "Daily breakfast and dinner",
        "All ground transfers by private vehicle suited to high-altitude roads",
        "Inner Line Permit assistance for Pangong Lake",
        "Shikara ride and Gulmarg Gondola Phase 1",
    ],
    "exclusions": [
        "Airfare/train fare", "Oxygen cylinder or medical evacuation if required",
        "Lunches, personal expenses", "GST and anything not mentioned under inclusions",
    ],
    "faqs": [
        ("Is this trip physically demanding?", "The Ladakh leg involves high-altitude travel (Leh sits at about 3,500m). We build in a dedicated acclimatisation day and recommend travellers with heart or breathing conditions consult a doctor before booking."),
        ("What is the best season for this combined trip?", "June to September, when the Srinagar–Leh highway via Zoji La is fully open and Pangong Lake is accessible without snow closures."),
    ],
},
{
    "slug": "srinagar-houseboat-shikara-2n-3d",
    "title": "Kashmir Houseboat & Shikara Experience",
    "duration": "2 Nights / 3 Days",
    "route": "Srinagar Only",
    "category": "Quick Getaway",
    "price": 8999, "old_price": 9999,
    "hero": IMG["houseboat"], "gallery": [IMG["shikara"], IMG["dal_sunset"], IMG["nishat_bagh"]],
    "meta_title": "Srinagar Houseboat Package | Dal Lake Shikara Ride Booking | 2N/3D",
    "meta_desc": "Book a Srinagar houseboat stay with shikara ride on Dal Lake — a quick 2 nights 3 days Kashmir getaway, ideal as a standalone trip or add-on to another itinerary.",
    "intro": "Sometimes all you want is the Dal Lake experience itself — waking up to the sound of water against a wooden hull, floating markets at dawn, and a slow shikara ride at sunset. This compact package is built purely around that, and works equally well as a standalone weekend trip or as an add-on before/after another itinerary you're already booking with us or elsewhere.",
    "highlights": [
        "2 nights aboard a traditional Kashmiri houseboat",
        "Sunrise floating market shikara ride (optional, early start)",
        "Sunset shikara ride included",
        "Half-day Srinagar city and Mughal Garden tour",
        "Flexible add-on to any longer Kashmir itinerary",
    ],
    "itinerary": [
        ("Day 1 — Arrival & Houseboat Check-in", "Airport pickup, houseboat check-in, welcome tea, and an evening shikara ride on Dal Lake."),
        ("Day 2 — City & Gardens", "Half-day visit to Nishat Bagh and Shalimar Bagh, with the afternoon free to relax on the houseboat deck or explore the old city."),
        ("Day 3 — Departure", "Optional early-morning floating market shikara ride, then transfer to the airport."),
    ],
    "inclusions": [
        "2 nights houseboat accommodation, double sharing",
        "Daily breakfast", "Airport transfers", "2 shikara rides (sunset + optional sunrise)",
    ],
    "exclusions": [
        "Airfare/train fare", "Lunch and dinner", "Garden entry tickets",
        "GST and anything not mentioned under inclusions",
    ],
    "faqs": [
        ("Can this be combined with another package?", "Yes — many guests book this houseboat stay before or after a Gulmarg/Pahalgam itinerary, especially when arriving on an early flight and wanting to settle in gently."),
        ("Is there Wi-Fi and hot water on the houseboat?", "Most houseboats offer Wi-Fi and hot water; we confirm exact amenities of your specific houseboat at the time of booking so there are no surprises."),
    ],
},
{
    "slug": "best-of-kashmir-luxury-tour-6n-7d",
    "title": "Best of Kashmir Luxury Tour",
    "duration": "6 Nights / 7 Days",
    "route": "Srinagar – Gulmarg – Pahalgam – Sonmarg",
    "category": "Premium",
    "price": 43299, "old_price": 47999,
    "hero": IMG["shalimar_arch"], "gallery": [IMG["dal_sunset"], IMG["gulmarg_cable"], IMG["pahalgam_peaks"]],
    "meta_title": "Best Kashmir Tour Packages | Luxury Kashmir Trip 6N/7D | Plan My Trip Kashmir",
    "meta_desc": "Our premium, best-rated Kashmir tour package with 5-star houseboats, boutique hotels and a private guide across Srinagar, Gulmarg, Pahalgam and Sonmarg. Best tour packages for Kashmir, upgraded.",
    "intro": "This is our top-tier itinerary for travellers who want the full Kashmir circuit without compromising on comfort — deluxe/luxury-category houseboats, boutique hotels in Gulmarg and Pahalgam, a private guide for the Srinagar gardens, and a slower, more curated pace than our standard packages.",
    "highlights": [
        "Deluxe/luxury houseboat category with premium interiors",
        "Boutique 4-star hotel category in Gulmarg and Pahalgam",
        "Private licensed guide for Srinagar's Mughal Gardens",
        "Early-access Gulmarg Gondola slot to avoid queues",
        "Curated dining recommendations, including Wazwan multi-course dinner",
        "Priority airport meet-and-greet",
    ],
    "itinerary": [
        ("Day 1 — Arrival & Luxury Houseboat", "Priority airport pickup and check-in to a deluxe-category houseboat, followed by a private sunset shikara ride."),
        ("Day 2 — Srinagar with a Private Guide", "A private guide walks you through Nishat Bagh, Shalimar Bagh and Chashme Shahi with historical context on the Mughal era."),
        ("Day 3 — Gulmarg (Early Access)", "An early departure secures an early Gondola slot, avoiding the mid-day queues, followed by a boutique hotel check-in for the night."),
        ("Day 4 — Gulmarg to Pahalgam", "Scenic transfer to Pahalgam, checking into a boutique riverside property."),
        ("Day 5 — Pahalgam Valleys", "Private cab to Betaab and Aru Valley, with a riverside picnic lunch arranged on request."),
        ("Day 6 — Sonmarg & Return to Srinagar", "Morning at Sonmarg, then back to Srinagar for a Wazwan multi-course dinner experience on your final night."),
        ("Day 7 — Departure", "Priority transfer to Srinagar Airport."),
    ],
    "inclusions": [
        "6 nights in deluxe/luxury houseboat + boutique 4-star hotels",
        "Daily breakfast and dinner, including one Wazwan dinner experience",
        "Private guide for Srinagar sightseeing",
        "Private AC vehicle throughout, early Gondola access",
        "Priority airport meet-and-greet",
    ],
    "exclusions": [
        "Airfare/train fare", "Gondola Phase 2 ticket",
        "Alcoholic beverages, spa services", "GST and anything not mentioned under inclusions",
    ],
    "faqs": [
        ("What makes this different from your standard package?", "Higher accommodation category, a private licensed guide, priority gondola access, and a curated dining experience — the itinerary covers the same destinations as our Paradise Getaway package but at a noticeably more comfortable pace and quality level."),
        ("Can I upgrade an existing booking to this luxury tier?", "Yes, tell us your travel dates and we'll requote the price difference to upgrade hotel and houseboat categories."),
    ],
},
]

PACKAGES_SHORT_FOR_FOOTER = PACKAGES[:5]


DESTINATIONS = [
{
    "slug": "srinagar",
    "title": "Srinagar",
    "tagline": "Dal Lake, Houseboats & the Mughal Gardens",
    "hero": IMG["dal_sunset"],
    "gallery": [IMG["nishat_bagh"], IMG["shikara"], IMG["shalimar_arch"]],
    "meta_title": "Srinagar Tourism | Places to Visit, Houseboat Booking & Sightseeing Guide",
    "meta_desc": "Complete Srinagar travel guide — Dal Lake houseboats, Mughal Gardens, shikara rides and sightseeing itinerary. Book your Srinagar holiday package with Plan My Trip Kashmir.",
    "body": [
        "Srinagar is the summer capital of Jammu & Kashmir and the starting point for almost every Kashmir tour package. The city is built around Dal Lake, where rows of ornately carved houseboats sit moored beside floating vegetable gardens, and shikaras — the flat, cushioned gondolas of Kashmir — glide between them from before sunrise until after dark.",
        "Beyond the lake, Srinagar holds four Mughal-era gardens worth a full day on their own: Nishat Bagh and Shalimar Bagh on Dal Lake's eastern shore, and Chashme Shahi and Pari Mahal on the slopes above. Each was laid out on the classic charbagh plan — terraced lawns, a central water channel, and chinar trees planted centuries ago that now tower over the paths.",
        "The old city, on the western bank of the Jhelum River, is a different Srinagar entirely — wooden latticed houses, the 14th-century Jamia Masjid with its 370 deodar pillars, and narrow lanes where papier-mâché and Pashmina workshops still operate as they have for generations.",
    ],
    "attractions": [
        ("Dal Lake & Houseboats", "Stay a night on a traditional houseboat and explore the lake's floating gardens and market by shikara."),
        ("Nishat Bagh", "The largest of Srinagar's Mughal gardens, built in 1633 on the eastern shore of Dal Lake."),
        ("Shalimar Bagh", "Built by Emperor Jahangir in 1619, considered the high point of Mughal garden design in Kashmir."),
        ("Shankaracharya Temple", "A hilltop temple offering the best panoramic view of the city and lake."),
        ("Old City & Jamia Masjid", "Wooden architecture, historic mosques and the traditional handicraft markets."),
        ("Hazratbal Shrine", "A revered shrine on Dal Lake's northern shore, striking in white marble."),
    ],
    "best_time": "March to October for gardens and mild weather; December to February for a quieter, snow-dusted city.",
    "how_to_reach": "Srinagar International Airport connects to Delhi, Mumbai, Bengaluru, Chandigarh and other major Indian cities year-round. Srinagar is also the standard start and end point for road itineraries covering Gulmarg, Pahalgam and Sonmarg.",
    "related_packages": ["kashmir-paradise-getaway-5n-6d", "srinagar-short-break-3n-4d", "srinagar-houseboat-shikara-2n-3d"],
},
{
    "slug": "gulmarg",
    "title": "Gulmarg",
    "tagline": "Meadow of Flowers & Asia's Highest Gondola",
    "hero": IMG["gulmarg_cable"],
    "gallery": [IMG["gulmarg_gondola"], IMG["gulmarg_meadow"], IMG["gulmarg_station"]],
    "meta_title": "Gulmarg Tourism Guide | Gondola, Skiing & Best Time to Visit",
    "meta_desc": "Gulmarg travel guide — the Gulmarg Gondola cable car, skiing season, meadow walks and how to plan your Gulmarg day trip from Srinagar.",
    "body": [
        "Gulmarg — literally 'meadow of flowers' — sits at around 2,650m in the Pir Panjal range, about 50km from Srinagar. In summer it's a rolling green meadow ringed by pine forest and used as a golf course at one of the highest golf greens in the world; in winter it transforms into one of Asia's premier ski destinations.",
        "The Gulmarg Gondola is the main draw for most visitors — a two-stage cable car that climbs from Gulmarg to Kongdoori (Phase 1) and on to Apharwat Peak at roughly 3,980m (Phase 2, subject to weather). The views from the top, across snow-covered ridgelines toward the Line of Control, are some of the most dramatic in the Kashmir Valley.",
        "Most Kashmir tour packages treat Gulmarg as a day trip from Srinagar, though winter travellers — especially skiers — often prefer to stay 1–2 nights to make the most of the slopes and avoid a long return drive after a cold day on the mountain.",
    ],
    "attractions": [
        ("Gulmarg Gondola", "A two-phase cable car to Kongdoori and Apharwat Peak, among the highest in the world."),
        ("Gulmarg Golf Course", "One of the highest green golf courses globally, playable in the summer season."),
        ("Skiing & Snowboarding", "December to February brings reliable snow and a functioning ski school for beginners."),
        ("St. Mary's Church", "A small colonial-era church set among the pines."),
        ("Alpather Lake", "A high-altitude glacial lake, reachable by trek in the summer months."),
    ],
    "best_time": "April to June for meadows and mild weather; December to February for snow, skiing and gondola views over snow-covered peaks.",
    "how_to_reach": "About 50km / 1.5 hours by road from Srinagar via Tangmarg. All our packages include this transfer by private AC vehicle.",
    "related_packages": ["kashmir-paradise-getaway-5n-6d", "gulmarg-snow-special-5n-6d", "best-of-kashmir-luxury-tour-6n-7d"],
},
{
    "slug": "pahalgam",
    "title": "Pahalgam",
    "tagline": "Valley of Shepherds — Betaab, Aru & the Lidder River",
    "hero": IMG["betaab1"],
    "gallery": [IMG["aru_valley"], IMG["pahalgam_valley"], IMG["betaab2"]],
    "meta_title": "Pahalgam Tourism Guide | Betaab Valley, Aru Valley & Sightseeing",
    "meta_desc": "Pahalgam travel guide covering Betaab Valley, Aru Valley, Chandanwari and the Lidder River — everything you need for your Pahalgam sightseeing day.",
    "body": [
        "Pahalgam, meaning 'Valley of Shepherds', sits at the confluence of the Lidder River's east and west branches, about 90km from Srinagar. It's greener and gentler than Gulmarg's alpine terrain — pine and deodar forest, riverside meadows, and a handful of side valleys that have made it a favourite filming location for decades.",
        "Betaab Valley, renamed after the 1983 Bollywood film shot here, and Aru Valley, a quieter meadow used as a base camp for treks further into the mountains, are the two most-visited stops. Both are a short local-taxi ride from Pahalgam's main market, and both are included in every Pahalgam sightseeing plan we run.",
        "Pahalgam is also the traditional base camp for the Amarnath Yatra pilgrimage in July–August, when the town's infrastructure shifts to support pilgrims heading to the cave shrine. Outside yatra season, it's simply one of Kashmir's most relaxed valley towns.",
    ],
    "attractions": [
        ("Betaab Valley", "A lush meadow flanked by pine forest, 15km from Pahalgam market."),
        ("Aru Valley", "A quieter meadow and trekking base camp, known for alpine flowers in season."),
        ("Chandanwari", "The starting point of the Amarnath Yatra trek route, also a popular sledging spot in winter."),
        ("Lidder River", "A trout-filled mountain river running through the town, popular for riverside walks."),
        ("Baisaran Valley", "A meadow reachable by pony ride, sometimes called 'Mini Switzerland'."),
    ],
    "best_time": "March to June for wildflowers and mild weather; September to November for autumn colours and fewer crowds.",
    "how_to_reach": "About 90km / 2.5–3 hours by road from Srinagar, usually combined with a stop at the Pampore saffron fields en route.",
    "related_packages": ["kashmir-paradise-getaway-5n-6d", "kashmir-honeymoon-bliss-6n-7d", "kashmir-family-wonders-6n-7d"],
},
{
    "slug": "sonmarg-and-offbeat-kashmir",
    "title": "Sonmarg & Offbeat Kashmir",
    "tagline": "Thajiwas Glacier, Doodhpathri and Yusmarg",
    "hero": IMG["pahalgam_peaks"],
    "gallery": [IMG["dal_wide"], IMG["pahalgam_autumn"], IMG["gulmarg_meadow"]],
    "meta_title": "Sonmarg Travel Guide | Thajiwas Glacier & Offbeat Kashmir Destinations",
    "meta_desc": "Sonmarg and offbeat Kashmir guide — Thajiwas Glacier, Doodhpathri and Yusmarg meadows. Ideal add-ons to any Kashmir trip package for travellers who want to go beyond the usual circuit.",
    "body": [
        "Sonmarg — the 'meadow of gold' — sits at around 2,800m on the route toward Ladakh via Zoji La, roughly 80km from Srinagar. It's the last major stop before the high Himalaya proper, with the Sindh River running alongside the road and the Thajiwas Glacier a short pony ride or walk from the main viewpoint.",
        "Beyond the standard Srinagar–Gulmarg–Pahalgam circuit, Kashmir has a set of quieter meadows that most first-time visitors never see. Doodhpathri ('valley of milk'), about 42km from Srinagar, is a wide, flat meadow crossed by a small stream, popular for picnics and largely free of the crowds found at Gulmarg. Yusmarg, similarly close, is a forested meadow with a small trek up to Nilagrad's glacial stream.",
        "We build these into custom itineraries on request — they're not part of our standard packages by default, but travellers who've already done Kashmir once, or who simply want fewer crowds, often ask us to swap a day for Doodhpathri or Yusmarg instead.",
    ],
    "attractions": [
        ("Thajiwas Glacier", "A glacier viewpoint near Sonmarg, reachable by a short walk or pony ride."),
        ("Zoji La Pass", "The high mountain pass connecting Kashmir to Ladakh, usually open June–October."),
        ("Doodhpathri", "A quiet, less-visited meadow about 42km from Srinagar, ideal for a peaceful day trip."),
        ("Yusmarg", "A forested meadow with the Doodh Ganga stream and views of the Pir Panjal range."),
    ],
    "best_time": "May to September, when the Zoji La road is open and the meadows are green.",
    "how_to_reach": "Sonmarg is about 80km / 2.5 hours from Srinagar; Doodhpathri and Yusmarg are each roughly 40–45km and make easy half-day trips.",
    "related_packages": ["kashmir-paradise-getaway-5n-6d", "kashmir-honeymoon-bliss-6n-7d", "kashmir-ladakh-explorer-9n-10d"],
},
{
    "slug": "leh-ladakh",
    "title": "Leh-Ladakh",
    "tagline": "High-Altitude Desert & Pangong Lake",
    "hero": IMG["pangong2"],
    "gallery": [IMG["leh1"], IMG["leh2"], IMG["pangong3"]],
    "meta_title": "Leh Ladakh Tour Guide | Pangong Lake, Best Time & How to Reach from Kashmir",
    "meta_desc": "Leh-Ladakh travel guide for travellers combining it with a Kashmir trip — Pangong Lake, Leh sightseeing, acclimatisation tips and the overland route via Zoji La.",
    "body": [
        "Ladakh sits on the far side of the Zoji La pass from Kashmir — a high-altitude desert of bare mountains, Buddhist monasteries and turquoise lakes that feels like a different country from the green valley below. Leh, the main town, sits at roughly 3,500m, which means every itinerary here needs to account for acclimatisation before any serious sightseeing.",
        "Pangong Tso, made famous by Bollywood, is the highlight for most travellers — a 134km-long saline lake that changes colour through the day, with roughly 60% of it lying across the border in Chinese-administered territory. It's reached via the Chang La pass, one of the world's highest motorable roads.",
        "We only offer Ladakh as part of our combined Kashmir–Ladakh Explorer package, run overland via Sonmarg and the Zoji La pass — a genuinely spectacular drive, but one that's only feasible when the pass is open, typically June through early October.",
    ],
    "attractions": [
        ("Pangong Tso", "A vast, colour-shifting saline lake at over 4,200m, reached via Chang La pass."),
        ("Leh Palace", "A 17th-century royal palace overlooking Leh town, modelled on Lhasa's Potala Palace."),
        ("Shanti Stupa", "A white-domed Buddhist stupa with panoramic views over Leh."),
        ("Lamayuru Monastery", "One of Ladakh's oldest monasteries, set amid a striking 'moonland' landscape."),
    ],
    "best_time": "June to September, when the Srinagar–Leh highway via Zoji La is open and temperatures are manageable.",
    "how_to_reach": "Overland from Srinagar via Sonmarg and Zoji La (as part of our Kashmir with Ladakh Explorer package), or by direct flight into Leh Airport from Delhi.",
    "related_packages": ["kashmir-ladakh-explorer-9n-10d"],
},
]

DESTINATIONS_SHORT_FOR_FOOTER = DESTINATIONS[:5]


BLOG_POSTS = [
{
    "slug": "best-time-to-visit-kashmir-month-by-month-guide",
    "title": "Best Time to Visit Kashmir: A Month-by-Month Guide",
    "date": "2026-01-15", "read": "7 min read", "category": "Planning",
    "hero": IMG["nishat_bagh"],
    "meta_title": "Best Time to Visit Kashmir 2026 | Month-by-Month Weather Guide",
    "meta_desc": "When is the best time to visit Kashmir? A month-by-month breakdown of weather, crowd levels and what to pack, covering spring tulips, summer meadows, autumn chinars and winter snowfall.",
    "excerpt": "Kashmir changes character every few weeks — here's exactly what to expect if you're travelling in March versus July versus December, and how to pick the right month for your trip.",
    "body": """
<p>Kashmir doesn't really have an "off season" — it has four distinct ones, and each rewards a different kind of traveller. The trick is matching the month to what you actually want to see, because a Kashmir trip package booked for tulip season looks nothing like one booked for ski season.</p>

<h2>March to May — Spring</h2>
<p>Snow starts melting off the lower meadows, the Mughal Gardens fill with fresh blossoms, and by late March the Indira Gandhi Memorial Tulip Garden in Srinagar opens with over a million tulips across its terraces. Days are mild (12–22°C in Srinagar), nights are still cool, and Gulmarg's higher slopes can hold snow into April. This is a strong choice if you want gardens and greenery without peak-summer crowds.</p>

<h2>June to August — Summer</h2>
<p>This is peak season for a reason: every destination is fully accessible, Sonmarg and the road to Ladakh via Zoji La are open, and daytime temperatures in Srinagar hover comfortably around 25°C while Gulmarg and Pahalgam stay noticeably cooler. It's also the busiest and most expensive window, so book your houseboat and hotel category well in advance if you're travelling in July.</p>

<h2>September to November — Autumn</h2>
<p>Our personal favourite for photography. Chinar trees across Srinagar and Nishat Bagh turn deep red and gold, crowds thin out considerably after early October, and the light in the afternoons is soft and golden. Temperatures drop steadily through November, so pack layers if you're travelling toward the end of the season.</p>

<h2>December to February — Winter</h2>
<p>Kashmir in December is a genuinely different trip: snowfall usually begins in the second half of the month, Gulmarg becomes a full ski destination, and Dal Lake occasionally freezes at its edges. Houseboats run heating, and city sightseeing slows down, but if snow is the goal, late December through February is the most reliable window — see our dedicated <a href="thajiwas-glacier-sonmarg-kashmir-winter-travel-tips.html">Kashmir in Winter guide</a> for specifics.</p>

<h2>Our Quick Recommendation</h2>
<ul>
<li><strong>First-time visitors:</strong> April–June or September–October for the best balance of weather and crowd levels.</li>
<li><strong>Snow and skiing:</strong> Late December through February, focused on Gulmarg.</li>
<li><strong>Photography and gardens:</strong> Early April (tulips) or late October (chinars).</li>
<li><strong>Budget-conscious travellers:</strong> Shoulder months like March or November often have lower package rates.</li>
</ul>
<p>Whichever month you choose, our team adjusts every itinerary to the season — ask us for a season-specific quote when you enquire about any of our <a href="../packages/index.html">Kashmir tour packages</a>.</p>
""",
},
{
    "slug": "kashmir-itinerary-perfect-6-day-plan-first-timers",
    "title": "Kashmir Itinerary: The Perfect 6-Day Plan for First-Timers",
    "date": "2026-01-22", "read": "8 min read", "category": "Itinerary",
    "hero": IMG["dal_sunset"],
    "meta_title": "Kashmir 6 Day Itinerary for First-Timers | Complete Day-by-Day Plan",
    "meta_desc": "A detailed 6-day Kashmir itinerary covering Srinagar, Gulmarg, Pahalgam and Sonmarg — exactly how to sequence your trip, how long to spend in each place, and what to skip if you're short on time.",
    "excerpt": "If you only have six days for Kashmir, here's how we'd sequence Srinagar, Gulmarg, Pahalgam and Sonmarg to avoid backtracking and wasted travel time.",
    "body": """
<p>The single biggest planning mistake we see in DIY Kashmir itineraries is poor sequencing — bouncing between Srinagar and the outer valleys more times than necessary. Here's the route we run as our own <a href="../packages/kashmir-paradise-getaway-5n-6d.html">Kashmir Paradise Getaway package</a>, and why it's laid out this way.</p>

<h2>Day 1: Land in Srinagar, Settle into a Houseboat</h2>
<p>Keep arrival day light. Airports and flights are tiring, and Dal Lake at sunset is a gentle way to start. Skip sightseeing on day one if you can.</p>

<h2>Day 2: Srinagar City & Mughal Gardens</h2>
<p>Nishat Bagh, Shalimar Bagh and Chashme Shahi in a single day, finishing with a proper shikara ride through the lake's quieter channels rather than just the tourist stretch.</p>

<h2>Day 3: Gulmarg Day Trip</h2>
<p>Base yourself back in Srinagar and do Gulmarg as a day trip rather than an overnight, unless you're visiting in ski season — the drive is only about 90 minutes each way, and it avoids hauling luggage twice.</p>

<h2>Day 4: Move to Pahalgam</h2>
<p>This is your one genuine relocation day. Break the drive at Pampore's saffron fields (best mid-October to mid-November if you want to see it in bloom) and the Awantipora ruins.</p>

<h2>Day 5: Pahalgam Valleys</h2>
<p>Betaab Valley and Aru Valley by local taxi — both are close to town, so this is a relatively relaxed day compared to the rest of the trip.</p>

<h2>Day 6: Sonmarg & Departure Prep</h2>
<p>A half-day Sonmarg excursion works well on the way back toward Srinagar for your flight out, or as a final activity before an evening departure.</p>

<h2>What We'd Cut if You Only Had 4 Days</h2>
<p>Drop Sonmarg first, then consider making Gulmarg a half-day rather than a full one. See our <a href="../packages/kashmir-express-4n-5d.html">Kashmir Express package</a> for exactly that compressed version.</p>

<h2>What We'd Add if You Had 8+ Days</h2>
<p>Vaishno Devi (if arriving via Jammu) or a Ladakh extension over Zoji La — both covered in our longer packages.</p>
""",
},
{
    "slug": "gulmarg-vs-pahalgam-which-to-visit-first",
    "title": "Gulmarg vs Pahalgam: Which Should You Visit First?",
    "date": "2026-01-29", "read": "6 min read", "category": "Destinations",
    "hero": IMG["gulmarg_gondola"],
    "meta_title": "Gulmarg vs Pahalgam Comparison | Which to Visit First in Kashmir",
    "meta_desc": "Gulmarg or Pahalgam first? A practical comparison of terrain, activities, distance from Srinagar and which suits your travel style, so you can sequence your Kashmir trip correctly.",
    "excerpt": "Both are must-visit, but they're genuinely different landscapes — here's how to decide which one to see first, or whether you need both.",
    "body": """
<p>New visitors often ask us to pick one over the other, assuming they're interchangeable. They're not — Gulmarg is alpine and dramatic, built around the Gondola and its high-altitude views; Pahalgam is gentler, greener, and built around river valleys and meadows. Most of our packages include both, but here's how to think about sequencing them.</p>

<h2>Terrain and Scenery</h2>
<p>Gulmarg sits higher (around 2,650m) with sharper mountain views and, in winter, serious snow. Pahalgam (around 2,130m) is softer — pine forest, the Lidder River, and side valleys like Betaab and Aru that feel more like meadowland than high mountain.</p>

<h2>Best Activity in Each</h2>
<table class="plain">
<tr><th>Gulmarg</th><th>Pahalgam</th></tr>
<tr><td>Gondola cable car to Kongdoori/Apharwat</td><td>Betaab Valley &amp; Aru Valley sightseeing</td></tr>
<tr><td>Skiing and snowboarding (winter)</td><td>Riverside walks along the Lidder</td></tr>
<tr><td>Golf (summer, one of the world's highest courses)</td><td>Base camp for Amarnath Yatra (July–August)</td></tr>
</table>

<h2>Distance from Srinagar</h2>
<p>Gulmarg is closer — about 50km (1.5 hours). Pahalgam is roughly 90km (2.5–3 hours), usually combined with a stop at the Pampore saffron fields.</p>

<h2>So Which First?</h2>
<p>If your itinerary runs Srinagar → Gulmarg (day trip, return to Srinagar) → Pahalgam (overnight relocation), you avoid doubling back on the same road — which is exactly how our <a href="../packages/kashmir-paradise-getaway-5n-6d.html">standard 5N/6D package</a> is sequenced. Doing Pahalgam first and Gulmarg last means an extra return drive to Srinagar either way, so Gulmarg-then-Pahalgam is the more efficient order for most itineraries.</p>

<h2>Can You Skip One?</h2>
<p>If you truly only have time for one: choose Gulmarg for dramatic mountain views and (in winter) snow activities; choose Pahalgam if you prefer gentler walks, rivers and quieter valleys. Most travellers, though, tell us they're glad they saw both — they don't overlap as much as photos suggest.</p>
""",
},
{
    "slug": "srinagar-to-gulmarg-distance-route-travel-tips",
    "title": "Srinagar to Gulmarg: Distance, Route & Travel Tips",
    "date": "2026-02-03", "read": "5 min read", "category": "Travel Tips",
    "hero": IMG["gulmarg_meadow"],
    "meta_title": "Srinagar to Gulmarg Distance & Route | Travel Time, Road Conditions",
    "meta_desc": "How far is Gulmarg from Srinagar and how long does the drive take? Route, road conditions by season and practical tips for your Srinagar to Gulmarg day trip.",
    "excerpt": "Everything you need to know about the Srinagar-Gulmarg road — distance, drive time, seasonal conditions and what to pack for the day.",
    "body": """
<p>This is one of the most common practical questions we get from travellers planning their own route, so here's a straight answer with the detail behind it.</p>

<h2>Distance and Drive Time</h2>
<p>Gulmarg is approximately 50–52 km from central Srinagar, via Tangmarg. In good conditions the drive takes about 1.5 hours each way; allow closer to 2 hours in winter when the final stretch can be slower due to snow and traffic at the Tangmarg checkpoint, where vehicles sometimes need to switch to chain-fitted taxis for the final climb.</p>

<h2>The Route</h2>
<p>From Srinagar, the road runs through Magam and Tangmarg before climbing into Gulmarg itself. It's a well-maintained road, gradually gaining altitude with pine forest closing in on both sides in the last stretch before Gulmarg.</p>

<h2>Seasonal Road Conditions</h2>
<ul>
<li><strong>Summer (Apr–Oct):</strong> Fully open, no restrictions, comfortable drive.</li>
<li><strong>Winter (Dec–Feb):</strong> The final approach to Gulmarg can require snow chains after heavy snowfall; local authorities clear the road regularly but timings can shift after fresh snow.</li>
</ul>

<h2>Practical Tips</h2>
<ul>
<li>Start early (by 8–9am) if doing Gulmarg as a day trip, to get a good Gondola slot before midday queues build up.</li>
<li>Carry warm layers year-round — even in summer, temperatures at Kongdoori and Apharwat are noticeably colder than Srinagar.</li>
<li>Book Gondola tickets through your tour operator where possible; counter queues in peak season (May–June, Dec–Jan) can run long.</li>
<li>If you're travelling in winter specifically for snow, consider an overnight stay in Gulmarg rather than a rushed day trip — see our <a href="../packages/gulmarg-snow-special-5n-6d.html">Gulmarg Snow Special package</a>.</li>
</ul>
<p>All of our Kashmir packages include this transfer in a private AC vehicle with an experienced local driver, so road conditions and Gondola timing are handled for you.</p>
""",
},
{
    "slug": "kashmir-honeymoon-package-guide-best-places-couples",
    "title": "Kashmir Honeymoon Package Guide: Best Places for Couples",
    "date": "2026-02-10", "read": "7 min read", "category": "Honeymoon",
    "hero": IMG["shalimar_pav"],
    "meta_title": "Kashmir Honeymoon Guide | Best Places & Packages for Couples",
    "meta_desc": "Planning a Kashmir honeymoon? A guide to the most romantic spots — houseboats, Mughal gardens, Gulmarg and Pahalgam — plus what to look for in a couples-friendly package.",
    "excerpt": "From candlelight houseboat dinners to quiet valley viewpoints, here's how to plan a Kashmir honeymoon that doesn't feel like a standard group tour.",
    "body": """
<p>Kashmir earns its "Paradise on Earth" reputation partly because Mughal emperors built entire gardens here as gestures of devotion — Shalimar Bagh was literally designed as a pleasure garden for Emperor Jahangir and Empress Nur Jahan. That romantic history, combined with genuinely striking scenery, makes it one of India's most popular honeymoon destinations.</p>

<h2>Where to Stay</h2>
<p>A deluxe or luxury-category houseboat on Dal Lake is the single most memorable part of any Kashmir honeymoon — private decks, carved wooden interiors, and a candlelight dinner arranged on the water. For Gulmarg and Pahalgam, look for boutique or valley-view hotel categories rather than standard rooms.</p>

<h2>The Most Romantic Experiences</h2>
<ul>
<li><strong>Private sunset shikara ride</strong> — book a private boat rather than a shared one, and time it for the hour before sunset when the light over the Zabarwan hills is at its best.</li>
<li><strong>Mughal Gardens at a slow pace</strong> — Nishat Bagh and Shalimar Bagh, ideally on a weekday morning before tour groups arrive.</li>
<li><strong>A quiet Pahalgam evening</strong> — the Lidder riverside is far less crowded in the evening than during the day's sightseeing rush.</li>
<li><strong>Gulmarg's meadow</strong> — even a short walk away from the main Gondola queue opens up quiet, photogenic space.</li>
</ul>

<h2>What to Look for in a Honeymoon Package</h2>
<p>Not every "honeymoon package" is actually paced for couples — many are standard group itineraries with a room decoration thrown in. Look for: couple-only room categories (not triple-sharing add-ons), a private (not shared) shikara ride, realistic daily pacing without early-morning rushes, and a tour operator who'll actually customise the day order around you.</p>

<h2>Our Recommendation</h2>
<p>Our <a href="../packages/kashmir-honeymoon-bliss-6n-7d.html">Kashmir Honeymoon Bliss package</a> (6N/7D) is built specifically around these points — two houseboat nights instead of one, a private sunset shikara ride, and couple-view rooms across Gulmarg and Pahalgam. It can be shortened or extended depending on your leave dates.</p>
""",
},
{
    "slug": "kashmir-tour-packages-for-family-planning-trip-kids-parents",
    "title": "Kashmir Tour Packages for Family: Planning a Trip with Kids and Parents",
    "date": "2026-02-17", "read": "6 min read", "category": "Family Travel",
    "hero": IMG["aru_valley"],
    "meta_title": "Kashmir Tour Packages for Family | Trip Planning with Kids & Elderly Parents",
    "meta_desc": "Planning a Kashmir family trip with children or elderly parents? Practical tips on pacing, accommodation, altitude and what to pack for a comfortable multi-generational holiday.",
    "excerpt": "Multi-generational Kashmir trips need a different pace than a solo or couple itinerary — here's what actually matters when you're travelling with kids and grandparents together.",
    "body": """
<p>Kashmir is genuinely one of the easier Himalayan destinations for family travel — Srinagar sits at a modest altitude (about 1,585m), so unlike Ladakh, there's no serious acclimatisation concern. Still, a family itinerary needs different choices than a couple's or solo trip.</p>

<h2>Pacing Matters More Than Sightseeing Count</h2>
<p>The instinct is to pack in every attraction; the better approach is to build in slack. We deliberately keep driving distances shorter per day in our <a href="../packages/kashmir-family-wonders-6n-7d.html">Family Wonders package</a> and avoid scheduling two long transfer days back to back.</p>

<h2>Accommodation Choices</h2>
<ul>
<li>Ask specifically for family or triple-sharing rooms — not all houseboats and hotels have them, so confirm before booking.</li>
<li>A ground-floor or lower-deck houseboat cabin is easier for young children and grandparents than upper decks.</li>
<li>Heating (winter) or good ventilation (summer) should be confirmed directly, especially for elderly travellers sensitive to temperature.</li>
</ul>

<h2>Activities That Work Well for Mixed Ages</h2>
<ul>
<li>Shikara rides — relaxed, seated, and enjoyable for every age group.</li>
<li>Mughal Gardens — flat paths, open lawns, plenty of shade and benches.</li>
<li>Gulmarg Gondola Phase 1 — a seated cable car ride with no walking required at the top viewing area.</li>
<li>Pahalgam riverside — easy, flat walking with pony rides available for children who want them.</li>
</ul>

<h2>What to Pack</h2>
<p>Layered clothing regardless of season (Kashmir's evening temperatures drop faster than most Indian cities), comfortable walking shoes, sunscreen even in winter (UV reflects off snow), and any regular medication for elderly travellers, since pharmacy access outside Srinagar city can be limited.</p>

<h2>A Note on Assistance</h2>
<p>If anyone in your group needs wheelchair assistance, tell your tour operator in advance — Gondola stations and some garden entrances can arrange this with notice, but not always on the spot.</p>
""",
},
{
    "slug": "houseboat-stay-dal-lake-everything-you-need-to-know",
    "title": "Houseboat Stay on Dal Lake: Everything You Need to Know",
    "date": "2026-02-24", "read": "7 min read", "category": "Accommodation",
    "hero": IMG["houseboat"],
    "meta_title": "Houseboat Stay Dal Lake Srinagar | Booking Guide, Categories & Tips",
    "meta_desc": "A complete guide to booking a houseboat on Dal Lake, Srinagar — categories, what's included, safety, and how to choose the right one for your Kashmir trip.",
    "excerpt": "Houseboats are the single most distinctive part of any Srinagar visit — here's what they actually are, what to expect, and how to book one that suits your trip.",
    "body": """
<p>A Kashmir houseboat is a fixed, permanently moored wooden vessel — not something you drive around the lake yourself. Most were built decades ago in traditional deodar-wood carving style, with a living room, dining area, and 1–4 bedrooms, each with an attached bathroom. A shikara ferries you to and from the shore, since houseboats don't dock directly at a road.</p>

<h2>Houseboat Categories</h2>
<ul>
<li><strong>Standard:</strong> Simple, clean rooms with the essentials — attached bathroom, running water, basic furnishing.</li>
<li><strong>Deluxe:</strong> Larger rooms, better interiors, often with a small private sitting area.</li>
<li><strong>Luxury:</strong> Ornately carved interiors, premium linens, and the largest common areas — the category we use in our <a href="../packages/best-of-kashmir-luxury-tour-6n-7d.html">Best of Kashmir Luxury Tour</a>.</li>
</ul>

<h2>What's Usually Included</h2>
<p>Breakfast and dinner are typically served on board as part of most packages (this is the MAP — Modified American Plan — arrangement common across Kashmir). Hot water, basic heating (in winter) and Wi-Fi are standard in most mid-range-and-above houseboats today, though it's worth confirming with your operator for the specific houseboat you're assigned.</p>

<h2>Is It Safe?</h2>
<p>Yes, when booked through a registered operator. We only work with houseboat owners registered with Jammu & Kashmir Tourism, meeting their safety and hygiene standards. If you're booking independently, ask to see the registration certificate before confirming.</p>

<h2>How Many Nights Should You Book?</h2>
<p>One night is enough to experience it; two nights (as in our honeymoon and luxury packages) lets you add a sunrise floating-market shikara ride without feeling rushed on your only morning there.</p>

<h2>Booking Tip</h2>
<p>Book well ahead for May–July and the December–January winter holiday window — the well-reviewed houseboats fill up fastest in peak season. Our <a href="../packages/srinagar-houseboat-shikara-2n-3d.html">Houseboat &amp; Shikara Experience package</a> is a good standalone option if this is the only part of Kashmir you want to prioritise.</p>
""",
},
{
    "slug": "top-10-places-to-visit-jammu-and-kashmir",
    "title": "Top 10 Places to Visit in Jammu and Kashmir",
    "date": "2026-03-03", "read": "9 min read", "category": "Destinations",
    "hero": IMG["vaishno1"],
    "meta_title": "Top 10 Places to Visit in Jammu and Kashmir | Complete Travel List",
    "meta_desc": "The 10 best places to visit across Jammu and Kashmir — from Dal Lake and Gulmarg to Vaishno Devi and Pangong Lake — with what makes each one worth the trip.",
    "excerpt": "A region-wide list covering both the Kashmir Valley and Jammu division, for travellers planning a longer Jammu and Kashmir tour package.",
    "body": """
<p>Jammu and Kashmir spans far more than just the Kashmir Valley — it stretches from the Shivalik foothills around Jammu, through the valley itself, up to the high-altitude terrain bordering Ladakh. Here's our list of the 10 places worth prioritising, roughly in the order most itineraries visit them.</p>

<h2>1. Dal Lake, Srinagar</h2>
<p>The houseboats, shikaras and floating gardens that define most people's mental image of Kashmir.</p>

<h2>2. Mughal Gardens, Srinagar</h2>
<p>Nishat Bagh and Shalimar Bagh in particular — centuries-old terraced gardens on Dal Lake's shore.</p>

<h2>3. Gulmarg</h2>
<p>The Gondola, the meadow, and (in winter) some of the best skiing in India.</p>

<h2>4. Pahalgam</h2>
<p>Betaab Valley, Aru Valley and the Lidder River — Kashmir's gentler, greener side.</p>

<h2>5. Sonmarg</h2>
<p>The last major stop before Ladakh, with the Thajiwas Glacier as its main draw.</p>

<h2>6. Pampore Saffron Fields</h2>
<p>Best visited mid-October to mid-November, when the fields bloom purple with saffron crocus.</p>

<h2>7. Vaishno Devi, Katra</h2>
<p>One of Hinduism's most visited pilgrimage sites, in the Jammu division rather than the valley itself. See our <a href="../packages/jammu-kashmir-grand-tour-vaishno-devi-8n-9d.html">Vaishno Devi + Kashmir package</a> for how to combine both.</p>

<h2>8. Patnitop</h2>
<p>A hill station on the Jammu–Srinagar highway, a popular overnight stop for road travellers.</p>

<h2>9. Leh, Ladakh</h2>
<p>Technically a separate union territory today, but still commonly combined with Kashmir itineraries via the Zoji La pass.</p>

<h2>10. Pangong Tso</h2>
<p>The turquoise, ultra-high-altitude lake near the China border, reached from Leh.</p>

<h2>Building Your Own Route</h2>
<p>Most first-time visitors focus on numbers 1–6 in a single Kashmir Valley circuit. Numbers 7–10 typically require additional days and are best added if you have 8+ days available — browse our <a href="../packages/index.html">full package list</a> for ready-made combinations of these.</p>
""",
},
{
    "slug": "kashmir-budget-trip-how-to-plan-affordable-holiday",
    "title": "Kashmir Budget Trip: How to Plan an Affordable Holiday Package",
    "date": "2026-03-10", "read": "6 min read", "category": "Budget Travel",
    "hero": IMG["dal_wide"],
    "meta_title": "Kashmir Budget Trip Guide | How to Plan an Affordable Kashmir Holiday",
    "meta_desc": "Practical tips for planning an affordable Kashmir trip — when to travel, how to choose packages, and where costs typically add up so you can budget accurately.",
    "excerpt": "Kashmir doesn't have to be an expensive trip — here's where the real costs sit and how to plan a package that fits a tighter budget without cutting the highlights.",
    "body": """
<p>Kashmir tour packages can range from roughly ₹15,000 to well over ₹50,000 per person depending on duration, season and hotel category. Here's how to think about that spread so you're not overpaying for things that don't matter to you.</p>

<h2>Where the Cost Actually Comes From</h2>
<ul>
<li><strong>Season:</strong> May–July and the December holiday window carry the highest hotel and houseboat rates. Shoulder months (March, April, September, November) are noticeably cheaper for the same itinerary.</li>
<li><strong>Duration:</strong> A shorter, tightly-planned trip (like our 4N/5D Kashmir Express) naturally costs less than a full 6–7 night circuit, without cutting the core highlights.</li>
<li><strong>Accommodation category:</strong> Standard houseboats and 3-star hotels versus deluxe/luxury categories can shift the total package price by 30–50%.</li>
<li><strong>Airfare:</strong> Usually the single largest line item and entirely separate from your ground package — book flights early for the biggest savings.</li>
</ul>

<h2>How to Cut Cost Without Cutting the Trip Short</h2>
<ul>
<li>Travel in a shoulder month rather than peak season.</li>
<li>Choose a group/fixed-departure itinerary over a fully private one if your dates are flexible.</li>
<li>Book a shorter, well-sequenced itinerary (like our <a href="../packages/kashmir-express-4n-5d.html">Kashmir Express package</a>) rather than a long trip with padded, low-value days.</li>
<li>Confirm exactly what's included (meals, transfers, entry tickets) before comparing prices across operators — a lower headline price sometimes hides a longer list of exclusions.</li>
</ul>

<h2>A Realistic Budget Breakdown (Per Person, Twin Sharing)</h2>
<table class="plain">
<tr><th>Trip Type</th><th>Typical Range</th></tr>
<tr><td>3N/4D Srinagar-only</td><td>₹14,000 – ₹18,000</td></tr>
<tr><td>4N/5D Compact circuit</td><td>₹17,000 – ₹22,000</td></tr>
<tr><td>5N/6D Full circuit</td><td>₹23,000 – ₹30,000</td></tr>
<tr><td>6N/7D Premium/luxury</td><td>₹35,000 – ₹48,000</td></tr>
</table>
<p>Our packages are priced to typically run below the standard market rate for the equivalent itinerary and hotel category — see our <a href="../packages/index.html">full package list</a> for current pricing, or message us directly for a same-day custom quote.</p>
""",
},
{
    "slug": "srinagar-sightseeing-complete-one-day-two-day-guide",
    "title": "Srinagar Sightseeing: A Complete One-Day and Two-Day Guide",
    "date": "2026-03-17", "read": "6 min read", "category": "Itinerary",
    "hero": IMG["shalimar_arch"],
    "meta_title": "Srinagar Sightseeing Guide | Best One Day & Two Day Itinerary",
    "meta_desc": "How to plan Srinagar sightseeing in one day or two — Dal Lake, Mughal Gardens, the old city and Shankaracharya Temple, sequenced for minimal backtracking.",
    "excerpt": "Whether you have one day or two in Srinagar, here's how to sequence the city's highlights so you don't waste time doubling back across town.",
    "body": """
<p>Srinagar is compact enough to cover meaningfully in a single day if you have to, but a second day lets you slow down at the gardens and add the old city — which most rushed itineraries skip entirely.</p>

<h2>If You Only Have One Day</h2>
<ol>
<li><strong>Morning:</strong> Nishat Bagh, then Shalimar Bagh (both on Dal Lake's eastern shore, close together).</li>
<li><strong>Midday:</strong> Chashme Shahi, a smaller garden en route back toward the lake.</li>
<li><strong>Afternoon:</strong> Shankaracharya Temple for a hilltop view over the whole city.</li>
<li><strong>Evening:</strong> A sunset shikara ride on Dal Lake — the best way to end any Srinagar day.</li>
</ol>

<h2>If You Have Two Days</h2>
<p><strong>Day 1</strong> — Follow the one-day plan above, but at a more relaxed pace, allowing 45–60 minutes at each garden instead of rushing through.</p>
<p><strong>Day 2</strong> — Dedicate the morning to the old city: Jamia Masjid, the wooden architecture along the Jhelum's banks, and the handicraft workshops where Pashmina shawls and papier-mâché items are still made by hand. Add the Indira Gandhi Memorial Tulip Garden if you're visiting between late March and late April. Spend the afternoon at leisure on your houseboat, or take an early-morning floating-market shikara ride the next day before departure.</p>

<h2>Practical Tips</h2>
<ul>
<li>Garden entry tickets are inexpensive and paid on the spot — no need to pre-book.</li>
<li>The Mughal Gardens are busiest between 11am and 2pm; visiting Nishat Bagh right after opening avoids the largest tour groups.</li>
<li>A private vehicle (included in all our packages) saves significant time versus relying on shared transport between garden stops, which aren't within easy walking distance of each other.</li>
</ul>
<p>Our <a href="../packages/srinagar-short-break-3n-4d.html">Srinagar City &amp; Gardens Short Break</a> is built around exactly this two-day structure, with a third day added for the old city and markets.</p>
""",
},
{
    "slug": "kashmir-in-winter-snowfall-skiing-december-travel-tips",
    "title": "Kashmir in Winter: Snowfall, Skiing and December Travel Tips",
    "date": "2026-03-24", "read": "7 min read", "category": "Winter Travel",
    "hero": IMG["gulmarg_station"],
    "meta_title": "Kashmir in December | Winter Travel Guide, Snowfall & Skiing Tips",
    "meta_desc": "Planning a Kashmir trip in December? A practical guide to snowfall timing, Gulmarg skiing, what to pack and how winter changes your itinerary.",
    "excerpt": "Kashmir in December looks nothing like Kashmir in June — here's what to actually expect from the weather, roads and activities before you book.",
    "body": """
<p>Winter is Kashmir's most misunderstood season among first-time enquirers — some assume it's inaccessible, others assume guaranteed snow from day one of December. Neither is quite right.</p>

<h2>When Does It Actually Snow?</h2>
<p>Early December is often still dry, with the first significant snowfall in Srinagar and Gulmarg typically arriving in the second half of the month. January and February are the most reliably snowy months across the valley, including in Gulmarg's lower meadows and occasionally along Srinagar's Boulevard road.</p>

<h2>What Changes About Your Itinerary</h2>
<ul>
<li><strong>Gulmarg becomes the centrepiece</strong> rather than a quick day trip — most winter travellers stay 1–2 nights to make the most of the Gondola and ski slopes.</li>
<li><strong>Sonmarg and the Zoji La road toward Ladakh close</strong> for winter, so this leg drops from any itinerary between roughly November and April/May.</li>
<li><strong>Garden visits shorten</strong> — the Mughal Gardens keep reduced hours and less bloom in winter, though the bare chinar trees and occasional snow dusting have their own quiet beauty.</li>
<li><strong>Houseboats run heating</strong>, and most well-maintained ones are comfortable even in freezing temperatures — but confirm this specifically when booking.</li>
</ul>

<h2>Skiing in Gulmarg</h2>
<p>Gulmarg is genuinely one of Asia's top ski destinations, with runs suited to both beginners and experienced skiers, plus heli-skiing operators for advanced riders. Ski and snowboard equipment rental, along with lessons, are available locally and are not included in standard tour packages — budget for these separately.</p>

<h2>What to Pack</h2>
<ul>
<li>Heavy thermal layers, a proper winter jacket, waterproof snow boots (rentable locally if needed)</li>
<li>Gloves, a warm cap and sunglasses (snow glare is intense on clear days)</li>
<li>Moisturiser and lip balm — the dry mountain air is harder on skin than most travellers expect</li>
</ul>
<p>Our <a href="../packages/gulmarg-snow-special-5n-6d.html">Gulmarg Snow Special package</a> is built specifically around the winter season, with extra nights in Gulmarg and heated accommodation throughout.</p>
""",
},
{
    "slug": "jammu-kashmir-ladakh-combined-trip-itinerary-planning",
    "title": "Jammu and Kashmir with Ladakh: Planning a Combined Trip Itinerary",
    "date": "2026-03-31", "read": "8 min read", "category": "Itinerary",
    "hero": IMG["pangong1"],
    "meta_title": "Kashmir and Ladakh Combined Itinerary | How to Plan the Full Trip",
    "meta_desc": "Thinking of combining Kashmir and Ladakh in one trip? A planning guide covering the overland route via Zoji La, acclimatisation, timing and a suggested day-by-day itinerary.",
    "excerpt": "Kashmir and Ladakh sit right next to each other on the map but feel like entirely different trips — here's how to combine them properly in a single itinerary.",
    "body": """
<p>Kashmir and Ladakh are often lumped together in search results, but they're genuinely different environments — Kashmir's green valley versus Ladakh's high-altitude desert — separated by the Zoji La pass. Combining them into one trip is absolutely doable, but it needs deliberate planning around altitude and road timing.</p>

<h2>Can You Actually Drive Between Them?</h2>
<p>Yes — the Srinagar–Kargil–Leh highway crosses the Zoji La pass, typically open from around late May/June through October, weather dependent. Outside that window, the overland route closes and Leh becomes accessible only by flight from Delhi.</p>

<h2>The Altitude Problem</h2>
<p>This is the part most self-planned itineraries get wrong. Leh sits at roughly 3,500m, and altitude sickness is a real risk if you arrive too fast without adjusting. A responsible itinerary builds in at least one full acclimatisation day in Leh before pushing on to Pangong Lake (over 4,200m) or other high passes.</p>

<h2>Suggested Sequencing</h2>
<ol>
<li><strong>Days 1–2:</strong> Srinagar (gentle start, low altitude, easy sightseeing).</li>
<li><strong>Day 3:</strong> Drive to Kargil via Sonmarg and Zoji La — a full, scenic driving day.</li>
<li><strong>Day 4:</strong> Kargil to Leh, passing Lamayuru's moonland landscape.</li>
<li><strong>Day 5:</strong> Acclimatisation day in Leh — easy local sightseeing only, no long drives or high passes.</li>
<li><strong>Days 6–7:</strong> Pangong Lake via Chang La pass, then return to Leh.</li>
<li><strong>Days 8–10:</strong> Return toward Kashmir, with a final Gulmarg or Pahalgam day before departure from Srinagar.</li>
</ol>

<h2>Practical Notes</h2>
<ul>
<li>Inner Line Permits are required for Pangong Lake — your tour operator should handle this on your behalf.</li>
<li>Carry cash — ATM access is limited once you're past Kargil.</li>
<li>Anyone with heart or respiratory conditions should consult a doctor before undertaking the Ladakh leg specifically.</li>
</ul>
<p>This exact structure is what we run as our <a href="../packages/kashmir-ladakh-explorer-9n-10d.html">Kashmir with Ladakh Explorer package</a> (9N/10D) — built with the acclimatisation day already factored in rather than left to chance.</p>
""",
},
]


FAQ_CATEGORIES = [
("Booking & Packages", [
    ("How do I book a Kashmir tour package with Plan My Trip Kashmir?", "Call or WhatsApp us at +91 70060 83281, or fill in the enquiry form on our Contact page with your travel dates and group size. We'll share a customised itinerary and price within a few hours, and confirm your booking once you're happy with the plan and pay the advance."),
    ("Are your prices cheaper than other Kashmir tour operators?", "We price our packages to typically run below the standard market rate for the same itinerary, hotel category and inclusions, since we're a locally based Srinagar operator without the overheads of larger national travel platforms. Compare our package pages against any quote you've received elsewhere and message us the details — we're happy to review it."),
    ("Can I customise a package instead of booking a fixed itinerary?", "Yes. Every package on our site is a starting template. We regularly adjust the number of nights per destination, upgrade or downgrade hotel categories, add Ladakh or Vaishno Devi, or swap in offbeat spots like Doodhpathri and Yusmarg — at no separate planning fee."),
    ("How much advance payment is required to confirm a booking?", "This depends on the season and package, but typically a partial advance confirms your dates and hotel/houseboat booking, with the balance payable before or on arrival. We'll share exact terms in your booking confirmation."),
    ("Do you offer group discounts for large parties?", "Yes, group bookings (typically 8+ travellers) are eligible for custom pricing. Share your group size and dates with us and we'll work out a group rate."),
    ("What is your cancellation and refund policy?", "Cancellation terms depend on how close to your travel date you cancel, since hotel and houseboat bookings carry their own supplier policies. Full details are in our Terms & Conditions page — we always share the specific policy for your booking in writing before you pay."),
]),
("Best Time & Weather", [
    ("What is the best time to visit Kashmir?", "It depends on what you want to see. April–June and September–October offer the most reliable weather for sightseeing; December–February is best for snow and skiing in Gulmarg. Read our full guide on the Best Time to Visit Kashmir on our blog."),
    ("Is Kashmir open for tourism in December?", "Yes, Kashmir is open year-round. December sees the start of the winter season, with heavier, more reliable snowfall typically arriving in the second half of the month. Sonmarg and the Ladakh route close for winter, but Srinagar, Gulmarg and Pahalgam remain fully accessible."),
    ("How cold does it get in Kashmir in winter?", "Srinagar typically ranges from -2°C to 8°C in January, while Gulmarg can drop several degrees colder, especially at night. Pack heavy thermal layers, a proper winter jacket and waterproof boots."),
    ("Can I see snow in Kashmir without visiting in peak winter?", "Gulmarg's higher slopes (accessible via the Gondola) can hold snow well into April in a good year, so it's possible to see snow even on a spring trip, though it's not guaranteed."),
]),
("Travel & Documents", [
    ("Do Indian citizens need any special permit to visit Kashmir?", "No special permit is required for Indian citizens to visit Srinagar, Gulmarg, Pahalgam or Sonmarg. If you extend your trip into Ladakh, an Inner Line Permit is required for certain areas including Pangong Lake, which we arrange on your behalf."),
    ("Do foreign nationals need a permit to visit Kashmir?", "Foreign nationals generally do not need a special permit for the main Kashmir Valley circuit, though requirements can change and some areas near the border may have restrictions. We recommend checking current requirements with us at the time of booking, as rules are updated by the authorities from time to time."),
    ("How do I reach Srinagar?", "Srinagar International Airport has daily direct flights from Delhi, Mumbai, Bengaluru, Chandigarh, Jammu and several other major Indian cities. Srinagar is also connected by road via the Jammu-Srinagar National Highway."),
    ("Is it safe to travel to Kashmir right now?", "Kashmir receives a large number of domestic and international tourists every year, and the main tourist circuit — Srinagar, Gulmarg, Pahalgam and Sonmarg — operates normally with a visible security presence. As with any destination, we recommend checking current travel advisories closer to your travel date, and our on-ground team stays in touch with you throughout your trip."),
    ("What ID proof do I need to carry?", "A valid government photo ID (Aadhaar, passport, driving licence or voter ID) is required for hotel and houseboat check-ins. Foreign nationals should carry their passport and any relevant visa documentation."),
]),
("Accommodation", [
    ("What is a houseboat stay like?", "A houseboat is a fixed, ornately carved wooden vessel permanently moored on Dal Lake or Nigeen Lake, with bedrooms, a dining area and attached bathrooms. A shikara ferries you between the houseboat and the shore. See our full houseboat guide on the blog for details."),
    ("Are the hotels and houseboats safe and hygienic?", "We work only with houseboats registered with Jammu & Kashmir Tourism and hotels that meet our own quality checks for cleanliness, safety and service. If you have a specific concern, tell us and we'll confirm details of your exact property before booking."),
    ("Can I request a specific hotel or houseboat category?", "Yes — let us know your preferred category (standard, deluxe or luxury) and we'll quote accordingly. Photos of the specific property can be shared on request before you confirm."),
    ("Do hotels provide hot water and heating in winter?", "Yes, all hotels and houseboats we work with provide hot water year-round, and heating (room heaters or centrally heated common areas) during the winter months."),
]),
("On the Ground", [
    ("Will I have a private vehicle for the whole trip?", "Yes, all our standard packages include a private AC vehicle (not a shared coach) with an experienced local driver for every transfer and sightseeing day."),
    ("Are meals included in the packages?", "Most packages include daily breakfast and dinner (locally known as the MAP plan). Lunch is usually excluded so you can explore local restaurants along the route, though it can be added on request."),
    ("Is Wi-Fi available during the trip?", "Most hotels and houseboats offer Wi-Fi, and mobile network coverage (postpaid SIMs work best; some prepaid SIMs from outside J&K face restrictions) is generally reliable in Srinagar, Gulmarg and Pahalgam."),
    ("What if the weather affects my itinerary (e.g. Gondola closure)?", "Our local team monitors weather and road conditions daily. If a specific activity like the Gulmarg Gondola Phase 2 is closed due to weather, we'll adjust your day's plan on the spot rather than leaving you stranded."),
    ("Can I extend my trip once I'm already in Kashmir?", "Yes, subject to hotel and vehicle availability — just speak to your trip coordinator, who stays reachable on WhatsApp throughout your stay."),
]),
]

TESTIMONIALS = [
    ("Rohit & Ananya Sharma", "Delhi", 5, "Kashmir Honeymoon Bliss Package", "The houseboat stay was the highlight of our trip — the candlelight dinner on the deck was exactly what we'd hoped for. Our coordinator was reachable the entire week and adjusted our Sonmarg day when it started raining."),
    ("Priya Menon", "Bengaluru", 5, "Kashmir Paradise Getaway", "First time in Kashmir and it did not disappoint. The Gulmarg Gondola views were unreal and the driver knew exactly where to stop for photos without us having to ask."),
    ("The Kapoor Family", "Mumbai", 5, "Kashmir Family Wonders", "Travelling with my parents and two kids made me nervous about pacing, but the itinerary was genuinely relaxed. No rushed mornings, and the houseboat had a lower-deck room that was easy for my dad to get in and out of."),
    ("Arjun Verma", "Chandigarh", 4, "Kashmir Express 4N/5D", "Great value for a short trip — we only had 5 days off work and still managed to see Srinagar, Gulmarg and Pahalgam properly. Would have liked a bit more time in Pahalgam but that's on us for picking the short package."),
    ("Sana Iqbal", "Hyderabad", 5, "Best of Kashmir Luxury Tour", "Worth the upgrade. The private guide at the Mughal Gardens added a lot of context we would have missed on our own, and the Wazwan dinner on the last night was a wonderful send-off."),
    ("Vikram & Neha", "Pune", 5, "Kashmir with Ladakh Explorer", "The Zoji La crossing was the trip of a lifetime. Our driver was calm and experienced on the mountain roads, and the acclimatisation day in Leh made a real difference — no altitude issues at all."),
    ("Deepak Nair", "Kochi", 4, "Jammu Kashmir Grand Tour with Vaishno Devi", "Combining the Vaishno Devi darshan with the Kashmir circuit worked really well logistically. The Jawahar Tunnel drive into the valley was stunning. Communication before booking could have been slightly faster, but everything on-ground was smooth."),
    ("Fatima Sheikh", "Ahmedabad", 5, "Srinagar Houseboat & Shikara Experience", "A perfect quick getaway. Two nights was just enough to properly enjoy the lake without needing a full week off work. The sunrise floating market ride was magical."),
    ("Karan Malhotra", "Jaipur", 5, "Gulmarg Snow Special", "Booked this specifically for the snow and it delivered — heavy snowfall on our second day in Gulmarg and the Gondola ride through it was unforgettable. Well organised winter clothing advice beforehand too."),
]


# Core pages: home, about, contact, gallery, faq, testimonials, 404, legal

def render_home():
    prefix = ""
    top_packages = PACKAGES[:6]
    pkg_cards = ""
    for p in top_packages:
        pkg_cards += f"""
        <div class="card reveal">
          <div class="card-img"><span class="tag">{p['category']}</span><img src="{p['hero']}" alt="{esc(p['title'])} Kashmir tour package" loading="lazy"></div>
          <div class="card-body">
            <h3><a href="packages/{p['slug']}.html">{p['title']}</a></h3>
            <p style="margin-bottom:0;font-size:.9rem;">{p['route']}</p>
            <div class="meta-row"><span>📅 {p['duration']}</span></div>
            <div class="price-row">
              <div class="price">₹{p['price']:,}<small> /person</small></div>
              <a href="packages/{p['slug']}.html" class="btn btn-outline" style="padding:9px 16px;font-size:.78rem;">View Details</a>
            </div>
          </div>
        </div>"""

    dest_cards = ""
    for d in DESTINATIONS:
        dest_cards += f"""
        <a href="destinations/{d['slug']}.html" class="card reveal" style="text-decoration:none;">
          <div class="card-img"><img src="{d['hero']}" alt="{esc(d['title'])} Kashmir" loading="lazy"></div>
          <div class="card-body"><h3 style="margin-bottom:4px;">{d['title']}</h3><p style="margin:0;font-size:.88rem;">{d['tagline']}</p></div>
        </a>"""

    blog_cards = ""
    for b in BLOG_POSTS[:3]:
        blog_cards += f"""
        <div class="card blog-card reveal">
          <div class="card-img"><img src="{b['hero']}" alt="{esc(b['title'])}" loading="lazy"></div>
          <div class="card-body">
            <div class="blog-meta">{b['category']} · {b['read']}</div>
            <h3><a href="blog/{b['slug']}.html">{b['title']}</a></h3>
            <p style="font-size:.9rem;">{b['excerpt'][:120]}…</p>
            <a href="blog/{b['slug']}.html" class="btn btn-outline" style="padding:8px 16px;font-size:.78rem;">Read More</a>
          </div>
        </div>"""

    testi_cards = ""
    for t in TESTIMONIALS[:3]:
        stars = "★" * t[2] + "☆" * (5 - t[2])
        testi_cards += f"""
        <div class="testi reveal"><p>{t[4]}</p>
          <div class="stars">{stars}</div>
          <div class="who">{t[0]} <span style="color:var(--ink-soft);font-weight:400;">— {t[1]}</span></div>
        </div>"""

    faq_preview = ""
    for q, a in FAQ_CATEGORIES[0][1][:5]:
        faq_preview += f"""
        <div class="faq-item"><div class="faq-q">{q}<span class="plus">+</span></div><div class="faq-a"><p>{a}</p></div></div>"""

    body = f"""
<section class="hero">
  <div class="hero-grid">
    <div class="reveal in">
      <span class="eyebrow">Srinagar-Based Tour &amp; Travel Company</span>
      <h1>Kashmir, Planned by People<br>Who Actually Live Here</h1>
      <p class="lead">Custom Kashmir tour packages — houseboats on Dal Lake, Gulmarg's slopes, Pahalgam's valleys and beyond — built and run by a local Srinagar team, priced to typically beat the standard market rate by up to 10%.</p>
      <div class="hero-actions">
        <a href="packages/index.html" class="btn btn-gold">Explore Packages</a>
        <a href="https://wa.me/{PHONE_WA}" class="btn btn-ghost-light">💬 Chat on WhatsApp</a>
      </div>
      <div class="hero-stats">
        <div><strong>10+</strong><span>Curated Kashmir Packages</span></div>
        <div><strong>100%</strong><span>Locally Based in Srinagar</span></div>
        <div><strong>24/7</strong><span>On-Trip WhatsApp Support</span></div>
      </div>
    </div>
    <div class="hero-media reveal in">
      <div class="arch-frame"><img src="{IMG['dal_sunset']}" alt="Houseboat on Dal Lake at sunset, Srinagar Kashmir"></div>
      <div class="badge"><strong>Up to 10% Less</strong>than standard market package rates, same itinerary quality.</div>
    </div>
  </div>
</section>

<div class="container"><div class="trust-bar">
  <div><strong>🏠 Registered</strong>&nbsp;Houseboats &amp; Hotels</div>
  <div><strong>🚗 Private</strong>&nbsp;AC Vehicles, No Shared Coaches</div>
  <div><strong>📍 Local</strong>&nbsp;Srinagar Ground Team</div>
  <div><strong>💬 Direct</strong>&nbsp;WhatsApp Trip Coordinator</div>
</div></div>

<section>
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Our Kashmir Tour Packages</span>
      <h2>Find Your Kashmir Trip Package</h2>
      <p>From a quick houseboat weekend to a full Kashmir–Ladakh circuit — every itinerary is built by a team that runs these routes year-round.</p>
    </div>
    <div class="grid grid-3">{pkg_cards}</div>
    <div style="text-align:center;margin-top:36px;"><a href="packages/index.html" class="btn btn-primary">View All Packages</a></div>
  </div>
</section>

<section class="band-ivory2">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Places We Cover</span>
      <h2>Kashmir's Essential Destinations</h2>
    </div>
    <div class="grid grid-3">{dest_cards}</div>
  </div>
</section>

<section class="band-teal">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Why Plan My Trip Kashmir</span>
      <h2>Booking Direct with a Local Team, Not a Reseller</h2>
    </div>
    <div class="steps">
      <div class="step reveal"><div class="num">01</div><h3>You Tell Us the Dates</h3><p>Share your travel window, group size and budget by call, WhatsApp or the enquiry form.</p></div>
      <div class="step reveal"><div class="num">02</div><h3>We Build Your Itinerary</h3><p>Choose a ready package or let us customise the days, hotel category and destinations.</p></div>
      <div class="step reveal"><div class="num">03</div><h3>Confirm &amp; Travel</h3><p>Pay the advance, get your confirmed voucher, and land in Srinagar to a waiting driver.</p></div>
      <div class="step reveal"><div class="num">04</div><h3>We Stay On Call</h3><p>Your coordinator is reachable on WhatsApp for the entire trip — weather changes, upgrades, anything.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">From the Blog</span>
      <h2>Kashmir Travel Guides &amp; Tips</h2>
    </div>
    <div class="grid grid-3">{blog_cards}</div>
    <div style="text-align:center;margin-top:36px;"><a href="blog/index.html" class="btn btn-outline">Read More Guides</a></div>
  </div>
</section>

<section class="band-ivory2">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Guest Reviews</span>
      <h2>What Our Travellers Say</h2>
    </div>
    <div class="grid grid-3">{testi_cards}</div>
    <div style="text-align:center;margin-top:36px;"><a href="testimonials.html" class="btn btn-outline">Read All Reviews</a></div>
  </div>
</section>

<section>
  <div class="container" style="max-width:800px;">
    <div class="section-head reveal">
      <span class="eyebrow">Quick Answers</span>
      <h2>Frequently Asked Questions</h2>
    </div>
    <div class="faq-list">{faq_preview}</div>
    <div style="text-align:center;margin-top:30px;"><a href="faq.html" class="btn btn-outline">See All FAQs</a></div>
  </div>
</section>

<section class="band-teal">
  <div class="container" style="text-align:center;">
    <h2>Ready to Plan Your Kashmir Trip?</h2>
    <p style="max-width:520px;margin:0 auto 24px;">Tell us your dates on WhatsApp and get a custom quote — usually within a few hours.</p>
    <div class="hero-actions" style="justify-content:center;">
      <a href="contact.html" class="btn btn-gold">Get a Free Quote</a>
      <a href="tel:{PHONE_TEL}" class="btn btn-ghost-light">📞 Call {PHONE_DISPLAY}</a>
    </div>
  </div>
</section>
"""
    schema = local_business_schema()
    return page(prefix, "index.html", "Kashmir Tour Packages 2026 | Plan My Trip Kashmir — Srinagar Travel Agency",
                "Book Kashmir tour packages from a local Srinagar travel agency — Gulmarg, Pahalgam, Sonmarg, houseboats and Ladakh. Custom itineraries priced up to 10% below standard market rates.",
                "index.html", body, og_image=IMG['dal_sunset'], extra_schema=schema)


def render_about():
    prefix = ""
    body = f"""
<section class="page-hero">
  <div class="container">
    <div class="crumbs"><a href="index.html">Home</a> / About Us</div>
    <h1>About Plan My Trip Kashmir</h1>
    <p>A locally owned tour and travel company based in Check Pora Kalan, Srinagar — built by people who grew up on these roads.</p>
  </div>
</section>

<section>
  <div class="container" style="display:grid;grid-template-columns:1fr 1fr;gap:50px;align-items:center;">
    <div class="reveal">
      <span class="eyebrow">Our Story</span>
      <h2>Local Ground Team, Not a Call-Centre Reseller</h2>
      <p>Plan My Trip Kashmir was started right here in Srinagar with a simple idea: travellers booking a Kashmir tour package deserve to deal directly with the people who actually run the vehicles, know the houseboat owners personally, and can tell you honestly whether the Gondola is running today — not a call-centre agent reading a script from another city.</p>
      <p>Every itinerary on this site — from a 2-night houseboat stay to the full Kashmir–Ladakh circuit — is built and operated by our own Srinagar-based team. We work with a fixed network of registered houseboats, hotels and drivers we've vetted personally, which is how we're able to hold prices typically below the standard market rate without cutting corners on service.</p>
      <p>We're a small business by design. When you message us, you're talking to someone who can actually change your itinerary on the spot — not submit a ticket.</p>
    </div>
    <div class="arch-frame reveal"><img src="{IMG['shalimar_pav']}" alt="Mughal garden pavilion, Shalimar Bagh Srinagar"></div>
  </div>
</section>

<section class="band-ivory2">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">What We Stand For</span><h2>How We Work</h2></div>
    <div class="grid grid-3">
      <div class="card reveal"><div class="card-body"><h3>Transparent Pricing</h3><p>Every package page lists exactly what's included and excluded — no last-minute surprise charges at checkout.</p></div></div>
      <div class="card reveal"><div class="card-body"><h3>Registered Partners Only</h3><p>We work exclusively with houseboats and hotels registered with Jammu &amp; Kashmir Tourism.</p></div></div>
      <div class="card reveal"><div class="card-body"><h3>Real Customisation</h3><p>Every itinerary can be adjusted — more days here, fewer there, a different hotel category — at no planning fee.</p></div></div>
      <div class="card reveal"><div class="card-body"><h3>On-Trip Support</h3><p>A dedicated coordinator stays reachable on WhatsApp for your entire trip, not just before booking.</p></div></div>
      <div class="card reveal"><div class="card-body"><h3>Honest Weather Calls</h3><p>If the Gondola or a mountain pass is closed, we tell you straight and adjust the day rather than overpromising.</p></div></div>
      <div class="card reveal"><div class="card-body"><h3>Fair, Below-Market Pricing</h3><p>Our local overheads let us typically price 10% below comparable packages from larger national platforms.</p></div></div>
    </div>
  </div>
</section>

<section class="band-teal">
  <div class="container" style="text-align:center;">
    <h2>Visit Us or Say Hello</h2>
    <p>Check Pora Kalan, Srinagar, Jammu &amp; Kashmir 190015</p>
    <div class="hero-actions" style="justify-content:center;">
      <a href="contact.html" class="btn btn-gold">Contact Our Team</a>
      <a href="tel:{PHONE_TEL}" class="btn btn-ghost-light">📞 {PHONE_DISPLAY}</a>
    </div>
  </div>
</section>
"""
    return page(prefix, "about.html", "About Us | Plan My Trip Kashmir — Local Srinagar Travel Agency",
                "Meet Plan My Trip Kashmir, a locally owned tour and travel company based in Srinagar, Jammu & Kashmir, running direct Kashmir holiday packages since day one.",
                "about.html", body, og_image=IMG['shalimar_pav'])


def render_contact():
    prefix = ""
    body = f"""
<section class="page-hero">
  <div class="container">
    <div class="crumbs"><a href="index.html">Home</a> / Contact</div>
    <h1>Get a Free Kashmir Trip Quote</h1>
    <p>Tell us your dates and group size — we usually reply within a few hours with a custom itinerary and price.</p>
  </div>
</section>

<section>
  <div class="container" style="display:grid;grid-template-columns:1.1fr .9fr;gap:50px;">
    <div class="reveal">
      <h2>Send Us Your Trip Details</h2>
      <form data-wa-form>
        <div class="grid grid-2">
          <div class="form-field"><label for="name">Full Name</label><input id="name" name="Name" type="text" required></div>
          <div class="form-field"><label for="phone">Phone / WhatsApp</label><input id="phone" name="Phone" type="tel" required></div>
        </div>
        <div class="grid grid-2">
          <div class="form-field"><label for="dates">Travel Dates</label><input id="dates" name="Travel Dates" type="text" placeholder="e.g. 12–18 May 2026"></div>
          <div class="form-field"><label for="pax">Number of Travellers</label><input id="pax" name="Travellers" type="text" placeholder="e.g. 2 Adults"></div>
        </div>
        <div class="form-field"><label for="pkg">Interested Package</label>
          <select id="pkg" name="Package">
            <option value="">Not sure yet / Custom itinerary</option>
            {"".join(f'<option value="{p["title"]}">{p["title"]} ({p["duration"]})</option>' for p in PACKAGES)}
          </select>
        </div>
        <div class="form-field"><label for="msg">Tell Us More</label><textarea id="msg" name="Message" placeholder="Any preferences — hotel category, honeymoon, Ladakh add-on, budget range..."></textarea></div>
        <button type="submit" class="btn btn-primary">Send via WhatsApp</button>
        <p class="form-note">This site is hosted as a static page for now, so enquiries are sent straight to our WhatsApp — you'll see the message ready to send in a new tab. Prefer email? Write to {EMAIL}.</p>
      </form>
    </div>
    <div class="reveal">
      <div class="sticky-box" style="position:static;">
        <h3>Reach Us Directly</h3>
        <p style="margin-bottom:6px;"><strong>📞 Call / WhatsApp</strong></p>
        <p><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></p>
        <p style="margin-bottom:6px;"><strong>✉️ Email</strong></p>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
        <p style="margin-bottom:6px;"><strong>📍 Office Address</strong></p>
        <p>{ADDRESS}</p>
        <p style="margin-bottom:6px;"><strong>🕐 Response Time</strong></p>
        <p>Usually within a few hours, every day of the week.</p>
        <a href="https://wa.me/{PHONE_WA}" class="btn btn-gold" style="width:100%;justify-content:center;margin-top:10px;">💬 Chat on WhatsApp Now</a>
      </div>
    </div>
  </div>
</section>
"""
    return page(prefix, "contact.html", "Contact Us | Plan My Trip Kashmir — Srinagar Travel Agency",
                "Contact Plan My Trip Kashmir for a custom Kashmir tour package quote. Call or WhatsApp +91 70060 83281, email us, or visit our Srinagar office at Check Pora Kalan.",
                "contact.html", body, og_image=IMG['dal_sunset'])


def render_packages_index():
    prefix = "../"
    cards = ""
    for p in PACKAGES:
        cards += f"""
        <div class="card reveal">
          <div class="card-img"><span class="tag">{p['category']}</span><img src="{p['hero']}" alt="{esc(p['title'])}" loading="lazy"></div>
          <div class="card-body">
            <h3><a href="{p['slug']}.html">{p['title']}</a></h3>
            <p style="margin-bottom:0;font-size:.88rem;">{p['route']}</p>
            <div class="meta-row"><span>📅 {p['duration']}</span></div>
            <div class="price-row">
              <div class="price">₹{p['price']:,}<small> /person</small></div>
              <a href="{p['slug']}.html" class="btn btn-outline" style="padding:9px 16px;font-size:.78rem;">Details</a>
            </div>
          </div>
        </div>"""
    body = f"""
<section class="page-hero">
  <div class="container">
    <div class="crumbs"><a href="{prefix}index.html">Home</a> / Packages</div>
    <h1>Kashmir Tour Packages</h1>
    <p>10 ready-made Kashmir trip packages — from a quick Srinagar houseboat break to the full Kashmir–Ladakh circuit. Every itinerary can be customised on request.</p>
  </div>
</section>
<section>
  <div class="container">
    <p class="small-note" style="margin-bottom:30px;">All prices are per person on twin/double sharing, indicative and subject to season, hotel category and availability — confirm the exact quote with our team before booking. We aim to keep every package priced up to 10% below the typical market rate for the same itinerary.</p>
    <div class="grid grid-3">{cards}</div>
  </div>
</section>
<section class="band-teal">
  <div class="container" style="text-align:center;">
    <h2>Don't See Exactly What You Want?</h2>
    <p style="max-width:520px;margin:0 auto 24px;">Every package here is a starting template — tell us your dates, budget and interests and we'll build a custom Kashmir itinerary around them.</p>
    <a href="{prefix}contact.html" class="btn btn-gold">Request a Custom Itinerary</a>
  </div>
</section>
"""
    return page(prefix, "packages/index.html", "Kashmir Tour Packages List | 10 Curated Kashmir Trip Packages 2026",
                "Browse all Kashmir tour packages from Plan My Trip Kashmir — Srinagar, Gulmarg, Pahalgam, Sonmarg, Ladakh and Vaishno Devi circuits, priced up to 10% below standard market rates.",
                "packages/index.html", body, og_image=IMG['dal_sunset'])


def render_package_detail(p):
    prefix = "../"
    gallery_html = "".join(f'<div class="card-img" style="border-radius:4px;overflow:hidden;"><img src="{g}" alt="{esc(p["title"])} gallery photo" loading="lazy"></div>' for g in p['gallery'])
    highlights_html = "".join(f"<li>{h}</li>" for h in p['highlights'])
    itinerary_html = ""
    for day_title, day_desc in p['itinerary']:
        itinerary_html += f"""<div class="day"><h4>{day_title.split('—')[0].strip()}</h4><h3>{day_title.split('—',1)[1].strip() if '—' in day_title else ''}</h3><p>{day_desc}</p></div>"""
    incl_html = "".join(f"<li>{i}</li>" for i in p['inclusions'])
    excl_html = "".join(f"<li>{e}</li>" for e in p['exclusions'])
    faq_html = ""
    faq_schema_items = []
    for q, a in p['faqs']:
        faq_html += f"""<div class="faq-item"><div class="faq-q">{q}<span class="plus">+</span></div><div class="faq-a"><p>{a}</p></div></div>"""
        faq_schema_items.append((q, a))

    related = [d for d in PACKAGES if d['slug'] != p['slug']][:3]
    related_html = ""
    for r in related:
        related_html += f"""
        <div class="card reveal">
          <div class="card-img"><img src="{r['hero']}" alt="{esc(r['title'])}" loading="lazy"></div>
          <div class="card-body"><h3><a href="{r['slug']}.html">{r['title']}</a></h3>
          <div class="price-row"><div class="price">₹{r['price']:,}<small> /person</small></div></div></div>
        </div>"""

    save_pct = round((p['old_price'] - p['price']) / p['old_price'] * 100)

    faq_schema = ""
    if faq_schema_items:
        entities = ",".join(
            '{"@type":"Question","name":%r,"acceptedAnswer":{"@type":"Answer","text":%r}}' % (q, a)
            for q, a in faq_schema_items
        )
        faq_schema = f'<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{entities}]}}</script>'

    product_schema = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "TouristTrip",
  "name": "{esc(p['title'])}",
  "description": "{esc(p['intro'][:250])}",
  "image": "{p['hero']}",
  "provider": {{"@type":"TravelAgency","name":"{BIZ_NAME}","telephone":"{PHONE_TEL}"}},
  "offers": {{"@type":"Offer","price":"{p['price']}","priceCurrency":"INR","availability":"https://schema.org/InStock"}}
}}
</script>"""

    body = f"""
<section class="page-hero">
  <div class="container">
    <div class="crumbs"><a href="{prefix}index.html">Home</a> / <a href="index.html">Packages</a> / {p['title']}</div>
    <h1>{p['title']}</h1>
    <p>{p['route']} &nbsp;·&nbsp; {p['duration']}</p>
  </div>
</section>

<section style="padding-top:50px;">
  <div class="container" style="display:grid;grid-template-columns:2fr 1fr;gap:50px;align-items:start;">
    <div>
      <div class="arch-wide reveal" style="margin-bottom:30px;"><img src="{p['hero']}" alt="{esc(p['title'])} Kashmir package hero image"></div>
      <h2>Overview</h2>
      <p>{p['intro']}</p>

      <h2>Trip Highlights</h2>
      <ul>{highlights_html}</ul>

      <h2>Day-by-Day Itinerary</h2>
      <div class="itinerary">{itinerary_html}</div>

      <h2>Inclusions &amp; Exclusions</h2>
      <div class="incl-grid">
        <div class="incl-box yes"><h3>What's Included</h3><ul>{incl_html}</ul></div>
        <div class="incl-box no"><h3>What's Not Included</h3><ul>{excl_html}</ul></div>
      </div>

      <h2 style="margin-top:50px;">More Photos</h2>
      <div class="grid grid-3">{gallery_html}</div>

      <h2 style="margin-top:50px;">Package FAQs</h2>
      <div class="faq-list">{faq_html}</div>
    </div>

    <aside>
      <div class="sticky-box">
        <span class="save-tag">Save {save_pct}% vs standard rate</span>
        <div class="price" style="margin-top:8px;"><span class="old-price">₹{p['old_price']:,}</span>₹{p['price']:,}<small> / person</small></div>
        <p class="small-note" style="margin:6px 0 20px;">Twin/double sharing · Price varies by season</p>
        <a href="https://wa.me/{PHONE_WA}?text={esc(p['title']).replace(' ','%20')}%20-%20I'd%20like%20a%20quote" class="btn btn-gold" style="width:100%;justify-content:center;margin-bottom:10px;">💬 Get Exact Quote on WhatsApp</a>
        <a href="tel:{PHONE_TEL}" class="btn btn-outline" style="width:100%;justify-content:center;margin-bottom:10px;">📞 Call {PHONE_DISPLAY}</a>
        <a href="{prefix}contact.html" class="btn btn-primary" style="width:100%;justify-content:center;">Enquire via Form</a>
        <div class="jaali-divider" style="margin:20px 0;"></div>
        <p class="small-note">✓ Fully customisable &nbsp; ✓ Local Srinagar team &nbsp; ✓ Registered houseboats &amp; hotels</p>
      </div>
    </aside>
  </div>
</section>

<section class="band-ivory2">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">You Might Also Like</span><h2>Other Kashmir Packages</h2></div>
    <div class="grid grid-3">{related_html}</div>
  </div>
</section>
"""
    return page(prefix, "packages/index.html", p['meta_title'], p['meta_desc'], f"packages/{p['slug']}.html",
                body, og_image=p['hero'], extra_schema=product_schema + faq_schema)


def render_destinations_index():
    prefix = "../"
    cards = ""
    for d in DESTINATIONS:
        cards += f"""
        <a href="{d['slug']}.html" class="card reveal" style="text-decoration:none;">
          <div class="card-img"><img src="{d['hero']}" alt="{esc(d['title'])}" loading="lazy"></div>
          <div class="card-body"><h3 style="margin-bottom:4px;">{d['title']}</h3><p style="margin:0;font-size:.9rem;">{d['tagline']}</p></div>
        </a>"""
    body = f"""
<section class="page-hero">
  <div class="container">
    <div class="crumbs"><a href="{prefix}index.html">Home</a> / Destinations</div>
    <h1>Kashmir Destinations</h1>
    <p>Everything worth knowing about each stop on a Jammu &amp; Kashmir trip — what to expect, when to go, and which of our packages cover it.</p>
  </div>
</section>
<section><div class="container"><div class="grid grid-3">{cards}</div></div></section>
<section class="band-teal">
  <div class="container" style="text-align:center;">
    <h2>Ready to Put a Route Together?</h2>
    <a href="{prefix}packages/index.html" class="btn btn-gold" style="margin-top:14px;">Browse Ready-Made Packages</a>
  </div>
</section>
"""
    return page(prefix, "destinations/index.html", "Kashmir Destinations Guide | Srinagar, Gulmarg, Pahalgam, Sonmarg, Ladakh",
                "A complete guide to Kashmir's must-visit destinations — Srinagar, Gulmarg, Pahalgam, Sonmarg and Leh-Ladakh — with attractions, best time to visit and how to reach each one.",
                "destinations/index.html", body, og_image=IMG['dal_wide'])


def render_destination_detail(d):
    prefix = "../"
    body_paras = "".join(f"<p>{para}</p>" for para in d['body'])
    attractions_html = "".join(f"<div class='card reveal'><div class='card-body'><h3>{name}</h3><p>{desc}</p></div></div>" for name, desc in d['attractions'])
    gallery_html = "".join(f'<div class="card-img" style="border-radius:4px;overflow:hidden;"><img src="{g}" alt="{esc(d["title"])} photo" loading="lazy"></div>' for g in d['gallery'])
    related = [p for p in PACKAGES if p['slug'] in d['related_packages']]
    related_html = ""
    for r in related:
        related_html += f"""
        <div class="card reveal">
          <div class="card-img"><img src="{r['hero']}" alt="{esc(r['title'])}" loading="lazy"></div>
          <div class="card-body"><h3><a href="{prefix}packages/{r['slug']}.html">{r['title']}</a></h3>
          <div class="price-row"><div class="price">₹{r['price']:,}<small> /person</small></div></div></div>
        </div>"""
    body = f"""
<section class="page-hero">
  <div class="container">
    <div class="crumbs"><a href="{prefix}index.html">Home</a> / <a href="index.html">Destinations</a> / {d['title']}</div>
    <h1>{d['title']}</h1>
    <p>{d['tagline']}</p>
  </div>
</section>
<section style="padding-top:50px;">
  <div class="container">
    <div class="arch-wide reveal" style="margin-bottom:30px;"><img src="{d['hero']}" alt="{esc(d['title'])} Kashmir"></div>
    {body_paras}
    <h2>Top Attractions in {d['title']}</h2>
    <div class="grid grid-3">{attractions_html}</div>
    <div class="grid grid-2" style="margin-top:40px;">
      <div class="incl-box yes"><h3>Best Time to Visit</h3><p style="color:var(--ink-soft);">{d['best_time']}</p></div>
      <div class="incl-box yes"><h3>How to Reach</h3><p style="color:var(--ink-soft);">{d['how_to_reach']}</p></div>
    </div>
    <h2 style="margin-top:50px;">More Photos</h2>
    <div class="grid grid-3">{gallery_html}</div>
  </div>
</section>
<section class="band-ivory2">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">Plan Your Visit</span><h2>Packages Covering {d['title']}</h2></div>
    <div class="grid grid-3">{related_html}</div>
  </div>
</section>
"""
    return page(prefix, "destinations/index.html", d['meta_title'], d['meta_desc'], f"destinations/{d['slug']}.html",
                body, og_image=d['hero'])


def render_gallery():
    prefix = ""
    cats = ["Srinagar", "Gulmarg", "Pahalgam", "Ladakh"]
    items = [
        (IMG['dal_sunset'], "Srinagar", "Houseboats on Dal Lake at sunset"),
        (IMG['shikara'], "Srinagar", "Shikara boats gliding across Dal Lake"),
        (IMG['nishat_bagh'], "Srinagar", "Nishat Bagh Mughal Garden"),
        (IMG['shalimar_arch'], "Srinagar", "Mughal-era architecture, Shalimar Bagh"),
        (IMG['dal_wide'], "Srinagar", "Panoramic view of Dal Lake"),
        (IMG['houseboat'], "Srinagar", "Traditional carved Kashmiri houseboat"),
        (IMG['gulmarg_gondola'], "Gulmarg", "Gulmarg Gondola cable car"),
        (IMG['gulmarg_meadow'], "Gulmarg", "Gulmarg's green meadow"),
        (IMG['gulmarg_cable'], "Gulmarg", "Gondola cable car among pine forest"),
        (IMG['gulmarg_station'], "Gulmarg", "Kongdoori Gondola station"),
        (IMG['betaab1'], "Pahalgam", "Betaab Valley, Pahalgam"),
        (IMG['aru_valley'], "Pahalgam", "Aru Valley meadow"),
        (IMG['pahalgam_valley'], "Pahalgam", "Pahalgam Valley wide view"),
        (IMG['pahalgam_autumn'], "Pahalgam", "Autumn colours in Pahalgam"),
        (IMG['leh1'], "Ladakh", "View over Leh town"),
        (IMG['pangong1'], "Ladakh", "Pangong Tso lake, Ladakh"),
        (IMG['pangong3'], "Ladakh", "Panoramic view of Pangong Lake"),
        (IMG['vaishno1'], "Ladakh", "Hilltop shrine near Katra"),
    ]
    filter_btns = '<button data-cat="all" class="btn btn-outline active">All</button>' + "".join(f'<button data-cat="{c}" class="btn btn-outline">{c}</button>' for c in cats)
    grid_items = ""
    for src, cat, alt in items:
        grid_items += f"""<div class="g-item card" data-cat="{cat}"><div class="card-img"><img src="{src}" alt="{esc(alt)}" loading="lazy"></div></div>"""
    body = f"""
<section class="page-hero">
  <div class="container">
    <div class="crumbs"><a href="index.html">Home</a> / Gallery</div>
    <h1>Kashmir Photo Gallery</h1>
    <p>A look at what's waiting for you — Dal Lake, Gulmarg's gondola, Pahalgam's valleys and Ladakh's high passes.</p>
  </div>
</section>
<section>
  <div class="container">
    <div class="gallery-filter" style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:30px;">{filter_btns}</div>
    <div class="grid grid-4 gallery-grid">{grid_items}</div>
    <p class="small-note" style="margin-top:24px;">Photo credits: Wikimedia Commons contributors (Creative Commons licensed). Replace with your own HD photography any time — see the README included with this site.</p>
  </div>
</section>
<section class="band-teal">
  <div class="container" style="text-align:center;">
    <h2>Seen Enough? Let's Plan Your Trip.</h2>
    <a href="packages/index.html" class="btn btn-gold" style="margin-top:14px;">Browse Packages</a>
  </div>
</section>
<style>.gallery-filter button.active{{background:var(--gold);color:var(--teal);}}</style>
"""
    return page(prefix, "gallery.html", "Kashmir Photo Gallery | Srinagar, Gulmarg, Pahalgam & Ladakh Photos",
                "Browse photos of Kashmir's top destinations — Dal Lake houseboats, Gulmarg's Gondola, Pahalgam's valleys and Ladakh's Pangong Lake.",
                "gallery.html", body, og_image=IMG['dal_sunset'])


def render_faq_page():
    prefix = ""
    sections_html = ""
    schema_entities = []
    for cat_name, qas in FAQ_CATEGORIES:
        items_html = ""
        for q, a in qas:
            items_html += f"""<div class="faq-item"><div class="faq-q">{q}<span class="plus">+</span></div><div class="faq-a"><p>{a}</p></div></div>"""
            schema_entities.append((q, a))
        sections_html += f"""<div class="faq-cat"><h3>{cat_name}</h3><div class="faq-list">{items_html}</div></div>"""

    entities = ",".join(
        '{"@type":"Question","name":%r,"acceptedAnswer":{"@type":"Answer","text":%r}}' % (q, a)
        for q, a in schema_entities
    )
    faq_schema = f'<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{entities}]}}</script>'

    body = f"""
<section class="page-hero">
  <div class="container">
    <div class="crumbs"><a href="index.html">Home</a> / FAQs</div>
    <h1>Frequently Asked Questions</h1>
    <p>Everything travellers ask us before booking a Kashmir trip package — booking, weather, documents, accommodation and what happens on the ground.</p>
  </div>
</section>
<section>
  <div class="container" style="max-width:820px;">{sections_html}</div>
</section>
<section class="band-teal">
  <div class="container" style="text-align:center;">
    <h2>Still Have a Question?</h2>
    <p style="max-width:480px;margin:0 auto 20px;">Message us directly — we typically reply within a few hours.</p>
    <a href="https://wa.me/{PHONE_WA}" class="btn btn-gold">💬 Ask on WhatsApp</a>
  </div>
</section>
"""
    return page(prefix, "faq.html", "Kashmir Tour FAQs | Booking, Weather, Documents & Travel Questions Answered",
                "Frequently asked questions about booking a Kashmir tour package — best time to visit, houseboats, permits, pricing, weather and what's included.",
                "faq.html", body, og_image=IMG['dal_wide'], extra_schema=faq_schema)


def render_testimonials():
    prefix = ""
    cards = ""
    for t in TESTIMONIALS:
        stars = "★" * t[2] + "☆" * (5 - t[2])
        cards += f"""
        <div class="testi reveal"><p>{t[4]}</p>
          <div class="stars">{stars}</div>
          <div class="who">{t[0]} <span style="color:var(--ink-soft);font-weight:400;">— {t[1]}</span></div>
          <div class="small-note" style="margin-top:4px;">Booked: {t[3]}</div>
        </div>"""
    body = f"""
<section class="page-hero">
  <div class="container">
    <div class="crumbs"><a href="index.html">Home</a> / Reviews</div>
    <h1>What Our Travellers Say</h1>
    <p>Real feedback from guests who booked a Kashmir tour package with us.</p>
  </div>
</section>
<section><div class="container"><div class="grid grid-3">{cards}</div></div></section>
<section class="band-teal">
  <div class="container" style="text-align:center;">
    <h2>Add Your Trip to This Page</h2>
    <p style="max-width:480px;margin:0 auto 20px;">Booked with us before? We'd love your feedback — message us your review any time.</p>
    <a href="contact.html" class="btn btn-gold">Share Your Experience</a>
  </div>
</section>
"""
    return page(prefix, "testimonials.html", "Reviews & Testimonials | Plan My Trip Kashmir Guest Experiences",
                "Read real reviews from travellers who booked Kashmir tour packages with Plan My Trip Kashmir — honeymoon, family, luxury and Ladakh trips.",
                "testimonials.html", body, og_image=IMG['dal_sunset'])


def render_blog_index():
    prefix = "../"
    cards = ""
    for b in BLOG_POSTS:
        cards += f"""
        <div class="card blog-card reveal">
          <div class="card-img"><img src="{b['hero']}" alt="{esc(b['title'])}" loading="lazy"></div>
          <div class="card-body">
            <div class="blog-meta">{b['category']} · {b['read']}</div>
            <h3><a href="{b['slug']}.html">{b['title']}</a></h3>
            <p style="font-size:.9rem;">{b['excerpt']}</p>
            <a href="{b['slug']}.html" class="btn btn-outline" style="padding:8px 16px;font-size:.78rem;">Read More</a>
          </div>
        </div>"""
    body = f"""
<section class="page-hero">
  <div class="container">
    <div class="crumbs"><a href="{prefix}index.html">Home</a> / Blog</div>
    <h1>Kashmir Travel Blog</h1>
    <p>Practical, first-hand guides on planning your Kashmir trip — itineraries, best time to visit, budgets and destination deep-dives.</p>
  </div>
</section>
<section><div class="container"><div class="grid grid-3">{cards}</div></div></section>
"""
    return page(prefix, "blog/index.html", "Kashmir Travel Blog | Itineraries, Tips & Destination Guides",
                "Read our Kashmir travel blog for itinerary planning guides, best time to visit tips, budget advice and destination deep-dives on Srinagar, Gulmarg, Pahalgam, Sonmarg and Ladakh.",
                "blog/index.html", body, og_image=IMG['dal_sunset'])


def render_blog_post(b):
    prefix = "../"
    related = [x for x in BLOG_POSTS if x['slug'] != b['slug']][:3]
    related_html = ""
    for r in related:
        related_html += f"""
        <div class="card blog-card reveal">
          <div class="card-img"><img src="{r['hero']}" alt="{esc(r['title'])}" loading="lazy"></div>
          <div class="card-body"><div class="blog-meta">{r['category']}</div><h3><a href="{r['slug']}.html">{r['title']}</a></h3></div>
        </div>"""

    article_schema = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "{esc(b['title'])}",
  "datePublished": "{b['date']}",
  "image": "{b['hero']}",
  "author": {{"@type":"Organization","name":"{BIZ_NAME}"}},
  "publisher": {{"@type":"Organization","name":"{BIZ_NAME}"}}
}}
</script>"""

    body = f"""
<section class="page-hero">
  <div class="container">
    <div class="crumbs"><a href="{prefix}index.html">Home</a> / <a href="index.html">Blog</a> / {b['title']}</div>
    <h1 style="max-width:760px;">{b['title']}</h1>
    <p>{b['category']} · {b['read']} · {b['date']}</p>
  </div>
</section>
<section style="padding-top:44px;">
  <div class="container post-body">
    <div class="post-hero-img reveal"><img src="{b['hero']}" alt="{esc(b['title'])}"></div>
    {b['body']}
    <div class="jaali-divider" style="margin:40px 0;"></div>
    <p><strong>Planning your own trip?</strong> Browse our <a href="{prefix}packages/index.html">Kashmir tour packages</a> or <a href="{prefix}contact.html">message us on WhatsApp</a> for a same-day custom quote.</p>
  </div>
</section>
<section class="band-ivory2">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">Keep Reading</span><h2>More Kashmir Travel Guides</h2></div>
    <div class="grid grid-3">{related_html}</div>
  </div>
</section>
"""
    return page(prefix, "blog/index.html", b['meta_title'], b['meta_desc'], f"blog/{b['slug']}.html",
                body, og_image=b['hero'], extra_schema=article_schema)


def render_privacy():
    prefix = ""
    body = f"""
<section class="page-hero"><div class="container"><div class="crumbs"><a href="index.html">Home</a> / Privacy Policy</div><h1>Privacy Policy</h1></div></section>
<section><div class="container post-body">
<p>Last updated: 2026. {BIZ_NAME} ("we", "us") operates this website. This page explains how we handle information you share with us.</p>
<h2>Information We Collect</h2>
<p>When you contact us via our enquiry form, WhatsApp, phone or email, we collect the details you choose to share — typically your name, phone number, email address, travel dates and trip preferences. This site is currently a static informational website; enquiry forms send your message directly to our WhatsApp number and do not store data on a server.</p>
<h2>How We Use It</h2>
<p>We use the information you provide solely to respond to your enquiry, prepare an itinerary and price quote, and manage your booking if you choose to proceed. We do not sell or rent your personal information to third parties.</p>
<h2>Third-Party Services</h2>
<p>Sightseeing bookings, hotel and houseboat reservations are made with our vetted local partners as required to fulfil your trip. We share only the details necessary for your booking.</p>
<h2>Cookies</h2>
<p>This website does not currently use tracking cookies. If analytics or advertising tools are added in future, this policy will be updated accordingly.</p>
<h2>Contact Us</h2>
<p>For any privacy-related questions, write to us at <a href="mailto:{EMAIL}">{EMAIL}</a> or call {PHONE_DISPLAY}.</p>
</div></section>
"""
    return page(prefix, "privacy-policy.html", "Privacy Policy | Plan My Trip Kashmir", "Privacy policy for Plan My Trip Kashmir, explaining how we collect and use information shared through our website and enquiry forms.", "privacy-policy.html", body, noindex=False)


def render_terms():
    prefix = ""
    body = f"""
<section class="page-hero"><div class="container"><div class="crumbs"><a href="index.html">Home</a> / Terms &amp; Conditions</div><h1>Terms &amp; Conditions</h1></div></section>
<section><div class="container post-body">
<p>Last updated: 2026. Please read these terms carefully before booking a Kashmir tour package with {BIZ_NAME}.</p>
<h2>Bookings &amp; Payment</h2>
<p>A booking is confirmed only once the agreed advance payment is received and a written confirmation (via WhatsApp or email) is issued by our team. Package prices shown on this website are indicative starting prices per person on twin/double sharing and vary by season, hotel category, group size and availability at the time of booking.</p>
<h2>Cancellations &amp; Refunds</h2>
<p>Cancellation charges depend on how close to the travel date a cancellation is made, since houseboats and hotels apply their own supplier cancellation policies during peak season. We will share the specific cancellation terms applicable to your booking in writing before you make any payment.</p>
<h2>Itinerary Changes</h2>
<p>Sightseeing (such as the Gulmarg Gondola or mountain passes) may be affected by weather, road conditions or local authority restrictions beyond our control. In such cases, our team will offer the best available alternative; refunds for weather-affected activities are handled per the specific supplier's policy.</p>
<h2>Traveller Responsibility</h2>
<p>Travellers are responsible for carrying valid ID proof, any required permits (such as the Inner Line Permit for Ladakh, which we assist with), and for disclosing relevant medical conditions ahead of high-altitude travel.</p>
<h2>Liability</h2>
<p>{BIZ_NAME} acts as a facilitator between travellers and third-party hotels, houseboats, transport and activity providers. While we vet all our partners carefully, we are not liable for circumstances beyond our reasonable control, including natural events, government restrictions or third-party service failures.</p>
<h2>Governing Law</h2>
<p>These terms are governed by the laws of India, with disputes subject to the jurisdiction of the courts in Srinagar, Jammu &amp; Kashmir.</p>
<h2>Contact</h2>
<p>Questions about these terms can be sent to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</div></section>
"""
    return page(prefix, "terms-conditions.html", "Terms & Conditions | Plan My Trip Kashmir", "Terms and conditions for booking Kashmir tour packages with Plan My Trip Kashmir, including payment, cancellation and liability terms.", "terms-conditions.html", body)


def render_404():
    prefix = ""
    body = f"""
<section class="page-hero" style="text-align:center;">
  <div class="container">
    <h1>404 — Page Not Found</h1>
    <p>The page you're looking for may have moved. Let's get you back on track.</p>
  </div>
</section>
<section style="text-align:center;">
  <div class="container">
    <a href="index.html" class="btn btn-gold">Back to Home</a>
    <a href="packages/index.html" class="btn btn-outline" style="margin-left:12px;">Browse Packages</a>
  </div>
</section>
"""
    return page(prefix, "404.html", "Page Not Found | Plan My Trip Kashmir", "The page you requested could not be found.", "404.html", body, noindex=True)



# ---------------- WRITE ALL PAGES ----------------
write("index.html", render_home())
write("about.html", render_about())
write("contact.html", render_contact())
write("gallery.html", render_gallery())
write("faq.html", render_faq_page())
write("testimonials.html", render_testimonials())
write("privacy-policy.html", render_privacy())
write("terms-conditions.html", render_terms())
write("404.html", render_404())

write("packages/index.html", render_packages_index())
for _p in PACKAGES:
    write(f"packages/{_p['slug']}.html", render_package_detail(_p))

write("destinations/index.html", render_destinations_index())
for _d in DESTINATIONS:
    write(f"destinations/{_d['slug']}.html", render_destination_detail(_d))

write("blog/index.html", render_blog_index())
for _b in BLOG_POSTS:
    write(f"blog/{_b['slug']}.html", render_blog_post(_b))

# ---------------- sitemap.xml ----------------
urls = ["index.html","about.html","contact.html","gallery.html","faq.html","testimonials.html",
        "privacy-policy.html","terms-conditions.html","packages/index.html","destinations/index.html","blog/index.html"]
urls += [f"packages/{p['slug']}.html" for p in PACKAGES]
urls += [f"destinations/{d['slug']}.html" for d in DESTINATIONS]
urls += [f"blog/{b['slug']}.html" for b in BLOG_POSTS]

sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in urls:
    loc = SITE_URL + "/" + u
    sitemap += f"  <url><loc>{loc}</loc></url>\n"
sitemap += "</urlset>\n"
write("sitemap.xml", sitemap)

# ---------------- robots.txt ----------------
robots = f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""
write("robots.txt", robots)

print("Generated", len(urls), "HTML pages + sitemap.xml + robots.txt")
