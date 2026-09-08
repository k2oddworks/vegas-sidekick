#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "show-database.json"
BASE_SCRIPT = ROOT / "scripts" / "reconcile-spotlight.py"

spec = importlib.util.spec_from_file_location("spotlight_reconcile", BASE_SCRIPT)
base = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(base)


def concise_age(rule: str) -> str:
    r = (rule or "").strip()
    if not r:
        return ""
    if re.search(r"(?i)no age restrictions?|all ages", r):
        return "All ages"
    patterns = [
        r"(?i)must be\s+(\d{1,2})\s+years?",
        r"(?i)recommended age:?\s*(\d{1,2})\s+years?",
        r"(?i)ages?\s+(\d{1,2})\+",
        r"(?i)(\d{1,2})\s+years?\s+of age or older",
    ]
    for pat in patterns:
        m = re.search(pat, r)
        if m:
            return f"{m.group(1)}+"
    return r[:60]


def robust_prices(soup: BeautifulSoup) -> list[int]:
    text = " ".join(soup.stripped_strings)
    m = re.search(r"Best price guaranteed\s+From\s+(.{0,60}?)\s+Buy Tickets", text, flags=re.I)
    region = m.group(1) if m else text
    vals = []
    for raw in re.findall(r"\$\s*([0-9]+(?:\.[0-9]+)?)", region):
        v = int(float(raw))
        if v not in vals:
            vals.append(v)
        if len(vals) == 2:
            break
    return vals


def infer_suffix(raw_time: str, rec: dict, name: str) -> str:
    t = raw_time.strip()
    if re.search(r"(?i)[ap]m$", t):
        return base.compact_time(t)
    # Prefer any previously known same-clock value with an explicit suffix.
    hay = " ".join([
        str(rec.get("schedule_summary") or ""),
        " ".join((rec.get("spotlight") or {}).get("schedule_raw") or []),
    ])
    clock = re.escape(t)
    m = re.search(clock + r"\s*([ap]m)", hay, flags=re.I)
    if m:
        return base.compact_time(t + m.group(1))
    # Brunch/morning products are the one recurring morning pattern in this catalog.
    if "brunch" in name.lower():
        return base.compact_time(t + "am")
    return base.compact_time(t + "pm")


def repair_days(rec: dict, name: str):
    spot = rec.get("spotlight") or {}
    raw_lines = spot.get("schedule_raw") or []
    if not raw_lines:
        return
    days = {}
    variable = False
    for line in raw_lines:
        if re.search(r"(?i)(dates?|days?)\s*&?\s*(times?)\s*(may\s*)?vary|times? vary|various times", line):
            variable = True
            continue
        for day in base.DAY_ORDER:
            m = re.match(rf"^{day}\s*[–—-]\s*(.+)$", line, flags=re.I)
            if not m:
                continue
            rhs = m.group(1)
            times = re.findall(r"\b\d{1,2}:\d{2}\s*(?:[ap]m)?\b", rhs, flags=re.I)
            if not times:
                times = re.findall(r"\b\d{1,2}\s*(?:[ap]m)\b", rhs, flags=re.I)
            days[day] = [infer_suffix(t, rec, name) for t in times]
            break
    if days:
        grouped = {}
        for day in base.DAY_ORDER:
            if day not in days:
                continue
            grouped.setdefault(tuple(days[day]), []).append(day)
        parts = []
        for times, group_days in grouped.items():
            label = ", ".join(base.DAY_ABBR[d] for d in group_days)
            parts.append(f"{label} · {' & '.join(times) if times else 'Times vary'}")
        summary = "; ".join(parts)
    elif variable:
        summary = "Dates & times vary · check booking page"
    else:
        return
    spot["schedule_days"] = days
    spot["schedule_variable"] = variable
    spot["schedule_summary"] = summary
    rec["schedule_summary"] = summary


def main():
    data = json.loads(DB_PATH.read_text(encoding="utf-8"))
    session = requests.Session()
    session.headers.update({"User-Agent": "VegasSidekickDataAudit/1.1 (+https://vegassidekick.com/)"})
    refined = 0
    for rec in data.get("records", []):
        if rec.get("status") != "active" or rec.get("verification") != "verified_spotlight":
            continue
        spot = rec.get("spotlight") or {}
        old = dict(rec)
        try:
            resp = session.get(spot.get("spotlight_url") or base.base_spotlight_url(rec.get("ticket_url", "")), timeout=25)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            prices = robust_prices(soup)
            if prices:
                spot["our_price"] = prices[0]
                spot["regular_price"] = prices[1] if len(prices) > 1 else None
                rec["our_price"] = spot["our_price"]
                rec["regular_price"] = spot["regular_price"]
        except Exception as exc:
            print(f"WARN price refine failed for {rec['slug']}: {exc}")

        full_age = spot.get("age_rule") or rec.get("age_summary") or ""
        rec["age_summary"] = concise_age(full_age)
        spot["age_label"] = rec["age_summary"]
        repair_days(rec, rec.get("name") or spot.get("name") or "")

        # Re-run factual page sync using concise display age while preserving full rule in Spotlight data.
        page_spot = dict(spot)
        page_spot["age_rule"] = rec["age_summary"]
        base.sync_page(rec, old, page_spot)
        refined += 1

    data["spotlight_reconciled_on"] = "2026-09-08"
    DB_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    base.update_catalog_arrays(data.get("records", []))
    print(f"Refined {refined} Spotlight-backed records")


if __name__ == "__main__":
    main()
