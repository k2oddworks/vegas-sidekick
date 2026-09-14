/* Shared behavior only. Room artwork, hit zones and recommendations belong to adapters. */
(()=>{
  'use strict';
  const mounted=new WeakMap();
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  let openGuide=null;
  let sequence=0;

  function mount({root,controls,sections,getId,hitSelector,onSelect,initialId}){
    if(mounted.has(root))return mounted.get(root);
    const buttons=Array.from(controls);
    const byId=new Map(sections.map(section=>[String(section.id),section]));
    const hits=buttons.filter(button=>!hitSelector||button.matches(hitSelector));
    const popup=document.createElement('section');
    popup.className='vs-seat-popup';
    popup.id=`vs-seat-popup-${++sequence}`;
    popup.hidden=true;
    popup.setAttribute('role','region');
    const content=document.createElement('div');
    content.setAttribute('aria-live','polite');
    content.setAttribute('aria-atomic','true');
    const badge=document.createElement('span');
    badge.className='vs-seat-popup-badge';
    const title=document.createElement('h3');
    title.id=`${popup.id}-title`;
    popup.setAttribute('aria-labelledby',title.id);
    const copy=document.createElement('p');
    const closeButton=document.createElement('button');
    closeButton.type='button';
    closeButton.className='vs-seat-popup-close';
    closeButton.textContent='×';
    closeButton.setAttribute('aria-label','Close seat explanation');
    content.append(badge,title,copy);
    popup.append(content,closeButton);
    // Outside chart overflow/transform contexts, so the popup stays in the viewport.
    document.body.append(popup);
    root.classList.add('vs-seat-unified');
    root.dataset.seatInteractions='1';
    let lastControl=null;

    function position(){
      let clearance=12;
      const viewport=window.visualViewport;
      const bottom=(viewport?.offsetTop||0)+(viewport?.height||innerHeight);
      document.querySelectorAll('.mobile-bar, .mobile-sticky, .mob-bar, .mobile-cta').forEach(bar=>{
        const rect=bar.getBoundingClientRect();
        const style=getComputedStyle(bar);
        if(style.position==='fixed'&&style.display!=='none'&&style.visibility!=='hidden'&&rect.height>0&&rect.top<bottom&&rect.bottom>0){
          clearance=Math.max(clearance,bottom-rect.top+12);
        }
      });
      const keyboardInset=Math.max(0,innerHeight-bottom);
      popup.style.setProperty('--seat-popup-bottom',`${clearance+keyboardInset}px`);
      popup.style.setProperty('--seat-popup-max-height',`${Math.max(80,(viewport?.height||innerHeight)-clearance-24)}px`);
    }
    function close(restoreFocus=false){
      const focusInside=popup.contains(document.activeElement);
      popup.hidden=true;
      buttons.forEach(button=>button.setAttribute('aria-expanded','false'));
      if(openGuide===api)openGuide=null;
      if((restoreFocus||focusInside)&&lastControl?.isConnected)lastControl.focus({preventScroll:true});
    }
    function select(id,{open=true,control=null}={}){
      id=String(id);
      const section=byId.get(id);
      if(!section)return;
      if(open&&openGuide&&openGuide!==api)openGuide.close();
      const label=section.pick?'Sweet Spot / Our Pick':(section.badge||'Seat guide');
      buttons.forEach(button=>{
        const selected=String(getId(button))===id;
        button.classList.toggle('is-active',selected);
        button.setAttribute('aria-pressed',String(selected));
        button.setAttribute('aria-expanded',String(selected&&open));
        button.classList.remove('is-tapped');
      });
      if(open&&!reduced.matches){
        const selected=hits.filter(button=>String(getId(button))===id);
        // One layout flush restarts the pulse even when the same section is tapped twice.
        if(selected.length)void selected[0].offsetWidth;
        selected.forEach(button=>button.classList.add('is-tapped'));
      }
      onSelect?.(section,label);
      badge.textContent=label;
      title.textContent=section.label;
      copy.textContent=section.description;
      if(open){
        lastControl=control||buttons.find(button=>String(getId(button))===id);
        popup.hidden=false;
        openGuide=api;
        position();
      }
    }
    const api={select,close};
    mounted.set(root,api);
    hits.forEach(hit=>{
      hit.classList.add('vs-seat-control');
      hit.addEventListener('animationend',()=>hit.classList.remove('is-tapped'));
    });
    buttons.forEach(button=>{
      button.setAttribute('aria-controls',popup.id);
      button.setAttribute('aria-expanded','false');
      button.setAttribute('aria-pressed','false');
      button.addEventListener('click',()=>select(getId(button),{control:button}));
      // Native buttons already dispatch one click for Enter/Space. Do not double-activate.
      if(button.tagName!=='BUTTON')button.addEventListener('keydown',event=>{
        if(event.key==='Enter'||event.key===' '){event.preventDefault();select(getId(button),{control:button})}
      });
    });
    closeButton.addEventListener('click',()=>close(true));
    document.addEventListener('keydown',event=>{
      if(event.key==='Escape'&&openGuide===api){event.preventDefault();close(popup.contains(document.activeElement))}
    });
    document.addEventListener('click',event=>{
      if(openGuide===api&&!root.contains(event.target)&&!popup.contains(event.target))close();
    });
    addEventListener('resize',()=>{if(openGuide===api)position()},{passive:true});
    window.visualViewport?.addEventListener('resize',()=>{if(openGuide===api)position()},{passive:true});
    if(typeof ResizeObserver!=='undefined'){
      const observer=new ResizeObserver(()=>{if(openGuide===api)position()});
      document.querySelectorAll('.mobile-bar, .mobile-sticky, .mob-bar, .mobile-cta').forEach(bar=>observer.observe(bar));
    }
    if(initialId!=null)select(initialId,{open:false});
    return api;
  }
  window.VSSeatInteractions=Object.freeze({mount});
})();
