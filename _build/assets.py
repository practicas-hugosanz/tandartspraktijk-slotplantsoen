"""Zet de originele beelden van de oude site om naar geoptimaliseerde WebP/PNG.

Gebruik:  python -I _build/assets.py <map-met-uitgepakte-oude-site>
Draai eenmalig; de resultaten staan in assets/img/.
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

SRC = Path(sys.argv[1]) / "images"
ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
NAVY = (27, 33, 52)
GOLD = (200, 185, 146)


def webp(src, dst, width, quality=78, crop=None):
    im = Image.open(src).convert("RGB")
    if crop:
        im = im.crop(crop)
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    dst.parent.mkdir(parents=True, exist_ok=True)
    im.save(dst, "WEBP", quality=quality, method=6)
    print(dst.relative_to(ROOT), im.size)
    return im.size


# Teamportretten (800x1200) -> 480 breed, plus Kinan groter voor de hero
TEAM = ["Safae", "Alvaro", "Mauricio", "Kinan", "anna", "Ina", "Marloes", "Naima",
        "Elisa", "Hanita", "Freek", "Ferdy", "Sanae", "Brigitte"]
for n in TEAM:
    webp(SRC / f"{n}.jpg", IMG / "team" / f"{n.lower()}.webp", 480)
webp(SRC / "Kinan.jpg", IMG / "hero-kinan.webp", 760, 80)
webp(SRC / "Alvaro.jpg", IMG / "alvaro-groot.webp", 760, 80)

# Praktijk- en behandelfoto's
webp(SRC / "Schermafbeelding-2021-02-26-om-14.48.02.png", IMG / "praktijk-gevel.webp", 1100)
webp(SRC / "foto_invisalign.jpg", IMG / "invisalign.webp", 900)
webp(SRC / "foto_kids.jpg", IMG / "kinderen.webp", 900)
webp(SRC / "foto_cbct.jpg", IMG / "cbct.webp", 900)
webp(SRC / "OG2ODN0.jpg", IMG / "bleken.webp", 900)
webp(SRC / "19465.jpg", IMG / "kindertandarts.webp", 900)
webp(SRC / "homefotomobiel.jpg", IMG / "ontspannen.webp", 900)
webp(SRC / "naima2.jpg", IMG / "preventie.webp", 700)
webp(SRC / "OPG-800x534-1.jpg", IMG / "rontgen.webp", 900)
webp(SRC / "invo_banner.jpg", IMG / "invisalign-banner.webp", 970)

# Poster van de hero (getoond zolang er geen video is, en als stilstaand beeld bij de video)
gevel = Image.open(SRC / "Schermafbeelding-2021-02-26-om-14.48.02.png").convert("RGB")
gevel = ImageOps.fit(gevel, (1600, 900), Image.LANCZOS, centering=(0.5, 0.45))
gevel.save(IMG / "hero-poster.webp", "WEBP", quality=74, method=6)

# Behandeliconen: witte lijniconen -> alfamasker (kleur via CSS mask)
ICONS = {"esthetisch": "esthetisch", "bleken": "bleken", "implantologie": "implantaten",
         "kronen": "kronen", "protheses": "protheses", "orthodontie": "orthodontie",
         "vullen": "vullingen", "trekken": "extractie", "wortelkanaal": "wortelkanaal",
         "preventie": "preventie"}
for src, dst in ICONS.items():
    im = Image.open(SRC / f"{src}.png").convert("RGBA")
    a = im.getchannel("A")
    out = Image.new("RGBA", im.size, (255, 255, 255, 0))
    out.putalpha(a)
    out.save(IMG / "icons" / f"{dst}.png", optimize=True)

# Logo: origineel is crème + wit, bedoeld voor donkere achtergrond
logo = Image.open(SRC / "logo-retina.png").convert("RGBA")
logo.save(IMG / "logo-licht.png", optimize=True)
# Donkere variant (voor witte achtergronden, bv. print/e-mail)
px = logo.load()
dark = logo.copy()
dp = dark.load()
for y in range(logo.height):
    for x in range(logo.width):
        r, g, b, a = px[x, y]
        if a == 0:
            continue
        if r > 235 and g > 235 and b > 235:
            dp[x, y] = (*NAVY, a)
        else:
            dp[x, y] = (150, 128, 78, a)
dark.save(IMG / "logo-donker.png", optimize=True)

# Beeldmerk (de tand) uitsnijden voor favicons
bbox = logo.getchannel("A").point(lambda v: 255 if v > 20 else 0).getbbox()
mark = logo.crop((0, 0, 140, logo.height))
mark = mark.crop(mark.getchannel("A").getbbox())


def icon(size, pad=0.2, radius=0.22):
    can = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bg = Image.new("RGBA", (size, size), (*NAVY, 255))
    m = Image.new("L", (size, size), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, size - 1, size - 1), round(size * radius), fill=255)
    can.paste(bg, (0, 0), m)
    inner = round(size * (1 - 2 * pad))
    k = inner / max(mark.size)
    t = mark.resize((round(mark.width * k), round(mark.height * k)), Image.LANCZOS)
    can.alpha_composite(t, ((size - t.width) // 2, (size - t.height) // 2))
    return can


icon(512).save(IMG / "icon-512.png", optimize=True)
icon(192).save(IMG / "icon-192.png", optimize=True)
icon(180, pad=0.18, radius=0).save(IMG / "apple-touch-icon.png", optimize=True)
icon(64).save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])

# Open Graph-afbeelding 1200x630
og = Image.new("RGB", (1200, 630), NAVY)
d = ImageDraw.Draw(og)
portrait = Image.open(SRC / "Kinan.jpg").convert("RGB")
portrait = ImageOps.fit(portrait, (430, 630), centering=(0.5, 0.3))
og.paste(portrait, (770, 0))
grad = Image.new("L", (160, 630))
for x in range(160):
    ImageDraw.Draw(grad).line([(x, 0), (x, 630)], fill=round(255 * (1 - x / 159)))
og.paste(Image.new("RGB", (160, 630), NAVY), (770, 0), grad)
lg = logo.copy()
lg.thumbnail((360, 100), Image.LANCZOS)
og.paste(lg, (80, 70), lg)
try:
    serif = ImageFont.truetype(str(ROOT / "_build" / "Archivo.ttf"), 62)
    serif.set_variation_by_axes([700])
except OSError:
    serif = ImageFont.truetype("georgiab.ttf", 60)
sans = ImageFont.truetype("arial.ttf", 28)
d.text((80, 230), "Uw glimlach", font=serif, fill=(255, 255, 255))
d.text((80, 305), "verdient vertrouwen.", font=serif, fill=GOLD)
d.line([(82, 410), (150, 410)], fill=GOLD, width=3)
d.text((80, 440), "Tandarts in Meppel  ·  Slotplantsoen 1a", font=sans, fill=(220, 222, 230))
d.text((80, 482), "Bel 0522-247436", font=sans, fill=(220, 222, 230))
og.save(IMG / "og-slotplantsoen.jpg", quality=86)
print("klaar")
