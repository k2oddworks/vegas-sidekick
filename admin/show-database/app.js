const DATA_URL='/data/show-database.json';
const DRAFT_KEY='vs-show-database-draft-v1';
let source=null, rows=[], selected=new Set(), statusFilter='all', categoryFilter='all', searchTerm='', sortKey='name', sortDir=1, drawerSlug=null;

const $=s=>document.querySelector(s);
const esc=v=>String(v??'').replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
const money=v=>v===null||v===''?'':Number(v);
const today=()=>new Date().toISOString().slice(0,10);

async function init(){
  const res=await fetch(DATA_URL,{cache:'no-store'});
  if(!res.ok) throw new Error('Could not load show database');
  source=await res.json();
  const saved=localStorage.getItem(DRAFT_KEY);
  if(saved){
    try{ const draft=JSON.parse(saved); rows=draft.records||source.records; markDirty(true); }
    catch{ rows=structuredClone(source.records); }
  }else rows=structuredClone(source.records);
  buildCategoryFilter(); bind(); render();
}

function bind(){
  $('#search').addEventListener('input',e=>{searchTerm=e.target.value.trim().toLowerCase();renderRows()});
  $('#status-filters').addEventListener('click',e=>{const b=e.target.closest('[data-filter]');if(!b)return;statusFilter=b.dataset.filter;document.querySelectorAll('.filter').forEach(x=>x.classList.toggle('active',x===b));renderRows()});
  $('#category-filter').addEventListener('change',e=>{categoryFilter=e.target.value;renderRows()});
  $('#discard-btn').addEventListener('click',discardDraft);
  $('#export-btn').addEventListener('click',exportJson);
  $('#select-all').addEventListener('change',e=>{visibleRows().forEach(r=>e.target.checked?selected.add(r.slug):selected.delete(r.slug));renderRows();renderBulk()});
  $('#clear-selection').addEventListener('click',()=>{selected.clear();renderRows();renderBulk()});
  $('#bulk-status').addEventListener('change',e=>{if(!e.target.value)return;selected.forEach(slug=>patch(slug,'status',e.target.value,false));e.target.value='';persist();render()});
  $('#bulk-verified-btn').addEventListener('click',()=>{const v=$('#bulk-verified').value||today();selected.forEach(slug=>{patch(slug,'verified_on',v,false);patch(slug,'verification','verified',false)});persist();render()});
  document.querySelector('thead').addEventListener('click',e=>{const h=e.target.closest('[data-sort]');if(!h)return;const k=h.dataset.sort;if(sortKey===k)sortDir*=-1;else{sortKey=k;sortDir=1}renderRows()});
  $('#drawer-close').addEventListener('click',closeDrawer);$('#drawer-backdrop').addEventListener('click',closeDrawer);
}

function buildCategoryFilter(){
  const cats=[...new Set(source.records.map(r=>r.category).filter(Boolean))].sort();
  $('#category-filter').innerHTML='<option value="all">All categories</option>'+cats.map(c=>`<option value="${esc(c)}">${esc(title(c))}</option>`).join('');
}
function title(v){return String(v||'').replace(/-/g,' ').replace(/\b\w/g,c=>c.toUpperCase())}

function visibleRows(){
  let out=rows.filter(r=>{
    const reviewHit=r.verification==='needs_review'||r.verification==='partial';
    if(statusFilter==='active'&&r.status!=='active')return false;
    if(statusFilter==='closed'&&r.status!=='closed')return false;
    if(statusFilter==='needs_review'&&!reviewHit)return false;
    if(categoryFilter!=='all'&&r.category!==categoryFilter)return false;
    if(searchTerm){const hay=[r.name,r.slug,r.venue,r.showroom,r.schedule_summary,r.category].join(' ').toLowerCase();if(!hay.includes(searchTerm))return false}
    return true;
  });
  out.sort((a,b)=>{
    let av=a[sortKey],bv=b[sortKey];
    if(typeof av==='number'||typeof bv==='number'){av=av??Number.MAX_SAFE_INTEGER;bv=bv??Number.MAX_SAFE_INTEGER;return (av-bv)*sortDir}
    return String(av??'').localeCompare(String(bv??''),undefined,{numeric:true,sensitivity:'base'})*sortDir;
  });
  return out;
}

function render(){renderStats();renderRows();renderBulk();if(drawerSlug&&rows.some(r=>r.slug===drawerSlug))renderDrawer(drawerSlug)}
function renderStats(){
  const active=rows.filter(r=>r.status==='active').length,closed=rows.filter(r=>r.status==='closed').length,review=rows.filter(r=>['needs_review','partial'].includes(r.verification)).length,stale=rows.filter(r=>r.status==='active'&&(!r.verified_on||daysOld(r.verified_on)>30)).length;
  $('#stats').innerHTML=[['Active',active],['Closed archives',closed],['Need review',review],['30+ days / unverified',stale]].map(([l,n])=>`<div class="stat"><div class="num">${n}</div><div class="lbl">${l}</div></div>`).join('');
}
function daysOld(v){if(!v)return 9999;const d=new Date(v+'T00:00:00');return Math.floor((Date.now()-d.getTime())/86400000)}

function renderRows(){
  const list=visibleRows(), tbody=$('#show-rows');
  $('#empty').hidden=!!list.length;
  tbody.innerHTML=list.map(rowHtml).join('');
  tbody.querySelectorAll('[data-field]').forEach(el=>{
    el.addEventListener('change',handleCellChange);
    el.addEventListener('keydown',e=>{if(e.key==='Enter'&&e.target.tagName==='INPUT'){e.preventDefault();e.target.blur()}});
  });
  tbody.querySelectorAll('[data-open]').forEach(el=>el.addEventListener('click',()=>openDrawer(el.dataset.open)));
  tbody.querySelectorAll('[data-select]').forEach(el=>el.addEventListener('change',e=>{e.target.checked?selected.add(e.target.dataset.select):selected.delete(e.target.dataset.select);renderBulk()}));
  const visible=list.map(r=>r.slug),all=visible.length&&visible.every(s=>selected.has(s));$('#select-all').checked=!!all;
}

function rowHtml(r){
  const review=r.verification||'needs_review';
  return `<tr data-slug="${esc(r.slug)}">
    <td class="check-col"><input type="checkbox" data-select="${esc(r.slug)}" ${selected.has(r.slug)?'checked':''}></td>
    <td class="row-name"><button class="show-name" data-open="${esc(r.slug)}">${esc(r.name)}</button><span class="show-path">${esc(r.page_path)}</span></td>
    <td>${selectCell(r,'status',[['active','Active'],['closed','Closed'],['needs_review','Needs Review']],`status-${r.status}`)}</td>
    <td class="num">${inputCell(r,'our_price','number','1')}</td>
    <td class="num">${inputCell(r,'regular_price','number','1')}</td>
    <td>${inputCell(r,'venue')}</td>
    <td>${inputCell(r,'showroom')}</td>
    <td class="num">${inputCell(r,'runtime_minutes','number','1')}</td>
    <td>${inputCell(r,'age_summary')}</td>
    <td class="wide">${inputCell(r,'schedule_summary')}</td>
    <td class="url-cell">${inputCell(r,'ticket_url','url')}</td>
    <td>${inputCell(r,'verified_on','date')}</td>
    <td><span class="review-pill review-${esc(review)}">${reviewLabel(review)}</span></td>
  </tr>`;
}
function inputCell(r,field,type='text',step=''){return `<input class="edit" data-field="${field}" data-slug="${esc(r.slug)}" type="${type}" ${step?`step="${step}"`:''} value="${esc(r[field]??'')}">`}
function selectCell(r,field,options,extra=''){return `<select class="edit status-select ${extra}" data-field="${field}" data-slug="${esc(r.slug)}">${options.map(([v,l])=>`<option value="${v}" ${r[field]===v?'selected':''}>${l}</option>`).join('')}</select>`}
function reviewLabel(v){return v==='verified'?'✓ Verified':v==='partial'?'◐ Partial':'! Review'}

function handleCellChange(e){let v=e.target.value;if(e.target.type==='number')v=v===''?null:Number(v);patch(e.target.dataset.slug,e.target.dataset.field,v,true)}
function patch(slug,field,value,rerender){const r=rows.find(x=>x.slug===slug);if(!r)return;r[field]=value;if(!['verified_on','verification'].includes(field)&&r.verification==='verified')r.verification='needs_review';persist();if(rerender)render()}
function persist(){localStorage.setItem(DRAFT_KEY,JSON.stringify({schema_version:source.schema_version,updated_on:today(),records:rows}));markDirty(true)}
function markDirty(dirty){const el=$('#draft-state');el.classList.toggle('dirty',dirty);el.classList.toggle('clean',!dirty);el.querySelector('span:last-child').textContent=dirty?'Draft changes saved locally':'Saved locally'}
function discardDraft(){if(!confirm('Discard all local Show Database changes and reload the repository version?'))return;localStorage.removeItem(DRAFT_KEY);rows=structuredClone(source.records);selected.clear();markDirty(false);render()}
function exportJson(){const payload={schema_version:source.schema_version,updated_on:today(),source:'Vegas Sidekick Show Database',records:rows};const blob=new Blob([JSON.stringify(payload,null,2)+'\n'],{type:'application/json'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=`vegas-sidekick-show-database-${today()}.json`;a.click();URL.revokeObjectURL(a.href)}

function renderBulk(){const n=selected.size;$('#bulkbar').hidden=!n;$('#selected-count').textContent=n}

function openDrawer(slug){drawerSlug=slug;renderDrawer(slug);$('#drawer').classList.add('open');$('#drawer').setAttribute('aria-hidden','false');$('#drawer-backdrop').hidden=false}
function closeDrawer(){$('#drawer').classList.remove('open');$('#drawer').setAttribute('aria-hidden','true');$('#drawer-backdrop').hidden=true;drawerSlug=null}
function renderDrawer(slug){
  const r=rows.find(x=>x.slug===slug);if(!r)return;
  $('#drawer-title').textContent=r.name;$('#drawer-category').textContent=title(r.category)+' · '+title(r.status);
  const fields=[
    ['name','Show name','text'],['category','Category','text'],['status','Status','select'],['our_price','Our price','number'],['regular_price','Regular price','number'],['runtime_minutes','Runtime (minutes)','number'],['venue','Venue / property','text'],['showroom','Showroom','text'],['age_summary','Age policy','text'],['schedule_summary','Schedule summary','textarea'],['ticket_url','Ticket URL','textarea'],['official_trailer','Official trailer','text'],['verified_on','Last verified','date'],['verification','Verification state','select'],['notes','Internal notes','textarea']
  ];
  let html='<div class="drawer-grid">';
  for(const [f,label,type] of fields){
    const full=['age_summary','schedule_summary','ticket_url','notes'].includes(f)?' full':'';
    let control='';
    if(f==='status') control=`<select data-drawer-field="${f}"><option value="active" ${r[f]==='active'?'selected':''}>Active</option><option value="closed" ${r[f]==='closed'?'selected':''}>Closed</option><option value="needs_review" ${r[f]==='needs_review'?'selected':''}>Needs Review</option></select>`;
    else if(f==='verification') control=`<select data-drawer-field="${f}"><option value="verified" ${r[f]==='verified'?'selected':''}>Verified</option><option value="partial" ${r[f]==='partial'?'selected':''}>Partial</option><option value="needs_review" ${r[f]==='needs_review'?'selected':''}>Needs review</option></select>`;
    else if(type==='textarea') control=`<textarea data-drawer-field="${f}">${esc(r[f]??'')}</textarea>`;
    else control=`<input class="field-input" data-drawer-field="${f}" type="${type}" value="${esc(r[f]??'')}">`;
    html+=`<label class="field${full}"><span class="field-label">${label}</span>${control}</label>`;
  }
  html+='</div><div class="drawer-links"><a href="'+esc(r.page_path)+'" target="_blank" rel="noopener">Open live page ↗</a></div>';
  $('#drawer-body').innerHTML=html;
  $('#drawer-body').querySelectorAll('[data-drawer-field]').forEach(el=>el.addEventListener('change',e=>{let v=e.target.value;if(e.target.type==='number')v=v===''?null:Number(v);patch(slug,e.target.dataset.drawerField,v,false);renderStats();renderRows();renderDrawer(slug)}));
}

init().catch(err=>{console.error(err);document.body.innerHTML='<div style="padding:40px;color:white;font-family:Inter,sans-serif"><h1>Show Database could not load</h1><p>'+esc(err.message)+'</p></div>'});
