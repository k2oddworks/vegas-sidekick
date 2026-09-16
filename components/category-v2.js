// Vegas Sidekick — Category Pages V2
// Shared presentation/SEO layer for /shows/ and category browse pages.
// IMPORTANT: this file does not add, remove, reorder, or reclassify any show inventory.
(function () {
  'use strict';

  const PATH = location.pathname;
  const CONFIG = {
    '/shows/': {
      accent:'#ff2e7e', accent2:'#c6f22e', eyebrow:'LAS VEGAS SHOWS · 2026',
      title:'All Las Vegas Shows',
      metaTitle:'Las Vegas Shows 2026 | Compare Shows & Starting Prices | Vegas Sidekick',
      meta:'Compare Las Vegas shows across comedy, magic, Cirque, music, spectaculars, family and adult entertainment. See venues, starting prices and useful context before you choose.',
      sub:'Comedy, magic, Cirque, music, family shows, adult shows and big spectacles. Narrow the vibe first, then compare venue and starting price.',
      intro:'Vegas has too many shows to shop by logo alone. Start with the kind of night you want, use the category pages to narrow the field, then open the individual show page for seating, schedule and the tradeoffs worth knowing.',
      thirdNum:'7', thirdLabel:'Show categories',
      guideKicker:'QUICK WAY TO START', guideTitle:'Pick the kind of Vegas night you want first.', guideCopy:'Category first. Price second. That keeps a giant list of shows from turning into homework.',
      choices:[['Big visual night','Start with Cirque or Spectaculars if scale and production are the point.'],['Personality-driven night','Comedy, magic and music usually put the performer closer to the center of the experience.'],['Planning for a group','Family and All Shows make it easier to compare age fit, venue and budget together.']],
      bottomTitle:'Don’t overthink the list',
      bottomCopy:'Start with the kind of night you want — comedy, magic, Cirque, music, whatever sounds fun. The price on the card is just the starting number. Open a show page for the useful stuff: dates, venue, age guidance, seating advice and whether it fits your night.',
      take:'Don’t compare a magic show, a comedy club and a Cirque show like they’re the same thing. Pick the vibe first. Once you’re down to a few shows you’d actually choose between, then start looking at the price.'
    },
    '/shows/comedy/': {
      accent:'#ff2e7e', accent2:'#f59e0b', eyebrow:'LAS VEGAS COMEDY · 2026', title:'Las Vegas Comedy Shows',
      metaTitle:'Las Vegas Comedy Shows 2026 | Compare Prices & Venues | Vegas Sidekick',
      meta:'Compare Las Vegas comedy shows, resident headliners and comedy clubs by venue and starting price. Find the kind of comedy night that fits your Vegas plans.',
      sub:'Resident headliners, comedy clubs, prop comedy and late-night rooms. Compare the room, performer and starting price before you pick the laugh.',
      intro:'Vegas comedy is not one product. A resident headliner, a rotating club lineup and a visual comedy show can all be great nights for completely different reasons. Use the cards below to compare format, venue and starting price.',
      thirdNum:'Mix', thirdLabel:'Headliners + clubs',
      guideKicker:'QUICK WAY TO NARROW IT DOWN', guideTitle:'Start with the kind of comedy room you want.', guideCopy:'The room changes the night almost as much as the comic.',
      choices:[['Resident headliner','Best when you are choosing a specific performer and want a polished, repeatable Vegas production.'],['Comedy club','Best when you want several comics, a smaller room and more of a traditional stand-up night.'],['Visual or hybrid comedy','Best when props, audience interaction or a bigger stage concept matters as much as straight stand-up.']],
      bottomTitle:'Choosing a comedy show in Las Vegas', bottomCopy:'Compare format before price. A club ticket and a resident-headliner ticket can sit in the same price range while delivering very different nights. Venue size, lineup format and how much audience interaction you want are the useful tie-breakers.',
      take:'I would not shop Vegas comedy by cheapest ticket alone. Decide whether you want a specific headliner or the energy of a comedy club first. That one decision cuts the list down fast.'
    },
    '/shows/magic/': {
      accent:'#8b5cf6', accent2:'#ff2e7e', eyebrow:'LAS VEGAS MAGIC · 2026', title:'Las Vegas Magic Shows',
      metaTitle:'Las Vegas Magic Shows 2026 | Compare Prices & Styles | Vegas Sidekick',
      meta:'Compare Las Vegas magic shows from close-up and mentalism to comedy magic and large-scale illusion. See venues, starting prices and the style of night each show offers.',
      sub:'Close-up, mentalism, comedy magic and big illusion. Start with the style of magic you want, then compare venue and starting price.',
      intro:'“Magic show” covers everything from intimate sleight-of-hand to giant illusions built for a full theater. The best choice depends less on which poster looks biggest and more on how close, funny or spectacular you want the night to feel.',
      thirdNum:'Styles', thirdLabel:'Close-up to illusion',
      guideKicker:'QUICK WAY TO NARROW IT DOWN', guideTitle:'Choose scale before you choose a magician.', guideCopy:'The distance between close-up magic and a big illusion show is basically a different genre.',
      choices:[['Close-up / mentalism','Best when technique, mind-reading and a more intimate room are the appeal.'],['Comedy magic','Best when laughs and personality matter as much as the tricks.'],['Big illusion','Best when you want stage scale, production value and the classic Vegas magic-show feeling.']],
      bottomTitle:'Choosing a magic show in Las Vegas', bottomCopy:'Start with scale and tone. After that, venue size and starting price become much more useful comparison points. The individual show pages are where to check age guidance, schedule and seating context.',
      take:'Magic is one category where “best” changes completely based on what you want to feel. I would choose intimate versus big-stage first and only then start comparing prices.'
    },
    '/shows/cirque/': {
      accent:'#0fb5c9', accent2:'#3b82f6', eyebrow:'LAS VEGAS CIRQUE · 2026', title:'Las Vegas Cirque & Acrobatic Shows',
      metaTitle:'Las Vegas Cirque Shows 2026 | Compare Productions & Prices | Vegas Sidekick',
      meta:'Compare Las Vegas Cirque and acrobatic shows by production style, venue and starting price. See which big visual experience fits the night you want.',
      sub:'Acrobatics, water, physical theater and giant stage engineering. Compare the production style before you compare the ticket price.',
      intro:'The Cirque and acrobatic category is built around visual spectacle, but the shows are not interchangeable. Some lean dreamlike, some physical, some comic and some are designed around a single technical centerpiece.',
      thirdNum:'Visual', thirdLabel:'Acrobatics + spectacle',
      guideKicker:'QUICK WAY TO NARROW IT DOWN', guideTitle:'Pick the visual language that sounds fun to you.', guideCopy:'Same broad category. Very different productions.',
      choices:[['Dreamlike spectacle','Best when atmosphere, choreography and visual composition matter most.'],['Big technical centerpiece','Best when you want the theater itself — water, machinery or stage engineering — to be part of the attraction.'],['Lighter / funnier energy','Best when you want acrobatics without the night feeling overly serious.']],
      bottomTitle:'Choosing a Cirque or acrobatic show', bottomCopy:'Do not choose only by brand name. Compare the production concept, venue and kind of visual experience first. Then use starting price and seating guidance to decide where the value is for your night.',
      take:'The useful question is not “Which Cirque show is best?” It is “What kind of spectacle do you want?” Once you answer that, the list gets much easier.'
    },
    '/shows/music/': {
      accent:'#3b82f6', accent2:'#0fb5c9', eyebrow:'LAS VEGAS MUSIC & VARIETY · 2026', title:'Las Vegas Music & Variety Shows',
      metaTitle:'Las Vegas Music & Variety Shows 2026 | Compare Prices | Vegas Sidekick',
      meta:'Compare Las Vegas music and variety shows, resident performers, tribute productions and dance-driven entertainment by venue and starting price.',
      sub:'Resident performers, tribute shows, dance productions and Vegas variety. Decide whether the artist, the music or the production is the main event.',
      intro:'Music and variety is one of Vegas’s broadest categories. Some nights are built around a specific performer, some around a catalog of songs, and some use music as the engine for a full visual production.',
      thirdNum:'Formats', thirdLabel:'Legends + tribute + variety',
      guideKicker:'QUICK WAY TO NARROW IT DOWN', guideTitle:'Figure out what you want to be the main event.', guideCopy:'Artist connection, familiar songs or production spectacle — that is the useful split.',
      choices:[['Resident performer','Best when you are going because you specifically want that artist or personality.'],['Tribute / catalog show','Best when the songs and nostalgia matter more than seeing the original performer.'],['Dance / variety production','Best when music is part of a larger visual Vegas show.']],
      bottomTitle:'Choosing a music or variety show', bottomCopy:'Compare what is actually carrying the night: the performer, the songbook or the production. That makes starting price and venue size much easier to judge.',
      take:'A tribute show and a resident headliner can both sit under “music,” but they solve completely different Vegas nights. I would separate those in your head before comparing the numbers.'
    },
    '/shows/spectaculars/': {
      accent:'#f59e0b', accent2:'#ff2e7e', eyebrow:'BIG VEGAS SPECTACLES · 2026', title:'Las Vegas Spectaculars',
      metaTitle:'Las Vegas Spectacular Shows 2026 | Compare Big Productions | Vegas Sidekick',
      meta:'Compare Las Vegas spectaculars and large-scale productions by venue, style and starting price. Find the big visual show that earns a spot in your Vegas night.',
      sub:'The biggest rooms, biggest visual ideas and shows built around scale. If spectacle is the reason you came to Vegas, start here.',
      intro:'Spectaculars are the shows where scale is part of the product: large rooms, ambitious staging, major visual systems and productions designed to feel bigger than a normal theater night.',
      thirdNum:'Scale', thirdLabel:'Big-room productions',
      guideKicker:'QUICK WAY TO NARROW IT DOWN', guideTitle:'Decide what kind of “big” you actually want.', guideCopy:'Technology, stagecraft and classic Vegas spectacle hit differently.',
      choices:[['Immersive / technology-led','Best when screens, projection, effects or the venue itself are part of the draw.'],['Stagecraft-led','Best when choreography, machinery, acrobatics or theatrical design carry the spectacle.'],['Classic Vegas scale','Best when you want a polished production that simply feels like a big Vegas night out.']],
      bottomTitle:'Choosing a Las Vegas spectacular', bottomCopy:'This is the category where paying more can make sense — if scale is actually what you want. Compare the production concept first, then use starting price and seating context to decide what is worth the splurge.',
      take:'Big does not automatically mean better. But if you came to Vegas specifically for something you cannot reproduce in a normal theater, this is the category where the premium can make sense.'
    },
    '/shows/family/': {
      accent:'#52b7f6', accent2:'#c6f22e', eyebrow:'FAMILY-FRIENDLY VEGAS · 2026', title:'Las Vegas Family Shows',
      metaTitle:'Las Vegas Family Shows 2026 | Compare Kid-Friendly Options | Vegas Sidekick',
      meta:'Compare Las Vegas family shows across magic, comedy, acrobatics and variety. See venues, starting prices and age guidance before planning a night with kids.',
      sub:'Magic, comedy, acrobatics and spectacle that can work for a family night. Check the individual age guidance before you book.',
      intro:'Family-friendly does not always mean “made for little kids.” Some shows are true all-ages productions; others simply work well for families with older kids. The individual listing matters.',
      thirdNum:'Plan', thirdLabel:'Check age guidance',
      guideKicker:'QUICK WAY TO NARROW IT DOWN', guideTitle:'Match the show to the kids, not just the category label.', guideCopy:'Age, attention span and showtime matter more here than almost anywhere else on the site.',
      choices:[['Younger kids','Look for clear visual storytelling, animals, magic or physical comedy that does not depend on following a long plot.'],['Older kids / teens','Big illusion, acrobatics and higher-energy variety can open up a much wider set of options.'],['Mixed-age group','Prioritize a broadly visual show and a schedule that works for the youngest person in the group.']],
      bottomTitle:'Choosing a family show in Las Vegas', bottomCopy:'Use the category as a starting point, then check the individual show page for age guidance, runtime and showtime. “Family-friendly” is not a substitute for knowing whether the specific kid in your group will enjoy it.',
      take:'Kid-friendly and kid-targeted are not the same thing. I would rather put a family into a strong visual show everyone can enjoy than pick something just because the word “family” appears in the marketing.'
    },
    '/shows/adult/': {
      accent:'#ff2e7e', accent2:'#8b5cf6', eyebrow:'LAS VEGAS AFTER DARK · 2026', title:'Las Vegas Adult Shows',
      metaTitle:'Las Vegas Adult Shows 2026 | Compare 18+ Shows | Vegas Sidekick',
      meta:'Compare Las Vegas adult shows, including burlesque, male revues, adults-only comedy, circus and parody. See venues, starting prices and the tradeoffs worth knowing before you book.',
      sub:'Burlesque, male revues, adults-only comedy, circus and parody. Compare the vibe, venue and starting price before you pick your night. Age rules vary by show, so check the individual listing before booking.',
      intro:'Vegas adult entertainment covers more ground than the label suggests. Some shows are polished burlesque revues, some are high-energy dance productions, and some lean into comedy, circus or parody. Use the cards below to compare starting price, venue and tone — then open the individual show page for the details that actually matter.',
      thirdNum:'18+/21+', thirdLabel:'Check each show',
      guideKicker:'QUICK WAY TO NARROW IT DOWN', guideTitle:'Pick the kind of night you actually want.', guideCopy:'“Adult show” is a broad bucket in Vegas. Start with the experience, then compare price.',
      choices:[['Classic revue / burlesque','Best when choreography, costumes and a traditional Vegas after-dark production are the point.'],['Crowd-energy dance show','Best when audience interaction, party energy and a louder room are what you want.'],['Comedy / circus / parody','Best when you want the adult material wrapped inside a bigger theatrical or comic idea.']],
      bottomTitle:'What “adult show” means in Vegas', bottomCopy:'Vegas uses the adult-show label for several different experiences: topless or burlesque revues, male dance productions, raunchier comedy, circus and parody. Compare the vibe first. Then use starting price and venue to narrow the list.',
      take:'I would not start by asking which adult show is “best.” Start by deciding whether you want a revue, a party-style dance show or something funny and theatrical. Those are three different nights wearing the same category label.'
    }
  };

  const cfg = CONFIG[PATH];
  if (!cfg || document.documentElement.dataset.vsCategoryV2 === '1') return;
  document.documentElement.dataset.vsCategoryV2 = '1';
  document.documentElement.style.setProperty('--v2-accent', cfg.accent);
  document.documentElement.style.setProperty('--v2-accent2', cfg.accent2);

  function setMeta(selector, value) {
    const node = document.querySelector(selector);
    if (node && value) node.setAttribute('content', value);
  }
  document.title = cfg.metaTitle;
  setMeta('meta[name="description"]', cfg.meta);
  setMeta('meta[property="og:title"]', cfg.metaTitle.replace(' | Vegas Sidekick',''));
  setMeta('meta[property="og:description"]', cfg.meta);

  const styles = document.createElement('style');
  styles.id = 'vs-category-v2-styles';
  styles.textContent = `
    body{background:#f7f6fb}
    .age-banner{display:none!important}
    .cat-hero{padding:118px 24px 46px;background:
      radial-gradient(900px 460px at 82% 12%,color-mix(in srgb,var(--v2-accent) 24%,transparent),transparent 62%),
      radial-gradient(760px 420px at 8% 95%,color-mix(in srgb,var(--v2-accent2) 22%,transparent),transparent 68%),
      linear-gradient(155deg,#1b0935 0%,#2b0f55 58%,#13071f 100%)}
    .cat-hero::before{background:radial-gradient(ellipse at 72% 44%,color-mix(in srgb,var(--v2-accent) 13%,transparent),transparent 58%)}
    .cat-hero::after{height:2px;background:linear-gradient(90deg,#ff2e7e,#7c3aed,#0fb5c9,#c6f22e)}
    .cat-hero-inner{max-width:1000px}
    .cat-badge{color:color-mix(in srgb,var(--v2-accent) 58%,white);font-weight:600;letter-spacing:.13em}
    .cat-badge-dot{background:var(--v2-accent);box-shadow:0 0 12px color-mix(in srgb,var(--v2-accent) 70%,transparent)}
    .cat-headline{font-size:clamp(2.7rem,6vw,4.9rem);line-height:.98;letter-spacing:-.045em;max-width:820px;margin-bottom:16px}
    .cat-sub{max-width:720px;color:rgba(255,255,255,.76);font-size:1rem;line-height:1.65;margin-bottom:25px}
    .cat-stats{gap:12px}
    .cat-stat{min-width:118px;padding:11px 14px;border:1px solid rgba(255,255,255,.1);background:rgba(255,255,255,.055);border-radius:12px;backdrop-filter:blur(8px)}
    .cat-stat-num{font-size:1.15rem;color:#fff;letter-spacing:-.02em}
    .cat-stat-lbl{font-family:'Inter',sans-serif;font-size:.64rem;color:#bdb0c8;letter-spacing:.02em;text-transform:none;margin-top:3px}
    .v2-hero-media{display:none;position:relative;overflow:hidden;border-radius:15px;border:1px solid rgba(255,255,255,.16);background:#170925;box-shadow:0 16px 38px rgba(0,0,0,.28);margin:0 0 22px;aspect-ratio:16/9}
    .v2-hero-media img{width:100%;height:100%;object-fit:cover;object-position:center;display:block}
    .v2-hero-media:after{content:'';position:absolute;inset:auto 0 0;height:42%;background:linear-gradient(transparent,rgba(12,4,22,.72));pointer-events:none}
    .v2-hero-caption{position:absolute;z-index:2;left:12px;right:12px;bottom:10px;color:#fff;font:700 .7rem 'Plus Jakarta Sans',sans-serif;text-shadow:0 1px 10px rgba(0,0,0,.6)}
    .cat-nav-bar{border-bottom:1px solid #ece9f6;padding:10px 24px;background:rgba(255,255,255,.96)}
    .cat-nav-bar-inner{max-width:1200px}
    .cat-nav-link{font-family:'Inter',sans-serif;font-size:.76rem;letter-spacing:0;border:1px solid #e8e4f0;background:#f7f6fb}
    .cat-nav-link.current{background:#281047;border-color:#281047}
    .cat-intro{padding:28px 24px 22px;background:#fff;border-bottom:0}
    .cat-intro-inner{max-width:900px}
    .cat-intro p{font-size:.98rem;line-height:1.72;color:#49415b}
    .v2-guide{max-width:1200px;margin:0 auto;padding:10px 24px 22px}
    .v2-guide-inner{background:linear-gradient(110deg,#fff,#faf8ff);border:1px solid #e8e3f0;border-radius:16px;padding:20px;box-shadow:0 8px 28px rgba(41,16,71,.055)}
    .v2-guide-kicker{font:800 .68rem 'Plus Jakarta Sans',sans-serif;color:var(--v2-accent);text-transform:uppercase;letter-spacing:.12em;margin-bottom:7px}
    .v2-guide h2{font:800 clamp(1.28rem,2vw,1.65rem) 'Plus Jakarta Sans',sans-serif;color:#21152f;letter-spacing:-.035em;margin:0 0 7px}
    .v2-guide-copy{color:#6d6478;font-size:.9rem;line-height:1.6;margin:0 0 16px;max-width:760px}
    .v2-choices{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
    .v2-choice{padding:13px 14px;border-radius:11px;background:#f7f4fb;border:1px solid #ebe6f1}
    .v2-choice b{display:block;font:700 .83rem 'Plus Jakarta Sans',sans-serif;color:#28163c;margin-bottom:4px}
    .v2-choice span{display:block;color:#71677b;font-size:.76rem;line-height:1.45}
    .filter-bar{position:sticky;top:88px;margin:0;background:transparent;border:0;box-shadow:none;padding:10px 24px;z-index:100}
    .filter-bar-inner{max-width:1200px;background:#fff;border:1px solid #e8e4ef;border-radius:14px;padding:9px 10px;box-shadow:0 6px 20px rgba(39,17,61,.07)}
    .filter-btn,.sort-btn{font-family:'Inter',sans-serif;font-size:.76rem;letter-spacing:0;padding:7px 13px}
    .filter-btn.active:not([class*="fb-"]),.sort-btn.active{background:#281047!important;border-color:#281047!important;color:#fff!important}
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
    .card-age-badge,.card-cat-tag{background:rgba(25,10,45,.88);border:1px solid rgba(255,255,255,.24);font-size:.54rem;border-radius:6px}
    .cat-desc{display:none!important}
    .v2-bottom{background:#fff;border-top:1px solid #ece8f0;padding:48px 24px 60px}
    .v2-bottom-inner{max-width:900px;margin:0 auto}
    .v2-bottom h2{font:800 clamp(1.55rem,3vw,2.15rem) 'Plus Jakarta Sans',sans-serif;color:#21152f;letter-spacing:-.04em;margin:0 0 12px}
    .v2-bottom>div>p{color:#635a6d;line-height:1.72;font-size:.94rem;margin:0 0 22px}
    .v2-take{background:#f6f2fb;border:1px solid #e7dff0;border-left:4px solid var(--v2-accent);border-radius:12px;padding:17px 18px;margin:22px 0}
    .v2-take b{display:block;font:800 .75rem 'Plus Jakarta Sans',sans-serif;color:#28163c;margin-bottom:6px}
    .v2-take p{margin:0!important;color:#554b60!important;font-size:.88rem!important;line-height:1.65!important}
    .v2-links{display:flex;flex-wrap:wrap;gap:9px;margin-top:20px}
    .v2-links a{padding:9px 13px;border-radius:9px;text-decoration:none;font:700 .76rem 'Plus Jakarta Sans',sans-serif;border:1px solid #e3dce9;background:#faf8fc;color:#28163c}
    .v2-links a:hover{border-color:var(--v2-accent);color:var(--v2-accent)}
    @media(max-width:940px){.filter-bar{top:54px}}
    @media(max-width:700px){.cat-hero{padding:72px 18px 34px}.v2-hero-media{display:block}.cat-badge{font-size:.62rem;margin-bottom:12px}.cat-headline{font-size:clamp(2.35rem,11.5vw,3.45rem);line-height:1;max-width:none;margin-bottom:14px}.cat-sub{font-size:.94rem;line-height:1.58;margin-bottom:20px}.cat-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.cat-stat{min-width:0;padding:10px 10px}.cat-stat-num{font-size:1rem}.cat-stat-lbl{font-size:.58rem}.cat-nav-bar{padding:9px 14px}.cat-intro{padding:24px 20px 18px}.cat-intro p{font-size:.92rem;line-height:1.68}.v2-guide{padding:8px 14px 20px}.v2-guide-inner{padding:18px 16px}.v2-choices{grid-template-columns:1fr}.filter-bar{padding:8px 12px}.filter-bar-inner{padding:8px;border-radius:12px}.grid-wrap{padding:8px 14px 38px}.v2-bottom{padding:38px 20px 50px}}
    @media(max-width:520px){.show-grid{gap:0}.show-card{border-radius:0;box-shadow:none;border-left:0;border-right:0;background:transparent}.show-card:hover{box-shadow:none}.card-body{padding:0}.card-name{font-size:1.08rem}.card-price{font-size:1.55rem!important}}
    @media(prefers-reduced-motion:reduce){.cat-badge-dot{animation:none}}
  `;
  document.head.appendChild(styles);

  const badge = document.querySelector('.cat-badge');
  const headline = document.querySelector('.cat-headline');
  const sub = document.querySelector('.cat-sub');
  if (badge) badge.innerHTML = '<span class="cat-badge-dot"></span>' + cfg.eyebrow;
  if (headline) headline.textContent = cfg.title;
  if (sub) sub.textContent = cfg.sub;

  const intro = document.querySelector('.cat-intro p');
  if (intro) intro.textContent = cfg.intro;

  if (PATH === '/shows/') {
    const categoryUrls = {
      all:'/shows/', comedy:'/shows/comedy/', magic:'/shows/magic/', cirque:'/shows/cirque/',
      music:'/shows/music/', spectaculars:'/shows/spectaculars/', family:'/shows/family/', adult:'/shows/adult/'
    };
    const filterWrap = document.getElementById('cat-filter-btns');
    if (filterWrap) {
      const row = filterWrap.closest('.filter-row');
      const label = row && row.querySelector('.filter-label');
      if (label) label.textContent = 'Browse category';
      filterWrap.addEventListener('click', function (e) {
        const btn = e.target.closest('button');
        if (!btn || !filterWrap.contains(btn)) return;
        const match = Array.from(btn.classList).find(c => c.indexOf('fb-') === 0);
        const key = match ? match.replace('fb-','').replace('specs','spectaculars') : null;
        const url = key && categoryUrls[key];
        if (!url) return;
        e.preventDefault();
        e.stopImmediatePropagation();
        window.location.href = url;
      }, true);
    }
  }

  function getCards() { return Array.from(document.querySelectorAll('#show-grid .show-card, .show-grid .show-card')); }
  function priceValues(cards) {
    return cards.map(card => {
      const t = card.querySelector('.card-price');
      if (!t) return NaN;
      return Number((t.textContent || '').replace(/[^0-9.]/g,''));
    }).filter(n => Number.isFinite(n) && n > 0);
  }

  const cards = getCards();
  const prices = priceValues(cards);
  const count = cards.length;
  const low = prices.length ? Math.min.apply(null, prices) : null;
  const stats = document.querySelectorAll('.cat-stat');
  if (stats[0]) stats[0].innerHTML = '<div class="cat-stat-num">' + count + '</div><div class="cat-stat-lbl">Shows to compare</div>';
  if (stats[1]) stats[1].innerHTML = '<div class="cat-stat-num">' + (low ? '$' + Math.round(low) : 'Compare') + '</div><div class="cat-stat-lbl">' + (low ? 'Lowest listed start' : 'Starting prices') + '</div>';
  if (stats[2]) stats[2].innerHTML = '<div class="cat-stat-num">' + cfg.thirdNum + '</div><div class="cat-stat-lbl">' + cfg.thirdLabel + '</div>';

  const heroInner = document.querySelector('.cat-hero-inner');
  const firstImage = document.querySelector('#show-grid .show-card img, .show-grid .show-card img');
  if (heroInner && firstImage && !heroInner.querySelector('.v2-hero-media')) {
    const media = document.createElement('div');
    media.className = 'v2-hero-media';
    const img = document.createElement('img');
    img.src = firstImage.currentSrc || firstImage.src;
    img.alt = firstImage.alt || cfg.title;
    img.loading = 'eager';
    img.decoding = 'async';
    const caption = document.createElement('div');
    caption.className = 'v2-hero-caption';
    const card = firstImage.closest('.show-card');
    const showName = card && card.querySelector('.card-name') ? card.querySelector('.card-name').textContent.trim() : '';
    caption.textContent = showName ? 'One of the shows in this category: ' + showName : 'Browse the current Vegas lineup';
    media.appendChild(img); media.appendChild(caption);
    heroInner.insertBefore(media, heroInner.firstChild);
  }

  const introSection = document.querySelector('.cat-intro');
  if (introSection && !document.querySelector('.v2-guide')) {
    const guide = document.createElement('section');
    guide.className = 'v2-guide';
    guide.setAttribute('aria-labelledby','v2-guide-title');
    guide.innerHTML = '<div class="v2-guide-inner"><div class="v2-guide-kicker">' + cfg.guideKicker + '</div><h2 id="v2-guide-title">' + cfg.guideTitle + '</h2><p class="v2-guide-copy">' + cfg.guideCopy + '</p><div class="v2-choices">' + cfg.choices.map(c => '<div class="v2-choice"><b>' + c[0] + '</b><span>' + c[1] + '</span></div>').join('') + '</div></div>';
    introSection.insertAdjacentElement('afterend', guide);
  }

  const footer = document.getElementById('vs-footer');
  if (footer && !document.querySelector('.v2-bottom')) {
    const bottom = document.createElement('section');
    bottom.className = 'v2-bottom';
    bottom.innerHTML = '<div class="v2-bottom-inner"><h2>' + cfg.bottomTitle + '</h2><p>' + cfg.bottomCopy + '</p><div class="v2-take"><b>🌵 Kris’s take</b><p>' + cfg.take + '</p></div><div class="v2-links"><a href="/guides/">Browse Vegas Guides</a><a href="/guides/best-cheap-vegas-shows/">Deals Under $50</a><a href="/guides/best-shows-for-first-timers/">First-Timer Guide</a><a href="/venues/">Shows by Venue</a></div></div>';
    footer.insertAdjacentElement('beforebegin', bottom);
  }
})();