from pathlib import Path

path = Path('shows/comedy/carrot-top/index.html')
text = path.read_text(encoding='utf-8')

old_css = '''.final{background:var(--navy);color:#fff;padding:60px 0;text-align:center}
.final p{color:#cfc8df;margin:10px 0 22px}
.final-price{font-family:var(--display);font-size:3rem;font-weight:800;margin-bottom:18px}
.final .cta{border:2px solid #fff}
.final-note{font-size:.72rem!important;margin-top:16px!important;color:#cfc8df!important}'''

new_css = '''.final{position:relative;overflow:hidden;background:linear-gradient(135deg,#12061f 0%,#24104d 52%,#1c0a3a 100%);color:#fff;padding:72px 0}
.final::before{content:"";position:absolute;inset:-30%;background:radial-gradient(circle at 20% 40%,rgba(124,58,237,.34),transparent 34%),radial-gradient(circle at 82% 58%,rgba(255,44,125,.22),transparent 30%);pointer-events:none}
.final::after{content:"";position:absolute;top:0;left:0;right:0;height:4px;background:linear-gradient(90deg,var(--lime),var(--blue),var(--pink))}
.final .wrap{position:relative;z-index:1}
.final-card{max-width:960px;margin:auto;display:grid;grid-template-columns:minmax(0,1fr) 280px;gap:34px;align-items:center;padding:36px 40px;border:1px solid rgba(255,255,255,.22);border-radius:26px;background:linear-gradient(135deg,rgba(255,255,255,.1),rgba(255,255,255,.045));box-shadow:0 24px 60px rgba(5,2,18,.32);backdrop-filter:blur(10px)}
.final-copy{text-align:left}
.final-eyebrow{font-family:var(--display);font-size:.72rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--lime);margin-bottom:10px}
.final h2{font-size:clamp(2rem,4vw,3.25rem);margin:0 0 10px}
.final-meta{color:#d8d1e8;font-size:.92rem;margin:0 0 20px}
.final-offer{display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.final-price-pill{display:inline-flex;align-items:baseline;gap:7px;padding:10px 15px;border-radius:999px;background:rgba(198,242,46,.12);border:1px solid rgba(198,242,46,.5);color:#fff;font-family:var(--display);font-weight:800}
.final-price-pill small{font-size:.68rem;text-transform:uppercase;letter-spacing:.09em;color:var(--lime)}
.final-support{color:#eee9f7;font-size:.9rem;max-width:48ch;margin:0}
.final-chips{display:flex;gap:8px;flex-wrap:wrap;margin-top:18px}
.final-chip{display:inline-flex;align-items:center;gap:6px;padding:7px 10px;border-radius:999px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);color:#f6f2ff;font-size:.7rem;font-weight:700}
.final-actions{display:flex;flex-direction:column;gap:12px;min-width:0}
.final .cta{width:100%;border:2px solid #fff;padding:17px 22px;font-size:1.02rem;box-shadow:0 14px 34px rgba(59,130,246,.3)}
.final .cta::after{content:"";position:absolute;top:-35%;bottom:-35%;left:-55%;width:38%;transform:skewX(-20deg);background:linear-gradient(90deg,transparent,rgba(255,255,255,.42),transparent);animation:finalCtaShimmer 5.2s ease-in-out infinite}
@keyframes finalCtaShimmer{0%,74%{left:-55%}90%,100%{left:135%}}
.final-note{font-size:.74rem;color:#cfc8df;text-align:center;margin:0}
@media(max-width:760px){.final{padding:54px 0}.final-card{grid-template-columns:1fr;padding:28px 22px;gap:26px}.final-actions{width:100%}.final h2{font-size:clamp(2rem,9vw,2.7rem)}}'''

old_html = '''<section class="final">
  <div class="wrap">
    <h2>Carrot Top from $62</h2>
    <p>Luxor · typical Mon–Sat 8 PM schedule · 75 minutes · ages 16+</p>
    <div class="final-price">From $62</div>
    <a class="cta final-cta-btn" href="https://spotlight.vegas/shows/comedy/carrot-top/ref/vegassidekick" target="_blank" rel="noopener sponsored">Get Tickets →</a>
    <p class="final-note">Choose your date, compare seats and review the final total before paying.</p>
  </div>
</section>'''

new_html = '''<section class="final">
  <div class="wrap">
    <div class="final-card">
      <div class="final-copy">
        <div class="final-eyebrow">🌵 One last look</div>
        <h2>Ready for Carrot Top?</h2>
        <p class="final-meta">Luxor · typical Mon–Sat 8 PM · 75 minutes · ages 16+</p>
        <div class="final-offer">
          <div class="final-price-pill"><small>From</small> $62</div>
          <p class="final-support">Choose your date, compare seats and see the live total before checkout.</p>
        </div>
        <div class="final-chips" aria-label="Booking benefits">
          <span class="final-chip">● Live pricing</span>
          <span class="final-chip">↔ Compare seats</span>
          <span class="final-chip">✓ Choose your date</span>
        </div>
      </div>
      <div class="final-actions">
        <a class="cta final-cta-btn" href="https://spotlight.vegas/shows/comedy/carrot-top/ref/vegassidekick" target="_blank" rel="noopener sponsored">Check dates &amp; prices →</a>
        <p class="final-note">See the available seats and final total before you pay.</p>
      </div>
    </div>
  </div>
</section>'''

if old_css not in text:
    raise SystemExit('Expected final CTA CSS block not found; refusing to patch.')
if old_html not in text:
    raise SystemExit('Expected final CTA HTML block not found; refusing to patch.')

text = text.replace(old_css, new_css, 1).replace(old_html, new_html, 1)
path.write_text(text, encoding='utf-8')
print('Carrot Top final CTA updated.')
