from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
# High-value public index surfaces with incomplete share identity.
targets={
'guides/index.html':'https://vegassidekick.com/images/guides/guide-first-timers-cover.jpg',
'shows/magic/index.html':'https://vegassidekick.com/images/guides/guide-magic-cover.jpg',
'shows/cirque/index.html':'https://vegassidekick.com/images/guides/guide-cirque-cover.jpg',
'shows/comedy/index.html':'https://vegassidekick.com/images/site/home-og.jpg',
'shows/music/index.html':'https://vegassidekick.com/images/site/home-og.jpg',
'shows/family/index.html':'https://vegassidekick.com/images/guides/guide-families-cover.jpg',
'shows/spectaculars/index.html':'https://vegassidekick.com/images/site/home-og.jpg',
}
for rel,img in targets.items():
 p=ROOT/rel
 if not p.exists(): continue
 s=p.read_text()
 title=re.search(r'<title>(.*?)</title>',s,re.S)
 desc=re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']\s*/?>',s,re.S|re.I)
 canon=re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']',s,re.I)
 if not (title and desc and canon): continue
 t=re.sub(r'\s+',' ',title.group(1)).strip(); d=re.sub(r'\s+',' ',desc.group(1)).strip(); u=canon.group(1)
 additions=[]
 if 'rel="icon"' not in s and "rel='icon'" not in s: additions.append('<link rel="icon" href="/favicon.png" type="image/png">')
 if 'property="og:site_name"' not in s: additions.append('<meta property="og:site_name" content="Vegas Sidekick">')
 if 'property="og:type"' not in s: additions.append('<meta property="og:type" content="website">')
 if 'property="og:title"' not in s: additions.append(f'<meta property="og:title" content="{t}">')
 if 'property="og:description"' not in s: additions.append(f'<meta property="og:description" content="{d}">')
 if 'property="og:url"' not in s: additions.append(f'<meta property="og:url" content="{u}">')
 if 'property="og:image"' not in s: additions.append(f'<meta property="og:image" content="{img}">')
 if 'name="twitter:card"' not in s: additions.append('<meta name="twitter:card" content="summary_large_image">')
 if 'name="twitter:title"' not in s: additions.append(f'<meta name="twitter:title" content="{t}">')
 if 'name="twitter:description"' not in s: additions.append(f'<meta name="twitter:description" content="{d}">')
 if 'name="twitter:image"' not in s: additions.append(f'<meta name="twitter:image" content="{img}">')
 if additions: s=s.replace('</head>','\n'+'\n'.join(additions)+'\n</head>',1)
 p.write_text(s)
