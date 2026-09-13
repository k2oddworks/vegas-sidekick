#!/usr/bin/env python3
from pathlib import Path
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]

def y(v):
    if not v:return None
    if isinstance(v,dict):v=v.get("video_id") or v.get("url") or v.get("watch_url") or v.get("embed_url") or ""
    v=str(v)
    for p in (r"youtu\.be/([A-Za-z0-9_-]{6,20})",r"[?&]v=([A-Za-z0-9_-]{6,20})",r"/embed/([A-Za-z0-9_-]{6,20})",r"/shorts/([A-Za-z0-9_-]{6,20})"):
        m=re.search(p,v)
        if m:return m.group(1)
    return v if re.fullmatch(r"[A-Za-z0-9_-]{6,20}",v) else None

def rows(o):
    if isinstance(o,list):return o
    if isinstance(o,dict):
        for k in ("shows","records","items"):
            if isinstance(o.get(k),list):return o[k]
    return []

verified={}
p=ROOT/"data/show-database.json"
if p.exists():
    for r in rows(json.loads(p.read_text(encoding="utf-8"))):
        if not isinstance(r,dict):continue
        v=y(r.get("official_trailer") or ((r.get("media") or {}).get("official_trailer") if isinstance(r.get("media"),dict) else None)); page=r.get("page_path") or r.get("canonical_path")
        if v and page and str(r.get("status","active")).lower() not in {"closed","ended","inactive","archived"}:verified[page]=v
for fp in (ROOT/"data/shows").glob("*.json") if (ROOT/"data/shows").exists() else []:
    try:r=json.loads(fp.read_text(encoding="utf-8"))
    except Exception:continue
    v=y(((r.get("media") or {}).get("official_trailer") if isinstance(r.get("media"),dict) else None));page=r.get("canonical_path")
    if v and page and str(r.get("status","active")).lower() not in {"closed","ended","inactive","archived"}:verified[page]=v
problems=[]
for page,vid in sorted(verified.items()):
    fp=ROOT/page.lstrip("/")/"index.html"
    if not fp.exists():problems.append(f"{page}: verified trailer but page missing");continue
    t=fp.read_text(encoding="utf-8",errors="ignore")
    if not re.search(r'class="vs-video"[^>]*data-youtube-id="'+re.escape(vid)+r'"',t):problems.append(f"{page}: verified trailer {vid} missing shared component")
    if re.search(r'<iframe[^>]+youtube',t,re.I):problems.append(f"{page}: eager YouTube iframe found; use click-to-load component")
    if re.search(r'class="(?:video|video-preview)"[^>]*data-(?:youtube-id|video-id)',t):problems.append(f"{page}: legacy video markup remains")
if problems:
    print("Show video audit FAILED:")
    print("\n".join(" - "+x for x in problems));sys.exit(1)
print(f"Show video audit passed: {len(verified)} verified active trailer(s).")
