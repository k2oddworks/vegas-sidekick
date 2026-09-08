#!/usr/bin/env python3
import glob,re,sys
from pathlib import Path
CLOSED={'shows/cirque/mad-apple/index.html','shows/magic/david-goldrake/index.html'}
DIV=re.compile(r'<div class="hero-media"[^>]*data-mobile-fit="([^"]+)"[^>]*style="([^"]*)"[^>]*>')
IMG=re.compile(r'<img\b[^>]*\bsrc="([^"]+)"')
allowed={'safe','cover','contain'}; issues=0; checked=0; modes={}
for f in sorted(glob.glob('shows/*/*/index.html')):
    if f in CLOSED: continue
    checked+=1; text=Path(f).read_text(); dm=DIV.search(text)
    if not dm: print(f'{f}: missing structured mobile hero treatment'); issues+=1; continue
    im=IMG.search(text,dm.end(),min(len(text),dm.end()+1200))
    if not im: print(f'{f}: hero image not found'); issues+=1; continue
    mode,style=dm.groups(); src=im.group(1); modes[mode]=modes.get(mode,0)+1
    if mode not in allowed: print(f'{f}: invalid mode {mode}'); issues+=1
    if '--mobile-hero-position:' not in style: print(f'{f}: missing focal position'); issues+=1
    if mode=='safe' and '--mobile-hero-image:' not in style: print(f'{f}: safe mode missing background image'); issues+=1
    if not src.startswith('/images/'): print(f'{f}: unexpected hero src {src}'); issues+=1
print(f'Checked {checked} active show mobile heroes. Modes: {modes}')
if issues: print(f'{issues} mobile hero issue(s) found.'); sys.exit(1)
print('All active show mobile heroes have an explicit safe treatment.')
