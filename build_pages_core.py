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
