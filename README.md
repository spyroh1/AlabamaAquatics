# Alabama Aquatics — alabamaaquatics.com

Static marketing site for Alabama Aquatics LLC. No framework, no build step.
Hosted on Netlify, auto-deployed from the `main` branch of this repo.

## Structure

```
index.html              Home page
404.html                Custom not-found page
<service>/index.html    One folder per service = one clean URL
                        (pool-cleaning, pool-openings, chemical-balancing,
                         liner-installation, spa-service, filter-maintenance,
                         equipment-repair, pressure-washing, pool-closings,
                         liner-repairs)
assets/site.css         Shared stylesheet for every page
images/                 All photos + logos + favicons
sitemap.xml             Listed URLs for search engines
robots.txt              Points crawlers at the sitemap
_redirects              Netlify redirects (old /chemical-delivery -> /liner-installation)
netlify.toml            Deploy + cache config
_build/gen.py           Page generator (see below)
```

## Making changes

**Text / content on a service page:** edit `_build/gen.py` (the copy for each
service lives in the `S = { ... }` dictionary), then regenerate:

```
python _build/gen.py
```

That rewrites every `*.html` file so the shared header, footer, nav and
"other services" list stay in sync. Commit the regenerated HTML.

**Styling:** edit `assets/site.css` directly.

**Images:** drop the file in `images/` and reference it as `/images/<name>`.
Keep photos under ~1400px wide and compressed.

**A one-off HTML tweak** can also just be edited directly in the `.html` file —
but if you later run the generator it will overwrite that change, so prefer
editing `_build/gen.py`.

## Deploying

Push to `main`. Netlify builds and publishes in ~30 seconds. That's it.

```
git add -A
git commit -m "describe the change"
git push
```

## Forms

Quote forms are Netlify Forms. Each service page has one form; the form name
matches the folder (e.g. `pool-cleaning`, `liner-installation`). Submissions
show up under **Forms** in the Netlify dashboard — set up notification emails
there.

## Business info (single source of truth: `_build/gen.py`)

- Phone: 205-810-6288
- Email: contact@alabamaaquatics.com
- Service area: Greater Birmingham — St. Clair, Jefferson & Shelby County
- Facebook: https://www.facebook.com/profile.php?id=61574288617629
- Instagram: https://www.instagram.com/alabamaaquatics/
