from pathlib import Path
import re
p=Path('shows/comedy/carrot-top/index.html')
s=p.read_text()
old='<a href="#quick">Quick take</a><a href="#photos">Photos</a><a href="#trailer">Trailer</a><a href="#seats">Seat guide</a><a href="#fit">Is it for you?</a><a href="#showtimes">Showtimes</a><a href="#faq">FAQ</a>'
new='<a href="#quick">Quick take</a><a href="#showtimes">Showtimes</a><a href="#photos">Photos</a><a href="#trailer">Trailer</a><a href="#seats">Seat guide</a><a href="#fit">Is it for you?</a><a href="#faq">FAQ</a>'
if old not in s: raise SystemExit('Expected Carrot Top subnav not found')
s=s.replace(old,new,1)
pat=re.compile(r'(<section class="[^"]*\bsection\b[^"]*" id="(?P<id>quick|photos|trailer|seats|fit|showtimes|faq)".*?</section>)')
matches=list(pat.finditer(s))
byid={m.group('id'):m.group(1) for m in matches}
required=['quick','photos','trailer','seats','fit','showtimes','faq']
missing=[x for x in required if x not in byid]
if missing: raise SystemExit(f'Missing sections: {missing}')
start=min(m.start() for m in matches); end=max(m.end() for m in matches)
order=['quick','showtimes','photos','trailer','seats','fit','faq']
s=s[:start]+''.join(byid[x] for x in order)+s[end:]
p.write_text(s)
print('Carrot Top order:', ' > '.join(order))
