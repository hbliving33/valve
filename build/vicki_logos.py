"""Build vicki-logos.html: conservative badge options for Vicki's partner card (they replace her V circle).
Every option keeps a clear V so the VALVE spell-out on the cards still reads.
Run:  python3 build/vicki_logos.py   then   python3 stamp.py"""
import pathlib, math

ROOT = pathlib.Path(__file__).resolve().parent.parent
NAVY, GOLD, GOLDB, WHITE = "#1B1F3B", "#C9A227", "#E0B93A", "#FFFFFF"
SERIF = "Georgia, 'Times New Roman', serif"

def disc(fill, ring=None):
    g = f'<circle cx="50" cy="50" r="48" fill="{fill}"/>'
    if ring:
        g += f'<circle cx="50" cy="50" r="44" fill="none" stroke="{ring}" stroke-width="1.6"/>'
    return g

def constellation(ink, line, faint):
    pts = [(27, 30), (35, 47), (43, 63), (50, 74), (57, 63), (65, 47), (73, 30)]
    g = "".join(f'<circle cx="{x}" cy="{y}" r="1.1" fill="{faint}"/>' for x, y in [(20, 55), (80, 58), (38, 24), (62, 22), (50, 40), (30, 70), (70, 72)])
    g += f'<polyline points="{" ".join(f"{x},{y}" for x, y in pts)}" fill="none" stroke="{line}" stroke-width="1.6" stroke-linejoin="round"/>'
    g += "".join(f'<circle cx="{x}" cy="{y}" r="{3.6 if i in (0, 3, 6) else 2.6}" fill="{ink}"/>' for i, (x, y) in enumerate(pts))
    return g

def converging(ink, dot):
    return (f'<path d="M24 26 C30 46 40 62 50 74" fill="none" stroke="{ink}" stroke-width="6" stroke-linecap="round"/>'
            f'<path d="M76 26 C70 46 60 62 50 74" fill="none" stroke="{ink}" stroke-width="6" stroke-linecap="round"/>'
            f'<circle cx="50" cy="74" r="6.5" fill="{dot}" stroke="{ink}" stroke-width="2"/>')

def network(ink, node):
    pts = [(26, 28), (38, 51), (50, 74), (62, 51), (74, 28)]
    g = f'<polyline points="{" ".join(f"{x},{y}" for x, y in pts)}" fill="none" stroke="{ink}" stroke-width="3" stroke-linejoin="round"/>'
    g += f'<line x1="38" y1="51" x2="62" y2="51" stroke="{ink}" stroke-width="1.4" opacity="0.55"/>'
    return g + "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="{node}" stroke="{ink}" stroke-width="2.2"/>' for x, y in pts)

def serif_v(ink, size=62, y=72):
    return f'<text x="50" y="{y}" text-anchor="middle" font-family="{SERIF}" font-size="{size}" fill="{ink}">V</text>'

def star(cx, cy, r, ink):
    pts = []
    for i in range(8):
        a = math.radians(-90 + 45 * i)
        rr = r if i % 2 == 0 else r * 0.32
        pts.append(f"{cx + rr*math.cos(a):.1f},{cy + rr*math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{ink}"/>'

def ribbon(ink, gap):
    g = ""
    for off in (-3.2, 3.2):
        g += (f'<polyline points="{26+off},{26} {50+off*0},{74+abs(off)*0.2} {74-off},{26}" fill="none" stroke="{ink}" '
              f'stroke-width="4" stroke-linejoin="miter" opacity="{1 if off < 0 else 0.55}"/>')
    return g

OPTIONS = [
    ("Constellation V, gold", disc(GOLD) + constellation(NAVY, NAVY, NAVY), "Points like cities across the country, connected into a V: her nationwide connections."),
    ("Constellation V, navy", disc(NAVY, GOLD) + constellation(GOLDB, "#E9EEF6", "#8C97B3"), "The same constellation, gold stars on navy inside a thin gold ring."),
    ("Two Paths", disc(GOLD) + converging(NAVY, GOLDB), "Two paths from different directions meeting at one point: bringing the right people together."),
    ("Network V", disc(GOLD) + network(NAVY, GOLDB), "A V built from connected points: her network, all leading back to her."),
    ("Classic Monogram", disc(GOLD) + serif_v(NAVY), "A simple serif V, the most conservative option."),
    ("Monogram with North Star", disc(GOLD) + serif_v(NAVY, 54, 78) + star(50, 24, 9, NAVY), "The serif V under a small north star: she points you the right way."),
    ("Monogram, navy", disc(NAVY, GOLD) + serif_v(GOLDB), "The serif V in gold on navy inside a thin gold ring."),
    ("Two Strands", disc(GOLD) + ribbon(NAVY, 3), "Two strands running side by side into one V: long-term relationships."),
]

def svg(body, n, size):
    return (f'<svg viewBox="0 0 100 100" width="{size}" height="{size}" role="img" aria-label="Vicki logo option {n}">{body}</svg>')

cards = []
for n, (name, body, desc) in enumerate(OPTIONS, 1):
    cards.append(f'''        <figure class="logo-card vk-card">
          <div class="vk-tile">{svg(body, n, 180)}
            <div class="vk-preview"><span class="vk-mini">{svg(body, f"{n}s", 54)}</span><span class="vk-name">Vicki</span></div>
          </div>
          <figcaption><strong>{n}. {name}</strong><span>{desc}</span></figcaption>
        </figure>''')

page = (ROOT / "lauren-logos.html").read_text()
head, foot = page.split("<main>")[0], "<footer" + page.split("<footer", 1)[1]
head = head.replace("<title>HILO Logo Options | Valve Partners</title>", "<title>Vicki Logo Options | Valve Partners</title>")
head = head.replace('content="HILO logo options for Lauren\'s page."', 'content="Logo options for Vicki\'s partner card."')
html = head + f'''<main>
  <section class="page-hero">
    <div class="wrap">
      <h1>Vicki Logo Options</h1>
      <p>For Vicki's partner card, in place of her V circle.  Conservative, nothing flashy, and every one keeps a clear V so VALVE still spells out across the cards.  Each shows large, then at the real size on her card.  Pick by number.</p>
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
(ROOT / "vicki-logos.html").write_text(html)
print("options:", len(OPTIONS))
