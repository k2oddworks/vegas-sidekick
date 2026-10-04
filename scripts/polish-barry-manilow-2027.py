from pathlib import Path
root=Path(__file__).resolve().parents[1]

# Dispatch article: protect the portrait crop on mobile and strengthen Kris Kidd identity.
p=root/'news/barry-manilow-adds-2027-las-vegas-dates/index.html'
s=p.read_text()
s=s.replace('@media(max-width:800px){.grid{grid-template-columns:1fr}.media{order:-1;min-height:0;height:410px}.copy{padding:34px 22px 42px}.media:after{background:linear-gradient(0deg,#130821,transparent 30%)}}','@media(max-width:800px){.grid{grid-template-columns:1fr}.media{order:-1;min-height:0;height:auto;aspect-ratio:1024/1365;background:#130821}.media img{width:100%;height:auto;aspect-ratio:1024/1365;object-fit:contain;object-position:center top}.copy{padding:34px 22px 42px}.media:after{background:linear-gradient(0deg,#130821 0,transparent 16%)}}')
s=s.replace('.take b{color:#d6f33c}', '.take b{color:#d6f33c}.take-head{display:flex;align-items:center;gap:11px;margin-bottom:10px}.take-head img{width:42px;height:42px;border-radius:50%;object-fit:cover;border:2px solid rgba(255,255,255,.75)}.take-head b{display:block}')
s=s.replace('<div class="take"><b>🌵 Kris\'s take</b><p>', '<div class="take"><div class="take-head"><img src="/images/brand/kris-kidd.webp" alt="Kris Kidd"><b>🌵 Kris Kidd\'s take</b></div><p>')
p.write_text(s)

# Product page: use full name in the authority callout and show the actual posted 2027 dates.
p=root/'shows/music/barry-manilow/index.html'
s=p.read_text()
s=s.replace('.take b{color:#ffd36e;text-transform:uppercase}', '.take b{color:#ffd36e;text-transform:uppercase}.take-head{display:flex;align-items:center;gap:10px;margin-bottom:8px}.take-head img{width:40px;height:40px;border-radius:50%;object-fit:cover;border:2px solid rgba(255,255,255,.7)}')
s=s.replace('<div class="take"><b>🌵 Kris\'s take</b><p>', '<div class="take"><div class="take-head"><img src="/images/brand/kris-kidd.webp" alt="Kris Kidd"><b>🌵 Kris Kidd\'s take</b></div><p>',1)
# Replace the temporary 2027 notice with concrete date cards in the existing dates grid.
s=s.replace('<div class="wrap"><div class="take"><b>2027 dates added</b><p>Barry Manilow’s Westgate calendar now extends into 2027. Current listings include February 18–20 and 25–27, March 25–27, and April 1–3. Check current ticket inventory for the exact time and availability on your date.</p></div></div>', '<div class="wrap"><div class="take"><b>2027 dates added</b><p>Barry Manilow’s Westgate calendar now extends into April 2027. Current posted dates are below.</p></div><div class="dates" style="margin-top:14px"><div class="month"><b>February 2027</b><p>18, 19, 20 · 25, 26, 27</p></div><div class="month"><b>March 2027</b><p>25, 26, 27</p></div><div class="month"><b>April 2027</b><p>1, 2, 3</p></div></div></div>')
p.write_text(s)
