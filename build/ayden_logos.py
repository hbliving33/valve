"""Build ayden-logos.html: numbered logo options for the round badge on Ayden's tutoring page.
Run:  python3 build/ayden_logos.py   then   python3 stamp.py"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
NAVY, GOLD, GOLDB, WHITE = "#1B1F3B", "#C9A227", "#E0B93A", "#FFFFFF"
FONT = "Montserrat, 'Segoe UI', Arial, sans-serif"
TAG = "TUTORING"

SCHEMES = [
    dict(name="Gold Ring", disc="none", ring=GOLD, ring2=None, text=GOLDB, accent=GOLD, tag=GOLDB),
    dict(name="Solid Gold", disc=GOLD, ring=GOLD, ring2=None, text=NAVY, accent=NAVY, tag=GOLDB),
    dict(name="Double Ring", disc="none", ring=GOLD, ring2=GOLD, text=WHITE, accent=GOLD, tag=GOLDB),
    dict(name="White Disc", disc=WHITE, ring=GOLD, ring2=None, text=NAVY, accent=GOLD, tag=WHITE),
    dict(name="White and Gold", disc="none", ring=GOLD, ring2=None, text=WHITE, accent=GOLD, tag=WHITE),
]

def t(x, y, s, size, color, weight=800, ls=0):
    return (f'<text x="{x}" y="{y}" text-anchor="middle" font-family="{FONT}" font-weight="{weight}" '
            f'font-size="{size}" letter-spacing="{ls}" fill="{color}">{s}</text>')

def A_plus(c):  # the grade everyone wants
    return t(132, 188, "A", 130, c["text"]) + t(214, 128, "+", 76, c["accent"])

def book(c):  # open book with the A above it
    a = c["accent"]
    pages = (f'<path d="M66 200 Q108 182 150 200 V244 Q108 226 66 244 Z" fill="none" stroke="{a}" stroke-width="7" stroke-linejoin="round"/>'
             f'<path d="M234 200 Q192 182 150 200 V244 Q192 226 234 244 Z" fill="none" stroke="{a}" stroke-width="7" stroke-linejoin="round"/>')
    return t(150, 172, "A", 104, c["text"]) + pages

def pencil(c):  # a pencil is the crossbar of the A
    a = c["accent"]
    legs = (f'<path d="M92 226 L150 72 L208 226" fill="none" stroke="{c["text"]}" stroke-width="26" stroke-linejoin="miter" stroke-linecap="butt"/>')
    pen = (f'<g transform="rotate(-12 150 168)"><rect x="80" y="158" width="118" height="20" fill="{a}"/>'
           f'<polygon points="198,158 222,168 198,178" fill="{a}"/><rect x="72" y="158" width="10" height="20" fill="{a}" opacity="0.6"/></g>')
    return legs + pen

def cap(c):  # graduation cap sitting on the A
    a = c["accent"]
    hat = (f'<polygon points="150,58 232,88 150,118 68,88" fill="{a}"/>'
           f'<path d="M112 102 V124 Q150 140 188 124 V102" fill="{a}"/>'
           f'<line x1="214" y1="94" x2="214" y2="132" stroke="{a}" stroke-width="5"/><circle cx="214" cy="136" r="7" fill="{a}"/>')
    return hat + t(150, 238, "A", 116, c["text"])

def name(c):  # AYDEN across the middle with lines above and below
    a = c["accent"]
    return (f'<line x1="56" y1="112" x2="244" y2="112" stroke="{a}" stroke-width="5"/>'
            + t(150, 170, "AYDEN", 54, c["text"], ls=3) +
            f'<line x1="56" y1="194" x2="244" y2="194" stroke="{a}" stroke-width="5"/>')

def bulb(c):  # the bright idea, with the A inside the bulb
    a = c["accent"]
    shape = (f'<path d="M150 56 C96 56 70 98 76 138 C80 166 104 182 110 208 H190 C196 182 220 166 224 138 C230 98 204 56 150 56 Z" '
             f'fill="none" stroke="{a}" stroke-width="7"/>'
             f'<rect x="116" y="218" width="68" height="10" rx="3" fill="{a}"/><rect x="124" y="234" width="52" height="10" rx="3" fill="{a}"/>')
    return shape + t(150, 182, "A", 92, c["text"])

LAYOUTS = [
    ("A Plus", A_plus, "An A with a plus: the grade every student is after."),
    ("Open Book", book, "The A over an open book."),
    ("Pencil A", pencil, "The A drawn with a pencil as its crossbar."),
    ("Grad Cap", cap, "A graduation cap sitting on the A, a nod to his Cal Poly Humboldt degree."),
    ("Name Band", name, "AYDEN across the middle between two lines."),
    ("Bright Idea", bulb, "A light bulb with the A inside: the moment it clicks."),
]

def svg(layout, c, n):
    ring = f'<circle cx="150" cy="150" r="136" fill="{c["disc"]}" stroke="{c["ring"]}" stroke-width="6"/>'
    if c["ring2"]:
        ring += f'<circle cx="150" cy="150" r="124" fill="none" stroke="{c["ring2"]}" stroke-width="2"/>'
    clip = f'<clipPath id="ac{n}"><circle cx="150" cy="150" r="131"/></clipPath>'
    return (f'<svg viewBox="0 0 300 350" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Ayden tutoring logo option {n}">'
            f'<defs>{clip}</defs>{ring}<g clip-path="url(#ac{n})">{layout(c)}</g>{t(150, 330, TAG, 24, c["tag"], ls=5)}</svg>')

cards, n = [], 0
for lname, fn, desc in LAYOUTS:
    for c in SCHEMES:
        n += 1
        cards.append(f'''        <figure class="logo-card hilo-card">
          <div class="hilo-tile">{svg(fn, c, n)}</div>
          <figcaption><strong>{n}. {lname}, {c["name"]}</strong><span>{desc}</span></figcaption>
        </figure>''')

page = (ROOT / "lauren-logos.html").read_text()
head, foot = page.split("<main>")[0], "<footer" + page.split("<footer", 1)[1]
head = head.replace("<title>HILO Logo Options | Valve Partners</title>", "<title>Ayden Logo Options | Valve Partners</title>")
head = head.replace('content="HILO logo options for Lauren\'s page."', 'content="Logo options for Ayden\'s tutoring page."')
html = head + f'''<main>
  <section class="page-hero">
    <div class="wrap">
      <h1>Ayden Logo Options</h1>
      <p>For the round badge on Ayden's tutoring page, in the same gold and navy as Lauren's.  Shown on navy, the way they'll sit on his page.  Pick by number.</p>
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
(ROOT / "ayden-logos.html").write_text(html)
print("options:", n)
