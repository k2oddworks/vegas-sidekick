from pathlib import Path
import json, re
ROOT=Path(__file__).resolve().parents[1]

def rw(path, reps):
 p=ROOT/path
 if not p.exists(): return
 s=p.read_text()
 old=s
 for a,b in reps: s=s.replace(a,b)
 if s!=old: p.write_text(s)

# Awakening: final performance Oct 10, Sunday second performance is 7 PM.
p=ROOT/'shows/spectaculars/awakening/index.html'
s=p.read_text()
s=s.replace('"endDate":"2027-01-01"','"endDate":"2026-10-10"')
s=s.replace('"priceValidUntil":"2027-12-31"','"priceValidUntil":"2026-10-10"')
s=s.replace('["https://schema.org/Sunday"],"startTime":"18:00"','["https://schema.org/Sunday"],"startTime":"19:00"')
s=s.replace('Sun · 4 PM &amp; 6 PM','Sun · 4 PM &amp; 7 PM').replace('data-times="4 PM|6 PM"','data-times="4 PM|7 PM"')
s=s.replace('Monday, Tuesday, Friday, Saturday, and Sunday at 6:30 PM and 9:00 PM. The show is dark on Wednesday and Thursday.','Monday, Tuesday, Friday and Saturday at 6:30 PM and 9:00 PM, with Sunday performances at 4:00 PM and 7:00 PM. The final performance is October 10, 2026.')
banner='<div class="show-closing-banner" role="status" style="background:#fff3cd;color:#3d2c00;padding:14px 20px;text-align:center;font-weight:800;border-bottom:1px solid #e4bd55">Final performances: Awakening closes October 10, 2026. Tickets are only available through the final performance.</div>'
s=s.replace('<div id="vs-header"></div>','<div id="vs-header"></div>'+banner,1)
p.write_text(s)

# Database record.
db=ROOT/'data/show-database.json'
d=json.loads(db.read_text())
for r in d.get('records',[]):
 if r.get('slug')=='awakening':
  r['schedule_summary']='Mon, Tue, Fri, Sat · 6:30 PM & 9 PM; Sun · 4 PM & 7 PM'
  r['status']='closing'
  r['closing_date']='2026-10-10'
  r['verified_on']='2026-09-15'
  if isinstance(r.get('spotlight'),dict):
   days=r['spotlight'].get('schedule_days',{})
   if 'Sunday' in days: days['Sunday']=['4 PM','7 PM']
 if r.get('slug')=='mad-apple': r['status']='closed'
d['updated_on']='2026-09-15'
db.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')

# Remove Mad Apple from live Cirque catalog, preserve its historical page.
cp=ROOT/'shows/cirque/index.html'
c=cp.read_text()
# Remove SHOWS object/card entries containing mad-apple where represented as one-line JS/object markup.
c=re.sub(r"\n?\s*\{[^\n{}]*slug:'mad-apple'[^\n{}]*\},?",'',c)
c=re.sub(r'<a[^>]+href="/shows/cirque/mad-apple/"[\s\S]*?</a>','',c)
c=c.replace('Mad Apple adds rock music, burlesque, and a downtown New York energy. ','')
c=c.replace('five resident Cirque','four resident Cirque').replace('five Cirque','four Cirque')
cp.write_text(c)

# Remove active Mad Apple references from the Cirque guide without deleting closure/history links generally.
g=ROOT/'guides/best-cirque-shows/index.html'
if g.exists():
 x=g.read_text()
 x=re.sub(r'<a[^>]+href="/shows/cirque/mad-apple/"[\s\S]*?</a>','',x)
 x=x.replace(' and <a href="/news/mad-apple-closing-september-5/" style="color:var(--blue-lt);font-weight:600;"></a>','')
 g.write_text(x)

# Normal post-final closing checklist, deliberately not executed yet.
check=ROOT/'docs/awakening-closing-checklist.md'
check.write_text('''# Awakening closing checklist\n\nRun after the final performance on October 10, 2026.\n\n- Mark Awakening closed in `data/show-database.json`.\n- Convert the show page from closing to historical/closed treatment; do not delete it.\n- Remove active ticket CTAs and active Offer/Event scheduling schema.\n- Remove Awakening from active homepage, spectaculars catalog, all-shows/search data, venue pages, and active guides.\n- Update category counts and any price/ranking claims affected by the closure.\n- Keep useful historical copy, photos, closure notice, canonical URL and internal links live.\n- Run repo link, structured-data and show-page audits.\n- Deploy to main and independently verify the archived page plus affected catalogs.\n''')
