#!/usr/bin/env python3
from pathlib import Path
import re,sys
root=Path(__file__).resolve().parents[1]
problems=[];count=0
for p in root.glob('shows/*/*/index.html'):
    t=p.read_text(encoding='utf-8',errors='ignore')
    for m in re.finditer(r'<div class="vs-video"[^>]*data-youtube-id="([^"]+)"[^>]*>(.*?)</div>',t,re.S):
        count+=1;vid,body=m.groups()
        if not re.fullmatch(r'[A-Za-z0-9_-]{6,20}',vid): problems.append(f'{p.relative_to(root)}: invalid YouTube video ID')
        if not re.search(r'<img[^>]+alt="[^"]+"',body): problems.append(f'{p.relative_to(root)}: trailer thumbnail missing alt text')
        if not re.search(r'<button[^>]+aria-label="[^"]+"',body): problems.append(f'{p.relative_to(root)}: trailer play button missing aria-label')
if problems:
    print('Show video audit FAILED:');[print(' - '+x) for x in problems];sys.exit(1)
print(f'Show video audit passed. Shared video components checked: {count}')
