#!/usr/bin/env python3
from pathlib import Path
import html, re, sys

ROOT=Path(__file__).resolve().parents[1]
CLOSED={'shows/cirque/mad-apple/index.html','shows/magic/david-goldrake/index.html'}

CATEGORY_THINK={
'adult':'You need an all-ages option or a quieter, low-key night.',
'cirque':'You want a comedy club, concert or personality-led headliner to be the whole point.',
'comedy':'You want a big visual production, concert or Cirque-style experience instead.',
'family':'Your group is specifically looking for an adults-only nightlife show.',
'magic':'You want a concert, comedy club or large-scale production instead.',
'music':'You want magic, stand-up or a spectacle-first production instead.',
'spectaculars':'You want an intimate, personality-led show where one performer is the main attraction.',
}
OVERRIDES={
'shows/spectaculars/absinthe/index.html':(
    'You want a raunchy, close-up mix of circus, comedy and audience interaction.',
    'You want a polished family-friendly production or a low-interaction night.'),
'shows/spectaculars/america-the-show/index.html':(
    'You want an old-school Vegas-style production built around American music and showmanship.',
    'You want a magic, comedy or concert-first night instead.'),
'shows/spectaculars/awakening/index.html':(
    'You want a large-scale production where visuals, choreography and effects are a big part of the draw.',
    'You want an intimate, personality-led headliner or a simple concert setup.'),
'shows/spectaculars/wizard-of-oz/index.html':(
    'You want the Sphere itself to be part of the attraction and you like immersive, effects-heavy spectacle.',
    'You want a conventional theater production or a low-sensory show.'),
'shows/spectaculars/wow-the-vegas-spectacular/index.html':(
    'You want a variety-style spectacle with acrobatics and big visual moments.',
    'You want a stripped-down, personality-led show instead of a production showcase.'),
}
BAD_THINK=(
    'you actually want a magic show',
    'a different show category is the real priority',
    'you would rather spend the night with one comedian, magician or singer as the clear focus',
)

def clean(s):
    return re.sub(r'<[^>]+>','',html.unescape(s)).strip()

def first_fit_item(text, kind):
    m=re.search(rf'<div class="fit-card {kind}".*?</div>',text,re.S|re.I)
    if not m:return ''
    li=re.search(r'<li>(.*?)</li>',m.group(0),re.S|re.I)
    return clean(li.group(1)) if li else ''

def selected_seat(text):
    for pat in [
        r'<button class="seat-zone[^"]*active[^"]*"[^>]*data-copy="([^"]+)"[^>]*data-title="([^"]+)"',
        r'<button class="seat-zone[^"]*center[^"]*"[^>]*data-copy="([^"]+)"[^>]*data-title="([^"]+)"',
    ]:
        m=re.search(pat,text,re.S|re.I)
        if m:return clean(m.group(2)),clean(m.group(1))
    return ('','')

def rewrite(path):
    rel=path.relative_to(ROOT).as_posix()
    if rel in CLOSED:return None
    text=path.read_text(encoding='utf-8')
    # Only replace the legacy three-card template. Leave custom Good fit / Think twice modules alone.
    legacy=re.compile(
        r'<div class="decision">\s*'
        r'<div class="decision-card(?: good)?"><h3>Book it if…?</h3><p>(.*?)</p></div>\s*'
        r'<div class="decision-card(?: watch)?"><h3>Know this first</h3><p>(.*?)</p></div>\s*'
        r'<div class="decision-card"><h3>Best practical angle</h3><p>(.*?)</p></div>\s*'
        r'</div>',re.S|re.I)
    m=legacy.search(text)
    if not m:return None
    old_good,old_know,old_tip=map(clean,m.groups())
    cat=rel.split('/')[1]
    fit_good=first_fit_item(text,'good')
    fit_think=first_fit_item(text,'twice')

    if rel in OVERRIDES:
        good,think=OVERRIDES[rel]
    else:
        good=fit_good or old_good
        low=fit_think.lower()
        bad=(not fit_think or any(x in low for x in BAD_THINK) or ('magic show' in low and cat!='magic'))
        think=CATEGORY_THINK.get(cat,'You are really shopping for a different kind of Vegas night.') if bad else fit_think

    # Keep genuinely useful existing planning advice. If the legacy line is vague seat language,
    # make the selected seat explicit so the card is actionable on its own.
    tip=old_tip
    vague=('safest choice for reading the production as a whole' in tip.lower() or
           'chasing the closest possible row' in tip.lower())
    if vague:
        seat,copy=selected_seat(text)
        if seat:
            tip=f'Start with {seat}. {copy}'
    if not tip:
        seat,copy=selected_seat(text)
        tip=f'Start with {seat}. {copy}' if seat else 'Check the exact showtime and available seat map for your date before you book.'

    new=(f'<div class="decision">'
         f'<div class="decision-card good"><h3>Good fit</h3><p>{html.escape(good,quote=False)}</p></div>'
         f'<div class="decision-card watch"><h3>Think twice</h3><p>{html.escape(think,quote=False)}</p></div>'
         f'<div class="decision-card"><h3>Booking tip</h3><p>{html.escape(tip,quote=False)}</p></div>'
         f'</div>')
    text=text[:m.start()]+new+text[m.end():]
    path.write_text(text,encoding='utf-8')
    return rel,good,think,tip

rows=[]
for path in sorted(ROOT.glob('shows/*/*/index.html')):
    r=rewrite(path)
    if r:rows.append(r)
print(f'Replaced {len(rows)} legacy decision blocks')
for rel,good,think,tip in rows:
    print(f'[{rel}]\n  GOOD: {good}\n  THINK: {think}\n  TIP: {tip}')
if not rows:sys.exit('No legacy decision blocks found')
