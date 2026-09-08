/* Walk the Strip v2 — self-contained spectacle renderer/gameplay layer */
(function(){
'use strict';
function boot(){
  const old=document.getElementById('game');
  const overlay=document.getElementById('overlay');
  const startBtn=document.getElementById('startBtn');
  const shareBtn=document.getElementById('shareBtn');
  const scoreEl=document.getElementById('score');
  const bestEl=document.getElementById('best');
  const livesEl=document.getElementById('lives');
  const soundBtn=document.getElementById('soundBtn');
  if(!old||!overlay||!startBtn||!scoreEl||!bestEl||!livesEl) return;

  const css=document.createElement('link');css.rel='stylesheet';css.href='/play/walk-the-strip/v2.css?v=2';document.head.appendChild(css);
  const canvas=old.cloneNode(false); old.replaceWith(canvas);
  const ctx=canvas.getContext('2d');
  const COLS=11, ROWS=13, TILE=48, W=COLS*TILE, H=ROWS*TILE;
  let dpr=1;
  function fit(){dpr=Math.min(devicePixelRatio||1,2);canvas.width=W*dpr;canvas.height=H*dpr;ctx.setTransform(dpr,0,0,dpr,0,0);ctx.imageSmoothingEnabled=true}
  fit();addEventListener('resize',fit);

  const CAST=[
    {kind:'promoter',label:'CLUB PROMOTER',color:'#4f8df7'},
    {kind:'showgirl',label:'COSTUMED CHARACTER',color:'#ff2e7e'},
    {kind:'mascot',label:'OFF-BRAND MASCOT',color:'#e6534f'},
    {kind:'timeshare',label:'TIMESHARE REP',color:'#d3ae69'},
    {kind:'selfie',label:'SELFIE SQUAD',color:'#19d3e6'},
    {kind:'magician',label:'STREET MAGICIAN',color:'#a855f7'},
    {kind:'dancer',label:'STREET DANCER',color:'#ff7a2f'},
    {kind:'swirl',label:'HYPNOTIC SWIRL',color:'#77d8ff'}
  ];
  const HITS={
    promoter:'BRO. BRO. One second, bro. It was not one second.',
    showgirl:'Photo op initiated. Tip expected. Trauma acquired.',
    mascot:'An unofficial mascot hugged you without asking. He now expects a tip.',
    timeshare:'Quick survey? You now co-own a studio in Laughlin.',
    selfie:'Trapped behind a 14-person group photo. Nobody blinked in unison.',
    magician:'Is THIS your card? It was. It is always your card. How.',
    dancer:'Pulled into the circle. The crowd is chanting. There is no way out.',
    swirl:'You looked directly at the swirl. You are now one hour behind schedule.'
  };
  const EVENTS=[
    {name:'FOUNTAINS',text:'The fountains are doing the most.',type:'fountain'},
    {name:'SPHERE EYE',text:'The Sphere has noticed Spike.',type:'eye'},
    {name:'WEDDING PARTY',text:'Of course there is a wedding party.',type:'wedding'},
    {name:'LIMO NIGHT',text:'A limo the length of Henderson has arrived.',type:'limo'},
    {name:'DESERT RAIN',text:'Four drops. Everyone panics.',type:'rain'},
    {name:'ELVIS?',text:'Do not make eye contact.',type:'elvis'},
    {name:'F1 FLASHBACK',text:'A barrier has entered the chat.',type:'f1'}
  ];
  const SECRET=['🐧','👽','🦩','🐔','🎰'];

  function lsGet(k){try{return localStorage.getItem(k)}catch(e){return null}}
  function lsSet(k,v){try{localStorage.setItem(k,v)}catch(e){}}
  function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}
  function clamp(v,a,b){return Math.max(a,Math.min(b,v))}
  function rr(x,y,w,h,r){ctx.beginPath();ctx.roundRect(x,y,w,h,r)}

  let best=Number(lsGet('vs_dc_best'))||0;
  let score=0,crossings=0,lives=3,playing=false,invuln=0,last=performance.now(),shake=0,flash=0;
  let spike,hazards=[],doors=[],particles=[],popups=[],nearSeen=new Set(),combo=0,comboTimer=0;
  let hit={t:0,kind:'',label:'',text:''}, event={type:'',t:0,name:''}, eventClock=0, secret=null;
  let phase=0,phaseTarget=0,ambientT=0;
  let soundOn=lsGet('vs_dc_sound')==='1',audio=null,ambTimer=0;
  bestEl.textContent=best;

  function resetSpike(){spike={col:5,row:12,x:5*TILE,y:12*TILE,hop:0,idle:Math.random()*10,look:0}}
  function buildDoors(){
    const p=Array(COLS).fill(1),o=shuffle([...Array(COLS).keys()]);[5,3,3,2,2].forEach((m,i)=>p[o[i]]=m);
    const s=(26+Math.random()*20)*(Math.random()<.5?1:-1);
    doors=p.map((mult,i)=>({mult,x:i*TILE,speed:s,phase:Math.random()*6}));
  }
  function buildHazards(d){
    hazards=[];nearSeen.clear();
    const order=shuffle([...CAST]);let ci=0;
    for(let r=1;r<12;r++){
      if(r===6)continue;
      const kind=order[ci++%order.length].kind,dir=r%2?1:-1;
      const base=(1.02+Math.random()*.8+d*.14)*TILE*(kind==='swirl'?.58:1);
      const count=2+Math.floor(Math.random()*2);
      for(let i=0;i<count;i++)hazards.push({id:Math.random().toString(36).slice(2),kind,row:r,x:(i*(COLS/count)+Math.random()*1.25)*TILE,w:kind==='selfie'?TILE*1.9:TILE*.88,speed:base*dir,p:Math.random()*6});
    }
  }
  function doorAt(px){for(const z of doors){const e=z.x+TILE;if(e<=W&&px>=z.x&&px<e)return z;if(e>W&&(px>=z.x||px<e-W))return z}return null}

  function ensureAudio(){if(!audio){const AC=window.AudioContext||window.webkitAudioContext;if(AC)audio=new AC()}if(audio&&audio.state==='suspended')audio.resume()}
  function tone(f,d=.06,type='sine',v=.035,delay=0){if(!soundOn)return;ensureAudio();if(!audio)return;const t=audio.currentTime+delay,o=audio.createOscillator(),g=audio.createGain();o.type=type;o.frequency.setValueAtTime(f,t);g.gain.setValueAtTime(v,t);g.gain.exponentialRampToValueAtTime(.001,t+d);o.connect(g).connect(audio.destination);o.start(t);o.stop(t+d)}
  function sfxHop(){tone(480+Math.random()*80,.045,'square',.025)}
  function sfxNear(){tone(920,.045,'sine',.018)}
  function sfxHit(kind){tone(kind==='swirl'?130:190,.12,'sawtooth',.045);tone(110,.2,'triangle',.035,.08)}
  function sfxScore(m){tone(590+m*45,.07,'square',.045);tone(820+m*55,.09,'square',.04,.07);if(m===5){tone(1120,.16,'sine',.05,.14);tone(1450,.2,'sine',.04,.22)}}
  function sfxEvent(){tone(330,.08,'triangle',.025);tone(495,.11,'triangle',.025,.07)}
  function ambient(dt){if(!soundOn||!playing)return;ambTimer-=dt;if(ambTimer>0)return;ambTimer=1.6+Math.random()*2.2;tone(80+Math.random()*35,.35,'sine',.008);if(Math.random()<.45)tone(900+Math.random()*600,.035,'square',.007,.15)}
  function renderSound(){soundBtn.textContent=soundOn?'ON':'OFF';soundBtn.classList.toggle('on',soundOn)}
  renderSound();soundBtn.onclick=function(e){e.stopPropagation();soundOn=!soundOn;lsSet('vs_dc_sound',soundOn?'1':'0');if(soundOn){ensureAudio();tone(660,.06,'square',.04)}renderSound()};

  function updateHUD(){scoreEl.textContent=score;bestEl.textContent=best;const faces=['','','☠️','😠','😎'];livesEl.textContent=lives>0?'🌵'.repeat(lives)+(lives<3?' '+faces[lives+1]:''): '☠️'}
  function toast(t){let el=document.getElementById('wts-toast');if(!el){el=document.createElement('div');el.id='wts-toast';document.body.appendChild(el)}el.textContent=t;el.classList.add('show');clearTimeout(el._t);el._t=setTimeout(()=>el.classList.remove('show'),1500)}
  function burst(x,y,color,n=18,spd=85){for(let i=0;i<n;i++){const a=Math.random()*Math.PI*2,s=25+Math.random()*spd;particles.push({x,y,vx:Math.cos(a)*s,vy:Math.sin(a)*s-20,t:.5+Math.random()*.65,c:color,r:1+Math.random()*2.5})}}
  function popup(text,x,y,color='#fff',big=false){popups.push({text,x,y,t:1.1,color,big})}
  function triggerEvent(force){if(event.t>0)return;const e=force||EVENTS[Math.floor(Math.random()*EVENTS.length)];event={type:e.type,t:5.5,name:e.name};toast(e.name+' · '+e.text);sfxEvent();if(e.type==='rain')burst(W/2,0,'#78cfff',50,130);if(Math.random()<.35)secret={icon:SECRET[Math.floor(Math.random()*SECRET.length)],x:-30,y:(2+Math.floor(Math.random()*8))*TILE+24,vx:60+Math.random()*50,t:8}}

  function start(){score=0;crossings=0;lives=3;playing=true;invuln=.8;shake=0;flash=0;hit.t=0;event.t=0;eventClock=6+Math.random()*5;combo=0;particles=[];popups=[];phaseTarget=0;resetSpike();buildHazards(0);buildDoors();updateHUD();overlay.classList.add('hidden');shareBtn.classList.add('hidden');startBtn.textContent='CROSS AGAIN';if(soundOn)ensureAudio()}
  startBtn.addEventListener('click',start);

  function finish(){
    const z=doorAt(spike.col*TILE+TILE/2),m=z?z.mult:1;
    crossings++;score+=m;if(score>best){best=score;lsSet('vs_dc_best',best);popup('🏆 NEW BEST',W/2,H*.38,'#ffcf5a',true)}
    sfxScore(m);flash=m===5?.9:.25;shake=m===5?7:2;burst(spike.x+24,30,m===5?'#ffcf5a':'#19d3e6',m===5?46:20,m===5?150:80);
    popup(m===5?'JACKPOT ×5':'+'+m,spike.x+24,42,m===5?'#ffcf5a':'#fff',m===5);
    if(m===5)toast('HOUSE UPGRADE · Spike approves.');
    updateHUD();phaseTarget=Math.min(1,crossings/8);
    setTimeout(()=>{resetSpike();buildHazards(crossings);invuln=.65},190);
    setTimeout(buildDoors,1100);
    if(crossings>0&&crossings%3===0&&event.t<=0)triggerEvent();
  }
  function move(dir){if(!playing||spike.hop>0)return;let c=spike.col,r=spike.row;if(dir==='up')r--;if(dir==='down')r++;if(dir==='left')c--;if(dir==='right')c++;c=clamp(c,0,COLS-1);r=clamp(r,0,ROWS-1);if(c===spike.col&&r===spike.row)return;sfxHop();spike.col=c;spike.row=r;spike.hop=.12;spike.look=dir==='left'?-1:dir==='right'?1:0;if(r===0)finish()}
  addEventListener('keydown',e=>{const m={ArrowUp:'up',ArrowDown:'down',ArrowLeft:'left',ArrowRight:'right',w:'up',a:'left',s:'down',d:'right',W:'up',A:'left',S:'down',D:'right'};if(m[e.key]){e.preventDefault();move(m[e.key])}});

  const joy=document.createElement('div');joy.id='wts-joystick';joy.innerHTML='<div id="wts-stick"></div>';document.body.appendChild(joy);const stick=joy.firstChild;
  let pointer=null,lastJoyMove=0;
  canvas.addEventListener('pointerdown',e=>{if(!playing)return;pointer={id:e.pointerId,x:e.clientX,y:e.clientY};canvas.setPointerCapture(e.pointerId);joy.style.left=e.clientX+'px';joy.style.top=e.clientY+'px';stick.style.transform='translate(-50%,-50%)';joy.classList.add('visible')});
  canvas.addEventListener('pointermove',e=>{if(!pointer||e.pointerId!==pointer.id)return;let dx=e.clientX-pointer.x,dy=e.clientY-pointer.y;const mag=Math.hypot(dx,dy),max=34;if(mag>max){dx*=max/mag;dy*=max/mag}stick.style.transform=`translate(calc(-50% + ${dx}px),calc(-50% + ${dy}px))`;if(mag>18&&performance.now()-lastJoyMove>125){lastJoyMove=performance.now();if(Math.abs(dx)>Math.abs(dy))move(dx>0?'right':'left');else move(dy>0?'down':'up');pointer.x=e.clientX;pointer.y=e.clientY;joy.style.left=e.clientX+'px';joy.style.top=e.clientY+'px'}});
  function joyEnd(){pointer=null;joy.classList.remove('visible')}
  canvas.addEventListener('pointerup',joyEnd);canvas.addEventListener('pointercancel',joyEnd);

  function hitHazard(h){
    lives--;invuln=1.35;shake=8;flash=.8;combo=0;const c=CAST.find(x=>x.kind===h.kind)||CAST[0];hit={t:2.4,kind:h.kind,label:c.label,text:HITS[h.kind]};sfxHit(h.kind);burst(spike.x+24,spike.y+24,c.color,28,120);updateHUD();
    if(h.kind==='selfie')flash=1.4;if(h.kind==='swirl')event={type:'swirlhit',t:1.2,name:'THE SWIRL'};
    if(lives<=0){gameOver();return}resetSpike();
  }
  function gameOver(){
    playing=false;const label=hit.label||'Strip regular';overlay.querySelector('h2').textContent='OUT OF PATIENCE';overlay.querySelectorAll('p')[0].innerHTML=`Spike scored <b style="color:#19d3e6">${score}</b> across <b>${crossings}</b> crossing${crossings===1?'':'s'} before <b style="color:#ffb000">${label}</b> ended the run.<br>Best: <b style="color:#ffb000">${best}</b>.`;overlay.querySelector('.hint').textContent='Gold doors are worth ×5. Near misses build bonus points.';overlay.querySelector('.quote').textContent=score>=35?'“Respectable. You may walk beside me.” — Spike':score>=15?'“Adequate. The desert acknowledges you.” — Spike':'“The Strip remains undefeated.” — Spike';overlay.classList.remove('hidden');shareBtn.classList.remove('hidden');startBtn.textContent='CROSS AGAIN';tone(280,.16,'triangle',.04);tone(190,.2,'triangle',.035,.16);tone(120,.28,'triangle',.03,.32)
  }
  shareBtn.onclick=function(){const url='https://vegassidekick.com/play/walk-the-strip/';const text=`🌵 Walk the Strip: ${score} points across ${crossings} crossing${crossings===1?'':'s'}. Beat me → ${url}`;if(navigator.share)navigator.share({text,url}).catch(()=>{});else if(navigator.clipboard)navigator.clipboard.writeText(text).then(()=>toast('SCORE COPIED'))};

  function update(dt){
    ambient(dt);ambientT+=dt;phase+=(phaseTarget-phase)*Math.min(1,dt*.8);if(invuln>0)invuln-=dt;if(hit.t>0)hit.t-=dt;if(event.t>0)event.t-=dt;if(comboTimer>0)comboTimer-=dt;else combo=0;if(shake>0)shake=Math.max(0,shake-dt*18);if(flash>0)flash=Math.max(0,flash-dt*2.3);
    for(const d of doors){d.x+=d.speed*dt;d.phase+=dt*2;if(d.x>=W)d.x-=W;if(d.x<0)d.x+=W}
    for(let i=particles.length-1;i>=0;i--){const p=particles[i];p.t-=dt;p.x+=p.vx*dt;p.y+=p.vy*dt;p.vy+=60*dt;if(p.t<=0)particles.splice(i,1)}
    for(let i=popups.length-1;i>=0;i--){const p=popups[i];p.t-=dt;p.y-=22*dt;if(p.t<=0)popups.splice(i,1)}
    if(secret){secret.x+=secret.vx*dt;secret.t-=dt;if(secret.t<=0||secret.x>W+50)secret=null}
    if(!playing)return;
    eventClock-=dt;if(eventClock<=0){eventClock=8+Math.random()*8;if(Math.random()<.8)triggerEvent()}
    if(spike.hop>0)spike.hop-=dt;spike.idle+=dt;spike.x+=(spike.col*TILE-spike.x)*Math.min(1,dt*18);spike.y+=(spike.row*TILE-spike.y)*Math.min(1,dt*18);
    const sx=spike.x+TILE*.22,sw=TILE*.56;
    for(const h of hazards){
      h.x+=h.speed*dt;h.p+=dt*5;if(h.speed>0&&h.x>W+TILE)h.x=-h.w-TILE;if(h.speed<0&&h.x<-h.w-TILE)h.x=W+TILE;
      if(h.row!==spike.row)continue;const hx=h.x+h.w*.12,hw=h.w*.76;const gap=Math.max(hx-(sx+sw),sx-(hx+hw),0);
      if(invuln<=0&&sx<hx+hw&&sx+sw>hx){hitHazard(h);break}
      if(gap>0&&gap<8&&!nearSeen.has(h.id)){nearSeen.add(h.id);combo++;comboTimer=1.6;score+=combo>=3?2:1;if(score>best){best=score;lsSet('vs_dc_best',best)}updateHUD();sfxNear();popup(combo>=3?'LOCAL BEHAVIOR +2':'CLOSE CALL +1',spike.x+24,spike.y,'#c6f22e');burst(spike.x+24,spike.y+24,'#c6f22e',8,55)}
    }
  }

  function sky(){
    const dusk=[30,8,48],night=[4,7,20];const t=phase;const r=Math.round(dusk[0]*(1-t)+night[0]*t),g=Math.round(dusk[1]*(1-t)+night[1]*t),b=Math.round(dusk[2]*(1-t)+night[2]*t);ctx.fillStyle=`rgb(${r},${g},${b})`;ctx.fillRect(0,0,W,H);
    const grad=ctx.createLinearGradient(0,0,0,H);grad.addColorStop(0,`rgba(255,61,132,${.13*(1-t)})`);grad.addColorStop(.42,'rgba(43,22,78,.18)');grad.addColorStop(1,'rgba(0,0,0,.22)');ctx.fillStyle=grad;ctx.fillRect(0,0,W,H);
    for(let i=0;i<34;i++){const x=(i*83+17)%W,y=(i*47+11)%190,a=.15+.32*Math.abs(Math.sin(ambientT*.7+i));ctx.fillStyle=`rgba(255,255,255,${a*t})`;ctx.fillRect(x,y,1,1)}
  }
  function skyline(){
    ctx.save();ctx.translate(0,3);const bases=[{x:0,w:74,h:112,c:'#171329'},{x:68,w:50,h:84,c:'#121b2e'},{x:112,w:82,h:132,c:'#20142d'},{x:188,w:62,h:98,c:'#111a28'},{x:246,w:90,h:142,c:'#25152f'},{x:331,w:58,h:104,c:'#111b2b'},{x:385,w:83,h:128,c:'#1d1430'},{x:463,w:65,h:90,c:'#101827'}];
    bases.forEach((b,i)=>{ctx.fillStyle=b.c;ctx.fillRect(b.x,190-b.h,b.w,b.h);for(let yy=190-b.h+12;yy<182;yy+=15)for(let xx=b.x+9;xx<b.x+b.w-6;xx+=15){const on=(xx+yy+i*19)%37<18;ctx.fillStyle=on?`rgba(${i%2?'255,176,0':'25,211,230'},${.16+.22*Math.abs(Math.sin(ambientT*.8+xx))})`:'rgba(255,255,255,.025)';ctx.fillRect(xx,yy,5,7)}});
    // pseudo neon marquees
    const signs=[['VEGAS',28,94,'#ff2e7e'],['SHOWS',145,69,'#19d3e6'],['24 HR',275,82,'#ffb000'],['LIVE',406,60,'#c6f22e']];ctx.font="800 10px 'Barlow Condensed'";ctx.textAlign='center';signs.forEach((s,i)=>{const pulse=.65+.35*Math.sin(ambientT*2+i);ctx.shadowBlur=12;ctx.shadowColor=s[3];ctx.fillStyle=s[3];ctx.globalAlpha=pulse;ctx.fillText(s[0],s[1],s[2]);ctx.globalAlpha=1});ctx.shadowBlur=0;
    // Sphere horizon
    const ex=448,ey=143,er=29;ctx.fillStyle='#11152a';ctx.beginPath();ctx.arc(ex,ey,er,0,Math.PI*2);ctx.fill();ctx.strokeStyle='#673ab7';ctx.lineWidth=2;ctx.stroke();const eye=event.type==='eye'&&event.t>0;ctx.fillStyle=eye?'#f7f2e8':'#5b39a8';ctx.beginPath();ctx.ellipse(ex,ey,eye?20:13,eye?9:13,0,0,Math.PI*2);ctx.fill();if(eye){ctx.fillStyle='#67b7ff';ctx.beginPath();ctx.arc(ex+Math.sin(ambientT)*5,ey,6,0,Math.PI*2);ctx.fill();ctx.fillStyle='#05060d';ctx.beginPath();ctx.arc(ex+Math.sin(ambientT)*5,ey,2.4,0,Math.PI*2);ctx.fill()}
    ctx.restore();
  }
  function street(){
    for(let r=0;r<ROWS;r++){const y=r*TILE;const rest=r===0||r===6||r===12;if(rest){ctx.fillStyle=r===6?'#171329':'#12101d';ctx.fillRect(0,y,W,TILE);ctx.fillStyle='rgba(255,255,255,.06)';for(let x=(r%2)*22;x<W;x+=48)ctx.fillRect(x,y+1,1,TILE-2)}else{ctx.fillStyle=r%2?'#0b0c14':'#0d0e18';ctx.fillRect(0,y,W,TILE);ctx.strokeStyle='rgba(255,255,255,.035)';ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke();for(let x=(r%2)*24;x<W;x+=48){ctx.strokeStyle='rgba(255,255,255,.025)';ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x,y+TILE);ctx.stroke()}}
      const glow=ctx.createLinearGradient(0,y,0,y+TILE);glow.addColorStop(0,'rgba(255,46,126,.025)');glow.addColorStop(1,'rgba(25,211,230,.02)');ctx.fillStyle=glow;ctx.fillRect(0,y,W,TILE)}
    // palms on median
    for(let x=48;x<W;x+=144){ctx.strokeStyle='#66422e';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(x,6*TILE+38);ctx.lineTo(x+2,6*TILE+13);ctx.stroke();ctx.strokeStyle='rgba(40,185,102,.72)';ctx.lineWidth=3;for(let a=-1.2;a<=1.2;a+=.6){ctx.beginPath();ctx.moveTo(x+2,6*TILE+13);ctx.lineTo(x+2+Math.cos(a)*14,6*TILE+13+Math.sin(a)*10);ctx.stroke()}}
    // moving head/tail light reflections
    for(let i=0;i<9;i++){const yy=(1+(i%10))*TILE+36,xx=(ambientT*(28+i*7)*(i%2?1:-1)+i*77)% (W+80);const x=(xx+W+80)%(W+80)-40;ctx.fillStyle=i%2?'rgba(255,52,102,.28)':'rgba(255,242,180,.25)';ctx.fillRect(x,yy,20,2)}
  }
  function doorsDraw(){for(const z of doors){drawDoor(z,z.x);if(z.x+TILE>W)drawDoor(z,z.x-W)}}
  function drawDoor(z,x){const m=z.mult;const c=m===5?'#ffcf5a':m===3?'#ff2e7e':m===2?'#19d3e6':'#6d6177';ctx.save();ctx.translate(x,2);ctx.shadowColor=c;ctx.shadowBlur=m===5?18:7;ctx.fillStyle='rgba(5,5,12,.9)';rr(3,2,TILE-6,TILE-5,6);ctx.fill();ctx.strokeStyle=c;ctx.lineWidth=m===5?2.6:1.2;ctx.stroke();ctx.shadowBlur=0;for(let i=0;i<5;i++){const bx=8+i*7.2;ctx.fillStyle=`rgba(255,220,120,${m===5?.55+.4*Math.sin(ambientT*5+i):.22})`;ctx.beginPath();ctx.arc(bx,6,1.5,0,Math.PI*2);ctx.fill()}ctx.fillStyle=c;ctx.font=`800 ${m===5?15:12}px 'Barlow Condensed'`;ctx.textAlign='center';ctx.fillText('×'+m,TILE/2,27);ctx.font="700 7px 'Barlow Condensed'";ctx.fillText(m===5?'JACKPOT':m===3?'UPGRADE':m===2?'GOOD DOOR':'DOOR',TILE/2,38);ctx.restore()}
  function drawSpike(){
    const x=spike.x+24,y=spike.y+24;ctx.save();ctx.translate(x,y+(spike.hop>0?-5:Math.sin(spike.idle*2)*1.2));if(invuln>0&&Math.floor(invuln*10)%2===0)ctx.globalAlpha=.48;
    // shadow
    ctx.fillStyle='rgba(0,0,0,.28)';ctx.beginPath();ctx.ellipse(0,18,14,5,0,0,Math.PI*2);ctx.fill();
    const lean=spike.look*.06+Math.sin(spike.idle*.7)*.015;ctx.rotate(lean);const squash=spike.hop>0?1.08:1;ctx.scale(1/squash,squash);
    // arms animated
    ctx.strokeStyle='#29964b';ctx.lineWidth=8;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(-7,-2);ctx.lineTo(-17,-8+Math.sin(spike.idle*3)*2);ctx.moveTo(7,-5);ctx.lineTo(16,-11-Math.sin(spike.idle*3)*2);ctx.stroke();
    ctx.fillStyle='#31a654';rr(-10,-18,20,37,8);ctx.fill();ctx.strokeStyle='rgba(5,50,22,.34)';ctx.lineWidth=1.2;for(const dx of[-4,4]){ctx.beginPath();ctx.moveTo(dx,-14);ctx.lineTo(dx,14);ctx.stroke()}
    // shades
    ctx.shadowColor='#ffcf5a';ctx.shadowBlur=6;ctx.strokeStyle='#d7b548';ctx.lineWidth=1.4;ctx.fillStyle='#090b14';rr(-10,-10,9,7,2);ctx.fill();ctx.stroke();rr(1,-10,9,7,2);ctx.fill();ctx.stroke();ctx.shadowBlur=0;ctx.fillStyle='#d7b548';ctx.fillRect(-1,-8,2,1.5);ctx.fillStyle='rgba(255,255,255,.75)';ctx.fillRect(-8,-9,2,1);ctx.fillRect(3,-9,2,1);
    // tiny smirk
    ctx.strokeStyle='#17351e';ctx.lineWidth=1.2;ctx.beginPath();ctx.arc(2,2,5,.25,1.2);ctx.stroke();ctx.restore();
  }
  function person(h,color){const step=Math.sin(h.p*1.7)*4;ctx.fillStyle=color;ctx.beginPath();ctx.arc(0,-13,6.5,0,Math.PI*2);ctx.fill();rr(-6,-7,12,17,4);ctx.fill();ctx.fillRect(-5+step*.35,9,4,9);ctx.fillRect(1-step*.35,9,4,9)}
  function drawHazard(h){const y=h.row*TILE+24,c=CAST.find(x=>x.kind===h.kind);ctx.save();ctx.translate(h.x+h.w/2,y+Math.sin(h.p)*1.8);if(h.speed<0)ctx.scale(-1,1);ctx.shadowColor=c.color;ctx.shadowBlur=7;
    if(h.kind==='promoter'){person(h,c.color);ctx.strokeStyle='#ffb000';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(-3,-8);ctx.lineTo(0,-1);ctx.lineTo(3,-8);ctx.stroke();ctx.fillStyle=c.color;ctx.fillRect(6,-8,17,5);if(Math.sin(h.p*1.3)>.55){ctx.save();ctx.scale(h.speed<0?-1:1,1);ctx.shadowBlur=10;ctx.fillStyle='rgba(8,6,16,.92)';rr(14,-31,42,15,6);ctx.fill();ctx.fillStyle='#fff';ctx.font="800 8px 'Barlow Condensed'";ctx.textAlign='center';ctx.fillText('BRO.',35,-21);ctx.restore()}}
    else if(h.kind==='timeshare'){person(h,c.color);ctx.fillStyle='#724c2a';ctx.rotate(Math.sin(h.p)*.05);ctx.fillRect(8,-11,13,17);ctx.fillStyle='#fff';ctx.fillRect(10,-9,9,12)}
    else if(h.kind==='selfie'){for(let i=-1;i<=1;i++){ctx.save();ctx.translate(i*13,Math.abs(i)*3);person(h,['#5a8ed6','#d65aa0','#6ac98f'][i+1]);ctx.restore()}ctx.strokeStyle='#aaa';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(0,-12);ctx.lineTo(22,-27);ctx.stroke();ctx.fillStyle='#090b14';ctx.fillRect(18,-32,8,12);if(Math.sin(h.p*2)>.92){ctx.fillStyle='#fff';ctx.globalAlpha=.9;ctx.beginPath();ctx.arc(22,-26,8,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1}}
    else if(h.kind==='magician'){person(h,c.color);ctx.fillStyle='#662bb9';ctx.fillRect(-7,-26,14,3);ctx.fillRect(-5,-34,10,9);ctx.fillStyle='#fff';for(let i=0;i<4;i++){ctx.save();ctx.translate(12,-3);ctx.rotate(-.5+i*.28+Math.sin(h.p)*.08);ctx.fillRect(0,-8,6,9);ctx.restore()}}
    else if(h.kind==='dancer'){ctx.save();ctx.rotate(Math.sin(h.p)*.22);person(h,c.color);ctx.restore();ctx.strokeStyle=c.color;ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(-6,-6);ctx.lineTo(-18,-13+Math.sin(h.p)*7);ctx.moveTo(6,-6);ctx.lineTo(18,-13-Math.sin(h.p)*7);ctx.stroke()}
    else if(h.kind==='showgirl'){person(h,c.color);ctx.strokeStyle='#ffb000';ctx.lineWidth=4;for(let a=-1.2;a<=1.2;a+=.6){ctx.beginPath();ctx.moveTo(0,-17);ctx.lineTo(Math.sin(a)*14,-17-Math.cos(a)*18);ctx.stroke()}}
    else if(h.kind==='mascot'){person(h,c.color);ctx.fillStyle=c.color;ctx.beginPath();ctx.arc(0,-16,11,0,Math.PI*2);ctx.fill();ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(-4,-17,3,0,Math.PI*2);ctx.arc(4,-17,3,0,Math.PI*2);ctx.fill();ctx.fillStyle='#111';ctx.beginPath();ctx.arc(-4,-16,1.3,0,Math.PI*2);ctx.arc(4,-16,1.3,0,Math.PI*2);ctx.fill()}
    else if(h.kind==='swirl'){ctx.rotate(h.p*.55);for(let arm=0;arm<2;arm++){ctx.strokeStyle=arm?'#fff':'#19d3e6';ctx.lineWidth=4;ctx.beginPath();for(let t=0;t<=1;t+=.04){const a=t*Math.PI*4+arm*Math.PI,r=t*17,x=Math.cos(a)*r,yy=Math.sin(a)*r;t===0?ctx.moveTo(x,yy):ctx.lineTo(x,yy)}ctx.stroke()}}
    ctx.restore()}
  function eventDraw(){if(event.t<=0)return;ctx.save();const a=Math.min(1,event.t,.8);ctx.globalAlpha=a;
    if(event.type==='fountain'){ctx.strokeStyle='rgba(160,220,255,.75)';ctx.lineWidth=2;for(let i=0;i<11;i++){const x=50+i*43,h=20+Math.abs(Math.sin(ambientT*2+i))*55;ctx.beginPath();ctx.moveTo(x,205);ctx.quadraticCurveTo(x+(i%2?8:-8),205-h,x+2,205);ctx.stroke()}}
    if(event.type==='rain'){ctx.strokeStyle='rgba(130,205,255,.42)';ctx.lineWidth=1;for(let i=0;i<55;i++){const x=(i*67+ambientT*130)%W,y=(i*41+ambientT*220)%H;ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x-5,y+12);ctx.stroke()}}
    if(event.type==='limo'){const y=8*TILE+8,x=((5.5-event.t)*88)%(W+190)-190;ctx.fillStyle='#0a0a0e';rr(x,y,180,28,9);ctx.fill();ctx.strokeStyle='#ff2e7e';ctx.stroke();ctx.fillStyle='#f9df9a';ctx.beginPath();ctx.arc(x+30,y+28,7,0,Math.PI*2);ctx.arc(x+150,y+28,7,0,Math.PI*2);ctx.fill()}
    if(event.type==='wedding'){ctx.font='24px serif';ctx.fillText('💒  🥂  💍  🕺',80,7*TILE+31)}
    if(event.type==='elvis'){ctx.font='28px serif';const x=((5.5-event.t)*100)% (W+60)-30;ctx.fillText('🕺',x,4*TILE+34)}
    if(event.type==='f1'){ctx.fillStyle='rgba(255,60,60,.75)';for(let x=0;x<W;x+=42)ctx.fillRect(x,10*TILE+34,28,6)}
    if(event.type==='swirlhit'){ctx.translate(W/2,H/2);ctx.rotate(Math.sin(ambientT*12)*.025);ctx.translate(-W/2,-H/2);ctx.strokeStyle='rgba(120,170,255,.25)';for(let r=20;r<300;r+=20){ctx.beginPath();ctx.arc(W/2,H/2,r,0,Math.PI*2);ctx.stroke()}}
    ctx.restore();
  }
  function hitDraw(){if(hit.t<=0)return;const a=Math.min(1,hit.t);ctx.save();ctx.globalAlpha=a;const w=438,x=(W-w)/2,y=H/2-48;ctx.fillStyle='rgba(8,5,17,.94)';rr(x,y,w,88,12);ctx.fill();ctx.strokeStyle='#ffb000';ctx.lineWidth=2;ctx.stroke();ctx.fillStyle='#ffb000';ctx.font="800 14px 'Barlow Condensed'";ctx.textAlign='center';ctx.fillText('⚠ '+hit.label+' ⚠',W/2,y+23);ctx.fillStyle='#fff';ctx.font="700 12px 'Nunito'";wrap(hit.text,W/2,y+45,w-34,16);if(hit.kind==='timeshare'){ctx.save();ctx.translate(W/2,y-10);ctx.rotate(-.09);ctx.fillStyle='#d94141';ctx.font="900 24px 'Barlow Condensed'";ctx.fillText('90-MINUTE PRESENTATION',0,0);ctx.restore()}if(hit.kind==='promoter'){ctx.fillStyle='#fff';ctx.font="900 34px 'Barlow Condensed'";ctx.globalAlpha=.16+.1*Math.sin(ambientT*15);ctx.fillText('BRO. BRO. BRO.',W/2,H*.22)}ctx.restore()}
  function wrap(text,x,y,maxW,lh){const words=text.split(' ');let line='',yy=y;for(const w of words){const test=line+w+' ';if(ctx.measureText(test).width>maxW&&line){ctx.fillText(line.trim(),x,yy);line=w+' ';yy+=lh}else line=test}ctx.fillText(line.trim(),x,yy)}
  function draw(){ctx.save();const sx=shake?(Math.random()-.5)*shake:0,sy=shake?(Math.random()-.5)*shake:0;ctx.translate(sx,sy);sky();skyline();street();doorsDraw();eventDraw();hazards.forEach(drawHazard);if(spike)drawSpike();if(secret){ctx.font='26px serif';ctx.fillText(secret.icon,secret.x,secret.y)}for(const p of particles){ctx.globalAlpha=Math.max(0,p.t);ctx.fillStyle=p.c;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1}for(const p of popups){ctx.globalAlpha=Math.max(0,p.t);ctx.fillStyle=p.color;ctx.font=`800 ${p.big?28:16}px 'Barlow Condensed'`;ctx.textAlign='center';ctx.shadowColor=p.color;ctx.shadowBlur=p.big?12:4;ctx.fillText(p.text,p.x,p.y);ctx.shadowBlur=0;ctx.globalAlpha=1}hitDraw();ctx.restore();if(flash>0){ctx.fillStyle=`rgba(255,${hit.kind==='selfie'?255:225},${hit.kind==='selfie'?255:120},${Math.min(.55,flash*.35)})`;ctx.fillRect(0,0,W,H)}}

  resetSpike();buildHazards(0);buildDoors();updateHUD();
  let prev=performance.now();function frame(now){const dt=Math.min(.05,(now-prev)/1000);prev=now;update(dt);draw();requestAnimationFrame(frame)}requestAnimationFrame(frame);
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(boot,0));else setTimeout(boot,0);
})();
