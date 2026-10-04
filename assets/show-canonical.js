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
