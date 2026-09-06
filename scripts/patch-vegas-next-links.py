from pathlib import Path

p=Path('shows/music/vegas-the-show/index.html')
s=p.read_text(encoding='utf-8')

# Add small author/disclosure styling for the Carrot Top-style utility section.
css_anchor=".final{background:radial-gradient(circle at 15% 10%,rgba(214,243,60,.16),transparent 30%),linear-gradient(135deg,#150525,#4d104a);color:#fff;text-align:center;padding:68px 24px;border-radius:24px}"
css_add=".next-links .decision{grid-template-columns:repeat(3,1fr);margin-top:26px}.next-links .decision-card{display:block;padding:24px 26px;min-height:150px}.next-links .decision-card h3{font-size:1.05rem;color:var(--ink);margin-bottom:8px}.next-links .decision-card p{font-size:.94rem;line-height:1.55}.byline{margin:38px 0 0;font-size:.9rem;color:#332b3c}.byline a{text-decoration:underline;text-underline-offset:3px}.next-links .disclosure{text-align:left;margin:18px 0 0;max-width:none;font-size:.82rem;color:#756c80}@media(max-width:800px){.next-links .decision{grid-template-columns:1fr}.next-links .decision-card{min-height:0;padding:22px}.byline{font-size:.86rem}.next-links .disclosure{margin-bottom:0}}"
if css_anchor not in s:
    raise SystemExit('final CSS anchor not found')
s=s.replace(css_anchor,css_add+css_anchor,1)

# Insert the same decision-support layer used on Carrot Top, tailored to this show.
anchor='<section class="section"><div class="wrap"><div class="final"><div class="eyebrow" style="color:var(--gold)">Classic Vegas, still onstage</div>'
if anchor not in s:
    raise SystemExit('final section anchor not found')
block='''<section class="section next-links"><div class="wrap"><div class="eyebrow">Still deciding?</div><h2>Make the next click useful</h2><div class="decision"><a class="decision-card" href="/shows/music/"><h3>Compare music &amp; variety shows →</h3><p>Want more concert energy or a different kind of stage production? Compare the other music and variety options.</p></a><a class="decision-card" href="/venues/planet-hollywood/"><h3>Explore Planet Hollywood shows →</h3><p>See what else is playing at Planet Hollywood and Miracle Mile Shops before adding another rideshare.</p></a><a class="decision-card" href="/guides/best-shows-for-first-timers/"><h3>First trip to Vegas? →</h3><p>Compare our first-timer picks if you want the show that gives you the clearest "we're in Vegas" moment.</p></a></div><p class="byline">By <a href="/about/kris-kidd/">Kris Kidd</a> · Las Vegas local since 2005, in show ticketing since 2006. Last updated September 2026.</p><p class="disclosure"><strong>Affiliate disclosure:</strong> Vegas Sidekick may earn a commission when you book through links on this page, at no extra cost to you.</p></div></section>'''
s=s.replace(anchor,block+anchor,1)

# Remove the duplicate disclosure that previously lived inside the final CTA section.
dupe='<p class="disclosure">Vegas Sidekick may earn a commission when you book through ticket links on this page, at no extra cost to you.</p>'
s=s.replace(dupe,'',1)

p.write_text(s,encoding='utf-8')
print('VEGAS decision-support section added')
