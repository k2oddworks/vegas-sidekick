#!/usr/bin/env python3
"""Fail when Sidekick Index datasets are missing, swapped, malformed, or duplicated."""
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    ("headliners-residencies", "Headliners & Residencies", "act", "dates"),
    ("touring-shows-concerts", "Touring Shows & Concerts", "name", "date"),
)
STATUSES = {"canceled"}


def name_key(text):
    """Order- and punctuation-insensitive key, so 'The X 2027' matches '2027 X'."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    return " ".join(sorted(re.sub(r"[^a-z0-9]+", " ", text).split()))


def validate():
    errors = []
    performances = defaultdict(list)  # (name key, date) -> [(dataset, name)]
    for stem, expected, act_key, date_key in FILES:
        path = ROOT / "data" / "reference" / f"{stem}.json"
        try:
            obj = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            errors.append(f"{path}: {exc}")
            continue
        if expected.casefold() not in obj.get("name", "").casefold():
            errors.append(f"{path}: wrong dataset title: {obj.get('name')!r}")
        entries = obj.get("entries")
        if not isinstance(entries, list) or not entries:
            errors.append(f"{path}: entries must be a populated list")
            continue
        for i, entry in enumerate(entries):
            if not isinstance(entry, dict) or not entry.get(act_key):
                errors.append(f"{path}: entry {i} missing {act_key}")
                continue
            dates = entry.get(date_key)
            if stem == "headliners-residencies":
                if not isinstance(dates, list) or not dates:
                    errors.append(f"{path}: entry {i} missing date list")
                    continue
            else:
                dates = [dates]
            for day in dates:
                if not isinstance(day, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", day):
                    errors.append(f"{path}: entry {i} malformed date {day!r}")
            status = entry.get("status")
            if status is not None:
                if status not in STATUSES:
                    errors.append(f"{path}: entry {i} ({entry[act_key]}) unknown status {status!r}")
                elif not entry.get("notes"):
                    errors.append(f"{path}: entry {i} ({entry[act_key]}) {status} needs a notes explanation")
                continue  # canceled records are preserved but never count as live performances
            for day in dates:
                if isinstance(day, str):
                    performances[(name_key(entry[act_key]), day)].append((stem, entry[act_key]))
    for (_, day), found in sorted(performances.items(), key=lambda kv: kv[0][1]):
        if len(found) > 1:
            where = ", ".join(f"{stem}: {name}" for stem, name in found)
            errors.append(f"duplicate performance on {day}: {where}")
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        print("\n".join(problems), file=sys.stderr)
        sys.exit(1)
    print("Sidekick Index datasets: PASS")
