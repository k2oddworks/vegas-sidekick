#!/usr/bin/env python3
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]

EXACT = {
    "news/matt-rife-stay-golden-dolby-live-december-4/index.html": [
        ("Record-breaking comedian Matt Rife adds a Las Vegas date to his Stay Golden World Tour. Dolby Live at Park MGM, Friday December 4, 2026 at 8 p.m. Citi presale starts May 12. General on sale May 15.",
         "Matt Rife brings the Stay Golden World Tour to Dolby Live on December 4, 2026. See the Las Vegas date, venue details and what to know before buying."),
        ("Concert announcements, presale reminders, and deals — before they sell out.",
         "Concert announcements, show updates and useful Vegas ticketing context."),
    ],
    "news/best-vegas-shows-for-first-timers/index.html": [
        ("Cirque Mystère fills fast on weekends. VEGAS! The Show and V have better walk-up availability, but prime seats sell out. Mid-week is the easiest window.",
         "Weekend and prime-seat availability can be tighter. Mid-week is usually the easiest window if your dates are flexible."),
        ("Book at Least a Few Days Out", "Check Your Date Before You Go"),
    ],
    "guides/best-cheap-vegas-shows/index.html": [
        ("The Strip's longest-running topless revue — 25+ years and still selling out. Slick production, live vocals, and a wallet-friendly way to do a grown-up night out. 18+.",
         "The Strip's longest-running topless revue — 25+ years and still running. Slick production, live vocals, and a wallet-friendly way to do a grown-up night out. 18+."),
    ],
    "news/bini-signals-world-tour-august-8/index.html": [
        ("selling fast", "on the schedule"),
        ("Selling fast", "On the schedule"),
    ],
    "shows/cirque/index.html": [
        ("five of its shows still run here simultaneously", "four of its shows still run here simultaneously"),
    ],
    "affiliate-disclosure/index.html": [
        ("Last updated: April 2026", "Last updated: September 2026"),
    ],
    "about/index.html": [
        ("Handpicked Las Vegas show tickets at real discounts — no membership, no hidden fees, no markup games.",
         "Independent Las Vegas show recommendations, ticket links and practical booking guidance from a local ticketing perspective."),
    ],
    "terms/index.html": [
        ("Prices listed reflect our affiliate partner's current pricing at the time of publishing and are subject to change. The urgency language on this Site (\"prices may increase closer to show date\") reflects typical ticketing market behavior and is not a guarantee of price movement.",
         "Prices listed reflect available pricing at the time of publishing and are subject to change. Vegas Sidekick does not guarantee future price movement or use unsupported scarcity claims as a substitute for current ticket information."),
    ],
}

CATEGORY_META = {
    "shows/magic/index.html": "Browse Las Vegas magic shows including Penn & Teller, Shin Lim, Criss Angel and more. Compare current prices, show styles, schedules and practical booking details.",
    "shows/comedy/index.html": "Browse Las Vegas comedy shows including Carrot Top, Tape Face, Comedy Cellar and more. Compare current prices, schedules and what kind of comedy night each show delivers.",
    "shows/music/index.html": "Browse Las Vegas music and variety shows including VEGAS! The Show, Blue Man Group and more. Compare current prices, schedules and show styles before choosing.",
    "shows/family/index.html": "Browse family-friendly Las Vegas shows including Tournament of Kings and more. Compare current prices, age fit, schedules and practical details for your group.",
    "shows/spectaculars/index.html": "Browse large-scale Las Vegas productions including The Wizard of Oz at Sphere and Awakening. Compare current prices, schedules and what each spectacle is actually like.",
}

GENERIC_FILES = [
    "about/index.html", "shows/index.html", "shows/adult/index.html", "shows/cirque/index.html",
    "shows/comedy/index.html", "shows/family/index.html", "shows/magic/index.html", "shows/music/index.html", "shows/spectaculars/index.html",
    "guides/best-adult-shows/index.html", "guides/best-cheap-vegas-shows/index.html",
    "guides/best-cirque-shows/index.html", "guides/best-magic-shows/index.html",
    "guides/best-shows-for-families/index.html", "guides/best-tribute-shows/index.html",
]


def set_meta(text, desc):
    encoded=desc.replace('&','&amp;').replace('"','&quot;')
    p=r'<meta\s+name=["\']description["\']\s+content=["\'].*?["\']\s*/?>'
    return re.sub(p, f'<meta name="description" content="{encoded}">', text, count=1, flags=re.I|re.S)


def main():
    changed=[]
    for rel,rules in EXACT.items():
        p=ROOT/rel
        if not p.exists(): continue
        text=p.read_text(encoding='utf-8'); new=text
        for old,repl in rules: new=new.replace(old,repl)
        if rel.endswith('matt-rife-stay-golden-dolby-live-december-4/index.html'):
            new=re.sub(r'[^"\']*presale starts May 12\. General on sale May 15\.', 'Matt Rife brings the Stay Golden World Tour to Dolby Live on December 4, 2026. See the Las Vegas date, venue details and what to know before buying.', new, flags=re.I)
        if new!=text:
            p.write_text(new,encoding='utf-8'); changed.append(rel)
    for rel,desc in CATEGORY_META.items():
        p=ROOT/rel
        if not p.exists(): continue
        text=p.read_text(encoding='utf-8'); new=set_meta(text,desc)
        if new!=text:
            p.write_text(new,encoding='utf-8'); changed.append(rel)
    for rel in GENERIC_FILES:
        p=ROOT/rel
        if not p.exists(): continue
        text=p.read_text(encoding='utf-8'); new=text
        new=re.sub(r'\bzero hidden fees\b', 'clear ticket details', new, flags=re.I)
        new=re.sub(r'\bno hidden fees\b', 'clear ticket details', new, flags=re.I)
        new=re.sub(r'\binstant delivery\b', 'current show details', new, flags=re.I)
        if new!=text:
            p.write_text(new,encoding='utf-8'); changed.append(rel)
    print('Changed files:', len(set(changed)))
    for rel in sorted(set(changed)): print('-',rel)

if __name__=='__main__': main()
