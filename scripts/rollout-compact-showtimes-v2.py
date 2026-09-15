#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CATS = ['adult', 'cirque', 'comedy', 'family', 'magic', 'music', 'spectaculars']

PLAN_AHEAD = '<div class="vs-plan-ahead"><div aria-hidden="true" class="vs-calendar-icon">▦</div><div><strong>Planning ahead?</strong><p>You can book tickets weeks and months in advance.</p></div></div>'


def update_show_pages():
    changed = []
    regular = 0
    variable = 0
    custom = 0

    for cat in CATS:
        for p in sorted((ROOT / 'shows' / cat).glob('*/index.html')):
            s = p.read_text(encoding='utf-8', errors='replace')
            if 'vs-booking-section' not in s:
                continue
            old = s

            s = s.replace('showtimes-booking.css?v=1', 'showtimes-booking.css?v=2')
            s = s.replace('showtimes-booking.js?v=1', 'showtimes-booking.js?v=2')

            # Remove the Awakening-only experiment skin now that compact v2 is shared.
            s = re.sub(r'<style id="awakening-booking-experiment">.*?</style>', '', s, flags=re.S)
            s = s.replace('class="vs-awakening-closing-chip"', 'class="vs-booking-pill"')
            s = s.replace('class="vs-awakening-deadline"', 'class="vs-booking-note"')
            s = s.replace('class="vs-awakening-selected-day"', 'class="vs-selected-day-context"')

            # The compact system intentionally drops generic planning filler.
            s = s.replace(PLAN_AHEAD, '')

            # Keep the selected day available to assistive tech without repeating it visually.
            s = re.sub(
                r'<h3><span data-selected-day="">([^<]+)</span> showtimes</h3>',
                r'<h3>Choose a time <span class="vs-selected-day-context">for <span data-selected-day="">\1</span></span></h3>',
                s,
            )

            # The selected day is already obvious in the picker; keep the purchase CTA short.
            s = re.sub(
                r'(<a class="vs-primary-book vs-ticket-primary"[^>]*>)Get Tickets for [^<]+ →(</a>)',
                r'\1Get Tickets →\2',
                s,
            )
            s = s.replace('View all dates &amp; times →', 'See all dates &amp; times →')

            # Pills are static in the HTML for resilience; JS also supplies the same fallback
            # for future pages that omit one. Verified show-specific messaging may override it.
            if 'class="vs-booking-pill"' not in s:
                pill = 'CHECK YOUR DATE' if 'vs-variable-panel' in s else 'CHOOSE YOUR DAY'
                m = re.search(r'<div class="vs-booking-shell"[^>]*>', s)
                if not m:
                    raise RuntimeError(f'Booking shell not found in {p.relative_to(ROOT)}')
                s = s[:m.end()] + f'<div class="vs-booking-pill">{pill}</div>' + s[m.end():]

            if 'Final performances · Oct 10' in s:
                custom += 1
            elif 'vs-variable-panel' in s:
                variable += 1
            else:
                regular += 1

            if s != old:
                p.write_text(s, encoding='utf-8')
                changed.append(str(p.relative_to(ROOT)))

    return changed, regular, variable, custom


def update_docs():
    changed = []

    p = ROOT / 'AGENTS.md'
    s = p.read_text(encoding='utf-8')
    old = s
    reps = {
        '- Showtime buttons and the primary **Get Tickets for [day] →** CTA use the show’s existing verified affiliate URL.': '- Showtime buttons and the primary **Get Tickets →** CTA use the show’s existing verified affiliate URL.',
        '- Keep **View all dates & times →** as a visually substantial filled lavender secondary CTA.': '- Keep **See all dates & times →** as a compact secondary text action beneath the primary purchase path.',
        '- Include the compact **Planning ahead? You can book tickets weeks and months in advance.** treatment.': '- Put a compact booking pill above the headline. Default copy is **CHOOSE YOUR DAY** for regular schedules and **CHECK YOUR DATE** for variable schedules. Use show-specific factual copy only when it is verified, such as a closing date.',
        '- Keep the shared Vegas dusk / skyline / Sphere artwork as the decorative footer treatment without a slogan.': '- Keep the shared Vegas dusk / skyline / Sphere artwork as a thin decorative footer treatment without a slogan.',
    }
    for a, b in reps.items():
        if a not in s:
            raise RuntimeError(f'AGENTS.md expected text not found: {a}')
        s = s.replace(a, b)
    if s != old:
        p.write_text(s, encoding='utf-8')
        changed.append(str(p.relative_to(ROOT)))

    p = ROOT / 'SHOW-PAGE-BENCHMARK.md'
    s = p.read_text(encoding='utf-8')
    old = s
    reps = {
        '**Locked:** September 13, 2026': '**Locked:** September 15, 2026',
        '- **Pick your night** eyebrow': '- compact booking pill above the headline: **CHOOSE YOUR DAY** for regular schedules by default; verified show-specific facts may replace it',
        '- one dominant Warm Amber **Get Tickets for [day] →** CTA': '- one dominant Warm Amber **Get Tickets →** CTA; the selected day remains obvious in the picker and available in the accessible label',
        '- one substantial filled-lavender **View all dates & times →** secondary CTA': '- one compact **See all dates & times →** secondary text action',
        '- a compact **Planning ahead? You can book tickets weeks and months in advance.** card': '- no generic planning-ahead card; omit filler unless there is a genuinely useful show-specific fact',
        '- the shared decorative Vegas dusk / skyline / Sphere artwork at the bottom, with **no slogan**': '- the shared decorative Vegas dusk / skyline / Sphere artwork as a thin footer strip, with **no slogan**',
        '- retain the planning-ahead treatment and shared artwork': '- use the **CHECK YOUR DATE** pill and retain the thin shared artwork; do not add generic planning filler',
    }
    for a, b in reps.items():
        if a not in s:
            raise RuntimeError(f'SHOW-PAGE-BENCHMARK.md expected text not found: {a}')
        s = s.replace(a, b)
    if s != old:
        p.write_text(s, encoding='utf-8')
        changed.append(str(p.relative_to(ROOT)))

    p = ROOT / 'SHOW-BUILDER-PROMPT.md'
    s = p.read_text(encoding='utf-8')
    old = s
    anchor = '> Key current rules: no formal downside/Think twice modules; Good to know only for real useful facts; Booking tip is optional and actionable only; no customer-facing “tradeoff”; no interaction/participation claims unless Kris explicitly confirms them; use Start time/Start times; prefer “See available dates & times”; use one visible “Show info confirmed Month YYYY” freshness line near the author card; galleries support arrows/keyboard/swipe; seating charts are room-based, geometrically faithful, slab-row when exact seat counts are unnecessary, and mobile tap feedback must appear immediately in view.'
    note = '\n>\n> **Booking module update — September 15, 2026:** compact v2 is the shared standard. Use the pill + compact day/time/amber CTA treatment in `assets/showtimes-booking.css` and `.js`; do not restore the old large secondary CTA or generic Planning Ahead card.'
    if note.strip() not in s:
        if anchor not in s:
            raise RuntimeError('SHOW-BUILDER-PROMPT.md booking update anchor not found')
        s = s.replace(anchor, anchor + note)
    if s != old:
        p.write_text(s, encoding='utf-8')
        changed.append(str(p.relative_to(ROOT)))

    return changed


def main():
    pages, regular, variable, custom = update_show_pages()
    docs = update_docs()
    print(f'Booking pages changed: {len(pages)}')
    print(f'Booking modules found: regular={regular}, variable={variable}, custom={custom}')
    print(f'Docs changed: {len(docs)}')
    for path in pages + docs:
        print(path)


if __name__ == '__main__':
    main()
