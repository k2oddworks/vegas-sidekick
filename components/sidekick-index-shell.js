// Vegas Sidekick — Sidekick Index shared page navigation + signup placement
// v1 — reference page pills and shared Insider List signup
(function(){
  'use strict';

  const pages=[
    {path:'/sidekick-index/',label:'Overview',accent:'#c6f22e',fg:'#171225'},
    {path:'/sidekick-index/headliners-residencies/',label:'Headliners & Residencies',accent:'#ff2e7e',fg:'#fff'},
    {path:'/sidekick-index/show-price-index/',label:'Show Price Index',accent:'#0fb5c9',fg:'#fff'},
    {path:'/sidekick-index/touring-shows-concerts/',label:'More Touring Shows & Concerts',accent:'#7c3aed',fg:'#fff'}
  ];

  function cleanPath(path){
    if(!path)return '/';
    return path.endsWith('/')?path:path+'/';
  }

  function currentPage(){
    const here=cleanPath(location.pathname);
    return pages.find(function(page){return page.path===here})||pages[0];
  }

  function addStyles(){
    if(document.getElementById('sidekick-index-shell-styles'))return;
    const style=document.createElement('style');
    style.id='sidekick-index-shell-styles';
    style.textContent=`
      .sidekick-index-nav{margin-top:28px}
      .sidekick-index-nav-label{display:block;margin:0 0 9px;color:rgba(255,255,255,.62);font:700 .62rem 'IBM Plex Mono',monospace;letter-spacing:.1em;text-transform:uppercase}
      .sidekick-index-nav-pills{display:flex;flex-wrap:wrap;gap:8px}
      .sidekick-index-nav-pill{display:inline-flex;align-items:center;justify-content:center;min-height:38px;padding:8px 12px;border:1px solid rgba(255,255,255,.22);border-radius:999px;background:rgba(255,255,255,.075);color:#fff;text-decoration:none;font:800 .72rem 'Plus Jakarta Sans',sans-serif;line-height:1.1;box-shadow:0 3px 10px rgba(0,0,0,.08);transition:transform .16s,background .16s,border-color .16s}
      .sidekick-index-nav-pill:hover{transform:translateY(-1px);background:rgba(255,255,255,.13);border-color:rgba(255,255,255,.35)}
      .sidekick-index-nav-pill.active{background:var(--idx-accent);color:var(--idx-fg);border-color:var(--idx-accent);box-shadow:0 5px 16px rgba(0,0,0,.18)}
      .sidekick-index-nav-pill.active:before{content:'✓';display:inline-grid;place-items:center;width:17px;height:17px;margin-right:6px;border-radius:50%;background:rgba(255,255,255,.2);font-size:.64rem}
      .sidekick-index-email-wrap{width:min(1160px,calc(100% - 40px));margin:0 auto 56px}
      .sidekick-index-email-wrap .vs-email-bar{border:1px solid rgba(255,255,255,.1);border-radius:22px;overflow:hidden;box-shadow:0 18px 42px rgba(23,18,37,.12)}
      .sidekick-index-email-wrap .vs-email-bar-inner{width:100%;padding:24px}
      @media(max-width:720px){
        .sidekick-index-nav{margin-top:22px}
        .sidekick-index-nav-pills{gap:7px}
        .sidekick-index-nav-pill{padding:8px 10px;font-size:.67rem}
        .sidekick-index-email-wrap{width:min(100% - 24px,1160px);margin-bottom:34px}
        .sidekick-index-email-wrap .vs-email-bar-inner{padding:20px}
      }
      @media(prefers-reduced-motion:reduce){.sidekick-index-nav-pill{transition:none}}
    `;
    document.head.appendChild(style);
  }

  function mountNav(){
    const hero=document.querySelector('.hero .wrap');
    if(!hero||hero.querySelector('.sidekick-index-nav'))return;
    const active=currentPage();
    const nav=document.createElement('nav');
    nav.className='sidekick-index-nav';
    nav.setAttribute('aria-label','Sidekick Index reference pages');
    nav.innerHTML='<span class="sidekick-index-nav-label">Reference pages</span><div class="sidekick-index-nav-pills">'+pages.map(function(page){
      const isActive=page.path===active.path;
      return '<a class="sidekick-index-nav-pill'+(isActive?' active':'')+'" href="'+page.path+'"'+(isActive?' aria-current="page"':'')+' style="--idx-accent:'+page.accent+';--idx-fg:'+page.fg+'">'+page.label+'</a>';
    }).join('')+'</div>';
    hero.appendChild(nav);
  }

  function ensureEmailSlot(){
    if(document.getElementById('sidekick-index-email-slot'))return document.getElementById('sidekick-index-email-slot');
    const footer=document.getElementById('vs-footer');
    if(!footer)return null;
    const section=document.createElement('section');
    section.className='sidekick-index-email-wrap';
    section.setAttribute('aria-label','Vegas Sidekick email updates');
    const slot=document.createElement('div');
    slot.id='sidekick-index-email-slot';
    section.appendChild(slot);
    footer.parentNode.insertBefore(section,footer);
    return slot;
  }

  function moveSharedSignup(){
    const slot=ensureEmailSlot();
    const emailBar=document.getElementById('vsEmailBar');
    if(!slot||!emailBar||slot.contains(emailBar))return false;
    slot.appendChild(emailBar);
    return true;
  }

  function boot(){
    if(!location.pathname.startsWith('/sidekick-index'))return;
    addStyles();
    mountNav();
    if(moveSharedSignup())return;
    const observer=new MutationObserver(function(){
      if(moveSharedSignup())observer.disconnect();
    });
    observer.observe(document.body,{childList:true,subtree:true});
    setTimeout(function(){observer.disconnect();moveSharedSignup();},5000);
  }

  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);
  else boot();
})();