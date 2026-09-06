from pathlib import Path

OVERRIDE = """
/* Match Carrot Top FAQ icon motion */
.faq summary::before{transition:transform .2s,background .2s!important}
.faq details[open] summary::before{transform:rotate(180deg)}
"""

def patch(path_str, fix_o=False):
    path = Path(path_str)
    s = path.read_text(encoding='utf-8')
    if fix_o:
        s = s.replace('/images/o-hero.jpg', '/images/o-show-2.jpg')
        s = s.replace('/images/o-hero.webp', '/images/o-show-2.jpg')
    if 'Match Carrot Top FAQ icon motion' not in s:
        marker = '</style>'
        if marker not in s:
            raise SystemExit(f'No </style> in {path_str}')
        s = s.replace(marker, OVERRIDE + '\n' + marker, 1)
    path.write_text(s, encoding='utf-8')

patch('shows/cirque/mystere/index.html', fix_o=True)
patch('shows/music/vegas-the-show/index.html')
print('Patched O image and FAQ icon motion on Mystere + VEGAS! The Show')
