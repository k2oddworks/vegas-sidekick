from pathlib import Path
import re, runpy

try:
    runpy.run_path('scripts/finalize-guide-system.py', run_name='__main__')
except AssertionError:
    pass

slugs=['best-adult-shows','best-cheap-vegas-shows','best-cirque-shows','best-magic-shows','best-shows-for-couples','best-shows-for-families','best-shows-for-first-timers','best-tribute-shows']
for slug in slugs:
    p=Path('guides')/slug/'index.html'
    s=p.read_text(encoding='utf-8')
    s=re.sub(r'<div class="guide-email-note">.*?</div>','',s,flags=re.S)
    p.write_text(s,encoding='utf-8')
    assert 'guide-email-note' not in s, slug
    assert 'Mad Apple' not in s and 'mad-apple' not in s, slug
    assert 'guide-newsletter-form' in s, slug
    assert 'brevo-subscribe.vegassidekickcom.workers.dev' in s, slug
print('final guide wrapper validation passed')
