#!/usr/bin/env python3
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
paths = [ROOT/'shows'/'index.html'] + sorted((ROOT/'shows').glob('*/index.html'))

replacements = {
    "venue:\"Bugsy's Cabaret - Flamingo Hotel\"s Cabaret · Flamingo Las Vegas'": "venue:\"Bugsy's Cabaret · Flamingo Las Vegas\"",
    "venue:'King Arthur’s Arena – Excalibur Hotel's Arena · Excalibur'": "venue:\"King Arthur’s Arena · Excalibur\"",
}

replacement_counts = {old: 0 for old in replacements}
for path in paths:
    text = path.read_text(encoding='utf-8')
    original = text
    for old, new in replacements.items():
        count = text.count(old)
        if count:
            replacement_counts[old] += count
            text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding='utf-8')

for old, count in replacement_counts.items():
    if count == 0:
        raise SystemExit(f'Expected malformed catalog string not found anywhere: {old}')

# Syntax-check inline JS on all root/category catalog pages so one malformed
# data value cannot silently zero an entire customer-facing grid.
checked = 0
for path in paths:
    html = path.read_text(encoding='utf-8')
    for i, match in enumerate(re.finditer(r'<script(?:\s[^>]*)?>(.*?)</script>', html, re.S | re.I), 1):
        code = match.group(1).strip()
        if not code or 'application/ld+json' in match.group(0)[:200]:
            continue
        with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as fh:
            fh.write(code)
            temp = fh.name
        proc = subprocess.run(['node', '--check', temp], capture_output=True, text=True)
        Path(temp).unlink(missing_ok=True)
        if proc.returncode:
            raise SystemExit(f'JS syntax error in {path.relative_to(ROOT)} inline script {i}:\n{proc.stderr}')
        checked += 1

print('Repaired malformed catalog strings:')
for old, count in replacement_counts.items():
    print(f'  {count}x {old[:72]}')
print(f'Syntax-checked {checked} inline catalog scripts')
