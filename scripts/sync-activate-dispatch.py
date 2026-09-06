from pathlib import Path

for name in ['news/index.html','index.html']:
    p=Path(name); s=p.read_text(encoding='utf-8')
    s=s.replace('55+ games across 15 arenas', '14 game rooms with dozens of active-game combinations')
    s=s.replace('55+ games spread across 15 arenas', '14 game rooms with dozens of active-game combinations')
    p.write_text(s,encoding='utf-8')

p=Path('sitemap.xml'); s=p.read_text(encoding='utf-8')
needle='<loc>https://vegassidekick.com/news/activate-town-square-opens-october-3/</loc>'
pos=s.find(needle)
if pos>=0:
    end=s.find('</url>',pos)
    block=s[pos:end]
    import re
    new=re.sub(r'<lastmod>[^<]+</lastmod>','<lastmod>2026-09-05</lastmod>',block)
    s=s[:pos]+new+s[end:]
p.write_text(s,encoding='utf-8')
print('synced')