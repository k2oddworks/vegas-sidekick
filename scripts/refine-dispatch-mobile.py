from pathlib import Path
p=Path(__file__).resolve().parents[1]/'news/index.html'
s=p.read_text()
# Tighten mobile hero and the transition from filters into the newest story.
s=s.replace(".n-hero{min-height:470px;padding:100px 20px 34px;background-position:62% center;align-items:flex-end}",".n-hero{min-height:410px;padding:72px 20px 28px;background-position:62% center;align-items:flex-end}",1)
s=s.replace(".n-wrap{padding-left:18px;padding-right:18px}",".n-wrap{padding:24px 18px 72px}",1)
p.write_text(s)
