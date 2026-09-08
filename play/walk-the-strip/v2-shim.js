/* Walk the Strip v2 control isolation.
   Loaded after the legacy game has bound its handlers, before v2 boots. */
(function(){
  'use strict';
  function clean(id){
    var old=document.getElementById(id);
    if(!old) return;
    var fresh=old.cloneNode(true);
    old.replaceWith(fresh);
  }
  function run(){
    clean('startBtn');
    clean('shareBtn');
    clean('soundBtn');
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',run,{once:true});
  else run();
})();