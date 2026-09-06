from pathlib import Path
import re

ROOT = Path('.')
TEXT_EXTS = {'.html','.js','.json','.md','.xml'}
changed=[]

for path in ROOT.rglob('*'):
    if not path.is_file() or path.suffix.lower() not in TEXT_EXTS or '.git' in path.parts:
        continue
    try:
        text=path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue
    old=text

    # Single-line catalog objects for Mystere.
    def fix_obj(m):
        s=m.group(0)
        s=re.sub(r'price\s*:\s*68\b','price:84',s)
        s=s.replace("pd:'$68'","pd:'$84'").replace('pd:"$68"','pd:"$84"')
        return s
    text=re.sub(r"\{[^{}\n]{0,1600}slug\s*:\s*['\"]mystere['\"][^{}\n]{0,1600}\}",fix_obj,text)

    # Links/cards that specifically point at the Mystere page.
    def fix_anchor(m):
        s=m.group(0)
        s=s.replace('$68','$84').replace('from 68','from 84')
        s=re.sub(r'data-price=["\']68["\']','data-price="84"',s)
        return s
    text=re.sub(r'<a\b[^>]*href=["\']/shows/cirque/mystere/["\'][\s\S]{0,2500}?</a>',fix_anchor,text,flags=re.I)

    # Common structured-data/list snippets where name and price live together.
    def fix_named_window(m):
        s=m.group(0)
        return s.replace('$68','$84').replace('"price":"68"','"price":"84"').replace('"price":68','"price":84')
    text=re.sub(r'(?is)(?:Mystère|Mystere)[\s\S]{0,500}(?:\$68|"price"\s*:\s*"?68"?)',fix_named_window,text)

    if text != old:
        path.write_text(text,encoding='utf-8')
        changed.append(str(path))

print('Updated files:')
for p in changed:
    print(' -',p)

# Validation: no obvious stale $68 references remain near Mystere identifiers.
problems=[]
for path in ROOT.rglob('*'):
    if not path.is_file() or path.suffix.lower() not in TEXT_EXTS or '.git' in path.parts:
        continue
    try:
        text=path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue
    for m in re.finditer(r'(?is)(?:Mystère|Mystere|mystere)[\s\S]{0,350}\$68|\$68[\s\S]{0,350}(?:Mystère|Mystere|mystere)',text):
        problems.append((str(path),m.group(0)[:220].replace('\n',' ')))
        break
if problems:
    print('\nRemaining possible stale Mystere $68 references:')
    for p,s in problems:
        print(' -',p,':',s)
    raise SystemExit(2)
