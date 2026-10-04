#!/usr/bin/env python3
"""Full curated internal-link build for Vegas Sidekick.

Adds only high-confidence contextual relationships. It does not change category
membership, guide rankings, factual show data, or affiliate URLs.
"""
from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parents[1]

# Source show -> target show. The script reads the target page for current name,
# image and starting price so this map never becomes a second price database.
SHOW_RELATED = {
    "shows/magic/the-mentalist/index.html": "shows/magic/mind2mind/index.html",
    "shows/magic/colin-cloud/index.html": "shows/magic/mind2mind/index.html",
    "shows/magic/mind2mind/index.html": "shows/magic/colin-cloud/index.html",
    "shows/magic/paranormal/index.html": "shows/magic/the-mentalist/index.html",
    "shows/comedy/marc-savard-comedy-hypnosis/index.html": "shows/comedy/steve-falcons-comedy-hypnosis-hour/index.html",
    "shows/comedy/steve-falcons-comedy-hypnosis-hour/index.html": "shows/comedy/marc-savard-comedy-hypnosis/index.html",
    "shows/comedy/tape-face/index.html": "shows/comedy/carrot-top/index.html",
    "shows/comedy/carrot-top/index.html": "shows/comedy/tape-face/index.html",
    "shows/adult/chippendales/index.html": "shows/adult/magic-mike-live/index.html",
    "shows/adult/magic-mike-live/index.html": "shows/adult/chippendales/index.html",
    "shows/adult/zombie-burlesque/index.html": "shows/adult/atomic-saloon/index.html",
    "shows/adult/atomic-saloon/index.html": "shows/adult/zombie-burlesque/index.html",
    "shows/music/mj-live/index.html": "shows/cirque/michael-jackson-one/index.html",
    "shows/cirque/michael-jackson-one/index.html": "shows/music/mj-live/index.html",
    "shows/music/all-motown/index.html": "shows/music/soul-of-motown/index.html",
    "shows/music/soul-of-motown/index.html": "shows/music/all-motown/index.html",
    "shows/family/battlebots-destruct-a-thon/index.html": "shows/family/tournament-of-kings/index.html",
    "shows/family/tournament-of-kings/index.html": "shows/family/battlebots-destruct-a-thon/index.html",
}

# All eight Guides get a useful cross-guide path. These are discovery links, not
# ranking changes inside the guides themselves.
GUIDE_LINKS = {
    "guides/best-shows-for-first-timers/index.html": [
        ("/guides/best-shows-for-couples/", "Planning a date night?", "Compare the shows that work best for couples."),
        ("/guides/best-shows-for-families/", "Bringing kids?", "Switch to the family-friendly shortlist."),
        ("/guides/best-cheap-vegas-shows/", "Watching the budget?", "See the strongest lower-cost show options."),
    ],
    "guides/best-shows-for-couples/index.html": [
        ("/guides/best-shows-for-first-timers/", "First Vegas trip?", "Start with the easiest first-timer picks."),
        ("/guides/best-adult-shows/", "Want a more grown-up night?", "Compare Vegas adult shows before you choose."),
        ("/guides/best-cirque-shows/", "Want spectacle instead?", "Compare the current Cirque productions."),
    ],
    "guides/best-adult-shows/index.html": [
        ("/guides/best-shows-for-couples/", "Planning date night?", "See the broader couples shortlist."),
        ("/guides/best-cheap-vegas-shows/", "Need a lower price?", "Compare shows with cheaper starting tickets."),
        ("/guides/best-shows-for-first-timers/", "First Vegas trip?", "See the safest all-around first-timer picks."),
    ],
    "guides/best-tribute-shows/index.html": [
        ("/guides/best-cheap-vegas-shows/", "Want value first?", "Compare lower-cost shows across every category."),
        ("/guides/best-shows-for-couples/", "Building a date night?", "See shows that work well for couples."),
        ("/guides/best-shows-for-first-timers/", "New to Vegas?", "Start with the first-timer shortlist."),
    ],
    "guides/best-cheap-vegas-shows/index.html": [
        ("/guides/best-shows-for-families/", "Shopping for a family?", "Compare the kid-friendly options."),
        ("/guides/best-magic-shows/", "Want magic specifically?", "See every current magic option ranked."),
        ("/guides/best-shows-for-first-timers/", "First trip?", "See the easiest Vegas show picks."),
    ],
    "guides/best-magic-shows/index.html": [
        ("/guides/best-shows-for-families/", "Need family-friendly?", "See the best shows for mixed-age groups."),
        ("/guides/best-cheap-vegas-shows/", "Price matters?", "Compare the best lower-cost show options."),
        ("/guides/best-shows-for-first-timers/", "First time in Vegas?", "See the broader first-timer shortlist."),
    ],
    "guides/best-shows-for-families/index.html": [
        ("/guides/best-shows-for-first-timers/", "First family trip?", "See the broader first-timer picks."),
        ("/guides/best-cheap-vegas-shows/", "Keeping costs down?", "Compare strong shows with lower starting prices."),
        ("/guides/best-magic-shows/", "Kids want magic?", "Compare the current Vegas magic lineup."),
    ],
    "guides/best-cirque-shows/index.html": [
        ("/guides/best-shows-for-first-timers/", "First Vegas trip?", "See the broader first-timer shortlist."),
        ("/guides/best-shows-for-couples/", "Planning date night?", "Compare shows that work well for couples."),
        ("/guides/best-shows-for-families/", "Bringing kids?", "See the family-friendly shortlist."),
    ],
}

# Related comedy coverage gives the Matt Rife Dispatch article real contextual
# inbound support instead of relying only on the Dispatch index.
NEWS_LINKS = {
    "news/jo-koy-live-colosseum-caesars-palace-september-19/index.html": [
        ("/news/matt-rife-stay-golden-dolby-live-december-4/", "Matt Rife at Dolby Live", "Another major stand-up date coming to the Strip."),
        ("/shows/comedy/", "Compare Vegas comedy shows", "See the recurring comedy lineup."),
    ],
    "news/lewis-black-live-venetian-october-30/index.html": [
        ("/news/matt-rife-stay-golden-dolby-live-december-4/", "Matt Rife at Dolby Live", "Compare another major comedy date later this year."),
        ("/shows/comedy/", "Compare Vegas comedy shows", "See the recurring comedy lineup."),
    ],
}

# Show pages at The STRAT should link the actual property hub, not only the generic
# venue index. This also makes the venue page a stronger decision hub.
STRAT_SHOWS = [
    "shows/comedy/la-comedy-club/index.html",
    "shows/adult/rouge/index.html",
    "shows/music/ikons-of-rock/index.html",
]

CARD_RE = re.compile(r'<a class="related-card" href="[^"]+">.*?</a>', re.S)
GRID_RE = re.compile(r'(<div class="related-grid">)(.*?)(</div></div></section>)', re.S)


def read(rel):
    p = ROOT / rel
    if not p.exists():
        raise SystemExit(f"Missing expected page: {rel}")
    return p, p.read_text(encoding="utf-8")


def target_card(target_rel):
    _, text = read(target_rel)
    url = "/" + str(Path(target_rel).parent).replace("\\", "/") + "/"
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.S)
    name = re.sub(r'<[^>]+>', '', h1.group(1)).strip() if h1 else Path(target_rel).parent.name.replace('-', ' ').title()
    img = re.search(r'<div class="hero-media"><img src="([^"]+)"', text)
    if not img:
        img = re.search(r'<meta property="og:image" content="https://vegassidekick.com([^"]+)"', text)
    image = img.group(1) if img else "/images/brand/logo-badge.png"
    price = re.search(r'<div class="price"><small>Tickets from</small>\$([0-9]+(?:\.[0-9]+)?)</div>', text)
    if not price:
        price = re.search(r'"price"\s*:\s*"?([0-9]+(?:\.[0-9]+)?)"?', text)
    label = f"From ${price.group(1)}" if price else "See show guide"
    return url, html.escape(name), image, label


def apply_related(source_rel, target_rel):
    path, text = read(source_rel)
    target_url, name, image, label = target_card(target_rel)
    if target_url in text:
        return False
    m = GRID_RE.search(text)
    if not m:
        print(f"WARN no related grid: {source_rel}")
        return False
    cards = CARD_RE.findall(m.group(2))
    if len(cards) < 3:
        print(f"WARN fewer than 3 related cards: {source_rel}")
        return False
    card = (f'<a class="related-card" href="{target_url}"><img src="{image}" alt="{name}" loading="lazy">'
            f'<div><strong>{name}</strong><small>{label}</small></div></a>')
    new = m.group(1) + "".join(cards[:2] + [card]) + m.group(3)
    path.write_text(text[:m.start()] + new + text[m.end():], encoding="utf-8")
    return True


def link_rail(links, eyebrow="Keep comparing"):
    cards = "".join(
        f'<a href="{href}" style="display:block;padding:16px 18px;border:1px solid #ece9f6;border-radius:14px;text-decoration:none;color:inherit;background:#fff">'
        f'<strong style="display:block;margin-bottom:4px">{html.escape(title)} →</strong>'
        f'<span style="color:#6c6883;font-size:.92rem">{html.escape(desc)}</span></a>'
        for href, title, desc in links
    )
    return (
        '<section class="vs-internal-links" style="padding:34px 0;border-top:1px solid #ece9f6">'
        '<div class="wrap"><div style="font-size:.72rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:#7c3aed;margin-bottom:8px">'
        + html.escape(eyebrow) + '</div><h2 style="margin:0 0 16px">Make the next click useful</h2>'
        '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px">'
        + cards + '</div></div></section>')


def inject_before_footer(rel, links, eyebrow):
    path, text = read(rel)
    marker = '<div id="vs-footer"></div>'
    if marker not in text:
        print(f"WARN no footer marker: {rel}")
        return False
    # Idempotent: don't add a second rail.
    if 'class="vs-internal-links"' in text:
        return False
    text = text.replace(marker, link_rail(links, eyebrow) + "\n" + marker, 1)
    path.write_text(text, encoding="utf-8")
    return True


def apply_strat(rel):
    path, text = read(rel)
    if '/venues/the-strat/' in text:
        return False
    # Replace the generic venue destination in the canonical next-click module.
    old = 'href="/venues/"'
    if old not in text:
        print(f"WARN no generic venue link: {rel}")
        return False
    text = text.replace(old, 'href="/venues/the-strat/"', 1)
    path.write_text(text, encoding="utf-8")
    return True


def fix_known_broken_link():
    rel = "guides/best-cirque-shows/index.html"
    path, text = read(rel)
    old = "/news/cirque-closing-september-5/"
    new = "/news/mad-apple-closing-september-5/"
    if old not in text:
        return False
    path.write_text(text.replace(old, new), encoding="utf-8")
    return True


def main():
    changed = []
    for source, target in SHOW_RELATED.items():
        if apply_related(source, target):
            changed.append(source)
    for rel, links in GUIDE_LINKS.items():
        if inject_before_footer(rel, links, "Related Vegas guides"):
            changed.append(rel)
    for rel, links in NEWS_LINKS.items():
        if inject_before_footer(rel, links, "More Vegas comedy"):
            changed.append(rel)
    for rel in STRAT_SHOWS:
        if apply_strat(rel):
            changed.append(rel)
    if fix_known_broken_link():
        changed.append("guides/best-cirque-shows/index.html")

    print(f"Changed {len(set(changed))} page(s).")
    for rel in sorted(set(changed)):
        print(rel)


if __name__ == "__main__":
    main()
