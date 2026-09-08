#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
from pathlib import Path

import requests
from bs4 import BeautifulSoup, NavigableString

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "show-database.json"
BASE_SCRIPT = ROOT / "scripts" / "reconcile-spotlight.py"

spec = importlib.util.spec_from_file_location("spotlight_reconcile", BASE_SCRIPT)
base = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(base)


def prior_database() -> dict:
    try:
        raw = subprocess.check_output(["git", "show", "origin/main:data/show-database.json"], cwd=ROOT, text=True)
        return json.loads(raw)
    except Exception:
        return {"records": []}


def parse_runtime(strings: list[str]) -> int | None:
    lines = base.find_section(strings, "Show Length", ["Age Restrictions", "Other Restrictions", "Additional Information:", "Additional Information"])
    text = " ".join(lines)
    m = re.search(r"(\d{2,3})\s*minutes?", text, flags=re.I)
    if m:
        return int(m.group(1))
    m = re.search(r"(\d+(?:\.\d+)?)\s*hours?", text, flags=re.I)
    if m:
        return int(round(float(m.group(1)) * 60))
    return None


def set_full_age_faq(page: Path, full_rule: str):
    if not full_rule or not page.exists():
        return
    soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
    changed = False
    for faq in soup.select("#faq .faq"):
        q = faq.find(["button", "h3", "h4"])
        a = faq.select_one(".faq-a p") or faq.find("p")
        if q and a and re.search(r"(?i)age|young kids|children", q.get_text(" ", strip=True)):
            a.string = full_rule
            changed = True
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        raw = script.string or script.get_text()
        try:
            obj = json.loads(raw)
        except Exception:
            continue
        if obj.get("@type") in ("Event", "EventSeries"):
            obj["audience"] = {"@type": "Audience", "audienceType": full_rule}
            script.string = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
            changed = True
        if obj.get("@type") == "FAQPage":
            for item in obj.get("mainEntity") or []:
                q = str(item.get("name") or "")
                ans = item.get("acceptedAnswer")
                if isinstance(ans, dict) and re.search(r"(?i)age|young kids|children", q):
                    ans["text"] = full_rule
                    changed = True
            script.string = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    if changed:
        page.write_text(str(soup), encoding="utf-8")


def replace_text(scope, old: str, new: str) -> int:
    count = 0
    for node in list(scope.find_all(string=True)):
        if isinstance(node, NavigableString) and old in str(node):
            node.replace_with(str(node).replace(old, new))
            count += 1
    return count


def propagate_linked_prices(old_db: dict, new_db: dict):
    old_by = {r.get("slug"): r for r in old_db.get("records", [])}
    new_by = {r.get("slug"): r for r in new_db.get("records", [])}
    price_changes = []
    for slug, rec in new_by.items():
        old = old_by.get(slug) or {}
        if old.get("our_price") is not None and rec.get("our_price") is not None and old.get("our_price") != rec.get("our_price"):
            price_changes.append((slug, rec.get("page_path"), old["our_price"], rec["our_price"]))
    touched = 0
    for p in sorted(ROOT.rglob("index.html")):
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith("admin/"):
            continue
        soup = BeautifulSoup(p.read_text(encoding="utf-8", errors="ignore"), "html.parser")
        changed = False
        for slug, page_path, old_price, new_price in price_changes:
            if not page_path:
                continue
            anchors = [a for a in soup.find_all("a", href=True) if a["href"].rstrip("/") == page_path.rstrip("/")]
            for a in anchors:
                target = None
                node = a
                for _ in range(5):
                    if node is None:
                        break
                    text = node.get_text(" ", strip=True) if hasattr(node, "get_text") else ""
                    if f"${old_price}" in text and len(text) < 1400:
                        target = node
                        break
                    node = getattr(node, "parent", None)
                if target and replace_text(target, f"${old_price}", f"${new_price}"):
                    changed = True
        if changed:
            p.write_text(str(soup), encoding="utf-8")
            touched += 1
    print(f"Propagated {len(price_changes)} changed show prices across {touched} linked customer pages")


def main():
    old_db = prior_database()
    data = json.loads(DB_PATH.read_text(encoding="utf-8"))
    session = requests.Session()
    session.headers.update({"User-Agent": "VegasSidekickDataAudit/1.2 (+https://vegassidekick.com/)"})
    runtime_changes = 0
    for rec in data.get("records", []):
        if rec.get("status") != "active" or rec.get("verification") != "verified_spotlight":
            continue
        spot = rec.get("spotlight") or {}
        url = spot.get("spotlight_url") or base.base_spotlight_url(rec.get("ticket_url", ""))
        try:
            resp = session.get(url, timeout=25)
            resp.raise_for_status()
            strings = list(BeautifulSoup(resp.text, "html.parser").stripped_strings)
            runtime = parse_runtime(strings)
        except Exception as exc:
            print(f"WARN runtime finalize failed for {rec['slug']}: {exc}")
            runtime = None
        if runtime and runtime != rec.get("runtime_minutes"):
            old = dict(rec)
            rec["runtime_minutes"] = runtime
            spot["runtime_minutes"] = runtime
            page_spot = dict(spot)
            page_spot["age_rule"] = rec.get("age_summary") or ""
            base.sync_page(rec, old, page_spot)
            runtime_changes += 1
        page = ROOT / rec["page_path"].lstrip("/") / "index.html"
        set_full_age_faq(page, spot.get("age_rule") or "")

    DB_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    base.update_catalog_arrays(data.get("records", []))
    propagate_linked_prices(old_db, data)
    print(f"Normalized {runtime_changes} hour/minute runtime edge cases")


if __name__ == "__main__":
    main()
