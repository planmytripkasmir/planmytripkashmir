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
