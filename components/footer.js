// Vegas Sidekick — Shared Footer Loader v26
// Keeps the approved footer implementation in footer-core.js,
// loads canonical show runtime only on individual show pages,
// and loads the isolated Walk the Strip spectacle layer only on its game route.
(function(){
  'use strict';
  function add(src, marker){
    if(marker && document.querySelector('script['+marker+']')) return;
    var s=document.createElement('script');
    s.src=src;
    s.async=false;
    if(marker) s.setAttribute(marker,'1');
    document.body.appendChild(s);
  }
  function addStyle(href, marker){
    if(marker && document.querySelector('link['+marker+']')) return;
    var l=document.createElement('link');
    l.rel='stylesheet';
    l.href=href;
    if(marker) l.setAttribute(marker,'1');
    document.head.appendChild(l);
  }
  addStyle('/assets/site-polish.css?v=4','data-vs-site-polish');
  add('/assets/site-polish.js?v=5','data-vs-site-polish-script');
  add('/components/footer-core.js?v=15','data-vs-footer-core');
  if(/^\/shows\/(adult|cirque|comedy|family|magic|music|spectaculars)\/[^/]+\/?$/.test(location.pathname)){
    addStyle('/assets/show-video.css?v=2','data-vs-show-video-style');
    add('/assets/show-video.js?v=2','data-vs-show-video-script');
    add('/components/show-canonical-runtime.js?v=3','data-vs-show-runtime');
  }
  if(/^\/play\/walk-the-strip\/?$/.test(location.pathname)){
    // The legacy game is still preserved in the page as a fallback/core reference.
    // Suppress its first RAF registration so it does not burn CPU drawing a detached canvas.
    var nativeRAF=window.requestAnimationFrame;
    window.requestAnimationFrame=function(){ return 0; };
    add('/play/walk-the-strip/v2-shim.js?v=1','data-vs-walk-strip-shim');
    add('/play/walk-the-strip/v2.js?v=2','data-vs-walk-strip-v2');
    document.addEventListener('DOMContentLoaded',function(){ window.requestAnimationFrame=nativeRAF; },{once:true});
  }
})();