#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup, NavigableString

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "show-database.json"
REPORT_PATH = ROOT / "docs" / "spotlight-reconciliation-2026-09-08.md"
DAY_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
DAY_ABBR = {d: d[:3] for d in DAY_ORDER}

# Explicit editorial/source-of-truth overrides for schedules that cannot safely be
# represented by the current public Spotlight markup. Do not remove without re-verifying.
MANUAL_SCHEDULE_OVERRIDES = {
    "marc-savard-comedy-hypnosis": {
        "schedule_days": {},
        "schedule_summary": "Times vary · Check live calendar",
        "schedule_variable": True,
        "schedule_raw": [],
    },
}


def money_values(text: str) -> list[int]:
    vals = []
    for raw in re.findall(r"\$\s*([0-9]+(?:\.[0-9]+)?)", text):
        val = int(float(raw))
        if val not in vals:
            vals.append(val)
    return vals


def base_spotlight_url(url: str) -> str:
    url = (url or "").strip()
    if not url:
        return ""
    url = re.sub(r"/ref/[^/?#]+/?(?:[?#].*)?$", "/", url)
    if not url.endswith("/"):
        url += "/"
    return url


def affiliate_url(url: str) -> str:
    base = base_spotlight_url(url)
    return base.rstrip("/") + "/ref/vegassidekick" if base else ""


def compact_time(value: str) -> str:
    s = value.strip()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"(?i)(\d{1,2}):00\s*([ap]m)", lambda m: f"{m.group(1)} {m.group(2).upper()}", s)
    s = re.sub(r"(?i)(\d{1,2}):(\d{2})\s*([ap]m)", lambda m: f"{m.group(1)}:{m.group(2)} {m.group(3).upper()}", s)
    s = s.replace("&", "&")
    return s


def find_section(strings: list[str], start_label: str, end_labels: list[str]) -> list[str]:
    try:
        start = next(i for i, s in enumerate(strings) if s.strip() == start_label)
    except StopIteration:
        return []
    out = []
    for s in strings[start + 1:]:
        if s.strip() in end_labels:
            break
        if s.strip():
            out.append(s.strip())
    return out


def parse_schedule(lines: list[str]) -> tuple[dict[str, list[str]], str, bool]:
    days: dict[str, list[str]] = {}
    variable = False
    notes = []
    for raw in lines:
        line = re.sub(r"\s+", " ", raw).strip()
        if not line:
            continue
        if re.search(r"(?i)(dates?|days?)\s*&?\s*(times?)\s*(may\s*)?vary|times? vary|various times", line):
            variable = True
            notes.append(line)
            continue
        matched = False
        for day in DAY_ORDER:
            m = re.match(rf"^{day}\s*[–—-]\s*(.+)$", line, flags=re.I)
            if m:
                rhs = m.group(1).strip()
                times = re.findall(r"\b\d{1,2}:\d{2}\s*[ap]m\b", rhs, flags=re.I)
                if not times:
                    times = re.findall(r"\b\d{1,2}\s*[ap]m\b", rhs, flags=re.I)
                days[day] = [compact_time(t) for t in times]
                matched = True
                break
        if not matched and line not in notes:
            notes.append(line)

    if days:
        grouped: dict[tuple[str, ...], list[str]] = defaultdict(list)
        for day in DAY_ORDER:
            if day in days:
                grouped[tuple(days[day])].append(day)
        parts = []
        for times, group_days in grouped.items():
            labels = ", ".join(DAY_ABBR[d] for d in group_days)
            time_label = " & ".join(times) if times else "Times vary"
            parts.append(f"{labels} · {time_label}")
        summary = "; ".join(parts)
    elif variable:
        summary = "Dates & times vary · check booking page"
    else:
        summary = " · ".join(notes[:3])
    return days, summary, variable


def scrape_product(session: requests.Session, url: str) -> dict:
    response = session.get(base_spotlight_url(url), timeout=25, allow_redirects=True)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    strings = list(soup.stripped_strings)

    h1 = soup.find("h1")
    name = h1.get_text(" ", strip=True) if h1 else ""

    # Primary price lives between the first 'From' label and Buy Tickets.
    price_text = ""
    try:
        idx = next(i for i, s in enumerate(strings) if s.strip() == "From")
        price_text = " ".join(strings[idx + 1: idx + 4])
    except StopIteration:
        pass
    prices = money_values(price_text)

    location_lines = find_section(strings, "Show Location", ["Show Days & Times", "Show Length", "Age Restrictions"])
    schedule_lines = find_section(strings, "Show Days & Times", ["Show Length", "Age Restrictions", "Other Restrictions"])
    length_lines = find_section(strings, "Show Length", ["Age Restrictions", "Other Restrictions", "Additional Information:"])
    age_lines = find_section(strings, "Age Restrictions", ["Other Restrictions", "Additional Information:", "You may also like…"])
    restriction_lines = find_section(strings, "Other Restrictions", ["Additional Information:", "You may also like…"])

    runtime = None
    if length_lines:
        m = re.search(r"(\d{2,3})\s*minutes?", " ".join(length_lines), flags=re.I)
        if m:
            runtime = int(m.group(1))

    schedule_days, schedule_summary, variable = parse_schedule(schedule_lines)
    final_base = base_spotlight_url(response.url)

    return {
        "name": name,
        "our_price": prices[0] if prices else None,
        "regular_price": prices[1] if len(prices) > 1 else None,
        "location": " · ".join(location_lines[:2]) if location_lines else "",
        "runtime_minutes": runtime,
        "age_rule": " ".join(age_lines).strip(),
        "other_restrictions": " ".join(restriction_lines).strip(),
        "schedule_days": schedule_days,
        "schedule_summary": schedule_summary,
        "schedule_variable": variable,
        "schedule_raw": schedule_lines,
        "spotlight_url": final_base,
        "affiliate_url": affiliate_url(final_base),
    }


def replace_text_nodes(scope, old: str, new: str):
    if old == new or not old or not new:
        return
    for node in list(scope.find_all(string=True)):
        if isinstance(node, NavigableString) and old in str(node):
            node.replace_with(str(node).replace(old, new))


def set_fact(soup: BeautifulSoup, label: str, value: str):
    for fact in soup.select(".fact"):
        span = fact.find("span")
        strong = fact.find("strong")
        if span and strong and span.get_text(" ", strip=True).lower() == label.lower():
            strong.clear()
            strong.append(value)
            for attr in ["data-count", "data-prefix", "data-suffix"]:
                strong.attrs.pop(attr, None)
            return True
    return False


def set_chip_values(soup: BeautifulSoup, runtime: int | None, age: str, venue: str):
    chips = soup.select(".hero .chips .chip")
    if not chips:
        return
    if runtime and len(chips) >= 1:
        chips[0].string = f"{runtime} minutes"
    if age and len(chips) >= 2:
        chips[1].string = age
    if venue and len(chips) >= 3:
        chips[2].string = venue


def schedule_objects(days: dict[str, list[str]]) -> list[dict]:
    out = []
    grouped: dict[tuple[str, ...], list[str]] = defaultdict(list)
    for day in DAY_ORDER:
        if day in days:
            grouped[tuple(days[day])].append(day)
    for times, group_days in grouped.items():
        for display in times:
            m = re.match(r"(\d{1,2})(?::(\d{2}))?\s+(AM|PM)", display, flags=re.I)
            if not m:
                continue
            h = int(m.group(1)); minute = int(m.group(2) or 0); ap = m.group(3).upper()
            if ap == "PM" and h != 12: h += 12
            if ap == "AM" and h == 12: h = 0
            out.append({"@type": "Schedule", "byDay": [f"https://schema.org/{d}" for d in group_days], "startTime": f"{h:02d}:{minute:02d}"})
    return out


def update_jsonld(soup: BeautifulSoup, rec: dict, spot: dict):
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        raw = script.string or script.get_text()
        try:
            obj = json.loads(raw)
        except Exception:
            continue
        typ = obj.get("@type")
        if typ in ("Event", "EventSeries"):
            offers = obj.setdefault("offers", {"@type": "Offer"})
            if spot.get("our_price") is not None:
                offers["price"] = spot["our_price"]
                offers["priceCurrency"] = "USD"
            if spot.get("affiliate_url"):
                offers["url"] = spot["affiliate_url"]
            if spot.get("location"):
                loc = obj.setdefault("location", {"@type": "Place"})
                if isinstance(loc, dict):
                    loc["name"] = spot["location"]
            if spot.get("runtime_minutes"):
                obj["duration"] = f"PT{spot['runtime_minutes']}M"
            if spot.get("age_rule"):
                obj["audience"] = {"@type": "Audience", "audienceType": spot["age_rule"]}
            if spot.get("schedule_days"):
                sched = schedule_objects(spot["schedule_days"])
                if sched:
                    obj["eventSchedule"] = sched[0] if len(sched) == 1 else sched
            elif spot.get("schedule_variable"):
                obj.pop("eventSchedule", None)
            script.string = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
        elif typ == "FAQPage":
            for item in obj.get("mainEntity") or []:
                q = str(item.get("name") or "").lower()
                ans = item.get("acceptedAnswer")
                if not isinstance(ans, dict):
                    continue
                if "how much" in q or "ticket" in q and "cost" in q:
                    if spot.get("our_price") is not None:
                        ans["text"] = f"Tickets currently start at ${spot['our_price']}. Your date and seat determine the final total."
                elif "how long" in q or "runtime" in q:
                    if spot.get("runtime_minutes"):
                        ans["text"] = f"Spotlight currently lists the show length as {spot['runtime_minutes']} minutes."
                elif "age" in q or "young kids" in q or "children" in q:
                    if spot.get("age_rule"):
                        ans["text"] = spot["age_rule"]
            script.string = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def update_schedule_section(soup: BeautifulSoup, spot: dict):
    section = soup.find(id="showtimes") or soup.find(id="schedule")
    if not section:
        return
    lede = section.select_one(".lede")
    summary = spot.get("schedule_summary") or "Check current schedule"
    if lede:
        lede.string = f"Typical schedule: {summary}. Check the live booking page for the dates currently available."
    grid = section.select_one(".schedule")
    if not grid:
        return
    grid.clear()
    if spot.get("schedule_days"):
        for day in DAY_ORDER:
            div = soup.new_tag("div")
            times = spot["schedule_days"].get(day)
            if times:
                div["class"] = ["day"]
                a = soup.new_tag("a", href=spot["affiliate_url"], target="_blank", rel="noopener sponsored")
                strong = soup.new_tag("strong"); strong.string = DAY_ABBR[day]
                span = soup.new_tag("span"); span.string = " & ".join(times)
                a.extend([strong, span]); div.append(a)
            else:
                div["class"] = ["day", "dark"]
                strong = soup.new_tag("strong"); strong.string = DAY_ABBR[day]
                span = soup.new_tag("span"); span.string = "Dark"
                div.extend([strong, span])
            grid.append(div)
    else:
        div = soup.new_tag("div")
        div["class"] = ["day"]
        div["style"] = "grid-column:1/-1"
        strong = soup.new_tag("strong"); strong.string = "Schedule"
        span = soup.new_tag("span"); span.string = summary
        div.extend([strong, span]); grid.append(div)


def update_visible_faq(soup: BeautifulSoup, spot: dict):
    for faq in soup.select("#faq .faq"):
        q = faq.find(["button", "h3", "h4"])
        a = faq.select_one(".faq-a p") or faq.find("p")
        if not q or not a:
            continue
        qt = q.get_text(" ", strip=True).lower()
        if ("age" in qt or "young kids" in qt or "children" in qt) and spot.get("age_rule"):
            a.string = spot["age_rule"]
        elif ("how long" in qt or "runtime" in qt) and spot.get("runtime_minutes"):
            a.string = f"Spotlight currently lists the show length as {spot['runtime_minutes']} minutes."
        elif ("how much" in qt or ("ticket" in qt and "cost" in qt)) and spot.get("our_price") is not None:
            a.string = f"Tickets currently start at ${spot['our_price']}. Your date and seat determine the final total."


def sync_page(rec: dict, old: dict, spot: dict) -> list[str]:
    path = ROOT / rec["page_path"].lstrip("/") / "index.html"
    if not path.exists():
        return ["page missing"]
    html = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    changes = []

    old_url = old.get("ticket_url") or ""
    new_url = spot.get("affiliate_url") or old_url
    if old_url and new_url and old_url != new_url:
        html = html.replace(old_url, new_url)
        soup = BeautifulSoup(html, "html.parser")
        changes.append("ticket URL")

    old_price = old.get("our_price")
    new_price = spot.get("our_price")
    if new_price is not None:
        price = soup.select_one(".buybox .price")
        if price:
            price.clear()
            small = soup.new_tag("small"); small.string = "Tickets from"
            price.extend([small, f"${new_price}"])
        set_fact(soup, "Tickets from", f"${new_price}")
        for tag in [soup.title, *soup.find_all("meta", attrs={"name": "description"}), *soup.find_all("meta", attrs={"property": re.compile(r"^og:(title|description)$")})]:
            if not tag:
                continue
            if tag.name == "title" and old_price is not None and tag.string:
                tag.string.replace_with(str(tag.string).replace(f"${old_price}", f"${new_price}"))
            elif tag.name == "meta" and old_price is not None and tag.get("content"):
                tag["content"] = tag["content"].replace(f"${old_price}", f"${new_price}")
        changes.append("price")

    old_runtime = old.get("runtime_minutes")
    new_runtime = spot.get("runtime_minutes")
    if new_runtime:
        set_fact(soup, "Runtime", f"{new_runtime} min")
        if old_runtime and old_runtime != new_runtime:
            for scope in [soup.select_one("#quick"), soup.select_one("#faq")]:
                if scope:
                    replace_text_nodes(scope, f"{old_runtime}-minute", f"{new_runtime}-minute")
                    replace_text_nodes(scope, f"{old_runtime} minutes", f"{new_runtime} minutes")
        changes.append("runtime")

    age = spot.get("age_rule") or old.get("age_summary") or ""
    set_fact(soup, "Age guidance", age)
    set_chip_values(soup, new_runtime, age, spot.get("location") or old.get("venue") or "")
    update_visible_faq(soup, spot)
    update_schedule_section(soup, spot)
    update_jsonld(soup, rec, spot)

    eyebrow = soup.select_one(".hero .eyebrow")
    if eyebrow and spot.get("location"):
        current = eyebrow.get_text(" ", strip=True)
        if "·" in current:
            eyebrow.string = current.split("·", 1)[0].strip() + " · " + spot["location"]

    # Keep all Spotlight referral links normalized to the canonical product path.
    if new_url:
        for a in soup.find_all("a", href=True):
            if "spotlight.vegas" in a["href"] and (old_url and old_url in a["href"] or rec["slug"] in a["href"]):
                a["href"] = new_url

    rendered = str(soup)
    path.write_text(rendered, encoding="utf-8")
    changes.extend(["age", "venue", "schedule", "schema"])
    return changes


def update_catalog_arrays(records: list[dict]):
    by_slug = {r["slug"]: r for r in records if r.get("status") == "active"}
    for p in [ROOT / "shows" / "index.html", *sorted((ROOT / "shows").glob("*/index.html"))]:
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        original = text
        for slug, rec in by_slug.items():
            spot = rec.get("spotlight") or {}
            price = rec.get("our_price")
            runtime = rec.get("runtime_minutes")
            age = rec.get("age_summary") or ""
            venue = rec.get("venue") or ""
            schedule = rec.get("schedule_summary") or ""
            pattern = re.compile(r"\{[^\n]*slug:'" + re.escape(slug) + r"'[^\n]*\}")
            m = pattern.search(text)
            if not m:
                continue
            line = m.group(0)
            if price is not None:
                line = re.sub(r"price:\s*\d+(?:\.\d+)?", f"price:{price}", line)
                line = re.sub(r"pd:'\$\d+(?:\.\d+)?'", f"pd:'${price}'", line)
            if runtime:
                line = re.sub(r"duration:'[^']*'", f"duration:'{runtime} min'", line)
            if age:
                line = re.sub(r"age:'[^']*'", "age:" + repr(age), line)
            if venue:
                line = re.sub(r"venue:'[^']*'", "venue:" + repr(venue), line)
            if schedule:
                line = re.sub(r"schedule:'[^']*'", "schedule:" + repr(schedule), line)
            text = text[:m.start()] + line + text[m.end():]
        if text != original:
            p.write_text(text, encoding="utf-8")


def main() -> int:
    data = json.loads(DB_PATH.read_text(encoding="utf-8"))
    session = requests.Session()
    session.headers.update({"User-Agent": "VegasSidekickDataAudit/1.0 (+https://vegassidekick.com/)"})
    report = ["# Spotlight reconciliation — 2026-09-08", "", "Operational facts refreshed from current Spotlight product pages.", ""]
    matched = 0
    failed = 0
    changed_pages = 0

    for rec in data.get("records", []):
        if rec.get("status") != "active":
            continue
        old = dict(rec)
        url = rec.get("ticket_url") or ""
        if "spotlight.vegas" not in url:
            rec["verification"] = "needs_review"
            report.append(f"- ❓ **{rec['name']}** — no Spotlight URL in database")
            failed += 1
            continue
        try:
            spot = scrape_product(session, url)
            manual_schedule = MANUAL_SCHEDULE_OVERRIDES.get(rec.get("slug"))
            if manual_schedule:
                spot.update(manual_schedule)
        except Exception as exc:
            rec["verification"] = "needs_review"
            report.append(f"- ❌ **{rec['name']}** — Spotlight fetch failed: {exc}")
            failed += 1
            continue
        if not spot.get("name") or spot.get("our_price") is None:
            rec["verification"] = "needs_review"
            report.append(f"- ❓ **{rec['name']}** — Spotlight page did not expose enough labeled show data")
            failed += 1
            continue

        rec["spotlight"] = spot
        rec["our_price"] = spot["our_price"]
        rec["regular_price"] = spot["regular_price"]
        if spot.get("runtime_minutes"):
            rec["runtime_minutes"] = spot["runtime_minutes"]
        if spot.get("age_rule"):
            rec["age_summary"] = spot["age_rule"]
        if spot.get("location"):
            rec["venue"] = spot["location"]
            rec["showroom"] = ""
        if spot.get("schedule_summary"):
            rec["schedule_summary"] = spot["schedule_summary"]
        rec["ticket_url"] = spot["affiliate_url"]
        rec["verified_on"] = date.today().isoformat()
        rec["verification"] = "verified_spotlight"
        matched += 1

        deltas = []
        for field in ["our_price", "regular_price", "runtime_minutes", "age_summary", "venue", "schedule_summary", "ticket_url"]:
            if old.get(field) != rec.get(field):
                deltas.append(f"{field}: {old.get(field)!r} → {rec.get(field)!r}")
        page_changes = sync_page(rec, old, spot)
        changed_pages += 1
        report.append(f"- ✅ **{rec['name']}** — " + ("; ".join(deltas) if deltas else "matched existing operational facts"))

    data["updated_on"] = date.today().isoformat()
    data["spotlight_reconciled_on"] = date.today().isoformat()
    DB_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    update_catalog_arrays(data.get("records", []))

    report.extend(["", f"Matched/refreshed: **{matched}**", f"Needs review / fetch failures: **{failed}**", f"Customer show pages synced: **{changed_pages}**", ""])
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(report), encoding="utf-8")
    print(f"Spotlight reconciliation complete: matched={matched}, failed={failed}, pages={changed_pages}")
    if failed:
        print(f"WARNING: {failed} records still need review; see {REPORT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
