"""Stamp script.js and styles.css with a content hash in every page, so browsers load new versions right away.
Run after changing script.js or styles.css:  python3 stamp.py"""
import hashlib, pathlib, re
root = pathlib.Path(__file__).parent
ver = lambda f: hashlib.md5((root / f).read_bytes()).hexdigest()[:8]
js, css = ver("script.js"), ver("styles.css")
for page in root.glob("*.html"):
    t = page.read_text()
    n = re.sub(r'src="script\.js(\?v=[0-9a-f]+)?"', f'src="script.js?v={js}"', t)
    n = re.sub(r'href="styles\.css(\?v=[0-9a-f]+)?"', f'href="styles.css?v={css}"', n)
    if n != t:
        page.write_text(n)
        print("stamped", page.name)
print("script.js", js, "styles.css", css)
