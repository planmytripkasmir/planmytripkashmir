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
