// Vegas Sidekick — Header Component
// Drop <div id="vs-header"></div> at top of body + <script src="/components/header.js"></script>
// v13 — new brand header (dark theme for interior pages); GA + tracking + mobile menu preserved
(function() {
  const html = `
<nav id="vs-nav">
  <div class="vs-announce">&#127917; Your Vegas adventure costs less here &mdash; <span>save up to 55% on select shows</span></div>
  <div class="vs-nav-row">
    <a class="nav-logo" href="/">vegas <span class="sk">sidekick</span></a>
    <ul class="nav-links">
      <li><a href="/shows/">Shows</a></li>
      <li><a href="/guides/best-cheap-vegas-shows/">Deals</a></li>
      <li><a href="/news/">Vegas Dispatch</a></li>
    </ul>
    <span class="nav-spacer"></span>
    <a href="/shows/" class="nav-cta">Find deals</a>
    <button class="nav-mobile-menu" onclick="vsToggleMenu()" aria-label="Menu">&#9776;</button>
  </div>
</nav>
<div class="nav-mobile-drawer" id="vsMobileDrawer">
  <button class="drawer-x" onclick="vsToggleMenu()" aria-label="Close menu">&times;</button>
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
  <a href="/guides/">Guides</a>
  <a href="/guides/best-cheap-vegas-shows/" class="d-guides">&#127797; Deals Under $50</a>
  <a href="/news/" class="d-dispatch">Vegas Dispatch</a>
  <a href="/shows/" class="d-cta">All Shows &rarr;</a>
</div>
<div class="nav-overlay" id="vsNavOverlay" onclick="vsToggleMenu()"></div>`;

  const styles = `
<style>
#vs-nav { position: fixed; top: 0; left: 0; right: 0; z-index: 200; font-family: 'Inter', sans-serif; }
.vs-announce { background: #12061f; color: #efe9ff; text-align: center; font-size: 0.8rem; font-weight: 500; line-height: 1; padding: 8px 16px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.vs-announce span { color: #c6f22e; font-weight: 700; }
.vs-nav-row { position: relative; display: flex; align-items: center; gap: 24px; height: 56px; padding: 0 40px; background: rgba(20,8,40,0.92); backdrop-filter: saturate(160%) blur(12px); }
.vs-nav-row::after { content: ''; position: absolute; left: 0; right: 0; bottom: 0; height: 2px; background: linear-gradient(90deg, #ff2e7e 0%, #7c3aed 50%, #c6f22e 100%); opacity: 0.9; }
.nav-logo { font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800; font-size: 1.26rem; letter-spacing: -0.03em; text-decoration: none; color: #fff; white-space: nowrap; }
.nav-logo .sk { color: #ff2e7e; }
.nav-links { display: flex; gap: 26px; list-style: none; align-items: center; margin: 0; padding: 0; }
.nav-links a { color: rgba(255,255,255,0.82); text-decoration: none; font-family: 'Inter', sans-serif; font-weight: 600; font-size: 0.92rem; letter-spacing: 0; text-transform: none; transition: color 0.18s; }
.nav-links a:hover { color: #c6f22e; }
.nav-spacer { flex: 1; }
.nav-cta { display: inline-flex; align-items: center; background: #ff2e7e; color: #fff !important; font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 700; font-size: 0.92rem; text-decoration: none; padding: 10px 20px; border-radius: 100px; box-shadow: 0 8px 20px rgba(255,46,126,0.3); transition: background 0.18s, transform 0.18s; white-space: nowrap; }
.nav-cta:hover { background: #ff1f72; transform: translateY(-2px); }
.nav-mobile-menu { display: none; background: none; border: none; color: #fff; font-size: 1.5rem; cursor: pointer; padding: 4px 8px; line-height: 1; }
.nav-overlay { display: none; position: fixed; inset: 0; background: rgba(6,3,14,0.55); z-index: 250; }
.nav-overlay.visible { display: block; }
/* mobile drawer (dark) */
.nav-mobile-drawer { display: none; position: fixed; top: 0; right: 0; width: min(320px, 84vw); height: 100vh; z-index: 300; flex-direction: column; gap: 2px; padding: 18px 22px 28px; transform: translateX(100%); transition: transform 0.28s ease; overflow-y: auto; background: linear-gradient(180deg, #1c0a3a, #12061f); border-left: 1px solid rgba(198,242,46,0.14); box-shadow: -12px 0 40px rgba(10,4,26,0.5); }
.nav-mobile-drawer.open { transform: none; }
.drawer-x { align-self: flex-end; background: none; border: none; color: #fff; font-size: 1.7rem; line-height: 1; cursor: pointer; margin-bottom: 4px; }
.nav-mobile-drawer .drawer-search { display: flex; gap: 6px; margin-bottom: 12px; }
.nav-mobile-drawer .drawer-search input { flex: 1; min-width: 0; border: none; border-radius: 10px; padding: 11px 13px; font-family: 'Inter', sans-serif; font-size: 0.92rem; outline: none; color: #171225; }
.nav-mobile-drawer .drawer-search button { flex: 0 0 auto; border: none; border-radius: 10px; background: #ff2e7e; color: #fff; padding: 0 15px; font-size: 1rem; cursor: pointer; }
.nav-mobile-drawer > a { color: rgba(255,255,255,0.86); text-decoration: none; font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 700; font-size: 0.9rem; letter-spacing: 0.05em; text-transform: uppercase; padding: 13px 4px; border-bottom: 1px solid rgba(255,255,255,0.1); transition: color 0.18s; }
.nav-mobile-drawer > a:hover { color: #c6f22e; }
.nav-mobile-drawer > a.d-guides { margin-top: 10px; background: #7c3aed; color: #fff; border-left: 3px solid #c6f22e; border-bottom: none; border-radius: 8px; padding: 13px 12px; box-shadow: 0 4px 14px rgba(124,58,237,0.35); }
.nav-mobile-drawer > a.d-guides:hover { color: #fff; background: #8b3be0; }
.nav-mobile-drawer > a.d-dispatch { border-left: 3px solid #ff2e7e; border-bottom: none; padding-left: 12px; color: #ff5fa0; margin-top: 4px; }
.nav-mobile-drawer > a.d-dispatch:hover { color: #ff86b6; }
.nav-mobile-drawer > a.d-cta { margin-top: 10px; background: #ff2e7e; color: #fff; text-align: center; border-radius: 10px; border-bottom: none; padding: 14px; box-shadow: 0 6px 16px rgba(255,46,126,0.32); }
.nav-mobile-drawer > a.d-cta:hover { color: #fff; background: #ff1f72; }
@media (max-width: 980px) {
  .vs-announce { display: none; }
  .nav-links { display: none; }
  .vs-nav-row { padding: 0 20px; height: 54px; gap: 14px; }
  .nav-mobile-menu { display: block; }
  .nav-mobile-drawer { display: flex; }
}
@media (max-width: 460px) {
  .nav-cta { padding: 9px 15px; font-size: 0.85rem; }
  .nav-logo { font-size: 1.12rem; }
}
</style>`;

  const target = document.getElementById('vs-header');
  if (target) {
    target.innerHTML = styles + html;
  }

  // Load display + body fonts used by the header/footer (idempotent)
  (function(){
    if (!document.getElementById('vs-fontlink')) {
      var l = document.createElement('link');
      l.id = 'vs-fontlink'; l.rel = 'stylesheet';
      l.href = 'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap';
      document.head.appendChild(l);
    }
  })();

  // Favicon — set once, applies to every page via this component
  (function() {
    var existing = document.querySelector("link[rel*='icon']");
    if (existing) existing.parentNode.removeChild(existing);
    var link = document.createElement('link');
    link.rel = 'icon';
    link.type = 'image/png';
    link.href = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAW+0lEQVR42q2baYxtWXXff2vvM9ypbo2vhvdev6He1I82dJupDQHCYGNigrHaoR2IcKwMsp0gxYqUD5GVpFE+RsoAH8AKURJZsd2Jo0SWQkCGBEhjN9Dthm6gTXc/3vyqXr2aq+50ztl75cM5d6iqe6uqEVe6UtUdztl77bX+67/+a11RVaV4eK8YIwDcX1njj/7rF/nil/4fP3j5Ghtbu3gFEUCh9yWK1479KC7w03jowCWBfCeKEWFivMYjVxf5pV98N3/zyV9ifm7mwB4BpGsA7z3GGDLn+Df/7j/z2c/9IbdvLYG1hFGItXb4RnVgT3LYRmXIyo/Y3ICxj2NkHbisc440SSBzPHRmgU/9g4/zj//RbxBY29trYQCvuVUM95Ye8Ilf/yd8/SvfJBirUyrHqCrqFT1k0brvLRlcrWqxARl+fLr3BGXw7xGmkhE21X1ryJ/Q7iS47W3e/f538Ae//684fXKuZwRxzqkxhnvLD/j5D/09Xn7pVeqzU2Rp1t/0gdMd5X77FilSLEyHG2DP0Wpv03uPW3v3795DRjjLKN8SEYIgYGd1nSuPLPLVL/0HTi3kRpAsy9R75ec//Pf5xlefpT47TZqmP1lIDmAE8nowYe9GfyrYIAfXFkYhOyvrvOv9b+OrX/wC1liMtZbPfu6/8I0/fYb63ODmZchqZMQK89d7ByeM+J6Mcub8b5Fj3Ot12HQfUKdJytjsFM985c/47Of+AGsN8mB1XR/7uSdZWVknjEL6SUGOgN5BSw9zwMNc4bB76PGzxVEeM+Q2gpAmKbNzU7zw509jzy4++tTTf/RFKrUq3vt9X5JjXni0V4xetRxp3wPRIYdsfpRNh8BJGAWsraxx9txJrJOZp358425++l6H32i/QQ71zqNcVw5GhezzVZEDoCeD99cRxpchtpQhNhEhSx3OO2xHJ59qtZOcHOgQYiODF5Jj4sGovRfZQEEzBU/+7IKnkT0b69pCBWTwZGSEQUdwrqHYZIRGs4VUZh5X9XrounWPYeQQnz2E9IiAA+8UU1KCMYEgf08yIdsF1wJjgEAGLqt7eMHo0NTj40QvpIRAVQ+PpT1vyzFgV/t3HWRzmSL1jMmrIZXTIaakTJ2uArBxp0nW8LSWPbuveLJ1QSxgtHc5OdS5RoDEHpDWA2RJVZHy9Nv1UIvpYYR/BGINXEc9YKB8NePyL5zg5KUpbr58n4UrE9SmYlBobiXceHGV2ljIzkaH+8932H0J1AlidHTMH7ifHKSF+17bn2NsWDn11JEhfCQRH5KyDOAFCZXJd8Ff+duXufKWBX70F3eYOT9GfaZM2nZ4r8S1kHItYuNOg1Nn65QWhDRO6dxVyAB7DA+UfQcwgnZ0caX7XjCUyR0wiA4/5cOQR3MXHn+H8p5PvoHZM3W+9+w1JIDJuSrtZoqxObqlHUd9usTmVIn11RYz8zXs2wz4Hda/4XMUPFB5Ddvl8arMQdpuXt939XgfFEEzIb6c8fjfuMjMqTFu375PYzVh7uw4WeL6JakXDIJPHLNnx2i3PWnHMTFe5tTPVqk+Imj6umvuQ20iDDOAHHIPHZKwdQgIaZ7qcGDqGYvvneT8lTnWNzbpbKUEoaE0FuKcHrCn91CuBsTlgE4r48FSg7GxmNm3xNgphUz3eqMelYLl4GcG8LmgGn0D6NDDlV7+PpD/95OFAfuoVyoX4Y3vOsf6+jYbS7u0dzIq4xFihKF0oiA+E3MVlm7vIFaI44Cp+TLVi5KD6cjQHOGdss9zBu7TNYT56Sg3A8CjApFn9pEa9ekqraTN2r0mD25tMzZTRjM/kjiqV0pjIWEpYGqmTJZ6KpWQscUAqRTEaRQGGvYZVw8lbXogBPZ8RQ6J/yNwwIEZd5x8eJLUp6hzLCyOg0BcDvBeD2Y0ze3mvRKVLXE1IEvz3RpjqM9GBBOKun1pTQrBJVF8B1xHwcmxSF337+DAlrtxPDSP6Ijif+BlD9GEML0wRtpJ8V7BQnU6xgg4N2D2AVua4v8gMBgxZKkjjkPwUKoEhONCeq+gxl0YSAVKjvJ5gykDqdC+63E7ggTHq5qD0R6vI0orHZ32JDdeVDeUKhFJJ8EaQ6vZAZ9TT9UB5Wcf0+yW4kEouFSRUh77YWgJ66anGiF5ZgjmHKc/UCKeCDl9eZo7r63SWk9Y/XZG8xo5mzwiI5jDs50eQ3TYq1MpENcsUcmiKHEpABHiSkhYskSxIYoMYVA8I0NQPMPYEpYspbEIDBibx3YYGYJqH3vVgdQyFj9a4x0feZhyNWT6dIX6RIkzPzPF4kfHCE54NOtGTJ9Py75EFhy3kDtaculWcIpEQrOTsbqyiyaO7dUOaSdj+dYOzaYjCiylUPDFiRoROqknzTIqlZCdtTZpIyXLQK1BS4IGA4v3Sum88qb3nGVnq4lEuQpcnYppbCY8dHWKpTfusPY1PRLGg4MsUI5geqMTgTFC22WEbc+5GwkPdyr4VpvAOybmThF01pgIt1hrRdxeEcqBIgrNVFmcrzB78ix3l+6yTkoz3SDcLZGIsrap3G86UmJiBTWe6QsVqpMxt15boVSNUFXicsjq3QalcsDUxTLrzzagZXIqrcPDIBim6A7fvx7pE0nDMX8p5J9+5CLfef42SzsGMQFrW9s0mneoxnBqUviVt9b4+mqLH2YRRpRHSjFXp5o8/aWX2W5assSysROQJbuUQ+H8OHzqZyv869sZK9cstqJUJkMUJUsdUSXAeTBhX4Yr1QJMDL55eDoP9qTwIu77l9HhisseHVp6WpsvN/n4Ry/ywg/u8uz1iKvnTrLbanB3bZlWuw0YvndTefF2wj97cpqH11KstVyYifi3f7JFtXaW+akxNrY3uLtxnzTzCMK3b3lMKeHDj8N/WgFxggkNXhX1IMYgRcfHWCHrOMQKJgS3D672swNzgPQV7En2VFc5gGgqaAaqHs204OhgjdBsJjzx5By/88GY7766zWOXz9JobfHSK98nTTrEYUAcCjNjllbHk6XwQsPw/K7QaWwThhUunJxkdeM+P3j1B+AdcSDEAcyOWb5zPeE331nmQ3/V0e44jKXoW+RPbwArJB3H9RdX80LLgKZ6KHQFg5qZDKVYBdlwEJ9xVM5bolpAspvRvK50boMPIC6FPPPNdf5kcZfJepn76+v86Mev4LzHWpuLDwKtxHNxPub6WsLW4jwY4eade0xXPdfu3OPardcAyVtXRb7MPIyVLF+7nvKdHxqiUIZKBMYIVgzzi+NsbzRBlLE3CM3biibDNcPggFqihevLgCCoMPE2OPueSYwxXHjTPN//9i3Ct1uuf3mb3ZeUIDQsvapcXzGE0ua5v3yZyDqssb38Hlphqw1XpzzLRqjNlhDgwVLEvN3kaz9aZqZmcH7AHQW8Qr0E15Ydyz+OKNd8zil6QZqv02fKwmKd+myJtaUdag8LnWvg2+TEaEi7zXRBcCjuiaKZEp7OeOvHz3B2cZ64YjGRpxSHzJ6qs/ihOuG8xycewpC7y20mbJOtliMKAgTFSK53ru16zk0bLs0avh9UqJQslZLl+ybm4gm4cCJgo9n/vBGwArsdz5lpw8Zuf9U2kN7Cu6W1R9lab+HSXItoXoPGNe1tfgQR0j1Ngz0MWAGrzDxa4tyVWZburlGuhzjniasB7WbC6SuT1C4avEAo8H+ez3jLpTKPn43YTT2tVGmlSuqUNz8U8MnHAr6WxYw/PAOZg9Qx8fAMX/cVfv3NEW89E5I6pZnmz0bieXReeOx8xDM/tARiwCo2Nr3G7aCiXZ8uYwy4VMl2FBPJQYV7VBY4SP0FShlzl6ZJXUqj0WL6oQqqSlgOaDdSwmpA7VTERtghdLByN+b3v+v51bfFvHtdSJ0QBJYwVFID/zstwaPznKhYstTjgUpZWHvTPP/rxfu880qbd12wZE5QFaJQCEqe//itjHs3Y0oREEJcDfDO47xiQ4MRyDqO5Rt51ZklOlQzGKwl+iCog2mv+ICAdsDUoTwekSQZPlXE5HzeGkGdYsUQVgSs4p0QKby6afjDrMTMWIVYoNFIaWIw0zWmz9UZmwxxmWIDg6J4Byfmymw9fpIvX9/BPNglSBKikiXxwkoTVnZdToJUsCWlMhbjUodzOf4AZIknCC1ihKzl8ix1SBu/zwR7maAPiBJA9YrQ3gFjBe+VyYUK1pqe0quaG2+w9a2ASTPe8HPn0BB2Gy2ypSah85x7ZIpOy9HcTPCZ7pk2MYFQqQRcfvMJbrwcsLvZplaPCYwwT8rGd7dpJB5Ty5i4GDI+U6Gx3cEIhLEFhbSVEUY5J+jsZmjSPd3RZGho0SiG3HoKY28w/fRghN6oROEJSBeE+jDq0jx8osgQe0OpZElbSpp6EFi9s8vOahsT5CfnM09tpsTpy5NkmccYKIdCvRKgDjY3O5ROw8JCQGU64Mo7TlKdjrj+zftFzOc9q9ZOQnU8Jkky2htZXgyZY9YCIL1cDXkltvuKJ0o9/oN5KrKB6bNEK3jNm6kmyBsZ3dzsHTjnCcX0wslrHj4+85x8eHJvOir+cc5jbIBTj6rgfW7opO059TM1zrxxijAqgSqvPHePrOOZvTqGSz2Y3ADzFybYXNmltexzWT7goJy21wD9pewvFU0kZFuQtjOMFdq7Kdl4iTjOjeGLCwclk9+oix0ZZM4hJix6c31vQek1YXub93vyUL7wbo6X/O1Oy7N2s0mns0NjJyEqByw+egLnPFEp4N5rW5THIqLA8OD6Du2lvYNTwwBQRoXAnoaLh6SRYY2hvZ2SnHDE1YAgMGiWA1hUDjCR4Lun7SBLPUZyEUNMV4jUI7vjqCK+iw9KlnomT5RodTJajZTSeMzM6THK1YA08YRxwPZam837TRYfnebBzU02bnRIH/TJz0gQlJ4BZGCYaV+1kEoOKOR6Xdp2OYUM8zycJo7SWIitKek9ybNEkrMyU4SAmELV1cEuo/ak68GqXZE8XLofdUpcC5hcKENgCeIATT0uVYLAsL7UYPnaFg9dnqS93mHp5jZbL3k0zYsh7W1KD45x5JqgHlLsKpoKzfUUl3nK1YikmQFgI0NUDthcbTJzus7849vcdU2yB+A0odNIewxNjAwwMTkQat1ULMVAlWo+69cbvTGFubRQhkVo7iQIwua9BnMLNXzLcX9lm5XnEzq3BAn712aPgUcoQnnMDdHVnWFnqUOrkVCdKrF0bSt/L1NOnK5x/cU1xk+UeefHLrH89m12HrRI2hmTs2M47/KSUwayR3carLuwYqOmcJDeek3ulcbA7nbCg6VdRASvuaRmC8V4bqFGq5Fy58Ym9/+ixe738s0fV+kP9gwvDCsGFVrLjpWbmyxcmsQ7T3snpVwJKI9FLFwc59oLK8w+NMbUqTEWLowTxSFJkrK1vptXdYYCMHXfkIf0Uqzv7lsN3ilhkXIlENZuNCjHIaVKgI0McSnAWiHJMu4vbbO13Wb9uxlb3wITvr42bi8L7BmCGERKC+kDw/KPtpleqDF7rs7Sq5tcfMssSTtjaq5CqRKyfH2btbsNJBCyzFGfKTN3pt7HAN2rRggyAEp9DxHVnpRO8RlxUK4HlKqWTjtjezul1UjZXk7Y+suUdE2oLBiqi0Lz5pDiZ98gl+wNAT1c97TgNmHjtZTlc5ucvjTNZtTk1svrnH1kmrSdUapYFh+dIUkdWeLwBT3tzuUa05fDh431aFF3SHEQ2mWXRV71Hl77sw3EGVxbSbaUdENxW4J2cqaTrCgmKqRwHaFe7xsbEN2XBmXPDE6/gSkWGj9Uls83iAPL/Lk6yze3ee2FFU5fmiSKLS5zGCtElSAHs2LDWggV/Y11s32BCN1EP3Aqvqg1RHLl2Dtl41lFm9oXbiUnXxINfDc72B8dFtKDcdALATlk8E4suB1h5U9TAruNiDAzU2FttcnOejvX9EsWRQgjm9PjoBta/Zyufv/E0j5MllzyNkLuTV4pVS1Z4hExSCTFoFVxoMroeewjFP1udgxg/yzZIFMZGFCyOePbveu4mW0yd36MifES6oXOZkIj8+xsJnkl5jxBZDj/phlsaPJA684Mk1d0vZP0+xpMorjUs7GZcGKhmntEWkyK6Oiq7qhRnVFkLzj4CRk5ESoBbD3n2VRP47Etpi43GZ8tUa1FVKOQWjXEO8WrcvfWDuphd6ODsZJjQpbX7r1UqLLnTjbIJ8k6Dcf4eIlSOSR1Lhdi/cEpGOToabBRA2Cyd0RGR29+4OXmDc3VVoXNZzw7L3eonEmonrKUpwOioiVmLLjU45zHBoY7r6znU2LS1/r23KkAvc2VFpVaRFwJqE3EOOdzvSDdt5kjxxOHTIiNVIWPM2vX1c+iwcECwW3AzirsvJhhKhmmAqaU++jkYyG1eoVMU05dnOTG91ZR0T4rpJC1pZ/u1u7uEl6YGOge5wzQdaVt2SfsHzbDcMymVsDreeg+AwfFFVTQJmS7+Xs+hXRRqVRKbG+nlOsR1ekSLvGEUV8lHlykdz4vq01REA1mhUzxiWJjOaJbNQxg9dCxQiPDBoP0GGbU/phrV16VACQGEwuu48g6GcaYggQp3vmBDlSRDn0OiOq7cluODd1leVWyBsSzEEzmneGh8zUjJ9hk6OZ7/cx6rYJz/pAoGCKl6uiJ2K5hXFtxWYEZuaVzGWygGJIBQ7tU+2mtOB4x4NqeaBqqFw2uoQMKz08wNTawbuc9Y2MVzIXF06Rpv3LbW6vr/lnZQ4cQ90zKpIrLit/lSK4rOqcHBs2kGIwwVpier+Kd7zftiiLKNT1bz3u0M2r8RQ8ZmNID6zZiyJKUi4unMR943+NomiFHiWev6yG4RElTV4QAGGtQ7/viSLGg4sdbBLFlcr6Skx7b36UXpb1cjMMEr39mUb0eHGIVQdOM97/3cczf+rUPU5+qk2bZTwajIyZrfQfSjsOaQhUKBO+0l/sHew9haNl60GT5+jZiBDM4P5gp6vSIoTUZmhG60pvuY05pmlGbGOMTT/41zOVL5/i1Jz5IZ32LMCx40agBw8PiYF/15RMlaxceQBECmeL3XSzn+p64ElKbiPPW9sAPG33m0c5wMBttiK7wkmuLvespBDags7nFx574Ba4+fAHjVfkXv/vbnDg9R7vVxlizr+0qAwOHcrh3DNojhU47RYwBD9bmdX6+GNmLyBaSVpaXyFkugnRv7TLFZ3KwdSXHc8XB+xlr6LQ7TC2c4Knf/e0ce9R7Tp2c4wuf/zRJq416j7XmiPgaNjm693/NoNNJe+wvV5H90Olt9VCq5gOSeV9A9oCppoPDTschQgc5sTH5/ZNmk3//+U9z5qGF/MeT1hqcc/zyh9/HF37vX9LcbdJpJ4Rh0GuV9W90nNmhXNxTJ/mpFqBnAoN3++Kx+9sgr8TlgCC2OXBa6XmHT3WgzJXRzOwQdAjDgKST0Npp8Pnf+zRP/PIHcM5hrc1Jp7WWLHP83d94gv/5x59heqLG9v01nM/fM8YM/F5Ijs61AmRC0nQIeRq0BQj2ByMl5wGD7NLngGfE9PTDLM3H3YaTnxFzrpLrhdZanPds319jql7jf/zxZ/jNv/MxsizffJe/5WkosDjn+Ohffx/P/fnT/NanPkG1FLG7uUWj0SRz7nWkgXxktdPMeq0zG+YuqF6HQlYXrV2Wq0hSCCpZx/c9QI8a181fzzJHo9lkd3Obainit/7hJ3ju2af5lY+8H+ccQWCH1wLW5kY4dXKOz33mn/M7n/ok/+2/f5mv/N9v8eq122xu7x5Ri/c9RLyQNlzu/hgCo0U/X4ofh8lgLwgtCh31mv+iM//JCT7Jw+nwH2zJQI6Hyak6ly6c4QPvfZwnf/UXuXLlfI4nrn/y3cf/B+8OkcE3SHJYAAAAAElFTkSuQmCC';
    document.head.appendChild(link);
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
