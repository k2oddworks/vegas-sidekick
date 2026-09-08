#!/usr/bin/env python3
"""Fail when inline JavaScript on a show catalog page is syntactically invalid."""
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CATALOGS = [ROOT / "shows" / "index.html"] + sorted((ROOT / "shows").glob("*/index.html"))

checked = 0
failures = []
for path in CATALOGS:
    html = path.read_text(encoding="utf-8")
    for index, match in enumerate(re.finditer(r'<script(?:\s[^>]*)?>(.*?)</script>', html, re.S | re.I), 1):
        tag = match.group(0)[:240]
        code = match.group(1).strip()
        if not code or "application/ld+json" in tag:
            continue
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as handle:
            handle.write(code)
            temp_path = Path(handle.name)
        result = subprocess.run(["node", "--check", str(temp_path)], capture_output=True, text=True)
        temp_path.unlink(missing_ok=True)
        checked += 1
        if result.returncode:
            failures.append(f"{path.relative_to(ROOT)} inline script {index}:\n{result.stderr.strip()}")

print(f"Catalog pages checked: {len(CATALOGS)}")
print(f"Inline JavaScript blocks checked: {checked}")
if failures:
    print(f"Syntax failures: {len(failures)}")
    for failure in failures:
        print(f"\n{failure}")
    raise SystemExit(1)
print("All show catalog JavaScript parses cleanly.")
