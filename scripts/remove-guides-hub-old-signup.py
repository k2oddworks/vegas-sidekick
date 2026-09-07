from pathlib import Path
p=Path('guides/index.html')
s=p.read_text()
old='<div class="signup"><h3>Want the Vegas stuff worth knowing?</h3><p>New openings, show changes and genuinely useful deals. Email not required. Want occasional Vegas updates? Join our list.</p></div>'
assert old in s, 'old signup card not found'
s=s.replace(old,'',1)
assert 'Want the Vegas stuff worth knowing?' not in s
p.write_text(s)
