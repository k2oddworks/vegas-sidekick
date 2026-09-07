from pathlib import Path
p=Path('guides/index.html')
s=p.read_text()
old='@media(max-width:760px){.hero{padding:78px 0 48px}'
new='@media(max-width:760px){.hero{padding:108px 0 48px}'
assert old in s, 'expected mobile hero rule not found'
s=s.replace(old,new,1)
assert new in s
p.write_text(s)
# one-time mobile clearance fix
