from pathlib import Path
p=Path(__file__).resolve().parents[1]/'index.html'
s=p.read_text()
# A focused mobile-only polish layer: tighter rhythm, better crops, larger tap targets,
# cleaner text wrapping, and a more Dispatch-like editorial density.
css='''
<style id="mobile-homepage-polish">
@media(max-width:760px){
  .wrap{width:min(100% - 32px,1180px)}
  .hero-inner{padding:28px 0 24px;gap:14px}
  .hero-copy{max-width:38rem;line-height:1.55}
  .shop-tools .wrap{padding:12px 0 11px}
  .search-row{min-height:46px}.search-row button{min-width:76px;min-height:46px}
  .chip{min-height:40px;display:inline-flex;align-items:center;padding:8px 14px}
  .catalog{padding:27px 0 38px}.section-head{margin-bottom:12px}.section-head p{line-height:1.48}
  .show-card{grid-template-columns:116px minmax(0,1fr);padding:10px 0;min-height:96px}
  .poster{height:76px;aspect-ratio:auto}.poster img{object-position:center 28%}
  .card-body{min-width:0}.card-name{line-height:1.18;overflow-wrap:anywhere}.card-venue{white-space:normal}
  .show-card,.path,.price-link,.mini-card,.guide-card{touch-action:manipulation}
  .path{min-height:108px;padding:17px 48px 17px 18px}.paths{padding-bottom:38px}
  .trust-sec{padding:36px 0}.trust-card{padding:15px}.trust-card b{font-size:.86rem}
  .price-shop,.editorial,.about-block{padding:38px 0}
  .price-link{min-height:52px;padding:14px 15px}
  .edit-grid{gap:28px}.edit-head{margin-bottom:10px}.edit-head a{padding:8px 0;min-height:36px;display:flex;align-items:center}
  .mini-list{gap:8px}.mini-card{grid-template-columns:100px minmax(0,1fr);min-height:82px;padding:8px;gap:11px}
  .mini-card img{width:100px;height:66px;object-position:center 30%}
  .mini-card b{font-size:.84rem;line-height:1.28;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
  .guide-card{min-height:70px;padding:14px 42px 14px 15px}
  .about-inner{align-items:start}.about-inner p{line-height:1.52}
}
@media(max-width:420px){
  .hero h1{font-size:clamp(2.15rem,11.5vw,3.25rem)}
  .show-card{grid-template-columns:108px minmax(0,1fr)}.poster{height:72px}
  .mini-card{grid-template-columns:92px minmax(0,1fr)}.mini-card img{width:92px;height:64px}
}
</style>
'''
if 'id="mobile-homepage-polish"' not in s:
    s=s.replace('</head>',css+'</head>',1)
p.write_text(s)
