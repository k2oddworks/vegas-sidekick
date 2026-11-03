#!/usr/bin/env python3
"""Fail when Sidekick Index datasets are missing, swapped, or malformed."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    ("headliners-residencies", "Headliners & Residencies", "act", "dates"),
    ("touring-shows-concerts", "Touring Shows & Concerts", "name", "date"),
)

def validate():
    errors = []
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
    return errors

if __name__ == "__main__":
    problems = validate()
    if problems:
        print("\n".join(problems), file=sys.stderr)
        sys.exit(1)
    print("Sidekick Index datasets: PASS")
