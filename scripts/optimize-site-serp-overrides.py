#!/usr/bin/env python3
"""Apply hand-curated title/meta improvements to high-value non-show pages flagged by the SERP audit."""
from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parents[1]

OVERRIDES = {
    "news/index.html": (
        "Vegas Show News & Concert Updates | Vegas Dispatch",
        "Las Vegas show news, concert announcements, closures and ticketing context from Vegas Sidekick. Follow what changed, what’s coming and what matters.",
    ),
    "news/matt-rife-stay-golden-dolby-live-december-4/index.html": (
        "Matt Rife Las Vegas Dec. 4, 2026 | Dolby Live",
        "Matt Rife brings the Stay Golden World Tour to Dolby Live on December 4, 2026. See the Las Vegas date, venue details and what to know before buying.",
    ),
    "news/donny-osmond-extends-harrahs-residency-through-2027/index.html": (
        "Donny Osmond Vegas Residency Extended Through June 2027",
        "Donny Osmond’s Harrah’s Las Vegas residency now runs through June 2027. See the extension, venue details and what it means for future Vegas dates.",
    ),
    "news/best-vegas-shows-for-first-timers/index.html": (
        "3 Vegas Shows for First-Timers | Dispatch Picks",
        "Three easy starting points for a first Las Vegas show: what each one does well, who it fits and where to go next if you want more options.",
    ),
    "news/new-shows-announced-may-14-2026/index.html": (
        "Vegas Show Announcements: May 14, 2026 Archive",
        "Archive of Las Vegas show announcements from the week of May 14, 2026, kept for reference with the original reporting and event context.",
    ),
    "news/bini-signals-world-tour-august-8/index.html": (
        "BINI Las Vegas Aug. 8, 2026 | Signals Tour Archive",
        "Archive of BINI’s Signals World Tour Las Vegas date on August 8, 2026, with the original venue and event reporting preserved for reference.",
    ),
    "news/live-nation-las-vegas-listings-update-may-2026/index.html": (
        "Las Vegas Concert Announcements: May 7, 2026 Archive",
        "Archive of the May 7, 2026 Las Vegas concert announcement wave, preserving the original artist, venue and event details for reference.",
    ),
    "news/smashing-pumpkins-rats-in-a-cage-tour-mgm-grand-october-30/index.html": (
        "Smashing Pumpkins Las Vegas Oct. 30 | MGM Grand",
        "Smashing Pumpkins bring the Rats in a Cage Tour to MGM Grand on October 30. See the Las Vegas date, venue details and event context.",
    ),
    "news/blue-dot-fever-what-it-means-for-vegas/index.html": (
        "Blue Dot Fever: What Vegas Seat Maps Really Tell You",
        "What do empty blue dots on a Vegas seat map actually mean? A practical look at inventory, demand signals and what seat maps can—and can’t—tell you.",
    ),
    "news/jay-silent-bob-save-vegas-october-16/index.html": (
        "Jay & Silent Bob Las Vegas Oct. 16 | Palazzo Theatre",
        "Jay & Silent Bob Save Vegas comes to The Palazzo Theatre on October 16. See the event details, venue and what to know about the Las Vegas date.",
    ),
    "venues/alexis-park/index.html": (
        "Alexis Park Las Vegas Shows 2026 | 9 Shows & Prices",
        None,
    ),
    "venues/linq-flamingo-harrahs/index.html": (
        "LINQ, Flamingo & Harrah’s Shows 2026 | Vegas Guide",
        None,
    ),
    "venues/planet-hollywood/index.html": (
        "Planet Hollywood Las Vegas Shows 2026 | Tickets & Prices",
        None,
    ),
    "venues/excalibur-luxor-mandalay-bay/index.html": (
        "Excalibur, Luxor & Mandalay Bay Shows 2026 | Vegas Guide",
        None,
    ),
    "venues/the-strat/index.html": (
        "The STRAT Las Vegas Shows 2026 | 3 Shows & Prices",
        None,
    ),
    "venues/horseshoe/index.html": (
        "Horseshoe Las Vegas Shows 2026 | 3 Shows & Prices",
        None,
    ),
    "venues/mgm-grand/index.html": (
        "MGM Grand & New York-New York Shows 2026 | Vegas Guide",
        None,
    ),
    "guides/best-cirque-shows/index.html": (
        "Best Cirque du Soleil Shows in Vegas 2026 | Ranked",
        "All four current Cirque du Soleil shows in Las Vegas ranked by experience, spectacle and fit, with prices and practical tradeoffs for choosing one.",
    ),
    "guides/best-magic-shows/index.html": (
        "Best Magic Shows in Las Vegas 2026 | 11 Ranked",
        "Eleven current Las Vegas magic shows ranked by style, price and who they fit best, from close-up magic and mentalism to large-scale illusion.",
    ),
    "guides/best-shows-for-first-timers/index.html": (
        "Best Vegas Shows for First-Timers 2026 | 12 Picks",
        "Twelve Las Vegas shows that work especially well for first-time visitors, with prices, honest tradeoffs and quick guidance on who each show fits.",
    ),
    "guides/best-shows-for-families/index.html": (
        "Best Family Shows in Las Vegas 2026 | 12 Picks",
        "Twelve family-friendly Las Vegas shows compared by age fit, style and price, with practical guidance for choosing a show that works for your group.",
    ),
    "guides/best-tribute-shows/index.html": (
        None,
        "Fourteen Las Vegas tribute shows ranked by music, production style and value, with current starting prices and practical notes on who each show fits.",
    ),
    "guides/best-shows-for-couples/index.html": (
        None,
        "Ten Las Vegas date-night shows compared by vibe, price and experience, with honest tradeoffs for couples choosing what kind of night they actually want.",
    ),
    "shows/cirque/mad-apple/index.html": (
        "Mad Apple Las Vegas Closed Sept. 5, 2026 | Archive",
        "Mad Apple at New York-New York closed September 5, 2026. This page remains as an archive; compare current Las Vegas Cirque and adult show options.",
    ),
    "about/kris-kidd/index.html": (
        "Kris Kidd | Las Vegas Entertainment & Ticketing Expert",
        None,
    ),
    "vegas-sign/index.html": (
        "Welcome to Las Vegas Sign | 3D Interactive Experience",
        "Explore a 3D interactive version of the Welcome to Fabulous Las Vegas sign, with day, sunset and night views built by Vegas Sidekick.",
    ),
}


def replace(text: str, title, desc):
    if title:
        text = re.sub(r'<title[^>]*>.*?</title>', f'<title>{html.escape(title)}</title>', text, count=1, flags=re.I | re.S)
    if desc:
        encoded = html.escape(desc, quote=True)
        p1 = r'<meta\s+name=["\']description["\']\s+content=["\'].*?["\']\s*/?>'
        p2 = r'<meta\s+content=["\'].*?["\']\s+name=["\']description["\']\s*/?>'
        if re.search(p1, text, re.I | re.S):
            text = re.sub(p1, f'<meta name="description" content="{encoded}">', text, count=1, flags=re.I | re.S)
        elif re.search(p2, text, re.I | re.S):
            text = re.sub(p2, f'<meta name="description" content="{encoded}">', text, count=1, flags=re.I | re.S)
    return text


def main():
    changed = 0
    for rel, (title, desc) in OVERRIDES.items():
        path = ROOT / rel
        if not path.exists():
            print(f"SKIP missing: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        updated = replace(text, title, desc)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(rel)
    print(f"Updated {changed} hand-curated page(s).")


if __name__ == "__main__":
    main()
