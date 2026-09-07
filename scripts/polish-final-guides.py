from pathlib import Path
import re

slugs=['best-adult-shows','best-cheap-vegas-shows','best-cirque-shows','best-magic-shows','best-shows-for-couples','best-shows-for-families','best-shows-for-first-timers','best-tribute-shows']
for slug in slugs:
    p=Path('guides')/slug/'index.html'
    s=p.read_text(encoding='utf-8')
    s=re.sub(r'"dateModified":\s*"[^"]+"','"dateModified": "2026-09-06"',s)
    s=re.sub(r'Updated <b>(?:Jul|Aug|Sep) 2026</b>','Updated <b>Sep 2026</b>',s)
    p.write_text(s,encoding='utf-8')

p=Path('guides/best-cirque-shows/index.html')
s=p.read_text(encoding='utf-8')
s=re.sub(r'<meta name="description" content="[^"]*"\s*/>', '<meta name="description" content="All 4 current Cirque du Soleil shows in Las Vegas, ranked by a local — O, Michael Jackson ONE, KÀ and Mystère. Real prices, venues, and which Cirque show is right for you." />', s, count=1)
s=s.replace('"description": "The five Cirque du Soleil shows in Las Vegas, ranked by a local — with real prices and who each is best for."','"description": "The four current Cirque du Soleil shows in Las Vegas, ranked by a local — with real prices and who each is best for."')
s=s.replace('Every Cirque du Soleil show in Las Vegas ranked — the icon, the crowd-pleaser, the epic, the original and the newest. Real prices and which is right for you.','All four current Cirque du Soleil shows in Las Vegas ranked — the icon, the crowd-pleaser, the epic and the original. Real prices and which is right for you.')
lines=[]
for line in s.splitlines():
    if '"name": "How many Cirque du Soleil shows are in Las Vegas?"' in line:
        line='    { "@type": "Question", "name": "How many Cirque du Soleil shows are in Las Vegas?", "acceptedAnswer": { "@type": "Answer", "text": "There are four current resident Cirque du Soleil shows in Las Vegas: O at Bellagio, Michael Jackson ONE at Mandalay Bay, KÀ at MGM Grand and Mystère at Treasure Island." } },'
    elif '"name": "What is the cheapest Cirque du Soleil show in Vegas?"' in line:
        line='    { "@type": "Question", "name": "What is the cheapest Cirque du Soleil show in Vegas?", "acceptedAnswer": { "@type": "Answer", "text": "Mystère at Treasure Island is usually the lowest-priced current resident Cirque option, starting around $84. Check your date before booking because prices move by performance and seat." } },'
    lines.append(line)
s='\n'.join(lines)+'\n'
s=s.replace('a now-closed Cirque production','')
p.write_text(s,encoding='utf-8')

for slug in slugs:
    s=(Path('guides')/slug/'index.html').read_text(encoding='utf-8')
    assert 'Mad Apple' not in s and 'mad-apple' not in s
    assert 'guide-newsletter-form' in s
    assert 'guide-email-note"><' not in s
    assert '"dateModified": "2026-09-06"' in s
s=p.read_text(encoding='utf-8')
assert 'now-closed Cirque' not in s
assert 'five resident Cirque' not in s
assert 'The five Cirque' not in s
assert 'five Cirque du Soleil shows' not in s
print('final guide polish validated')
# trigger 2
