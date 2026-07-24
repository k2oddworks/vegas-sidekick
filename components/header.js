// Vegas Sidekick — Header Component
// Drop <div id="vs-header"></div> at top of body + <script src="/components/header.js"></script>
// [connection test] 2026-07-12 v8 — fix UFO drift causing page-width jitter/fixed-button shift
(function() {
  const html = `
<nav id="vs-nav">
  <canvas id="vs-logo-orbs" style="position:absolute;left:0;top:0;width:100%;height:100%;pointer-events:none;z-index:0;"></canvas>
  <a class="nav-logo" href="/" style="position:relative;z-index:1;display:flex;align-items:center;text-decoration:none;"><img src="data:image/webp;base64,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" alt="" style="height:80px;width:auto;margin-right:8px;flex-shrink:0;"><span class="vs-logo-text"><span class="vs-lv">VEGAS</span><span class="vs-ls">SIDEKICK</span></span></a>
  <ul class="nav-links">
    <li><a href="/shows/comedy/">Comedy</a></li>
    <li><a href="/shows/magic/">Magic</a></li>
    <li><a href="/shows/cirque/">Cirque</a></li>
    <li><a href="/shows/music/">Music</a></li>
    <li><a href="/shows/family/">Family</a></li>
    <li><a href="/guides/">Guides</a></li>
    <li class="nav-more">
      <button class="nav-more-btn" aria-haspopup="true">MORE &#9660;</button>
      <div class="nav-more-menu">
        <a href="/shows/spectaculars/">Spectaculars</a>
        <a href="/shows/adult/">Adult Shows</a>
      </div>
    </li>
    <li><a href="/news/">Dispatch</a></li>
    <li><a href="/shows/" class="nav-cta">All Shows →</a></li>
  </ul>
  <div class="nav-mobile-right">
    <a class="nav-mobile-tickets" href="/shows/">🎟 All Shows</a>
    <button class="nav-mobile-menu" onclick="vsToggleMenu()" aria-label="Menu">☰</button>
  </div>
</nav>
<div class="nav-mobile-drawer" id="vsMobileDrawer">
  <form class="drawer-search" role="search" onsubmit="return vsMobileSearch(event)">
    <input id="vsDrawerSearch" type="search" name="q" placeholder="Search shows&hellip;" aria-label="Search shows" autocomplete="off" />
    <button type="submit" aria-label="Search">&#128269;</button>
  </form>
  <a href="/shows/comedy/">Comedy</a>
  <a href="/shows/magic/">Magic</a>
  <a href="/shows/cirque/">Cirque &amp; Acrobatic</a>
  <a href="/shows/music/">Music &amp; Variety</a>
  <a href="/shows/spectaculars/">Spectaculars</a>
  <a href="/shows/family/">Family Shows</a>
  <a href="/shows/adult/">Adult Shows</a>
  <a href="/guides/" class="mobile-drawer-guides">🌵 Guides</a>
  <a href="/news/" class="mobile-drawer-dispatch">Vegas Dispatch</a>
  <a href="/shows/" class="mobile-drawer-cta">All Shows →</a>
</div>
<div class="nav-overlay" id="vsNavOverlay" onclick="vsToggleMenu()"></div>
<div id="vs-memorial-banner" role="banner" aria-live="polite"></div>`;

  const styles = `
<style>
#vs-nav { position: fixed; top: 0; left: 0; right: 0; z-index: 200; display: flex; align-items: center; justify-content: space-between; padding: 10px 40px; background: rgba(10,22,40,0.95); backdrop-filter: blur(12px); }
#vs-nav::after { content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #FF6B2B 0%, #1A6BFF 100%); }
.nav-logo { display: flex !important; align-items: center; } .vs-logo-text { font-family: 'Barlow Condensed', sans-serif; font-weight: 800; font-size: 2.1rem; letter-spacing: .03em; text-transform: uppercase; line-height: 1; white-space: nowrap; } .vs-lv { color: #1A6BFF; } .vs-ls { color: #FF6B2B; }
.nav-links { display: flex; gap: 22px; list-style: none; align-items: center; }
.nav-links a { color: #D4DCE8; text-decoration: none; font-weight: 600; font-size: 0.85rem; letter-spacing: 1px; text-transform: uppercase; transition: color 0.2s; font-family: 'Barlow', sans-serif; }
.nav-links a:hover { color: #FF6B2B; }
.nav-cta { background: #FF6B2B !important; color: #0A1628 !important; padding: 8px 18px; border-radius: 4px; border: 2px solid #60A5FA; white-space: nowrap; }
.nav-mobile-right { display: none; align-items: center; gap: 8px; }
.nav-mobile-tickets { display: inline-block; background: #FF6B2B; color: #0A1628 !important; font-family: 'Barlow Condensed', 'Barlow', sans-serif; font-weight: 800; font-size: 0.78rem; letter-spacing: 1px; text-transform: uppercase; text-decoration: none; padding: 6px 12px; border-radius: 4px; border: 2px solid #60A5FA; white-space: nowrap; transition: background 0.2s; }
.nav-mobile-tickets:hover { background: #e85e22; }
.nav-mobile-menu { display: none; background: none; border: none; color: #D4DCE8; font-size: 1.6rem; cursor: pointer; padding: 4px 8px; }
.nav-mobile-drawer { display: none; position: fixed; top: 0; right: -280px; width: 280px; height: 100vh; background: #0D1F3C; z-index: 300; flex-direction: column; padding: 80px 32px 32px; gap: 8px; transition: right 0.3s ease; border-left: 1px solid rgba(26,127,232,0.2); overflow-y: auto; }
.nav-mobile-drawer.open { right: 0; }
.nav-mobile-drawer a { color: #D4DCE8; text-decoration: none; font-family: 'Barlow', sans-serif; font-weight: 600; font-size: 1rem; letter-spacing: 1px; text-transform: uppercase; padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.14); transition: color 0.2s; }
.nav-mobile-drawer a:hover { color: #FF6B2B; }
.drawer-search { display: flex; gap: 6px; margin-bottom: 8px; }
.drawer-search input { flex: 1; min-width: 0; background: #fff; border: 1.5px solid #fff; border-radius: 8px; padding: 10px 12px; color: #0A1628; font-family: 'Barlow', sans-serif; font-size: 0.95rem; outline: none; }
.drawer-search input::placeholder { color: #6b7280; }
.drawer-search input:focus { border-color: #60A5FA; box-shadow: 0 0 0 3px rgba(96,165,250,0.35); }
.drawer-search button { flex: 0 0 auto; background: #FF6B2B; color: #0A1628; border: none; border-radius: 8px; padding: 0 14px; font-size: 1rem; cursor: pointer; transition: background 0.2s; }
.drawer-search button:hover { background: #e85e22; }
.mobile-drawer-guides { background: #1A6BFF !important; border-left: 3px solid #60A5FA !important; padding: 12px !important; padding-left: 12px !important; color: #FFFFFF !important; margin-top: 4px; border-radius: 6px; border-bottom: none !important; box-shadow: 0 2px 10px rgba(26,107,255,0.35); }
.mobile-drawer-guides:hover { color: #FFFFFF !important; background: #2563EB !important; }
.mobile-drawer-dispatch { border-left: 3px solid #FF6B2B !important; padding-left: 12px !important; color: #FF8C2A !important; }
.mobile-drawer-dispatch:hover { color: #FFB347 !important; }
.mobile-drawer-cta { background: #FF6B2B !important; color: #0A1628 !important; text-align: center; border-radius: 6px; padding: 14px !important; border-bottom: none !important; margin-top: 8px; }
.nav-overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 250; }
.nav-overlay.visible { display: block; }
@media (max-width: 1240px) {
  #vs-nav { padding: 8px 20px; }
  .nav-logo img { height: 54px !important; } .vs-logo-text { font-size: 1.5rem; }
  .nav-links { display: none; }
  .nav-mobile-right { display: flex; }
  .nav-mobile-menu { display: block; }
  .nav-mobile-drawer { display: flex; }
}
#vs-memorial-banner { display: none; position: absolute; left: 0; right: 0; z-index: 199; background: linear-gradient(100deg, #050B18 0%, #0F3E9E 55%, #4D90F0 100%); box-shadow: 0 2px 14px rgba(0,0,0,0.4); overflow: visible; }
#vs-memorial-banner.vsm-visible { display: block; }
#vs-memorial-banner .vsm-clip { position: relative; overflow: hidden; padding: 7px 14px; }
#vs-memorial-banner .vsm-canvas { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; z-index: 1; }
#vs-memorial-banner .vsm-inner { position: relative; z-index: 2; display: flex; align-items: center; justify-content: space-between; gap: 14px; flex-wrap: nowrap; font-family: 'Barlow Condensed', 'Barlow', sans-serif; font-weight: 800; font-size: 0.8rem; letter-spacing: 0.3px; text-transform: uppercase; color: #fff; }
#vs-memorial-banner .vsm-msg { display: flex; align-items: center; gap: 8px; flex: 1 1 auto; min-width: 0; text-align: left; }
#vs-memorial-banner .vsm-text { white-space: normal; line-height: 1.25; display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 2; overflow: hidden; -webkit-text-stroke: 0.6px rgba(0,0,0,0.6); text-shadow: 0 1px 3px rgba(0,0,0,0.4); }
#vs-memorial-banner .vsm-icon { display: inline-block; flex-shrink: 0; font-size: 1.15em; line-height: 1; animation: vsmBob 2.4s ease-in-out infinite; filter: drop-shadow(0 1px 2px rgba(0,0,0,0.45)); }
#vs-memorial-banner .vsm-icon.vsm-icon-2 { animation-delay: 1.1s; }
@keyframes vsmBob { 0%, 100% { transform: translateY(0) rotate(0deg); } 50% { transform: translateY(-3px) rotate(-6deg); } }
#vs-memorial-banner .vsm-btn { display: inline-flex; align-items: center; gap: 6px; flex-shrink: 0; background: #FF6B2B; color: #0A1628; text-decoration: none; font-weight: 800; letter-spacing: 0.05em; padding: 7px 16px; border-radius: 100px; font-size: 0.78rem; white-space: nowrap; border: 2px solid rgba(255,255,255,0.9); box-shadow: 0 2px 8px rgba(0,0,0,0.3); transition: background 0.2s, transform 0.2s; }
#vs-memorial-banner .vsm-btn:hover { background: #ff7d40; transform: translateY(-1px); }

/* Floating UFO sprite — flashing lights + subtle laser beam */
#vs-memorial-banner .vsm-ufo { position: absolute; top: 30%; left: -50px; width: 36px; height: 30px; cursor: pointer; z-index: 3; animation: vsmUfoDrift 18s linear infinite; }
#vs-memorial-banner .vsm-ufo:hover, #vs-memorial-banner .vsm-ufo.vsm-paused { animation-play-state: paused; }
#vs-memorial-banner .vsm-ufo-body { font-size: 1.6rem; line-height: 1; text-align: center; filter: saturate(1.6) brightness(1.05) drop-shadow(0 0 7px rgba(255,107,43,1)) drop-shadow(0 0 14px rgba(255,107,43,0.7)); animation: vsmUfoWobble 3s ease-in-out infinite; }
#vs-memorial-banner .vsm-ufo-beam { position: absolute; left: 50%; top: 76%; width: 12px; height: 20px; transform: translateX(-50%); background: linear-gradient(to bottom, rgba(255,107,43,0.7), rgba(255,107,43,0)); clip-path: polygon(32% 0, 68% 0, 100% 100%, 0% 100%); animation: vsmBeamPulse 2.6s ease-in-out infinite; pointer-events: none; }
#vs-memorial-banner .vsm-ufo-light { position: absolute; width: 4px; height: 4px; border-radius: 50%; bottom: 6px; animation: vsmLightBlink 1.5s ease-in-out infinite; }
#vs-memorial-banner .vsm-ufo-light-1 { left: 2px; background: #A855F7; animation-delay: 0s; }
#vs-memorial-banner .vsm-ufo-light-2 { left: 16px; background: #22D3EE; animation-delay: 0.5s; }
#vs-memorial-banner .vsm-ufo-light-3 { right: 2px; background: #F472B6; animation-delay: 1s; }
@keyframes vsmUfoWobble { 0%, 100% { transform: translateY(0) rotate(0deg); } 50% { transform: translateY(-2px) rotate(4deg); } }
@keyframes vsmBeamPulse { 0%, 100% { opacity: 0.15; } 50% { opacity: 0.55; } }
@keyframes vsmLightBlink { 0%, 100% { opacity: 0.25; } 50% { opacity: 1; } }
@keyframes vsmUfoDrift { 0% { left: -50px; } 100% { left: calc(100% + 50px); } }

/* Spike email popover */
#vs-memorial-banner .vsm-popover { display: none; position: absolute; top: 100%; right: 16px; margin-top: 8px; background: #0A1628; border: 1px solid rgba(255,255,255,0.15); border-radius: 12px; padding: 16px; width: 250px; box-shadow: 0 14px 34px rgba(0,0,0,0.45); z-index: 250; text-align: left; text-transform: none; letter-spacing: normal; }
#vs-memorial-banner .vsm-popover.vsm-pop-open { display: block; }
#vs-memorial-banner .vsm-pop-close { position: absolute; top: 8px; right: 10px; background: none; border: none; color: rgba(255,255,255,0.5); font-size: 1.1rem; line-height: 1; cursor: pointer; padding: 2px; }
#vs-memorial-banner .vsm-pop-close:hover { color: #fff; }
#vs-memorial-banner .vsm-pop-msg { font-family: 'Barlow', sans-serif; font-weight: 600; font-size: 0.82rem; color: #fff; margin-bottom: 10px; padding-right: 14px; -webkit-text-stroke: 0; text-shadow: none; }
#vs-memorial-banner .vsm-pop-form { display: flex; flex-direction: column; gap: 8px; }
#vs-memorial-banner .vsm-pop-form input { font-family: 'Barlow', sans-serif; font-size: 0.8rem; padding: 8px 10px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.2); background: rgba(255,255,255,0.06); color: #fff; }
#vs-memorial-banner .vsm-pop-form input::placeholder { color: rgba(255,255,255,0.4); }
#vs-memorial-banner .vsm-pop-form button { font-family: 'Barlow Condensed', sans-serif; font-weight: 800; font-size: 0.78rem; letter-spacing: 0.05em; text-transform: uppercase; background: #FF6B2B; color: #0A1628; border: none; border-radius: 6px; padding: 8px; cursor: pointer; transition: background 0.2s; }
#vs-memorial-banner .vsm-pop-form button:hover { background: #ff7d40; }
#vs-memorial-banner .vsm-pop-success { display: none; font-family: 'Barlow', sans-serif; font-weight: 600; font-size: 0.82rem; color: #4ade80; -webkit-text-stroke: 0; text-shadow: none; }
#vs-memorial-banner .vsm-pop-success.vsm-show { display: block; }

@media (prefers-reduced-motion: reduce) { #vs-memorial-banner .vsm-icon, #vs-memorial-banner .vsm-ufo, #vs-memorial-banner .vsm-ufo-body, #vs-memorial-banner .vsm-ufo-beam, #vs-memorial-banner .vsm-ufo-light { animation: none; } }
@media (max-width: 900px) {
  #vs-memorial-banner .vsm-clip { padding: 6px 10px; }
  #vs-memorial-banner .vsm-inner { gap: 10px; font-size: 0.66rem; }
  #vs-memorial-banner .vsm-btn { font-size: 0.64rem; padding: 6px 13px; }
  #vs-memorial-banner .vsm-ufo { width: 28px; height: 24px; }
  #vs-memorial-banner .vsm-ufo-body { font-size: 1.25rem; }
}
@media (max-width: 480px) {
  #vs-memorial-banner .vsm-icon { display: none; }
  #vs-memorial-banner .vsm-inner { font-size: 0.6rem; gap: 8px; }
  #vs-memorial-banner .vsm-btn { padding: 6px 11px; font-size: 0.58rem; }
  #vs-memorial-banner .vsm-popover { right: 8px; width: 210px; }
}
.nav-more { position: relative; }
.nav-more-btn { background: none; border: none; color: #D4DCE8; font-weight: 600; font-size: 0.85rem; letter-spacing: 1px; text-transform: uppercase; cursor: pointer; font-family: 'Barlow', sans-serif; padding: 0; transition: color 0.2s; line-height: inherit; }
.nav-more:hover .nav-more-btn { color: #FF6B2B; }
.nav-more-menu { visibility: hidden; opacity: 0; position: absolute; top: calc(100% + 8px); left: 50%; transform: translateX(-50%); background: #0D1F3C; border: 1px solid rgba(255,255,255,0.12); border-radius: 8px; overflow: hidden; box-shadow: 0 8px 24px rgba(0,0,0,0.45); min-width: 172px; z-index: 300; transition: opacity 0.15s, visibility 0.15s; }
.nav-more:hover .nav-more-menu { visibility: visible; opacity: 1; }
.nav-more-menu a { display: block; padding: 11px 18px; color: #D4DCE8; text-decoration: none; font-family: 'Barlow', sans-serif; font-weight: 600; font-size: 0.82rem; letter-spacing: 1px; text-transform: uppercase; transition: color 0.2s, background 0.2s; border-bottom: 1px solid rgba(255,255,255,0.07); }
.nav-more-menu a:last-child { border-bottom: none; }
.nav-more-menu a:hover { color: #FF6B2B; background: rgba(255,107,43,0.07); }
</style>`;

  const target = document.getElementById('vs-header');
  if (target) {
    target.innerHTML = styles + html;
  }
  // Favicon — set once, applies to every page via this component
  (function() {
    var existing = document.querySelector("link[rel*='icon']");
    if (existing) existing.parentNode.removeChild(existing);
    var link = document.createElement('link');
    link.rel = 'icon';
    link.type = 'image/png';
    link.href = 'data:image/png;base64,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';
    document.head.appendChild(link);
  })();
  // Orb particles — bright intro on first session visit, fades to subtle on subsequent pages
  (function() {
    var canvas = document.getElementById('vs-logo-orbs');
    if (!canvas) return;
    var nav = document.getElementById('vs-nav');
    function resize() {
      canvas.width  = nav.offsetWidth  || 1200;
      canvas.height = nav.offsetHeight || 84;
    }
    resize();
    // sessionStorage: first visit this session gets bright intro, all other pages skip it
    var firstVisit = !sessionStorage.getItem('vsOrbs');
    sessionStorage.setItem('vsOrbs', '1');
    var introStart = firstVisit ? Date.now() : null;
    var HOLD = 1500;  // ms to hold bright before fading
    var FADE = 2000;  // ms to fade down to soft
    var cols = ['#1A6BFF','#FF6B2B','#3B7FFF','#FF8040'];
    var orbs = [];
    for (var i = 0; i < 4; i++) {
      var xMax = (canvas.width || 1200) * 0.34;
      var softOp = 0.13 + Math.random() * 0.12;
      orbs.push({
        x: Math.random() * xMax, y: Math.random() * canvas.height,
        r: 18 + Math.random() * 10,
        color: cols[i % cols.length],
        vx: (Math.random() - 0.5) * 0.21,
        vy: -0.15 - Math.random() * 0.21,
        op: firstVisit ? 0.55 : softOp,
        softOp: softOp,
        xMax: xMax
      });
    }
    var ctx = canvas.getContext('2d');
    function frame() {
      if (introStart) {
        var el = Date.now() - introStart;
        if (el >= HOLD + FADE) {
          for (var j = 0; j < orbs.length; j++) orbs[j].op = orbs[j].softOp;
          introStart = null;
        } else if (el >= HOLD) {
          var t = (el - HOLD) / FADE;
          t = t * t * (3 - 2 * t); // smooth-step easing
          for (var j = 0; j < orbs.length; j++)
            orbs[j].op = 0.55 + (orbs[j].softOp - 0.55) * t;
        }
      }
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      for (var i = 0; i < orbs.length; i++) {
        var o = orbs[i];
        var g = ctx.createRadialGradient(o.x, o.y, 0, o.x, o.y, o.r);
        g.addColorStop(0, o.color); g.addColorStop(1, 'rgba(0,0,0,0)');
        ctx.save(); ctx.globalAlpha = o.op; ctx.fillStyle = g;
        ctx.beginPath(); ctx.arc(o.x, o.y, o.r, 0, Math.PI * 2); ctx.fill();
        ctx.restore();
        o.x += o.vx; o.y += o.vy;
        if (o.y < -o.r * 2) { o.y = canvas.height + o.r; o.x = Math.random() * o.xMax; }
        if (o.x < 0) o.x = o.xMax;
        if (o.x > o.xMax) o.x = 0;
      }
      requestAnimationFrame(frame);
    }
    frame();
  })();


  window.vsToggleMenu = function() {
    const drawer = document.getElementById('vsMobileDrawer');
    const overlay = document.getElementById('vsNavOverlay');
    drawer.classList.toggle('open');
    overlay.classList.toggle('visible');
  };

  window.vsMobileSearch = function(e) {
    if (e) e.preventDefault();
    var input = document.getElementById('vsDrawerSearch');
    var q = input ? input.value.trim() : '';
    window.location.href = '/search/' + (q ? '?q=' + encodeURIComponent(q) : '');
    return false;
  };

  // Labor Day Weekend Advance Notice (PDT = UTC-7)
  // Shows through end of Labor Day 2026 (Mon Sept 7) — hides after midnight PDT Sept 8 (= 2026-09-08T07:00:00Z)
  (function() {
    var banner = document.getElementById('vs-memorial-banner');
    if (!banner) return;
    var EXPIRE = new Date('2026-09-08T07:00:00Z'); // midnight PDT end of Labor Day
    var now = new Date();
    if (now >= EXPIRE) return;

    banner.innerHTML =
      '<div class="vsm-clip">' +
        '<canvas class="vsm-canvas" id="vsmCanvas"></canvas>' +
        '<div class="vsm-inner">' +
          '<span class="vsm-msg">' +
            '<span class="vsm-icon">🧳</span>' +
            '<span class="vsm-text">Labor Day Weekend is coming and many shows sell out early. Be smart and book ahead.</span>' +
            '<span class="vsm-icon vsm-icon-2">🌵</span>' +
          '</span>' +
          '<a class="vsm-btn" href="/shows/">All Shows &#8594;</a>' +
        '</div>' +
        '<div class="vsm-ufo" id="vsmUfo" role="button" tabindex="0" aria-label="A friendly UFO passing by — click to say hi">' +
          '<div class="vsm-ufo-beam"></div>' +
          '<div class="vsm-ufo-body">🛸</div>' +
          '<span class="vsm-ufo-light vsm-ufo-light-1"></span>' +
          '<span class="vsm-ufo-light vsm-ufo-light-2"></span>' +
          '<span class="vsm-ufo-light vsm-ufo-light-3"></span>' +
        '</div>' +
      '</div>' +
      '<div class="vsm-popover" id="vsmPopover">' +
        '<button class="vsm-pop-close" id="vsmPopClose" aria-label="Close">&times;</button>' +
        '<div class="vsm-pop-msg" id="vsmPopMsg">&#127942; Psst — want Vegas deals before everyone else?</div>' +
        '<form class="vsm-pop-form" id="vsmPopForm">' +
          '<input type="email" id="vsmPopEmail" placeholder="you@email.com" required autocomplete="email">' +
          '<button type="submit">Join Spike\'s List</button>' +
        '</form>' +
        '<div class="vsm-pop-success" id="vsmPopSuccess">You\'re in — Spike says welcome! &#127796;</div>' +
      '</div>';
    banner.classList.add('vsm-visible');

    // Position banner right below the fixed nav and reserve room for it,
    // regardless of whether this page clears the nav via body padding-top
    // or via its own hero/first-section padding-top (both conventions exist
    // across the site's page templates).
    (function() {
      var nav = document.getElementById('vs-nav');
      function place() {
        var navHeight = nav ? nav.getBoundingClientRect().height : 84;
        banner.style.top = navHeight + 'px';
        var bannerHeight = banner.offsetHeight;
        var origPT = parseFloat(banner.getAttribute('data-orig-pt'));
        if (isNaN(origPT)) {
          origPT = parseFloat(window.getComputedStyle(document.body).paddingTop) || 0;
          banner.setAttribute('data-orig-pt', origPT);
        }
        document.body.style.setProperty('padding-top', (origPT + bannerHeight) + 'px', 'important');
      }
      place();
      window.addEventListener('resize', place);
    })();

    // Drifting orange flare/bubble canvas
    (function() {
      var canvas = document.getElementById('vsmCanvas');
      var clip = banner.querySelector('.vsm-clip');
      if (!canvas || !clip) return;
      function resize() {
        canvas.width = clip.offsetWidth || 1200;
        canvas.height = clip.offsetHeight || 50;
      }
      resize();
      window.addEventListener('resize', resize);
      var cols = ['#FF6B2B', '#FFA35C', '#FF8C42'];
      var flares = [];
      for (var i = 0; i < 5; i++) {
        flares.push({
          x: Math.random() * (canvas.width || 1200),
          y: Math.random() * (canvas.height || 50),
          r: 6 + Math.random() * 10,
          color: cols[i % cols.length],
          vx: 0.12 + Math.random() * 0.18,
          op: 0.14 + Math.random() * 0.16
        });
      }
      var ctx = canvas.getContext('2d');
      function frame() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for (var i = 0; i < flares.length; i++) {
          var f = flares[i];
          var g = ctx.createRadialGradient(f.x, f.y, 0, f.x, f.y, f.r);
          g.addColorStop(0, f.color);
          g.addColorStop(1, 'rgba(0,0,0,0)');
          ctx.save();
          ctx.globalAlpha = f.op;
          ctx.fillStyle = g;
          ctx.beginPath();
          ctx.arc(f.x, f.y, f.r, 0, Math.PI * 2);
          ctx.fill();
          ctx.restore();
          f.x += f.vx;
          if (f.x - f.r > canvas.width) {
            f.x = -f.r;
            f.y = Math.random() * canvas.height;
          }
        }
        requestAnimationFrame(frame);
      }
      frame();
    })();

    // UFO click-to-email popover
    (function() {
      var ufo = document.getElementById('vsmUfo');
      var popover = document.getElementById('vsmPopover');
      var closeBtn = document.getElementById('vsmPopClose');
      var form = document.getElementById('vsmPopForm');
      if (!ufo || !popover) return;

      function openPop() {
        popover.classList.add('vsm-pop-open');
        ufo.classList.add('vsm-paused');
      }
      function closePop() {
        popover.classList.remove('vsm-pop-open');
        ufo.classList.remove('vsm-paused');
      }
      function toggle(e) {
        e.preventDefault();
        if (popover.classList.contains('vsm-pop-open')) { closePop(); } else { openPop(); }
      }
      ufo.addEventListener('click', toggle);
      ufo.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') { toggle(e); }
      });
      closeBtn.addEventListener('click', closePop);

      form.addEventListener('submit', function(e) {
        e.preventDefault();
        var email = document.getElementById('vsmPopEmail').value.trim();
        if (!email || !email.includes('@')) return;
        var btn = form.querySelector('button');
        btn.disabled = true;
        btn.textContent = '...';
        fetch('https://brevo-subscribe.vegassidekickcom.workers.dev', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: email })
        }).catch(function() {}).then(function() {
          form.style.display = 'none';
          document.getElementById('vsmPopMsg').style.display = 'none';
          document.getElementById('vsmPopSuccess').classList.add('vsm-show');
          setTimeout(closePop, 2600);
        });
      });
    })();
  })();

  // Google Analytics — injected once via header, covers every page
  const gtagScript = document.createElement('script');
  gtagScript.async = true;
  gtagScript.src = 'https://www.googletagmanager.com/gtag/js?id=G-BM6QGF7B4Y';
  document.head.appendChild(gtagScript);

  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  window.gtag = gtag;
  gtag('js', new Date());
  gtag('config', 'G-BM6QGF7B4Y');

  // ---- Custom event tracking (site-wide via header) ----
  window.vsTrack = function(name, params){
    try { gtag('event', name, params || {}); } catch(e){}
  };

  // Best-effort show/page name for event context
  function vsShowName(){
    var h1 = document.querySelector('h1');
    var t = (h1 && h1.textContent.trim()) || document.title || '';
    return t.replace(/\s*[|–—-]\s*Vegas Sidekick.*$/i, '').trim().slice(0, 120);
  }

  // Delegated clicks: affiliate CTAs, search-result cards, seen widget, FAQ, seating, deal popup
  document.addEventListener('click', function(e){
    var t = e.target;
    if (!t || !t.closest) return;

    // 1) Affiliate ticket clicks (the money metric)
    var a = t.closest('a[href*="spotlight.vegas"]');
    if (a){
      var c = a.className || '';
      var loc = /hero-cta/.test(c) ? 'hero'
              : /sb-cta/.test(c) ? 'sidebar'
              : /mob-cta/.test(c) ? 'mobile_bar'
              : /final-cta-btn/.test(c) ? 'final_cta'
              : 'other';
      window.vsTrack('affiliate_click', { show: vsShowName(), cta_location: loc, link_url: a.href });
    }

    // 2) Search-result card clicks (search page)
    var hit = t.closest('.show-hit-card');
    if (hit){
      var ha = hit.tagName === 'A' ? hit : hit.querySelector('a');
      window.vsTrack('search_result_click', { link_url: ha ? ha.href : '' });
    }

    // 3) "Have you seen this show?" widget
    var seen = t.closest('.seen-btn');
    if (seen){
      window.vsTrack('seen_widget', { show: vsShowName(), answer: seen.classList.contains('seen-yes') ? 'yes' : 'no' });
    }

    // 4) FAQ open (fire only when it ends up open)
    var faqQ = t.closest('.faq-q');
    if (faqQ){
      var item = faqQ.closest('.faq-item');
      var qEl = faqQ.querySelector('.faq-q-text');
      setTimeout(function(){
        if (item && item.classList.contains('open')){
          window.vsTrack('faq_open', { show: vsShowName(), question: qEl ? qEl.textContent.trim().slice(0,120) : '' });
        }
      }, 0);
    }

    // 5) Seating-chart zone clicks
    var zone = t.closest('.seat-zone');
    if (zone){
      var lbl = (zone.getAttribute('aria-label') || '').split('—')[0].split(' - ')[0].trim();
      window.vsTrack('seating_zone', { show: vsShowName(), zone: lbl.slice(0,80) });
    }

    // 6) Deal-popup email signup (button, not a form submit)
    var dealBtn = t.closest('.vs-deal-btn');
    if (dealBtn){
      var di = document.getElementById('vsDealInput');
      if (di && di.value.trim()) window.vsTrack('email_signup', { form_location: 'deal_popup' });
    }
  }, true);

  // Email signups: any real <form> that contains an email field (footer, hero, article)
  document.addEventListener('submit', function(e){
    var f = e.target;
    if (f && f.querySelector && f.querySelector('input[type="email"]')){
      var id = (f.id || '').toLowerCase();
      var loc = /footer|vsemail/.test(id) ? 'footer'
              : /spikes|picks|hero/.test(id) ? 'homepage_hero'
              : /article|dispatch|news/.test(id) ? 'article'
              : 'other';
      window.vsTrack('email_signup', { form_location: loc });
    }
  }, true);

  // Search performed — fires on the /search results page (hero + drawer + direct all land here)
  (function(){
    var path = location.pathname.replace(/\/+$/, '');
    if (path === '/search' || path === '/search/index'){
      try {
        var q = (new URLSearchParams(location.search).get('q') || '').trim();
        if (q) window.vsTrack('search', { search_term: q.slice(0,120) });
      } catch(err){}
    }
  })();

})();
