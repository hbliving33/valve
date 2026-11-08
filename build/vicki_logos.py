"""Build vicki-logos.html: Vicki's logo options, round 2.
Built on the family badge (same single gold ring, gold top half, navy bottom half, one word under the circle at the
same fixed width as SOLAR / SOURDOUGH / TUTORING), plus two elegant signature versions.
Run:  python3 build/vicki_logos.py   then   python3 stamp.py"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
NAVY, GOLD, GOLDB, WHITE = "#1B1F3B", "#C9A227", "#E0B93A", "#FFFFFF"
SANS = "Montserrat, 'Segoe UI', Arial, sans-serif"
SCRIPT = "'Great Vibes', 'Allura', cursive"
SCRIPT2 = "'Allura', 'Great Vibes', cursive"
SERIF = "'Cormorant Garamond', Georgia, serif"
FONTS_LINK = ("https://fonts.googleapis.com/css2?family=Great+Vibes&family=Allura"
              "&family=Cormorant+Garamond:wght@600;700&display=swap")

def tag_text(s, color=GOLDB):
    # same 200-unit width as every other logo; longer phrases get smaller letters instead of being squeezed
    size = min(26, round(200 / (len(s) * 0.78), 1))
    return (f'<text x="150" y="330" text-anchor="middle" textLength="200" lengthAdjust="spacing" font-family="{SANS}" '
            f'font-weight="800" font-size="{size}" fill="{color}">{s}</text>')

def badge(inner, tag, uid, split=True):
    top = f'<path d="M0 150 H300 V0 H0 Z" fill="{GOLD}"/>' if split else ""
    return (f'<defs><clipPath id="c{uid}"><circle cx="150" cy="150" r="131"/></clipPath></defs>'
            f'<circle cx="150" cy="150" r="131" fill="{NAVY}"/><g clip-path="url(#c{uid})">{top}{inner}</g>'
            f'<circle cx="150" cy="150" r="136" fill="none" stroke="{GOLD}" stroke-width="6"/>{tag_text(tag) if tag else ""}')

def words(top, bottom, size=54):
    """Two words split like HI / LO: same weight, same distance from the line, both centred."""
    return (f'<text x="150" y="{150 - 22}" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="{size}" '
            f'textLength="190" lengthAdjust="spacingAndGlyphs" fill="{NAVY}" stroke="{NAVY}" stroke-width="2" paint-order="stroke">{top}</text>'
            f'<text x="150" y="{150 + 22 + size*0.72:.0f}" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="{size}" '
            f'textLength="190" lengthAdjust="spacingAndGlyphs" fill="{GOLDB}">{bottom}</text>')

def two_tone_v(family, weight, size, y):
    """One big V crossing the line: navy on the gold half, gold on the navy half."""
    v = f'font-family="{family}" font-weight="{weight}" font-size="{size}" text-anchor="middle"'
    cid = "tv" + "".join(ch for ch in family if ch.isalnum())[:6] + str(size)
    return (f'<clipPath id="{cid}"><rect x="0" y="0" width="300" height="150"/></clipPath>'
            f'<text x="150" y="{y}" {v} fill="{GOLDB}">V</text>'
            f'<text x="150" y="{y}" {v} fill="{NAVY}" clip-path="url(#{cid})">V</text>')

def signature(family, size, color, underline, y=172):
    return (f'<text x="150" y="{y}" text-anchor="middle" font-family="{family}" font-size="{size}" fill="{color}">Vicki</text>'
            f'<path d="M78 {y + 22} Q150 {y + 8} 224 {y + 20}" fill="none" stroke="{underline}" stroke-width="2.2" stroke-linecap="round"/>')

OPTIONS = [
    ("People First", lambda u: badge(words("PEOPLE", "FIRST"), "VICKI", u),
     "Same build as HILO: PEOPLE over FIRST, split by the line.  Her whole approach in two words."),
    ("Right Fit", lambda u: badge(words("RIGHT", "FIT", 60), "VICKI", u),
     "RIGHT over FIT.  Finding the right person for the job, at the right price."),
    ("Two-Tone V, People First", lambda u: badge(two_tone_v(SANS, 800, 190, 218), "PEOPLE FIRST", u),
     "One bold V crossing the line, navy on gold and gold on navy, with PEOPLE FIRST underneath."),
    ("Two-Tone V, Never a Number", lambda u: badge(two_tone_v(SANS, 800, 190, 218), "NEVER A NUMBER", u),
     "The same V with her line underneath: nobody is ever just a number."),
    ("Classic Serif V", lambda u: badge(two_tone_v(SERIF, 700, 210, 222), "PEOPLE FIRST", u),
     "A classic serif V in the two tones.  The most traditional of the set."),
    ("Signature, Gold on Navy", lambda u: badge(signature(SCRIPT, 92, GOLDB, GOLD), "PEOPLE FIRST", u, split=False),
     "Her name as a signature, gold on navy, with a fine underline.  Personal, the way she works."),
    ("Signature, Split", lambda u: badge(f'<text x="150" y="128" text-anchor="middle" font-family="{SCRIPT2}" font-size="86" fill="{NAVY}">Vicki</text>', "NEVER A NUMBER", u),
     "The signature sitting on the gold half, navy below, in the family split."),
    ("Signature, Navy on Gold", lambda u: (badge(signature(SCRIPT, 92, NAVY, NAVY), "PEOPLE FIRST", u, split=False)
                                          .replace(f'<circle cx="150" cy="150" r="131" fill="{NAVY}"/>', f'<circle cx="150" cy="150" r="131" fill="{GOLD}"/>')),
     "The signature in navy on a solid gold disc."),
]

def svg(body, size, label):
    return f'<svg viewBox="0 0 300 350" width="{size}" height="{size*350/300:.0f}" role="img" aria-label="{label}">{body}</svg>'

def mini(body, size):
    return f'<svg viewBox="0 0 300 300" width="{size}" height="{size}" aria-hidden="true">{body}</svg>'

cards = []
for n, (name, make, desc) in enumerate(OPTIONS, 1):
    big = make(f"v{n}")
    small = make(f"s{n}")
    cards.append(f'''        <figure class="logo-card hilo-card">
          <div class="hilo-tile">{svg(big, 260, f"Vicki logo option {n}")}</div>
          <div class="vk-preview vk-light"><span class="vk-mini">{mini(small, 54)}</span><span class="vk-name">Vicki</span></div>
          <figcaption><strong>V{n}. {name}</strong><span>{desc}</span></figcaption>
        </figure>''')

page = (ROOT / "lauren-logos.html").read_text()
head, foot = page.split("<main>")[0], "<footer" + page.split("<footer", 1)[1]
head = head.replace("<title>HILO Logo Options | Valve Partners</title>", "<title>Vicki Logo Options | Valve Partners</title>")
head = head.replace('content="HILO logo options for Lauren\'s page."', 'content="Logo options for Vicki."')
head = head.replace("</head>", f'<link rel="stylesheet" href="{FONTS_LINK}">\n</head>', 1)
html = head + f'''<main>
  <section class="page-hero">
    <div class="wrap">
      <h1>Vicki Logo Options</h1>
      <p>Round 2, a different direction: the same badge as Lauren's HILO, with the same ring, the same split and one word underneath at the same width, plus three signature versions.  Each shows large, then at real size beside her name.  Pick by V number.</p>
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
