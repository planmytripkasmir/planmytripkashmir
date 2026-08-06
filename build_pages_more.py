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
