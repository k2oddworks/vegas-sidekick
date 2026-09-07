#!/usr/bin/env python3
"""Audit Vegas Sidekick's contextual internal-link graph.

This is a reporting tool, not an auto-linker. It ignores global header/footer/nav
links where possible and focuses on the page families that drive discovery,
decision-making and conversion.

Usage:
    python3 scripts/audit-internal-links.py

Writes:
    docs/internal-link-audit.md

The command exits 0 even when opportunities are found. Broken local targets are
reported for review; hard broken-link gating remains the job of audit-site-health.py.
"""

from __future__ import annotations

from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import json
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs" / "internal-link-audit.md"

THRESHOLDS = {
    "show": (3, 2),
    "guide": (4, 2),
    "dispatch": (2, 1),
    "venue": (3, 2),
    "category": (3, 2),
}


def classify(path: Path) -> str | None:
    rel = path.relative_to(ROOT).as_posix()
    if re.fullmatch(r"shows/[^/]+/[^/]+/index\.html", rel):
        return "show"
    if re.fullmatch(r"guides/[^/]+/index\.html", rel):
        return "guide"
    if re.fullmatch(r"news/[^/]+/index\.html", rel):
        return "dispatch"
    if re.fullmatch(r"venues/[^/]+/index\.html", rel):
        return "venue"
    if rel == "shows/index.html" or re.fullmatch(r"shows/[^/]+/index\.html", rel):
        return "category"
    return None


def is_active_show(path: Path, text: str) -> bool:
    if classify(path) != "show":
        return True
    # Closed archives intentionally remain live but should not be forced to act as
    # active conversion hubs.
    return "https://schema.org/EventScheduled" in text


def title_for(path: Path, text: str) -> str:
    m = re.search(r"<title[^>]*>(.*?)</title>", text, re.I | re.S)
    if m:
        title = re.sub(r"<[^>]+>", "", m.group(1))
        title = re.sub(r"\s+", " ", title).strip()
        if "|" in title:
            title = title.split("|", 1)[0].strip()
        return title
    return path.parent.name.replace("-", " ").title()


def contextual_html(text: str) -> str:
    """Remove broad chrome regions before extracting links.

    The site injects much of its shared header/footer at runtime, but pages also
    contain breadcrumbs/sticky nav. Removing these blocks keeps the report focused
    on useful contextual relationships rather than global navigation volume.
    """
    cleaned = text
    for tag in ("header", "footer", "nav", "script", "style", "noscript"):
        cleaned = re.sub(
            rf"<{tag}\b[^>]*>.*?</{tag}>",
            " ",
            cleaned,
            flags=re.I | re.S,
        )
    # Remove common div-based global chrome if present in source HTML.
    cleaned = re.sub(
        r'<div\b[^>]*(?:id|class)=["\'][^"\']*(?:site-header|site-footer|mobile-drawer|global-nav)[^"\']*["\'][^>]*>.*?</div>',
        " ",
        cleaned,
        flags=re.I | re.S,
    )
    return cleaned


def normalize_local_href(href: str) -> str | None:
    href = (href or "").strip()
    if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
        return None
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc:
        if parsed.netloc not in {"vegassidekick.com", "www.vegassidekick.com"}:
            return None
        path = parsed.path
    else:
        path = parsed.path
    if not path or not path.startswith("/"):
        return None
    path = re.sub(r"/{2,}", "/", path)
    if path == "/":
        return "index.html"
    rel = path.lstrip("/")
    if rel.endswith("/"):
        return rel + "index.html"
    if Path(rel).suffix:
        return rel
    return rel + "/index.html"


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []
        self.anchor_href: str | None = None
        self.anchor_text: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        attrs_dict = dict(attrs)
        self.anchor_href = attrs_dict.get("href")
        self.anchor_text = []

    def handle_data(self, data):
        if self.anchor_href is not None:
            self.anchor_text.append(data)

    def handle_endtag(self, tag):
        if tag != "a" or self.anchor_href is None:
            return
        text = re.sub(r"\s+", " ", " ".join(self.anchor_text)).strip()
        self.links.append((self.anchor_href, text))
        self.anchor_href = None
        self.anchor_text = []


def main() -> None:
    html_files = sorted(ROOT.rglob("*.html"))
    existing = {p.relative_to(ROOT).as_posix() for p in html_files}

    pages: dict[str, dict] = {}
    raw_links: dict[str, list[tuple[str, str]]] = defaultdict(list)
    broken: list[tuple[str, str, str]] = []
    graph_out: dict[str, set[str]] = defaultdict(set)

    # Build the complete tracked-page inventory before resolving edges so file
    # traversal order cannot affect whether a target is recognized.
    for path in html_files:
        kind = classify(path)
        if not kind:
            continue
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        pages[rel] = {
            "kind": kind,
            "title": title_for(path, text),
            "active": is_active_show(path, text),
        }
        parser = LinkParser()
        try:
            parser.feed(contextual_html(text))
        except Exception:
            pass
        raw_links[rel] = parser.links

    tracked = set(pages)

    for rel, links in raw_links.items():
        for href, anchor in links:
            target = normalize_local_href(href)
            if not target:
                continue
            if target not in existing:
                broken.append((rel, href, anchor))
                continue
            if target == rel:
                continue
            if target in tracked:
                graph_out[rel].add(target)

    inbound: dict[str, set[str]] = defaultdict(set)
    for src, targets in graph_out.items():
        for dst in targets:
            inbound[dst].add(src)

    rows = []
    opportunities = []
    for rel, meta in pages.items():
        out_count = len(graph_out.get(rel, set()))
        in_count = len(inbound.get(rel, set()))
        min_out, min_in = THRESHOLDS[meta["kind"]]
        # Closed show archives remain part of the graph but are not treated as
        # underlinked active conversion pages.
        review = meta["active"] and (out_count < min_out or in_count < min_in)
        rows.append((meta["kind"], meta["title"], rel, out_count, in_count, review))
        if review:
            reasons = []
            if out_count < min_out:
                reasons.append(f"outbound {out_count}/{min_out}")
            if in_count < min_in:
                reasons.append(f"inbound {in_count}/{min_in}")
            opportunities.append((in_count + out_count, rel, meta["title"], meta["kind"], ", ".join(reasons)))

    rows.sort(key=lambda r: (r[0], r[1].lower()))
    opportunities.sort(key=lambda r: (r[0], r[3], r[2].lower()))

    summary = defaultdict(int)
    weak_summary = defaultdict(int)
    for kind, _, _, _, _, review in rows:
        summary[kind] += 1
        if review:
            weak_summary[kind] += 1

    out = [
        "# Vegas Sidekick Internal Link Audit",
        "",
        "Generated from contextual links in the current checkout. Global header/footer/navigation links are excluded where detectable. Thresholds are review signals, not permission for automated link insertion.",
        "",
        "## Summary",
        "",
        "| Page family | Pages | Review candidates |",
        "|---|---:|---:|",
    ]
    for kind in ("show", "guide", "dispatch", "venue", "category"):
        out.append(f"| {kind.title()} | {summary[kind]} | {weak_summary[kind]} |")

    out += [
        "",
        f"- Broken contextual local targets found: **{len(broken)}**",
        f"- Total review candidates: **{len(opportunities)}**",
        "",
        "## Highest-priority linking opportunities",
        "",
        "Pages with the weakest combined contextual support appear first. Review relevance before adding anything.",
        "",
        "| Type | Page | Issue |",
        "|---|---|---|",
    ]
    if opportunities:
        for _, rel, title, kind, reason in opportunities:
            out.append(f"| {kind.title()} | [{title}](/{rel.removesuffix('index.html')}) | {reason} |")
    else:
        out.append("| — | — | No pages below current review thresholds |")

    out += [
        "",
        "## Full graph inventory",
        "",
        "| Type | Page | Contextual outbound | Contextual inbound | Review |",
        "|---|---|---:|---:|:---:|",
    ]
    for kind, title, rel, out_count, in_count, review in rows:
        out.append(f"| {kind.title()} | [{title}](/{rel.removesuffix('index.html')}) | {out_count} | {in_count} | {'Yes' if review else '—'} |")

    out += ["", "## Broken contextual local targets", ""]
    if broken:
        out += ["| Source | Href | Anchor |", "|---|---|---|"]
        for src, href, anchor in sorted(broken)[:200]:
            safe_anchor = (anchor or "—").replace("|", "/")
            out.append(f"| `{src}` | `{href}` | {safe_anchor} |")
        if len(broken) > 200:
            out.append(f"\n_First 200 shown; {len(broken) - 200} additional targets omitted._")
    else:
        out.append("No broken contextual local targets found.")

    out += [
        "",
        "## Interpretation",
        "",
        "- A low count is a **review flag**, not an instruction to manufacture links.",
        "- A high count is not automatically good; relevance still wins.",
        "- Closed show archives are counted in the graph but exempt from active-show thresholds.",
        "- The audit should be paired with Search Console/conversion data when choosing which opportunities to fix first.",
        "",
    ]

    REPORT.write_text("\n".join(out), encoding="utf-8")
    print(json.dumps({
        "tracked_pages": len(pages),
        "review_candidates": len(opportunities),
        "broken_contextual_targets": len(broken),
        "report": str(REPORT.relative_to(ROOT)),
    }, indent=2))


if __name__ == "__main__":
    main()
