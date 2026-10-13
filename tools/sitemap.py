#!/usr/bin/env python3
"""Write sitemap.xml for apps.johnkatez.com. Run from the repo root: python3 tools/sitemap.py
Lists every public page. Skips drafts and private paths (pocketarr until launch, join links, 404, sources)."""
import pathlib, datetime
ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://apps.johnkatez.com"
SKIP_DIRS = {"pocketarr", "join", "_src", "docs", "fonts", "assets", "img", "tools", "music-video-night", ".git", ".github"}
SKIP_FILES = {"404.html", "mvn/join.html", "og-cover.source.html"}
# pages other sessions publish separately (listed with their OK)
EXTRA = ["sitout/how-to/pickleball-round-robin-10-players.html", "sitout/how-to/pickleball-round-robin-12-players.html",
         "sitout/how-to/pickleball-round-robin-16-players.html", "sitout/how-to/mixed-doubles-round-robin.html",
         "sitout/how-to/pickleball-round-robin-scoring.html", "sitout/how-to/how-to-run-pickleball-open-play.html"]
today = datetime.date.today().isoformat()
paths = set()
for p in ROOT.rglob("*.html"):
    rel = p.relative_to(ROOT).as_posix()
    if rel.split("/")[0] in SKIP_DIRS or rel in SKIP_FILES or any(part.startswith(".") for part in rel.split("/")):
        continue
    if p.name.endswith(".source.html"):
        continue
    paths.add(rel)
paths |= set(EXTRA)
def url(rel):
    return f"{SITE}/" + (rel[:-len("index.html")] if rel.endswith("index.html") else rel)
def prio(rel):
    if rel == "index.html": return "1.0"
    if rel.endswith("/index.html") and rel.count("/") == 1: return "0.9"
    if "/guide/" in rel or "/how-to/" in rel: return "0.7"
    return "0.4"
items = "".join(f"<url><loc>{url(r)}</loc><lastmod>{today}</lastmod><priority>{prio(r)}</priority></url>\n" for r in sorted(paths, key=lambda r: (r.count('/'), r)))
(ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}</urlset>\n')
print(len(paths), "urls")
