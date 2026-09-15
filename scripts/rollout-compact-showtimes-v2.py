#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CATS = ['adult', 'cirque', 'comedy', 'family', 'magic', 'music', 'spectaculars']

PLAN_AHEAD = '<div class="vs-plan-ahead"><div aria-hidden="true" class="vs-calendar-icon">▦</div><div><strong>Planning ahead?</strong><p>You can book tickets weeks and months in advance.</p></div></div>'
BOOKING_ART = '<div aria-hidden="true" class="vs-booking-art"><div class="vs-art-moon"></div><div class="vs-art-sphere"></div><div class="vs-art-strip"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div></div>'


def ensure_barry_booking_module():
    """Bring the one remaining active legacy product page into the shared module."""
    p = ROOT / 'shows/music/barry-manilow/index.html'
    s = p.read_text(encoding='utf-8', errors='replace')
    if 'vs-booking-section' in s:
        return False

    css_anchor = '<link rel="stylesheet" href="/assets/ticket-cta.css">'
    if css_anchor not in s:
        raise RuntimeError('Barry Manilow ticket CTA stylesheet anchor not found')
    s = s.replace(css_anchor, css_anchor + '<link rel="stylesheet" href="/assets/showtimes-booking.css?v=2">', 1)

    nav_anchor = '<a href="#quick">Quick take</a>'
    if nav_anchor not in s:
        raise RuntimeError('Barry Manilow nav anchor not found')
    s = s.replace(nav_anchor, nav_anchor + '<a href="#showtimes">Showtimes</a>', 1)

    ticket = 'https://spotlight.vegas/shows/music/barry-manilow/ref/vegassidekick'
    module = (
        '<section class="section vs-booking-section" id="showtimes"><div class="wrap">'
        '<div class="vs-booking-shell"><div class="vs-booking-pill">CHECK YOUR DATE</div>'
        '<div class="vs-booking-copy"><h2>See available dates &amp; times</h2>'
        '<p class="vs-booking-summary"><strong>Schedule varies by date</strong>'
        '<span>Use the live calendar to choose your performance.</span></p></div>'
        '<div class="vs-time-panel vs-variable-panel">'
        f'<a class="vs-primary-book vs-ticket-primary" href="{ticket}" rel="noopener sponsored" target="_blank">See available dates &amp; times →</a>'
        '</div>' + BOOKING_ART + '</div></div></section>'
    )

    quick_start = s.find('<section class="section" id="quick">')
    if quick_start < 0:
        raise RuntimeError('Barry Manilow quick section not found')
    quick_end = s.find('</section>', quick_start)
    if quick_end < 0:
        raise RuntimeError('Barry Manilow quick section end not found')
    quick_end += len('</section>')
    s = s[:quick_end] + module + s[quick_end:]

    if 'showtimes-booking.js?v=2' not in s:
        s = s.replace('</body>', '<script src="/assets/showtimes-booking.js?v=2"></script></body>', 1)

    p.write_text(s, encoding='utf-8')
    return True


def update_show_pages():
    changed = []
    regular = 0
    variable = 0
    custom = 0

    if ensure_barry_booking_module():
        changed.append('shows/music/barry-manilow/index.html')

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
                rel = str(p.relative_to(ROOT))
                if rel not in changed:
                    changed.append(rel)

    return changed, regular, variable, custom


def apply_replacements(text, replacements, label):
    for old, new in replacements.items():
        if old in text:
            text = text.replace(old, new)
        elif new not in text:
            raise RuntimeError(f'{label} expected text not found: {old}')
    return text


def update_docs():
    changed = []

    p = ROOT / 'AGENTS.md'
    s = p.read_text(encoding='utf-8')
    old = s
    s = apply_replacements(s, {
        '- Showtime buttons and the primary **Get Tickets for [day] →** CTA use the show’s existing verified affiliate URL.': '- Showtime buttons and the primary **Get Tickets →** CTA use the show’s existing verified affiliate URL.',
        '- Keep **View all dates & times →** as a visually substantial filled lavender secondary CTA.': '- Keep **See all dates & times →** as a compact secondary text action beneath the primary purchase path.',
        '- Include the compact **Planning ahead? You can book tickets weeks and months in advance.** treatment.': '- Put a compact booking pill above the headline. Default copy is **CHOOSE YOUR DAY** for regular schedules and **CHECK YOUR DATE** for variable schedules. Use show-specific factual copy only when it is verified, such as a closing date.',
        '- Keep the shared Vegas dusk / skyline / Sphere artwork as the decorative footer treatment without a slogan.': '- Keep the shared Vegas dusk / skyline / Sphere artwork as a thin decorative footer treatment without a slogan.',
    }, 'AGENTS.md')
    if s != old:
        p.write_text(s, encoding='utf-8')
        changed.append(str(p.relative_to(ROOT)))

    p = ROOT / 'SHOW-PAGE-BENCHMARK.md'
    s = p.read_text(encoding='utf-8')
    old = s
    s = apply_replacements(s, {
        '**Locked:** September 13, 2026': '**Locked:** September 15, 2026',
        '- **Pick your night** eyebrow': '- compact booking pill above the headline: **CHOOSE YOUR DAY** for regular schedules by default; verified show-specific facts may replace it',
        '- one dominant Warm Amber **Get Tickets for [day] →** CTA': '- one dominant Warm Amber **Get Tickets →** CTA; the selected day remains obvious in the picker and available in the accessible label',
        '- one substantial filled-lavender **View all dates & times →** secondary CTA': '- one compact **See all dates & times →** secondary text action',
        '- a compact **Planning ahead? You can book tickets weeks and months in advance.** card': '- no generic planning-ahead card; omit filler unless there is a genuinely useful show-specific fact',
        '- the shared decorative Vegas dusk / skyline / Sphere artwork at the bottom, with **no slogan**': '- the shared decorative Vegas dusk / skyline / Sphere artwork as a thin footer strip, with **no slogan**',
        '- retain the planning-ahead treatment and shared artwork': '- use the **CHECK YOUR DATE** pill and retain the thin shared artwork; do not add generic planning filler',
    }, 'SHOW-PAGE-BENCHMARK.md')
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
