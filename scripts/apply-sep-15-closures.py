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
s=s.replace('"dateModified":"2026-09-07","lastReviewed":"2026-09-07"','"dateModified":"2026-09-15","lastReviewed":"2026-09-15"')
s=s.replace('Last updated September 2026 · Your date and seat determine the final total.','Show info confirmed September 2026')
s=s.replace('Las Vegas show and ticketing guidance. Last updated September 2026.','Las Vegas show and ticketing guidance. Show info confirmed September 2026.')

banner='<div class="show-closing-banner" role="status" style="background:#fff3cd;color:#3d2c00;padding:14px 20px;text-align:center;font-weight:800;border-bottom:1px solid #e4bd55">Final performance October 10, 2026. Tickets remain available for performances through the closing date.</div>'
spacer='<style id="awakening-closing-banner-style">.show-closing-banner-spacer{height:85px}@media(max-width:980px){.show-closing-banner-spacer{height:54px}}</style><div class="show-closing-banner-spacer" aria-hidden="true"></div>'
if 'Final performance October 10, 2026.' not in s:
 s=s.replace('<div id="vs-header"></div>','<div id="vs-header"></div>'+spacer+banner,1)
elif 'show-closing-banner-spacer' not in s:
 s=s.replace('<div id="vs-header"></div>','<div id="vs-header"></div>'+spacer,1)

# Awakening-only booking experiment: compact the conversion module without touching the shared system.
booking_style='''<style id="awakening-booking-experiment">
#showtimes.vs-booking-section{padding:42px 0 44px;background:linear-gradient(180deg,#f8f4ff 0%,#f2eaff 100%)}
#showtimes .wrap{max-width:1080px}
#showtimes .vs-booking-shell{padding:20px 24px 0;border-radius:24px}
#showtimes .vs-awakening-closing-chip{width:max-content;max-width:100%;margin:0 auto 9px;padding:7px 12px;border-radius:999px;background:#171225;color:#FFB000;font:800 .7rem/1 'Plus Jakarta Sans',sans-serif;letter-spacing:.09em;text-transform:uppercase}
#showtimes .vs-booking-copy h2{font-size:clamp(2rem,4vw,3rem);margin:0 0 4px}
#showtimes .vs-booking-summary{gap:1px;font-size:.92rem}
#showtimes .vs-booking-summary strong{font-size:.76rem;text-transform:uppercase;letter-spacing:.07em;color:#7b6e89}
#showtimes .vs-day-picker{margin:15px 0 13px;gap:7px}
#showtimes .vs-day{min-height:50px;border-radius:12px;font-size:.84rem}
#showtimes .vs-day small{margin-top:5px;font-size:.61rem}
#showtimes .vs-time-panel{max-width:none;margin:0;padding:14px 16px;display:grid;grid-template-columns:auto minmax(240px,1fr) minmax(220px,.9fr);grid-template-areas:'heading times primary' '. all all';align-items:center;gap:9px 14px;border-radius:18px}
#showtimes .vs-time-panel h3{grid-area:heading;margin:0;font-size:1rem;white-space:nowrap}
#showtimes .vs-awakening-selected-day{position:absolute!important;width:1px!important;height:1px!important;padding:0!important;margin:-1px!important;overflow:hidden!important;clip:rect(0,0,0,0)!important;white-space:nowrap!important;border:0!important}
#showtimes .vs-time-grid{grid-area:times;grid-template-columns:repeat(2,minmax(108px,1fr));gap:8px}
#showtimes .vs-time-grid a{min-height:46px;border-radius:11px;font-size:.9rem}
#showtimes .vs-primary-book{grid-area:primary;margin:0;min-height:48px;border-radius:12px;font-size:0!important;padding:10px 16px}
#showtimes .vs-primary-book:after{content:'Get Tickets →';font:900 .92rem/1 'Plus Jakarta Sans',sans-serif}
#showtimes .vs-all-dates{grid-area:all;justify-self:center;display:inline-flex;min-height:0;margin:0;padding:3px 8px;border:0;background:transparent;box-shadow:none;color:#5e23bd;font-size:.82rem;text-decoration:underline;text-underline-offset:3px}
#showtimes .vs-all-dates:hover,#showtimes .vs-all-dates:focus-visible{border:0;background:transparent;box-shadow:none;color:#421486}
#showtimes .vs-awakening-deadline{display:flex;align-items:center;justify-content:center;gap:8px;margin:11px auto 0;color:#5d526a;font-size:.8rem}
#showtimes .vs-awakening-deadline strong{color:#25133f}
#showtimes .vs-awakening-deadline i{width:4px;height:4px;border-radius:50%;background:#ff2e7e}
#showtimes .vs-booking-art{height:92px;margin:16px -24px 0}
#showtimes .vs-art-moon{width:76px;height:76px;right:11%;top:5px}
#showtimes .vs-art-sphere{width:62px;height:62px;right:12%;bottom:-18px}
#showtimes .vs-art-strip{height:50px;padding:0 14px;gap:6px}
#showtimes .vs-art-strip i:nth-child(1){height:24px}#showtimes .vs-art-strip i:nth-child(2){height:39px}#showtimes .vs-art-strip i:nth-child(3){height:31px}#showtimes .vs-art-strip i:nth-child(4){height:46px}#showtimes .vs-art-strip i:nth-child(5){height:29px}#showtimes .vs-art-strip i:nth-child(6){height:41px}#showtimes .vs-art-strip i:nth-child(7){height:34px}#showtimes .vs-art-strip i:nth-child(8){height:44px}
@media(max-width:700px){
 #showtimes.vs-booking-section{padding:34px 0 36px}
 #showtimes .vs-booking-shell{padding:17px 13px 0;border-radius:20px}
 #showtimes .vs-awakening-closing-chip{font-size:.64rem;padding:7px 10px;margin-bottom:8px}
 #showtimes .vs-booking-copy h2{font-size:2rem}
 #showtimes .vs-booking-summary{font-size:.82rem;line-height:1.4}
 #showtimes .vs-booking-summary strong{font-size:.67rem}
 #showtimes .vs-day-picker{margin:13px 0 11px;gap:5px;padding-bottom:1px}
 #showtimes .vs-day{min-height:48px;font-size:.76rem;border-radius:10px}
 #showtimes .vs-time-panel{display:block;padding:13px;border-radius:16px}
 #showtimes .vs-time-panel h3{margin:0 0 9px;font-size:.92rem}
 #showtimes .vs-time-grid{gap:7px}
 #showtimes .vs-time-grid a{min-height:45px;font-size:.88rem}
 #showtimes .vs-primary-book{margin-top:9px;min-height:50px}
 #showtimes .vs-all-dates{margin:7px auto 0;font-size:.79rem}
 #showtimes .vs-awakening-deadline{margin-top:10px;gap:6px;flex-wrap:wrap;text-align:center;font-size:.74rem;line-height:1.35}
 #showtimes .vs-booking-art{height:76px;margin:13px -13px 0}
 #showtimes .vs-art-moon{width:62px;height:62px;top:3px}
 #showtimes .vs-art-sphere{width:50px;height:50px;bottom:-15px}
 #showtimes .vs-art-strip{height:42px}
}
</style>'''
if 'id="awakening-booking-experiment"' in s:
 s=re.sub(r'<style id="awakening-booking-experiment">[\s\S]*?</style>',booking_style,s,count=1)
else:
 s=s.replace('</head>',booking_style+'</head>',1)

booking_section='''<section class="section vs-booking-section" id="showtimes"><div class="wrap"><div class="vs-booking-shell" data-ticket-url="https://spotlight.vegas/shows/production/awakening/ref/vegassidekick"><div class="vs-awakening-closing-chip">Final performances · Oct 10</div><div class="vs-booking-copy"><h2>Find your showtime</h2><p class="vs-booking-summary"><strong>Regular weekly schedule</strong><span>Mon, Tue, Fri, Sat · 6:30 PM &amp; 9 PM; Sun · 4 PM &amp; 7 PM</span></p></div><div aria-label="Choose a show day" class="vs-day-picker" role="tablist"><button aria-selected="true" class="vs-day is-active" data-day="Monday" data-times="6:30 PM|9 PM" role="tab" type="button"><span>Mon</span></button><button aria-selected="false" class="vs-day" data-day="Tuesday" data-times="6:30 PM|9 PM" role="tab" type="button"><span>Tue</span></button><button aria-selected="false" class="vs-day is-dark" disabled="" role="tab" type="button"><span>Wed</span><small>Dark</small></button><button aria-selected="false" class="vs-day is-dark" disabled="" role="tab" type="button"><span>Thu</span><small>Dark</small></button><button aria-selected="false" class="vs-day" data-day="Friday" data-times="6:30 PM|9 PM" role="tab" type="button"><span>Fri</span></button><button aria-selected="false" class="vs-day" data-day="Saturday" data-times="6:30 PM|9 PM" role="tab" type="button"><span>Sat</span></button><button aria-selected="false" class="vs-day" data-day="Sunday" data-times="4 PM|7 PM" role="tab" type="button"><span>Sun</span></button></div><div aria-live="polite" class="vs-time-panel"><h3>Choose a time <span class="vs-awakening-selected-day">for <span data-selected-day="">Monday</span></span></h3><div class="vs-time-grid"><a href="https://spotlight.vegas/shows/production/awakening/ref/vegassidekick" rel="noopener sponsored" target="_blank">6:30 PM</a><a href="https://spotlight.vegas/shows/production/awakening/ref/vegassidekick" rel="noopener sponsored" target="_blank">9 PM</a></div><a class="vs-primary-book vs-ticket-primary" href="https://spotlight.vegas/shows/production/awakening/ref/vegassidekick" rel="noopener sponsored" target="_blank">Get Tickets for Monday →</a><a class="vs-all-dates" href="https://spotlight.vegas/shows/production/awakening/ref/vegassidekick" rel="noopener sponsored" target="_blank">See all dates &amp; times →</a></div><div class="vs-awakening-deadline"><strong>Final performance October 10</strong><i aria-hidden="true"></i><span>Remaining dates available now.</span></div><div aria-hidden="true" class="vs-booking-art"><div class="vs-art-moon"></div><div class="vs-art-sphere"></div><div class="vs-art-strip"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div></div></div></div></section>'''
s=re.sub(r'<section class="section vs-booking-section" id="showtimes">[\s\S]*?</section>\s*<section class="section alt" id="photos">',booking_section+'\n<section class="section alt" id="photos">',s,count=1)
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
