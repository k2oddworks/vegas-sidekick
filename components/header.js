// Vegas Sidekick — Shared Header Component
// v18 — dedicated cropped header asset to avoid stale padded-logo cache
(function () {
  'use strict';

  const html = `
<nav id="vs-nav" aria-label="Primary navigation">
  <div class="vs-announce">&#127917; Real Vegas show savings, when the numbers support them &mdash; <span>compare current deals</span></div>
  <div class="vs-nav-row">
    <a class="nav-logo" href="/" aria-label="Vegas Sidekick home"><img src="/images/logo-horizontal-header.png" alt="Vegas Sidekick" width="841" height="144" loading="eager" fetchpriority="high" decoding="async"></a>

    <div class="nav-desktop">
      <div class="nav-dropdown-wrap">
        <button class="nav-link-btn" id="vsShowsButton" type="button" aria-expanded="false" aria-controls="vsShowsMenu" onclick="vsToggleShowsDropdown(event)">Shows <span class="nav-chevron" aria-hidden="true">&#8964;</span></button>
        <div class="nav-dropdown" id="vsShowsMenu" role="menu" aria-label="Show categories">
          <div class="nav-dropdown-grid">
            <a href="/shows/comedy/" role="menuitem"><span class="nav-dot dot-pink"></span><span><b>Comedy</b><small>Stand-up and headliners</small></span></a>
            <a href="/shows/magic/" role="menuitem"><span class="nav-dot dot-purple"></span><span><b>Magic</b><small>Illusions and mentalism</small></span></a>
            <a href="/shows/cirque/" role="menuitem"><span class="nav-dot dot-blue"></span><span><b>Cirque &amp; Acrobatic</b><small>Big visual productions</small></span></a>
            <a href="/shows/music/" role="menuitem"><span class="nav-dot dot-teal"></span><span><b>Music &amp; Variety</b><small>Concert-style Vegas shows</small></span></a>
            <a href="/shows/spectaculars/" role="menuitem"><span class="nav-dot dot-gold"></span><span><b>Spectaculars</b><small>Large-scale Vegas productions</small></span></a>
            <a href="/shows/family/" role="menuitem"><span class="nav-dot dot-sky"></span><span><b>Family Shows</b><small>Good picks with kids</small></span></a>
            <a href="/shows/adult/" role="menuitem"><span class="nav-dot dot-rose"></span><span><b>Adult Shows</b><small>18+ and late-night options</small></span></a>
            <a href="/shows/" role="menuitem" class="dropdown-all"><span class="nav-dot dot-lime"></span><span><b>All Shows</b><small>Browse everything</small></span><span class="dropdown-arrow">&#8594;</span></a>
          </div>
        </div>
      </div>
      <a class="nav-text-link nav-deals" href="/shows/deals/">Deals</a>
      <a class="nav-text-link nav-guides" href="/guides/">Guides</a>
      <a class="nav-text-link nav-dispatch" href="/news/">Vegas Dispatch</a>
    </div>

    <span class="nav-spacer"></span>

    <div class="nav-search-wrap">
      <button class="nav-search-btn" id="vsDesktopSearchButton" type="button" aria-label="Search Vegas Sidekick" aria-expanded="false" onclick="vsToggleDesktopSearch(event)">&#128269;</button>
      <form class="nav-search-popover" id="vsDesktopSearch" role="search" onsubmit="return vsDesktopSearch(event)">
        <label class="sr-only" for="vsDesktopSearchInput">Search shows</label>
        <input id="vsDesktopSearchInput" type="search" placeholder="Search shows&hellip;" autocomplete="off">
        <button type="submit">Search</button>
      </form>
    </div>

    <a href="/shows/" class="nav-cta">All Shows</a>
    <button class="nav-mobile-menu" id="vsMobileMenuButton" type="button" onclick="vsToggleMenu()" aria-label="Open menu" aria-expanded="false" aria-controls="vsMobileDrawer">&#9776;</button>
  </div>
</nav>

<div class="nav-mobile-drawer" id="vsMobileDrawer" aria-hidden="true">
  <button class="drawer-x" type="button" onclick="vsToggleMenu()" aria-label="Close menu">&times;</button>

  <form class="drawer-search" role="search" onsubmit="return vsMobileSearch(event)">
    <label class="sr-only" for="vsDrawerSearch">Search shows</label>
    <input id="vsDrawerSearch" type="search" name="q" placeholder="Search shows&hellip;" autocomplete="off">
    <button type="submit" aria-label="Search">&#128269;</button>
  </form>

  <div class="drawer-priority" aria-label="Popular destinations">
    <a href="/shows/" class="drawer-primary primary-all"><span>&#127915;</span> All Shows <b>&#8594;</b></a>
    <a href="/shows/deals/" class="drawer-primary primary-deals"><span>&#128176;</span> Current Show Deals</a>
    <a href="/guides/" class="drawer-primary primary-guides"><span>&#128214;</span> Guides</a>
  </div>

  <div class="drawer-section-label">Browse by show type</div>
  <div class="drawer-categories">
    <a href="/shows/comedy/" class="cat-comedy"><span class="cat-icon">&#9786;</span> Comedy <span class="cat-arrow">&#8594;</span></a>
    <a href="/shows/magic/" class="cat-magic"><span class="cat-icon">&#10024;</span> Magic <span class="cat-arrow">&#8594;</span></a>
    <a href="/shows/cirque/" class="cat-cirque"><span class="cat-icon">&#9670;</span> Cirque &amp; Acrobatic <span class="cat-arrow">&#8594;</span></a>
    <a href="/shows/music/" class="cat-music"><span class="cat-icon">&#9835;</span> Music &amp; Variety <span class="cat-arrow">&#8594;</span></a>
    <a href="/shows/spectaculars/" class="cat-spectacular"><span class="cat-icon">&#9733;</span> Spectaculars <span class="cat-arrow">&#8594;</span></a>
    <a href="/shows/family/" class="cat-family"><span class="cat-icon">&#9788;</span> Family Shows <span class="cat-arrow">&#8594;</span></a>
    <a href="/shows/adult/" class="cat-adult"><span class="cat-icon">&#9829;</span> Adult Shows <span class="cat-arrow">&#8594;</span></a>
  </div>

  <div class="drawer-divider"></div>
  <a href="/news/" class="drawer-dispatch"><span>&#128240;</span><span><b>Vegas Dispatch</b><small>What changed, what opened, what matters</small></span><span class="cat-arrow">&#8594;</span></a>
</div>
<div class="nav-overlay" id="vsNavOverlay" onclick="vsToggleMenu()"></div>`;

  const styles = `
<style>
#vs-nav{position:fixed;top:0;left:0;right:0;z-index:200;font-family:'Inter',sans-serif}
#vs-nav *,.nav-mobile-drawer *{box-sizing:border-box}
.sr-only{position:absolute!important;width:1px!important;height:1px!important;padding:0!important;margin:-1px!important;overflow:hidden!important;clip:rect(0,0,0,0)!important;white-space:nowrap!important;border:0!important}
.vs-announce{background:#12061f;color:#efe9ff;text-align:center;font-size:.8rem;font-weight:500;line-height:1;padding:8px 16px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.vs-announce span{color:#FFB000;font-weight:700}
.vs-nav-row{position:relative;display:flex;align-items:center;gap:20px;height:56px;padding:0 40px;background:rgba(20,8,40,.94);backdrop-filter:saturate(160%) blur(14px)}
.vs-nav-row::after{content:'';position:absolute;left:0;right:0;bottom:0;height:2px;background:linear-gradient(90deg,#ff2e7e 0%,#7c3aed 42%,#0fb5c9 70%,#c6f22e 100%);opacity:.95}
.nav-logo{display:flex;align-items:center;flex:0 0 auto;text-decoration:none;line-height:0}
.nav-logo img{display:block;width:auto;height:40px;max-width:240px;object-fit:contain}
.nav-desktop{display:flex;align-items:center;gap:6px}
.nav-text-link,.nav-link-btn{appearance:none;border:0;background:transparent;color:rgba(255,255,255,.84);font:600 .9rem 'Inter',sans-serif;text-decoration:none;padding:10px 11px;border-radius:9px;cursor:pointer;transition:.18s;white-space:nowrap}
.nav-link-btn{display:flex;align-items:center;gap:5px}
.nav-chevron{font-size:.9rem;line-height:1;transform:translateY(-1px);transition:transform .18s}
.nav-link-btn[aria-expanded="true"] .nav-chevron{transform:rotate(180deg) translateY(1px)}
.nav-text-link:hover,.nav-link-btn:hover,.nav-link-btn[aria-expanded="true"]{color:#fff;background:rgba(255,255,255,.08)}
.nav-deals:hover{background:rgba(255,176,0,.16);color:#ffd46f}.nav-guides:hover{background:rgba(59,130,246,.18);color:#dceaff}.nav-dispatch:hover{background:rgba(15,181,201,.18);color:#d9fbff}
.nav-spacer{flex:1}
.nav-cta{display:inline-flex;align-items:center;background:#ff2e7e;color:#fff!important;font:700 .9rem 'Plus Jakarta Sans',sans-serif;text-decoration:none;padding:10px 20px;border-radius:100px;box-shadow:0 8px 20px rgba(255,46,126,.28);transition:.18s;white-space:nowrap}
.nav-cta:hover{background:#ff1f72;transform:translateY(-2px)}
.nav-mobile-menu{display:none;background:none;border:0;color:#fff;font-size:1.55rem;cursor:pointer;padding:4px 7px;line-height:1}

.nav-dropdown-wrap{position:relative}
.nav-dropdown{position:absolute;left:0;top:calc(100% + 10px);width:560px;padding:12px;background:rgba(20,8,40,.98);border:1px solid rgba(255,255,255,.11);border-radius:16px;box-shadow:0 22px 55px rgba(5,2,12,.38);opacity:0;visibility:hidden;transform:translateY(-8px);transition:.18s;z-index:240}
.nav-dropdown.open{opacity:1;visibility:visible;transform:none}
.nav-dropdown-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px}
.nav-dropdown a{display:flex;align-items:center;gap:11px;color:#fff;text-decoration:none;padding:12px;border-radius:11px;transition:.16s;min-width:0}
.nav-dropdown a:hover{background:rgba(255,255,255,.075)}
.nav-dropdown a b{display:block;font:700 .88rem 'Plus Jakarta Sans',sans-serif}
.nav-dropdown a small{display:block;color:#a99db5;font-size:.72rem;margin-top:2px}
.nav-dot{width:9px;height:9px;border-radius:50%;flex:0 0 9px;box-shadow:0 0 0 5px rgba(255,255,255,.04)}
.dot-pink{background:#ff2e7e}.dot-purple{background:#8b5cf6}.dot-blue{background:#4f8df7}.dot-teal{background:#16c6c3}.dot-gold{background:#f3b93f}.dot-sky{background:#52b7f6}.dot-rose{background:#f06292}.dot-lime{background:#c6f22e}
.dropdown-all{border:1px solid rgba(198,242,46,.18);background:rgba(198,242,46,.055)}
.dropdown-arrow{margin-left:auto;color:#c6f22e;font-size:1.15rem}

.nav-search-wrap{position:relative}
.nav-search-btn{display:grid;place-items:center;width:38px;height:38px;border:1px solid rgba(255,255,255,.12);border-radius:50%;background:rgba(255,255,255,.06);color:#fff;cursor:pointer;font-size:1rem;transition:.18s}
.nav-search-btn:hover,.nav-search-btn[aria-expanded="true"]{background:rgba(255,255,255,.13);border-color:rgba(255,255,255,.24)}
.nav-search-popover{position:absolute;right:0;top:calc(100% + 11px);width:340px;display:flex;gap:7px;padding:10px;background:#190a30;border:1px solid rgba(255,255,255,.12);border-radius:13px;box-shadow:0 18px 45px rgba(5,2,12,.35);opacity:0;visibility:hidden;transform:translateY(-6px);transition:.18s}
.nav-search-popover.open{opacity:1;visibility:visible;transform:none}
.nav-search-popover input{flex:1;min-width:0;border:1px solid #e5deeb;border-radius:9px;padding:10px 12px;font:500 .88rem Inter,sans-serif;outline:none;color:#171225;background:#fff}
.nav-search-popover input:focus{box-shadow:0 0 0 3px rgba(198,242,46,.2);border-color:#c6f22e}
.nav-search-popover button{border:0;border-radius:9px;background:#ff2e7e;color:#fff;font:700 .82rem 'Plus Jakarta Sans',sans-serif;padding:0 13px;cursor:pointer}

.nav-overlay{display:none;position:fixed;inset:0;background:rgba(6,3,14,.62);z-index:250;backdrop-filter:blur(2px)}
.nav-overlay.visible{display:block}
.nav-mobile-drawer{display:none;position:fixed;top:0;right:0;width:min(390px,91vw);height:100dvh;z-index:300;flex-direction:column;padding:18px 20px 28px;transform:translateX(100%);transition:transform .28s ease;overflow-y:auto;background:linear-gradient(180deg,#1c0a3a 0%,#12061f 100%);border-left:1px solid rgba(198,242,46,.14);box-shadow:-12px 0 40px rgba(10,4,26,.55)}
.nav-mobile-drawer.open{transform:none}
.drawer-x{align-self:flex-end;background:none;border:0;color:#fff;font-size:1.85rem;line-height:1;cursor:pointer;padding:2px 6px;margin:0 0 8px}
.drawer-search{display:flex;gap:7px;margin-bottom:14px}
.drawer-search input{flex:1;min-width:0;border:0;border-radius:11px;padding:13px 14px;font:500 1rem Inter,sans-serif;outline:none;color:#171225;background:#fff}
.drawer-search button{flex:0 0 54px;border:0;border-radius:11px;background:#ff2e7e;color:#fff;font-size:1.1rem;cursor:pointer}
.drawer-priority{display:grid;gap:9px;margin-bottom:21px}
.drawer-primary{display:flex;align-items:center;gap:9px;border-radius:11px;padding:14px 15px;color:#fff!important;text-decoration:none;font:800 .94rem 'Plus Jakarta Sans',sans-serif;letter-spacing:.015em;box-shadow:0 7px 20px rgba(0,0,0,.14);transition:.18s}
.drawer-primary:hover{transform:translateY(-1px);filter:brightness(1.06)}
.drawer-primary b{margin-left:auto;font-size:1.1rem}.primary-all{background:#ff2e7e}.primary-deals{background:#FFB000!important;color:#171225!important;border-left:3px solid #ffd46f}.primary-guides{background:#3b82f6}
.drawer-section-label{color:#a99db5;font:700 .66rem 'Plus Jakarta Sans',sans-serif;text-transform:uppercase;letter-spacing:.14em;margin:0 3px 8px}
.drawer-categories{display:grid;gap:7px}
.drawer-categories a{--accent:#fff;--tint:rgba(255,255,255,.05);display:flex;align-items:center;gap:10px;color:rgba(255,255,255,.92);text-decoration:none;font:700 .88rem 'Plus Jakarta Sans',sans-serif;letter-spacing:.025em;padding:12px 12px;border:1px solid rgba(255,255,255,.07);border-left:3px solid var(--accent);border-radius:10px;background:var(--tint);transition:.16s}
.drawer-categories a:hover{transform:translateX(2px);border-color:rgba(255,255,255,.15)}
.cat-icon{display:grid;place-items:center;width:23px;color:var(--accent);font-size:.92rem}.cat-arrow{margin-left:auto;color:rgba(255,255,255,.45)}
.cat-comedy{--accent:#ff5a91!important;--tint:rgba(255,46,126,.09)!important}.cat-magic{--accent:#a879ff!important;--tint:rgba(124,58,237,.1)!important}.cat-cirque{--accent:#6b9cff!important;--tint:rgba(59,130,246,.09)!important}.cat-music{--accent:#39d1cb!important;--tint:rgba(15,181,201,.09)!important}.cat-spectacular{--accent:#f4bd4c!important;--tint:rgba(244,189,76,.08)!important}.cat-family{--accent:#66c8ff!important;--tint:rgba(82,183,246,.09)!important}.cat-adult{--accent:#f47da3!important;--tint:rgba(240,98,146,.09)!important}
.drawer-divider{height:1px;background:rgba(255,255,255,.11);margin:17px 0 12px}
.drawer-dispatch{display:flex;align-items:center;gap:11px;color:#fff!important;text-decoration:none;padding:13px 12px;border:1px solid rgba(15,181,201,.2);border-left:3px solid #0fb5c9;border-radius:10px;background:rgba(15,181,201,.09)}
.drawer-dispatch>span:first-child{font-size:1rem}.drawer-dispatch b{display:block;font:800 .88rem 'Plus Jakarta Sans',sans-serif}.drawer-dispatch small{display:block;color:#9fcbd0;font-size:.68rem;margin-top:2px}.drawer-dispatch .cat-arrow{margin-left:auto}

@media(max-width:980px){
  .vs-announce{display:none}
  .nav-desktop,.nav-search-wrap{display:none}
  .vs-nav-row{padding:0 20px;height:54px;gap:13px}
  .nav-mobile-menu{display:block}
  .nav-mobile-drawer{display:flex}
  .nav-cta{padding:9px 16px;font-size:.85rem}
}
@media(max-width:460px){.nav-logo img{height:36px;max-width:220px}.nav-cta{display:none}.vs-nav-row{padding:0 15px}}
@media(prefers-reduced-motion:reduce){.nav-dropdown,.nav-search-popover,.nav-mobile-drawer,.drawer-primary,.drawer-categories a,.nav-cta{transition:none!important}}
</style>`;

  const target = document.getElementById('vs-header');
  if (!target) return;
  target.innerHTML = styles + html;

  if (!document.getElementById('vs-fontlink')) {
    const fontLink = document.createElement('link');
    fontLink.id = 'vs-fontlink';
    fontLink.rel = 'stylesheet';
    fontLink.href = 'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap';
    document.head.appendChild(fontLink);
  }

  // Keep favicon consistent without shipping a large inline image in every header request.
  (function () {
    let favicon = document.querySelector("link[rel~='icon']");
    if (!favicon) {
      favicon = document.createElement('link');
      favicon.rel = 'icon';
      document.head.appendChild(favicon);
    }
    favicon.type = 'image/png';
    favicon.href = '/favicon.png';
  })();

  window.vsToggleMenu = function () {
    const drawer = document.getElementById('vsMobileDrawer');
    const overlay = document.getElementById('vsNavOverlay');
    const button = document.getElementById('vsMobileMenuButton');
    if (!drawer || !overlay) return;
    const opening = !drawer.classList.contains('open');
    drawer.classList.toggle('open', opening);
    overlay.classList.toggle('visible', opening);
    drawer.setAttribute('aria-hidden', opening ? 'false' : 'true');
    if (button) {
      button.setAttribute('aria-expanded', opening ? 'true' : 'false');
      button.setAttribute('aria-label', opening ? 'Close menu' : 'Open menu');
    }
    document.documentElement.style.overflow = opening ? 'hidden' : '';
    if (opening) setTimeout(function () { const input = document.getElementById('vsDrawerSearch'); if (input) input.focus({preventScroll:true}); }, 120);
  };

  window.vsMobileSearch = function (e) {
    if (e) e.preventDefault();
    const input = document.getElementById('vsDrawerSearch');
    const q = input ? input.value.trim() : '';
    window.location.href = '/search/' + (q ? '?q=' + encodeURIComponent(q) : '');
    return false;
  };

  window.vsDesktopSearch = function (e) {
    if (e) e.preventDefault();
    const input = document.getElementById('vsDesktopSearchInput');
    const q = input ? input.value.trim() : '';
    window.location.href = '/search/' + (q ? '?q=' + encodeURIComponent(q) : '');
    return false;
  };

  window.vsToggleShowsDropdown = function (e) {
    if (e) e.stopPropagation();
    const menu = document.getElementById('vsShowsMenu');
    const button = document.getElementById('vsShowsButton');
    const search = document.getElementById('vsDesktopSearch');
    const searchButton = document.getElementById('vsDesktopSearchButton');
    if (!menu || !button) return;
    const opening = !menu.classList.contains('open');
    menu.classList.toggle('open', opening);
    button.setAttribute('aria-expanded', opening ? 'true' : 'false');
    if (search) search.classList.remove('open');
    if (searchButton) searchButton.setAttribute('aria-expanded', 'false');
  };

  window.vsToggleDesktopSearch = function (e) {
    if (e) e.stopPropagation();
    const search = document.getElementById('vsDesktopSearch');
    const button = document.getElementById('vsDesktopSearchButton');
    const menu = document.getElementById('vsShowsMenu');
    const showsButton = document.getElementById('vsShowsButton');
    if (!search || !button) return;
    const opening = !search.classList.contains('open');
    search.classList.toggle('open', opening);
    button.setAttribute('aria-expanded', opening ? 'true' : 'false');
    if (menu) menu.classList.remove('open');
    if (showsButton) showsButton.setAttribute('aria-expanded', 'false');
    if (opening) setTimeout(function () { const input = document.getElementById('vsDesktopSearchInput'); if (input) input.focus(); }, 60);
  };

  document.addEventListener('click', function (e) {
    const menu = document.getElementById('vsShowsMenu');
    const showsButton = document.getElementById('vsShowsButton');
    const search = document.getElementById('vsDesktopSearch');
    const searchButton = document.getElementById('vsDesktopSearchButton');
    if (menu && !menu.contains(e.target) && e.target !== showsButton) {
      menu.classList.remove('open');
      if (showsButton) showsButton.setAttribute('aria-expanded', 'false');
    }
    if (search && !search.contains(e.target) && e.target !== searchButton) {
      search.classList.remove('open');
      if (searchButton) searchButton.setAttribute('aria-expanded', 'false');
    }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    const drawer = document.getElementById('vsMobileDrawer');
    if (drawer && drawer.classList.contains('open')) window.vsToggleMenu();
    const menu = document.getElementById('vsShowsMenu');
    const showsButton = document.getElementById('vsShowsButton');
    const search = document.getElementById('vsDesktopSearch');
    const searchButton = document.getElementById('vsDesktopSearchButton');
    if (menu) menu.classList.remove('open');
    if (search) search.classList.remove('open');
    if (showsButton) showsButton.setAttribute('aria-expanded', 'false');
    if (searchButton) searchButton.setAttribute('aria-expanded', 'false');
  });

  // Google Analytics — injected once via shared header.
  if (!document.querySelector('script[src*="googletagmanager.com/gtag/js?id=G-BM6QGF7B4Y"]')) {
    const gtagScript = document.createElement('script');
    gtagScript.async = true;
    gtagScript.src = 'https://www.googletagmanager.com/gtag/js?id=G-BM6QGF7B4Y';
    document.head.appendChild(gtagScript);
  }
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  window.gtag('js', new Date());
  window.gtag('config', 'G-BM6QGF7B4Y');
})();