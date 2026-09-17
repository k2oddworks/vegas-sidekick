/* Vegas Sidekick reusable official-video component */
(()=>{'use strict';
 const selector='.vs-video[data-youtube-id],.video[data-youtube-id],.video-preview[data-video-id]';
 const showName=()=>{
  const h1=document.querySelector('h1');
  return (h1?.textContent||document.title.split('|')[0]||'Show').trim();
 };
 const addHeading=root=>{
  const shell=root.closest('.vs-video-shell');
  if(!shell||shell.querySelector('.vs-video-preview-title'))return;
  const title=document.createElement('h3');
  title.className='vs-video-preview-title';
  title.textContent=showName()+' Video Preview';
  shell.insertBefore(title,root);
 };
 const mount=root=>{
  if(root.dataset.vsVideoReady==='1')return;
  const id=(root.dataset.youtubeId||root.dataset.videoId||'').trim();
  if(!/^[A-Za-z0-9_-]{6,20}$/.test(id))return;
  root.dataset.vsVideoReady='1';
  root.classList.add('vs-video');
  addHeading(root);
  let button=root.querySelector('.vs-video-play,.play,button');
  if(!button){button=document.createElement('button');button.type='button';button.className='vs-video-play';button.innerHTML='<span aria-hidden="true">▶</span>';root.appendChild(button)}
  else button.classList.add('vs-video-play');
  const name=showName();
  button.setAttribute('aria-label','Play '+name+' video preview');
  const image=root.querySelector('img');
  if(image&&!image.getAttribute('alt'))image.setAttribute('alt',name+' video preview thumbnail');
  button.addEventListener('click',()=>{
   const iframe=document.createElement('iframe');
   iframe.src='https://www.youtube-nocookie.com/embed/'+encodeURIComponent(id)+'?autoplay=1&rel=0';
   iframe.title=name+' video preview';
   iframe.loading='eager';
   iframe.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
   iframe.referrerPolicy='strict-origin-when-cross-origin';
   iframe.allowFullscreen=true;
   root.replaceChildren(iframe);
  },{once:true});
 };
 document.querySelectorAll(selector).forEach(mount);
})();
