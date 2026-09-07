/* Vegas Sidekick — canonical show-page runtime v1
   Shared interaction layer for show detail pages. Keeps page-specific content/schema in HTML. */
(function(){
  'use strict';
  var path=location.pathname;
  if(!/^\/shows\/(comedy|magic|cirque|music|spectaculars|family|adult)\/[^/]+\/?$/.test(path)) return;

  function addStyle(){
    if(document.getElementById('vs-canonical-runtime-style')) return;
    var s=document.createElement('style'); s.id='vs-canonical-runtime-style';
    s.textContent=`
      .vs-runtime-clickable-day{cursor:pointer;transition:transform .18s,box-shadow .18s,border-color .18s}.vs-runtime-clickable-day:hover,.vs-runtime-clickable-day:focus-visible{transform:translateY(-2px);box-shadow:0 10px 24px rgba(66,24,100,.12);border-color:#8b5cf6!important;outline:none}.vs-runtime-clickable-day:after{content:'Tickets →';display:block;margin-top:7px;font:700 .62rem 'Plus Jakarta Sans',sans-serif;color:#ff6b35;letter-spacing:.04em}
      .faq details summary::before{transition:transform .3s cubic-bezier(.2,.9,.2,1),box-shadow .3s!important}.faq details[open] summary::before{content:'+'!important;transform:rotate(45deg) scale(1.08);box-shadow:0 0 0 6px rgba(124,58,237,.12)}
      .faq-icon,.plus,.sv-faq-q span:last-child{transition:transform .3s cubic-bezier(.2,.9,.2,1),box-shadow .3s!important}.faq-item.open .faq-icon,.faq-row.open .plus,.sv-faq-item.open .sv-faq-q span:last-child{transform:rotate(45deg) scale(1.08)}
      .vs-runtime-fit{padding:72px 0;background:#f5f0ff}.vs-runtime-wrap{width:min(1120px,calc(100% - 36px));margin:auto}.vs-runtime-eyebrow{font:700 .72rem 'Plus Jakarta Sans',sans-serif;letter-spacing:.12em;text-transform:uppercase;color:#f43f8c;margin-bottom:10px}.vs-runtime-fit h2,.vs-runtime-related h2,.vs-runtime-next h2{font:800 clamp(2rem,4.4vw,3.5rem) 'Plus Jakarta Sans',sans-serif;letter-spacing:-.045em;line-height:1.05;color:#17082e;margin:0 0 18px}.vs-runtime-fit-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;max-width:900px}.vs-runtime-fit-card{background:#fff;border:1px solid #e9e2f2;border-radius:18px;padding:24px;border-top:7px solid #c6f22e}.vs-runtime-fit-card.think{border-top-color:#f43f8c}.vs-runtime-fit-card h3{font:800 1.18rem 'Plus Jakarta Sans',sans-serif;margin:0 0 9px;color:#17082e}.vs-runtime-fit-card p{margin:0;color:#62596d;line-height:1.65}
      .vs-runtime-related,.vs-runtime-next{padding:72px 0}.vs-runtime-related-grid,.vs-runtime-next-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:26px}.vs-runtime-related-card{border:1px solid #e9e2f2;border-radius:16px;overflow:hidden;background:#fff;transition:.2s}.vs-runtime-related-card:hover{transform:translateY(-3px);box-shadow:0 12px 30px rgba(35,12,60,.12)}.vs-runtime-related-card img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block}.vs-runtime-related-card div{padding:15px}.vs-runtime-related-card strong{display:block;font:800 1rem 'Plus Jakarta Sans',sans-serif}.vs-runtime-related-card span{font-size:.82rem;color:#696176}.vs-runtime-next{background:linear-gradient(135deg,#f5efff,#fff7fb)}.vs-runtime-next-card{display:block;background:#fff;border:1px solid #e9e2f2;border-radius:18px;padding:24px;border-top:7px solid var(--vs-accent,#7c3aed);min-height:145px}.vs-runtime-next-card h3{font:800 1.05rem 'Plus Jakarta Sans',sans-serif;margin:0 0 8px;color:#17082e}.vs-runtime-next-card p{margin:0;color:#62596d;line-height:1.55;font-size:.93rem}
      @media(max-width:800px){.vs-runtime-fit-grid,.vs-runtime-related-grid,.vs-runtime-next-grid{grid-template-columns:1fr}.vs-runtime-fit,.vs-runtime-related,.vs-runtime-next{padding:60px 0}.vs-runtime-next-card{min-height:0}}
      @media(prefers-reduced-motion:reduce){.vs-runtime-clickable-day,.faq details summary::before,.faq-icon,.plus,.sv-faq-q span:last-child{transition:none!important}}
    `;
    document.head.appendChild(s);
  }

  function ticketUrl(){
    var a=document.querySelector('a[href*="spotlight.vegas"]');
    return a ? a.href : '';
  }

  function countFacts(){
    if(matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    var nodes=[].slice.call(document.querySelectorAll('.fact strong,.stat .n,.stat-num,.sv-fact b'));
    var seen=[];
    nodes.forEach(function(el){
      if(seen.indexOf(el)>=0 || el.dataset.vsCounted) return; seen.push(el);
      var raw=(el.textContent||'').trim();
      var m=raw.match(/^([^0-9]*)(\d+(?:\.\d+)?)(.*)$/); if(!m) return;
      var target=parseFloat(m[2]); if(!isFinite(target)||target<=0) return;
      el.dataset.vsCounted='1';
      var prefix=m[1], suffix=m[3], decimals=(m[2].split('.')[1]||'').length;
      var startAt=performance.now(), dur=720;
      function tick(now){var p=Math.min((now-startAt)/dur,1),e=1-Math.pow(1-p,3),v=target*e;el.textContent=prefix+(decimals?v.toFixed(decimals):Math.round(v))+suffix;if(p<1)requestAnimationFrame(tick)}
      var io=new IntersectionObserver(function(entries){entries.forEach(function(en){if(en.isIntersecting){el.textContent=prefix+'0'+suffix;requestAnimationFrame(tick);io.disconnect()}})},{threshold:.45});io.observe(el);
    });
  }

  function makeScheduleClickable(){
    var url=ticketUrl(); if(!url) return;
    var sel='.schedule .day:not(.dark),.daygrid .day:not(.dark),.sk-row:not(.is-dark),.schedule-grid .day-card:not(.dark)';
    document.querySelectorAll(sel).forEach(function(el){
      if(el.closest('a[href*="spotlight.vegas"]')||el.dataset.vsDayLink) return;
      var txt=(el.textContent||'').toLowerCase(); if(txt.indexOf('dark')>=0||txt.indexOf('no show')>=0)return;
      el.dataset.vsDayLink='1';el.classList.add('vs-runtime-clickable-day');el.tabIndex=0;el.setAttribute('role','link');el.setAttribute('aria-label',(el.textContent||'Showtime').trim()+' — see tickets');
      function go(){window.open(url,'_blank','noopener')}
      el.addEventListener('click',go);el.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();go()}});
    });
  }

  function faqAnimation(){
    document.querySelectorAll('.sv-faq-item').forEach(function(item){var b=item.querySelector('.sv-faq-q');if(!b)return;b.addEventListener('click',function(){setTimeout(function(){item.classList.toggle('open',b.getAttribute('aria-expanded')==='true')},0)})});
  }

  function category(){var m=path.match(/^\/shows\/([^/]+)\//);return m?m[1]:''}
  var CAT={
    comedy:{label:'Comedy',good:'You want laughs and personality to drive the night.',think:'You are really shopping for magic, Cirque or a large-scale visual spectacle.',guide:'/guides/best-comedy-shows/'},
    magic:{label:'Magic',good:'You want illusions, mind-reading or sleight-of-hand to be the main event.',think:'You are really looking for a concert, Cirque production or traditional Vegas revue.',guide:'/guides/best-magic-shows/'},
    cirque:{label:'Cirque & Acrobatic',good:'You want physical spectacle, acrobatics and visual stagecraft.',think:'You are really looking for a magic show, stand-up set or singer-led concert.',guide:'/guides/best-cirque-shows/'},
    music:{label:'Music & Variety',good:'You want music, performers and stage energy to carry the night.',think:'You are really shopping for close-up magic, stand-up comedy or a Cirque-first production.',guide:'/guides/'},
    spectaculars:{label:'Spectaculars',good:'You want the production itself — scale, effects and visual spectacle — to be the attraction.',think:'You would rather spend the night with a single comedian, magician or singer as the clear focus.',guide:'/guides/'},
    family:{label:'Family Shows',good:'You want something a mixed-age group can enjoy together.',think:'Your group specifically wants an adults-only night or late-night edge.',guide:'/guides/best-shows-for-families/'},
    adult:{label:'Adult Shows',good:'You want a grown-up Vegas night with more edge than the family catalog.',think:'You need an all-ages show or are bringing younger guests.',guide:'/guides/'}
  };

  function currentRecord(){var p=path.endsWith('/')?path:path+'/';return (window.VS_SHOWS||[]).find(function(s){return s.url===p})||null}
  function hasHeading(phrase){return [].some.call(document.querySelectorAll('h2,h3'),function(h){return (h.textContent||'').toLowerCase().indexOf(phrase)>=0})}
  function insertBeforeFooter(sec){var f=document.getElementById('vs-footer')||document.querySelector('footer');if(f&&f.parentNode)f.parentNode.insertBefore(sec,f);else document.body.appendChild(sec)}

  function ensureFit(){
    if(hasHeading('good fit')||hasHeading('think twice')||document.querySelector('.decision-card.good,.fit-grid')) return;
    var c=CAT[category()]; if(!c)return;
    var sec=document.createElement('section');sec.className='vs-runtime-fit';sec.id='fit';sec.innerHTML='<div class="vs-runtime-wrap"><div class="vs-runtime-eyebrow">Is it for you?</div><h2>Good fit / Think twice</h2><div class="vs-runtime-fit-grid"><div class="vs-runtime-fit-card"><h3>Good fit</h3><p>'+c.good+'</p></div><div class="vs-runtime-fit-card think"><h3>Think twice</h3><p>'+c.think+'</p></div></div></div>';
    var faq=[].find.call(document.querySelectorAll('section,div.section,.sv-section'),function(x){return x.id==='faq'||x.querySelector&&x.querySelector('.faq,.sv-faq')});
    if(faq&&faq.parentNode)faq.parentNode.insertBefore(sec,faq);else insertBeforeFooter(sec);
  }

  function ensureRelated(){
    if(hasHeading('you may also like')||document.querySelector('[data-vs-picks],.related,.also-grid,.sv-related')) return;
    if(!window.VS_SHOWS||!window.VS_SHOWS.length)return;
    var self=currentRecord(),cat=category(),list=window.VS_SHOWS.filter(function(s){return s.url!==path&&s.url!==path+'/'&&s.url.indexOf('/shows/'+cat+'/')===0&&s.img}).slice(0,3);if(list.length<3)return;
    var sec=document.createElement('section');sec.className='vs-runtime-related';sec.innerHTML='<div class="vs-runtime-wrap"><div class="vs-runtime-eyebrow">Keep comparing</div><h2>You may also like</h2><div class="vs-runtime-related-grid">'+list.map(function(s){return '<a class="vs-runtime-related-card" href="'+s.url+'"><img src="'+s.img+'" alt="'+s.name+' Las Vegas show" loading="lazy"><div><strong>'+s.name+'</strong><span>'+((s.sub||s.venue||s.cat)||'')+'</span></div></a>'}).join('')+'</div></div>';
    insertBeforeFooter(sec);
  }

  function ensureNext(){
    if(hasHeading('make the next click useful')) return;
    var c=CAT[category()];if(!c)return;
    var venue=document.querySelector('a[href^="/venues/"]');var venueHref=venue?venue.getAttribute('href'):'/venues/';var venueName=venue?(venue.textContent||'this venue').replace(/^\s*[📍🚝]+\s*/,'').trim():'the venue';
    var sec=document.createElement('section');sec.className='vs-runtime-next';sec.innerHTML='<div class="vs-runtime-wrap"><div class="vs-runtime-eyebrow">Still deciding?</div><h2>Make the next click useful</h2><div class="vs-runtime-next-grid"><a class="vs-runtime-next-card" style="--vs-accent:#7c3aed" href="/shows/'+category()+'/"><h3>Compare '+c.label+' shows →</h3><p>See the full category before you lock in the night.</p></a><a class="vs-runtime-next-card" style="--vs-accent:#0fb5c9" href="'+venueHref+'"><h3>Explore '+venueName+' shows →</h3><p>See what else is playing nearby before adding another trip across the Strip.</p></a><a class="vs-runtime-next-card" style="--vs-accent:#f43f8c" href="'+c.guide+'"><h3>Open a Vegas Sidekick guide →</h3><p>Use the guide when you want recommendations instead of another long list.</p></a></div></div>';
    insertBeforeFooter(sec);
  }

  function run(){addStyle();countFacts();makeScheduleClickable();faqAnimation();ensureFit();ensureRelated();ensureNext()}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',function(){setTimeout(run,0)});else setTimeout(run,0);
})();
