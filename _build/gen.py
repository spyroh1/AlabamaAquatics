# -*- coding: utf-8 -*-
import os, html as _h

import pathlib
# repo root = parent of the _build/ folder this script lives in
OUT = str(pathlib.Path(__file__).resolve().parent.parent)
BASE = 'https://alabamaaquatics.com'
PHONE = '205-810-6288'
TEL = '2058106288'
EMAIL = 'contact@alabamaaquatics.com'
FB = 'https://www.facebook.com/profile.php?id=61574288617629'
IG = 'https://www.instagram.com/alabamaaquatics/'

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
<link rel="stylesheet" href="/assets/site.css">
{extra}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
"""

def header():
    return f"""<nav class="site-nav">
  <a class="nav-logo" href="/" aria-label="Alabama Aquatics home"><img src="/images/logo-nav.png" alt="Alabama Aquatics" width="120" height="52"></a>
  <a class="nav-phone" href="tel:{TEL}">{PHONE}</a>
</nav>
<div class="trust-strip">
  <span>Licensed &amp; Insured</span>
  <span>Weekly Service</span>
  <span>Greater Birmingham</span>
  <span>Locally Owned</span>
</div>
"""

def footer():
    links = ''.join(f'<a href="/{s}/">{NAVLABEL[s]}</a>\n      ' for s in ORDER)
    return f"""<footer>
  <a class="footer-logo" href="/"><img src="/images/logo-nav.png" alt="Alabama Aquatics" width="102" height="44"></a>
  <p>&copy; 2026 Alabama Aquatics LLC &nbsp;&bull;&nbsp; Birmingham, Alabama &nbsp;&bull;&nbsp; {PHONE}</p>
  <nav class="footer-nav" aria-label="Services">
      {links}
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
    doc = head(d['title'], d['desc'].replace('&amp;','&'), url, extra=service_jsonld(slug, d))
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
  {other_services(slug)}
  {CTA}
</main>
"""
    doc += footer()
    doc += FORM_JS + "\n</body>\n</html>\n"
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
  }
}
</script>"""

home = head(
  "Alabama Aquatics | Professional Pool Service",
  "Professional pool service, cleaning, chemical balancing, equipment repair and pressure washing for the Greater Birmingham, Alabama area. Licensed, insured, and built on integrity.",
  f"{BASE}/",
  extra=HOME_JSONLD,
)
home += header()
home += f"""<main id="main">
<h1 class="visually-hidden">Alabama Aquatics &mdash; Professional Pool Service, Repair &amp; Pressure Washing in Greater Birmingham, Alabama</h1>
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
  <div class="hero-sub">Professional Pool Service</div>
  <img class="hero-logo" src="/images/logo-hero.png" alt="Alabama Aquatics" width="460" height="220">
  <div class="divider"><div class="dl"></div><div class="dd"></div><div class="dl"></div></div>
  <p>Professional pool service and pressure washing for the Greater Birmingham area. Licensed, insured, and built on integrity.</p>
  <a class="hero-btn" href="tel:{TEL}">Call Us Today &mdash; {PHONE}</a>
  <img class="hero-badge" src="/images/badge.png" alt="" width="100" height="100">
</section>

<section class="services">
  <h2>Our Services</h2>
  <div class="section-sub">What We Do</div>
  <div class="services-grid">

{home_cards()}

  </div>
</section>

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

<section class="cta">
  <h2>Ready for a Cleaner Pool?</h2>
  <p>Serving Greater Birmingham &mdash; St. Clair, Jefferson &amp; Shelby County</p>
  <a href="tel:{TEL}">Call {PHONE}</a>
</section>
</main>
"""
home += footer()
home += "\n</body>\n</html>\n"
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(home)
print('wrote index.html', len(home))

# ----------------------------------------------------------------------------
# sitemap.xml, robots.txt, _redirects
# ----------------------------------------------------------------------------
from datetime import date
today = date.today().isoformat()
urls = [f"{BASE}/"] + [f"{BASE}/{s}/" for s in ORDER]
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
nf += footer() + "\n</body>\n</html>\n"
open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8').write(nf)

print('wrote sitemap.xml, robots.txt, _redirects, 404.html')
print('DONE')
