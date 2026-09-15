from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'shows/music/barry-manilow/index.html'
s=p.read_text()
s=s.replace('Barry Manilow Las Vegas Tickets from $91 | 2026 Westgate Dates','Barry Manilow Las Vegas Tickets from $91 | 2026–2027 Westgate Dates')
s=s.replace('See current 2026 dates, showtimes, photos, seat tips and whether it\'s right for you.','See current 2026 and 2027 dates, showtimes, photos, seat tips and whether it\'s right for you.')
s=s.replace('Barry Manilow Las Vegas Tickets & 2026 Westgate Show Guide','Barry Manilow Las Vegas Tickets & 2026–2027 Westgate Show Guide')
s=s.replace('Barry Manilow Las Vegas Tickets & 2026 Westgate Dates','Barry Manilow Las Vegas Tickets & 2026–2027 Westgate Dates')
s=s.replace('Remaining posted 2026 dates run in select Thursday-through-Saturday blocks from October 8 through December 19.','Posted dates now extend into 2027, including February, March and April performances at Westgate.')
s=s.replace('<span class="chip">Select Thu–Sat blocks</span>','<span class="chip">2027 dates added</span><span class="chip">Select Thu–Sat blocks</span>',1)
s=s.replace('Last updated September 8, 2026','Show info confirmed September 2026')
s=s.replace('<a href="#dates">2026 dates</a>','<a href="#dates">Dates</a>')
s=s.replace('<strong>Oct–Dec</strong><span>Remaining 2026 blocks</span>','<strong>Into 2027</strong><span>Dates now posted</span>')
s=s.replace('The residency plays select Thursday-through-Saturday blocks. Remaining posted 2026 dates run from October 8 through December 19.','The residency plays select date blocks. Posted performances now extend into April 2027.')
s=s.replace('"dateModified":"2026-09-08","lastReviewed":"2026-09-08"','"dateModified":"2026-09-15","lastReviewed":"2026-09-15"')
# Add a visible update near the dates section without inventing a full schedule beyond verified listings.
marker='<section class="section" id="dates">'
if marker in s and '2027 dates added' not in s[s.find(marker):s.find(marker)+1500]:
    s=s.replace(marker,marker+'<div class="wrap"><div class="take"><b>2027 dates added</b><p>Barry Manilow’s Westgate calendar now extends into 2027. Current listings include February 18–20 and 25–27, March 25–27, and April 1–3. Check current ticket inventory for the exact time and availability on your date.</p></div></div>',1)
p.write_text(s)

# Put the new Dispatch story first on the Dispatch index using the existing card system.
idx=root/'news/index.html'
t=idx.read_text()
if '/news/barry-manilow-adds-2027-las-vegas-dates/' not in t:
    anchor='<div class="news-grid">'
    card='''<article class="news-card"><a href="/news/barry-manilow-adds-2027-las-vegas-dates/"><img src="/images/news/barry-manilow-residency-poster.jpg" alt="Barry Manilow record-breaking residency artwork" loading="lazy"><div class="news-card-body"><div class="news-card-meta">September 15, 2026 · Residency News</div><h2>Barry Manilow’s Westgate run now reaches into 2027</h2><p>Newly posted February, March and April performances give Manilow fans more Vegas dates to plan around.</p><span>Read the story →</span></div></a></article>'''
    if anchor in t: t=t.replace(anchor,anchor+card,1)
idx.write_text(t)
