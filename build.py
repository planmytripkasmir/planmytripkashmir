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
