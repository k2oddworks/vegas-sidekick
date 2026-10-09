/* Savings category badges are derived from verified show data, never a manual show allowlist. */
(()=>{'use strict';
const DEAL_MIN=5,LARGE_MIN=20,MAX_AGE_DAYS=30;let records=new Map();
const slugOf=c=>(c.querySelector('a[href^="/shows/"]')?.getAttribute('href')||'').split('/').filter(Boolean).pop();
const money=n=>'$'+(Number.isInteger(n)?String(n):n.toFixed(2));
const fresh=value=>{
 if(typeof value!=='string'||!/^\d{4}-\d{2}-\d{2}$/.test(value))return false;
 const stamp=Date.parse(value+'T00:00:00Z'),age=Math.floor((Date.now()-stamp)/86400000);
 return Number.isFinite(stamp)&&age>=0&&age<=MAX_AGE_DAYS;
};
const deal=r=>{
 if(!r||r.status!=='active'||typeof r.our_price!=='number'||typeof r.regular_price!=='number'||!Number.isFinite(r.our_price)||!Number.isFinite(r.regular_price))return null;
 const saving=r.regular_price-r.our_price;
 if(saving<DEAL_MIN)return null;
 // Fail closed on expired large-price evidence rather than repeating stale discounts.
 if(saving>=LARGE_MIN&&!fresh(r.price_source_last_checked_on))return null;
 return {amount:Math.round(saving),large:saving>=LARGE_MIN,regular:r.regular_price};
};
const setText=(el,value)=>{if(el&&el.textContent!==value)el.textContent=value;};
function decorate(){
 document.querySelectorAll('.show-card').forEach(c=>{
  const r=records.get(slugOf(c)),d=deal(r),row=c.querySelector('.card-price-row');
  c.dataset.vsDeal=d?'1':'0';c.classList.toggle('vs-savings-pilot',!!d?.large);
  if(!row)return;
  const price=row.querySelector('.card-price');
  if(r&&typeof r.our_price==='number'&&Number.isFinite(r.our_price))setText(price,money(r.our_price));
  let regular=row.querySelector('.card-regular'),badge=row.querySelector('.card-save-badge');
  if(!d){regular?.remove();badge?.remove();return;}
  if(!price)return;
  if(!regular){regular=document.createElement('span');regular.className='card-regular';price.insertAdjacentElement('afterend',regular);}
  if(!badge){badge=document.createElement('span');badge.className='card-save-badge';regular.insertAdjacentElement('afterend',badge);}
  setText(regular,money(d.regular));setText(badge,'Save $'+d.amount);
 });
}
window.vsSavingsSort=function(btn){
 const grid=document.querySelector('.show-grid');if(!grid)return;
 document.querySelectorAll('.sort-btn,.filter-btn').forEach(x=>x.classList.remove('active'));btn?.classList.add('active');
 [...grid.children].sort((a,b)=>(deal(records.get(slugOf(b)))?.amount||0)-(deal(records.get(slugOf(a)))?.amount||0)).forEach(x=>grid.appendChild(x));decorate();
};
window.vsDealsFilter=function(btn){
 decorate();const cards=[...document.querySelectorAll('.show-card')],active=btn?.dataset.active!=='1';
 if(btn){btn.dataset.active=active?'1':'0';btn.classList.toggle('active',active);btn.textContent=active?'🔥 Showing Deals':'🔥 Deals';}
 cards.forEach(c=>{c.style.display=active&&c.dataset.vsDeal!=='1'?'none':'';});
 const count=document.querySelector('.show-count-wrap');
 if(count)count.textContent=cards.filter(c=>c.style.display!=='none').length+(active?' deals':' shows');
};
fetch('/data/show-database.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw Error('Show Database unavailable');return r.json();}).then(db=>{
 records=new Map((db.records||[]).filter(r=>r.status==='active').map(r=>[r.slug,r]));decorate();
 const grid=document.querySelector('.show-grid');
 if(grid)new MutationObserver(decorate).observe(grid,{childList:true,subtree:true});
}).catch(()=>{/* Do not invent savings when the source data is unavailable. */});
})();