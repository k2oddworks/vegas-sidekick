#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

# Make the canonical generator produce the approved labels going forward.
p=ROOT/'scripts/canonicalize-show-pages.py'
t=p.read_text(encoding='utf-8')
for old,new in [
    ('Book it if…','Good fit'),('Book it if...','Good fit'),
    ('Know this first','Think twice'),('Best practical angle','Booking tip')]:
    t=t.replace(old,new)
p.write_text(t,encoding='utf-8')

# Record the product/content rule in the living briefing.
p=ROOT/'VS_CHAT_CONTEXT.md'; t=p.read_text(encoding='utf-8')
marker='## Show Decision Cards'
if marker not in t:
    t += '''\n\n---\n\n## Show Decision Cards\n\nThe customer-facing three-card decision aid uses these labels:\n\n- **Good fit** — who the show is genuinely a match for.\n- **Think twice** — one honest mismatch, tradeoff, or reason to choose another category.\n- **Booking tip** — a concrete seat, timing, or booking action.\n\nDo not use the old labels `Book it if…`, `Know this first`, or `Best practical angle`. Do not fill these cards with generic category filler when a useful show-specific point is available. If there is no defensible booking tip, use a verified planning action rather than inventing seat advice. Existing custom/benchmark decision modules that are more detailed should not be flattened just to match the generic card format.\n'''
p.write_text(t,encoding='utf-8')

# Add the same rule to the builder guide.
p=ROOT/'SHOW-BUILDER-PROMPT.md'; t=p.read_text(encoding='utf-8')
marker='### Decision-card standard (September 2026)'
if marker not in t:
    t += '''\n\n### Decision-card standard (September 2026)\nUse **Good fit**, **Think twice**, and **Booking tip** for the three-card buyer decision aid. The copy must be useful on its own and specific to the show when possible. Never use the retired labels **Book it if…**, **Know this first**, or **Best practical angle**. Preserve stronger custom decision modules on benchmark pages rather than flattening them.\n'''
p.write_text(t,encoding='utf-8')

# Add a permanent Operations gate so old labels cannot silently return.
p=ROOT/'.github/workflows/operations-audits.yml'; t=p.read_text(encoding='utf-8')
if 'show-decision-copy:' not in t:
    t += '''\n\n  show-decision-copy:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - name: Audit show decision-card copy\n        run: python3 scripts/audit-show-decision-copy.py\n'''
p.write_text(t,encoding='utf-8')

print('Finalized generator, documentation and Operations guardrail for show decision cards.')
