// Vegas Sidekick — Shared Footer Component
// v11 — SEO/internal-link polish, worker-only email capture, Spike sparkle Easter egg
(function () {
  'use strict';

  const WORKER_URL = 'https://brevo-subscribe.vegassidekickcom.workers.dev';

  const html = `
<div class="vs-email-bar" id="vsEmailBar">
  <div class="vs-email-bar-inner">
    <div class="vs-email-copy">
      <span class="vs-email-bar-badge">🌵 Spike's Insider List</span>
      <div class="vs-email-bar-headline">The Vegas stuff worth knowing</div>
      <div class="vs-email-bar-proof">Show changes, openings and useful Vegas deals. No daily spam.</div>
    </div>
    <div class="vs-email-action">
      <form class="vs-email-form" id="vsEmailForm" onsubmit="return vsSubmitEmail(event)">
        <label class="vs-sr-only" for="vsEmailInput">Email address</label>
        <input type="email" id="vsEmailInput" placeholder="your@email.com" required autocomplete="email">
        <button type="submit" id="vsEmailBtn">Join the list</button>
      </form>
      <div class="vs-email-success" id="vsEmailSuccess" role="status" aria-live="polite">You're on the list. 🌵</div>
      <div class="vs-email-error" id="vsEmailError" role="status" aria-live="polite"></div>
    </div>
  </div>
</div>

<footer id="vs-footer-inner">
  <div class="vs-footer-shell">
    <div class="vs-footer-grid">
      <section class="vs-footer-brand" aria-labelledby="vsFooterBrandName">
        <button class="vs-footer-spike-button" id="vsFooterSpike" type="button" aria-label="Make Spike sparkle">
          <img class="vs-footer-spike" src="/images/spike-podcast-badge.webp" alt="Spike, the Vegas Sidekick cactus mascot" width="140" height="140" loading="lazy">
          <span class="vs-spike-ring" aria-hidden="true"></span>
        </button>
        <a class="vs-footer-logo" id="vsFooterBrandName" href="/" aria-label="Vegas Sidekick home">vegas <span>sidekick</span></a>
        <p class="vs-footer-tagline"><strong>Biggest Shows. Real Discounts. No BS.</strong><br>We live here. We know the shows. We tell you the truth.</p>
        <p class="vs-footer-seo">Vegas Sidekick is a Las Vegas show guide built by locals who work around tickets and entertainment. We compare shows, prices, venues and the tradeoffs worth knowing before you book.</p>
      </section>

      <nav class="vs-footer-nav" aria-label="Las Vegas show categories">
        <h2>Shows</h2>
        <a href="/shows/" class="vs-footer-all">All Shows</a>
        <a href="/shows/comedy/">Comedy</a>
        <a href="/shows/magic/">Magic</a>
        <a href="/shows/cirque/">Cirque &amp; Acrobatic</a>
        <a href="/shows/music/">Music &amp; Variety</a>
        <a href="/shows/spectaculars/">Spectaculars</a>
        <a href="/shows/family/">Family Shows</a>
        <a href="/shows/adult/">Adult Shows</a>
      </nav>

      <nav class="vs-footer-nav vs-footer-explore" aria-label="Explore Vegas Sidekick">
        <h2>Explore</h2>
        <a href="/search/">Search All Shows</a>
        <a href="/venues/">Shows by Venue</a>
        <a href="/guides/" class="vs-footer-feature vs-feature-guides"><span>●</span> Vegas Guides</a>
        <a href="/guides/best-shows-for-first-timers/">Best Shows for First-Timers</a>
        <a href="/guides/best-cheap-vegas-shows/" class="vs-footer-feature vs-feature-deals"><span>●</span> Deals Under $50</a>
        <a href="/news/" class="vs-footer-feature vs-feature-dispatch"><span>●</span> Vegas Dispatch</a>
        <a href="/about/">About Vegas Sidekick</a>
        <a href="/about/kris-kidd/">About Kris Kidd</a>
        <a href="/contact/">Contact</a>
      </nav>

      <nav class="vs-footer-nav" aria-label="Legal and policies">
        <h2>Legal</h2>
        <a href="/affiliate-disclosure/">Affiliate Disclosure</a>
        <a href="/privacy/">Privacy Policy</a>
        <a href="/terms/">Terms of Use</a>
        <a class="vs-footer-easter" href="/play/walk-the-strip/">Walk the Strip ↗</a>
      </nav>
    </div>

    <div class="vs-footer-bottom">
      <span>© 2026 Vegas Sidekick. All rights reserved.</span>
      <span>Vegas Sidekick may earn a commission when you buy tickets through our links. That never changes our recommendations.</span>
    </div>
  </div>
</footer>`;

  const styles = `
<style id="vs-footer-styles">
#vs-footer,#vs-footer-inner,#vs-email-bar{font-family:'Inter',sans-serif;box-sizing:border-box}#vs-footer *,#vs-footer-inner *,#vs-email-bar *{box-sizing:border-box}.vs-sr-only{position:absolute!important;width:1px!important;height:1px!important;padding:0!important;margin:-1px!important;overflow:hidden!important;clip:rect(0,0,0,0)!important;white-space:nowrap!important;border:0!important}
.vs-email-bar{background:linear-gradient(100deg,#27104a,#38155d 55%,#113a49);color:#fff;border-top:1px solid rgba(255,255,255,.08);border-bottom:1px solid rgba(255,255,255,.08)}.vs-email-bar-inner{width:min(1180px,calc(100% - 40px));margin:auto;display:flex;align-items:center;justify-content:space-between;gap:30px;padding:25px 0}.vs-email-copy{min-width:0}.vs-email-bar-badge{display:block;color:#c6f22e;font:700 .68rem 'Plus Jakarta Sans',sans-serif;text-transform:uppercase;letter-spacing:.11em;margin-bottom:7px}.vs-email-bar-headline{font:800 clamp(1.25rem,2vw,1.65rem) 'Plus Jakarta Sans',sans-serif;letter-spacing:-.03em;line-height:1.1}.vs-email-bar-proof{color:#cfc4d7;font-size:.82rem;margin-top:6px}.vs-email-action{width:min(450px,100%)}.vs-email-form{display:flex;gap:8px}.vs-email-form input{flex:1;min-width:0;border:1px solid rgba(255,255,255,.22);background:rgba(255,255,255,.1);color:#fff;border-radius:10px;padding:13px 14px;font:500 .9rem Inter,sans-serif;outline:none}.vs-email-form input::placeholder{color:#bdb0c6}.vs-email-form input:focus{border-color:#c6f22e;box-shadow:0 0 0 3px rgba(198,242,46,.12)}.vs-email-form button{border:2px solid #fff;background:#ff2e7e;color:#fff;border-radius:10px;padding:12px 17px;font:800 .86rem 'Plus Jakarta Sans',sans-serif;cursor:pointer;white-space:nowrap;transition:.18s}.vs-email-form button:hover{transform:translateY(-1px);background:#ff1f72}.vs-email-form button:disabled{opacity:.65;cursor:default;transform:none}.vs-email-success,.vs-email-error{display:none;font-weight:700;font-size:.88rem}.vs-email-success.visible{display:block;color:#dff78b}.vs-email-error.visible{display:block;color:#ffd2e3;margin-top:7px}
#vs-footer-inner{position:relative;overflow:hidden;background:radial-gradient(700px 440px at 9% 12%,rgba(124,58,237,.17),transparent 70%),linear-gradient(180deg,#160724 0%,#100519 100%);color:#fff;border-top:1px solid rgba(255,255,255,.07)}#vs-footer-inner:before{content:'';position:absolute;inset:0 0 auto;height:2px;background:linear-gradient(90deg,#ff2e7e,#7c3aed,#0fb5c9,#c6f22e);opacity:.85}.vs-footer-shell{position:relative;width:min(1180px,calc(100% - 48px));margin:auto;padding:58px 0 36px}.vs-footer-grid{display:grid;grid-template-columns:minmax(260px,1.45fr) repeat(3,minmax(150px,.8fr));gap:44px}.vs-footer-brand{min-width:0}.vs-footer-spike-button{position:relative;display:block;width:118px;height:118px;padding:0;margin:0 0 24px;background:none;border:0;border-radius:50%;cursor:pointer;isolation:isolate}.vs-footer-spike{width:118px;height:118px;object-fit:cover;border-radius:50%;display:block;box-shadow:0 0 0 1px rgba(255,255,255,.13),0 12px 32px rgba(0,0,0,.25);transition:transform .18s,filter .18s}.vs-footer-spike-button:hover .vs-footer-spike,.vs-footer-spike-button:focus-visible .vs-footer-spike{transform:scale(1.035);filter:brightness(1.06)}.vs-footer-spike-button:focus-visible{outline:3px solid #c6f22e;outline-offset:5px}.vs-spike-ring{position:absolute;inset:-5px;border:1px solid rgba(168,85,247,.3);border-radius:50%;pointer-events:none;transition:.2s}.vs-footer-spike-button.is-sparkling .vs-spike-ring{box-shadow:0 0 30px rgba(168,85,247,.55);border-color:#a855f7}.vs-footer-spark{position:fixed;z-index:9999;width:5px;height:5px;border-radius:50%;pointer-events:none;transform:translate(-50%,-50%);animation:vsSpark .68s cubic-bezier(.17,.67,.22,1) forwards;box-shadow:0 0 8px currentColor}@keyframes vsSpark{0%{opacity:0;transform:translate(-50%,-50%) scale(.35)}15%{opacity:1}100%{opacity:0;transform:translate(calc(-50% + var(--sx)),calc(-50% + var(--sy))) scale(.1)}}.vs-footer-logo{display:inline-block;color:#fff;text-decoration:none;font:800 1.45rem 'Plus Jakarta Sans',sans-serif;letter-spacing:-.045em;margin-bottom:14px}.vs-footer-logo span{color:#ff2e7e}.vs-footer-tagline{color:#bdb1c7;font-size:.95rem;line-height:1.55;margin:0 0 18px}.vs-footer-tagline strong{color:#fff;font-family:'Plus Jakarta Sans',sans-serif}.vs-footer-seo{max-width:420px;margin:0;color:#8f8299;font-size:.79rem;line-height:1.65}.vs-footer-nav{display:flex;flex-direction:column;align-items:flex-start;gap:8px}.vs-footer-nav h2{margin:0 0 8px;color:#c6f22e;font:800 .72rem 'Plus Jakarta Sans',sans-serif;text-transform:uppercase;letter-spacing:.14em}.vs-footer-nav a{position:relative;color:#b8acbf;text-decoration:none;font-size:.9rem;line-height:1.35;padding:2px 0;transition:color .16s,transform .16s}.vs-footer-nav a:after{content:'';position:absolute;left:0;right:100%;bottom:0;height:1px;background:#a855f7;transition:right .18s}.vs-footer-nav a:hover,.vs-footer-nav a:focus-visible{color:#fff;transform:translateX(2px)}.vs-footer-nav a:hover:after,.vs-footer-nav a:focus-visible:after{right:0}.vs-footer-nav a:focus-visible{outline:2px solid rgba(198,242,46,.6);outline-offset:4px;border-radius:2px}.vs-footer-all{color:#fff!important;font-weight:700}.vs-footer-feature{font-weight:700!important}.vs-footer-feature span{font-size:.7em;margin-right:5px}.vs-feature-guides{color:#9fc4ff!important}.vs-feature-guides span{color:#3b82f6}.vs-feature-deals{color:#ceb8ff!important}.vs-feature-deals span{color:#a855f7}.vs-feature-dispatch{color:#9feaf3!important}.vs-feature-dispatch span{color:#0fb5c9}.vs-footer-easter{color:#b46cf4!important;margin-top:3px}.vs-footer-bottom{display:grid;grid-template-columns:auto minmax(260px,560px);justify-content:space-between;gap:28px;border-top:1px solid rgba(255,255,255,.1);margin-top:50px;padding-top:24px;color:#7f7487;font-size:.72rem;line-height:1.55}.vs-footer-bottom span:last-child{text-align:right}
#vs-deal-overlay{position:fixed;inset:0;z-index:9000;display:flex;align-items:center;justify-content:center;padding:20px;opacity:0;pointer-events:none;transition:opacity .25s ease}#vs-deal-overlay.visible{opacity:1;pointer-events:auto}.vs-deal-backdrop{position:absolute;inset:0;background:rgba(6,3,14,.84);backdrop-filter:blur(5px)}.vs-deal-card{position:relative;z-index:1;width:min(400px,100%);padding:32px 28px 25px;background:#160724;color:#fff;border:1px solid rgba(168,85,247,.28);border-top:3px solid #ff2e7e;border-radius:16px;box-shadow:0 24px 60px rgba(0,0,0,.55);transform:translateY(10px);transition:transform .25s}.visible .vs-deal-card{transform:none}.vs-deal-close{position:absolute;top:12px;right:13px;border:0;background:none;color:#a99db2;font-size:1.1rem;cursor:pointer}.vs-deal-opening{color:#0fb5c9;font:700 .67rem 'Plus Jakarta Sans',sans-serif;text-transform:uppercase;letter-spacing:.1em;margin-bottom:10px}.vs-deal-headline{font:800 1.65rem 'Plus Jakarta Sans',sans-serif;line-height:1.08;margin-bottom:17px}.vs-deal-form{display:grid;gap:8px}.vs-deal-input{width:100%;padding:12px 13px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);border-radius:9px;color:#fff;font:500 .86rem Inter,sans-serif;outline:none}.vs-deal-input:focus{border-color:#c6f22e}.vs-deal-btn{border:0;border-radius:9px;padding:12px;background:#ff2e7e;color:#fff;font:800 .85rem 'Plus Jakarta Sans',sans-serif;cursor:pointer}.vs-deal-success{display:none;color:#c6f22e;font-weight:700;margin:12px 0}.vs-deal-success.visible{display:block}.vs-deal-tagline{color:#8f8299;font-size:.7rem;margin:13px 0}.vs-deal-skip{border:0;background:none;color:#807487;font-size:.68rem;text-decoration:underline;cursor:pointer;padding:0}
@media(max-width:900px){.vs-footer-grid{grid-template-columns:1.2fr 1fr 1fr}.vs-footer-brand{grid-column:1/-1;max-width:600px}.vs-footer-spike-button{width:104px;height:104px}.vs-footer-spike{width:104px;height:104px}.vs-footer-bottom{grid-template-columns:1fr}.vs-footer-bottom span:last-child{text-align:left}.vs-email-bar-inner{align-items:flex-start;flex-direction:column;gap:16px}.vs-email-action{width:100%}}
@media(max-width:620px){.vs-footer-shell{width:calc(100% - 40px);padding:46px 0 28px}.vs-footer-grid{grid-template-columns:1fr 1fr;gap:36px 26px}.vs-footer-brand{grid-column:1/-1}.vs-footer-nav:last-of-type{grid-column:1/-1}.vs-footer-seo{font-size:.78rem}.vs-email-bar-inner{width:calc(100% - 40px);padding:22px 0}.vs-email-form{display:grid}.vs-email-form button{width:100%}.vs-footer-bottom{margin-top:38px}.vs-footer-spike-button{width:96px;height:96px}.vs-footer-spike{width:96px;height:96px}}
@media(max-width:400px){.vs-footer-grid{grid-template-columns:1fr}.vs-footer-nav:last-of-type{grid-column:auto}}
@media(prefers-reduced-motion:reduce){.vs-footer-spark{display:none}.vs-footer-spike,.vs-footer-nav a,.vs-footer-nav a:after,.vs-email-form button{transition:none!important}}
</style>`;

  function mountFooter() {
    const target = document.getElementById('vs-footer');
    if (!target) return false;
    if (!document.getElementById('vs-footer-styles')) document.head.insertAdjacentHTML('beforeend', styles);
    target.innerHTML = html;
    bindSpike();
    injectOrganizationSchema();
    initDealOverlay();
    return true;
  }

  function bindSpike() {
    const button = document.getElementById('vsFooterSpike');
    if (!button || button.dataset.bound === '1') return;
    button.dataset.bound = '1';
    button.addEventListener('click', function () {
      button.classList.add('is-sparkling');
      setTimeout(function () { button.classList.remove('is-sparkling'); }, 650);
      if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
      const rect = button.getBoundingClientRect();
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;
      const colors = ['#a855f7','#7c3aed','#c084fc','#c6f22e','#b56cff'];
      for (let i = 0; i < 16; i++) {
        const p = document.createElement('span');
        p.className = 'vs-footer-spark';
        const angle = (Math.PI * 2 * i / 16) + (Math.random() - .5) * .22;
        const distance = 34 + Math.random() * 55;
        p.style.left = cx + 'px';
        p.style.top = cy + 'px';
        p.style.color = colors[i % colors.length];
        p.style.background = 'currentColor';
        p.style.setProperty('--sx', Math.cos(angle) * distance + 'px');
        p.style.setProperty('--sy', Math.sin(angle) * distance + 'px');
        document.body.appendChild(p);
        setTimeout(function () { if (p.parentNode) p.parentNode.removeChild(p); }, 760);
      }
    });
  }

  function injectOrganizationSchema() {
    if (document.getElementById('vs-organization-schema')) return;
    const script = document.createElement('script');
    script.id = 'vs-organization-schema';
    script.type = 'application/ld+json';
    script.textContent = JSON.stringify({
      '@context':'https://schema.org',
      '@type':'Organization',
      '@id':'https://vegassidekick.com/#organization',
      name:'Vegas Sidekick',
      url:'https://vegassidekick.com/',
      logo:{'@type':'ImageObject',url:'https://vegassidekick.com/images/logo-pill-alt.png'},
      founder:{'@type':'Person','@id':'https://vegassidekick.com/about/kris-kidd/#kris',name:'Kris Kidd',url:'https://vegassidekick.com/about/kris-kidd/'}
    });
    document.head.appendChild(script);
  }

  window.vsSubmitEmail = async function (e) {
    if (e) e.preventDefault();
    const input = document.getElementById('vsEmailInput');
    const btn = document.getElementById('vsEmailBtn');
    const form = document.getElementById('vsEmailForm');
    const success = document.getElementById('vsEmailSuccess');
    const error = document.getElementById('vsEmailError');
    const email = input ? input.value.trim() : '';
    if (!email || !email.includes('@')) return false;
    if (error) { error.classList.remove('visible'); error.textContent = ''; }
    if (btn) { btn.disabled = true; btn.textContent = 'Joining…'; }
    try {
      const response = await fetch(WORKER_URL,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:email})});
      if (!response.ok) throw new Error('subscribe failed');
      if (form) form.style.display = 'none';
      if (success) success.classList.add('visible');
    } catch (err) {
      if (btn) { btn.disabled = false; btn.textContent = 'Try again'; }
      if (error) { error.textContent = 'Could not subscribe right now.'; error.classList.add('visible'); }
    }
    return false;
  };

  function initDealOverlay() {
    if (document.getElementById('vs-deal-overlay')) return;
    const STORAGE_KEY = 'vs_deal_alert_captured';
    if (localStorage.getItem(STORAGE_KEY)) return;
    const overlayHTML = `
      <div id="vs-deal-overlay" role="dialog" aria-modal="true" aria-label="Vegas deal alerts">
        <div class="vs-deal-backdrop"></div>
        <div class="vs-deal-card">
          <button class="vs-deal-close" type="button" onclick="vsDealClose()" aria-label="Close">✕</button>
          <div class="vs-deal-opening">Your tickets are opening now →</div>
          <div class="vs-deal-headline">Want useful Vegas show updates?</div>
          <div class="vs-deal-form" id="vsDealForm">
            <input type="email" class="vs-deal-input" id="vsDealInput" placeholder="your@email.com" autocomplete="email" aria-label="Email address">
            <button class="vs-deal-btn" type="button" onclick="vsDealSubmit()">Join Spike's list</button>
          </div>
          <div class="vs-deal-success" id="vsDealSuccess">You're in — Spike's on it. 🌵</div>
          <div class="vs-deal-tagline">Show changes, openings and useful Vegas deals.</div>
          <button class="vs-deal-skip" type="button" onclick="vsDealClose()">No thanks</button>
        </div>
      </div>`;
    document.body.insertAdjacentHTML('beforeend',overlayHTML);
    const backdrop = document.querySelector('#vs-deal-overlay .vs-deal-backdrop');
    if (backdrop) backdrop.addEventListener('click',window.vsDealClose);
    document.addEventListener('click',function(e){
      if (localStorage.getItem(STORAGE_KEY)) return;
      const link = e.target.closest && e.target.closest('a[href*="spotlight.vegas"]');
      if (!link) return;
      e.preventDefault();
      window.open(link.href,'_blank','noopener,noreferrer');
      setTimeout(function(){const overlay=document.getElementById('vs-deal-overlay');if(overlay)overlay.classList.add('visible');},180);
    },true);
  }

  window.vsDealClose = function () {
    const overlay = document.getElementById('vs-deal-overlay');
    if (overlay) overlay.classList.remove('visible');
  };

  window.vsDealSubmit = async function () {
    const input = document.getElementById('vsDealInput');
    const val = input ? input.value.trim() : '';
    if (!val || !val.includes('@') || !val.includes('.')) {
      if (input) { input.style.borderColor='#ff2e7e'; setTimeout(function(){input.style.borderColor='';},1600); }
      return;
    }
    try {
      const response = await fetch(WORKER_URL,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:val})});
      if (!response.ok) throw new Error('subscribe failed');
      localStorage.setItem('vs_deal_alert_captured','1');
      const form=document.getElementById('vsDealForm');
      const success=document.getElementById('vsDealSuccess');
      if(form)form.style.display='none';
      if(success)success.classList.add('visible');
      setTimeout(window.vsDealClose,2200);
    } catch(err) {
      if (input) { input.style.borderColor='#ff2e7e'; }
    }
  };

  if (!document.getElementById('vs-fontlink')) {
    const font = document.createElement('link');
    font.id='vs-fontlink';font.rel='stylesheet';font.href='https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap';
    document.head.appendChild(font);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded',mountFooter);
  else mountFooter();
})();