#!/usr/bin/env python3
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
GENERIC={
'You need an all-ages option or a quieter, low-key night.',
'You want a comedy club, concert or personality-led headliner to be the whole point.',
'You want a big visual production, concert or Cirque-style experience instead.',
'Your group is specifically looking for an adults-only nightlife show.',
'You want a concert, comedy club or large-scale production instead.',
'You want magic, stand-up or a spectacle-first production instead.',
'You want an intimate, personality-led show where one performer is the main attraction.',
'You are really shopping for magic, Cirque or a concert.',
'You are really looking for a concert or Cirque production.',
'You are really shopping for close-up magic or stand-up comedy.',
'You need an all-ages show.',
}
closed={'shows/cirque/mad-apple/index.html','shows/magic/david-goldrake/index.html'}
removed=[]
pat=re.compile(r'<div class="decision-card(?: watch| maybe)?"><h3>(?:🤔 )?Think twice(?: if…)?</h3><p>(.*?)</p></div>',re.S|re.I)
for p in sorted(ROOT.glob('shows/*/*/index.html')):
    rel=p.relative_to(ROOT).as_posix()
    if rel in closed: continue
    text=p.read_text(encoding='utf-8')
    def repl(m):
        body=re.sub(r'<[^>]+>','',m.group(1)).strip()
        if body in GENERIC:
            removed.append((rel,body)); return ''
        return m.group(0)
    new=pat.sub(repl,text)
    if new!=text: p.write_text(new,encoding='utf-8')

# Update living guidance: Think twice is optional, never filler.
for rel in ['SHOW-BUILDER-PROMPT.md','VS_CHAT_CONTEXT.md']:
    p=ROOT/rel
    text=p.read_text(encoding='utf-8')
    text=text.replace('Use **Good fit**, **Think twice**, and **Booking tip** for the three-card buyer decision aid. The copy must be useful on its own and specific to the show when possible.',
                      'Use **Good fit** and **Booking tip** as the core buyer decision aid. **Think twice** is optional and should appear only when there is a real, show-specific downside, mismatch, or tradeoff. Never add it just to fill a third card.')
    text=text.replace('- **Think twice** — one honest mismatch, tradeoff, or reason to choose another category.',
                      '- **Think twice** — optional; include only for a real, show-specific mismatch, downside, or tradeoff. Omit it rather than use category filler.')
    p.write_text(text,encoding='utf-8')

# Update canonical generator so generic profile Think-twice copy is not emitted by default.
p=ROOT/'scripts/canonicalize-show-pages.py'
text=p.read_text(encoding='utf-8')
old='<div class="decision-card"><h3>Think twice</h3><p>{htmllib.escape(ctx[\'think\'][0])}</p></div>'
text=text.replace(old,'')
p.write_text(text,encoding='utf-8')

print(f'Removed {len(removed)} generic Think twice cards')
for rel,body in removed: print(rel, '::', body)
