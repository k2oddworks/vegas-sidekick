from pathlib import Path

paths = [
    Path('news/activate-town-square-opens-october-3/index.html'),
    Path('news/index.html'),
]
for p in paths:
    s = p.read_text(encoding='utf-8')
    s = s.replace('/images/kris-kidd-avatar.jpg', '/images/kris-kidd.webp')
    p.write_text(s, encoding='utf-8')

print('Switched author avatar to existing production Kris image.')
