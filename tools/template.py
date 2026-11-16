# Page template for SVSGK project detail pages (layout modelled on the reference project page).
import html, json, urllib.parse, hashlib, os

e = html.escape
PHONE = "9849630690"
WA = f"https://wa.me/91{PHONE}"
SITE = "https://svsgkrealty.com"
# cache-busting stamp: changes whenever project.css/js change, so browsers never mix new HTML with old cached assets
_A = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
ASSET_V = hashlib.md5(b"".join(open(os.path.join(_A, f), "rb").read() for f in ("project.css", "project.js"))).hexdigest()[:8]

EXTRA_ICONS = {
 "train":  '<rect x="6" y="3" width="12" height="13" rx="3"/><path d="M6 10h12M9 16l-2 5M15 16l2 5M8 19h8"/><circle cx="9" cy="13" r=".6"/><circle cx="15" cy="13" r=".6"/>',
 "school": '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c3 2.5 9 2.5 12 0v-5M22 9v6"/>',
 "office": '<rect x="4" y="3" width="10" height="18"/><path d="M14 9h6v12h-6M7 7h1M10 7h1M7 11h1M10 11h1M7 15h1M10 15h1M3 21h18"/>',
 "route":  '<circle cx="6" cy="5" r="2"/><circle cx="18" cy="19" r="2"/><path d="M6 7v3a4 4 0 0 0 4 4h4a4 4 0 0 1 4 4"/>',
 "junction":'<path d="M12 3v18M3 12h18M8 8l-2-2M16 8l2-2M8 16l-2 2M16 16l2 2"/>',
}

AM_CAT = {
 "INFRASTRUCTURE": {"road","compass","tank","bolt","light","pipe","drop","rain","trash","land","path"},
 "LIFESTYLE": {"tree","walk","gym","kids","flower","villa","apt"},
 "SAFETY": {"gate","cam","shield"},
}

def feat_icon(t):
    s = t.lower()
    if "railway" in s or "station" in s: return "train"
    if any(k in s for k in ("school","college","university","nit ")) or s.endswith("nit warangal"): return "school"
    if "it hub" in s or "it companies" in s or "office" in s or "registrar" in s: return "office"
    if "highway" in s or "ring road" in s or "orr" in s or "road" in s: return "junction"
    if "construction" in s or "homes" in s or "village" in s: return "villa"
    if "authority" in s or "municipal" in s or "corporation" in s: return "shield"
    return "route"

def card(o, base):
    oa = dict(o["approvals"])
    dev = next((b for a, b in o["approvals"] if a == "Land"), None)
    return f'''<a class="rc" href="{base}{o["slug"]}/"><div class="im"><img src="{base}assets/p/{o["card"]}" alt="{e(o["name"])}" loading="lazy"><span class="badge">Ongoing</span></div>
<div class="bub">{e(o["name"])}</div><div class="bd"><span class="cfg">Open Plots</span>
<span class="ln"><svg viewBox="0 0 24 24"><path d="M12 2a7 7 0 0 0-7 7c0 5.3 7 13 7 13s7-7.7 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg><b>{e(o["loc"])}</b></span>
<span class="ln">Plot Size: <b>{e(o["facts"][1][2].replace(" and ", ", "))}</b></span>
{f'<span class="ln">Development Size: <b>{e(dev)}</b></span>' if dev else f'<span class="ln">Approval: <b>{e(oa.get("Approval",""))}</b></span>'}
<span class="ln">Price: <b>Get a Quote</b></span><span class="vd">View details</span></div></a>'''

def render(p, others, I):
    icons = dict(I); icons.update(EXTRA_ICONS)
    svg = lambda k: f'<svg viewBox="0 0 24 24" aria-hidden="true">{icons[k]}</svg>'
    A = lambda s: "../assets/p/" + s
    hero = "../assets/hero.webp" if p["hero"].startswith("..") else A(p["hero"])
    wa_txt = urllib.parse.quote(f"Hi SVSGK, I'm interested in {p['name']}. Please share plot availability and price details.")
    visit = urllib.parse.quote(f"Hi SVSGK, I'd like to schedule a site visit to {p['name']}.")
    map_src = "https://maps.google.com/maps?q=" + urllib.parse.quote(p["map_q"]) + "&z=13&output=embed"

    ap = dict(p["approvals"])
    reg_key = next((k for k in ap if k in ("TS RERA No.","LP No.","LTP No.")), None)
    rows = []
    if reg_key: rows.append(f'<small>{e(reg_key.replace(" No.", ""))} No.</small><small><b>{e(ap[reg_key])}</b></small>')
    rows.append(f'<small><b>{e(ap.get("Approval","KUDA Approved"))}</b></small>')
    rows.append('<small>https://rera.telangana.gov.in/</small>' if "TS RERA No." in ap else f'<small>{e(p["loc"])}</small>')
    permit = "".join(rows)

    sizes = p["facts"][1][2]
    keys = [("Location", p["loc"].split(",")[0]), ("Plot Sizes", sizes.replace(" and ", ", ")), ("Approval", ap.get("Approval","KUDA Approved")), ("Price", "Get a Quote")]
    keys_html = "".join(f'<div><span>{e(a)}</span><h4>{e(b)}</h4></div>' for a, b in keys)
    nums = "".join(f'<div><h5>{e(a)}</h5><h3>{e(b)}</h3></div>' for a, b in p["stats"])

    feats = []
    for k in p["location"]:
        feats += p["location"][k]
    seen, flist = set(), []
    for f in feats:
        if f not in seen: seen.add(f); flist.append(f)
    flist = flist[:10]
    feats_html = "".join(f'<li>{svg(feat_icon(f))}<p>{e(f)}</p></li>' for f in flist)

    ltabs = list(p["location"].keys())
    ltab_html = "".join(f'<button role="tab" aria-selected="{"true" if i==0 else "false"}" data-k="{e(k)}">{e(k)}</button>' for i, k in enumerate(ltabs))
    checks = "".join(f'<li data-k="{e(k)}"{"" if i==0 else " hidden"}>{e(x)}</li>' for i, k in enumerate(ltabs) for x in p["location"][k])

    cats = [c for c in AM_CAT if any(k in AM_CAT[c] for k, _ in p["amenities"])]
    def cat_of(k):
        for c in AM_CAT:
            if k in AM_CAT[c]: return c
        return "INFRASTRUCTURE"
    am_tabs = "".join(f'<button role="tab" aria-selected="{"true" if i==0 else "false"}" data-c="{c}">{c}</button>' for i, c in enumerate(cats))
    am_html = "".join(f'<div class="am" data-c="{cat_of(k)}"{"" if cat_of(k)==cats[0] else " hidden"}><span class="ring">{svg(k)}</span><p>{e(t)}</p></div>' for k, t in p["amenities"])

    gal = "".join(f'<figure data-full="{A(s)}" data-cap="{e(c)}"><img src="{A(s)}" alt="{e(c)}" decoding="async"></figure>' for s, c in p["gallery"])

    lp_meta = "".join(f'<div><span>{e(a)}</span><b>{e(b)}</b></div>' for a, b, _ in p["lps"])

    lp_all = "; ".join(f"{a}: {b}" for a, b, _ in p["lps"])
    faqs = [
      (f"What is {p['name']}?", p["intro"]),
      (f"Where is {p['name']} located?", f"{p['name']} is located at {p['facts'][0][2]}."),
      (f"What are the locational advantages of {p['name']}?", " ".join(x.rstrip(".") + "." for x in flist[:5])),
      (f"Is {p['name']} an approved layout?", f"Yes. {p['facts'][3][2]}. {lp_all}."),
      (f"What plot sizes are available at {p['name']}?", f"Plots are available in {sizes} sizes, all 100% Vaastu compliant."),
      ("Is a bank loan available?", "Yes, bank loans are available for plots in this layout."),
    ]
    faq_html = "".join(f'<div class="item{" open" if i==0 else ""}"{" hidden" if i>=3 else ""}><button class="q" aria-expanded="{"true" if i==0 else "false"}"><h3>{e(q)}</h3><svg viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></svg></button><div class="a"><div><p>{e(a)}</p></div></div></div>' for i, (q, a) in enumerate(faqs))

    recs = "".join(card(o, "../") for o in others)

    social = (
      f'<a href="https://www.instagram.com/svsgkrealty/" target="_blank" rel="noopener" aria-label="Instagram" style="background:linear-gradient(45deg,#f9ce34,#ee2a7b,#6228d7)"><svg viewBox="0 0 24 24"><path d="M12 7.3A4.7 4.7 0 1 0 12 16.7 4.7 4.7 0 0 0 12 7.3zm0 7.7a3 3 0 1 1 0-6 3 3 0 0 1 0 6zm4.9-7.9a1.1 1.1 0 1 1-2.2 0 1.1 1.1 0 0 1 2.2 0zM21 8.1c-.1-1.5-.4-2.8-1.5-3.9S17.1 2.8 15.6 2.7c-1.5-.1-6-.1-7.5 0-1.5.1-2.8.4-3.9 1.5S2.8 6.6 2.7 8.1c-.1 1.5-.1 6 0 7.5.1 1.5.4 2.8 1.5 3.9s2.4 1.4 3.9 1.5c1.5.1 6 .1 7.5 0 1.5-.1 2.8-.4 3.9-1.5s1.4-2.4 1.5-3.9c.1-1.5.1-6 0-7.5z"/></svg></a>'
      f'<a href="https://www.facebook.com/profile.php?id=61561106980623" target="_blank" rel="noopener" aria-label="Facebook" style="background:#1877F2;border-radius:50%"><svg viewBox="0 0 24 24"><path d="M14 8V6.5c0-.7.3-1 1.1-1H17V2.2C16.6 2.1 15.4 2 14.3 2 11.7 2 10 3.6 10 6.4V8H7.5v3.4H10V22h4V11.4h2.8L17.3 8z"/></svg></a>'
      f'<a href="https://www.linkedin.com/company/svsgk-realty/" target="_blank" rel="noopener" aria-label="LinkedIn" style="background:#0A66C2"><svg viewBox="0 0 24 24"><path d="M6.9 8.8H3.4V20h3.5zM5.2 3.5a2 2 0 1 0 0 4 2 2 0 0 0 0-4zM20.6 13.9c0-3-.7-5.3-4.2-5.3-1.7 0-2.8.9-3.3 1.8V8.8H9.8V20h3.5v-5.5c0-1.5.3-2.9 2.1-2.9s1.8 1.7 1.8 3V20h3.5z"/></svg></a>'
      f'<a href="https://wa.me/91{PHONE}" target="_blank" rel="noopener" aria-label="WhatsApp" style="background:#25D366;border-radius:50%"><svg viewBox="0 0 24 24"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1l-.9 1.2c-.2.2-.4.2-.7.1-1.6-.8-2.7-1.4-3.7-3.2-.3-.5.3-.5.8-1.6.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4s-1 1-1 2.5 1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5 1.9.8 2.6.9 3.6.7.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3zM12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2z"/></svg></a>'
    )

    ld = {"@context":"https://schema.org","@type":"Residence","name":p["name"],"description":p["intro"],
          "address":{"@type":"PostalAddress","addressLocality":p["loc"],"addressRegion":"Telangana","addressCountry":"IN"}}

    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(p["name"])} | Open Plots for Sale in {e(p["loc"].split(",")[0])} | SVSGK Realty</title>
<meta name="description" content="{e(p["summary"])} {e(p["facts"][3][2])}. Plot sizes {e(sizes)}.">
<meta name="theme-color" content="#0C385D">
<link rel="icon" href="../assets/svsgk-logo.png">
<link rel="preload" as="image" href="{hero}" fetchpriority="high">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Open+Sans:wght@400;500;600;700&family=Raleway:wght@500;600&family=Roboto:wght@500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/project.css?v={ASSET_V}">
<script type="application/ld+json">{json.dumps(ld)}</script>
</head>
<body>



<section class="hero" id="top" style="background-image:url('{hero}')" aria-label="{e(p["name"])}">
  <header>
    <div class="box">
      <a href="{SITE}/" class="logo" aria-label="SVSGK Realty home"><img src="../assets/svsgk-logo.webp" alt="SVSGK Realty" width="66" height="65"></a>
      <ul class="nav" id="menu">
        <li class="mx"><button type="button" data-navclose aria-label="Close menu">&#x2715;</button></li>
        <li><a href="{SITE}/">Home</a></li>
        <li><a href="{SITE}/about-us/">About us</a></li>
        <li><a href="../" class="on">Projects</a></li>
        <li><a href="{SITE}/gallery/">Gallery</a></li>
        <li><a href="https://nri.svsgkrealty.com/">NRI</a></li>
        <li><a href="{SITE}/blogs/">Blogs</a></li>
        <li class="mc"><a href="#" data-enq>Contact Us</a></li>
      </ul>
      <a href="#" class="cta" data-enq>Contact us</a>
      <button class="burger" id="burger" aria-label="Open menu" aria-expanded="false"><i></i></button>
    </div>
  </header>
  <div class="permit"><div class="pl">{e(p["name"])}</div><div class="tbl">{permit}</div></div>
  <a href="#overview" class="down" aria-label="Scroll down"><svg viewBox="0 0 24 24"><path d="M12 5v14M6 13l6 6 6-6"/></svg></a>
</section>

<section id="overview">
  <div class="wrap">
    <div class="keys">{keys_html}</div>
    <h1 class="main">Open Plots in {e(p["loc"].split(",")[0])} - {e(p["name"])}</h1>
    <div class="rich">{e(p["tag"])}</div>
    <div class="nums">{nums}</div>
    <p class="blurb">{e(p["intro"])}</p>
  </div>
  <h2 class="heading">Standout Features</h2>
  <div class="feat">
    <div class="feat-img" style="background-image:url('{A(p["ov_img"])}')"><span>{e(p["name"])}</span></div>
    <ul>{feats_html}</ul>
  </div>
</section>

<section id="location" class="sec">
  <div class="wrap">
    <h2 class="heading">Location Highlights</h2>
    <div class="tabs"><div class="grp" role="tablist" id="ltabs">{ltab_html}</div></div>
    <div class="loc">
      <div><iframe src="{map_src}" title="{e(p["name"])} on Google Maps" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe><p class="eta">*Distances approx. as per project brochure</p></div>
      <ul class="checks" id="checks">{checks}</ul>
    </div>
    <div class="cta-row"><a class="btn-red" href="{WA}?text={visit}" target="_blank" rel="noopener">Schedule a site visit</a></div>
  </div>
</section>

<section id="amenities" class="band sec">
  <div class="wrap">
    <h2 class="heading">Amenities</h2>
    <div class="am-tabs" role="tablist" id="atabs">{am_tabs}</div>
    <div class="am-grid" id="agrid">{am_html}</div>
  </div>
</section>

<section id="gallery" class="gal">
  <h2 class="heading" style="padding-top:36px;margin-bottom:20px">Gallery</h2>
  <div style="position:relative">
    <button class="arr l" data-dir="-1" aria-label="Previous"><svg viewBox="0 0 24 24"><path d="M19 12H5M11 6l-6 6 6 6"/></svg></button>
    <div class="gal-track" id="gal">{gal}</div>
    <button class="arr r" data-dir="1" aria-label="Next"><svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button>
  </div>
  <p class="gal-cap" id="galcap"></p>
</section>

<section id="layout" class="sec">
  <div class="wrap">
    <h2 class="heading" style="margin-bottom:20px">Layout</h2>
    <div class="layout-img" data-full="{A(p["layout"])}"><img src="{A(p["layout"])}" alt="{e(p["name"])} layout plan" loading="lazy"></div>
    <div class="plan-meta">{lp_meta}</div>
    <div class="dl"><a class="btn-out" href="../brochures/{p["brochure"]}" download>Download Brochure</a><a class="btn-red" style="padding:10px 24px" href="{WA}?text={wa_txt}" target="_blank" rel="noopener">Check plot availability</a></div>
  </div>
</section>

<section id="faqs" class="sec">
  <div class="wrap">
    <h2 class="heading" style="padding-bottom:12px">FAQs</h2>
    <div class="faq" id="faq">{faq_html}</div>
    <div class="vm"><button class="btn-out" id="vm">View More</button></div>
  </div>
</section>

<section class="band rec">
  <div class="wrap">
    <h2 class="heading" style="margin-bottom:12px">Recommended Projects</h2>
    <div class="rec-grid">{recs}</div>
  </div>
</section>

<footer>
  <div class="ftw ft">
    <div>
      <a href="{SITE}/" class="ft-logo" aria-label="SVSGK Realty"><img src="../assets/svsgk-logo.webp" alt="SVSGK Realty" loading="lazy"></a>
      <p>At SVSGK realty, every project is a testament to our promises, quality, and services. For your home, trust SVSGK realty and discover the difference for yourself.</p>
    </div>
    <div>
      <h3>Impotant Links</h3>
      <ul>
        <li><a href="{SITE}/">Home</a></li>
        <li><a href="{SITE}/about-us/">About us</a></li>
        <li><a href="../">Projects</a></li>
        <li><a href="{SITE}/gallery/">Gallery</a></li>
        <li><a href="https://nri.svsgkrealty.com/">NRI</a></li>
        <li><a href="{SITE}/blogs/">Blogs</a></li>
        <li><a href="{SITE}/terms-and-condition/">Terms and condition</a></li>
      </ul>
    </div>
    <div>
      <h3>Address</h3>
      <a href="mailto:support@svsgkrealty.com" style="margin-top:10px">support@svsgkrealty.com</a>
      <b><a href="tel:+91{PHONE}">9849630690, 950417199</a></b>
      <address>H.No. 1-1-28, Chaitanyapuri Colony, Near: Sri Venkateshwaraswamy Temple, Hanamkonda, Warangal, Telangana.</address>
    </div>
    <div>
      <h3>Our social media</h3>
      <div class="social">
        <a href="https://www.facebook.com/profile.php?id=61561106980623" target="_blank" rel="noopener" aria-label="Facebook"><svg viewBox="0 0 24 24"><path d="M9.1 23.7v-8H6.6V12h2.5v-1.6c0-4.1 1.9-6 5.9-6 .8 0 2.1.2 2.6.3v3.4c-.3 0-.8-.1-1.4-.1-2 0-2.7.7-2.7 2.7V12h3.9l-.7 3.7h-3.3V24A12 12 0 1 0 9.1 23.7z"/></svg></a>
        <a class="li" href="https://www.linkedin.com/company/svsgk-realty/" target="_blank" rel="noopener" aria-label="LinkedIn"><svg viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 1 1 0-4.125 2.062 2.062 0 0 1 0 4.125zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg></a>
        <a href="https://www.instagram.com/svsgkrealty/" target="_blank" rel="noopener" aria-label="Instagram"><svg viewBox="0 0 24 24"><path d="M12 2.16c3.2 0 3.58.01 4.85.07 3.25.15 4.77 1.69 4.92 4.92.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.15 3.23-1.66 4.77-4.92 4.92-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-3.26-.15-4.77-1.7-4.92-4.92C2.17 15.58 2.16 15.2 2.16 12s.01-3.58.07-4.85C2.38 3.92 3.9 2.38 7.15 2.23 8.42 2.17 8.8 2.16 12 2.16zM12 0C8.74 0 8.33.01 7.05.07 2.7.27.27 2.69.07 7.05.01 8.33 0 8.74 0 12s.01 3.67.07 4.95c.2 4.36 2.62 6.78 6.98 6.98C8.33 23.99 8.74 24 12 24s3.67-.01 4.95-.07c4.35-.2 6.78-2.62 6.98-6.98.06-1.28.07-1.69.07-4.95s-.01-3.67-.07-4.95c-.2-4.35-2.62-6.78-6.98-6.98C15.67.01 15.26 0 12 0zm0 5.84a6.16 6.16 0 1 0 0 12.32 6.16 6.16 0 0 0 0-12.32zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.4-11.85a1.44 1.44 0 1 0 0 2.88 1.44 1.44 0 0 0 0-2.88z"/></svg></a>
        <a href="https://www.youtube.com/" target="_blank" rel="noopener" aria-label="YouTube"><svg viewBox="0 0 24 24"><path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.6 12 3.6 12 3.6s-7.5 0-9.4.5A3 3 0 0 0 .5 6.2 31 31 0 0 0 0 12a31 31 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.5 9.4.5 9.4.5s7.5 0 9.4-.5a3 3 0 0 0 2.1-2.1A31 31 0 0 0 24 12a31 31 0 0 0-.5-5.8zM9.6 15.6V8.4l6.2 3.6-6.2 3.6z"/></svg></a>
        <a href="https://wa.me/919849630690" target="_blank" rel="noopener" aria-label="WhatsApp"><svg viewBox="0 0 24 24"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.65.07-.3-.15-1.26-.46-2.4-1.48-.89-.79-1.49-1.77-1.66-2.07-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.61-.92-2.21-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.21 3.08c.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.69.63.71.23 1.36.19 1.87.12.57-.09 1.76-.72 2.01-1.41.25-.69.25-1.29.17-1.41-.07-.12-.27-.2-.57-.35zM12.05 21.5h-.01a9.4 9.4 0 0 1-4.8-1.31l-.34-.2-3.57.94.95-3.48-.22-.36a9.43 9.43 0 1 1 7.99 4.41zm8.03-17.46A11.32 11.32 0 0 0 12.05.72 11.37 11.37 0 0 0 2.2 17.77L.6 23.6l5.96-1.56a11.35 11.35 0 0 0 5.48 1.4h.01c6.27 0 11.37-5.1 11.37-11.37 0-3.04-1.18-5.89-3.34-8.04z"/></svg></a>
      </div>
    </div>
  </div>
</footer>

<nav class="dock" id="dock" aria-label="Quick contact">
  <a href="tel:+91{PHONE}" class="call" aria-label="Call SVSGK Realty"><span class="ic"><svg viewBox="0 0 24 24" width="16" height="16" fill="#fff"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg></span>Call now</a>
  <a href="{WA}?text={urllib.parse.quote(f"Hi, I'm interested in {p['name']}. Please share details.")}" class="wa" target="_blank" rel="noopener" aria-label="Chat on WhatsApp"><span class="ic"><svg viewBox="0 0 24 24" width="16" height="16" fill="#fff"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1l-.9 1.2c-.2.2-.4.2-.7.1-1.6-.8-2.7-1.4-3.7-3.2-.3-.5.3-.5.8-1.6.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4s-1 1-1 2.5 1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5 1.9.8 2.6.9 3.6.7.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3zM12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2z"/></svg></span>WhatsApp</a>
</nav>

<a href="#top" class="totop" id="totop" aria-label="Back to top"><svg viewBox="0 0 24 24"><path d="M12 19V5M6 11l6-6 6 6"/></svg></a>

<dialog class="enqm" id="enqm"><div class="hd">Enquire about {e(p["name"])}<button type="button" data-close aria-label="Close">&#x2715;</button></div>
<form id="enqf" data-project="{e(p["name"])}" data-wa="{WA}">
  <label>Name<input name="name" required autocomplete="name"></label>
  <label>Phone<input name="phone" type="tel" required autocomplete="tel" pattern="[0-9+ ]{{10,15}}"></label>
  <label>Message<textarea name="msg" rows="3">Please share plot availability and price details.</textarea></label>
  <button class="sub" type="submit">Send on WhatsApp</button>
</form></dialog>

<dialog class="lb" id="lb"><button class="x" aria-label="Close">&#x2715;</button><div class="stage"><img alt=""></div></dialog>

<script src="../assets/project.js?v={ASSET_V}" defer></script>
</body>
</html>
'''
