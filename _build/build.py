# -*- coding: utf-8 -*-
"""Bouwt de statische site van Tandartspraktijk Slotplantsoen.

Gebruik (vanuit de projectmap):  python -I _build/build.py
Alle pagina's, sitemap.xml en robots.txt worden opnieuw geschreven.
De URL-structuur volgt de oude WordPress-site, zodat bestaande Google-posities behouden blijven.
"""
import json
import os
import posixpath
import re
import sys
from datetime import date
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from content import TEAM, TREATMENTS, T  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://praktijkslotplantsoen.nl/"
TODAY = date.today().isoformat()
NAME = "Tandartspraktijk Slotplantsoen"
TEL = "0522-247436"
TEL_HREF = "tel:+31522247436"
MAIL = "info@praktijkslotplantsoen.nl"
INSTA = "https://www.instagram.com/tandartspraktijkslotplantsoen/"
CID = int("0x291e114ff302f1d2", 16)
MAPS = f"https://www.google.com/maps?cid={CID}"
MAP_EMBED = "https://www.google.com/maps?q=Tandartspraktijk+Slotplantsoen,+Slotplantsoen+1a,+7941+LP+Meppel&output=embed"
ROUTE = "https://www.google.com/maps/dir/?api=1&destination=Tandartspraktijk+Slotplantsoen+Slotplantsoen+1a+7941+LP+Meppel"

TMAP = {t[0]: t for t in TREATMENTS}

# Demo-build (bv. GitHub Pages): SLOT_DEMO=1 zet noindex op elke pagina zodat de demo niet concurreert met de echte site;
# SLOT_BASE is het pad waaronder de site draait (voor de 404-pagina), bv. /tandartspraktijk-slotplantsoen/
DEMO = os.environ.get("SLOT_DEMO") == "1"
SITE_BASE = os.environ.get("SLOT_BASE", "/")


def _v(path):
    import hashlib
    return hashlib.md5((ROOT / path).read_bytes()).hexdigest()[:8]


CSS_V = _v("assets/css/style.css")
JS_V = _v("assets/js/main.js")

PRAKTIJK = [
    ("homepage/praktijkinformatie/", "Over de praktijk"),
    ("homepage/ons-team/", "Ons team"),
    ("cbct-rontgen/", "CBCT-scan (3D-röntgen)"),
    ("kinderen-en-de-tandarts/", "Kinderen en de tandarts"),
    ("angst-voor-de-tandarts/", "Angst voor de tandarts"),
    ("vacatures/", "Vacatures"),
]
INFO = [
    ("homepage/spoedgevallen-en-weekenddienst/", "Spoed en weekenddienst"),
    ("homepage/tarieven-en-betaling/", "Tarieven en betaling"),
    ("homepage/betalen-en-vergoedingen/", "Verzekering en vergoedingen"),
    ("homepage/huisregels/", "Huisregels"),
    ("doorverwijzing-cbct-scan-voor-behandelaars/", "Voor verwijzers (CBCT)"),
]

HOURS_ROWS = [
    (1, "Maandag", "08:00-12:30 en 13:15-20:00"),
    (2, "Dinsdag", "08:00-12:30 en 13:15-16:45"),
    (3, "Woensdag", "08:00-12:30 en 13:15-16:45"),
    (4, "Donderdag", "08:00-12:30 en 13:15-16:45"),
    (5, "Vrijdag", None),
    (6, "Zaterdag", None),
    (0, "Zondag", None),
]

# ---------------------------------------------------------------- helpers

def rel(cur, target):
    """Relatieve link van pagina-map `cur` naar `target` (map met / of bestand)."""
    is_dir = target == "" or target.endswith("/")
    t = target.rstrip("/") or "."
    c = cur.rstrip("/") or "."
    r = posixpath.relpath(t, c)
    if is_dir:
        return "./" if r == "." else r + "/"
    return r


def resolve(html, cur):
    html = re.sub(r"\{u:([^}]*)\}", lambda m: rel(cur, m.group(1)), html)
    return re.sub(r"\{a:([^}]*)\}", lambda m: rel(cur, m.group(1)), html)


def icon(name, cls=""):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"/></svg>' if cls else f'<svg aria-hidden="true"><use href="#i-{name}"/></svg>'


def tico(cur, key):
    u = rel(cur, "assets/img/icons/" + key + ".png")
    return f'<span class="ico" aria-hidden="true"><i style="-webkit-mask-image:url({u});mask-image:url({u})"></i></span>'


STARS = '<span class="stars" aria-hidden="true">' + "".join('<svg><use href="#i-star"/></svg>' for _ in range(4)) + '<span class="hstar"><svg><use href="#i-star"/></svg><svg><use href="#i-star"/></svg></span></span>'

SPRITE = """<svg width="0" height="0" style="position:absolute" aria-hidden="true">
<symbol id="i-phone" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 3.5h3.2l1.6 4.2-2 1.4a11 11 0 0 0 7.1 7.1l1.4-2 4.2 1.6V19a1.8 1.8 0 0 1-1.9 1.8A16.5 16.5 0 0 1 3.2 5.4 1.8 1.8 0 0 1 5 3.5Z"/></symbol>
<symbol id="i-pin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11Z"/><circle cx="12" cy="10" r="2.4"/></symbol>
<symbol id="i-clock" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/></symbol>
<symbol id="i-mail" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><rect x="3.5" y="5.5" width="17" height="13" rx="2"/><path d="m4 7 8 6 8-6"/></symbol>
<symbol id="i-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 12h15M13.5 6l6 6-6 6"/></symbol>
<symbol id="i-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></symbol>
<symbol id="i-cal" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/></symbol>
<symbol id="i-alert" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3.5 2.8 19.5h18.4L12 3.5Z"/><path d="M12 10v4.2M12 17h.01"/></symbol>
<symbol id="i-insta" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r=".9" fill="currentColor"/></symbol>
<symbol id="i-star" viewBox="0 0 24 24"><path fill="currentColor" d="m12 2.8 2.8 5.9 6.4.8-4.7 4.4 1.2 6.4L12 17.2l-5.7 3.1 1.2-6.4-4.7-4.4 6.4-.8L12 2.8Z"/></symbol>
<symbol id="i-user" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><circle cx="10" cy="8" r="3.8"/><path d="M3.5 20a6.5 6.5 0 0 1 13 0M19 8v6M16 11h6"/></symbol>
</svg>"""

# ---------------------------------------------------------------- schema

def dentist_schema(full=True):
    d = {
        "@type": "Dentist",
        "@id": BASE + "#praktijk",
        "name": NAME,
        "alternateName": "Tandartsenpraktijk Slotplantsoen",
        "url": BASE,
    }
    if not full:
        return d
    d.update({
        "description": "Tandartspraktijk in het centrum van Meppel voor algemene tandheelkunde, implantologie, orthodontie (Invisalign), protheses, esthetiek en preventie. Met eigen CBCT-scanner en tandtechnisch laboratorium.",
        "logo": BASE + "assets/img/icon-512.png",
        "image": [BASE + "assets/img/og-slotplantsoen.jpg", BASE + "assets/img/praktijk-gevel.webp"],
        "telephone": "+31522247436",
        "email": MAIL,
        "address": {"@type": "PostalAddress", "streetAddress": "Slotplantsoen 1a", "postalCode": "7941 LP",
                    "addressLocality": "Meppel", "addressRegion": "Drenthe", "addressCountry": "NL"},
        "geo": {"@type": "GeoCoordinates", "latitude": 52.698499, "longitude": 6.1919536},
        "hasMap": MAPS,
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Monday", "opens": "08:00", "closes": "12:30"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Monday", "opens": "13:15", "closes": "20:00"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday"], "opens": "08:00", "closes": "12:30"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday"], "opens": "13:15", "closes": "16:45"},
        ],
        "areaServed": [{"@type": "City", "name": n} for n in ["Meppel", "Nijeveen", "Havelte", "Staphorst", "Ruinerwold", "De Wijk"]],
        "medicalSpecialty": "Dentistry",
        "isAcceptingNewPatients": True,
        "currenciesAccepted": "EUR",
        "paymentAccepted": "Pin, factuur via Infomedics",
        "sameAs": [INSTA, MAPS],
        "availableService": [
            {"@type": "MedicalProcedure", "name": T[s]["procedure"], "url": BASE + "behandelingen/" + s + "/"}
            for s, *_ in TREATMENTS
        ],
    })
    return d


def breadcrumb_schema(crumbs):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + p} for i, (p, n) in enumerate(crumbs)]}


def ld(*objs):
    graph = {"@context": "https://schema.org", "@graph": list(objs)}
    return '<script type="application/ld+json">' + json.dumps(graph, ensure_ascii=False, separators=(",", ":")) + "</script>"

# ---------------------------------------------------------------- layout

def head(p):
    cur = p["path"]
    canon = BASE + cur
    title = escape(p["title"])
    desc = escape(p["desc"])
    og_img = BASE + "assets/img/og-slotplantsoen.jpg"
    robots = "noindex,follow" if p.get("noindex") else "index,follow,max-image-preview:large,max-snippet:-1"
    if DEMO:
        robots = "noindex,nofollow"
    preload = ""
    if p.get("preload"):
        preload = f'<link rel="preload" as="image" href="{rel(cur, p["preload"])}" fetchpriority="high">\n'
    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="nl-NL" href="{canon}">
<meta name="theme-color" content="#1b2134">
<meta name="format-detection" content="telephone=no">
<meta name="geo.region" content="NL-DR">
<meta name="geo.placename" content="Meppel">
<meta name="geo.position" content="52.698499;6.1919536">
<meta name="ICBM" content="52.698499, 6.1919536">
<meta property="og:type" content="{p.get('ogtype', 'website')}">
<meta property="og:locale" content="nl_NL">
<meta property="og:site_name" content="{NAME}, Meppel">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{NAME} in Meppel, Uw glimlach verdient vertrouwen">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{rel(cur, 'favicon.ico')}" sizes="any">
<link rel="icon" type="image/png" sizes="192x192" href="{rel(cur, 'assets/img/icon-192.png')}">
<link rel="apple-touch-icon" href="{rel(cur, 'assets/img/apple-touch-icon.png')}">
<link rel="manifest" href="{rel(cur, 'site.webmanifest')}">
<link rel="preload" href="{rel(cur, 'assets/fonts/archivo-latin.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{rel(cur, 'assets/fonts/worksans-latin.woff2')}" as="font" type="font/woff2" crossorigin>
{preload}<link rel="stylesheet" href="{rel(cur, 'assets/css/style.css')}?v={CSS_V}">
{p.get('schema', '')}
</head>"""


def header(p):
    cur = p["path"]
    sect = p.get("section")

    def a(path, label, cls="nav__link"):
        ac = ' aria-current="page"' if path == cur else ""
        return f'<a class="{cls}" href="{rel(cur, path)}"{ac}>{label}</a>'

    mega = "".join(
        f'<a href="{rel(cur, "behandelingen/" + s + "/")}"{" aria-current=\"page\"" if cur == "behandelingen/" + s + "/" else ""}>{tico(cur, ic)}<span>{n}</span><small>{d}</small></a>'
        for s, n, d, ic in TREATMENTS)
    mega += f'<a class="all" href="{rel(cur, "behandelingen/")}">Alle behandelingen bekijken {icon("arrow")}</a>'

    def simple(lst):
        return "".join(f'<a href="{rel(cur, pth)}"{" aria-current=\"page\"" if pth == cur else ""}>{n}</a>' for pth, n in lst)

    def dd(id_, label, inner, mega_=False, key=None):
        act = " is-active" if sect == key else ""
        return (f'<li class="nav__item has-drop"><button class="nav__link{act}" type="button" aria-expanded="false" aria-controls="dd-{id_}">'
                f'{label} {icon("chev")}</button><div class="drop{" drop--mega" if mega_ else ""}" id="dd-{id_}">{inner}</div></li>')

    def mob(label, lst):
        return f'<details><summary>{label} {icon("chev")}</summary><div>{simple(lst)}</div></details>'

    beh_list = [("behandelingen/", "Alle behandelingen")] + [("behandelingen/" + s + "/", n) for s, n, *_ in TREATMENTS]
    return f"""<body>
{SPRITE}
<a class="skip" href="#main">Direct naar de inhoud</a>
<header class="mast">
  <div class="wrap mast__top">
    <div class="mast__visit">
      <span class="status" data-status role="status">Open maandag tot en met donderdag</span>
      <a href="{MAPS}" rel="noopener" target="_blank">Slotplantsoen 1a, Meppel</a>
    </div>
    <a class="mast__logo" href="{rel(cur, '')}" aria-label="{NAME}, naar de homepage"><img src="{rel(cur, 'assets/img/logo-licht.png')}" alt="{NAME}" width="580" height="160"></a>
    <div class="mast__act">
      <a class="mast__tel" href="{TEL_HREF}">{icon("phone")}<span>{TEL}</span></a>
      <a class="btn" href="{rel(cur, 'afspraak-maken/')}">Afspraak maken</a>
    </div>
    <a class="mast__call" href="{TEL_HREF}" aria-label="Bel {TEL}">{icon("phone")}</a>
    <button class="burger" type="button" aria-expanded="false" aria-controls="drawer" aria-label="Menu openen"><span></span></button>
  </div>
  <div class="mast__bar">
    <div class="wrap mast__row">
      <a class="mast__mark" href="{rel(cur, '')}" tabindex="-1" aria-hidden="true"><img src="{rel(cur, 'assets/img/mark-licht.png')}" alt="" width="125" height="116"></a>
      <nav class="nav" aria-label="Hoofdmenu">
        <ul class="nav__list">
          {dd("beh", "Behandelingen", mega, True, "beh")}
          {dd("praktijk", "Praktijk", simple(PRAKTIJK), key="praktijk")}
          {dd("info", "Patiënteninfo", simple(INFO), key="info")}
          <li class="nav__item">{a("inschrijven-als-nieuwe-patient/", "Nieuwe patiënten")}</li>
          <li class="nav__item">{a("contact/", "Contact")}</li>
        </ul>
      </nav>
      <a class="mast__quick" href="{rel(cur, 'afspraak-maken/')}" tabindex="-1">Afspraak maken</a>
    </div>
  </div>
</header>
<div class="drawer" id="drawer">
  {mob("Behandelingen", beh_list)}
  {mob("Praktijk", PRAKTIJK)}
  {mob("Patiënteninfo", INFO)}
  <a href="{rel(cur, 'inschrijven-als-nieuwe-patient/')}">Nieuwe patiënten {icon("arrow")}</a>
  <a href="{rel(cur, 'contact/')}">Contact {icon("arrow")}</a>
  <div class="drawer__cta">
    <a class="btn" href="{rel(cur, 'afspraak-maken/')}">{icon("cal")}Afspraak maken</a>
    <a class="btn btn--line" href="{TEL_HREF}">{icon("phone")}Bel {TEL}</a>
  </div>
  <p class="drawer__meta"><span class="status" data-status></span><br>Slotplantsoen 1a, 7941 LP Meppel<br><a href="mailto:{MAIL}">{MAIL}</a></p>
</div>"""


def footer(p):
    cur = p["path"]
    beh = "".join(f'<li><a href="{rel(cur, "behandelingen/" + s + "/")}">{n}</a></li>' for s, n, *_ in TREATMENTS)
    prak = "".join(f'<li><a href="{rel(cur, pth)}">{n}</a></li>' for pth, n in PRAKTIJK + INFO[:4])
    return f"""<footer class="footer dark">
  <div class="wrap">
    <div class="footer__grid">
      <div>
        <a class="logo" href="{rel(cur, '')}" aria-label="{NAME}, homepage"><img src="{rel(cur, 'assets/img/logo-licht.png')}" alt="{NAME}" width="580" height="160" loading="lazy"></a>
        <p>Persoonlijke aandacht en vertrouwde zorg voor het hele gezin, midden in Meppel.</p>
        <address style="font-style:normal">
          <p><a href="{MAPS}" rel="noopener" target="_blank">Slotplantsoen 1a<br>7941 LP Meppel</a></p>
          <p><a href="{TEL_HREF}">{TEL}</a><br><a href="mailto:{MAIL}">{MAIL}</a></p>
        </address>
        <div class="social"><a href="{INSTA}" rel="noopener" target="_blank" aria-label="Volg ons op Instagram">{icon("insta")}</a><a href="{MAPS}" rel="noopener" target="_blank" aria-label="Bekijk ons op Google Maps">{icon("pin")}</a></div>
      </div>
      <div><h2>Behandelingen</h2><ul>{beh}</ul></div>
      <div><h2>Praktijk</h2><ul>{prak}</ul></div>
      <div><h2>Openingstijden</h2>
        <ul>
          <li>Ma: 08:00-12:30 / 13:15-20:00</li>
          <li>Di t/m do: 08:00-12:30 / 13:15-16:45</li>
          <li>Vr t/m zo: gesloten</li>
        </ul>
        <p style="margin-top:14px"><a href="{rel(cur, 'afspraak-maken/')}">Afspraak maken</a><br><a href="{rel(cur, 'inschrijven-als-nieuwe-patient/')}">Inschrijven als nieuwe patiënt</a></p>
      </div>
    </div>
  </div>
  <div class="wrap footer__bottom">
    <span>© <span data-year>{date.today().year}</span> {NAME}, Meppel</span>
    <span class="footer__legal"><a href="{rel(cur, 'privacyverklaring/')}">Privacyverklaring</a><a href="{rel(cur, 'homepage/huisregels/')}">Huisregels</a><a href="{rel(cur, 'sitemap.xml')}">Sitemap</a></span>
  </div>
</footer>
<div class="mbar"><a class="btn btn--navy" href="{TEL_HREF}">{icon("phone")}Bellen</a><a class="btn" href="{rel(cur, 'afspraak-maken/')}">{icon("cal")}Afspraak maken</a></div>
<script src="{rel(cur, 'assets/js/main.js')}?v={JS_V}" defer></script>
</body>
</html>
"""


def crumbs_html(cur, crumbs):
    items = []
    for i, (pth, n) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            items.append(f'<li aria-current="page">{n}</li>')
        else:
            items.append(f'<li><a href="{rel(cur, pth)}">{n}</a></li>')
    return f'<nav class="crumbs" aria-label="Kruimelpad"><ol>{"".join(items)}</ol></nav>'


# Elke soort pagina krijgt een eigen kop, zodat niet alles op hetzelfde sjabloon lijkt.
HERO_KIND = {
    "behandelingen/": "plain",
    "homepage/ons-team/": "count",
    "homepage/praktijkinformatie/": "poster",
    "cbct-rontgen/": "poster",
    "kinderen-en-de-tandarts/": "poster",
    "homepage/spoedgevallen-en-weekenddienst/": "spoed",
    "contact/": "plain",
    "homepage/tarieven-en-betaling/": "plain",
    "homepage/betalen-en-vergoedingen/": "plain",
    "homepage/huisregels/": "plain",
    "privacyverklaring/": "plain",
    "doorverwijzing-cbct-scan-voor-behandelaars/": "plain",
    "afspraak-maken/": "form",
    "inschrijven-als-nieuwe-patient/": "form",
}
POSTER = {
    "homepage/praktijkinformatie/": ("hero-poster.webp", "De entree van Tandartspraktijk Slotplantsoen in Meppel", "50% 45%"),
    "cbct-rontgen/": ("cbct.webp", "De Cone Beam CT-scanner van de praktijk", "50% 50%"),
    "kinderen-en-de-tandarts/": ("kinderen.webp", "Een meisje leert tandenpoetsen bij de tandarts", "60% 35%"),
}


def page_hero(p, cta=True):
    cur = p["path"]
    kind = HERO_KIND.get(cur) or ("light" if p.get("img") else "plain")
    crumbs = crumbs_html(cur, p["crumbs"])
    btns = ""
    if cta:
        line = "btn--line" if kind in ("poster", "spoed") else "btn--line btn--ink"
        btns = (f'<div class="btn-row"><a class="btn" href="{rel(cur, "afspraak-maken/")}">{icon("cal")}Afspraak maken</a>'
                f'<a class="btn {line}" href="{TEL_HREF}">{icon("phone")}Bel {TEL}</a></div>')
    h1, lead = p["h1"], p["lead"]

    if kind == "light":
        img = (f'<figure class="ph__img"><img src="{rel(cur, "assets/img/" + p["img"])}" alt="{escape(p.get("img_alt", ""))}" '
               f'width="480" height="600" fetchpriority="high" decoding="async"></figure>')
        return f"""<section class="ph ph--light on-light">
  <div class="wrap">
    {crumbs}
    <div class="ph__grid">
      <div class="ph__copy"><h1>{h1}</h1><p class="lead">{lead}</p>{btns}</div>
      {img}
    </div>
  </div>
</section>"""

    if kind == "poster":
        src, alt, pos = POSTER[cur]
        return f"""<section class="ph ph--poster dark">
  <div class="ph__bg"><img src="{rel(cur, "assets/img/" + src)}" alt="{escape(alt)}" width="1600" height="900" fetchpriority="high" decoding="async" style="object-position:{pos}"></div>
  <div class="wrap">
    {crumbs}
    <div class="ph__copy"><h1>{h1}</h1><p class="lead">{lead}</p>{btns}</div>
  </div>
</section>"""

    if kind == "spoed":
        return f"""<section class="ph ph--spoed dark">
  <div class="wrap">
    {crumbs}
    <div class="ph__grid">
      <div class="ph__copy"><h1>{h1}</h1><p class="lead">{lead}</p></div>
      <div class="ph__call">
        <p>Tijdens openingstijden</p>
        <a href="{TEL_HREF}">{TEL}</a>
        <p>Buiten openingstijden hoort u op het antwoordapparaat het nummer van de dienstdoende tandarts.</p>
      </div>
    </div>
  </div>
</section>"""

    if kind == "count":
        return f"""<section class="ph ph--plain ph--count on-light">
  <div class="wrap">
    {crumbs}
    <div class="ph__split">
      <div><h1>{h1}</h1><p class="lead">{lead}</p>{btns}</div>
      <p class="ph__num"><span>{len(TEAM)}</span><small>collega’s, van tandarts tot tandtechnieker</small></p>
    </div>
  </div>
</section>"""

    if kind == "form":
        return f"""<section class="ph ph--form dark">
  <div class="wrap">
    {crumbs}
    <div class="ph__copy"><h1>{h1}</h1><p class="lead">{lead}</p></div>
  </div>
</section>"""

    return f"""<section class="ph ph--plain on-light">
  <div class="wrap">
    {crumbs}
    <div class="ph__split">
      <h1>{h1}</h1>
      <div><p class="lead">{lead}</p>{btns}</div>
    </div>
  </div>
</section>"""


def aside(p, nav=None):
    cur = p["path"]
    hours = "".join(f'<li data-day="{d}"><span>{n[:2]}</span><span>{h.replace(", ", "-").replace(" en ", "<br>") if h else "gesloten"}</span></li>' for d, n, h in HOURS_ROWS[:5])
    navhtml = ""
    if nav:
        navhtml = '<div class="card"><h2>' + nav[0] + '</h2><nav aria-label="' + nav[0] + '"><ul>' + "".join(
            f'<li><a href="{rel(cur, pth)}"{" aria-current=\"page\"" if pth == cur else ""}>{n}</a></li>' for pth, n in nav[1]) + "</ul></nav></div>"
    return f"""<aside class="aside" aria-label="Afspraak en openingstijden">
  <div class="card dark">
    <h2>Afspraak maken</h2>
    <p>Online aanvragen kan altijd. Bellen kan ma t/m do van 08:30-12:30 en 13:30-16:30 uur.</p>
    <a class="btn" href="{rel(cur, 'afspraak-maken/')}">{icon("cal")}Afspraak aanvragen</a>
    <a class="btn btn--line" href="{TEL_HREF}">{icon("phone")}{TEL}</a>
  </div>
  <div class="card">
    <h2>Openingstijden</h2>
    <p><span class="status" data-status></span></p>
    <ul class="mini-hours">{hours}</ul>
    <a class="link" href="{rel(cur, 'homepage/spoedgevallen-en-weekenddienst/')}">Spoed buiten openingstijden {icon("arrow")}</a>
  </div>
  {navhtml}
</aside>"""


def cta_band(cur, title="Klaar voor een gezonde glimlach?", text="Bel ons, vraag online een afspraak aan of schrijf u in als nieuwe patiënt. We nemen weer nieuwe patiënten aan."):
    return f"""<section class="cta-band dark">
  <div class="wrap">
    <div><h2>{title}</h2><p>{text}</p></div>
    <div class="btn-row"><a class="btn" href="{rel(cur, 'afspraak-maken/')}">{icon("cal")}Afspraak maken</a><a class="btn btn--line" href="{rel(cur, 'inschrijven-als-nieuwe-patient/')}">{icon("user")}Inschrijven</a></div>
  </div>
</section>"""


def who_html(cur, keys, label="Uw behandelaar"):
    out = []
    for k in keys:
        n, role, _ = TEAM[k]
        out.append(f'<div class="who"><img src="{rel(cur, "assets/img/team/" + k + ".webp")}" alt="{escape(n)}" width="84" height="84" loading="lazy" decoding="async">'
                   f'<div><small>{label}</small><b>{n}</b><span>{role}</span></div></div>')
    return '<div class="who-row">' + "".join(out) + "</div>"


def faq_html(faq):
    items = "".join(f"<details><summary>{q}</summary><div><p>{a}</p></div></details>" for q, a in faq)
    return f'<section class="faq" aria-labelledby="faq-h"><h2 id="faq-h">Veelgestelde vragen</h2>{items}</section>'


def faq_schema(url, faq):
    return {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}


def hours_table():
    rows = []
    for d, n, h in HOURS_ROWS:
        rows.append(f'<tr data-day="{d}"><th scope="row">{n}</th>' + (f"<td>{h} uur</td>" if h else '<td class="closed">Gesloten</td>') + "</tr>")
    return f'<table class="hours"><caption class="sr-only">Openingstijden van de praktijk</caption>{"".join(rows)}</table>'


def contact_dl(cur):
    return f"""<dl class="dl">
  <div>{icon("pin")}<div><dt>Adres</dt><dd><a href="{MAPS}" rel="noopener" target="_blank">Slotplantsoen 1a, 7941 LP Meppel</a></dd></div></div>
  <div>{icon("phone")}<div><dt>Telefoon</dt><dd><a href="{TEL_HREF}">{TEL}</a><span class="dl__note">Ma t/m do 08:30-12:30 en 13:30-16:30 uur. Tussen 12:00 en 13:30 uur alleen bereikbaar op <a href="tel:+31627443039">06-27443039</a>.</span></dd></div></div>
  <div>{icon("mail")}<div><dt>E-mail</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd></div></div>
</dl>"""


def map_block():
    return f"""<div class="map">
  <div>
    {icon("pin", "")}
    <h3>Slotplantsoen 1a, Meppel</h3>
    <p>De kaart wordt geladen via Google Maps. Daarbij kan Google gegevens verwerken.</p>
    <div class="btn-row" style="justify-content:center"><button class="btn" type="button" data-map="{MAP_EMBED}">Kaart laden</button><a class="btn btn--line" href="{ROUTE}" rel="noopener" target="_blank">Route plannen</a></div>
  </div>
</div>"""


def write(p, main):
    cur = p["path"]
    html = head(p) + "\n" + header(p) + '\n<main id="main">\n' + main + "\n</main>\n" + footer(p)
    html = resolve(html, cur)
    html = re.sub(r'<em class="g">(.*?)</em>', r"\1", html)
    out = ROOT / (cur + "index.html" if cur.endswith("/") or cur == "" else cur)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    PAGES.append(p)


PAGES = []

# ---------------------------------------------------------------- formulieren

def field(name, label, typ="text", req=True, full=False, ac=None, opts=None, err=None, hint=None, attrs=""):
    cls = "field full" if full else "field"
    r = " required" if req else ""
    opt = "" if req else ' <span class="opt">(optioneel)</span>'
    ac_ = f' autocomplete="{ac}"' if ac else ""
    err = err or "Vul dit veld in."
    hint_html = f'<small class="hint" id="{name}-h">{hint}</small>' if hint else ""
    desc = f' aria-describedby="{name}-h"' if hint else ""
    if typ == "select":
        o = "".join(f'<option value="{v}">{t}</option>' for v, t in opts)
        ctl = f'<select id="{name}" name="{name}"{r}{attrs}><option value="">Maak een keuze</option>{o}</select>'
    elif typ == "textarea":
        ctl = f'<textarea id="{name}" name="{name}"{r}{desc}{attrs}></textarea>'
    else:
        ctl = f'<input id="{name}" name="{name}" type="{typ}"{r}{ac_}{desc}{attrs}>'
    return f'<div class="{cls}"><label for="{name}">{label}{opt}</label>{ctl}{hint_html}<span class="err">{err}</span></div>'


def checks(name, legend, vals):
    boxes = "".join(f'<label class="chip"><input type="checkbox" name="{name}" value="{v}"><span>{v}</span></label>' for v in vals)
    return f'<div class="field full"><fieldset><legend>{legend} <span class="opt">(optioneel)</span></legend><div class="chips">{boxes}</div></fieldset></div>'


def choice(name, legend, opts, param=None):
    """Een verplichte keuze als knoppen (radio's); de waarde blijft de code die ook ?soort= gebruikt."""
    dp = f' data-param="{param}"' if param else ""
    items = "".join(f'<label class="chip"><input type="radio" name="{name}" value="{v}" required><span>{t}</span></label>' for v, t in opts)
    return f'<div class="field full"><fieldset{dp}><legend>{legend}</legend><div class="chips">{items}</div></fieldset><span class="err">Maak een keuze.</span></div>'


def group(title, inner):
    return f'<fieldset class="fgroup full"><legend class="fgroup__t">{title}</legend><div class="fgroup__b">{inner}</div></fieldset>'


def form_page(cur, crumbs, title, desc, h1, lead, side, form, form_title, img=None, img_alt=None):
    """Een formulierpagina: korte kop, links de praktische info, rechts het formulier."""
    url = BASE + cur
    p = dict(path=cur, title=title, desc=desc, h1=h1, lead=lead, crumbs=crumbs, img=img, img_alt=img_alt)
    p["schema"] = ld({"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc, "inLanguage": "nl-NL",
                      "dateModified": TODAY, "publisher": {"@id": BASE + "#praktijk"}}, breadcrumb_schema(crumbs), dentist_schema(False))
    main = page_hero(p, cta=False) + f"""
<section class="fp section on-light">
  <div class="wrap fp__grid">
    <aside class="fp__side" aria-label="Praktische informatie">{side}</aside>
    <div class="fp__main"><h2>{form_title}</h2>{form}</div>
  </div>
</section>"""
    write(p, main)


def consent(cur):
    return (f'<div class="field full"><label class="consent"><input type="checkbox" name="akkoord" required> '
            f'<span>Ik ga akkoord met de verwerking van mijn gegevens volgens de <a href="{rel(cur, "privacyverklaring/")}">privacyverklaring</a>.</span></label>'
            f'<span class="err">Geef toestemming om uw aanvraag te kunnen versturen.</span></div>')


def form_wrap(cur, subject, inner, ok, button):
    return (f'<form class="form" data-form="{subject}" action="mailto:{MAIL}" method="post">{inner}{consent(cur)}'
            f'<div class="full"><button class="btn btn--navy" type="submit">{button} {icon("arrow")}</button></div>'
            f'<p class="form__ok" role="status">{ok}</p><p class="form__err" role="alert" hidden>Versturen is niet gelukt. Bel ons gerust op {TEL}.</p></form>')

# ================================================================= PAGINA'S

def hero_media(cur):
    """Achtergrondvideo van de hero. Zet de video van de praktijk in assets/video/ als hero.mp4 (en eventueel hero.webm);
    zolang die er niet is, toont de hero de poster (assets/img/hero-poster.webp)."""
    vid = ROOT / "assets" / "video"
    sources = ""
    if (vid / "hero.webm").exists():
        sources += f'<source src="{rel(cur, "assets/video/hero.webm")}" type="video/webm">'
    if (vid / "hero.mp4").exists():
        sources += f'<source src="{rel(cur, "assets/video/hero.mp4")}" type="video/mp4">'
    poster = rel(cur, "assets/img/hero-poster.webp")
    if not sources:
        return (f'<div class="hx__media" aria-hidden="true"><img src="{poster}" alt="" width="1600" height="900" '
                f'fetchpriority="high" decoding="async"></div>')
    return (f'<div class="hx__media" aria-hidden="true"><video class="hx__video" autoplay muted loop playsinline '
            f'preload="metadata" poster="{poster}" data-hero-video>{sources}</video></div>'
            f'<button class="hx__pause" type="button" aria-pressed="false" data-hero-pause>'
            f'<svg aria-hidden="true" viewBox="0 0 24 24"><path d="M8 5v14M16 5v14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
            f'<span>Video pauzeren</span></button>')


def home():
    cur = ""
    p = dict(path=cur, title="Tandarts Meppel | Tandartspraktijk Slotplantsoen",
             desc="Tandarts in het centrum van Meppel: controle, implantaten, Invisalign, kunstgebit en esthetiek. CBCT en eigen lab in huis. Nieuwe patiënten welkom.",
             preload="assets/img/hero-poster.webp")
    p["schema"] = ld(dentist_schema(), {"@type": "WebSite", "@id": BASE + "#website", "url": BASE, "name": NAME, "inLanguage": "nl-NL", "publisher": {"@id": BASE + "#praktijk"}},
                     {"@type": "WebPage", "@id": BASE + "#webpage", "url": BASE, "name": p["title"], "isPartOf": {"@id": BASE + "#website"}, "about": {"@id": BASE + "#praktijk"}, "inLanguage": "nl-NL", "dateModified": TODAY})
    index = "".join(
        f'<li><a href="{{u:behandelingen/{s}/}}"><span class="hx__name">{n.replace("Wortelkanaalbehandeling", "Wortelkanaal&shy;behandeling")}</span>{icon("arrow", "hx__arr")}</a></li>'
        for s, n, d, ic in TREATMENTS)
    team = "".join(
        f'<figure class="person"><img src="{{a:assets/img/team/{k}.webp}}" alt="{escape(n)}, {escape(r.lower())}" width="480" height="720" loading="lazy" decoding="async"><figcaption><b>{n}</b><span>{r}</span></figcaption></figure>'
        for k, (n, r, _) in TEAM.items())
    week = ""
    for d, n, h in HOURS_ROWS:
        times = "".join(f"<span>{t.replace(' – ', '-')}</span>" for t in h.split(" en ")) if h else '<span class="week__closed">Gesloten</span>'
        week += f'<li data-day="{d}"{" class=\"is-closed\"" if not h else ""}><b>{n}</b>{times}</li>'
    main = f"""
<section class="hx dark" aria-labelledby="hero-h">
  {hero_media(cur)}
  <div class="wrap">
    <div class="hx__head">
      <h1 id="hero-h">Uw glimlach verdient<br><em class="sig">vertrouwen.</em></h1>
      <div class="hx__side">
        <p class="lead">Tandarts in het hart van Meppel. Nieuwe patiënten zijn welkom.</p>
        <div class="btn-row">
          <a class="btn" href="{{u:afspraak-maken/}}">{icon("cal")}Afspraak maken</a>
          <a class="btn btn--line" href="{{u:inschrijven-als-nieuwe-patient/}}">{icon("user")}Inschrijven</a>
        </div>
      </div>
    </div>
    <nav class="hx__index" aria-label="Behandelingen">
      <ul>{index}</ul>
      <a class="hx__all" href="{{u:behandelingen/}}">Alle behandelingen met uitleg en vergoeding</a>
    </nav>
  </div>
</section>

<section class="pk section on-light" aria-labelledby="intro-h">
  <div class="wrap">
    <div class="pk__head rv">
      <h2 id="intro-h">Alle zorg voor uw gebit, onder één dak in Meppel.</h2>
      <div>
        <p class="lead">Tandartspraktijk Slotplantsoen is een klantgerichte praktijk voor algemene tandheelkunde, esthetiek, orthodontie en implantologie. Preventie krijgt bij ons een belangrijke plek: liever voorkomen dan genezen.</p>
        <p>Tandartsen, preventieassistenten, tandprothetici en een tandtechnieker werken hier samen. Zo hoeft u voor een 3D-scan, een nieuwe kroon of de reparatie van uw prothese niet ergens anders heen.</p>
        <p><a class="link" href="{{u:homepage/praktijkinformatie/}}">Meer over de praktijk {icon("arrow")}</a></p>
      </div>
    </div>
    <div class="pk__pics rv">
      <figure class="pk__wide"><img src="{{a:assets/img/praktijk-gevel.webp}}" alt="Entree van Tandartspraktijk Slotplantsoen aan het Slotplantsoen in Meppel" width="1100" height="736" loading="lazy" decoding="async"><figcaption><b>Slotplantsoen 1a, midden in Meppel.</b> Op maandag geopend tot 20:00 uur. In huis: een 3D CBCT-scanner en een eigen tandtechnisch laboratorium voor kronen, bruggen en protheses.</figcaption></figure>
      <figure class="pk__tall"><img src="{{a:assets/img/alvaro-groot.webp}}" alt="Alvaro Soler, tandarts-implantoloog bij Tandartspraktijk Slotplantsoen" width="760" height="1140" loading="lazy" decoding="async"><figcaption><b>Alvaro Soler, tandarts-implantoloog,</b> een van onze vijf tandartsen. Samen hebben zij aandacht voor implantologie, orthodontie en esthetiek.</figcaption></figure>
    </div>
  </div>
</section>

<section class="section section--sand on-light" aria-labelledby="zorg-h">
  <div class="wrap">
    <div class="section__head rv"><div><h2 id="zorg-h">Voor groot en klein, en voor wie het spannend vindt.</h2></div></div>
    <div class="stories">
      <a class="story story--a rv" href="{{u:kinderen-en-de-tandarts/}}">
        <img src="{{a:assets/img/kinderen.webp}}" alt="Meisje leert tandenpoetsen bij de tandarts" width="900" height="588" loading="lazy" decoding="async">
        <div class="story__body"><h3>Kinderen en de tandarts</h3><p>Vanaf twee jaar mag uw kind mee om rustig te wennen. Op een speelse manier bouwen we vertrouwen op, en twee controles per jaar is meestal genoeg.</p><span class="link">Tips voor ouders {icon("arrow")}</span></div>
      </a>
      <a class="story story--b story--dark story--quote rv rv-d1" href="{{u:angst-voor-de-tandarts/}}">
        <div class="story__body"><blockquote>U bepaalt het tempo. Wij nemen de tijd en leggen alles vooraf uit.</blockquote><p>Bang voor de tandarts? U bent niet de enige. Met een rustige ontvangst, eigen muziek en een afgesproken stopteken maken we het u zo makkelijk mogelijk.</p><span class="link">Angst voor de tandarts {icon("arrow")}</span></div>
      </a>
      <a class="story story--c rv" href="{{u:cbct-rontgen/}}">
        <img src="{{a:assets/img/cbct.webp}}" alt="Cone Beam CT-scanner in de praktijk" width="900" height="588" loading="lazy" decoding="async">
        <div class="story__body"><h3>3D CBCT-scan in huis</h3><p>Minder straling dan een gewone CT-scan en direct een betrouwbaar 3D-beeld. Ook voor verwijzende tandartsen.</p><span class="link">Over de CBCT-scan {icon("arrow")}</span></div>
      </a>
      <a class="story story--d rv rv-d1" href="{{u:behandelingen/othodontie-en-invisalign/}}">
        <img src="{{a:assets/img/invisalign.webp}}" alt="Doorzichtige Invisalign-aligner" width="900" height="588" loading="lazy" decoding="async">
        <div class="story__body"><h3>Invisalign: rechte tanden, onopvallend</h3><p>Doorzichtige, uitneembare aligners die uw tanden stap voor stap verplaatsen. Begeleid door onze tandarts voor orthodontie.</p><span class="link">Meer over Invisalign {icon("arrow")}</span></div>
      </a>
    </div>
  </div>
</section>

<section class="section section--paper on-light" aria-labelledby="team-h">
  <div class="wrap">
    <div class="section__head rv">
      <div><h2 id="team-h">Ons team</h2><p>Vertrouwde gezichten: veertien collega’s die elke dag klaarstaan voor uw mondgezondheid, van tandarts tot tandtechnieker.</p></div>
      <div class="team-head__act">
        <a class="link" href="{{u:homepage/ons-team/}}">Maak kennis met het team {icon("arrow")}</a>
        <div class="rail-nav"><button type="button" data-rail="-1" aria-controls="team-strip" aria-label="Vorige teamleden"><svg aria-hidden="true"><use href="#i-arrow"/></svg></button><button type="button" data-rail="1" aria-controls="team-strip" aria-label="Volgende teamleden"><svg aria-hidden="true"><use href="#i-arrow"/></svg></button></div>
      </div>
    </div>
    <div class="team-strip" id="team-strip" tabindex="0" aria-label="Teamleden, veeg of scroll horizontaal">{team}</div>
  </div>
</section>

<section class="np section on-light" aria-labelledby="nieuw-h">
  <div class="wrap np__grid">
    <figure class="np__pic rv"><img src="{{a:assets/img/preventie.webp}}" alt="Een assistente van de praktijk helpt een patiënte in de behandelstoel" width="567" height="850" loading="lazy" decoding="async"><figcaption>Naïma, tandarts- en preventieassistente, aan het werk</figcaption></figure>
    <div class="np__body rv rv-d1">
      <h2 id="nieuw-h">Nieuwe patiënten</h2>
      <p class="lead">In drie stappen patiënt bij ons.</p>
      <ol class="np__list">
        <li><h3>Schrijf u in</h3><p>Vul het online formulier in, voor uzelf of het hele gezin. Het duurt twee minuten.</p></li>
        <li><h3>U krijgt een uitnodiging</h3><p>We verwerken uw inschrijving en nodigen u uit voor een eerste consult.</p></li>
        <li><h3>Eerste consult</h3><p>Kennismaking, medische vragenlijst, een grondig onderzoek van gebit en tandvlees en zo nodig digitale röntgenfoto’s.</p></li>
      </ol>
      <a class="btn btn--navy" href="{{u:inschrijven-als-nieuwe-patient/}}">{icon("user")}Nu inschrijven</a>
      <p class="np__proof">{STARS}<span><b>4,3 van 5</b> gemiddeld in 29 Google-reviews</span><a class="link" href="{MAPS}" rel="noopener" target="_blank">Lees de reviews op Google {icon("arrow")}</a></p>
    </div>
  </div>
</section>

<section class="cl dark" aria-labelledby="contact-h">
  <div class="wrap cl__grid">
    <div class="cl__info">
      <h2 id="contact-h">Contact en openingstijden</h2>
      <p class="lead">Kom langs aan het Slotplantsoen 1a, midden in Meppel.</p>
      {contact_dl(cur)}
      <p><a class="link" href="{{u:contact/}}">Alle contactgegevens {icon("arrow")}</a></p>
    </div>
    <div class="cl__book">
      <p class="cl__now"><span class="status" data-status></span></p>
      <ol class="week" aria-label="Openingstijden per dag">{week}</ol>
      <div class="cl__intake">
        <h3>Gratis intake</h3>
        <p>Twijfelt u over een beugel, Invisalign of een nieuw (klik)gebit? Tijdens een gratis intake bekijken we uw situatie en hoort u eerlijk wat er mogelijk is, zonder verplichtingen.</p>
        <div class="cl__choices">
          <a class="btn btn--line" href="{{u:afspraak-maken/}}?soort=intake-orthodontie">Orthodontie</a>
          <a class="btn btn--line" href="{{u:afspraak-maken/}}?soort=intake-invisalign">Esthetische orthodontie</a>
          <a class="btn btn--line" href="{{u:afspraak-maken/}}?soort=intake-prothese">Gebitsprothese of klikgebit</a>
        </div>
      </div>
      <a class="btn cl__cta" href="{{u:afspraak-maken/}}">{icon("cal")}Afspraak maken</a>
      <p class="cl__spoed">{icon("alert")}<span><b>Pijn of spoed?</b> Bel tijdens openingstijden bij voorkeur tussen 08:30 en 10:00 uur, dan proberen we u dezelfde dag te helpen. <a href="{{u:homepage/spoedgevallen-en-weekenddienst/}}">Wat te doen buiten openingstijden</a></span></p>
    </div>
  </div>
  <div class="wrap cl__map">{map_block()}</div>
</section>
"""
    write(p, main)


def treatment_pages():
    for s, n, d, ic in TREATMENTS:
        t = T[s]
        cur = f"behandelingen/{s}/"
        url = BASE + cur
        crumbs = [("", "Home"), ("behandelingen/", "Behandelingen"), (cur, n)]
        p = dict(path=cur, title=t["title"], desc=t["desc"], h1=t["h1"], lead=t["lead"], img=t.get("img"), img_alt=t.get("img_alt"),
                 crumbs=crumbs, section="beh", preload="assets/img/" + t["img"] if t.get("img") else None, ogtype="article")
        p["schema"] = ld(
            {"@type": "MedicalWebPage", "@id": url + "#webpage", "url": url, "name": t["title"], "description": t["desc"], "inLanguage": "nl-NL",
             "dateModified": TODAY, "lastReviewed": TODAY,
             "about": {"@type": "MedicalProcedure", "name": t["procedure"]},
             "publisher": {"@id": BASE + "#praktijk"}, "breadcrumb": {"@id": url + "#breadcrumb"}},
            dict(breadcrumb_schema(crumbs), **{"@id": url + "#breadcrumb"}),
            faq_schema(url, t["faq"]),
            dentist_schema(False))
        rel_items = "".join(
            f'<a href="{{u:behandelingen/{r}/}}">{tico(cur, TMAP[r][3])}<b>{TMAP[r][1]}</b></a>' for r in t["related"])
        main = page_hero(p) + f"""
<section class="section on-light">
  <div class="wrap layout">
    <article class="prose">
      {t["body"]}
      {who_html(cur, t["who"], "Uw behandelaar" if len(t["who"]) == 1 else "Behandeld door")}
      {faq_html(t["faq"])}
    </article>
    {aside(p, ("Behandelingen", [("behandelingen/" + x, y) for x, y, *_ in TREATMENTS]))}
  </div>
</section>
<section class="section section--sand on-light" style="padding-block:clamp(48px,6vw,80px)">
  <div class="wrap">
    <h2 style="font-size:clamp(1.6rem,2.6vw,2.2rem)">Gerelateerde behandelingen</h2>
    <div class="related">{rel_items}</div>
  </div>
</section>
""" + cta_band(cur)
        write(p, main)


def behandelingen_index():
    cur = "behandelingen/"
    crumbs = [("", "Home"), (cur, "Behandelingen")]
    p = dict(path=cur, title="Behandelingen | Tandarts Meppel | Tandartspraktijk Slotplantsoen",
             desc="Alle behandelingen van Tandartspraktijk Slotplantsoen in Meppel: implantaten, Invisalign, kronen en bruggen, protheses, bleken, vullingen, preventie en meer.",
             h1='Behandelingen bij uw tandarts in <em class="g">Meppel</em>',
             lead="Algemene tandheelkunde, esthetiek, orthodontie en implantologie onder één dak. Hieronder vindt u per behandeling uitleg over het verloop, de mogelijkheden en de vergoeding.",
             crumbs=crumbs, section="beh")
    p["schema"] = ld({"@type": "CollectionPage", "@id": BASE + cur + "#webpage", "url": BASE + cur, "name": p["title"], "inLanguage": "nl-NL",
                      "hasPart": [{"@type": "MedicalWebPage", "url": BASE + "behandelingen/" + s + "/", "name": n} for s, n, *_ in TREATMENTS]},
                     breadcrumb_schema(crumbs), dentist_schema(False))
    tlist = "".join(
        f'<li class="rv"><a href="{{u:behandelingen/{s}/}}">{tico(cur, ic)}<div><h2>{n}</h2><p>{d}</p></div>{icon("arrow", "arr")}</a></li>'
        for s, n, d, ic in TREATMENTS)
    main = page_hero(p) + f"""
<section class="section on-light"><div class="wrap"><ul class="tlist">{tlist}</ul>
<div class="note" style="margin-top:48px;max-width:760px"><p><b>Tarieven.</b> Voor alle behandelingen gelden de tarieven die jaarlijks door de Nederlandse Zorgautoriteit (NZa) worden vastgesteld. Vooraf een begroting? Vraag er gerust om. Lees meer over <a href="{{u:homepage/tarieven-en-betaling/}}">tarieven en betaling</a> en <a href="{{u:homepage/betalen-en-vergoedingen/}}">vergoedingen</a>.</p></div>
</div></section>""" + cta_band(cur)
    write(p, main)


def team_page():
    cur = "homepage/ons-team/"
    crumbs = [("", "Home"), ("homepage/praktijkinformatie/", "Praktijk"), (cur, "Ons team")]
    p = dict(path=cur, title="Ons team | Tandartsen in Meppel | Tandartspraktijk Slotplantsoen",
             desc="Maak kennis met het team van Tandartspraktijk Slotplantsoen in Meppel: tandartsen, implantoloog, orthodontie, preventieassistenten, tandprothetici en tandtechnieker.",
             h1='Maak kennis met <em class="g">ons team</em>', lead="Veertien collega’s, één doel: persoonlijke aandacht en vertrouwde zorg voor uw gebit. Bij ons ziet u vertrouwde gezichten, van de balie tot de behandelstoel.",
             crumbs=crumbs, section="praktijk", img="hero-kinan.webp", img_alt="Tandarts Kinan Khalil in de behandelkamer")
    people = [{"@type": "Person", "name": n, "jobTitle": r, "image": BASE + "assets/img/team/" + k + ".webp", "worksFor": {"@id": BASE + "#praktijk"}} for k, (n, r, _) in TEAM.items()]
    p["schema"] = ld({"@type": "AboutPage", "@id": BASE + cur + "#webpage", "url": BASE + cur, "name": p["title"], "inLanguage": "nl-NL", "about": {"@id": BASE + "#praktijk"}},
                     breadcrumb_schema(crumbs), dict(dentist_schema(False), employee=people))
    groups = [("tandarts", "Tandartsen"), ("mondzorg", "Preventie en assistentie"), ("prothetiek", "Prothetiek en tandtechniek"), ("management", "Praktijkmanagement")]
    html = ""
    for g, label in groups:
        figs = "".join(
            f'<figure class="person rv"><img src="{{a:assets/img/team/{k}.webp}}" alt="{escape(n)}, {escape(r.lower())}" width="480" height="720" loading="lazy" decoding="async"><figcaption><b>{n}</b><span>{r}</span></figcaption></figure>'
            for k, (n, r, gg) in TEAM.items() if gg == g)
        html += f'<div class="team-group"><h2>{label}</h2><div class="team-grid">{figs}</div></div>'
    main = page_hero(p) + f"""<section class="section on-light"><div class="wrap">{html}
<div class="note" style="margin-top:56px;max-width:760px"><p><b>Werken bij Slotplantsoen?</b> We zoeken regelmatig nieuwe collega’s. Bekijk de <a href="{{u:vacatures/}}">vacatures</a>.</p></div>
</div></section>""" + cta_band(cur)
    write(p, main)


def text_page(cur, crumbs, section, title, desc, h1, lead, body, img=None, img_alt=None, nav=None, faq=None, extra_schema=None, cta=True, after=""):
    url = BASE + cur
    p = dict(path=cur, title=title, desc=desc, h1=h1, lead=lead, crumbs=crumbs, section=section, img=img, img_alt=img_alt)
    objs = [{"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc, "inLanguage": "nl-NL", "dateModified": TODAY, "publisher": {"@id": BASE + "#praktijk"}},
            breadcrumb_schema(crumbs)]
    if faq:
        objs.append(faq_schema(url, faq))
    objs.extend(extra_schema or [dentist_schema(False)])
    p["schema"] = ld(*objs)
    main = page_hero(p) + f"""
<section class="section on-light">
  <div class="wrap layout">
    <article class="prose">{body}{faq_html(faq) if faq else ""}</article>
    {aside(p, nav)}
  </div>
</section>{after}""" + (cta_band(cur) if cta else "")
    write(p, main)


PRAKTIJK_NAV = ("Praktijk", PRAKTIJK)
INFO_NAV = ("Patiënteninfo", INFO)


def other_pages():
    # Over de praktijk
    text_page("homepage/praktijkinformatie/", [("", "Home"), ("homepage/praktijkinformatie/", "Over de praktijk")], "praktijk",
              "Over de praktijk | Tandartspraktijk Slotplantsoen in Meppel",
              "Tandartspraktijk Slotplantsoen in het centrum van Meppel: algemene tandheelkunde, esthetiek, orthodontie en implantologie, met CBCT en eigen tandtechnisch lab.",
              'Welkom bij Tandartspraktijk <em class="g">Slotplantsoen</em>',
              "Een klantgerichte tandartspraktijk midden in Meppel. Met persoonlijke aandacht, vertrouwde zorg en alle specialismen onder één dak.",
              f"""
<h2>Persoonlijke aandacht, vertrouwde zorg</h2>
<p>Tandartspraktijk Slotplantsoen biedt algemene tandheelkunde, esthetische tandheelkunde, orthodontie en implantologie. Preventie heeft bij ons een belangrijke plek: met regelmatige controles en een goede mondhygiëne voorkomen we samen dat kleine problemen groot worden.</p>
<p>We nemen de tijd voor u, leggen vooraf uit wat we gaan doen en wat het kost, en stemmen de behandeling af op uw wensen. Zo werken we samen aan een gezonde glimlach.</p>
<figure><img src="{{a:assets/img/praktijk-gevel.webp}}" alt="De entree van Tandartspraktijk Slotplantsoen in Meppel" width="1100" height="736" loading="lazy" decoding="async"><figcaption>Onze praktijk aan het Slotplantsoen 1a, in het centrum van Meppel.</figcaption></figure>
<h2>Alles onder één dak</h2>
<ul class="types">
  <li><b>Vijf tandartsen</b><span>Met aandachtsgebieden als implantologie, orthodontie en esthetiek.</span></li>
  <li><b>Preventie</b><span>(Paro-)preventieassistenten voor gebitsreiniging en tandvleeszorg.</span></li>
  <li><b>Tandprothetici</b><span>Kunstgebit en klikgebit op maat, reparaties in eigen lab.</span></li>
  <li><b>Tandtechnisch lab</b><span>Kronen, bruggen en facings worden in huis gemaakt.</span></li>
  <li><b>CBCT-scanner</b><span>3D-röntgenbeelden voor implantaten, wortelkanalen en meer.</span></li>
  <li><b>Avondspreekuur</b><span>Op maandag geopend tot 20:00 uur.</span></li>
</ul>
<h2>Halfjaarlijkse controle</h2>
<p>We adviseren onze patiënten om twee keer per jaar op controle te komen. Zo houden we uw gebit en tandvlees goed in de gaten en zijn we er snel bij als er iets is. Nieuw bij ons? <a href="{{u:inschrijven-als-nieuwe-patient/}}">Schrijf u in als nieuwe patiënt</a>.</p>
""", img="team/brigitte.webp", img_alt="Brigitte Hendriks, praktijkmanager", nav=PRAKTIJK_NAV, extra_schema=[dentist_schema(True)])

    # Spoed
    text_page("homepage/spoedgevallen-en-weekenddienst/", [("", "Home"), ("homepage/spoedgevallen-en-weekenddienst/", "Spoed en weekenddienst")], "info",
              "Spoed tandarts Meppel | Avond- en weekenddienst | Slotplantsoen",
              "Kiespijn of een spoedgeval? Bel Tandartspraktijk Slotplantsoen in Meppel op 0522-247436. Buiten openingstijden kunt u terecht bij de dienstdoende tandarts.",
              'Pijn of een <em class="g">spoedgeval?</em>',
              "Wacht bij pijnklachten niet tot uw volgende controle. Bel ons direct, dan zoeken we samen naar een snelle oplossing.",
              f"""
<h2>Tijdens openingstijden</h2>
<p>Bel <a href="{TEL_HREF}"><b>{TEL}</b></a>, bij voorkeur tussen <b>08:30 en 10:00 uur</b>. Dan proberen we u nog dezelfde dag te helpen. Tussen 12:00 en 13:30 uur zijn we alleen bereikbaar op <a href="tel:+31627443039">06-27443039</a>.</p>
<h2>Buiten openingstijden, ’s avonds en in het weekend</h2>
<p>Is de praktijk gesloten, dan kunt u bij spoedgevallen terecht bij de <b>dienstdoende tandarts</b>. Als u ons nummer belt, hoort u op het antwoordapparaat het nummer van de tandarts die dienst heeft. U kunt ook de spoeddienst bellen via <b>0900-8602</b>.</p>
<div class="note">
<p><b>Goed om te weten</b></p>
<ul>
  <li>Een bezoek aan de spoeddienst in de avond of het weekend brengt extra kosten met zich mee.</li>
  <li>Deze kosten moet u soms direct contant of met de pin afrekenen.</li>
  <li>Neem uw zorgpas en identiteitsbewijs mee.</li>
</ul>
</div>
<h2>Wat is een spoedgeval?</h2>
<ul>
  <li>hevige kiespijn die niet overgaat met een gewone pijnstiller;</li>
  <li>een dikke wang of zwelling, eventueel met koorts;</li>
  <li>een nabloeding na het trekken van een tand of kies;</li>
  <li>een ongeluk waarbij een tand is afgebroken of uit de mond is geslagen.</li>
</ul>
<p>Is er een tand uit de mond geslagen? Pak hem vast aan de kroon (niet aan de wortel), bewaar hem in melk of in uw mond tegen de wang en bel direct.</p>
""", nav=INFO_NAV)

    # Tarieven
    text_page("homepage/tarieven-en-betaling/", [("", "Home"), ("homepage/tarieven-en-betaling/", "Tarieven en betaling")], "info",
              "Tarieven en betaling | Tandartspraktijk Slotplantsoen Meppel",
              "Tarieven van Tandartspraktijk Slotplantsoen volgens de NZa. Betalen via Infomedics, binnen 30 dagen, met mogelijkheid tot betalingsregeling. Begroting op aanvraag.",
              'Tarieven en <em class="g">betaling</em>', "Duidelijkheid vooraf: u weet wat een behandeling kost en hoe u betaalt.",
              """
<h2>Tarieven volgens de NZa</h2>
<p>De tarieven voor tandheelkundige zorg worden elk jaar vastgesteld door de Nederlandse Zorgautoriteit (NZa). Iedere tandarts in Nederland rekent dezelfde codes. Op uw nota staat bij elke behandeling de bijbehorende code.</p>
<div class="note"><p><b>Begroting.</b> Voor elke behandeling kunt u vooraf een begroting krijgen. Bij behandelingen boven de € 250 kunt u om een schriftelijke begroting vragen.</p></div>
<h2>Betalen via Infomedics</h2>
<p>De nota’s worden verzorgd door Infomedics. Zij sturen u de rekening en verzorgen de incasso.</p>
<ul>
  <li>U heeft <b>30 dagen</b> om de nota te betalen.</li>
  <li>Lukt dat niet in één keer? Via de website van Infomedics kunt u online een <b>betalingsregeling</b> aanvragen.</li>
  <li>Met de <b>rekeningchecker</b> op <a href="https://www.infomedics.nl" rel="noopener" target="_blank">infomedics.nl</a> ziet u met het referentienummer van uw nota of deze is betaald.</li>
  <li>Vragen over uw nota? De servicedesk van Infomedics is bereikbaar op <a href="tel:+31362031900">036-20 31 900</a> (ma t/m vr 09:00-17:00 uur). Antwoorden op veelgestelde vragen vindt u op infomedics.nl/faq.</li>
</ul>
<p>Onze baliemedewerkers vertellen u graag meer over de betalingsvoorwaarden.</p>
<h2>Afspraak verzet of vergeten?</h2>
<p>Afspraken moeten minstens <b>24 uur van tevoren</b> worden afgezegd. Afspraken die niet of te laat zijn afgezegd, kunnen in rekening worden gebracht. Verzetten en afzeggen kan alleen telefonisch.</p>
""", nav=INFO_NAV)

    # Verzekering
    text_page("homepage/betalen-en-vergoedingen/", [("", "Home"), ("homepage/betalen-en-vergoedingen/", "Verzekering en vergoedingen")], "info",
              "Verzekering en vergoedingen tandarts | Slotplantsoen Meppel",
              "Wat vergoedt de basisverzekering bij de tandarts en wanneer heeft u een aanvullende tandartsverzekering nodig? Uitleg voor volwassenen en kinderen tot 18 jaar.",
              'Verzekering en <em class="g">vergoedingen</em>', "Wat vergoedt uw zorgverzekering bij de tandarts? Een overzicht, zodat u een goede keuze kunt maken.",
              """
<h2>Basisverzekering</h2>
<ul>
  <li>Voor volwassenen vergoedt de basisverzekering maar een beperkt deel van de tandheelkundige zorg.</li>
  <li>Volledige kunstgebitten en klikgebitten worden grotendeels vergoed uit de basisverzekering.</li>
  <li>Het eigen risico geldt alleen voor zorg uit de basisverzekering.</li>
  <li>Vraag bij uw zorgverzekeraar na welke vergoeding u precies krijgt.</li>
</ul>
<h2>Kinderen tot 18 jaar</h2>
<p>Voor kinderen tot 18 jaar valt de mondzorg onder de basisverzekering. Uitzonderingen zijn beugels, kronen en bruggen.</p>
<h2>Aanvullende tandartsverzekering</h2>
<p>Een aanvullende tandartsverzekering is niet verplicht. U bepaalt zelf of en hoe uitgebreid u zich verzekert. Let daarbij op:</p>
<ul>
  <li>welke behandelingen worden vergoed en tot welk bedrag per jaar, veel verzekeringen hebben een jaarmaximum;</li>
  <li>wachttijden: sommige verzekeringen vergoeden bijvoorbeeld een beugel pas na een wachttijd;</li>
  <li>of de vergoeding bij uw eigen tandarts verandert als u overstapt naar een andere verzekeraar.</li>
</ul>
<div class="note"><p><b>Tip.</b> Vergelijk de polisvoorwaarden elk jaar; ze veranderen regelmatig. Bespreek met uw tandarts welke behandelingen er het komende jaar aankomen en kies daar uw verzekering op. Zeg uw oude verzekering pas op als de nieuwe u heeft geaccepteerd.</p></div>
""", nav=INFO_NAV)

    # Huisregels
    text_page("homepage/huisregels/", [("", "Home"), ("homepage/huisregels/", "Huisregels")], "info",
              "Huisregels | Tandartspraktijk Slotplantsoen Meppel",
              "Huisregels van Tandartspraktijk Slotplantsoen: afspraken afzeggen, pijnklachten, prothesereparaties, medische gegevens, privacy en betaling.",
              'Onze <em class="g">huisregels</em>', "Een paar afspraken die ervoor zorgen dat alles prettig en duidelijk verloopt, voor u en voor ons.",
              """
<h2>Afspraken afzeggen</h2>
<p>Kunt u niet komen? Zeg uw afspraak dan minstens <b>24 uur van tevoren</b> telefonisch af. Niet of te laat afgezegde afspraken kunnen in rekening worden gebracht.</p>
<h2>Pijnklachten</h2>
<p>Heeft u pijn, wacht dan niet tot uw volgende controle maar neem direct contact op. Bel bij voorkeur tussen 08:30 en 10:00 uur, dan proberen we u dezelfde dag te helpen. Is de praktijk gesloten, dan hoort u op het antwoordapparaat het nummer van de dienstdoende tandarts.</p>
<h2>Reparatie van protheses</h2>
<p>Reparaties gebeuren in ons eigen laboratorium:</p>
<ul>
  <li>maandag t/m woensdag: brengen vóór 09:30 uur, ophalen om 12:00 uur;</li>
  <li>donderdag: brengen vanaf 13:30 uur, ophalen om 16:00 uur;</li>
  <li>vrijdag: geen reparaties mogelijk.</li>
</ul>
<h2>Medische gegevens</h2>
<p>Meld medische bijzonderheden altijd aan uw behandelaar, zoals zwangerschap, medicijngebruik, ziekten en infecties. Dat is belangrijk voor uw veiligheid en die van anderen. Bij uw eerste bezoek vult u een gezondheidsvragenlijst in.</p>
<h2>Privacy</h2>
<p>Uw gegevens worden niet aan derden verstrekt. Een verwijzing naar een andere zorgverlener gebeurt alleen in overleg met u. Lees ook onze <a href="{u:privacyverklaring/}">privacyverklaring</a>.</p>
<h2>Tevredenheid</h2>
<p>We meten regelmatig hoe tevreden onze patiënten zijn. Heeft u een opmerking of suggestie? Laat het weten aan de balie of aan uw behandelaar.</p>
<h2>Betaling</h2>
<p>Betalingen lopen via Infomedics (<a href="tel:+31362031900">036-20 31 900</a>). Voor elke behandeling kunt u vooraf een begroting krijgen; boven de € 250 ook schriftelijk. Meer over <a href="{u:homepage/tarieven-en-betaling/}">tarieven en betaling</a>.</p>
""", nav=INFO_NAV)

    # CBCT
    text_page("cbct-rontgen/", [("", "Home"), ("homepage/praktijkinformatie/", "Praktijk"), ("cbct-rontgen/", "CBCT-scan")], "praktijk",
              "CBCT-scan Meppel | 3D-röntgenfoto in de praktijk | Slotplantsoen",
              "Tandartspraktijk Slotplantsoen in Meppel heeft een eigen Cone Beam CT-scanner: minder straling, korte scantijd en direct een betrouwbaar 3D-beeld van kaak en gebit.",
              'CBCT-scan: uw kaak in <em class="g">3D</em>',
              "Onze praktijk beschikt over een Cone Beam CT-scanner. Daarmee maken we een driedimensionaal röntgenbeeld van de kaken, het gebit, de bijholtes en de kaakgewrichten.",
              f"""
<h2>Wat is een Cone Beam CT-scan?</h2>
<p>Een Cone Beam CT-scan is een speciaal soort CT-scan voor het hoofd-halsgebied. Met röntgenstralen wordt een driedimensionaal beeld gemaakt van de aangezichtsschedel, de holtes in uw hoofd, de onder- en bovenkaak en de kaakkopjes. Afwijkingen die op een gewone röntgenfoto niet zichtbaar zijn, worden zo duidelijk.</p>
<ul class="types">
  <li><b>Minder straling</b><span>Veel minder röntgenstraling dan bij een normale CT-scan.</span></li>
  <li><b>Snel</b><span>Het scannen zelf duurt ongeveer een minuut.</span></li>
  <li><b>Direct 3D</b><span>Na computerreconstructie direct betrouwbare driedimensionale beelden.</span></li>
</ul>
<figure><img src="{{a:assets/img/cbct.webp}}" alt="Cone Beam CT-scanner van Tandartspraktijk Slotplantsoen" width="900" height="588" loading="lazy" decoding="async"></figure>
<h2>Wanneer krijgt u een CBCT-scan?</h2>
<ul>
  <li>bij het plannen van een <a href="{{u:behandelingen/implantaten/}}">implantaat</a>: hoeveel kaakbot is er en hoe liggen eerder geplaatste implantaten?</li>
  <li>bij een tand of kies die nog in het kaakbot ligt, en de ligging van zenuwen daaromheen;</li>
  <li>bij het beoordelen van de bijholtes en een bijholteontsteking;</li>
  <li>voor een orthodontische behandeling of een chirurgische kaakcorrectie;</li>
  <li>bij onderzoek van de kaakgewrichten of van bot dat door een infectie is aangetast;</li>
  <li>na een ongeluk of trauma in het gezicht.</li>
</ul>
<h2>Hoe verloopt het onderzoek?</h2>
<ol>
  <li>U meldt zich op de afgesproken tijd bij de balie. De assistente haalt u op uit de wachtruimte en vertelt wat er gaat gebeuren.</li>
  <li>Metalen voorwerpen en sieraden in het hoofd-halsgebied verstoren het beeld. Die doet u daarom af, net als een uitneembare prothese.</li>
  <li>U staat of zit stil achter het apparaat. Een röntgenbuis draait in ongeveer één minuut om u heen en maakt opnames uit steeds een andere hoek; u hoort een zoemend geluid.</li>
</ol>
<div class="note"><p><b>Bent u tandarts of specialist?</b> U kunt uw patiënten bij ons laten scannen. <a href="{{u:doorverwijzing-cbct-scan-voor-behandelaars/}}">Verwijs een patiënt door</a>.</p></div>
""", img="cbct.webp", img_alt="CBCT-scanner in de praktijk", nav=PRAKTIJK_NAV,
              faq=[("Is een CBCT-scan veilig?", "Ja. Een Cone Beam CT-scan gebruikt veel minder straling dan een gewone CT-scan in het ziekenhuis. We maken alleen een scan als dat voor uw behandeling echt meerwaarde heeft."),
                   ("Hoe lang duurt een CBCT-scan?", "Het apparaat draait ongeveer één minuut om u heen. Met voorbereiding bent u meestal binnen een kwartier klaar."),
                   ("Moet ik voor een CBCT-scan naar het ziekenhuis?", "Nee, de scanner staat bij ons in de praktijk aan het Slotplantsoen in Meppel.")])

    # Kinderen
    text_page("kinderen-en-de-tandarts/", [("", "Home"), ("homepage/praktijkinformatie/", "Praktijk"), ("kinderen-en-de-tandarts/", "Kinderen en de tandarts")], "praktijk",
              "Kindertandarts Meppel | Kinderen en de tandarts | Slotplantsoen",
              "Met uw kind naar de tandarts in Meppel? Vanaf twee jaar is uw kind welkom bij Tandartspraktijk Slotplantsoen. Tips om het eerste bezoek ontspannen te laten verlopen.",
              'Kinderen en de <em class="g">tandarts</em>',
              "Bij kinderen draait het om vertrouwen. Op een speelse manier laten we uw kind wennen aan de praktijk, zodat het later net zo ontspannen in de stoel zit.",
              f"""
<h2>Het eerste bezoek</h2>
<p>Neem uw kind vanaf ongeveer <b>twee jaar</b> mee naar de controle. Uw kind mag rondkijken en wennen aan de praktijk en aan ons. Op die leeftijd is meestal nog geen behandeling nodig: de tandarts kijkt in het mondje, telt de tandjes en geeft advies over poetsen en voeding. Ook onze preventieassistenten helpen daarbij graag.</p>
<p>Tip: neem uw kind ook eens mee als u zelf op controle komt. Ziet het dat papa of mama ook in de stoel gaat zitten, dan voelt het vertrouwd.</p>
<figure><img src="{{a:assets/img/kindertandarts.webp}}" alt="Tandarts laat een jong meisje op speelse wijze kennismaken met de behandelstoel" width="600" height="400" loading="lazy" decoding="async"></figure>
<h2>Voorbereiden thuis</h2>
<ul>
  <li>Vertel op het niveau van uw kind wat het gaat zien: de stoel, de lamp, de tandarts en de assistente.</li>
  <li>Geef vooral een gevoel van veiligheid en ga niet te veel in detail.</li>
  <li>Begin bij kinderen jonger dan vier jaar niet over behandelingen.</li>
  <li>Vertel de tandarts wat uw kind al weet, bijvoorbeeld over tandenpoetsen.</li>
  <li>Vindt u de tandarts zelf spannend? Laat dan een andere volwassene meegaan, of overleg vooraf met ons.</li>
</ul>
<h2>Gaatjes in het melkgebit</h2>
<p>Gaatjes zijn het meest voorkomende probleem bij kinderen, en ze beginnen meestal in de kiezen. Een groter gaatje kan pijn en ontstekingen geven en zelfs het blijvende gebit beschadigen. Daarom vult de tandarts een gaatje meestal, zodat het niet verder groeit. Bij heel kleine gaatjes is advies over voeding en poetsen soms genoeg; tanden die binnenkort wisselen, behandelen we meestal niet.</p>
<div class="note"><p><b>Eerlijk is het fijnst.</b> Leg rustig uit dat een tand ‘ziek’ is en dat de tandarts hem beter maakt, en laat de tandarts zelf vertellen wat er gaat gebeuren. Maak een behandeling niet mooier dan hij is: dat kan het vertrouwen schaden en een volgende keer juist spannender maken.</p></div>
<p>Twee controles per jaar zijn voor de meeste kinderen voldoende. Voor kinderen tot 18 jaar valt de mondzorg onder de basisverzekering (behalve beugels, kronen en bruggen).</p>
""", img="kinderen.webp", img_alt="Meisje met tandenborstel bij de tandarts", nav=PRAKTIJK_NAV,
              faq=[("Vanaf welke leeftijd kan mijn kind naar de tandarts?", "Vanaf ongeveer twee jaar. Het eerste bezoek is vooral kennismaken en wennen."),
                   ("Hoe vaak moet mijn kind op controle?", "Meestal is twee keer per jaar voldoende. De tandarts geeft aan of vaker nodig is."),
                   ("Wat kost de tandarts voor kinderen?", "Voor kinderen tot 18 jaar valt de mondzorg onder de basisverzekering, zonder eigen risico. Beugels, kronen en bruggen vallen daarbuiten.")])

    # Angst
    text_page("angst-voor-de-tandarts/", [("", "Home"), ("homepage/praktijkinformatie/", "Praktijk"), ("angst-voor-de-tandarts/", "Angst voor de tandarts")], "praktijk",
              "Angst voor de tandarts? | Rustige tandarts in Meppel",
              "Bang voor de tandarts? Bij Tandartspraktijk Slotplantsoen in Meppel nemen we de tijd, leggen alles vooraf uit en bepaalt u het tempo. Lees hoe we u helpen.",
              'Angst voor de <em class="g">tandarts?</em>',
              "U bent zeker niet de enige. Een groot deel van de mensen vindt een bezoek aan de tandarts min of meer spannend. Wij nemen dat serieus.",
              """
<h2>Waar komt de angst vandaan?</h2>
<p>Angst voor de tandarts heeft vaak een reden: een vervelende ervaring of pijn in het verleden, of schaamte over de staat van het gebit. Ook het geluid van de boor, bepaalde geuren en het gevoel geen controle te hebben, spelen vaak mee.</p>
<h2>Zo maken we het u makkelijker</h2>
<ul class="types">
  <li><b>Tijd en rust</b><span>We nemen voldoende tijd voor u en zorgen voor een rustige, warme ontvangst.</span></li>
  <li><b>Kort wachten</b><span>We houden de wachttijd zo kort mogelijk, zodat u niet lang hoeft te piekeren.</span></li>
  <li><b>Eigen muziek</b><span>Neem een koptelefoon mee en luister naar uw eigen muziek, ook tijdens de behandeling.</span></li>
  <li><b>Vooraf uitleg</b><span>We stellen het behandelplan samen met u op en leggen uit wat er gaat gebeuren.</span></li>
  <li><b>Goed verdoofd</b><span>Behandelingen zijn tegenwoordig vrijwel pijnloos. Voelt u toch iets, dan verdoven we extra.</span></li>
  <li><b>Uw stopteken</b><span>Spreek vooraf af hoe u aangeeft dat we even moeten stoppen, bijvoorbeeld door uw hand op te steken.</span></li>
</ul>
<blockquote>Uw wensen nemen we serieus. U bepaalt het tempo.</blockquote>
<p>Vertel het ons gerust als u het spannend vindt, bij het maken van de afspraak of als u in de stoel zit. Dan houden we er vanaf het begin rekening mee.</p>
""", img="ontspannen.webp", img_alt="Ontspannen patiënte in de tandartsstoel", nav=PRAKTIJK_NAV,
              faq=[("Kan ik eerst alleen kennismaken?", "Ja. U kunt een afspraak maken om eerst kennis te maken en te bespreken wat u spannend vindt, zonder dat er meteen behandeld wordt."),
                   ("Wat als ik me schaam voor mijn gebit?", "Daar hoeft u zich bij ons niet voor te schamen. We oordelen niet en kijken samen met u naar de beste volgende stap.")])

    # Vacatures
    text_page("vacatures/", [("", "Home"), ("homepage/praktijkinformatie/", "Praktijk"), ("vacatures/", "Vacatures")], "praktijk",
              "Vacatures | Werken bij Tandartspraktijk Slotplantsoen Meppel",
              "Werken bij Tandartspraktijk Slotplantsoen in Meppel? Wij zoeken een tandartsassistente voor 16 tot 32 uur per week. Stuur uw cv en motivatie.",
              'Werken bij <em class="g">Slotplantsoen</em>', "Een hecht team, afwisselend werk en alle disciplines onder één dak. Kom ons versterken.",
              f"""
<h2>Tandartsassistente <span style="display:block;font:500 1rem var(--sans);color:var(--ink-2)">16 tot 32 uur per week</span></h2>
<p>Voor onze praktijk in het centrum van Meppel zoeken we een enthousiaste tandartsassistente. Je werkt in een team met tandartsen, preventieassistenten, tandprothetici en een tandtechnieker, in een praktijk met een eigen CBCT-scanner en laboratorium.</p>
<h3>Solliciteren</h3>
<p>Stuur je cv en motivatie naar <a href="mailto:{MAIL}?subject=Sollicitatie%20tandartsassistente">{MAIL}</a>, t.a.v. Brigitte Hendriks. Vragen? Bel praktijkmanager Brigitte Hendriks op <a href="{TEL_HREF}">{TEL}</a>.</p>
<div class="note"><p>Staat jouw functie er niet tussen? Een open sollicitatie is ook welkom.</p></div>
""", img="team/brigitte.webp", img_alt="Brigitte Hendriks, praktijkmanager", nav=PRAKTIJK_NAV, cta=False,
              extra_schema=[dentist_schema(False), {"@type": "JobPosting", "title": "Tandartsassistente", "description": "<p>Tandartsassistente voor 16 tot 32 uur per week bij Tandartspraktijk Slotplantsoen in Meppel. Stuur je cv en motivatie naar info@praktijkslotplantsoen.nl, t.a.v. Brigitte Hendriks.</p>",
                                                    "datePosted": TODAY, "employmentType": "PART_TIME", "hiringOrganization": {"@type": "Organization", "name": NAME, "sameAs": BASE, "logo": BASE + "assets/img/icon-512.png"},
                                                    "jobLocation": {"@type": "Place", "address": {"@type": "PostalAddress", "streetAddress": "Slotplantsoen 1a", "postalCode": "7941 LP", "addressLocality": "Meppel", "addressRegion": "Drenthe", "addressCountry": "NL"}}}])

    # Privacy
    text_page("privacyverklaring/", [("", "Home"), ("privacyverklaring/", "Privacyverklaring")], None,
              "Privacyverklaring | Tandartspraktijk Slotplantsoen",
              "Hoe Tandartspraktijk Slotplantsoen in Meppel omgaat met uw persoonsgegevens, conform de AVG en de WGBO.",
              "Privacyverklaring", "Wij gaan zorgvuldig om met uw gegevens. Hier leest u welke gegevens we verwerken, waarom, en wat uw rechten zijn.",
              f"""
<h2>Wie zijn wij?</h2>
<p>{NAME}, Slotplantsoen 1a, 7941 LP Meppel, is verantwoordelijk voor de verwerking van persoonsgegevens zoals beschreven in deze verklaring. Vragen? Mail naar <a href="mailto:{MAIL}">{MAIL}</a> of bel <a href="{TEL_HREF}">{TEL}</a>.</p>
<h2>Welke gegevens verwerken wij?</h2>
<ul>
  <li><b>Patiëntendossier:</b> naam, geboortedatum, adres, contactgegevens, BSN, verzekeringsgegevens en uw medische en tandheelkundige gegevens. Dit is wettelijk verplicht op grond van de WGBO.</li>
  <li><b>Formulieren op deze website:</b> de gegevens die u invult bij een afspraakverzoek, inschrijving of vraag. Die gebruiken we alleen om uw aanvraag af te handelen.</li>
</ul>
<h2>Bewaartermijn</h2>
<p>Medische dossiers bewaren we zo lang als de wet voorschrijft (in de regel twintig jaar). Gegevens uit contactformulieren die niet tot een behandeling leiden, verwijderen we zodra ze niet meer nodig zijn.</p>
<h2>Delen met anderen</h2>
<p>We verstrekken uw gegevens niet aan derden, tenzij dat nodig is voor uw behandeling (bijvoorbeeld een verwijzing, altijd in overleg met u), voor de facturatie via Infomedics, of als de wet ons daartoe verplicht.</p>
<h2>Cookies en kaarten</h2>
<p>Deze website plaatst geen tracking- of advertentiecookies. De kaart van Google Maps wordt pas geladen nadat u daarvoor kiest; Google kan dan gegevens verwerken volgens zijn eigen privacybeleid.</p>
<h2>Uw rechten</h2>
<p>U heeft het recht om uw gegevens in te zien, te laten corrigeren of (waar de wet dat toestaat) te laten verwijderen. Neem daarvoor contact met ons op. Heeft u een klacht over de verwerking van uw gegevens, dan kunt u die ook indienen bij de Autoriteit Persoonsgegevens.</p>
""", cta=False)


def forms_pages():
    # Afspraak maken
    cur = "afspraak-maken/"
    soort = [("controle", "Controle"), ("klacht", "Klacht of pijn (niet acuut)"), ("preventie", "Gebitsreiniging of preventie"),
             ("intake-orthodontie", "Gratis intake orthodontie"), ("intake-invisalign", "Gratis intake Invisalign"),
             ("intake-prothese", "Gratis intake prothese of klikgebit"), ("implantaat", "Consult implantaat"), ("esthetisch", "Consult esthetiek of bleken"),
             ("prothese-reparatie", "Reparatie prothese"), ("anders", "Anders")]
    inner = (group("Waarvoor komt u?",
                   choice("soort", "Soort afspraak", soort, param="soort") +
                   choice("patient", "Bent u al patiënt bij ons?", [("ja", "Ja"), ("nee", "Nee, ik ben nieuw")])) +
             group("Wanneer komt het u uit?",
                   checks("dagen", "Voorkeursdagen", ["Maandag", "Dinsdag", "Woensdag", "Donderdag"]) +
                   checks("dagdeel", "Voorkeur dagdeel", ["Ochtend", "Middag", "Maandagavond"])) +
             group("Uw gegevens",
                   field("naam", "Naam", ac="name") + field("geboortedatum", "Geboortedatum", "date", ac="bday") +
                   field("telefoon", "Telefoonnummer", "tel", ac="tel", err="Vul een geldig telefoonnummer in.") +
                   field("email", "E-mailadres", "email", ac="email", err="Vul een geldig e-mailadres in.") +
                   field("opmerking", "Toelichting", "textarea", req=False, full=True)))
    form = form_wrap(cur, "Afspraakverzoek via website", inner,
                     "Uw e-mailprogramma is geopend met uw afspraakverzoek. Er is nog niets verstuurd: verstuur de e-mail om af te ronden.", "Afspraak aanvragen")
    side = f"""
<h2 class="fp__h">Liever bellen?</h2>
<a class="fp__tel" href="{TEL_HREF}">{TEL}</a>
<p>Maandag tot en met donderdag van 08:30 tot 12:30 en van 13:30 tot 16:30 uur. Tussen 12:00 en 13:30 uur alleen op <a href="tel:+31627443039">06-27443039</a>.</p>
<dl class="fp__facts">
  <div><dt>E-mail</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd></div>
  <div><dt>Verzetten of afzeggen</dt><dd>Alleen telefonisch, minstens 24 uur van tevoren.</dd></div>
</dl>
<div class="fp__alert">{icon("alert")}<p><b>Pijn of spoed?</b> Gebruik niet het formulier, maar bel direct. Buiten openingstijden: <a href="{{u:homepage/spoedgevallen-en-weekenddienst/}}">spoed en weekenddienst</a>.</p></div>"""
    form_page(cur, [("", "Home"), (cur, "Afspraak maken")],
              "Afspraak maken | Tandartspraktijk Slotplantsoen Meppel",
              "Maak een afspraak bij Tandartspraktijk Slotplantsoen in Meppel: bel 0522-247436, mail of vraag online een afspraak aan. Ook voor een gratis intake.",
              "Afspraak maken",
              "Kies waarvoor u komt en wanneer het u uitkomt. Wij bellen of mailen u om de afspraak te bevestigen.",
              side, form, "Afspraak aanvragen")

    # Inschrijven
    cur = "inschrijven-als-nieuwe-patient/"
    inner = (group("Uw gegevens",
                   field("naam", "Naam", ac="name") + field("geboortedatum", "Geboortedatum", "date", ac="bday") +
                   field("telefoon", "Telefoonnummer", "tel", ac="tel", err="Vul een geldig telefoonnummer in.") +
                   field("email", "E-mailadres", "email", ac="email", err="Vul een geldig e-mailadres in.") +
                   field("adres", "Adres en woonplaats", full=True, ac="street-address")) +
             group("Waarom schrijft u zich in?",
                   choice("reden", "Reden van uw inschrijving", [("verhuisd", "Ik ben verhuisd"), ("geen-tandarts", "Ik heb nu geen tandarts"), ("overstappen", "Ik wil overstappen"), ("behandeling", "Voor een specifieke behandeling"), ("anders", "Anders")]) +
                   field("vorige", "Vorige tandarts", req=False, full=True)) +
             group("Schrijft u meer gezinsleden in?",
                   field("gezin", "Gezinsleden", "textarea", req=False, full=True, hint="Naam en geboortedatum per gezinslid.") +
                   field("opmerking", "Opmerkingen", "textarea", req=False, full=True)))
    form = form_wrap(cur, "Inschrijving nieuwe patiënt via website", inner,
                     "Uw e-mailprogramma is geopend met uw inschrijving. Er is nog niets verstuurd: verstuur de e-mail om af te ronden.", "Inschrijving versturen")
    side = f"""
<h2 class="fp__h">Zo gaat het</h2>
<ol class="fp__steps">
  <li><b>Inschrijven</b><span>U vult het formulier in, voor uzelf of het hele gezin.</span></li>
  <li><b>Uitnodiging</b><span>Wij verwerken uw inschrijving en nodigen u uit voor een eerste consult.</span></li>
  <li><b>Eerste consult</b><span>Dit duurt iets langer dan een gewone controle. U vult een medische vragenlijst in (neem de namen van uw medicijnen mee), we bespreken uw tandheelkundige voorgeschiedenis en onderzoeken uw gebit, tandvlees, kaakbot, beet en kauwfunctie. Zo nodig maken we digitale röntgenfoto’s; die maken we normaal eens per twee jaar, of eerder bij klachten.</span></li>
</ol>
<div class="fp__alert">{icon("user")}<p><b>Neem mee naar het eerste consult:</b> uw identiteitsbewijs en zorgpas. Uw BSN noteren we dan; dat hoeft u niet via de website te sturen.</p></div>
<p class="fp__call">Vragen over inschrijven? Bel <a href="{TEL_HREF}">{TEL}</a>.</p>"""
    form_page(cur, [("", "Home"), (cur, "Inschrijven")],
              "Inschrijven bij de tandarts in Meppel | Nieuwe patiënten welkom",
              "Op zoek naar een tandarts in Meppel? Tandartspraktijk Slotplantsoen neemt weer nieuwe patiënten aan. Schrijf u en uw gezin online in in twee minuten.",
              "Inschrijven als nieuwe patiënt",
              "Goed nieuws: we nemen weer nieuwe patiënten aan. Schrijf uzelf of uw hele gezin in; daarna nodigen we u uit voor een eerste consult.",
              side, form, "Inschrijfformulier")

    # Contact
    cur = "contact/"
    inner = (field("naam", "Naam", ac="name") + field("email", "E-mailadres", "email", ac="email", err="Vul een geldig e-mailadres in.") +
             field("telefoon", "Telefoonnummer", "tel", req=False, ac="tel", err="Vul een geldig telefoonnummer in.") +
             field("onderwerp", "Onderwerp", req=False) + field("bericht", "Uw vraag", "textarea", full=True))
    form = form_wrap(cur, "Vraag via website", inner, "Uw e-mailprogramma is geopend met uw vraag. Er is nog niets verstuurd: verstuur de e-mail om af te ronden.", "Vraag versturen")
    crumbs = [("", "Home"), (cur, "Contact")]
    p = dict(path=cur, title="Contact & openingstijden | Tandarts Meppel | Slotplantsoen",
             desc="Contact met Tandartspraktijk Slotplantsoen, Slotplantsoen 1a, 7941 LP Meppel. Bel 0522-247436 of mail info@praktijkslotplantsoen.nl. Openingstijden en route.",
             h1='Contact en <em class="g">openingstijden</em>', lead="U vindt ons midden in het centrum van Meppel. Bel, mail of kom langs, we helpen u graag.",
             crumbs=crumbs)
    p["schema"] = ld({"@type": "ContactPage", "@id": BASE + cur + "#webpage", "url": BASE + cur, "name": p["title"], "inLanguage": "nl-NL", "about": {"@id": BASE + "#praktijk"}},
                     breadcrumb_schema(crumbs), dentist_schema(True))
    main = page_hero(p, cta=False) + f"""
<section class="section on-light">
  <div class="wrap contact">
    <div>
      <div class="card" style="margin-bottom:22px">{contact_dl(cur)}</div>
      <h2 style="font-size:1.7rem">Openingstijden praktijk</h2>
      <p><span class="status" data-status></span></p>
      {hours_table()}
      <p style="color:var(--ink-2);font-size:.95rem;margin-top:14px">Telefonisch bereikbaar: maandag t/m donderdag 08:30-12:30 en 13:30-16:30 uur. Verzetten of afzeggen van afspraken kan alleen telefonisch.</p>
      <div class="alert">{icon("alert")}<div><b>Spoed buiten openingstijden?</b> U hoort op ons antwoordapparaat het nummer van de dienstdoende tandarts. <a href="{{u:homepage/spoedgevallen-en-weekenddienst/}}">Lees meer over spoed</a></div></div>
    </div>
    <div>
      {map_block()}
      <div class="card" style="margin-top:22px">
        <h2 style="font-size:1.7rem">Stel een vraag</h2>
        <p style="color:var(--ink-2)">Niet voor spoed of afspraken: gebruik daarvoor de telefoon of het <a href="{{u:afspraak-maken/}}">afspraakformulier</a>.</p>
        {form}
      </div>
    </div>
  </div>
</section>"""
    write(p, main)

    # Verwijzers CBCT
    cur = "doorverwijzing-cbct-scan-voor-behandelaars/"
    inner = (field("praktijk", "Uw naam en praktijk") + field("telefoon", "Telefoonnummer", "tel", err="Vul een geldig telefoonnummer in.") +
             field("email", "E-mailadres", "email", err="Vul een geldig e-mailadres in.") + field("plaats", "Adres en plaats") +
             field("pnaam", "Naam patiënt") + field("pgeb", "Geboortedatum patiënt", "date") + field("ptel", "Telefoonnummer patiënt", "tel", err="Vul een geldig telefoonnummer in.") +
             field("indicatie", "Indicatie", "select", opts=[(v.lower(), v) for v in ["Implantologie", "Kaakchirurgie", "Orthodontie", "Endodontologie", "Gnathologie", "Anders"]]) +
             field("regio", "Regio en toelichting", "textarea", full=True))
    form = form_wrap(cur, "Verwijzing CBCT-scan", inner, "Uw e-mailprogramma is geopend met uw verwijzing. Er is nog niets verstuurd: verstuur de e-mail om af te ronden.", "Verwijzing versturen")
    text_page(cur, [("", "Home"), ("cbct-rontgen/", "CBCT-scan"), (cur, "Voor verwijzers")], "info",
              "CBCT-scan verwijzen | Voor tandartsen | Slotplantsoen",
              "Verwijs uw patiënt voor een Cone Beam CT-scan naar Tandartspraktijk Slotplantsoen in Meppel. Wij plannen de afspraak en sturen de scan zo spoedig mogelijk toe.",
              'CBCT-scan voor <em class="g">verwijzers</em>',
              "Tandartsen, orthodontisten en kaakchirurgen kunnen hun patiënten voor een 3D CBCT-scan naar onze praktijk in Meppel verwijzen.",
              f"""
<h2>Zo werkt het</h2>
<ol>
  <li>U vult het verwijsformulier in met de gegevens van de patiënt en de indicatie.</li>
  <li>Wij nemen contact op met de patiënt om een afspraak in te plannen.</li>
  <li>De CBCT-scan wordt u zo spoedig mogelijk toegezonden.</li>
</ol>
<p>Indicaties zijn onder andere implantologie, kaakchirurgie, orthodontie, endodontologie en gnathologie. Meer over het onderzoek leest u op de pagina <a href="{{u:cbct-rontgen/}}">CBCT-scan</a>. Vragen? Bel <a href="{TEL_HREF}">{TEL}</a>.</p>
<div class="note"><p>Stuur geen BSN of uitgebreide medische gegevens via dit formulier; die nemen we bij de afspraak telefonisch met de patiënt door.</p></div>
<h2>Verwijsformulier</h2>
{form}
""", cta=False)


def misc():
    # 404
    p = dict(path="404.html", title="Pagina niet gevonden | Tandartspraktijk Slotplantsoen", desc="Deze pagina bestaat niet (meer).", noindex=True)
    p["schema"] = ""
    # 404 wordt vanaf elke diepte geserveerd: relatieve paden vanaf <base href="/">
    html = head(dict(p, path="")) + "\n" + header(dict(p, path="")) + f"""
<main id="main">
<section class="phero dark" style="min-height:60vh;display:grid;align-items:center">
  <div class="wrap">
    <h1>Deze pagina is niet gevonden.</h1>
    <p class="lead">Misschien is de pagina verplaatst bij de vernieuwing van onze website. Kies hieronder waar u naartoe wilt, of bel ons op {TEL}.</p>
    <div class="btn-row"><a class="btn" href="./">Naar de homepage</a><a class="btn btn--line" href="behandelingen/">Behandelingen</a><a class="btn btn--line" href="afspraak-maken/">Afspraak maken</a></div>
  </div>
</section>
</main>
""" + footer(dict(p, path=""))
    html = resolve(html, "")
    html = html.replace('<meta charset="utf-8">', f'<meta charset="utf-8">\n<base href="{SITE_BASE}">', 1)
    (ROOT / "404.html").write_text(html, encoding="utf-8")

    # Doorverwijzingen van oude URL's (voor hosting zonder .htaccess)
    for old, new in [("invisalign/", "behandelingen/othodontie-en-invisalign/"), ("intake-gebitsprothese/", "behandelingen/protheses/"), ("homepage/", "homepage/praktijkinformatie/")]:
        target = rel(old, new)
        (ROOT / old).mkdir(parents=True, exist_ok=True)
        (ROOT / old / "index.html").write_text(
            f'<!DOCTYPE html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>Doorverwijzing | {NAME}</title><meta name="description" content="Deze pagina is verhuisd naar een nieuw adres op de website van {NAME}.">'
            f'<meta name="robots" content="noindex"><link rel="stylesheet" href="{rel(old, "assets/css/style.css")}?v={CSS_V}">'
            f'<link rel="canonical" href="{BASE + new}"><meta http-equiv="refresh" content="0; url={target}"></head>'
            f'<body><main id="main" class="wrap section"><h1>Deze pagina is verhuisd</h1><p><a class="link" href="{target}">Ga naar de nieuwe pagina</a></p></main></body></html>', encoding="utf-8")

    # sitemap + robots + manifest
    prio = {"": "1.0"}
    urls = []
    for p in PAGES:
        if p.get("noindex"):
            continue
        pr = prio.get(p["path"], "0.8" if p["path"].startswith("behandelingen/") or p["path"] in ("afspraak-maken/", "inschrijven-als-nieuwe-patient/", "contact/") else "0.6")
        urls.append(f"  <url><loc>{BASE + p['path']}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>")
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /_build/\n\nSitemap: {BASE}sitemap.xml\n", encoding="utf-8")
    (ROOT / "site.webmanifest").write_text(json.dumps({
        "name": NAME, "short_name": "Slotplantsoen", "lang": "nl", "start_url": "/", "display": "standalone",
        "background_color": "#1b2134", "theme_color": "#1b2134",
        "icons": [{"src": "assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}]},
        ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    home()
    behandelingen_index()
    treatment_pages()
    team_page()
    other_pages()
    forms_pages()
    misc()
    print(f"{len(PAGES)} pagina's gebouwd + 404, sitemap.xml, robots.txt")
