# Alabama Aquatics — alabamaaquatics.com

Static marketing site for Alabama Aquatics LLC. No framework, no build step.
Hosted on Netlify, auto-deployed from the `main` branch of this repo.

## Structure

```
index.html              Home page
404.html                Custom not-found page
contact/index.html      Contact page (details + quote form)
reviews/index.html      Reviews page — only generated once REVIEWS is populated
<service>/index.html    One folder per service = one clean URL
                        (pool-cleaning, pool-openings, chemical-balancing,
                         liner-installation, spa-service, filter-maintenance,
                         equipment-repair, pressure-washing, pool-closings,
                         leak-detection)
assets/site.css         Shared stylesheet for every page
images/                 All photos + logos + favicons
sitemap.xml             Listed URLs for search engines
robots.txt              Points crawlers at the sitemap
_redirects              Netlify redirects (/chemical-delivery, /liner-repairs)
netlify.toml            Deploy + cache config
_build/gen.py           Page generator (see below)
```

## Turning on reviews

Near the top of `_build/gen.py` there is a config block. Fill it in and
regenerate — until then, nothing review-related renders (no placeholder
content ships):

```python
GOOGLE_PROFILE_URL  = "https://g.page/r/..."   # your "write a review" link
GOOGLE_RATING       = 4.9
GOOGLE_REVIEW_COUNT = 27
REVIEWS = [
    dict(name="Jane D.", location="Trussville", service="Weekly Pool Cleaning",
         text="Real text copied from an actual Google review."),
    ...
]
```

Setting these activates: the hero rating badge, a reviews section on the
homepage + each service page, the `/reviews/` page, footer link, sitemap
entry, and `AggregateRating` + `Review` schema. Use **real** reviews only.

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

Push to `main`. Netlify (project `quiet-centaur-dea036`, team "Alabama Aquatics",
Free plan) builds and publishes in ~30 seconds.

```
git add -A
git commit -m "describe the change"
git push
```

### Commit author rules (important — Free plan restriction)

Netlify's Free plan **blocks builds from unrecognized Git contributors**. For a
push to actually deploy, every commit must:

- be authored as **`Alabama Aquatics <contact@alabamaaquatics.com>`**
  (this repo's `.git/config` is already set to this; a fresh clone must run
  `git config user.email contact@alabamaaquatics.com`)
- contain **no `Co-Authored-By:` trailer** (a second author email that Netlify
  doesn't recognize will block the whole build)

If a push doesn't deploy, this is almost always why — check `git log -1 --format='%ae%n%(trailers)'`.

### Manual deploy (fallback)

If Git deploys ever break, deploy the folder straight to Netlify with an API token:

```
# zip the site (forward-slash paths), then:
curl -X POST "https://api.netlify.com/api/v1/sites/abf362b6-5e07-4d76-af85-cd1e4531ef18/deploys" \
  -H "Authorization: Bearer $NETLIFY_TOKEN" \
  -H "Content-Type: application/zip" \
  --data-binary @site.zip
```

Site ID: `abf362b6-5e07-4d76-af85-cd1e4531ef18`. Token: Netlify → User settings →
Applications → Personal access tokens.

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
