// Vegas Sidekick — Adult Category V2 pilot
// Presentation/SEO layer only. Does not add, remove, reorder, or rewrite SHOWS inventory.
(function () {
  'use strict';
  if (location.pathname !== '/shows/adult/' || document.documentElement.dataset.vsAdultV2 === '1') return;
  document.documentElement.dataset.vsAdultV2 = '1';

  function setMeta(selector, value) {
    var node = document.querySelector(selector);
    if (node && value) node.setAttribute('content', value);
  }

  document.title = 'Las Vegas Adult Shows 2026 | Compare 18+ Shows | Vegas Sidekick';
  setMeta('meta[name="description"]', 'Compare Las Vegas adult shows, including burlesque, male revues, adults-only comedy, circus and parody. See venues, starting prices and the tradeoffs worth knowing before you book.');
  setMeta('meta[property="og:title"]', 'Las Vegas Adult Shows 2026 | Vegas Sidekick');
  setMeta('meta[property="og:description"]', 'Compare Vegas adult shows by vibe, venue and starting price — with useful context before you book.');

  var styles = document.createElement('style');
  styles.id = 'vs-adult-v2-styles';
  styles.textContent = `
    body{background:#f7f6fb}
    .age-banner{display:none!important}
    .cat-hero{padding:118px 24px 46px;background:
      radial-gradient(900px 460px at 82% 12%,rgba(255,46,126,.2),transparent 62%),
      radial-gradient(760px 420px at 8% 95%,rgba(124,58,237,.32),transparent 68%),
      linear-gradient(155deg,#1b0935 0%,#2b0f55 58%,#13071f 100%)}
    .cat-hero::before{background:radial-gradient(ellipse at 72% 44%,rgba(255,95,160,.12),transparent 58%)}
    .cat-hero::after{height:2px;background:linear-gradient(90deg,#ff2e7e,#7c3aed,#0fb5c9,#c6f22e)}
    .cat-hero-inner{max-width:1000px}
    .cat-badge{color:#ff9bc2;font-weight:600;letter-spacing:.13em}
    .cat-badge-dot{background:#ff2e7e;box-shadow:0 0 12px rgba(255,46,126,.7)}
    .cat-headline{font-size:clamp(2.7rem,6vw,4.9rem);line-height:.98;letter-spacing:-.045em;max-width:760px;margin-bottom:16px}
    .cat-sub{max-width:700px;color:rgba(255,255,255,.76);font-size:1rem;line-height:1.65;margin-bottom:25px}
    .cat-stats{gap:12px}
    .cat-stat{min-width:118px;padding:11px 14px;border:1px solid rgba(255,255,255,.1);background:rgba(255,255,255,.055);border-radius:12px;backdrop-filter:blur(8px)}
    .cat-stat-num{font-size:1.15rem;color:#fff;letter-spacing:-.02em}
    .cat-stat-lbl{font-family:'Inter',sans-serif;font-size:.64rem;color:#bdb0c8;letter-spacing:.02em;text-transform:none;margin-top:3px}

    .cat-nav-bar{border-bottom:1px solid #ece9f6;padding:10px 24px;background:rgba(255,255,255,.96)}
    .cat-nav-bar-inner{max-width:1200px}
    .cat-nav-link{font-family:'Inter',sans-serif;font-size:.76rem;letter-spacing:0;border:1px solid #e8e4f0;background:#f7f6fb}
    .cat-nav-link.current{background:#281047;border-color:#281047}

    .cat-intro{padding:28px 24px 22px;background:#fff;border-bottom:0}
    .cat-intro-inner{max-width:900px}
    .cat-intro p{font-size:.98rem;line-height:1.72;color:#49415b}

    .adult-v2-guide{max-width:1200px;margin:0 auto;padding:10px 24px 22px}
    .adult-v2-guide-inner{background:linear-gradient(110deg,#fff,#faf8ff);border:1px solid #e8e3f0;border-radius:16px;padding:20px;box-shadow:0 8px 28px rgba(41,16,71,.055)}
    .adult-v2-guide-kicker{font:800 .68rem 'Plus Jakarta Sans',sans-serif;color:#ff2e7e;text-transform:uppercase;letter-spacing:.12em;margin-bottom:7px}
    .adult-v2-guide h2{font:800 clamp(1.28rem,2vw,1.65rem) 'Plus Jakarta Sans',sans-serif;color:#21152f;letter-spacing:-.035em;margin:0 0 7px}
    .adult-v2-guide>div>p{color:#6d6478;font-size:.9rem;line-height:1.6;margin:0 0 16px;max-width:760px}
    .adult-v2-choices{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
    .adult-v2-choice{padding:13px 14px;border-radius:11px;background:#f7f4fb;border:1px solid #ebe6f1}
    .adult-v2-choice b{display:block;font:700 .83rem 'Plus Jakarta Sans',sans-serif;color:#28163c;margin-bottom:4px}
    .adult-v2-choice span{display:block;color:#71677b;font-size:.76rem;line-height:1.45}

    .filter-bar{position:sticky;top:88px;margin:0;background:transparent;border:0;box-shadow:none;padding:10px 24px;z-index:100}
    .filter-bar-inner{max-width:1200px;background:#fff;border:1px solid #e8e4ef;border-radius:14px;padding:9px 10px;box-shadow:0 6px 20px rgba(39,17,61,.07)}
    .filter-btn{font-family:'Inter',sans-serif;font-size:.76rem;letter-spacing:0;border:1px solid #e7e2ed;background:#f8f7fa;padding:7px 13px}
    .filter-btn.active{background:#281047!important;border-color:#281047!important}
    .show-count-wrap{font-family:'Inter',sans-serif;font-size:.7rem;color:#82798b}

    .grid-wrap{padding:12px 24px 54px}
    .show-grid{gap:16px}
    .show-card{border:1px solid #e6e2eb;border-radius:15px;box-shadow:0 5px 18px rgba(36,19,51,.055)}
    .show-card:hover{border-color:#d9d0e3;box-shadow:0 12px 30px rgba(40,18,60,.1)}
    .card-img-wrap{background:#21162d}
    .card-body{padding:15px 15px 16px}
    .card-name{font-size:1.22rem;letter-spacing:-.025em;line-height:1.15;color:#21152f}
    .card-subtitle{font-size:.82rem;letter-spacing:0;color:#796f82;margin-top:2px}
    .card-venue{font-family:'Inter',sans-serif;font-size:.68rem;letter-spacing:0;color:#8b8293;margin:5px 0 10px}
    .card-pill{font-family:'Inter',sans-serif;font-size:.62rem;letter-spacing:0;padding:4px 8px}
    .card-pill:nth-child(n+3){display:none}
    .card-price-row{margin-bottom:11px;align-items:flex-end}
    .card-from{font-family:'Inter',sans-serif;font-size:.59rem;letter-spacing:.02em;color:#8a8192;padding-bottom:3px}
    .card-price{font-size:2.12rem!important;color:#3b82f6!important;letter-spacing:-.05em}
    .card-cta{background:#3b82f6!important;border-radius:9px;text-transform:none;letter-spacing:0;font-family:'Plus Jakarta Sans',sans-serif;font-size:.82rem;padding:11px 10px}
    .card-cta:hover{background:#2563eb!important}
    .card-age-badge{background:rgba(25,10,45,.9);border:1px solid rgba(255,255,255,.24);font-size:.54rem;border-radius:6px}

    .adult-v2-after{background:#fff;border-top:1px solid #ece8f1;padding:48px 24px 54px}
    .adult-v2-after-inner{max-width:920px;margin:auto;display:grid;grid-template-columns:1.3fr .7fr;gap:24px;align-items:start}
    .adult-v2-after h2{font:800 clamp(1.45rem,2.8vw,2rem) 'Plus Jakarta Sans',sans-serif;color:#21152f;letter-spacing:-.04em;margin:0 0 10px}
    .adult-v2-after p{color:#685f72;font-size:.92rem;line-height:1.72;margin:0 0 13px}
    .adult-v2-take{background:#211039;color:#fff;border-radius:15px;padding:19px;border-left:4px solid #c6f22e}
    .adult-v2-take b{display:block;color:#c6f22e;font:800 .73rem 'Plus Jakarta Sans',sans-serif;text-transform:uppercase;letter-spacing:.08em;margin-bottom:7px}
    .adult-v2-take p{color:#ddd3e6;font-size:.82rem;line-height:1.6;margin:0}
    .adult-v2-links{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
    .adult-v2-links a{display:inline-flex;padding:8px 12px;border-radius:100px;background:#f5f2f8;border:1px solid #e4ddea;color:#39264c;font:700 .76rem 'Plus Jakarta Sans',sans-serif}
    .cat-desc{display:none}

    @media(max-width:940px){.filter-bar{top:54px}.cat-hero{padding-top:86px}}
    @media(max-width:720px){
      .cat-hero{padding:80px 20px 31px}
      .cat-headline{font-size:clamp(2.35rem,11vw,3.35rem);max-width:520px}
      .cat-sub{font-size:.93rem;margin-bottom:18px}
      .cat-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:7px}
      .cat-stat{min-width:0;padding:9px 9px}
      .cat-stat-num{font-size:1rem}.cat-stat-lbl{font-size:.57rem}
      .adult-v2-guide{padding:7px 14px 16px}.adult-v2-guide-inner{padding:16px}
      .adult-v2-choices{grid-template-columns:1fr}
      .filter-bar{padding:8px 14px}.filter-bar-inner{border-radius:12px;padding:7px 8px}
      .grid-wrap{padding:8px 14px 42px}
      .adult-v2-after{padding:38px 20px}.adult-v2-after-inner{grid-template-columns:1fr}
    }
    @media(max-width:520px){
      .show-card{border-radius:0;box-shadow:none}.show-card:hover{box-shadow:none}
      .card-name{font-size:1.08rem}.card-price{font-size:1.55rem!important}
      .card-price-row::after{color:#3b82f6}
    }
    @media(prefers-reduced-motion:reduce){.cat-badge-dot{animation:none}}
  `;
  document.head.appendChild(styles);

  function inventory() {
    try { return (typeof SHOWS !== 'undefined' && Array.isArray(SHOWS)) ? SHOWS : []; }
    catch (e) { return []; }
  }

  function updateHero() {
    var shows = inventory();
    var count = shows.length || 11;
    var prices = shows.map(function (s) { return Number(s.price); }).filter(function (n) { return Number.isFinite(n) && n > 0; });
    var min = prices.length ? Math.min.apply(Math, prices) : null;
    var badge = document.querySelector('.cat-badge');
    var sub = document.querySelector('.cat-sub');
    var stats = document.querySelector('.cat-stats');
    if (badge) badge.innerHTML = '<span class="cat-badge-dot"></span>Las Vegas after dark · 2026';
    if (sub) sub.textContent = 'Burlesque, male revues, adults-only comedy, circus and parody. Compare the vibe, venue and starting price before you pick your night. Age rules vary by show, so check the individual listing before booking.';
    if (stats) stats.innerHTML =
      '<div class="cat-stat"><div class="cat-stat-num">' + count + '</div><div class="cat-stat-lbl">Shows to compare</div></div>' +
      '<div class="cat-stat"><div class="cat-stat-num">' + (min ? ('$' + min) : 'Prices') + '</div><div class="cat-stat-lbl">Lowest listed start</div></div>' +
      '<div class="cat-stat"><div class="cat-stat-num">18+/21+</div><div class="cat-stat-lbl">Check each show</div></div>';
  }

  function updateIntro() {
    var intro = document.querySelector('.cat-intro p');
    if (intro) intro.textContent = 'Vegas adult entertainment covers more ground than the label suggests. Some shows are polished burlesque revues, some are high-energy dance productions, and some lean into comedy, circus or parody. Use the cards below to compare starting price, venue and tone — then open the individual show page for the details that actually matter.';

    var guide = document.createElement('section');
    guide.className = 'adult-v2-guide';
    guide.setAttribute('aria-labelledby','adult-v2-guide-title');
    guide.innerHTML = '<div class="adult-v2-guide-inner"><div class="adult-v2-guide-kicker">Quick way to narrow it down</div><h2 id="adult-v2-guide-title">Pick the kind of night you actually want.</h2><p>“Adult show” is a broad bucket in Vegas. Start with the experience, then compare price.</p><div class="adult-v2-choices"><div class="adult-v2-choice"><b>Classic revue / burlesque</b><span>Start here if you want choreography, costumes and a traditional Vegas-after-dark format.</span></div><div class="adult-v2-choice"><b>Big crowd-energy night</b><span>Look at the dance-driven productions if the point is a louder group-night-out atmosphere.</span></div><div class="adult-v2-choice"><b>Weirder Vegas</b><span>Comedy, circus and parody options are better if you want the adult label without a straight revue format.</span></div></div></div>';
    var introSection = document.querySelector('.cat-intro');
    if (introSection && !document.querySelector('.adult-v2-guide')) introSection.insertAdjacentElement('afterend', guide);
  }

  function addBottomGuidance() {
    if (document.querySelector('.adult-v2-after')) return;
    var gridWrap = document.querySelector('.grid-wrap');
    if (!gridWrap) return;
    var section = document.createElement('section');
    section.className = 'adult-v2-after';
    section.innerHTML = '<div class="adult-v2-after-inner"><div><h2>Choosing an adult show in Vegas</h2><p>Don’t use the word “adult” as a quality filter. The useful differences are format, audience energy, venue and how much interaction you want. A polished revue and a comedy-heavy circus can both belong on this page while being completely different nights out.</p><p>Starting prices are useful for comparison, but your date and seat can change the final total. Open the show page before booking for the current schedule, age policy and the tradeoffs worth knowing.</p><div class="adult-v2-links"><a href="/guides/">Vegas Guides →</a><a href="/guides/best-cheap-vegas-shows/">Deals Under $50 →</a><a href="/shows/">All Vegas Shows →</a></div></div><aside class="adult-v2-take"><b>🌵 Kris’s take</b><p>This is one category where the cheapest option tells you almost nothing about the experience. Decide whether you want burlesque, dance, comedy or full Vegas weirdness first. Then compare the prices inside that lane.</p></aside></div>';
    gridWrap.insertAdjacentElement('afterend', section);
  }

  function cleanClaims() {
    var count = document.getElementById('show-count');
    var shows = inventory();
    if (count && shows.length) count.textContent = String(shows.length);
    var label = document.querySelector('.show-count-wrap');
    if (label && shows.length) label.innerHTML = 'Showing <strong id="show-count">' + shows.length + '</strong> shows';
  }

  updateHero();
  updateIntro();
  addBottomGuidance();
  cleanClaims();
})();