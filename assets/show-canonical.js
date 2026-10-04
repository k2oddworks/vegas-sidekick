(function(){
  'use strict';

  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const progress=document.querySelector('.progress'),mobileProgress=document.getElementById('mobileProgress');
  function prog(){
    const d=document.documentElement,max=d.scrollHeight-innerHeight,p=max?Math.min(100,scrollY/max*100):0;
    if(progress)progress.style.width=p+'%';
    if(mobileProgress)mobileProgress.style.width=p+'%';
  }
  addEventListener('scroll',prog,{passive:true});
  prog();

  if(!reduce){
    document.querySelectorAll('.fact strong[data-count]').forEach(el=>{
      const target=parseFloat(el.dataset.count);
      if(!isFinite(target))return;
      const prefix=el.dataset.prefix||'',suffix=el.dataset.suffix||'';
      let done=false;
      const io=new IntersectionObserver(es=>es.forEach(en=>{
        if(!en.isIntersecting||done)return;
        done=true;
        io.disconnect();
        const start=performance.now(),dur=720;
        function tick(now){
          const p=Math.min(1,(now-start)/dur),e=1-Math.pow(1-p,3);
          el.textContent=prefix+Math.round(target*e)+suffix;
          if(p<1)requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
      }),{threshold:.35});
      io.observe(el);
    });
  }

  const detail=document.getElementById('seat-detail');
  document.querySelectorAll('.seat-zone').forEach(btn=>btn.addEventListener('click',()=>{
    document.querySelectorAll('.seat-zone').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    if(detail){
      detail.querySelector('.tag').textContent=btn.dataset.tag||'Seat guide';
      detail.querySelector('h3').textContent=btn.dataset.title||'';
      detail.querySelector('p').textContent=btn.dataset.copy||'';
    }
  }));

  /* Upgrade legacy show photo grids to the shared Absinthe-style viewer. */
  function upgradeShowGalleries(){
    document.querySelectorAll('#photos .gallery').forEach(old=>{
      if(old.closest('[data-show-gallery]'))return;
      const buttons=Array.from(old.querySelectorAll('button')).filter(b=>b.querySelector('img'));
      if(!buttons.length)return;

      const root=document.createElement('div');
      root.className='vs-show-gallery';
      root.setAttribute('data-show-gallery','');
      root.setAttribute('role','region');
      const heading=old.closest('#photos')&&old.closest('#photos').querySelector('h2');
      root.setAttribute('aria-label',(heading?heading.textContent.trim():'Show')+' gallery');

      const track=document.createElement('div');
      track.className='vs-gallery-track';
      buttons.forEach(b=>{
        const img=b.querySelector('img');
        const clue=((b.className||'')+' '+(b.getAttribute('aria-label')||'')+' '+(img.alt||'')+' '+(img.getAttribute('src')||'')).toLowerCase();
        const isChart=/seating|seat[-_ ]?chart|chart-gallery/.test(clue);
        b.classList.add('vs-gallery-slide');
        b.type='button';
        if(isChart){
          b.dataset.chart='true';
          if(!b.querySelector('.vs-gallery-label')){
            const label=document.createElement('span');
            label.className='vs-gallery-label';
            label.textContent='Seating chart';
            b.append(label);
          }
        }
        track.append(b);
      });
      root.append(track);
      old.replaceWith(root);
    });

    document.querySelectorAll('#photos h2').forEach(h=>{
      h.classList.add('vs-gallery-heading');
      if(!(h.children.length===1&&h.firstElementChild&&h.firstElementChild.tagName==='SPAN')){
        const span=document.createElement('span');
        while(h.firstChild)span.append(h.firstChild);
        h.append(span);
      }
    });

    if(!document.querySelector('[data-show-gallery]'))return;
    if(!document.querySelector('link[href*="/assets/show-gallery.css"]')){
      const link=document.createElement('link');
      link.rel='stylesheet';
      link.href='/assets/show-gallery.css?v=4';
      document.head.append(link);
    }
    if(!document.querySelector('script[data-vs-gallery-loader]')){
      const script=document.createElement('script');
      script.src='/assets/show-gallery.js?v=4';
      script.dataset.vsGalleryLoader='true';
      document.body.append(script);
    }
  }
  upgradeShowGalleries();

  const light=document.getElementById('lightbox'),lightImg=document.getElementById('lightboxImg'),close=document.getElementById('lightboxClose');
  function shut(){
    if(!light)return;
    light.classList.remove('open');
    document.body.style.overflow='';
  }
  document.querySelectorAll('.gallery button').forEach(b=>b.addEventListener('click',()=>{
    if(!light||!lightImg)return;
    lightImg.src=b.querySelector('img').src;
    light.classList.add('open');
    document.body.style.overflow='hidden';
  }));
  if(close)close.addEventListener('click',e=>{e.stopPropagation();shut()});
  if(light)light.addEventListener('click',e=>{if(e.target===light)shut()});
  addEventListener('keydown',e=>{if(e.key==='Escape')shut()});

  /* Show sharing: add the shared pilot control to current show product pages. */
  function ensureShowShareControl(){
    if(document.querySelector('[data-show-share]'))return;
    if(!location.pathname.startsWith('/shows/'))return;
    const hero=document.querySelector('.hero');
    if(!hero)return;
    const ticketAction=hero.querySelector('.vs-ticket-primary,.cta[href]');
    const anchor=hero.querySelector('.updated')||hero.querySelector('.buybox');
    if(!ticketAction||!anchor)return;

    const canonical=document.querySelector('link[rel="canonical"]');
    const heading=hero.querySelector('h1');
    const url=canonical&&canonical.href?canonical.href:location.href;
    const title=heading?heading.textContent.replace(/\s+/g,' ').trim():document.title;

    const wrap=document.createElement('div');
    wrap.className='show-share-wrap';
    const btn=document.createElement('button');
    btn.className='show-share';
    btn.type='button';
    btn.setAttribute('data-show-share','');
    btn.dataset.shareTitle=title;
    btn.dataset.shareUrl=url;
    btn.setAttribute('aria-label','Share '+title);

    const icon=document.createElement('span');
    icon.className='show-share-icon';
    icon.setAttribute('aria-hidden','true');
    icon.textContent='↗';
    const label=document.createElement('span');
    label.setAttribute('data-share-label','');
    label.textContent='Share this show';

    btn.append(icon,label);
    wrap.append(btn);
    anchor.insertAdjacentElement('afterend',wrap);
  }
  ensureShowShareControl();

  /* Show sharing: native share sheet when available; copy the canonical show URL otherwise. */
  document.querySelectorAll('[data-show-share]').forEach(btn=>{
    const label=btn.querySelector('[data-share-label]');
    const defaultLabel=label?label.textContent:'Share this show';
    const url=btn.dataset.shareUrl||document.querySelector('link[rel="canonical"]')?.href||location.href;
    const title=btn.dataset.shareTitle||document.querySelector('h1')?.textContent.trim()||document.title;
    let resetTimer=0;

    function setStatus(message){
      if(!label)return;
      label.textContent=message;
      clearTimeout(resetTimer);
      resetTimer=setTimeout(()=>{label.textContent=defaultLabel},1800);
    }
    function track(method){
      if(typeof window.gtag==='function'){
        window.gtag('event','show_share',{
          show_name:title,
          share_method:method,
          page_location:url
        });
      }
    }
    async function copyUrl(){
      try{
        if(navigator.clipboard&&window.isSecureContext){
          await navigator.clipboard.writeText(url);
        }else{
          const area=document.createElement('textarea');
          area.value=url;
          area.setAttribute('readonly','');
          area.style.position='fixed';
          area.style.opacity='0';
          document.body.append(area);
          area.select();
          document.execCommand('copy');
          area.remove();
        }
        setStatus('Link copied');
        track('copy_link');
      }catch(err){
        setStatus('Copy failed');
      }
    }

    btn.addEventListener('click',async()=>{
      if(navigator.share){
        try{
          await navigator.share({title:title,url:url});
          track('native_share');
          return;
        }catch(err){
          if(err&&err.name==='AbortError')return;
        }
      }
      await copyUrl();
    });
  });

  /* Sidekick Pick: hand off the recommendation from the hero to the mobile sticky bar. */
  const heroSidekickPick=document.querySelector('.hero-sidekick-pick');
  const mobileSidekickBar=document.querySelector('.mobile-bar.has-sidekick-pick');
  const mobileSidekickPick=document.querySelector('.sidekick-pick-mobile');
  function syncSidekickPickHandoff(){
    if(!heroSidekickPick||!mobileSidekickBar)return;
    const mobile=innerWidth<=800;
    const passed=mobile&&heroSidekickPick.getBoundingClientRect().bottom<=72;
    mobileSidekickBar.classList.toggle('show-sidekick-pick',passed);
    if(!passed&&mobileSidekickPick)mobileSidekickPick.open=false;
  }
  if(heroSidekickPick&&mobileSidekickBar){
    addEventListener('scroll',syncSidekickPickHandoff,{passive:true});
    addEventListener('resize',syncSidekickPickHandoff);
    syncSidekickPickHandoff();
  }

  /* Sidekick Pick: close open explainers when the user clicks elsewhere or presses Escape. */
  document.addEventListener('click',e=>{
    if(e.target.closest('.sidekick-pick'))return;
    document.querySelectorAll('.sidekick-pick[open]').forEach(d=>{d.open=false});
  });
  document.querySelectorAll('.sidekick-pick').forEach(d=>d.addEventListener('toggle',()=>{
    if(!d.open)return;
    document.querySelectorAll('.sidekick-pick[open]').forEach(o=>{if(o!==d)o.open=false});
  }));
  addEventListener('keydown',e=>{
    if(e.key==='Escape')document.querySelectorAll('.sidekick-pick[open]').forEach(d=>{d.open=false});
  });

  document.querySelectorAll('.faq details').forEach(d=>d.addEventListener('toggle',()=>{
    if(d.open)document.querySelectorAll('.faq details').forEach(o=>{if(o!==d)o.open=false});
  }));

  document.querySelectorAll('.video-preview[data-video-id]').forEach(btn=>btn.addEventListener('click',()=>{
    const id=btn.dataset.videoId,wrap=btn.parentElement;
    if(!id||!wrap)return;
    const f=document.createElement('iframe');
    f.src='https://www.youtube-nocookie.com/embed/'+encodeURIComponent(id)+'?autoplay=1';
    f.title='Official show preview';
    f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
    f.allowFullscreen=true;
    wrap.replaceChildren(f);
  }));
})();
