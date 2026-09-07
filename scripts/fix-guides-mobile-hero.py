from pathlib import Path
p=Path('guides/index.html')
s=p.read_text()
old="@media(max-width:760px){.hero{padding:48px 0}.start,.grid{grid-template-columns:1fr}"
new="@media(max-width:760px){.hero{padding:78px 0 48px}.start,.grid{grid-template-columns:1fr}"
assert old in s, 'mobile hero rule not found'
s=s.replace(old,new,1)
p.write_text(s)
# trigger mobile clearance fix
