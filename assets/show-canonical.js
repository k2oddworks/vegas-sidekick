(function(){
  'use strict';

  const approvedSeatChartUpgrades={
    '/shows/spectaculars/absinthe/':{
      image:'/images/absinthe-seating-chart.webp?v=aed2ac49',
      alt:'Absinthe seating chart at the Spiegeltent at Caesars Palace showing Reserved 1, Reserved 2, Reserved 3, Reserved 4 and VIP sections',
      layoutUrl:'/data/seat-layouts/spiegeltent-caesars-palace.json',
      layoutId:'spiegeltent-caesars-palace',
      ticketUrl:'https://spotlight.vegas/shows/production/absinthe/ref/vegassidekick',
      heading:'Find your seat at the Spiegeltent',
      summary:'Reserved 2 and Reserved 3 are the Vegas Sidekick Sweet Spot / Our Pick.'
    }
  };

  function upgradeApprovedSeatChart(){
    const path=location.pathname.endsWith('/')?location.pathname:location.pathname+'/';
    const cfg=approvedSeatChartUpgrades[path];
    if(!cfg)return;

    if(!document.querySelector('link[data-vs-room-map]')){
      const link=document.createElement('link');
      link.rel='stylesheet';
      link.href='/assets/seat-layouts/room-map.css?v=6';
      link.dataset.vsRoomMap='1';
      document.head.appendChild(link);
    }

    const gallery=document.querySelector('#photos .gallery');
    if(gallery&&!gallery.querySelector('.vs-chart-gallery')){
      const button=document.createElement('button');
      button.type='button';
      button.className='vs-chart-gallery';
      button.setAttribute('aria-label','Open Absinthe seating chart');
      const img=document.createElement('img');
      img.loading='lazy';
      img.src=cfg.image;
      img.alt=cfg.alt;
      button.appendChild(img);
      gallery.appendChild(button);
      gallery.classList.remove('gallery-1','gallery-2','gallery-3');
      gallery.classList.add('gallery-4');
    }

    const seats=document.querySelector('#seats .wrap');
    if(seats){
      seats.innerHTML=`<div class="eyebrow">Seat guide</div><h2>${cfg.heading}</h2><p class="vs-room-summary">${cfg.summary}</p><div class="vs-room-seat-guide" data-layout-url="${cfg.layoutUrl}" data-seat-layout="${cfg.layoutId}" data-ticket-url="${cfg.ticketUrl}"></div>`;
    }

    if(!document.querySelector('script[data-vs-room-map]')){
      const script=document.createElement('script');
      script.src='/assets/seat-layouts/room-map.js?v=6';
      script.dataset.vsRoomMap='1';
      document.body.appendChild(script);
    }
  }

  upgradeApprovedSeatChart();

  function ensureSeamlessTickers(){
    document.querySelectorAll('.ticker-track').forEach(track=>{
      const sets=Array.from(track.children).filter(el=>el.classList?.contains('ticker-set'));
      if(sets.length!==1)return;
      const clone=sets[0].cloneNode(true);
      clone.setAttribute('aria-hidden','true');
      track.appendChild(clone);
    });
  }

  ensureSeamlessTickers();

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
