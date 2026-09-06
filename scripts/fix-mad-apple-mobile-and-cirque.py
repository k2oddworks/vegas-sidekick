from pathlib import Path
import json,re

ROOT = Path('.')

def replace_required(path, old, new, label):
    p = ROOT / path
    text = p.read_text(encoding='utf-8')
    if old not in text:
        raise SystemExit(f'Missing expected text for {label} in {path}')
    text = text.replace(old, new, 1)
    p.write_text(text, encoding='utf-8')

# 1) Cirque category: remove the retired show from the live JS-driven list and fix live counts/copy.
cirque = ROOT / 'shows/cirque/index.html'
text = cirque.read_text(encoding='utf-8')
mad_line = "  { order:5, slug:'mad-apple', name:'Mad Apple', subtitle:'by Cirque du Soleil', venue:'New York-New York Theater', price:56, pd:'$56', sp:false, pills:['Cirque Goes Wild','Adult & Urban'], img:'/images/mad-apple-hero.jpg', duration:'90 min', age:'Ages 18+', schedule:'Tue–Sat · 7 & 9:30 PM' }\n"
if mad_line not in text:
    raise SystemExit('Mad Apple active SHOWS entry not found on Cirque category')
text = text.replace(mad_line, '', 1)
text = text.replace('"numberOfItems": 5,', '"numberOfItems": 4,', 1)
text = text.replace('content="5 Cirque du Soleil shows in one city. Real prices. No guesswork. Compare and book in seconds."', 'content="4 current Cirque du Soleil shows in one city. Real prices. No guesswork. Compare and book in seconds."', 1)
text = text.replace('No city on Earth has more Cirque du Soleil than Las Vegas — five resident productions, each in a purpose-built theater, from the aquatic icon &ldquo;O&rdquo; to the newest party show, Mad Apple. Compare every Cirque and acrobatic spectacular below, with real starting prices and our honest take on which is worth the splurge.', 'Las Vegas still has four resident Cirque du Soleil productions, each with a very different reason to go — from the aquatic spectacle of &ldquo;O&rdquo; to the original weirdness of Mystère. Compare the current lineup below, with real starting prices and our honest take on which is worth the splurge.', 1)
cirque.write_text(text, encoding='utf-8')

# 2) Retired Mad Apple product page: image first on mobile, but cap its height so status/copy arrives quickly.
product = ROOT / 'shows/cirque/mad-apple/index.html'
text = product.read_text(encoding='utf-8')
old = "@media(max-width:760px){.grid{grid-template-columns:1fr}.hero img{order:-1}.facts{grid-template-columns:repeat(2,1fr)}.cards{grid-template-columns:1fr}.hero{padding-top:22px}}"
new = "@media(max-width:760px){.grid{grid-template-columns:1fr;gap:24px}.grid>img{order:-1;width:100%;height:clamp(260px,62vw,390px);aspect-ratio:auto;object-fit:cover;object-position:center 42%}.facts{grid-template-columns:repeat(2,1fr)}.cards{grid-template-columns:1fr}.hero{padding-top:22px;padding-bottom:48px}}"
if old not in text:
    raise SystemExit('Expected Mad Apple product mobile rule not found')
text = text.replace(old, new, 1)
product.write_text(text, encoding='utf-8')

# 3) Dispatch article: standard mobile hero is editorial, not near-full-screen.
article = ROOT / 'news/mad-apple-closing-september-5/index.html'
text = article.read_text(encoding='utf-8')
anchor = "  .d-dot{opacity:.5}\n"
mobile = "  .d-dot{opacity:.5}\n  /* Dispatch mobile standard: keep the hero useful, not full-screen. */\n  @media(max-width:600px){\n    .d-hero{height:clamp(360px,104vw,430px);min-height:0;max-height:430px}\n    .d-hero img{object-position:center 44%}\n    .d-hero-content{padding:22px 20px 28px}\n    .d-crumb{margin-bottom:10px}\n    .d-tag{margin-bottom:10px}\n    .d-hero h1{font-size:clamp(1.65rem,7.5vw,2.2rem);margin-bottom:10px}\n  }\n"
if anchor not in text:
    raise SystemExit('Dispatch hero CSS anchor not found')
text = text.replace(anchor, mobile, 1)
article.write_text(text, encoding='utf-8')

# 4) Codify the Dispatch rule in the governing brand doc.
brand = ROOT / 'BRAND.md'
btext = brand.read_text(encoding='utf-8')
marker = '### Dispatch mobile hero standard'
if marker not in btext:
    btext += "\n\n### Dispatch mobile hero standard\n\nOn mobile, Vegas Dispatch article heroes should not consume a full screen before the reader reaches the story. Cap editorial hero height at roughly 360–430px depending on viewport, keep the headline and byline visible over the image, and use `object-fit: cover` / deliberate `object-position` cropping. Desktop can retain the larger cinematic treatment.\n"
    brand.write_text(btext, encoding='utf-8')

# Validation
c = cirque.read_text(encoding='utf-8')
assert "slug:'mad-apple'" not in c
assert '"numberOfItems": 4,' in c
assert 'Mad Apple. Compare every Cirque' not in c
p = product.read_text(encoding='utf-8')
assert 'height:clamp(260px,62vw,390px)' in p
a = article.read_text(encoding='utf-8')
assert 'height:clamp(360px,104vw,430px)' in a

# Parse JSON-LD blocks on the category and article/product pages.
for path in [cirque, product, article]:
    t = path.read_text(encoding='utf-8')
    for block in re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', t, re.S):
        json.loads(block)

print('Mad Apple category/mobile hero fixes validated')

# one-time trigger
