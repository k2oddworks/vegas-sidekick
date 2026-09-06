from pathlib import Path

path = Path('shows/music/vegas-the-show/index.html')
text = path.read_text(encoding='utf-8')

# 1) Mobile hero: photo first, like Carrot Top.
old_mobile = "@media(max-width:800px){.hero-grid,.verdict-grid,.seat-layout{grid-template-columns:1fr}.hero-copy{padding:38px 20px}.hero-media{min-height:360px}"
new_mobile = "@media(max-width:800px){.hero-grid,.verdict-grid,.seat-layout{grid-template-columns:1fr}.hero-copy{padding:38px 20px}.hero-media{order:-1;min-height:360px}"
if old_mobile not in text:
    raise SystemExit('Mobile hero CSS anchor not found')
text = text.replace(old_mobile, new_mobile, 1)

# 2) FAQ: add Carrot Top-style + / - circles.
old_faq = ".faq summary{cursor:pointer;list-style:none;font-weight:800;padding:18px 20px}.faq summary::-webkit-details-marker{display:none}.faq details p{margin:0;padding:0 20px 20px;color:#5d5468}"
new_faq = ".faq summary{cursor:pointer;list-style:none;font-weight:800;padding:18px 20px;display:flex;align-items:center;gap:14px}.faq summary::-webkit-details-marker{display:none}.faq summary::before{content:'+';display:grid;place-items:center;flex:0 0 34px;width:34px;height:34px;border-radius:50%;background:var(--purple);color:#fff;font:800 1.15rem 'Plus Jakarta Sans',sans-serif;line-height:1}.faq details:nth-child(2n) summary::before{background:var(--pink)}.faq details:nth-child(3n) summary::before{background:#f59e0b}.faq details[open] summary::before{content:'−'}.faq details p{margin:0;padding:0 20px 20px 68px;color:#5d5468}"
if old_faq not in text:
    raise SystemExit('FAQ CSS anchor not found')
text = text.replace(old_faq, new_faq, 1)

# 3) Later-date booking CTA in schedule section.
cta_css = ".later-date-cta{display:flex;align-items:center;justify-content:center;text-align:center;width:100%;margin:24px 0 4px;padding:18px 22px;border-radius:14px;background:linear-gradient(90deg,#ff6b20,#ff9a3d);color:#171225;font-family:'Plus Jakarta Sans',sans-serif;font-size:clamp(.95rem,2.5vw,1.08rem);font-weight:800;box-shadow:0 10px 28px rgba(255,107,32,.2);transition:.2s}.later-date-cta:hover{transform:translateY(-2px);filter:brightness(1.03)}"
css_anchor = ".schedule{display:grid;grid-template-columns:repeat(7,1fr);gap:8px;margin:24px 0}"
if css_anchor not in text:
    raise SystemExit('Schedule CSS anchor not found')
text = text.replace(css_anchor, css_anchor + cta_css, 1)

schedule_start = text.find('<section class="section" id="schedule">')
if schedule_start == -1:
    raise SystemExit('Schedule section not found')
schedule_end = text.find('</section>', schedule_start)
if schedule_end == -1:
    raise SystemExit('Schedule section end not found')
button = '<a class="later-date-cta" href="https://spotlight.vegas/shows/music/vegas-the-show/ref/vegassidekick" target="_blank" rel="noopener sponsored">Booking for a later date? See tickets weeks and months ahead →</a>'
if 'Booking for a later date?' not in text[schedule_start:schedule_end]:
    text = text[:schedule_end] + button + text[schedule_end:]

# 4) Fix All Shook Up card image extension.
text = text.replace('/images/all-shook-up-hero.webp', '/images/all-shook-up-hero.jpg')

path.write_text(text, encoding='utf-8')
print('VEGAS! The Show polish patch applied')
