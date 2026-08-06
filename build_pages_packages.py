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
