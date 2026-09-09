#!/usr/bin/env python3
"""One-time September 2026 cleanup for buyer-facing negative framing.

Replaces formal "Think twice" / "downside" framing with neutral, useful
"Good to know" language while preserving the underlying factual caveats.
Also updates the governing writing docs so the old labels do not return.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

GUIDANCE = [
    ROOT / "BRAND.md",
    ROOT / "SHOW-BUILDER-PROMPT.md",
    ROOT / "VS_CHAT_CONTEXT.md",
    ROOT / "docs" / "OPERATIONS-BOARD.md",
]

CUSTOMER_HTML = []
for path in ROOT.rglob("*.html"):
    rel = path.relative_to(ROOT)
    if "_archive" in rel.parts:
        continue
    # Admin copy is operational UI, not ticket-shopping/editorial copy.
    if rel.parts and rel.parts[0] == "admin":
        continue
    CUSTOMER_HTML.append(path)

# Exact replacements first, so headings and marketing claims land naturally.
EXACT_HTML = {
    "<h2>Good fit. Think twice.</h2>": "<h2>Is this your kind of show?</h2>",
    "<h3>🤔 Think twice if…</h3>": "<h3>Good to know</h3>",
    "<h3>Think twice if…</h3>": "<h3>Good to know</h3>",
    "<h3>Think twice if...</h3>": "<h3>Good to know</h3>",
    "<h3>Think twice</h3>": "<h3>Good to know</h3>",
    "<h3>The honest downside</h3>": "<h3>Good to know</h3>",
    "<h3>Honest downside</h3>": "<h3>Good to know</h3>",
    "<b>We tell you the downside</b>": "<b>Good to know, up front</b>",
    "<strong>We tell you the downside</strong>": "<strong>Good to know, up front</strong>",
    "Good Fit / Think Twice": "Good Fit / Good to Know",
    "Good fit / Think Twice": "Good fit / Good to know",
    "Good fit / Think twice": "Good fit / Good to know",
    "honest downside for every pick": "practical booking context for every pick",
    "local guides and honest tradeoffs": "local guides and practical booking context",
    "If a show has a tradeoff worth knowing, it belongs in the recommendation.": "If there’s something useful to know before booking, it belongs in the recommendation.",
}

EXACT_GUIDANCE = {
    "Good Fit / Think Twice": "Good Fit / Good to Know",
    "Good fit / Think Twice": "Good fit / Good to know",
    "Good Fit / Think Twice judgment": "Good Fit / Good to Know judgment",
    "**Say the downside.**": "**Give the useful context.**",
    "Say the downside.": "Give the useful context.",
    "Honest Tradeoffs": "Useful Context",
    "honest tradeoffs": "practical booking context",
    "comfortable stating downsides": "comfortable stating practical caveats",
    "comfortable stating downside": "comfortable stating practical caveats",
    "one real downside when it matters": "one useful caveat when it matters",
    "one real downside": "one useful caveat",
}


def apply_exact(text: str, mapping: dict[str, str]) -> str:
    for old, new in mapping.items():
        text = text.replace(old, new)
    return text


def clean_customer_html(text: str) -> str:
    text = apply_exact(text, EXACT_HTML)

    # Label variants with optional punctuation/emoji.
    text = re.sub(
        r"(<h[2-4][^>]*>\s*)(?:🤔\s*)?Think twice(?:\s+if(?:…|\.\.\.))?\s*(</h[2-4]>)",
        r"\1Good to know\2",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"(<(?:b|strong)[^>]*>\s*)(?:The\s+)?(?:honest\s+)?downside\s*:?(\s*</(?:b|strong)>)",
        r"\1Good to know:\2",
        text,
        flags=re.I,
    )

    # Prose should stay candid, just without a dedicated negative command.
    text = re.sub(r"\bThink twice only if\b", "It may be a weaker fit if", text, flags=re.I)
    text = re.sub(r"\bThink twice if\b", "It may be a weaker fit if", text, flags=re.I)
    # Catch any remaining command-style phrase. This does not touch ordinary
    # uses such as "never the same show twice" because the words are not adjacent.
    text = re.sub(r"\bThink twice\b", "Good to know", text, flags=re.I)
    text = re.sub(r"\bdownside(s)?\b", lambda m: "tradeoffs" if m.group(1) else "tradeoff", text, flags=re.I)

    # Cleanup a couple phrases created by the generic tradeoff replacement.
    text = text.replace("an honest tradeoff for every pick", "practical booking context for every pick")
    text = text.replace("the honest tradeoff", "what to know")
    text = text.replace("The honest tradeoff", "Good to know")
    text = text.replace("We tell you the tradeoff", "Good to know, up front")
    return text


def clean_guidance(text: str) -> str:
    text = apply_exact(text, EXACT_GUIDANCE)
    # Change the decision-label rule everywhere in governing docs.
    text = re.sub(r"\bThink twice\b", "Good to know", text, flags=re.I)
    text = re.sub(r"\bdownside(s)?\b", lambda m: "tradeoffs" if m.group(1) else "tradeoff", text, flags=re.I)

    # Make the resulting policy language positive and non-duplicative.
    text = text.replace(
        "**Good to know** is optional and should appear only when there is a real, show-specific tradeoff, mismatch, or tradeoff.",
        "**Good to know** is optional and should appear only when there is useful, show-specific context, a mismatch, or a meaningful tradeoff.",
    )
    text = text.replace(
        "**Good to know** — optional; include only for a real, show-specific mismatch, tradeoff, or tradeoff.",
        "**Good to know** — optional; include only for useful, show-specific context, a mismatch, or a meaningful tradeoff.",
    )
    text = text.replace(
        "Say who the show fits, what to know first and one real tradeoff when it matters.",
        "Say who the show fits, what to know first and one useful caveat when it matters.",
    )
    text = text.replace("**Say the tradeoff.**", "**Give the useful context.**")
    return text


changed = []
for path in sorted(CUSTOMER_HTML):
    before = path.read_text(encoding="utf-8", errors="ignore")
    after = clean_customer_html(before)
    if after != before:
        path.write_text(after, encoding="utf-8")
        changed.append(path.relative_to(ROOT).as_posix())

for path in GUIDANCE:
    if not path.exists():
        continue
    before = path.read_text(encoding="utf-8", errors="ignore")
    after = clean_guidance(before)
    if after != before:
        path.write_text(after, encoding="utf-8")
        changed.append(path.relative_to(ROOT).as_posix())

# Prevent the canonicalizer from regenerating the old command-style phrasing.
canon = ROOT / "scripts" / "canonicalize-show-pages.py"
if canon.exists():
    before = canon.read_text(encoding="utf-8", errors="ignore")
    after = re.sub(r"\bThink twice only if\b", "It may be a weaker fit if", before, flags=re.I)
    after = re.sub(r"\bThink twice if\b", "It may be a weaker fit if", after, flags=re.I)
    # Only change the literal label phrase; do not rename Python identifiers.
    after = after.replace("Think twice if…", "Good to know")
    after = after.replace("Think twice", "Good to know")
    if after != before:
        canon.write_text(after, encoding="utf-8")
        changed.append(canon.relative_to(ROOT).as_posix())

# Validate the customer-facing surface: the old formal language should be gone.
residual = []
for path in sorted(CUSTOMER_HTML):
    text = path.read_text(encoding="utf-8", errors="ignore")
    if re.search(r"\bthink twice\b", text, flags=re.I):
        residual.append(f"{path.relative_to(ROOT)}: still contains 'Think twice'")
    if re.search(r"\bdownsides?\b", text, flags=re.I):
        residual.append(f"{path.relative_to(ROOT)}: still contains 'downside'")

for path in GUIDANCE:
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8", errors="ignore")
    if re.search(r"\bthink twice\b", text, flags=re.I):
        residual.append(f"{path.relative_to(ROOT)}: guidance still contains 'Think twice'")
    if re.search(r"\bdownsides?\b", text, flags=re.I):
        residual.append(f"{path.relative_to(ROOT)}: guidance still contains 'downside'")

if canon.exists() and re.search(r"\bthink twice\b", canon.read_text(encoding="utf-8", errors="ignore"), flags=re.I):
    residual.append("scripts/canonicalize-show-pages.py: still contains 'Think twice'")

print(f"Changed {len(changed)} files:")
for rel in changed:
    print(f"  - {rel}")

if residual:
    print("\nResidual negative framing found:")
    print("\n".join(residual))
    sys.exit(1)

print("\nPositive-framing cleanup complete; no customer-facing 'Think twice' or 'downside' language remains in the scanned active site.")
