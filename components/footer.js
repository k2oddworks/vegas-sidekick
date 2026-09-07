// Vegas Sidekick — Shared Footer Loader v16
// Keeps the approved footer implementation byte-for-byte in footer-core.js,
// then loads the canonical show runtime only on individual show pages.
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
})();
