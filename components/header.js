// Vegas Sidekick — Shared Header Component
// v15 — priority navigation + canonical show runtime loader
(function () {
  'use strict';

  const html = `
<nav id="vs-nav" aria-label="Primary navigation">
  <div class="vs-announce">&#127917; Your Vegas adventure costs less here &mdash; <span>save up to 55% on select shows</span></div>
  <div class="vs-nav-row">
    <a class="nav-logo" href="/" aria-label="Vegas Sidekick home">vegas <span class="sk">sidekick</span></a>

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
      <a class="nav-text-link nav-deals" href="/guides/best-cheap-vegas-shows/">Deals</a>
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
    <a href="/guides/best-cheap-vegas-shows/" class="drawer-primary primary-deals"><span>&#127797;</span> Deals Under $50</a>
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
.vs-announce span{color:#c6f22e;font-weight:700}
.vs-nav-row{position:relative;display:flex;align-items:center;gap:20px;height:56px;padding:0 40px;background:rgba(20,8,40,.94);backdrop-filter:saturate(160%) blur(14px)}
.vs-nav-row::after{content:'';position:absolute;left:0;right:0;bottom:0;height:2px;background:linear-gradient(90deg,#ff2e7e 0%,#7c3aed 42%,#0fb5c9 70%,#c6f22e 100%);opacity:.95}
.nav-logo{font-family:'Plus Jakarta Sans',sans-serif;font-weight:800;font-size:1.26rem;letter-spacing:-.03em;text-decoration:none;color:#fff;white-space:nowrap}
.nav-logo .sk{color:#ff2e7e}
.nav-desktop{display:flex;align-items:center;gap:6px}
.nav-text-link,.nav-link-btn{appearance:none;border:0;background:transparent;color:rgba(255,255,255,.84);font:600 .9rem 'Inter',sans-serif;text-decoration:none;padding:10px 11px;border-radius:9px;cursor:pointer;transition:.18s;white-space:nowrap}
.nav-link-btn{display:flex;align-items:center;gap:5px}
.nav-chevron{font-size:.9rem;line-height:1;transform:translateY(-1px);transition:transform .18s}
.nav-link-btn[aria-expanded="true"] .nav-chevron{transform:rotate(180deg) translateY(1px)}
.nav-text-link:hover,.nav-link-btn:hover,.nav-link-btn[aria-expanded="true"]{color:#fff;background:rgba(255,255,255,.08)}
.nav-deals:hover{background:rgba(124,58,237,.2);color:#e9ddff}.nav-guides:hover{background:rgba(59,130,246,.18);color:#dceaff}.nav-dispatch:hover{background:rgba(15,181,201,.18);color:#d9fbff}
.nav-spacer{flex:1}
.nav-cta{display:inline-flex;align-items:center;background:#ff2e7e;color:#fff!important;font:700 .9rem 'Plus Jakarta Sans',sans-serif;text-decoration:none;padding:10px 20px;border-radius:100px;box-shadow:0 8px 20px rgba(255,46,126,.28);transition:.18s;white-space:nowrap}
.nav-cta:hover{background:#ff1f72;transform:translateY(-2px)}
.nav-mobile-menu{display:none;background:none;border:0;color:#fff;font-size:1.55rem;cursor:pointer;padding:4px 7px;line-height:1}
.nav-dropdown-wrap{position:relative}.nav-dropdown{position:absolute;left:0;top:calc(100% + 10px);width:560px;padding:12px;background:rgba(20,8,40,.98);border:1px solid rgba(255,255,255,.11);border-radius:16px;box-shadow:0 22px 55px rgba(5,2,12,.38);opacity:0;visibility:hidden;transform:translateY(-8px);transition:.18s;z-index:240}.nav-dropdown.open{opacity:1;visibility:visible;transform:none}.nav-dropdown-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px}.nav-dropdown a{display:flex;align-items:center;gap:11px;color:#fff;text-decoration:none;padding:12px;border-radius:11px;transition:.16s;min-width:0}.nav-dropdown a:hover{background:rgba(255,255,255,.075)}.nav-dropdown a b{display:block;font:700 .88rem 'Plus Jakarta Sans',sans-serif}.nav-dropdown a small{display:block;color:#a99db5;font-size:.72rem;margin-top:2px}.nav-dot{width:9px;height:9px;border-radius:50%;flex:0 0 9px;box-shadow:0 0 0 5px rgba(255,255,255,.04)}.dot-pink{background:#ff2e7e}.dot-purple{background:#8b5cf6}.dot-blue{background:#4f8df7}.dot-teal{background:#16c6c3}.dot-gold{background:#f3b93f}.dot-sky{background:#52b7f6}.dot-rose{background:#f06292}.dot-lime{background:#c6f22e}.dropdown-all{border:1px solid rgba(198,242,46,.18);background:rgba(198,242,46,.055)}.dropdown-arrow{margin-left:auto;color:#c6f22e;font-size:1.15rem}
.nav-search-wrap{position:relative}.nav-search-btn{display:grid;place-items:center;width:38px;height:38px;border:1px solid rgba(255,255,255,.12);border-radius:50%;background:rgba(255,255,255,.06);color:#fff;cursor:pointer;font-size:1rem;transition:.18s}.nav-search-btn:hover,.nav-search-btn[aria-expanded="true"]{background:rgba(255,255,255,.13);border-color:rgba(255,255,255,.24)}.nav-search-popover{position:absolute;right:0;top:calc(100% + 11px);width:340px;display:flex;gap:7px;padding:10px;background:#190a30;border:1px solid rgba(255,255,255,.12);border-radius:13px;box-shadow:0 18px 45px rgba(5,2,12,.35);opacity:0;visibility:hidden;transform:translateY(-6px);transition:.18s}.nav-search-popover.open{opacity:1;visibility:visible;transform:none}.nav-search-popover input{flex:1;min-width:0;border:1px solid #e5deeb;border-radius:9px;padding:10px 12px;font:500 .88rem Inter,sans-serif;outline:none;color:#171225;background:#fff}.nav-search-popover input:focus{box-shadow:0 0 0 3px rgba(198,242,46,.2);border-color:#c6f22e}.nav-search-popover button{border:0;border-radius:9px;background:#ff2e7e;color:#fff;font:700 .82rem 'Plus Jakarta Sans',sans-serif;padding:0 13px;cursor:pointer}
.nav-overlay{display:none;position:fixed;inset:0;background:rgba(6,3,14,.62);z-index:250;backdrop-filter:blur(2px)}.nav-overlay.visible{display:block}.nav-mobile-drawer{display:none;position:fixed;top:0;right:0;width:min(390px,91vw);height:100dvh;z-index:300;flex-direction:column;padding:18px 20px 28px;transform:translateX(100%);transition:transform .28s ease;overflow-y:auto;background:linear-gradient(180deg,#1c0a3a 0%,#12061f 100%);border-left:1px solid rgba(198,242,46,.14);box-shadow:-12px 0 40px rgba(10,4,26,.55)}.nav-mobile-drawer.open{transform:none}.drawer-x{align-self:flex-end;background:none;border:0;color:#fff;font-size:1.85rem;line-height:1;cursor:pointer;padding:2px 6px;margin:0 0 8px}.drawer-search{display:flex;gap:7px;margin-bottom:14px}.drawer-search input{flex:1;min-width:0;border:0;border-radius:11px;padding:13px 14px;font:500 1rem Inter,sans-serif;outline:none;color:#171225;background:#fff}.drawer-search button{flex:0 0 54px;border:0;border-radius:11px;background:#ff2e7e;color:#fff;font-size:1.1rem;cursor:pointer}.drawer-priority{display:grid;gap:9px;margin-bottom:21px}.drawer-primary{display:flex;align-items:center;gap:9px;border-radius:11px;padding:14px 15px;color:#fff!important;text-decoration:none;font:800 .94rem 'Plus Jakarta Sans',sans-serif;letter-spacing:.015em;box-shadow:0 7px 20px rgba(0,0,0,.14);transition:.18s}.drawer-primary:hover{transform:translateY(-1px);filter:brightness(1.06)}.drawer-primary b{margin-left:auto;font-size:1.1rem}.primary-all{background:#ff2e7e}.primary-deals{background:#7c3aed;border-left:3px solid #c6f22e}.primary-guides{background:#3b82f6}.drawer-section-label{color:#a99db5;font:700 .66rem 'Plus Jakarta Sans',sans-serif;text-transform:uppercase;letter-spacing:.14em;margin:0 3px 8px}.drawer-categories{display:grid;gap:5px}.drawer-categories a,.drawer-dispatch{display:flex;align-items:center;gap:11px;padding:12px 13px;border-radius:10px;text-decoration:none;color:#f7f3ff;font:700 .88rem Inter,sans-serif;transition:.16s}.drawer-categories a:hover,.drawer-dispatch:hover{background:rgba(255,255,255,.07)}.cat-icon{width:27px;text-align:center;font-size:1rem}.cat-arrow{margin-left:auto;color:#a99db5}.cat-comedy .cat-icon{color:#ff6a9f}.cat-magic .cat-icon{color:#a987ff}.cat-cirque .cat-icon{color:#6ca7ff}.cat-music .cat-icon{color:#35d8d2}.cat-spectacular .cat-icon{color:#ffd063}.cat-family .cat-icon{color:#7ed4ff}.cat-adult .cat-icon{color:#ff82ac}.drawer-divider{height:1px;background:rgba(255,255,255,.1);margin:16px 0 10px}.drawer-dispatch{align-items:flex-start;border:1px solid rgba(15,181,201,.15);background:rgba(15,181,201,.055)}.drawer-dispatch>span:first-child{font-size:1rem}.drawer-dispatch b{display:block;color:#8feaf2}.drawer-dispatch small{display:block;color:#a99db5;font-size:.7rem;margin-top:2px;font-weight:500}
@media(max-width:980px){.nav-desktop{display:none}.nav-mobile-menu{display:block}.nav-mobile-drawer{display:flex}.vs-nav-row{height:54px;padding:0 17px;gap:12px}.nav-cta{padding:9px 14px;font-size:.82rem}.nav-search-wrap{display:none}.vs-announce{font-size:.72rem;padding:7px 12px}.nav-logo{font-size:1.12rem}}
</style>`;

  const mount = document.getElementById('vs-header');
  if (mount) {
    mount.insertAdjacentHTML('beforebegin', styles);
    mount.innerHTML = html;
  } else {
    document.body.insertAdjacentHTML('afterbegin', styles + html);
  }

  window.vsToggleMenu = function () {
    const drawer = document.getElementById('vsMobileDrawer');
    const overlay = document.getElementById('vsNavOverlay');
    const btn = document.getElementById('vsMobileMenuButton');
    if (!drawer || !overlay || !btn) return;
    const opening = !drawer.classList.contains('open');
    drawer.classList.toggle('open', opening);
    overlay.classList.toggle('visible', opening);
    drawer.setAttribute('aria-hidden', opening ? 'false' : 'true');
    btn.setAttribute('aria-expanded', opening ? 'true' : 'false');
  };

  window.vsToggleShowsDropdown = function (event) {
    if (event) event.stopPropagation();
    const menu = document.getElementById('vsShowsMenu');
    const btn = document.getElementById('vsShowsButton');
    if (!menu || !btn) return;
    const open = !menu.classList.contains('open');
    menu.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  };

  window.vsToggleDesktopSearch = function (event) {
    if (event) event.stopPropagation();
    const form = document.getElementById('vsDesktopSearch');
    const btn = document.getElementById('vsDesktopSearchButton');
    if (!form || !btn) return;
    const open = !form.classList.contains('open');
    form.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (open) setTimeout(() => document.getElementById('vsDesktopSearchInput')?.focus(), 20);
  };

  window.vsDesktopSearch = function () {
    const q = document.getElementById('vsDesktopSearchInput')?.value.trim();
    if (q) location.href = '/search/?q=' + encodeURIComponent(q);
    return false;
  };

  window.vsMobileSearch = function () {
    const q = document.getElementById('vsDrawerSearch')?.value.trim();
    if (q) location.href = '/search/?q=' + encodeURIComponent(q);
    return false;
  };

  document.addEventListener('click', function (e) {
    const dropdown = document.getElementById('vsShowsMenu');
    const dropdownWrap = document.querySelector('.nav-dropdown-wrap');
    if (dropdown?.classList.contains('open') && !dropdownWrap?.contains(e.target)) {
      dropdown.classList.remove('open');
      document.getElementById('vsShowsButton')?.setAttribute('aria-expanded', 'false');
    }
    const search = document.getElementById('vsDesktopSearch');
    const searchWrap = document.querySelector('.nav-search-wrap');
    if (search?.classList.contains('open') && !searchWrap?.contains(e.target)) {
      search.classList.remove('open');
      document.getElementById('vsDesktopSearchButton')?.setAttribute('aria-expanded', 'false');
    }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    const drawer = document.getElementById('vsMobileDrawer');
    if (drawer?.classList.contains('open')) window.vsToggleMenu();
    document.getElementById('vsShowsMenu')?.classList.remove('open');
    document.getElementById('vsShowsButton')?.setAttribute('aria-expanded', 'false');
    document.getElementById('vsDesktopSearch')?.classList.remove('open');
    document.getElementById('vsDesktopSearchButton')?.setAttribute('aria-expanded', 'false');
  });

  // Every show-detail page mounts the shared header. Load the canonical interaction
  // runtime here so benchmark pages and legacy templates get the same fact count-up,
  // schedule/FAQ behavior and fallback utility modules. Category indexes are excluded.
  const showDetail = /^\/shows\/(adult|cirque|comedy|family|magic|music|spectaculars)\/[^/]+\/?$/.test(location.pathname);
  if (showDetail && !document.querySelector('script[data-vs-show-runtime]')) {
    const runtime = document.createElement('script');
    runtime.src = '/components/show-page-runtime.js?v=2';
    runtime.defer = true;
    runtime.dataset.vsShowRuntime = '1';
    document.body.appendChild(runtime);
  }
})();
