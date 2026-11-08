"""Build lauren-s-logos.html: HILO (option 26) variants for Lauren's three S's: solar, sourdough, soccer.
Run:  python3 build/lauren_s_logos.py   then   python3 stamp.py"""
import math, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
NAVY, GOLD, GOLDB, WHITE, CRUST = "#1B1F3B", "#C9A227", "#E0B93A", "#FFFFFF", "#D9A441"
FONT = "Montserrat, 'Segoe UI', Arial, sans-serif"

def t(x, y, s, size, color, ls=0, weight=800):
    return (f'<text x="{x}" y="{y}" text-anchor="middle" font-family="{FONT}" font-weight="{weight}" '
            f'font-size="{size}" letter-spacing="{ls}" fill="{color}">{s}</text>')

# Color treatments, all built from number 26
SCHEMES = [
    dict(name="Number 26", top=GOLD, hi=NAVY, lo=GOLDB, ring=GOLD, ring2=False, tag=GOLDB, ink=GOLDB, inkbg=NAVY),
    dict(name="Double Ring", top=GOLD, hi=NAVY, lo=GOLDB, ring=GOLD, ring2=True, tag=GOLDB, ink=WHITE, inkbg=NAVY),
    dict(name="Flipped", top=NAVY, hi=GOLDB, lo=NAVY, ring=GOLD, ring2=False, tag=GOLDB, ink=NAVY, inkbg=GOLD, bottom=GOLD),
]

# ---------- icons ----------
def sun(cx, cy, r, fg, bg, bolt=False):
    rays = "".join(
        f'<line x1="{cx + r*0.80*math.cos(a):.1f}" y1="{cy + r*0.80*math.sin(a):.1f}" '
        f'x2="{cx + r*1.08*math.cos(a):.1f}" y2="{cy + r*1.08*math.sin(a):.1f}" stroke="{fg}" stroke-width="{r*0.16:.1f}" stroke-linecap="round"/>'
        for a in [i * math.pi / 4 for i in range(8)])
    g = rays + f'<circle cx="{cx}" cy="{cy}" r="{r*0.6:.1f}" fill="{fg}"/>'
    if bolt:
        s = r * 0.42
        g += (f'<polygon points="{cx+s*0.15:.1f},{cy-s:.1f} {cx-s*0.55:.1f},{cy+s*0.12:.1f} {cx-s*0.02:.1f},{cy+s*0.12:.1f} '
              f'{cx-s*0.2:.1f},{cy+s:.1f} {cx+s*0.55:.1f},{cy-s*0.15:.1f} {cx+s*0.03:.1f},{cy-s*0.15:.1f}" fill="{bg}"/>')
    return g

def ball(cx, cy, r, fg, bg, uid):
    def pent(px, py, pr, rot=-90):
        return " ".join(f"{px + pr*math.cos(math.radians(rot + 72*i)):.1f},{py + pr*math.sin(math.radians(rot + 72*i)):.1f}" for i in range(5))
    pr = r * 0.36
    parts = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fg}"/>', f'<polygon points="{pent(cx, cy, pr)}" fill="{bg}"/>']
    for i in range(5):
        a = math.radians(-90 + 72 * i)
        vx, vy = cx + pr*math.cos(a), cy + pr*math.sin(a)
        ex, ey = cx + r*0.78*math.cos(a), cy + r*0.78*math.sin(a)
        parts.append(f'<line x1="{vx:.1f}" y1="{vy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{bg}" stroke-width="{r*0.07:.1f}"/>')
        ox, oy = cx + r*1.02*math.cos(a), cy + r*1.02*math.sin(a)
        parts.append(f'<polygon points="{pent(ox, oy, pr*0.85, -90 + 72*i + 36)}" fill="{bg}"/>')
    return (f'<clipPath id="b{uid}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
            f'<g clip-path="url(#b{uid})">{"".join(parts)}</g>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{fg}" stroke-width="{r*0.06:.1f}"/>')

def boule(cx, cy, r, fg, bg):
    """Round sourdough loaf seen from the side: domed top, flat bottom, curved scores and an ear."""
    w, h = r * 1.05, r * 1.15
    loaf = (f'<path d="M{cx-w:.1f} {cy+h*0.45:.1f} C{cx-w:.1f} {cy-h*0.9:.1f} {cx+w:.1f} {cy-h*0.9:.1f} {cx+w:.1f} {cy+h*0.45:.1f} '
            f'Q{cx+w:.1f} {cy+h*0.62:.1f} {cx+w*0.8:.1f} {cy+h*0.62:.1f} H{cx-w*0.8:.1f} Q{cx-w:.1f} {cy+h*0.62:.1f} {cx-w:.1f} {cy+h*0.45:.1f} Z" fill="{fg}"/>')
    scores = "".join(
        f'<path d="M{cx + dx - w*0.18:.1f} {cy - h*0.05 + abs(dx)*0.25:.1f} Q{cx + dx:.1f} {cy - h*0.42 + abs(dx)*0.25:.1f} {cx + dx + w*0.18:.1f} {cy - h*0.12 + abs(dx)*0.25:.1f}" '
        f'fill="none" stroke="{bg}" stroke-width="{r*0.09:.1f}" stroke-linecap="round"/>'
        for dx in (-w*0.42, 0, w*0.42))
    return loaf + scores

def batard(cx, cy, w, fg, bg, op):
    """Long oval loaf with diagonal scores, for the background."""
    h = w * 0.42
    g = f'<ellipse cx="{cx}" cy="{cy}" rx="{w/2:.1f}" ry="{h/2:.1f}" fill="{fg}"/>'
    for i in (-1, 0, 1):
        x = cx + i * w * 0.24
        g += (f'<path d="M{x - w*0.09:.1f} {cy + h*0.22:.1f} Q{x - w*0.02:.1f} {cy - h*0.05:.1f} {x + w*0.09:.1f} {cy - h*0.26:.1f}" '
              f'fill="none" stroke="{bg}" stroke-width="{w*0.035:.1f}" stroke-linecap="round"/>')
    return f'<g opacity="{op}">{g}</g>'

def goal(cx, top, w, h, fg, op):
    """Soccer goal and net, for the background."""
    x0, x1, y1 = cx - w/2, cx + w/2, top + h
    g = f'<path d="M{x0} {y1} V{top} H{x1} V{y1}" fill="none" stroke="{fg}" stroke-width="6" stroke-linejoin="round"/>'
    for i in range(1, 8):
        x = x0 + w * i / 8
        g += f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{y1}" stroke="{fg}" stroke-width="1.6"/>'
    for j in range(1, 5):
        y = top + h * j / 5
        g += f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="{fg}" stroke-width="1.6"/>'
    return f'<g opacity="{op}">{g}</g>'

def panel(cx, cy, w, fg, op):
    """Solar panel in perspective, for the background."""
    h = w * 0.42; sk = w * 0.18
    p = [(cx - w/2 + sk, cy - h/2), (cx + w/2 + sk, cy - h/2), (cx + w/2 - sk, cy + h/2), (cx - w/2 - sk, cy + h/2)]
    g = f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in p)}" fill="none" stroke="{fg}" stroke-width="5" stroke-linejoin="round"/>'
    for i in range(1, 6):
        f = i / 6
        tx, bx = p[0][0] + (p[1][0]-p[0][0])*f, p[3][0] + (p[2][0]-p[3][0])*f
        g += f'<line x1="{tx:.1f}" y1="{p[0][1]:.1f}" x2="{bx:.1f}" y2="{p[3][1]:.1f}" stroke="{fg}" stroke-width="2"/>'
    for j in range(1, 3):
        f = j / 3
        lx, rx = p[0][0] + (p[3][0]-p[0][0])*f, p[1][0] + (p[2][0]-p[1][0])*f
        y = p[0][1] + h*f
        g += f'<line x1="{lx:.1f}" y1="{y:.1f}" x2="{rx:.1f}" y2="{y:.1f}" stroke="{fg}" stroke-width="2"/>'
    return f'<g opacity="{op}">{g}</g>'

# ---------- layouts on number 26 ----------
def base(c, lo_text=True):
    g = f'<path d="M0 150 H300 V0 H0 Z" fill="{c["top"]}"/>'
    if c.get("bottom"):
        g += f'<path d="M0 150 H300 V300 H0 Z" fill="{c["bottom"]}"/>'
    g += t(150, 128, "HI", 72, c["hi"], ls=6)
    if lo_text:
        g += t(150, 230, "LO", 72, c["lo"], ls=6)
    return g

def icon_for(kind, cx, cy, r, c, uid, bolt=False):
    if kind == "solar":
        return sun(cx, cy, r, c["lo"], c["inkbg"], bolt)
    if kind == "sourdough":
        return boule(cx, cy, r, c["lo"], c["inkbg"])
    return ball(cx, cy, r, c["lo"], c["inkbg"], uid)

def lay_o(kind):           # the O in LO is the icon
    def draw(c, uid):
        r = {"solar": 30, "sourdough": 31, "soccer": 27}[kind]
        cy = {"solar": 205, "sourdough": 210, "soccer": 205}[kind]
        return base(c, lo_text=False) + t(112, 230, "L", 72, c["lo"]) + icon_for(kind, 180, cy, r, c, uid, bolt=(kind == "solar"))
    return draw

def lay_bg(kind):          # icon large and soft behind LO
    def draw(c, uid):
        ink = c["lo"]
        if kind == "solar":
            bg = panel(150, 218, 170, ink, 0.28)
        elif kind == "sourdough":
            bg = batard(150, 214, 190, ink, c["inkbg"], 0.26)
        else:
            bg = goal(150, 168, 190, 92, ink, 0.3)
        g = f'<path d="M0 150 H300 V0 H0 Z" fill="{c["top"]}"/>'
        if c.get("bottom"):
            g += f'<path d="M0 150 H300 V300 H0 Z" fill="{c["bottom"]}"/>'
        return g + bg + t(150, 128, "HI", 72, c["hi"], ls=6) + t(150, 230, "LO", 72, c["lo"], ls=6)
    return draw

def lay_seam(kind):        # small medallion on the line between HI and LO
    def draw(c, uid):
        ring = f'<circle cx="150" cy="150" r="24" fill="{c["inkbg"] if not c.get("bottom") else NAVY}" stroke="{GOLD}" stroke-width="4"/>'
        cc = dict(c, lo=GOLDB if not c.get("bottom") else GOLDB, inkbg=NAVY)
        g = f'<path d="M0 150 H300 V0 H0 Z" fill="{c["top"]}"/>'
        if c.get("bottom"):
            g += f'<path d="M0 150 H300 V300 H0 Z" fill="{c["bottom"]}"/>'
        g += t(150, 114, "HI", 66, c["hi"], ls=6) + t(150, 238, "LO", 66, c["lo"], ls=6)
        return g + ring + icon_for(kind, 150, 151, 15, cc, uid, bolt=(kind == "solar"))
    return draw

LAYOUTS = [
    ("The O", lay_o, {"solar": "The O in LO is a sun with a lightning bolt: solar and battery backup.",
                      "sourdough": "The O in LO is a little sourdough loaf.",
                      "soccer": "The O in LO is a soccer ball."}),
    ("In the Background", lay_bg, {"solar": "A solar panel sits softly behind LO.",
                                   "sourdough": "A scored sourdough loaf sits softly behind LO.",
                                   "soccer": "A soccer goal and net sit softly behind LO."}),
    ("On the Line", lay_seam, {"solar": "A small sun with a bolt sits on the line between HI and LO.",
                               "sourdough": "A small loaf sits on the line between HI and LO.",
                               "soccer": "A small soccer ball sits on the line between HI and LO."}),
]

DISCIPLINES = [("solar", "Solar", "SOLAR"), ("sourdough", "Sourdough", "SOURDOUGH"), ("soccer", "Soccer", "SOCCER")]

def svg(draw, c, tag, uid):
    ring = f'<circle cx="150" cy="150" r="136" fill="none" stroke="{c["ring"]}" stroke-width="6"/>'
    if c["ring2"]:
        ring += f'<circle cx="150" cy="150" r="124" fill="none" stroke="{c["ring"]}" stroke-width="2"/>'
    return (f'<svg viewBox="0 0 300 350" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="HILO {tag.lower()} logo option {uid}">'
            f'<defs><clipPath id="c{uid}"><circle cx="150" cy="150" r="131"/></clipPath></defs>'
            f'<g clip-path="url(#c{uid})">{draw(c, uid)}</g>{ring}{t(150, 330, tag, 26, c["tag"], ls=5)}</svg>')

sections, n = [], 0
for key, title, tag in DISCIPLINES:
    cards = []
    for lname, fn, descs in LAYOUTS:
        for c in SCHEMES:
            n += 1
            cards.append(f'''        <figure class="logo-card hilo-card">
          <div class="hilo-tile">{svg(fn(key), c, tag, n)}</div>
          <figcaption><strong>{n}. {title}: {lname}, {c["name"]}</strong><span>{descs[key]}</span></figcaption>
        </figure>''')
    sections.append(f'''    <section class="logo-theme">
      <h2>{title}</h2>
      <div class="logo-grid">
{chr(10).join(cards)}
      </div>
    </section>''')

page = (ROOT / "lauren-logos.html").read_text()
head, foot = page.split("<main>")[0], "<footer" + page.split("<footer", 1)[1]
head = head.replace("<title>HILO Logo Options | Valve Partners</title>", "<title>Lauren's Three S's Logos | Valve Partners</title>")
head = head.replace('content="HILO logo options for Lauren\'s page."', 'content="HILO logo options for Lauren\'s solar, sourdough and soccer."')
html = head + f'''<main>
  <section class="page-hero">
    <div class="wrap">
      <h1>Lauren's Three S's</h1>
      <p>Number 26, the HILO logo, made for each of Lauren's disciplines: solar, sourdough and soccer.  Each one comes in three ideas and three color treatments.  Pick by number.</p>
    </div>
  </section>
  <div class="wrap">
{chr(10).join(sections)}
  </div>
</main>

''' + foot
(ROOT / "lauren-s-logos.html").write_text(html)
print("options:", n)
