from pathlib import Path

ROOT=Path('.')

def read(p): return (ROOT/p).read_text(encoding='utf-8')
def write(p,s): (ROOT/p).write_text(s,encoding='utf-8')

css='''/* Vegas Sidekick reusable official-video component */
.vs-video-shell{max-width:920px;margin:28px auto 0}
.vs-video{position:relative;aspect-ratio:16/9;overflow:hidden;border-radius:22px;background:#17082e;box-shadow:0 18px 46px rgba(35,12,60,.16);isolation:isolate}
.vs-video img{width:100%;height:100%;display:block;object-fit:cover}
.vs-video:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 35%,rgba(13,4,25,.28));pointer-events:none}
.vs-video-play{position:absolute;left:50%;top:50%;z-index:2;transform:translate(-50%,-50%);width:78px;height:78px;border:2px solid rgba(255,255,255,.9);border-radius:999px;background:#FFB000;color:#171225;display:grid;place-items:center;cursor:pointer;box-shadow:0 10px 30px rgba(0,0,0,.28),0 0 0 8px rgba(255,255,255,.12);transition:transform .18s ease,box-shadow .18s ease,filter .18s ease}
.vs-video-play:hover{transform:translate(-50%,-50%) scale(1.06);filter:brightness(1.03);box-shadow:0 14px 36px rgba(0,0,0,.32),0 0 0 10px rgba(255,255,255,.14)}
.vs-video-play:focus-visible{outline:3px solid #c6f22e;outline-offset:4px}
.vs-video-play span{display:block;margin-left:5px;font-size:1.9rem;line-height:1}
.vs-video iframe{width:100%;height:100%;border:0;display:block;background:#000}
.vs-video-caption{margin:12px 2px 0;color:#6b6275;font-size:.9rem;line-height:1.55}
@media(max-width:700px){.vs-video{border-radius:16px}.vs-video-play{width:66px;height:66px}.vs-video-play span{font-size:1.6rem}}
@media(prefers-reduced-motion:reduce){.vs-video-play{transition:none}.vs-video-play:hover{transform:translate(-50%,-50%)}}
'''
write('assets/show-video.css',css)

js='''/* Vegas Sidekick reusable official-video component */
(()=>{'use strict';
 const selector='.vs-video[data-youtube-id],.video[data-youtube-id],.video-preview[data-video-id]';
 const mount=root=>{
  if(root.dataset.vsVideoReady==='1')return;
  const id=(root.dataset.youtubeId||root.dataset.videoId||'').trim();
  if(!/^[A-Za-z0-9_-]{6,20}$/.test(id))return;
  root.dataset.vsVideoReady='1';
  root.classList.add('vs-video');
  let button=root.querySelector('.vs-video-play,.play,button');
  if(!button){button=document.createElement('button');button.type='button';button.className='vs-video-play';button.innerHTML='<span aria-hidden="true">▶</span>';root.appendChild(button)}
  else button.classList.add('vs-video-play');
  if(!button.getAttribute('aria-label'))button.setAttribute('aria-label','Play official show trailer');
  button.addEventListener('click',()=>{
   const iframe=document.createElement('iframe');
   iframe.src='https://www.youtube-nocookie.com/embed/'+encodeURIComponent(id)+'?autoplay=1&rel=0';
   iframe.title=button.getAttribute('aria-label')||'Official show trailer';
   iframe.loading='eager';
   iframe.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
   iframe.referrerPolicy='strict-origin-when-cross-origin';
   iframe.allowFullscreen=true;
   root.replaceChildren(iframe);
  },{once:true});
 };
 document.querySelectorAll(selector).forEach(mount);
})();
'''
write('assets/show-video.js',js)

footer=read('components/footer.js')
footer=footer.replace('Shared Footer Loader v24','Shared Footer Loader v25')
needle="  if(/^\\/shows\\/(adult|cirque|comedy|family|magic|music|spectaculars)\\/[^/]+\\/?$/.test(location.pathname)){\n    add('/components/show-canonical-runtime.js?v=3','data-vs-show-runtime');\n  }"
replacement="  if(/^\\/shows\\/(adult|cirque|comedy|family|magic|music|spectaculars)\\/[^/]+\\/?$/.test(location.pathname)){\n    addStyle('/assets/show-video.css?v=1','data-vs-show-video-style');\n    add('/assets/show-video.js?v=1','data-vs-show-video-script');\n    add('/components/show-canonical-runtime.js?v=3','data-vs-show-runtime');\n  }"
if needle not in footer: raise SystemExit('footer show-route block not found')
write('components/footer.js',footer.replace(needle,replacement))

page=read('shows/comedy/carrot-top/index.html')
old='<div class="video-shell"><div class="video" data-youtube-id="XRdqvnCZe-A"><img alt="Official Carrot Top Las Vegas trailer thumbnail" loading="lazy" src="https://i.ytimg.com/vi/XRdqvnCZe-A/maxresdefault.jpg"/><button aria-label="Play official Carrot Top trailer" class="play" type="button"><span>▶</span></button></div></div>'
new='<div class="vs-video-shell"><div class="vs-video" data-youtube-id="XRdqvnCZe-A"><img alt="Official Carrot Top Las Vegas trailer thumbnail" loading="lazy" src="https://i.ytimg.com/vi/XRdqvnCZe-A/maxresdefault.jpg"/><button aria-label="Play official Carrot Top trailer" class="vs-video-play" type="button"><span aria-hidden="true">▶</span></button></div><p class="vs-video-caption">Official Carrot Top trailer · plays from YouTube after you tap play.</p></div>'
if old not in page: raise SystemExit('Carrot Top trailer block not found')
page=page.replace(old,new,1)
page=page.replace('"dateModified":"2026-09-09","lastReviewed":"2026-09-09"','"dateModified":"2026-09-13","lastReviewed":"2026-09-13"',1)
write('shows/comedy/carrot-top/index.html',page)

bench=read('SHOW-PAGE-BENCHMARK.md')
marker='## 12. Seating-chart system'
video='''## 11a. Official video component\n\nWhen a verified official YouTube trailer exists, use the shared Vegas Sidekick video component rather than a one-off iframe or custom click handler.\n\n- Assets: `assets/show-video.css` and `assets/show-video.js`.\n- Standard markup uses `.vs-video-shell` containing `.vs-video[data-youtube-id]`, a thumbnail image and `.vs-video-play`.\n- Keep the lightweight thumbnail visible until the customer presses play; only then create the privacy-enhanced `youtube-nocookie.com` iframe.\n- Never invent or guess a video ID. Use only a verified official trailer.\n- Do not autoplay before an explicit user action.\n- Keep descriptive thumbnail alt text and an accessible play-button label.\n- `VideoObject` schema is optional and should only be used when its metadata is verified.\n\n---\n\n'''
if '## 11a. Official video component' not in bench:
    bench=bench.replace(marker,video+marker)
write('SHOW-PAGE-BENCHMARK.md',bench)

agents=read('AGENTS.md')
line='- Official YouTube embeds only; never invent or re-host trailers.\n'
extra='- Official YouTube embeds only; never invent or re-host trailers.\n- For verified official trailers, use the shared `assets/show-video.css` + `assets/show-video.js` component with `.vs-video[data-youtube-id]`; load the YouTube iframe only after an explicit play click.\n'
if extra not in agents:
    agents=agents.replace(line,extra)
write('AGENTS.md',agents)

# Simple audit: official trailer component must have a usable ID, alt text and play label.
audit='''#!/usr/bin/env python3\nfrom pathlib import Path\nimport re,sys\nroot=Path(__file__).resolve().parents[1]\nproblems=[];count=0\nfor p in root.glob('shows/*/*/index.html'):\n    t=p.read_text(encoding='utf-8',errors='ignore')\n    for m in re.finditer(r'<div class="vs-video"[^>]*data-youtube-id="([^"]+)"[^>]*>(.*?)</div>',t,re.S):\n        count+=1;vid,body=m.groups()\n        if not re.fullmatch(r'[A-Za-z0-9_-]{6,20}',vid): problems.append(f'{p.relative_to(root)}: invalid YouTube video ID')\n        if not re.search(r'<img[^>]+alt="[^"]+"',body): problems.append(f'{p.relative_to(root)}: trailer thumbnail missing alt text')\n        if not re.search(r'<button[^>]+aria-label="[^"]+"',body): problems.append(f'{p.relative_to(root)}: trailer play button missing aria-label')\nif problems:\n    print('Show video audit FAILED:');[print(' - '+x) for x in problems];sys.exit(1)\nprint(f'Show video audit passed. Shared video components checked: {count}')\n'''
write('scripts/audit-show-videos.py',audit)
print('Applied reusable show video component and fixed Carrot Top trailer.')
