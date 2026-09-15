#!/usr/bin/env python3
from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-09-15"

SHOWS = {
    "/shows/adult/atomic-saloon/": {"page":"shows/adult/atomic-saloon/index.html","old":{90},"new":100,"slug":"atomic-saloon"},
    "/shows/family/tournament-of-kings/": {"page":"shows/family/tournament-of-kings/index.html","old":{74},"new":78,"slug":"tournament-of-kings"},
    "/shows/music/blue-man-group/": {"page":"shows/music/blue-man-group/index.html","old":{65,74},"new":68,"slug":"blue-man-group"},
}

changed=[]
def write(path, text):
    p=ROOT/path
    old=p.read_text(encoding="utf-8")
    if text != old:
        p.write_text(text, encoding="utf-8")
        changed.append(path)

# Canonical show pages: update every price representation that belongs to that page.
for href,cfg in SHOWS.items():
    p=ROOT/cfg["page"]
    s=p.read_text(encoding="utf-8")
    for old in cfg["old"]:
        s=s.replace(f"${old}", f"${cfg['new']}")
        s=s.replace(f'"price":{old}', f'"price":{cfg["new"]}')
    # Savings arithmetic where a known regular price remains valid.
    if cfg["slug"]=="tournament-of-kings": s=s.replace("Save $14", "Save $10")
    if cfg["slug"]=="blue-man-group": s=s.replace("Save $27", "Save $24")
    if cfg["slug"]=="atomic-saloon":
        s=re.sub(r'<div class="vs-deal-line"><span class="vs-regular-price">Regular \$100</span><span class="vs-save-badge">Save \$10</span></div>', '', s)
    s=re.sub(r'"dateModified":"[^"]+"', f'"dateModified":"{TODAY}"', s)
    s=re.sub(r'"lastReviewed":"[^"]+"', f'"lastReviewed":"{TODAY}"', s)
    write(cfg["page"],s)

# Ikons of Rock: canonical Spotlight route supplied Sep 15, 2026 + affiliate suffix.
ikons_page="shows/music/ikons-of-rock/index.html"
p=ROOT/ikons_page
s=p.read_text(encoding="utf-8")
s=s.replace("https://spotlight.vegas/shows/tribute/ikons-of-rock-hard-rock/ref/vegassidekick", "https://spotlight.vegas/shows/tribute/ikons-of-rock/ref/vegassidekick")
s=s.replace("https://spotlight.vegas/shows/tribute/ikons-of-rock-api/ref/vegassidekick", "https://spotlight.vegas/shows/tribute/ikons-of-rock/ref/vegassidekick")
s=s.replace("https://spotlight.vegas/shows/tribute/ikons-of-rock-hard-rock/", "https://spotlight.vegas/shows/tribute/ikons-of-rock/")
s=s.replace("https://spotlight.vegas/shows/tribute/ikons-of-rock-api/", "https://spotlight.vegas/shows/tribute/ikons-of-rock/")
s=re.sub(r'"dateModified":"[^"]+"', f'"dateModified":"{TODAY}"', s)
s=re.sub(r'"lastReviewed":"[^"]+"', f'"lastReviewed":"{TODAY}"', s)
write(ikons_page,s)

# Structured show database.
db_path=ROOT/"data/show-database.json"
db=json.loads(db_path.read_text(encoding="utf-8"))
by_slug={r.get("slug"):r for r in db["records"]}
for slug,new in [("atomic-saloon",100),("tournament-of-kings",78),("blue-man-group",68)]:
    r=by_slug[slug]; r["our_price"]=new; r["verified_on"]=TODAY; r["freshness_label"]="September 2026"
    if isinstance(r.get("spotlight"),dict): r["spotlight"]["our_price"]=new
r=by_slug.get("atomic-saloon")
if r:
    r["schedule_summary"]="Tue, Fri, Sat · 7:30 PM & 9:30 PM; Wed, Thu · 7:30 PM"
    if isinstance(r.get("spotlight"),dict):
        r["spotlight"]["schedule_days"]={"Tuesday":["7:30 PM","9:30 PM"],"Wednesday":["7:30 PM"],"Thursday":["7:30 PM"],"Friday":["7:30 PM","9:30 PM"],"Saturday":["7:30 PM","9:30 PM"]}
r=by_slug.get("ikons-of-rock")
if r:
    r["ticket_url"]="https://spotlight.vegas/shows/tribute/ikons-of-rock/ref/vegassidekick"; r["verified_on"]=TODAY; r["freshness_label"]="September 2026"
    if isinstance(r.get("spotlight"),dict):
        r["spotlight"]["spotlight_url"]="https://spotlight.vegas/shows/tribute/ikons-of-rock/"
        r["spotlight"]["affiliate_url"]="https://spotlight.vegas/shows/tribute/ikons-of-rock/ref/vegassidekick"
db["updated_on"]=TODAY
newdb=json.dumps(db,ensure_ascii=False,indent=2)+"\n"
write("data/show-database.json",newdb)

# Production catalogs, venue pages and current guides. Only modify the card/object for the named show.
roots=[ROOT/"index.html", ROOT/"shows", ROOT/"venues", ROOT/"guides"]
files=[]
for root in roots:
    if root.is_file(): files.append(root)
    elif root.exists(): files.extend(root.rglob("*.html"))
for p in files:
    rel=p.relative_to(ROOT).as_posix()
    if rel in {v["page"] for v in SHOWS.values()} or rel==ikons_page: continue
    s=p.read_text(encoding="utf-8")
    original=s
    for href,cfg in SHOWS.items():
        # HTML cards linking to the canonical show page.
        pat=re.compile(r'(<a\b[^>]*href=["\']'+re.escape(href)+r'["\'][^>]*>.*?</a>)',re.S|re.I)
        def card(m,cfg=cfg):
            block=m.group(1)
            for old in cfg["old"]: block=block.replace(f"${old}",f"${cfg['new']}")
            return block
        s=pat.sub(card,s)
        # JS catalog objects identified by canonical slug.
        objpat=re.compile(r'(\{[^{}]{0,1200}\bslug:["\']'+re.escape(cfg["slug"])+r'["\'][^{}]{0,1200}\})',re.S)
        def obj(m,cfg=cfg):
            block=m.group(1)
            block=re.sub(r'\bprice:\s*\d+',f'price:{cfg["new"]}',block)
            block=re.sub(r"\bpd:\s*['\"]\$\d+['\"]",f"pd:'${cfg['new']}'",block)
            return block
        s=objpat.sub(obj,s)
    if s!=original:
        p.write_text(s,encoding="utf-8"); changed.append(rel)

# Keep the active builder price table current (historical audits are intentionally untouched).
prompt="SHOW-BUILDER-PROMPT.md"
p=ROOT/prompt
if p.exists():
    s=p.read_text(encoding="utf-8")
    s=re.sub(r'(\|\s*Atomic Saloon Show\s*\|[^\n]*\|)\s*\$\d+\s*\|',r'\1 $100 |',s)
    s=re.sub(r'(\|\s*Tournament of Kings\s*\|[^\n]*\|)\s*\$\d+\s*\|',r'\1 $78 |',s)
    s=re.sub(r'(\|\s*Blue Man Group\s*\|[^\n]*\|)\s*\$\d+\s*\|',r'\1 $68 |',s)
    write(prompt,s)

print("Updated files:")
for x in sorted(set(changed)): print(" -",x)
if not changed: raise SystemExit("No changes produced")
