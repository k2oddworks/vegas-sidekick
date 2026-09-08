#!/usr/bin/env python3
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
page = ROOT / 'shows' / 'index.html'
text = page.read_text(encoding='utf-8')
old = "venue:\"Bugsy's Cabaret - Flamingo Hotel\"s Cabaret · Flamingo Las Vegas'"
new = "venue:\"Bugsy's Cabaret · Flamingo Las Vegas\""
if old not in text:
    raise SystemExit('Expected malformed X Burlesque venue string not found')
text = text.replace(old, new, 1)
page.write_text(text, encoding='utf-8')

# Syntax-check inline JS on all catalog pages so one broken record cannot zero a whole grid.
paths = [ROOT/'shows'/'index.html'] + sorted((ROOT/'shows').glob('*/index.html'))
checked = 0
for path in paths:
    html = path.read_text(encoding='utf-8')
    for i, match in enumerate(re.finditer(r'<script(?:\s[^>]*)?>(.*?)</script>', html, re.S | re.I), 1):
        code = match.group(1).strip()
        if not code or code.startswith('{') or 'application/ld+json' in match.group(0)[:200]:
            continue
        with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as fh:
            fh.write(code)
            temp = fh.name
        proc = subprocess.run(['node', '--check', temp], capture_output=True, text=True)
        Path(temp).unlink(missing_ok=True)
        if proc.returncode:
            raise SystemExit(f'JS syntax error in {path.relative_to(ROOT)} inline script {i}:\n{proc.stderr}')
        checked += 1
print(f'Fixed root catalog and syntax-checked {checked} inline catalog scripts')
