# -*- coding: utf-8 -*-
import os, html as _h

import pathlib, hashlib
# repo root = parent of the _build/ folder this script lives in
OUT = str(pathlib.Path(__file__).resolve().parent.parent)

# content hash of the stylesheet -> cache-busting query on every <link>
try:
    CSS_VER = hashlib.md5(
        open(os.path.join(OUT, 'assets', 'site.css'), 'rb').read()
    ).hexdigest()[:8]
except OSError:
    CSS_VER = '1'

# append ?v=<content hash> to every local /images, /assets and /favicon.ico
# reference so a changed file is never served from a stale browser cache
import re as _re
_ver_cache = {}
def _file_ver(rel):
    if rel not in _ver_cache:
        try:
            _ver_cache[rel] = hashlib.md5(
                open(os.path.join(OUT, rel.lstrip('/')), 'rb').read()
            ).hexdigest()[:8]
        except OSError:
            _ver_cache[rel] = None
    return _ver_cache[rel]

def add_asset_versions(html):
    def repl(m):
        attr, path = m.group(1), m.group(2)
        v = _file_ver(path)
        return f'{attr}="{path}?v={v}"' if v else m.group(0)
    return _re.sub(r'(src|href)="((?:/(?:images|assets)/[^"?]+)|/favicon\.ico)"', repl, html)

BASE = 'https://alabamaaquatics.com'
PHONE = '205-810-6288'
TEL = '2058106288'
EMAIL = 'contact@alabamaaquatics.com'
FB = 'https://www.facebook.com/profile.php?id=61574288617629'
IG = 'https://www.instagram.com/alabamaaquatics/'
SMS = TEL  # texting number

# ─────────────────────────────────────────────────────────────────────────────
# EDIT THESE to switch on the reviews / rating features.
# While REVIEWS is empty and GOOGLE_RATING is None, nothing review-related
# renders (no fake content ships) — the rest of the site is unaffected.
# ─────────────────────────────────────────────────────────────────────────────
FOUNDED_YEAR       = 2025
HOURS              = "Monday – Saturday, 8 AM – 6 PM"   # TODO: confirm real hours
GOOGLE_PROFILE_URL = ""      # paste your Google "write a review" / profile link
GOOGLE_RATING      = None    # e.g. 4.9
GOOGLE_REVIEW_COUNT = None   # e.g. 27
REVIEWS = [
    # Each: dict(name=, location=, service=, text=)  -- real Google reviews only.
    # e.g. dict(name="Jane D.", location="Trussville", service="Weekly Pool Cleaning",
    #           text="They show up every week like clockwork and the pool has never looked better."),
]

REVIEWS_ON = bool(REVIEWS)
RATING_ON  = GOOGLE_RATING is not None and GOOGLE_REVIEW_COUNT is not None


def stars_svg(rating):
    """Row of 5 stars, filled to `rating` (halves rounded to nearest)."""
    full = int(round(float(rating)))
    out = []
    for i in range(5):
        fill = "#f5b301" if i < full else "none"
        out.append(f'<svg viewBox="0 0 24 24" fill="{fill}" stroke="#f5b301" stroke-width="1.5" aria-hidden="true"><polygon points="12 2 15 9 22 9.5 17 14.5 18.5 22 12 18 5.5 22 7 14.5 2 9.5 9 9"/></svg>')
    return f'<span class="rating-stars">{"".join(out)}</span>'


def rating_badge():
    if not RATING_ON:
        return ""
    href = GOOGLE_PROFILE_URL or "#"
    return (f'<a class="rating-badge" href="{href}" target="_blank" rel="noopener noreferrer">'
            f'{stars_svg(GOOGLE_RATING)}'
            f'<span><strong>{GOOGLE_RATING}</strong> &middot; {GOOGLE_REVIEW_COUNT} Google reviews</span></a>')


def review_card(r):
    loc = f' &middot; {r["location"]}' if r.get("location") else ""
    svc = f'<span class="review-svc">{r["service"]}</span>' if r.get("service") else ""
    return (f'    <figure class="review-card">\n'
            f'      {stars_svg(GOOGLE_RATING or 5)}\n'
            f'      <blockquote>{r["text"]}</blockquote>\n'
            f'      <figcaption>&mdash; {r["name"]}{loc}</figcaption>\n'
            f'      {svc}\n'
            f'    </figure>')


def reviews_section(service=None, limit=3):
    if not REVIEWS_ON:
        return ""
    picked = [r for r in REVIEWS if r.get("service") == service] if service else []
    if len(picked) < limit:
        picked += [r for r in REVIEWS if r not in picked]
    picked = picked[:limit]
    head_line = ""
    if RATING_ON:
        href = GOOGLE_PROFILE_URL or "#"
        head_line = (f'  <a class="reviews-rating" href="{href}" target="_blank" rel="noopener noreferrer">'
                     f'{stars_svg(GOOGLE_RATING)} <span><strong>{GOOGLE_RATING}</strong> from {GOOGLE_REVIEW_COUNT} Google reviews</span></a>')
    more = f'  <a class="reviews-more" href="/reviews/">Read more reviews</a>' if len(REVIEWS) > limit else ''
    return f"""<section class="reviews">
  <h2>What Our Customers Say</h2>
  <div class="section-sub">Real Reviews</div>
{head_line}
  <div class="reviews-grid">
{chr(10).join(review_card(r) for r in picked)}
  </div>
{more}
</section>
"""


def review_jsonld():
    """AggregateRating + Review array — only when we have a real rating AND reviews."""
    if not (RATING_ON and REVIEWS_ON):
        return ""
    revs = ",\n".join(
        '    { "@type": "Review", "author": { "@type": "Person", "name": "%s" }, '
        '"reviewRating": { "@type": "Rating", "ratingValue": "%s", "bestRating": "5" }, '
        '"reviewBody": %s }' % (r["name"], GOOGLE_RATING, _json_str(r["text"]))
        for r in REVIEWS[:8]
    )
    return (',\n  "aggregateRating": { "@type": "AggregateRating", "ratingValue": "%s", "reviewCount": "%s" },\n'
            '  "review": [\n%s\n  ]' % (GOOGLE_RATING, GOOGLE_REVIEW_COUNT, revs))


def _json_str(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"').replace('&mdash;', '—').replace('&amp;', '&') + '"'

# ----------------------------------------------------------------------------
# service order (drives cards, other-services, sitemap, footer nav)
# ----------------------------------------------------------------------------
ORDER = ['pool-cleaning','pool-openings','chemical-balancing','liner-installation',
         'spa-service','filter-maintenance','equipment-repair','pressure-washing',
         'pool-closings','leak-detection']

ICONS = {
 'pool-cleaning':'<path d="M12 2a10 10 0 1 0 0 20A10 10 0 0 0 12 2z"/><path d="M2 12h4M18 12h4M12 2v4M12 18v4"/>',
 'pool-openings':'<circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>',
 'chemical-balancing':'<path d="M9 3H5a2 2 0 0 0-2 2v4m6-6h10a2 2 0 0 1 2 2v4M9 3v18m0 0h10a2 2 0 0 0 2-2v-4M9 21H5a2 2 0 0 1-2-2v-4m0 0h18"/>',
 'liner-installation':'<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>',
 'spa-service':'<path d="M4 22h16a2 2 0 0 0 2-2v-6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2z"/><path d="M8 12V6a4 4 0 0 1 8 0v6"/>',
 'filter-maintenance':'<polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>',
 'equipment-repair':'<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
 'pressure-washing':'<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>',
 'pool-closings':'<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/>',
 'leak-detection':'<circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><path d="M11 8c-1 1.2-1.6 2.2-1.6 3A1.6 1.6 0 0 0 11 12.6 1.6 1.6 0 0 0 12.6 11c0-.8-.6-1.8-1.6-3z"/>',
}

CARD = {
 'pool-cleaning':('Pool Cleaning','Weekly service keeping your pool crystal clear all season long.'),
 'pool-openings':('Pool Openings','Green to clean &mdash; we get your pool swim-ready from start to finish.'),
 'chemical-balancing':('Chemical Balancing','Precise water chemistry testing and treatment every visit.'),
 'liner-installation':('Liner Installation','Full vinyl liner replacement &mdash; custom fit, professional install.'),
 'spa-service':('Spa Service','Weekly maintenance contracts for hot tubs and pool/spa combos.'),
 'filter-maintenance':('Filter Maintenance','Cartridge cleanings, sand changes, and full filter installs.'),
 'equipment-repair':('Equipment Repair &amp; Sales','Pumps, filters, heaters, salt cells &amp; full installs. All major brands.'),
 'pressure-washing':('Pressure Washing','Pool decks, driveways, sidewalks, brick, pavers and home exteriors.'),
 'pool-closings':('Pool Closings','Close it right. Dewinterize equipment, final clean, and cover installation.'),
 'leak-detection':('Leak Detection','We find where your pool is losing water &mdash; and fix it, no draining.'),
}

NAVLABEL = {
 'pool-cleaning':'Pool Cleaning','pool-openings':'Pool Openings','chemical-balancing':'Chemical Balancing',
 'liner-installation':'Liner Installation','spa-service':'Spa Service','filter-maintenance':'Filter Maintenance',
 'equipment-repair':'Equipment Repair & Sales','pressure-washing':'Pressure Washing',
 'pool-closings':'Pool Closings','leak-detection':'Leak Detection',
}

# ----------------------------------------------------------------------------
# shared chrome
# ----------------------------------------------------------------------------
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&family=Playfair+Display:ital,wght@0,700;0,900;1,700&display=swap" rel="stylesheet">'

FAVICON = (
 '<link rel="icon" href="/favicon.ico" sizes="any">'
 '<link rel="icon" type="image/png" sizes="32x32" href="/images/favicon-32.png">'
 '<link rel="icon" type="image/png" sizes="96x96" href="/images/favicon-96.png">'
 '<link rel="apple-touch-icon" href="/images/apple-touch-icon.png">'
)

def head(title, desc, canonical, og_image='/images/logo-badge-512.png', extra=''):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{_h.escape(desc, quote=True)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow">
<meta property="og:type" content="website">
<meta property="og:title" content="{_h.escape(title, quote=True)}">
<meta property="og:description" content="{_h.escape(desc, quote=True)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}{og_image}">
<meta property="og:site_name" content="Alabama Aquatics">
<meta name="twitter:card" content="summary">
{FAVICON}
{FONTS}
<link rel="stylesheet" href="/assets/site.css?v={CSS_VER}">
{extra}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
"""

def header():
    return f"""<nav class="site-nav">
  <a class="nav-logo" href="/" aria-label="Alabama Aquatics home"><img src="/images/logo-nav.png" alt="Alabama Aquatics" width="120" height="52"></a>
  <div class="nav-contact">
    <a class="nav-email" href="mailto:{EMAIL}" aria-label="Email Alabama Aquatics at {EMAIL}">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
      <span>{EMAIL}</span>
    </a>
    <a class="nav-phone" href="tel:{TEL}">{PHONE}</a>
  </div>
</nav>
<div class="trust-strip">
  <div class="trust-items">
    <span>Licensed &amp; Insured</span>
    <span>Weekly Service</span>
    <span>Greater Birmingham</span>
    <span>Locally Owned</span>
  </div>
  <div class="trust-social">
    <a href="{FB}" target="_blank" rel="noopener noreferrer" aria-label="Alabama Aquatics on Facebook">
      <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg>
    </a>
    <a href="{IG}" target="_blank" rel="noopener noreferrer" aria-label="Alabama Aquatics on Instagram">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>
    </a>
  </div>
</div>
"""

def footer():
    links = ''.join(f'<a href="/{s}/">{NAVLABEL[s]}</a>\n      ' for s in ORDER)
    pages = '<a href="/service-area/">Service Area</a>\n      <a href="/gallery/">Before &amp; After</a>\n      <a href="/faq/">FAQ</a>\n      <a href="/contact/">Contact</a>'
    if REVIEWS_ON or GOOGLE_PROFILE_URL:
        pages += '\n      <a href="/reviews/">Reviews</a>'
    return f"""<footer>
  <a class="footer-logo" href="/"><img src="/images/logo-nav.png" alt="Alabama Aquatics" width="102" height="44"></a>
  <p>&copy; 2026 Alabama Aquatics LLC &nbsp;&bull;&nbsp; Birmingham, Alabama &nbsp;&bull;&nbsp; {PHONE}</p>
  <nav class="footer-nav" aria-label="Services">
      {links}
  </nav>
  <nav class="footer-nav footer-nav-pages" aria-label="More">
      {pages}
  </nav>
  <div class="footer-social">
    <a href="{FB}" target="_blank" rel="noopener noreferrer">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="#3d6070"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg>
      Facebook
    </a>
    <a href="{IG}" target="_blank" rel="noopener noreferrer">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#3d6070" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>
      Instagram
    </a>
    <a href="mailto:{EMAIL}">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#3d6070" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
      {EMAIL}
    </a>
  </div>
</footer>
"""


def sticky_bar(quote_href="#quote"):
    return f"""<div class="sticky-bar">
  <a href="tel:{TEL}" aria-label="Call Alabama Aquatics">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13 1 .37 1.96.72 2.88a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.2-1.2a2 2 0 0 1 2.11-.45c.92.35 1.88.59 2.88.72A2 2 0 0 1 22 16.92z"/></svg>
    <span>Call</span>
  </a>
  <a href="sms:{SMS}" aria-label="Text Alabama Aquatics">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
    <span>Text</span>
  </a>
  <a href="{quote_href}" class="sticky-quote" aria-label="Request a quote">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
    <span>Free Quote</span>
  </a>
</div>
"""


def page_tail(quote_href="#quote", with_form_js=True):
    return footer() + sticky_bar(quote_href) + (FORM_JS if with_form_js else "") + "\n</body>\n</html>\n"


# ── credentials band (homepage) ──────────────────────────────────────────────
def credentials_band():
    items = [
        ("Licensed &amp; Insured", "Full liability coverage on every visit"),
        ("Locally Owned &amp; Operated", "Birmingham &amp; St. Clair County"),
        (f"Serving Since {FOUNDED_YEAR}", "Alabama Aquatics LLC"),
        ("Free Quotes", "Weekly or one-time"),
    ]
    cells = "\n".join(
        f'    <div class="cred-item"><strong>{t}</strong><span>{s}</span></div>'
        for t, s in items)
    return f"""<section class="credentials" aria-label="Why trust Alabama Aquatics">
  <div class="credentials-inner">
{cells}
  </div>
</section>
"""


# ── home / contact quote form ────────────────────────────────────────────────
SERVICE_OPTS = "\n".join(
    f'          <option value="{NAVLABEL[s]}">{NAVLABEL[s]}</option>' for s in ORDER)

def quote_form(form_name, heading, intro, submit="Get My Free Quote", hidden=None):
    hid = "".join(f'\n        <input type="hidden" name="{k}" value="{v}">' for k, v in (hidden or {}).items())
    return f"""<section class="quote-form-wrap" id="quote">
  <div class="quote-form-inner">
      <h2>{heading}</h2>
      <p>{intro}</p>
      <form class="qform" name="{form_name}" method="POST" data-netlify="true" netlify-honeypot="bot-field" onsubmit="handleSubmit(event, '{form_name}')">
        <input type="hidden" name="form-name" value="{form_name}">{hid}
        <p class="hp-field"><label>Leave this field empty: <input name="bot-field"></label></p>
        <input type="text" name="name" placeholder="Full Name" required autocomplete="name">
        <input type="tel" name="phone" placeholder="Phone Number" required autocomplete="tel">
        <input type="email" name="email" placeholder="Email (optional)" autocomplete="email">
        <input type="text" name="address" placeholder="Property Address or City" required autocomplete="street-address">
        <select name="service" class="qform-full" aria-label="What do you need?">
          <option value="">What do you need? (optional)</option>
{SERVICE_OPTS}
          <option value="Not sure">Not sure &mdash; help me figure it out</option>
        </select>
        <textarea name="notes" placeholder="Tell us about your pool (size, condition, anything else)" class="qform-full"></textarea>
        <div class="qform-radio-group">
          <div class="radio-label">Best way to reach you:</div>
          <div class="qform-radio-opts">
          <label class="qform-radio-opt"><input type="radio" name="contact" value="Call"> Call</label>
          <label class="qform-radio-opt"><input type="radio" name="contact" value="Text"> Text</label>
          <label class="qform-radio-opt"><input type="radio" name="contact" value="Email"> Email</label>
          </div>
        </div>
        <button type="submit" class="qform-submit">{submit}</button>
      </form>
      <div class="form-success" id="success-{form_name}">Thanks! We&apos;ll get back to you shortly &mdash; usually same day.</div>
  </div>
</section>
"""

FORM_JS = """<script>
function handleSubmit(event, formName) {
  event.preventDefault();
  var form = event.target;
  var data = new FormData(form);
  fetch('/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams(data).toString()
  }).then(function() {
    form.style.display = 'none';
    var success = document.getElementById('success-' + formName);
    if (success) success.style.display = 'block';
  }).catch(function() {
    window.location.href = 'tel:%s';
  });
}
</script>""" % TEL

# ===========================================================================
# PHASE 2 — how it works, FAQ, pricing, gallery, service-area / town pages
# ===========================================================================

# Flip SHOW_PRICING to True once the number is OK to publish.
SHOW_PRICING       = False
WEEKLY_PRICE       = 340   # $/month, standard weekly service (4 visits)
WEEKLY_VISIT_PRICE = 85

# ---- How it works -------------------------------------------------------------
def how_it_works():
    steps = [
        ("1", "Get a free quote", "Call, text, or send the form. Tell us about your pool and where you are &mdash; we&apos;ll come back to you the same day with pricing."),
        ("2", "We schedule your first visit", "Pick weekly service or a one-time clean. No long-term contract to get started, and no surprise charges."),
        ("3", "We handle it from there", "We show up on the same day every week &mdash; skim, brush, vacuum, balance the water, check the equipment &mdash; and flag anything that needs attention."),
    ]
    cells = "\n".join(
        f'    <div class="step"><span class="step-num">{n}</span><h3>{t}</h3><p>{d}</p></div>'
        for n, t, d in steps)
    return f"""<section class="how">
  <h2>How It Works</h2>
  <div class="section-sub">Getting Started Is Easy</div>
  <div class="how-grid">
{cells}
  </div>
</section>
"""

# ---- FAQ --------------------------------------------------------------------
FAQ_HOME = [
    ("Do I have to sign a long-term contract?",
     "No. Weekly service is a simple recurring agreement you can pause or cancel &mdash; we earn your business every week. We also do one-time cleanings and green-to-clean jobs with no commitment."),
    ("How much does weekly pool service cost?",
     "Most standard residential pools run about the same each month for weekly service, with chemicals included. Add-ons like specialty treatments or extra visits are billed as clear line items on the same monthly invoice. Send the form or call for an exact quote for your pool."),
    ("What&apos;s included in a weekly visit?",
     "Every visit: empty skimmer and pump baskets, brush walls, steps and tile line, skim and vacuum, test and balance the water, adjust chemical feeders, and inspect the pump, filter and plumbing. Standard chemicals are included."),
    ("How long does green-to-clean take?",
     "Most green pools clear up in about a week. We visit roughly three times that week, treating and vacuuming each time until the water is clear and swim-ready. Chemicals and vacuuming are included &mdash; no hidden charges for the work it takes."),
    ("Do you service above-ground pools?",
     "We focus on in-ground pools &mdash; liner, plaster and fiberglass. If you have an above-ground pool, give us a call and we&apos;ll point you in the right direction."),
    ("What areas do you serve?",
     "Greater Birmingham and St. Clair County &mdash; including Trussville, Springville, Odenville, Moody, Argo, Leeds, Pell City, Hoover, Vestavia Hills, Mountain Brook and Chelsea. Not sure if you&apos;re in range? Just ask."),
    ("Do I need to be home for service?",
     "No. As long as we can get to the equipment and the pool, we&apos;ll take care of everything and let you know if anything needs your attention."),
    ("Do you handle repairs and liner work too?",
     "Yes &mdash; pumps, filters, heaters, salt cells, chlorinators, full equipment installs, leak detection, underwater liner patching, and full vinyl liner replacement. Weekly service customers get priority scheduling."),
]

SERVICE_FAQ = {
 'pool-cleaning': [
    ("How often do you come?", "Once a week, on the same day, for standard weekly service. We can also set up bi-weekly or one-time visits."),
    ("Are chemicals included?", "Yes &mdash; standard sanitizer and balancing chemicals are included in weekly service. Specialty products are billed as line items so you always see what you paid for."),
    ("Do I need to be home?", "No. We just need access to the pool and equipment."),
 ],
 'pool-openings': [
    ("When should I open my pool?", "Most Alabama pools open in April or early May, once nighttime temps are consistently above the 60s. We can open earlier if you heat your pool."),
    ("My pool is green &mdash; is that extra?", "Green-to-clean is handled under our service agreement with chemicals and vacuuming included. If it needs more visits than expected we&apos;ll tell you, but there are no hidden charges."),
 ],
 'chemical-balancing': [
    ("Can you balance my water without full cleaning service?", "Yes. Our standalone chemical-check service keeps your water dialed in on a regular schedule &mdash; popular for covered pools in the off-season."),
    ("What do you test for?", "Free chlorine, pH, total alkalinity, calcium hardness, cyanuric acid, salt (for saltwater pools) and phosphates."),
 ],
 'liner-installation': [
    ("How long does a liner last?", "Usually 7 to 12 years. Fading, wrinkles, leaks at the seams or a bead that won&apos;t stay in the track are signs it&apos;s time."),
    ("Do you drain the pool?", "Yes, a full liner replacement requires draining. We remove the old liner, prep the floor and walls, fit and vacuum-set the new liner, cut in the fittings and refill."),
    ("Can I pick the pattern?", "Yes. You choose from current liner patterns before we order."),
 ],
 'spa-service': [
    ("Is spa service contract-only?", "Yes &mdash; spas need consistent weekly attention to stay clean and safe, so we offer it as a recurring maintenance agreement."),
    ("Chlorine or bromine?", "Either. We handle both, plus specialty spa chemicals like enzymes and clarifiers."),
 ],
 'filter-maintenance': [
    ("How often should a cartridge filter be cleaned?", "Every 4 to 6 months for most pools. We can put you on a schedule so it never gets missed."),
    ("How often do sand filters need new sand?", "Every 3 to 5 years. We handle the full change &mdash; drain, remove old sand, replace media, restart the system."),
 ],
 'equipment-repair': [
    ("What brands do you work on?", "All major brands &mdash; Hayward, Pentair and Jandy &mdash; for pumps, filters, heaters, salt cells and chlorinators."),
    ("Will you tell me the cost before you start?", "Yes. We diagnose the problem and walk you through what it needs before any work begins. No surprises."),
 ],
 'pressure-washing': [
    ("What surfaces do you clean?", "Pool decks, driveways, sidewalks, pavers, brick and natural stone, plus soft-wash for home exteriors. We tailor the pressure and solution to the material."),
    ("Do you pressure wash wood or vehicles?", "No &mdash; we don&apos;t service wood fences, wood decks or vehicles."),
 ],
 'pool-closings': [
    ("Do I have to close my pool for winter?", "Not necessarily. We recommend covering it and keeping equipment running to save on spring opening costs, but we&apos;ll winterize and dewinterize if you prefer."),
    ("I don&apos;t have a cover.", "We can supply one and install it as part of the closing."),
 ],
 'leak-detection': [
    ("How do I know if my pool is leaking?", "If you&apos;re losing more than about a quarter-inch a day, or adding water constantly, you likely have a leak."),
    ("Do you have to drain the pool to patch it?", "No. We locate the leak and patch the liner underwater with professional-grade vinyl patch material &mdash; usually in one visit."),
 ],
}

def faq_jsonld(items):
    if not items:
        return ""
    q = ",\n".join(
        '    { "@type": "Question", "name": %s, "acceptedAnswer": { "@type": "Answer", "text": %s } }'
        % (_json_str(_h.unescape(qq).replace('&apos;', "'")), _json_str(_h.unescape(aa).replace('&apos;', "'").replace('&mdash;','—')))
        for qq, aa in items)
    return f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
{q}
  ]
}}
</script>"""

def faq_block(items, heading="Frequently Asked Questions"):
    if not items:
        return ""
    rows = "\n".join(
        f'    <details class="faq-item"><summary>{qq}</summary><div>{aa}</div></details>'
        for qq, aa in items)
    return f"""<section class="faq">
  <h2>{heading}</h2>
  <div class="faq-list">
{rows}
  </div>
</section>
"""

# ---- Pricing --------------------------------------------------------------
def pricing_section():
    price = ""
    if SHOW_PRICING:
        price = f"""    <div class="price-figure">
      <span class="price-amt">${WEEKLY_PRICE}<span>/mo</span></span>
      <span class="price-note">Standard weekly service &mdash; 4 visits, chemicals included. Larger pools and add-ons quoted individually.</span>
    </div>
"""
    return f"""<section class="pricing">
  <h2>Straightforward Pricing</h2>
  <div class="section-sub">No Surprises</div>
{price}  <div class="pricing-points">
    <div><strong>One flat monthly rate</strong><span>Weekly service is billed once a month, with standard chemicals included.</span></div>
    <div><strong>Add-ons are line items</strong><span>Specialty chemicals or an extra visit show up itemized on the same invoice &mdash; you always see what you paid for.</span></div>
    <div><strong>No long-term contract</strong><span>Weekly service is month-to-month. One-time cleanings and green-to-clean have no commitment at all.</span></div>
  </div>
  <a class="btn-primary" href="/#quote">Get Your Exact Price</a>
</section>
"""

# ---- Before / After gallery --------------------------------------------------
GALLERY = [
    ("emilysbefore.jpg", "emilysafter.jpg", "Green to Clean", "A neglected pool brought back to crystal clear with our green-to-clean process."),
    ("donnasbefore.jpg", "donnasafter.jpg", "Green to Clean", "Same pool, one week apart &mdash; from swamp to swim-ready."),
]
GALLERY_SINGLES = [
    ("scottandginaperfect.jpg", "Weekly Service Results", "A weekly-service pool kept dialed in all season."),
    ("pooldeckclean.jpg", "Pressure Washing", "Pool deck before and after a pressure wash."),
    ("housewash.jpg", "Soft Wash", "House exterior soft-washed &mdash; no high pressure on siding."),
]

def gallery_strip():
    b, a, label, _ = GALLERY[0]
    b2, a2, label2, _ = GALLERY[1]
    return f"""<section class="gallery-strip">
  <h2>Real Pools, Real Results</h2>
  <div class="section-sub">Before &amp; After</div>
  <div class="ba-grid">
    <figure class="ba"><img src="/images/{b}" alt="Green pool before service" loading="lazy"><figcaption>Before</figcaption></figure>
    <figure class="ba"><img src="/images/{a}" alt="Clear pool after service" loading="lazy"><figcaption>After</figcaption></figure>
    <figure class="ba"><img src="/images/{b2}" alt="Green pool before service" loading="lazy"><figcaption>Before</figcaption></figure>
    <figure class="ba"><img src="/images/{a2}" alt="Clear pool after service" loading="lazy"><figcaption>After</figcaption></figure>
  </div>
  <a class="reviews-more" href="/gallery/">See more before &amp; afters</a>
</section>
"""

# ---- Service-area / towns ---------------------------------------------------
TOWNS = [
 ("trussville", "Trussville", "Jefferson &amp; St. Clair County",
  "Trussville sits right between our St. Clair County home base and Birmingham, so it&apos;s one of the first places we serve. Whether you&apos;re near the Mall, in Cahaba Project, or out toward the Pinchgut Creek side, we keep Trussville pools clean and balanced every week."),
 ("springville", "Springville", "St. Clair County",
  "Springville is home turf. We know the well water, the tree cover along US-11, and how quickly a pool here can turn green after a storm. Weekly service, openings, and green-to-clean throughout Springville and out toward Big Canoe Creek."),
 ("odenville", "Odenville", "St. Clair County",
  "Odenville and the St. Clair-Springville corridor are core to our route. Rural lots, lots of shade, and pools that need consistent attention &mdash; exactly what our weekly service is built for."),
 ("moody", "Moody", "St. Clair County",
  "We serve pools all over Moody, from the neighborhoods off Kerr Road to the properties near Moody Crossroads. Weekly cleaning, chemical balancing, equipment repair and liner work, close to home for us."),
 ("argo", "Argo", "St. Clair &amp; Jefferson County",
  "Argo straddles the county line just north of Trussville, and it&apos;s a quick stop on our regular route. Weekly pool service, openings and repairs for Argo homeowners."),
 ("leeds", "Leeds", "Jefferson &amp; St. Clair County",
  "From the neighborhoods near the Interstate to the quieter streets toward Moody, we keep Leeds pools swim-ready. Weekly service, green-to-clean, pressure washing and full repair work."),
 ("pell-city", "Pell City", "St. Clair County",
  "Pell City and the Logan Martin Lake area have a lot of pools working hard through a long Alabama summer. We handle weekly service, openings and closings, equipment repair and liner replacement across Pell City."),
 ("ashville", "Ashville", "St. Clair County",
  "Ashville is our county seat and part of our regular service area. If you&apos;re keeping a pool up here, we can keep it clean, balanced and running right, every week."),
 ("hoover", "Hoover", "Jefferson &amp; Shelby County",
  "Hoover has one of the highest concentrations of backyard pools in the metro. We provide weekly service, chemical balancing, equipment repair and pressure washing throughout Hoover, from Bluff Park to Ross Bridge to Trace Crossings."),
 ("vestavia-hills", "Vestavia Hills", "Jefferson County",
  "Vestavia Hills pools tend to be established, mature, and surrounded by trees &mdash; which means consistent skimming, brushing and chemistry really matter. That&apos;s our weekly service in a nutshell."),
 ("mountain-brook", "Mountain Brook", "Jefferson County",
  "Mountain Brook pools deserve a service that shows up on schedule and treats the property with care. We provide weekly maintenance, repairs, liner work and pressure washing across Mountain Brook, Crestline, and English Village."),
 ("chelsea", "Chelsea", "Shelby County",
  "Chelsea has grown fast and so has the number of pools out here. We serve the neighborhoods along Highway 280 and Chelsea Road with weekly service, openings, and full repair work."),
 ("pinson", "Pinson", "Jefferson County",
  "Pinson and Clay are a short hop from our route through Trussville. Weekly pool cleaning, green-to-clean, and equipment repair for the Pinson Valley area."),
 ("clay", "Clay", "Jefferson County",
  "We serve Clay pools alongside our Trussville and Pinson customers &mdash; weekly service, chemical balancing, openings and closings, and repairs."),
]

def town_jsonld(name, county, url):
    return f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "Swimming Pool Cleaning and Maintenance",
  "name": "Pool Service in {name}, AL &ndash; Alabama Aquatics",
  "url": "{url}",
  "areaServed": {{ "@type": "City", "name": "{name}", "containedInPlace": {{ "@type": "AdministrativeArea", "name": "{_h.unescape(county)}, Alabama" }} }},
  "provider": {{
    "@type": "LocalBusiness", "name": "Alabama Aquatics LLC",
    "telephone": "+1-205-810-6288", "email": "{EMAIL}", "url": "{BASE}/",
    "image": "{BASE}/images/logo-badge-512.png",
    "address": {{ "@type": "PostalAddress", "addressRegion": "AL", "addressCountry": "US" }},
    "sameAs": ["{FB}", "{IG}"]
  }}
}}
</script>"""

def service_area_section():
    links = "\n".join(
        f'    <a href="/pool-service-{slug}/">{name}</a>' for slug, name, _c, _b in TOWNS)
    return f"""<section class="service-area">
  <h2>Where We Work</h2>
  <div class="section-sub">Greater Birmingham &amp; St. Clair County</div>
  <div class="area-grid">
{links}
  </div>
  <a class="reviews-more" href="/service-area/">See our full service area</a>
</section>
"""

# ----------------------------------------------------------------------------
# form field helpers
# ----------------------------------------------------------------------------
def contact_block():
    return """        <input type="text" name="name" placeholder="Full Name" required autocomplete="name">
        <input type="tel" name="phone" placeholder="Phone Number" required autocomplete="tel">
        <input type="email" name="email" placeholder="Email Address" required autocomplete="email">
        <input type="text" name="address" placeholder="Property Address" required autocomplete="street-address" class="qform-full">
"""

def radio(label, name, opts):
    o = '\n'.join(f'          <label class="qform-radio-opt"><input type="radio" name="{name}" value="{v}"> {v}</label>' for v in opts)
    return f"""        <div class="qform-radio-group">
          <div class="radio-label">{label}</div>
          <div class="qform-radio-opts">
{o}
          </div>
        </div>
"""

SURFACE = radio('Pool Surface:', 'pool-surface', ['Liner','Plaster','Fiberglass'])
SYSTEM  = radio('System:', 'system', ['Chlorine','Salt'])
WATER   = radio('Water:', 'water', ['Clear','Cloudy','Green'])
CONTACT = radio('Contact Preference:', 'contact', ['Call','Text','Email'])

def check(name, cid, label):
    return f"""        <div class="qform-check-group qform-full">
          <input type="checkbox" name="{name}" id="{cid}" value="Yes">
          <label for="{cid}">{label}</label>
        </div>
"""

def textarea(name, ph, required=False, minh=None):
    r = ' required' if required else ''
    st = f' style="min-height:{minh}px;"' if minh else ''
    return f'        <textarea name="{name}" placeholder="{ph}" class="qform-full"{st}{r}></textarea>\n'

def size_input():
    return '        <input type="text" name="size" placeholder="Approximate Pool Size (optional)" class="qform-full">\n'

def build_form(slug, intro, fields):
    return f"""<section class="quote-form-wrap" id="quote">
  <div class="quote-form-inner">
      <h2>Get a Quote</h2>
      <p>{intro}</p>
      <form class="qform" name="{slug}" method="POST" data-netlify="true" netlify-honeypot="bot-field" onsubmit="handleSubmit(event, '{slug}')">
        <input type="hidden" name="form-name" value="{slug}">
        <p class="hp-field"><label>Leave this field empty: <input name="bot-field"></label></p>
{fields}        <button type="submit" class="qform-submit">Request a Quote</button>
      </form>
      <div class="form-success" id="success-{slug}">Thank you! We&apos;ll be in touch shortly.</div>
  </div>
</section>
"""

# ----------------------------------------------------------------------------
# per-service content
# ----------------------------------------------------------------------------
S = {}

S['pool-cleaning'] = dict(
  title="Weekly Pool Cleaning Service in Birmingham, AL | Alabama Aquatics",
  desc="Weekly pool cleaning service for the Greater Birmingham area. Skimming, brushing, vacuuming, chemical balancing and equipment checks every visit. Licensed & insured.",
  eyebrow="Weekly Service Contracts &bull; Greater Birmingham",
  h1="Keep Your Pool Clean, Safe, and Ready to Swim",
  lede="Our weekly pool service contract takes the work off your hands entirely. We show up on a consistent schedule so you never have to wonder if your pool is ready &mdash; it just is.",
  body="""      <img src="/images/JANEDOE.jpg" alt="Clean backyard pool serviced by Alabama Aquatics" class="photo" style="object-position:center 70%;" loading="lazy" onerror="this.style.display='none'">
      <p>At Alabama Aquatics, our weekly pool service contract takes the work off your hands entirely. We show up on a consistent schedule so you never have to wonder if your pool is ready &mdash; it just is.</p>
      <h2>What We Do Every Visit</h2>
      <ul>
        <li><strong>Empty skimmer and pump baskets</strong> &mdash; keeping water flowing freely through your equipment</li>
        <li><strong>Backwash filter</strong> &mdash; flushing out built-up debris to maintain proper filtration</li>
        <li><strong>Brush walls, steps, and tile line</strong> &mdash; preventing algae from taking hold between visits</li>
        <li><strong>Rake and skim the surface</strong> &mdash; removing leaves, insects, and floating debris</li>
        <li><strong>Vacuum the pool floor</strong> &mdash; clearing settled debris for a clean, clear bottom</li>
        <li><strong>Test and balance water chemistry</strong> &mdash; adjusting chlorine, pH, alkalinity, and other levels to keep your water safe and comfortable</li>
        <li><strong>Inspect equipment</strong> &mdash; every visit we check your pump, filter, and plumbing for leaks, unusual sounds, or anything not operating as it should</li>
        <li><strong>Check and record water level</strong> &mdash; noting any significant drops that could indicate a leak and topping off as needed</li>
        <li><strong>Adjust chemical feeders</strong> &mdash; tab floaters and salt cell output settings kept dialed in</li>
        <li><strong>Flag any visible damage</strong> &mdash; cracks, loose fittings, or deteriorating equipment are documented and reported to you immediately</li>
      </ul>""",
  form=build_form('pool-cleaning',
     "Every pool is different. Fill out the form below and we&apos;ll get back to you shortly.",
     contact_block()+SURFACE+SYSTEM+size_input()+WATER
       +check('spa','spa-pc','Do you have a spa or hot tub that also needs serviced?')
       +CONTACT+textarea('notes',"Anything else you'd like us to know?")),
)

S['pool-openings'] = dict(
  title="Pool Opening & Green-to-Clean Service in Birmingham, AL | Alabama Aquatics",
  desc="Seasonal pool openings for Greater Birmingham. Cover removal, equipment dewinterizing and our Green to Clean process until your water is completely swim ready.",
  eyebrow="Green to Clean &bull; Greater Birmingham",
  h1="Swim Ready From Start to Finish",
  lede="When it&apos;s time to open your pool for the season, Alabama Aquatics handles everything &mdash; from pulling the cover to the moment you jump in.",
  body="""      <div class="photo-pair">
        <img src="/images/emilysbefore.jpg" alt="Green pool before opening service" loading="lazy" onerror="this.style.display='none'">
        <img src="/images/emilysafter.jpg" alt="Clear pool after Green to Clean service" loading="lazy" onerror="this.style.display='none'">
      </div>
      <p>When it's time to open your pool for the season, Alabama Aquatics handles everything &mdash; so you don't have to lift a finger. From pulling the cover to the moment you jump in, we take care of it all.</p>
      <h2>What Our Pool Opening Includes</h2>
      <p>Every pool opening starts with the basics &mdash; removing and storing your cover, dewinterizing your equipment, and inspecting everything to make sure it's operating correctly heading into the season. From there we test your water for all possible contaminants that may have accumulated over the winter and take every necessary step to get it clear, balanced, and safe to swim in.</p>
      <h2>The Green to Clean Process</h2>
      <p>Once your equipment is dewinterized and your pool is uncovered, we move forward with our Green to Clean service agreement. Alabama Aquatics will visit your pool approximately 3 days per week, treating and balancing the water on each visit until it is completely clear and swim ready. We don't stop until the job is done. If your pool requires more visits than originally agreed upon, we will notify you &mdash; but we keep coming until your water is perfect.</p>
      <p>Every Green to Clean visit includes chemicals, vacuuming, and all necessary treatments. There are no surprises and no hidden charges for the work required to get your pool where it needs to be.</p>""",
  form=build_form('pool-openings',
     "Fill out the form below and we&apos;ll get back to you shortly.",
     contact_block()+SURFACE+SYSTEM+size_input()+WATER+CONTACT
       +textarea('notes',"Anything else you'd like us to know?")),
)

S['chemical-balancing'] = dict(
  title="Pool Chemical Balancing & Water Testing in Birmingham, AL | Alabama Aquatics",
  desc="Professional pool water chemistry testing and balancing in Greater Birmingham. Chlorine, pH, alkalinity, calcium, stabilizer and salt dialed in on every visit.",
  eyebrow="Water Chemistry &bull; Chemical Check Service",
  h1="Properly Balanced Water. Every Time.",
  lede="Balanced water protects your equipment, extends the life of your pool surface, and keeps your family safe. We take the guesswork out of it entirely.",
  body="""      <img src="/images/scottandginaperfect.jpg" alt="Crystal clear balanced pool" class="photo" loading="lazy" onerror="this.style.display='none'">
      <p>Keeping your pool water chemically balanced isn't just about keeping it clear &mdash; it protects your equipment, extends the life of your pool surface, and most importantly keeps your family safe. At Alabama Aquatics we take the guesswork out of it entirely.</p>
      <h2>What We Test and Adjust Every Visit</h2>
      <ul>
        <li><strong>Free Chlorine</strong> &mdash; the active sanitizer that kills bacteria and algae. Too low and your pool becomes unsafe. Too high and it irritates eyes and skin.</li>
        <li><strong>pH</strong> &mdash; the most important number in pool chemistry. A proper pH (7.2&ndash;7.6) keeps chlorine effective, protects your equipment, and makes the water comfortable to swim in.</li>
        <li><strong>Total Alkalinity</strong> &mdash; acts as a buffer for pH, preventing it from swinging up or down rapidly. Getting this right makes everything else easier to maintain.</li>
        <li><strong>Calcium Hardness</strong> &mdash; too low and water becomes aggressive, slowly eating away at your plaster, grout, and metal fittings. Too high and you get scaling and cloudy water.</li>
        <li><strong>Cyanuric Acid (Stabilizer)</strong> &mdash; protects chlorine from being destroyed by UV rays. Critical for outdoor pools. Without it you're burning through chlorine rapidly.</li>
        <li><strong>Salt Level</strong> &mdash; for saltwater pools, keeping salt within the proper range ensures your salt cell runs efficiently and produces the right amount of chlorine.</li>
        <li><strong>Phosphates</strong> &mdash; a food source for algae. Elevated phosphate levels make it much harder to keep a pool clear even with proper chlorine levels.</li>
      </ul>
      <h2>Chemical Check Service</h2>
      <p>Especially popular for pools that are covered during the cooler months, our standalone chemical check service keeps your water properly balanced on a regular schedule without the full cleaning service.</p>
      <ul>
        <li><strong>Pools covered for winter</strong> &mdash; water chemistry still matters even under a cover. Staying on top of it throughout the winter saves significantly on chemicals, labor, and the time it takes to get the water back clear when pool opening season comes around.</li>
        <li><strong>Heated pools that stay open year-round</strong> &mdash; you're still swimming, the water still needs to be balanced, and a chemical check keeps everything dialed in through the cooler months.</li>
        <li><strong>Customers who handle their own cleaning</strong> but want a professional eye on the chemistry.</li>
      </ul>""",
  form=build_form('chemical-balancing',
     "Fill out the form below and we&apos;ll get back to you shortly.",
     contact_block()+SURFACE+SYSTEM+size_input()+WATER
       +check('spa','spa-cb','Do you have a spa or hot tub that also needs serviced?')
       +CONTACT+textarea('notes',"Anything else you'd like us to know?")),
)

S['liner-installation'] = dict(
  title="Vinyl Pool Liner Installation & Replacement in Birmingham, AL | Alabama Aquatics",
  desc="New vinyl pool liner installation and replacement in Greater Birmingham. Custom-fit liners, professional measuring, full install and refill. Licensed & insured.",
  eyebrow="New Vinyl Liners &bull; Custom Fit &bull; Full Install",
  h1="A New Liner Makes an Old Pool Look Brand New",
  lede="When your vinyl liner is faded, wrinkled, leaking, or just worn out, Alabama Aquatics handles the full replacement &mdash; measured, ordered, and installed start to finish.",
  body="""      <img src="/images/poollinerinstall.jpg" alt="Technician installing a new vinyl pool liner" class="photo" loading="lazy" onerror="this.style.display='none'">
      <p>A vinyl liner is what holds your water and gives your pool its finished look. Most liners last somewhere between 7 and 12 years before the vinyl gets brittle, stained, stretched, or starts leaking at the seams. Once it reaches that point, patching is only a short-term fix &mdash; a full replacement is the right call, and it makes a tired old pool look completely new.</p>
      <h2>Signs It&apos;s Time for a New Liner</h2>
      <ul>
        <li><strong>Fading and staining</strong> &mdash; the pattern has washed out or the liner has turned chalky and rough to the touch</li>
        <li><strong>Wrinkles on the floor</strong> &mdash; the liner has stretched and no longer sits tight against the pool</li>
        <li><strong>Slipping out of the track</strong> &mdash; the top bead keeps pulling loose from the coping</li>
        <li><strong>Leaks and water loss</strong> &mdash; you&apos;re adding water constantly and patches aren&apos;t holding</li>
        <li><strong>Brittle or torn vinyl</strong> &mdash; the material cracks or tears when handled, especially around fittings and steps</li>
      </ul>
      <h2>How the Installation Works</h2>
      <p>We start by measuring your pool &mdash; every wall, the floor slope, steps, and every fitting &mdash; so your new liner is built to spec. You choose your liner pattern, we place the order, and once it arrives we schedule the install.</p>
      <ul>
        <li><strong>Drain and remove the old liner</strong> &mdash; the pool is pumped down and the worn liner is taken out</li>
        <li><strong>Inspect and prep the shell</strong> &mdash; we check the floor and walls, smooth out and repair any bad spots, and treat for anything that could telegraph through the new vinyl</li>
        <li><strong>Hang and set the new liner</strong> &mdash; the liner is fitted into the track and vacuum-set so it pulls tight into every corner with no wrinkles</li>
        <li><strong>Cut in the fittings</strong> &mdash; skimmer, returns, main drain, lights and steps are sealed with new gaskets and faceplates</li>
        <li><strong>Fill and balance</strong> &mdash; we refill the pool, bring the water chemistry to swim-ready, and make sure the equipment is running properly before we leave</li>
      </ul>
      <p>Not sure whether your liner needs replacing or just a repair? We&apos;re also happy to take a look &mdash; if a patch or re-track will get you through the season, we&apos;ll tell you. Learn more about our <a class="inline-link" href="/leak-detection/">leak detection &amp; patching service</a>.</p>""",
  form=build_form('liner-installation',
     "Tell us about your pool and we&apos;ll get back to you with next steps.",
     contact_block()+SURFACE
       +'        <input type="text" name="size" placeholder="Pool Size / Dimensions (if known)" class="qform-full">\n'
       +radio('Approximate Liner Age:', 'liner-age', ['Under 5 yrs','5-10 yrs','10+ yrs','Not sure'])
       +radio('Reason for Inquiry:', 'reason', ['Leaking','Worn / faded','Wrinkled','Remodel','Not sure'])
       +CONTACT
       +textarea('notes',"Describe what's going on with your current liner.", minh=100)),
)

S['spa-service'] = dict(
  title="Hot Tub & Spa Maintenance Service in Birmingham, AL | Alabama Aquatics",
  desc="Weekly hot tub and spa maintenance contracts in Greater Birmingham for standalone spas and pool/spa combos. Brushing, chemical balancing and filter cleaning included.",
  eyebrow="Weekly Maintenance Contracts &bull; Standalone Spas &amp; Pool/Spa Combos",
  h1="Your Spa Should Be Perfect Every Time You Step In",
  lede="A spa needs consistent, specialized care to stay clean and safe. We offer weekly spa maintenance contracts for both standalone spas and pool/spa combos.",
  body="""      <img src="/images/hottub.jpg" alt="Hot tub spa serviced by Alabama Aquatics" class="photo" style="object-position:center bottom;" loading="lazy" onerror="this.style.display='none'">
      <p>A spa requires consistent, specialized care to stay clean, safe, and ready to use. At Alabama Aquatics we offer weekly spa maintenance contracts for both standalone spas and pool/spa combos &mdash; keeping your water crystal clear and your surfaces clean every single week.</p>
      <h2>What We Do Every Visit</h2>
      <ul>
        <li><strong>Debris removal</strong> &mdash; clearing out anything that has made its way into your spa since the last visit</li>
        <li><strong>Full surface brush down</strong> &mdash; walls and surfaces are brushed on every visit to prevent slime and biofilm buildup before it starts</li>
        <li><strong>Water testing and chemical balancing</strong> &mdash; we test and handle all chemical needs on every visit, including specialty spa chemicals such as enzyme treatments and clarifiers. Whether your spa runs on chlorine or bromine, we have you covered.</li>
        <li><strong>Filter cleaning every 2 weeks</strong> &mdash; included at no additional charge for all spa maintenance customers. <a class="inline-link" href="/filter-maintenance">Learn more about our Filter Maintenance service.</a></li>
      </ul>
      <h2>Repairs</h2>
      <p>Spa maintenance customers have access to our repair services for common spa issues. If something isn't working correctly we'll assess the situation and do our best to get it taken care of.</p>
      <h2>Spa Maintenance is Contract Only</h2>
      <p>Alabama Aquatics spa service is available exclusively as a recurring maintenance contract. This ensures your spa gets the consistent attention it needs to stay in peak condition year round.</p>""",
  form=build_form('spa-service',
     "Fill out the form below and we&apos;ll get back to you shortly.",
     contact_block()
       +radio('Spa Type:', 'spa-type', ['Standalone Spa','Pool/Spa Combo'])
       +WATER+CONTACT+textarea('notes',"Anything else you'd like us to know?")),
)

S['filter-maintenance'] = dict(
  title="Pool Filter Cleaning, Sand Changes & Installs in Birmingham, AL | Alabama Aquatics",
  desc="Cartridge filter cleaning, sand filter media changes and full filter installations in Greater Birmingham. All major brands. Keep your water clear and equipment healthy.",
  eyebrow="Cartridge Cleanings &bull; Sand Changes &bull; Full Installs",
  h1="Clean Filters. Better Water. Longer Equipment Life.",
  lede="Your filter is the difference between clear water and a losing battle. We handle cartridge cleanings, sand changes, and full filter upgrades.",
  body="""      <h2>Cartridge Filter Cleaning</h2>
      <img src="/images/cartridge-cleaning.jpg" alt="Pool cartridge filter before and after cleaning" class="photo" loading="lazy" onerror="this.style.display='none'">
      <p>Cartridge filters are one of the most common and effective filtration systems on the market, but they require regular cleaning to perform correctly. Over time they accumulate oils, calcium deposits, and debris that restrict water flow and reduce their ability to filter effectively.</p>
      <p>At Alabama Aquatics we clean cartridge filters using water and a specially formulated solution designed to break down all built-up residue while conditioning the filter material to protect it for future use. Most cartridge filters should be cleaned every 4 to 6 months &mdash; and we are happy to put you on a regular schedule so it never gets overlooked.</p>
      <p><strong>Spa customers receive complimentary cartridge filter cleanings every 2 weeks</strong> as part of their service. <a class="inline-link" href="/spa-service">Learn more about our Spa Service.</a></p>
      <h2>Sand Filter Changes</h2>
      <img src="/images/pentair-sand-dollar.jpg" alt="Pentair Sand Dollar pool filter" class="photo photo-contain" loading="lazy" onerror="this.style.display='none'">
      <p>Sand filters are incredibly durable and low maintenance &mdash; but the sand inside doesn't last forever. Over time the sand becomes coated and worn down, losing its ability to trap debris and properly filter your water. Most sand filters need a full sand change every 3 to 5 years.</p>
      <p>Alabama Aquatics handles the complete sand change process from start to finish &mdash; draining, removing the old sand, replacing it with fresh filter media, and getting your system back up and running properly.</p>
      <h2>Filter Installs and Upgrades</h2>
      <p>Looking to upgrade your filtration system to something higher performance? Alabama Aquatics installs filters from all major brands and will help you find the right system for your pool size, usage, and budget. Whether you're replacing an aging unit or upgrading for the first time, we'll handle the full installation and make sure everything is running correctly before we leave.</p>""",
  form=build_form('filter-maintenance',
     "Fill out the form below and we&apos;ll get back to you shortly.",
     contact_block()+SURFACE+WATER+CONTACT
       +textarea('notes',"Anything else you'd like us to know?")),
)

S['equipment-repair'] = dict(
  title="Pool Equipment Repair & Installation in Birmingham, AL | Alabama Aquatics",
  desc="Pool pump, filter, heater, salt cell and chlorinator repair and installation in Greater Birmingham. Hayward, Pentair and Jandy. Diagnosis before any work begins.",
  eyebrow="Diagnosis &bull; Repairs &bull; Full Installs &bull; All Major Brands",
  h1="When Something&apos;s Wrong, We&apos;ll Figure It Out",
  lede="Pool equipment problems don't fix themselves. We come out, diagnose exactly what's going wrong, and walk you through the fix before any work begins.",
  body="""      <img src="/images/equipment.webp" alt="Pool equipment pad with pump and filter" class="photo" loading="lazy" onerror="this.style.display='none'">
      <p>Pool equipment problems don't fix themselves &mdash; and the longer they go unaddressed the more damage they can cause. Alabama Aquatics will come out to your property, diagnose exactly what's going wrong, and walk you through what needs to be done before any work begins. No surprises.</p>
      <h2>What We Work On</h2>
      <ul>
        <li><strong>Pumps</strong> &mdash; the heart of your pool system. If it's not circulating properly, nothing else works right.</li>
        <li><strong>Filters</strong> &mdash; cartridge, sand, and DE filters repaired or replaced</li>
        <li><strong>Heaters</strong> &mdash; keeping your water at the perfect temperature all season long</li>
        <li><strong>Salt Cells</strong> &mdash; the engine behind your saltwater chlorination system</li>
        <li><strong>Chlorinators</strong> &mdash; automatic chemical feeders repaired and replaced</li>
        <li><strong>Full Equipment Installs</strong> &mdash; new equipment pad builds and complete system replacements</li>
      </ul>
      <p>We carry and install all major brands including <strong>Hayward, Pentair, and Jandy</strong>.</p>
      <h2>Considering an Upgrade?</h2>
      <p><strong>Salt Cell</strong> &mdash; If you're still manually adding chlorine to your pool, a salt cell changes everything. Instead of buying and handling chlorine products regularly, your pool generates its own chlorine automatically from a small amount of dissolved salt. The water feels softer, your eyes and skin thank you, and the long term cost savings are significant.</p>
      <p><strong>Heater</strong> &mdash; Alabama summers are long but they don't last forever. A pool heater extends your swim season well into the fall and lets you get in the water earlier in the spring. In Alabama's climate a heater can add 2 to 3 months of comfortable swimming to your year. Once you have one you'll wonder how you lived without it.</p>""",
  form=build_form('equipment-repair',
     "Fill out the form below and we&apos;ll get back to you shortly.",
     contact_block()+CONTACT
       +textarea('issue',"Please describe the equipment issue or service you are inquiring about.", required=True, minh=110)),
)

S['pressure-washing'] = dict(
  title="Pressure Washing & Soft Wash in Birmingham, AL | Alabama Aquatics",
  desc="Pool deck, driveway, sidewalk, paver and house soft-wash pressure washing in Greater Birmingham. Pressure and solution tailored to each surface. Licensed & insured.",
  eyebrow="Pool Decks &bull; Driveways &bull; Home Exteriors &bull; Pavers",
  h1="A Clean Pool Deserves a Clean Property",
  lede="The surfaces around your pool matter just as much as the water. From your deck to your driveway to your home exterior, we bring the same attention to detail to every surface.",
  body="""      <div class="photo-pair">
        <img src="/images/pooldeckclean.jpg" alt="Pool deck before and after pressure washing" loading="lazy" onerror="this.style.display='none'">
        <img src="/images/housewash.jpg" alt="House exterior before and after soft washing" loading="lazy" onerror="this.style.display='none'">
      </div>
      <p>At Alabama Aquatics we know that a beautiful pool is only part of the picture. The surfaces surrounding it matter just as much. From your pool deck to your driveway to the exterior of your home itself, we bring the same attention to detail to every surface we touch &mdash; and the results are instant.</p>
      <h2>What We Clean</h2>
      <ul>
        <li><strong>Pool Decks</strong> &mdash; concrete, pavers, brick, and natural stone cleaned safely and effectively without damaging the surface</li>
        <li><strong>Driveways and Sidewalks</strong> &mdash; years of buildup, algae, and staining removed in a single visit</li>
        <li><strong>Home Exteriors</strong> &mdash; vinyl siding, brick, and stucco treated with a specially formulated soft wash solution calculated specifically for your home's material and the severity of dirt and algae buildup. We never use high pressure on a home.</li>
        <li><strong>Pavers, Brick, and Natural Stone</strong> &mdash; cleaned with the appropriate pressure and technique for the material, restoring color and curb appeal without causing damage</li>
      </ul>
      <img src="/images/sidewalkclean.jpg" alt="Sidewalk before and after pressure washing" class="photo" loading="lazy" onerror="this.style.display='none'">
      <h2>Our Approach</h2>
      <p>Not every surface is the same and not every surface should be treated the same way. Alabama Aquatics specifically tailors the pressure and cleaning solution to the material being cleaned. This protects your property while delivering results that can instantly bring a surface back to life.</p>
      <p>Please note &mdash; we do not offer pressure washing services for vehicles, wood fences, or wood decks.</p>""",
  form=build_form('pressure-washing',
     "Fill out the form below and we&apos;ll get back to you shortly.",
     contact_block()+CONTACT
       +textarea('surfaces',"What surfaces do you need cleaned?", required=True)
       +textarea('notes',"Anything else you'd like us to know?")),
)

S['pool-closings'] = dict(
  title="Pool Closing & Winterization Service in Birmingham, AL | Alabama Aquatics",
  desc="End-of-season pool closings in Greater Birmingham. Final clean, line blow-out, equipment winterizing and cover installation. Covers supplied if you need one.",
  eyebrow="End of Season &bull; Equipment Dewinterize &bull; Cover Installation",
  h1="Close It Right. Open It Easy.",
  lede="A proper pool closing protects your investment, preserves your equipment, and sets you up for a smooth, affordable opening when warm weather returns.",
  body="""      <img src="/images/poolcover.jpg" alt="Pool covered for winter" class="photo" style="object-position:center 60%;" loading="lazy" onerror="this.style.display='none'">
      <p>Unfortunately pool season comes to an end at some point &mdash; but even when the fun is over, Alabama Aquatics has got you covered. A proper pool closing protects your investment, preserves your equipment, and sets you up for a smooth, affordable opening when warm weather returns.</p>
      <h2>What Our Pool Closing Includes</h2>
      <p>Every Alabama Aquatics pool closing starts with a final thorough cleaning of your pool before we put it to bed for the season. From there we blow out the lines, winterize your equipment, and secure your cover to protect everything through the colder months.</p>
      <p>Don't have a cover? No problem &mdash; Alabama Aquatics can supply one for you.</p>
      <h2>Our Recommendation</h2>
      <p>We strongly recommend all of our customers cover their pools and keep their equipment running through the winter. Doing so prevents major chemical buildup, algae growth, and debris accumulation that leads to expensive, time-consuming openings come spring. That said, we always respect our customers' decisions &mdash; if you prefer to dewinterize your equipment rather than keep it running, we will handle that as well.</p>""",
  form=build_form('pool-closings',
     "Fill out the form below and we&apos;ll get back to you shortly.",
     contact_block()+SURFACE+size_input()+CONTACT
       +textarea('notes',"Anything else you'd like us to know?")),
)

S['leak-detection'] = dict(
  title="Pool Leak Detection & Vinyl Liner Patching in Birmingham, AL | Alabama Aquatics",
  desc="Pool leak detection and underwater vinyl liner patching in Greater Birmingham. We find the leak and patch it in one visit \u2014 no draining, no refilling. Sagging liner re-tracks too.",
  eyebrow="Leak Location &bull; Underwater Patching &bull; No Draining Required",
  h1="Losing Water? We\u2019ll Find the Leak and Patch It.",
  lede="A slow leak wastes thousands of gallons and drives your chemical costs up. We track down where your vinyl liner is leaking and patch it underwater &mdash; usually in a single visit, with no need to drain the pool.",
  body="""      <p>If your pool is dropping more than about a quarter-inch a day, you likely have a leak &mdash; and a slow one can waste thousands of gallons and throw your water chemistry off all season. Alabama Aquatics tracks down where the water is going and fixes it on-site, usually in one visit.</p>
      <h2>Leak Detection</h2>
      <p>We work through the pool systematically &mdash; skimmers, returns, main drain, fittings, steps, and the liner surface itself &mdash; to pin down exactly where the leak is. No guesswork and no tearing things apart.</p>
      <h2>Underwater Patching</h2>
      <p>Once we find it, we patch the liner underwater with professional-grade vinyl patch material. No draining, no refilling, no water bill. Most patches are done in a single visit and hold for the life of the liner.</p>
      <h2>Sagging Liner Re-Track</h2>
      <p>While we're there: if your liner has pulled away from the coping track and is hanging into the water, we re-seat it by hand &mdash; restoring a clean, secure fit along the top edge.</p>
      <p>If the liner is brittle, badly faded, or leaking in several spots at once, patching may only buy you a season. In that case we'll walk you through a <a class="inline-link" href="/liner-installation/">full liner replacement</a> instead.</p>""",
  form=build_form('leak-detection',
     "Tell us what&apos;s going on and we&apos;ll get back to you shortly.",
     contact_block()+SURFACE
       +textarea('issue',"Describe the issue -- leak, sagging liner, location, how long it's been going on, etc.", required=True, minh=110)
       +CONTACT),
)

# ----------------------------------------------------------------------------
# assemble service pages
# ----------------------------------------------------------------------------
def other_services(active):
    tiles = []
    for s in ORDER:
        if s == active:
            tiles.append(f'    <span class="current" aria-current="page">{NAVLABEL[s]}</span>')
        else:
            tiles.append(f'    <a href="/{s}/">{NAVLABEL[s]}</a>')
    items = '\n'.join(tiles) + '\n'
    return f"""<section class="other-services">
  <h2>Explore Our Services</h2>
  <div class="section-sub">What We Do</div>
  <div class="other-grid">
{items}  </div>
</section>
"""

CTA = f"""<section class="cta">
  <h2>Ready to Get Started?</h2>
  <p>Serving Greater Birmingham &mdash; St. Clair, Jefferson &amp; Shelby County</p>
  <a href="tel:{TEL}">Call {PHONE}</a>
</section>
"""

def service_jsonld(slug, d):
    name = NAVLABEL[slug]
    url = f"{BASE}/{slug}/"
    return f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "{name}",
  "name": "{name} \\u2013 Alabama Aquatics",
  "description": "{_h.escape(d['desc'], quote=True)}",
  "url": "{url}",
  "areaServed": {{ "@type": "AdministrativeArea", "name": "Greater Birmingham, Alabama (St. Clair, Jefferson & Shelby County)" }},
  "provider": {{
    "@type": "LocalBusiness",
    "name": "Alabama Aquatics LLC",
    "telephone": "+1-205-810-6288",
    "email": "{EMAIL}",
    "url": "{BASE}/",
    "image": "{BASE}/images/logo-badge-512.png",
    "areaServed": "Greater Birmingham, AL",
    "address": {{ "@type": "PostalAddress", "addressLocality": "Birmingham", "addressRegion": "AL", "addressCountry": "US" }},
    "sameAs": ["{FB}", "{IG}"]
  }}
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "{BASE}/" }},
    {{ "@type": "ListItem", "position": 2, "name": "{name}", "item": "{url}" }}
  ]
}}
</script>"""

def build_service_page(slug):
    d = S[slug]
    url = f"{BASE}/{slug}/"
    faqs = SERVICE_FAQ.get(slug, [])
    doc = head(d['title'], d['desc'].replace('&amp;','&'), url,
               extra=service_jsonld(slug, d) + faq_jsonld(faqs))
    doc += header()
    doc += f"""<main id="main">
  <nav class="breadcrumb" aria-label="Breadcrumb">
    <a href="/">Home</a> &nbsp;/&nbsp; <span>{NAVLABEL[slug]}</span>
  </nav>
  <header class="service-hero">
    <p class="eyebrow">{d['eyebrow']}</p>
    <h1>{d['h1']}</h1>
    <p class="lede">{d['lede']}</p>
    <a class="hero-cta" href="#quote">Request a Quote</a>
  </header>
  <article class="service-content">
{d['body']}
  </article>
  {d['form']}
  {faq_block(faqs)}
  {reviews_section(NAVLABEL[slug])}
  {other_services(slug)}
  {CTA}
</main>
"""
    doc += page_tail(quote_href="#quote")
    doc = add_asset_versions(doc)
    folder = os.path.join(OUT, slug)
    os.makedirs(folder, exist_ok=True)
    open(os.path.join(folder, 'index.html'), 'w', encoding='utf-8').write(doc)
    print('wrote', slug + '/index.html', len(doc))

for slug in ORDER:
    build_service_page(slug)

# ----------------------------------------------------------------------------
# HOME PAGE
# ----------------------------------------------------------------------------
def home_cards():
    out = []
    for s in ORDER:
        t, sub = CARD[s]
        out.append(f"""    <a class="service-card" href="/{s}/">
      <div class="service-icon">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#5dade2" stroke-width="2">{ICONS[s]}</svg>
      </div>
      <h3>{t}</h3>
      <p>{sub}</p>
    </a>""")
    return '\n\n'.join(out)

HOME_JSONLD = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "{BASE}/#business",
  "name": "Alabama Aquatics LLC",
  "description": "Professional pool service, cleaning, repair and pressure washing serving the Greater Birmingham, Alabama area.",
  "url": "{BASE}/",
  "telephone": "+1-205-810-6288",
  "email": "{EMAIL}",
  "image": "{BASE}/images/logo-badge-512.png",
  "logo": "{BASE}/images/logo-badge-512.png",
  "priceRange": "$$",
  "address": {{ "@type": "PostalAddress", "addressLocality": "Birmingham", "addressRegion": "AL", "addressCountry": "US" }},
  "areaServed": [
    {{ "@type": "AdministrativeArea", "name": "St. Clair County, Alabama" }},
    {{ "@type": "AdministrativeArea", "name": "Jefferson County, Alabama" }},
    {{ "@type": "AdministrativeArea", "name": "Shelby County, Alabama" }}
  ],
  "sameAs": ["{FB}", "{IG}"],
  "hasOfferCatalog": {{
    "@type": "OfferCatalog",
    "name": "Pool Services",
    "itemListElement": [
""" + ",\n".join(
      f'      {{ "@type": "Offer", "itemOffered": {{ "@type": "Service", "name": "{NAVLABEL[s]}", "url": "{BASE}/{s}/" }} }}'
      for s in ORDER
) + """
    ]
  }""" + review_jsonld() + """
}
</script>"""

home = head(
  "Alabama Aquatics | Professional Pool Service",
  "Professional pool service, cleaning, chemical balancing, equipment repair and pressure washing for the Greater Birmingham, Alabama area. Licensed, insured, and built on integrity.",
  f"{BASE}/",
  extra=HOME_JSONLD + faq_jsonld(FAQ_HOME),
)
home += header()
home += f"""<main id="main">
<section class="hero">
  <div class="hero-bubbles" aria-hidden="true">
    <div class="bubble" style="width:190px;height:190px;bottom:-55px;left:-35px;"></div>
    <div class="bubble" style="width:64px;height:64px;top:27%;left:9%;"></div>
    <div class="bubble" style="width:26px;height:26px;top:17%;left:19%;"></div>
    <div class="bubble" style="width:225px;height:225px;top:-65px;right:-55px;"></div>
    <div class="bubble" style="width:82px;height:82px;top:33%;right:8%;"></div>
    <div class="bubble" style="width:20px;height:20px;top:60%;right:21%;"></div>
    <div class="bubble" style="width:40px;height:40px;bottom:14%;left:26%;"></div>
  </div>
  <div class="hero-sub">Weekly Pool Service &bull; Greater Birmingham &amp; St. Clair County</div>
  <img class="hero-logo" src="/images/logo-hero.png" alt="Alabama Aquatics" width="440" height="201">
  <h1>Owning the Pool Should Be the Fun Part</h1>
  <p class="hero-lede">We handle the cleaning, chemical balancing, repairs, liner work and pressure washing &mdash; weekly or one-time &mdash; for homeowners across Greater Birmingham and St.&nbsp;Clair County. Licensed, insured, and locally owned.</p>
  <div class="hero-cta-row">
    <a class="btn-primary" href="#quote">Get a Free Quote</a>
    <a class="btn-secondary" href="tel:{TEL}">Call {PHONE}</a>
  </div>
  {rating_badge()}
</section>

{credentials_band()}

{quote_form('home-quote', 'Get a Free Quote', 'Tell us a little about your pool and we&apos;ll get right back to you &mdash; usually the same day.')}

<section class="services">
  <h2>Our Services</h2>
  <div class="section-sub">What We Do</div>
  <div class="services-grid">

{home_cards()}

  </div>
</section>

{how_it_works()}

{gallery_strip()}

{reviews_section()}

{pricing_section()}

{service_area_section()}

<section class="why">
  <h2>Why Choose Us</h2>
  <div class="section-sub">The Alabama Aquatics Difference</div>
  <div class="why-grid">
    <div class="why-item">
      <div class="why-icon">&#x1F6E1;&#xFE0F;</div>
      <h4>Licensed &amp; Insured</h4>
      <p>Full liability coverage so you can have peace of mind on every visit.</p>
    </div>
    <div class="why-item">
      <div class="why-icon">&#x1F4CD;</div>
      <h4>Local &amp; Reliable</h4>
      <p>Birmingham-based and owner-operated with a commitment to showing up every time.</p>
    </div>
    <div class="why-item">
      <div class="why-icon">&#x1F4CB;</div>
      <h4>Weekly Contracts</h4>
      <p>We show up every week, on schedule &mdash; so your pool is always clean and ready.</p>
    </div>
    <div class="why-item">
      <div class="why-icon">&#x26A1;</div>
      <h4>Pro Equipment</h4>
      <p>Professional-grade equipment for a deep, thorough clean every visit.</p>
    </div>
  </div>
</section>

{faq_block(FAQ_HOME, "Common Questions")}

<section class="cta">
  <h2>Ready for a Cleaner Pool?</h2>
  <p>Serving Greater Birmingham &mdash; St. Clair, Jefferson &amp; Shelby County</p>
  <a href="tel:{TEL}">Call {PHONE}</a>
</section>
</main>
"""
home += page_tail(quote_href="#quote")
home = add_asset_versions(home)
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(home)
print('wrote index.html', len(home))

# ----------------------------------------------------------------------------
# sitemap.xml, robots.txt, _redirects
# ----------------------------------------------------------------------------
from datetime import date
today = date.today().isoformat()
urls = ([f"{BASE}/"] + [f"{BASE}/{s}/" for s in ORDER]
        + [f"{BASE}/service-area/", f"{BASE}/faq/", f"{BASE}/gallery/", f"{BASE}/contact/"]
        + [f"{BASE}/pool-service-{slug}/" for slug, _n, _c, _b in TOWNS])
if REVIEWS or GOOGLE_PROFILE_URL:
    urls.append(f"{BASE}/reviews/")
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in urls:
    pr = '1.0' if u.endswith('/') and u.count('/') == 3 else '0.8'
    sm += f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>{pr}</priority>\n  </url>\n"
sm += '</urlset>\n'
open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf-8').write(sm)

open(os.path.join(OUT, 'robots.txt'), 'w', encoding='utf-8').write(
  f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")

open(os.path.join(OUT, '_redirects'), 'w', encoding='utf-8').write(
  "# Netlify redirects\n"
  "/chemical-delivery    /liner-installation/   301\n"
  "/chemical-delivery/   /liner-installation/   301\n"
  "/liner-repairs        /leak-detection/       301\n"
  "/liner-repairs/       /leak-detection/       301\n")

# ----------------------------------------------------------------------------
# 404 page
# ----------------------------------------------------------------------------
nf = head("Page Not Found | Alabama Aquatics",
          "The page you were looking for could not be found.",
          f"{BASE}/404", extra='<meta name="robots" content="noindex">')
nf += header()
nf += f"""<main id="main">
  <header class="service-hero">
    <p class="eyebrow">404 &mdash; Page Not Found</p>
    <h1>We Couldn&apos;t Find That Page</h1>
    <p class="lede">The page may have moved. Head back to our homepage or pick a service below &mdash; or just give us a call.</p>
    <a class="hero-cta" href="tel:{TEL}">Call {PHONE}</a>
  </header>
  {other_services('')}
</main>
"""
nf += page_tail(quote_href="/#quote", with_form_js=False)
open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8').write(add_asset_versions(nf))

# ----------------------------------------------------------------------------
# /contact/  and  /reviews/
# ----------------------------------------------------------------------------
def _write(rel_dir, doc):
    d = os.path.join(OUT, rel_dir)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(add_asset_versions(doc))
    print('wrote', rel_dir + '/index.html', len(doc))

# ---- Contact ----
c = head("Contact Alabama Aquatics | Pool Service in Greater Birmingham, AL",
         "Contact Alabama Aquatics for pool cleaning, repairs, liner work and pressure washing in Greater Birmingham and St. Clair County. Call, text, or request a free quote.",
         f"{BASE}/contact/")
c += header()
c += f"""<main id="main">
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a> &nbsp;/&nbsp; <span>Contact</span></nav>
  <header class="service-hero">
    <p class="eyebrow">Get In Touch</p>
    <h1>Contact Alabama Aquatics</h1>
    <p class="lede">Call or text for the fastest response, or send the form below and we&apos;ll get right back to you &mdash; usually the same day.</p>
  </header>
  <section class="contact-cols">
    <div class="contact-details">
      <h2>Reach Us</h2>
      <ul class="contact-list">
        <li><span class="cl-label">Phone</span><a href="tel:{TEL}">{PHONE}</a></li>
        <li><span class="cl-label">Text</span><a href="sms:{SMS}">{PHONE}</a></li>
        <li><span class="cl-label">Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><span class="cl-label">Hours</span><span>{HOURS}</span></li>
        <li><span class="cl-label">Area</span><span>Greater Birmingham &mdash; St. Clair, Jefferson &amp; Shelby County (Trussville, Springville, Odenville, Moody, Leeds, Hoover, Vestavia Hills, Mountain Brook and nearby)</span></li>
      </ul>
      <div class="contact-social">
        <a href="{FB}" target="_blank" rel="noopener noreferrer">Facebook</a>
        <a href="{IG}" target="_blank" rel="noopener noreferrer">Instagram</a>
      </div>
    </div>
    <div class="contact-form-col">
      {quote_form('contact', 'Request a Free Quote', 'Every pool is different. Give us the basics and we&apos;ll follow up with next steps.', submit='Send')}
    </div>
  </section>
  {reviews_section()}
  {CTA}
</main>
"""
c += page_tail(quote_href="#quote")
_write('contact', c)

# ---- Reviews (only if there is something real to show) ----
if REVIEWS_ON or GOOGLE_PROFILE_URL:
    rv = head("Customer Reviews | Alabama Aquatics Pool Service",
              "Reviews from Alabama Aquatics pool service customers across Greater Birmingham and St. Clair County.",
              f"{BASE}/reviews/",
              extra=(f'<script type="application/ld+json">\n{{\n  "@context":"https://schema.org","@type":"LocalBusiness","name":"Alabama Aquatics LLC","url":"{BASE}/"'
                     + review_jsonld() + '\n}\n</script>' if (RATING_ON and REVIEWS_ON) else ''))
    rv += header()
    summary = ""
    if RATING_ON:
        href = GOOGLE_PROFILE_URL or "#"
        summary = f'<a class="reviews-rating" href="{href}" target="_blank" rel="noopener noreferrer">{stars_svg(GOOGLE_RATING)} <span><strong>{GOOGLE_RATING}</strong> from {GOOGLE_REVIEW_COUNT} Google reviews</span></a>'
    cards = "\n".join(review_card(r) for r in REVIEWS) if REVIEWS_ON else '  <p style="text-align:center;color:var(--slate);">Reviews are on the way &mdash; be our first!</p>'
    leave = f'<a class="btn-primary" href="{GOOGLE_PROFILE_URL}" target="_blank" rel="noopener noreferrer">Leave Us a Review on Google</a>' if GOOGLE_PROFILE_URL else ''
    rv += f"""<main id="main">
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a> &nbsp;/&nbsp; <span>Reviews</span></nav>
  <header class="service-hero">
    <p class="eyebrow">Customer Reviews</p>
    <h1>What Our Customers Say</h1>
    {summary}
  </header>
  <section class="reviews reviews-page">
    <div class="reviews-grid">
{cards}
    </div>
    <div style="text-align:center;margin-top:2.5rem;">{leave}</div>
  </section>
  {CTA}
</main>
"""
    rv += page_tail(quote_href="/#quote", with_form_js=False)
    _write('reviews', rv)

# ---- FAQ page ----
fq_extra = faq_jsonld(FAQ_HOME + [q for lst in SERVICE_FAQ.values() for q in lst][:6])
f = head("Pool Service FAQ | Alabama Aquatics",
         "Answers to common questions about pool cleaning, pricing, contracts, green-to-clean, liner work and service areas in Greater Birmingham and St. Clair County.",
         f"{BASE}/faq/", extra=fq_extra)
f += header()
f += f"""<main id="main">
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a> &nbsp;/&nbsp; <span>FAQ</span></nav>
  <header class="service-hero">
    <p class="eyebrow">Good Questions</p>
    <h1>Pool Service FAQ</h1>
    <p class="lede">The things people ask us most. Don&apos;t see your question? Call or text {PHONE} and we&apos;ll answer it straight.</p>
  </header>
  {faq_block(FAQ_HOME, "General")}
  {faq_block([q for s in ('pool-cleaning','pool-openings','liner-installation','leak-detection','equipment-repair') for q in SERVICE_FAQ.get(s, [])], "By Service")}
  {CTA}
</main>
"""
f += page_tail(quote_href="/#quote", with_form_js=False)
_write('faq', f)

# ---- Gallery page ----
def ba_pair(b, a, label, caption):
    return f"""    <figure class="ba-card">
      <div class="ba-pair">
        <div><img src="/images/{b}" alt="{label} &ndash; before" loading="lazy"><span>Before</span></div>
        <div><img src="/images/{a}" alt="{label} &ndash; after" loading="lazy"><span>After</span></div>
      </div>
      <figcaption><strong>{label}</strong> &mdash; {caption}</figcaption>
    </figure>"""
def ba_single(img, label, caption):
    return f"""    <figure class="ba-card ba-single">
      <img src="/images/{img}" alt="{label}" loading="lazy">
      <figcaption><strong>{label}</strong> &mdash; {caption}</figcaption>
    </figure>"""
g = head("Before &amp; After Gallery | Alabama Aquatics Pool Service",
         "Before and after photos of real pools serviced by Alabama Aquatics &mdash; green-to-clean transformations, weekly service results and pressure washing across Greater Birmingham.",
         f"{BASE}/gallery/")
g += header()
g += f"""<main id="main">
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a> &nbsp;/&nbsp; <span>Before &amp; After</span></nav>
  <header class="service-hero">
    <p class="eyebrow">Real Pools, Real Results</p>
    <h1>Before &amp; After</h1>
    <p class="lede">These are actual customer pools &mdash; no stock photos. Green-to-clean jobs, weekly-service results, and pressure washing around the property.</p>
  </header>
  <section class="gallery-page">
{chr(10).join(ba_pair(*x) for x in GALLERY)}
{chr(10).join(ba_single(*x) for x in GALLERY_SINGLES)}
  </section>
  {CTA}
</main>
"""
g += page_tail(quote_href="/#quote", with_form_js=False)
_write('gallery', g)

# ---- Service Area hub ----
sa_cards = "\n".join(
    f'''    <a class="area-card" href="/pool-service-{slug}/">
      <strong>{name}</strong><span>{county}</span>
    </a>''' for slug, name, county, _b in TOWNS)
sa = head("Pool Service Area | Greater Birmingham &amp; St. Clair County, AL | Alabama Aquatics",
          "Alabama Aquatics provides weekly pool service, repairs and pressure washing across St. Clair County and Greater Birmingham &mdash; Trussville, Springville, Odenville, Moody, Hoover, Vestavia Hills and more.",
          f"{BASE}/service-area/")
sa += header()
sa += f"""<main id="main">
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a> &nbsp;/&nbsp; <span>Service Area</span></nav>
  <header class="service-hero">
    <p class="eyebrow">Where We Work</p>
    <h1>Our Service Area</h1>
    <p class="lede">We&apos;re based in St. Clair County and run regular routes across Greater Birmingham. If your town is on this list &mdash; or right next to one &mdash; we can help. Not sure? Just ask.</p>
  </header>
  <section class="area-hub">
{sa_cards}
  </section>
  {CTA}
</main>
"""
sa += page_tail(quote_href="/#quote", with_form_js=False)
_write('service-area', sa)

# ---- Town pages ----
def build_town_page(slug, name, county, blurb):
    url = f"{BASE}/pool-service-{slug}/"
    svc_links = " &bull; ".join(
        f'<a class="inline-link" href="/{s}/">{NAVLABEL[s]}</a>' for s in
        ('pool-cleaning','pool-openings','chemical-balancing','equipment-repair','liner-installation','pressure-washing'))
    t_faq = [
        (f"Do you really serve {name}?",
         f"Yes &mdash; {name} ({_h.unescape(county)}) is part of our regular route. We provide weekly pool service, one-time cleanings, green-to-clean, equipment repair and liner work here."),
        ("How do I get started?",
         f"Call or text {PHONE}, or send the form on this page. We&apos;ll give you a same-day quote for your {name} pool."),
        ("Is there a contract?",
         "No long-term contract for weekly service &mdash; it&apos;s month-to-month. One-time work has no commitment at all."),
    ]
    tform = quote_form('area-quote', f'Get a Free Quote in {name}',
                       'Tell us about your pool and we&apos;ll get right back to you with pricing.',
                       submit='Get My Free Quote', hidden={'area': name})
    doc = head(
        f"Pool Service in {name}, AL | Cleaning, Repairs &amp; More | Alabama Aquatics",
        f"Weekly pool cleaning, chemical balancing, green-to-clean, equipment repair, liner installation and pressure washing in {name}, Alabama. Licensed, insured, locally owned. Free quotes.",
        url, extra=town_jsonld(name, county, url) + faq_jsonld(t_faq))
    doc += header()
    doc += f"""<main id="main">
  <nav class="breadcrumb" aria-label="Breadcrumb">
    <a href="/">Home</a> &nbsp;/&nbsp; <a href="/service-area/">Service Area</a> &nbsp;/&nbsp; <span>{name}</span>
  </nav>
  <header class="service-hero">
    <p class="eyebrow">{_h.unescape(county)}</p>
    <h1>Pool Service in {name}, Alabama</h1>
    <p class="lede">{blurb}</p>
    <a class="hero-cta" href="#quote">Get a Free {name} Quote</a>
  </header>
  <article class="service-content">
    <h2>What We Do in {name}</h2>
    <p>Alabama Aquatics provides full pool care for {name} homeowners: {svc_links}, plus <a class="inline-link" href="/spa-service/">spa service</a>, <a class="inline-link" href="/filter-maintenance/">filter maintenance</a>, <a class="inline-link" href="/pool-closings/">closings</a> and <a class="inline-link" href="/leak-detection/">leak detection</a>. Most customers are on weekly service &mdash; same day every week, chemicals included, no long-term contract.</p>
    <p>We&apos;re licensed, insured and locally owned, and we treat your property like it&apos;s our own. If your {name} pool has gone green, we&apos;ll get it clear; if the equipment&apos;s down, we&apos;ll diagnose it before any work starts.</p>
  </article>
  {tform}
  {faq_block(t_faq, f'{name} Pool Service &mdash; FAQ')}
  {other_services(None)}
  {CTA}
</main>
"""
    doc += page_tail(quote_href="#quote")
    _write(f'pool-service-{slug}', doc)

for slug, name, county, blurb in TOWNS:
    build_town_page(slug, name, county, blurb)

print('wrote faq, gallery, service-area,', len(TOWNS), 'town pages')
print('wrote sitemap.xml, robots.txt, _redirects, 404.html')
print('DONE')
