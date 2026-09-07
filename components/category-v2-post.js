// Vegas Sidekick — Category V2 post-catalog guidance patch
// Keeps show inventory first; moves optional decision help below the catalog.
(function(){
  'use strict';

  const PATH = location.pathname;
  const COPY = {
    '/shows/': [
      ['Big visual night','Cirque or Spectaculars for scale and production.'],
      ['Personality-driven night','Comedy, magic or music when the performer is the point.'],
      ['Planning for a group','Use the category pages to compare age fit, venue and budget.']
    ],
    '/shows/comedy/': [
      ['Resident headliner','Specific performer, polished Vegas production.'],
      ['Comedy club','Several comics, smaller room, traditional stand-up.'],
      ['Visual or hybrid comedy','Props, interaction or a bigger stage concept.']
    ],
    '/shows/magic/': [
      ['Close-up / mentalism','Technique, mind-reading and a more intimate room.'],
      ['Comedy magic','Laughs and personality alongside the tricks.'],
      ['Big illusion','Large-scale staging and classic Vegas spectacle.']
    ],
    '/shows/cirque/': [
      ['Dreamlike spectacle','Atmosphere, choreography and visual composition.'],
      ['Technical centerpiece','Water, machinery or stage engineering as part of the draw.'],
      ['Lighter energy','Acrobatics with more humor and less seriousness.']
    ],
    '/shows/music/': [
      ['Resident performer','Choose this when the artist is the reason you are going.'],
      ['Tribute / catalog show','Choose for familiar songs and nostalgia.'],
      ['Dance / variety production','Music inside a larger visual Vegas show.']
    ],
    '/shows/spectaculars/': [
      ['Immersive / technology-led','Screens, effects or the venue itself are part of the attraction.'],
      ['Stagecraft-led','Choreography, machinery or theatrical design carry the night.'],
      ['Classic Vegas scale','A polished production built to feel big.']
    ],
    '/shows/family/': [
      ['Younger kids','Favor clear visuals, magic, animals or physical comedy.'],
      ['Older kids / teens','Big illusion, acrobatics and higher-energy variety open up more options.'],
      ['Mixed-age group','Prioritize broad visual appeal and a workable showtime.']
    ],
    '/shows/adult/': [
      ['Classic revue / burlesque','Choreography, costumes and traditional Vegas after-dark production.'],
      ['Crowd-energy dance show','Audience interaction, party energy and a louder room.'],
      ['Comedy / circus / parody','Adult material wrapped in a bigger theatrical or comic idea.']
    ]
  };

  if (!COPY[PATH]) return;

  function apply(){
    const guide = document.querySelector('.v2-guide');
    const gridWrap = document.querySelector('.grid-wrap');
    if (!guide || !gridWrap) return false;
    if (guide.dataset.postCatalog === '1') return true;

    guide.dataset.postCatalog = '1';
    gridWrap.insertAdjacentElement('afterend', guide);

    const kicker = guide.querySelector('.v2-guide-kicker');
    if (kicker) kicker.textContent = 'NEED HELP NARROWING IT DOWN?';

    const copy = guide.querySelector('.v2-guide-copy');
    if (copy) copy.textContent = 'A quick cheat sheet if the show list still feels too broad.';

    const choices = guide.querySelectorAll('.v2-choice');
    COPY[PATH].forEach(function(item, i){
      const choice = choices[i];
      if (!choice) return;
      const title = choice.querySelector('b');
      const desc = choice.querySelector('span');
      if (title) title.textContent = item[0];
      if (desc) desc.textContent = item[1];
    });

    if (!document.getElementById('vs-category-post-styles')) {
      const style = document.createElement('style');
      style.id = 'vs-category-post-styles';
      style.textContent = `
        .v2-guide{max-width:1200px;margin:0 auto;padding:0 24px 36px}
        .v2-guide-inner{padding:18px 20px;background:#fff;border-color:#e8e3f0;box-shadow:none}
        .v2-guide-kicker{font-size:.62rem;margin-bottom:6px}
        .v2-guide h2{font-size:clamp(1.18rem,2vw,1.45rem);margin-bottom:5px}
        .v2-guide-copy{font-size:.82rem;line-height:1.5;margin-bottom:13px}
        .v2-choices{gap:8px}
        .v2-choice{padding:11px 12px;background:#f8f6fb}
        .v2-choice b{font-size:.78rem;margin-bottom:3px}
        .v2-choice span{font-size:.7rem;line-height:1.4}
        @media(max-width:700px){
          .v2-guide{padding:0 14px 28px}
          .v2-guide-inner{padding:16px 14px}
          .v2-choices{grid-template-columns:1fr;gap:7px}
          .v2-choice{padding:10px 11px}
        }
      `;
      document.head.appendChild(style);
    }
    return true;
  }

  if (apply()) return;
  let tries = 0;
  const timer = setInterval(function(){
    tries++;
    if (apply() || tries > 40) clearInterval(timer);
  }, 75);
})();