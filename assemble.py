import os

ROOT = "/home/claude/site"
order = [
    "build.py",
    "build_data_packages.py",
    "build_data_destinations.py",
    "build_data_blog.py",
    "build_data_faq.py",
    "build_pages_core.py",
    "build_pages_packages.py",
    "build_pages_destinations.py",
    "build_pages_more.py",
    "build_pages_blog.py",
]

src = ""
for fname in order:
    with open(os.path.join(ROOT, fname), encoding="utf-8") as f:
        src += f.read() + "\n\n"

# Append the execution block that actually writes every file
src += '''
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

sitemap = \'<?xml version="1.0" encoding="UTF-8"?>\\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\\n\'
for u in urls:
    loc = SITE_URL + "/" + u
    sitemap += f"  <url><loc>{loc}</loc></url>\\n"
sitemap += "</urlset>\\n"
write("sitemap.xml", sitemap)

# ---------------- robots.txt ----------------
robots = f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""
write("robots.txt", robots)

print("Generated", len(urls), "HTML pages + sitemap.xml + robots.txt")
'''

with open(os.path.join(ROOT, "_full_build.py"), "w", encoding="utf-8") as f:
    f.write(src)

print("Assembled _full_build.py, length:", len(src))
