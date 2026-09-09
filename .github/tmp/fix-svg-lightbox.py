from pathlib import Path

charts = {
    Path('images/carrot-top-atrium-showroom-seating-chart.svg'): ('700', '790'),
    Path('images/sphere-las-vegas-seating-chart.svg'): ('620', '780'),
}

for path, (width, height) in charts.items():
    text = path.read_text(encoding='utf-8')
    first_end = text.find('>')
    if first_end < 0:
        raise SystemExit(f'Invalid SVG: {path}')
    root = text[:first_end]
    if ' width=' not in root:
        root = root.replace('<svg xmlns="http://www.w3.org/2000/svg"', f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"', 1)
        text = root + text[first_end:]
        path.write_text(text, encoding='utf-8')

css_path = Path('assets/show-canonical.css')
css = css_path.read_text(encoding='utf-8')
marker = '/* Seating-chart SVG lightbox fallback */'
rule = '''\n\n/* Seating-chart SVG lightbox fallback */\n.lightbox img[src*=".svg"]{width:min(760px,92vw);height:min(82vh,900px);object-fit:contain}\n@media(max-width:800px){.lightbox img[src*=".svg"]{width:92vw;height:min(72vh,760px);object-fit:contain}}\n'''
if marker not in css:
    css_path.write_text(css.rstrip() + rule, encoding='utf-8')

# Regression assertions.
for path, (width, height) in charts.items():
    root = path.read_text(encoding='utf-8').split('>', 1)[0]
    assert f'width="{width}"' in root, path
    assert f'height="{height}"' in root, path
css = css_path.read_text(encoding='utf-8')
assert marker in css
assert '.lightbox img[src*=".svg"]' in css
print('SVG lightbox regression repair passed')
