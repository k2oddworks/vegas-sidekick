// Vegas Sidekick — Shared Footer Loader v17
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
  add('/components/footer-core.js?v=15','data-vs-footer-core');
  if(/^\/shows\/(adult|cirque|comedy|family|magic|music|spectaculars)\/[^/]+\/?$/.test(location.pathname)){
    add('/components/show-canonical-runtime.js?v=2','data-vs-show-runtime');
  }
  if(/^\/play\/walk-the-strip\/?$/.test(location.pathname)){
    add('/play/walk-the-strip/v2.js?v=2','data-vs-walk-strip-v2');
  }
})();