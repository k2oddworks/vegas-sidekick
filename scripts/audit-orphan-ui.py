#!/usr/bin/env python3
"""Fail on known deprecated show-page UI labels/generators."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
problems = []

for path in root.glob('shows/*/*/index.html'):
    text = path.read_text(encoding='utf-8', errors='ignore')
    checks = [
        (r'>\s*Typical start\s*<', 'visible "Typical start" label'),
        (r'>\s*Think twice\s*<', 'visible recurring "Think twice" label'),
        (r'>\s*Honest downside\s*<', 'visible "Honest downside" label'),
    ]
    for pattern, label in checks:
        if re.search(pattern, text, re.I):
            problems.append(f'{path.relative_to(root)}: {label}')

runtime = (root / 'components/show-canonical-runtime.js').read_text(encoding='utf-8')
if 'Good fit / Think twice' in runtime or '<h3>Think twice</h3>' in runtime:
    problems.append('components/show-canonical-runtime.js: deprecated Think twice fallback generator')
canon = (root / 'scripts/canonicalize-show-pages.py').read_text(encoding='utf-8')
if 'fact(first_time, "Typical start")' in canon:
    problems.append('scripts/canonicalize-show-pages.py: deprecated Typical start generator')

if problems:
    print('Orphan UI audit FAILED:')
    for problem in problems:
        print(' -', problem)
    raise SystemExit(1)
print('Orphan UI audit passed.')
