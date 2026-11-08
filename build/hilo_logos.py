"""Build lauren-logos.html: numbered HILO logo options for Lauren's page badge.
Run:  python3 build/hilo_logos.py   then   python3 stamp.py"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
NAVY, GOLD, GOLDB, WHITE = "#1B1F3B", "#C9A227", "#E0B93A", "#FFFFFF"
FONT = "Montserrat, 'Segoe UI', Arial, sans-serif"

# Color schemes: ring style, disc fill, letter color, cross color, cross opacity, tagline color
SCHEMES = [
    dict(name="Gold Ring", disc="none", ring=GOLD, ring2=None, text=GOLDB, cross=GOLD, tag=GOLDB),
    dict(name="Solid Gold", disc=GOLD, ring=GOLD, ring2=None, text=NAVY, cross=NAVY, tag=GOLDB),
    dict(name="Double Ring", disc="none", ring=GOLD, ring2=GOLD, text=WHITE, cross=GOLD, tag=GOLDB),
    dict(name="White Disc", disc=WHITE, ring=GOLD, ring2=None, text=NAVY, cross=GOLD, tag=WHITE),
    dict(name="White and Gold", disc="none", ring=GOLD, ring2=None, text=WHITE, cross=GOLD, tag=WHITE),
]

def t(x, y, s, size, color, anchor="middle", weight=800, ls=0):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{FONT}" font-weight="{weight}" '
            f'font-size="{size}" letter-spacing="{ls}" fill="{color}">{s}</text>')

def line(x1, y1, x2, y2, color, w=5, op=1):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}" stroke-linecap="butt" opacity="{op}"/>'

def half(color, d):
    return f'<path d="{d}" fill="{color}"/>'

# Layouts draw inside a circle centered at 150,150 (clipped to radius 131)
def L1(c):  # plus divider, HI up high on the left, LO down low on the right
    return (line(150, 0, 150, 300, c["cross"]) + line(0, 150, 300, 150, c["cross"]) +
            t(96, 124, "HI", 56, c["text"]) + t(204, 220, "LO", 56, c["text"]))

def L2(c):  # one horizontal divider, HI over LO
    return (line(40, 150, 260, 150, c["cross"], w=5) +
            t(150, 128, "HI", 76, c["text"], ls=6) + t(150, 232, "LO", 76, c["text"], ls=6))

def L3(c):  # diagonal slash, HI upper left, LO lower right
    return (line(240, 30, 60, 270, c["cross"], w=6) +
            t(104, 140, "HI", 64, c["text"]) + t(198, 222, "LO", 64, c["text"]))

def L4(c):  # X divider, HI in the top wedge, LO in the bottom wedge
    return (line(40, 40, 260, 260, c["cross"], w=4) + line(260, 40, 40, 260, c["cross"], w=4) +
            t(150, 98, "HI", 46, c["text"]) + t(150, 244, "LO", 46, c["text"]))

def L5(c):  # plus divider with an open center, HI top left, LO bottom right
    g = 24
    return (line(150, 0, 150, 150 - g, c["cross"]) + line(150, 150 + g, 150, 300, c["cross"]) +
            line(0, 150, 150 - g, 150, c["cross"]) + line(150 + g, 150, 300, 150, c["cross"]) +
            f'<circle cx="150" cy="150" r="7" fill="{c["cross"]}"/>' +
            t(94, 122, "HI", 52, c["text"]) + t(206, 220, "LO", 52, c["text"]))

def L6(c):  # the circle splits in two: top half solid, bottom half open
    top = half(c["cross"], "M0 150 H300 V0 H0 Z")
    on_top = NAVY if c["cross"] != NAVY else GOLDB
    return (top + f'<text x="156" y="126" text-anchor="middle" font-family="{FONT}" font-weight="800" font-size="72" letter-spacing="12" fill="{on_top}" stroke="{on_top}" stroke-width="2.6" stroke-linejoin="round" paint-order="stroke">HI</text>'
            + t(153, 226, "LO", 72, c["text"], ls=6))

LAYOUTS = [
    ("Quadrants", L1, "A plus-shaped divider splits the circle.  HI sits up high, LO sits down low."),
    ("Stacked", L2, "One clean line across the middle, HI over LO."),
    ("Slash", L3, "A diagonal line cuts through.  HI upper left, LO lower right."),
    ("X Split", L4, "An X divides the circle.  HI in the top wedge, LO in the bottom."),
    ("Open Center", L5, "A plus divider that doesn't meet in the middle, with a dot at center."),
    ("Half and Half", L6, "The circle is split: the top half filled for HI, the bottom open for LO."),
]

def tag_text(s, color, y=330, size=26):
    """Tagline under the circle: always exactly 200 units wide, whatever the word."""
    return (f'<text x="150" y="{y}" text-anchor="middle" textLength="200" lengthAdjust="spacing" font-family="{FONT}" '
            f'font-weight="800" font-size="{size}" fill="{color}">{s}</text>')

def svg(layout, c):
    ring = f'<circle cx="150" cy="150" r="136" fill="{c["disc"]}" stroke="{c["ring"]}" stroke-width="6"/>'
    if c["ring2"]:
        ring += f'<circle cx="150" cy="150" r="124" fill="none" stroke="{c["ring2"]}" stroke-width="2"/>'
    clip = '<clipPath id="CLIP"><circle cx="150" cy="150" r="131"/></clipPath>'
    body = f'<g clip-path="url(#CLIP)">{layout(c)}</g>'
    tag = tag_text("GET IT?", c["tag"])
    return (f'<svg viewBox="0 0 300 350" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="HILO logo with tagline Get it?">'
            f'<defs>{clip}</defs>{ring}{body}{tag}</svg>')

cards, n = [], 0
for lname, fn, desc in LAYOUTS:
    for c in SCHEMES:
        n += 1
        s = svg(fn, c).replace("CLIP", f"clip{n}")
        cards.append(f'''        <figure class="logo-card hilo-card">
          <div class="hilo-tile">{s}</div>
          <figcaption><strong>{n}. {lname}, {c["name"]}</strong><span>{desc}</span></figcaption>
        </figure>''')

page = (ROOT / "logos.html").read_text()
head = page.split("<main>")[0]
foot = "<footer" + page.split("<footer", 1)[1]
head = head.replace("<title>Logo Options | Valve Partners</title>", "<title>HILO Logo Options | Valve Partners</title>")
head = head.replace('content="Logo options for Valve Partners."', 'content="HILO logo options for Lauren\'s page."')
html = head + f'''<main>
  <section class="page-hero">
    <div class="wrap">
      <h1>HILO Logo Options</h1>
      <p>For the round badge on Lauren's page: HI and LO split by a divider, with "Get it?" underneath.  Shown on navy, the way they'll sit on her page.  Pick by number.</p>
    </div>
  </section>
  <div class="wrap">
    <section class="logo-theme">
      <div class="logo-grid">
{chr(10).join(cards)}
      </div>
    </section>
  </div>
</main>

''' + foot
(ROOT / "lauren-logos.html").write_text(html)
print("options:", n)
