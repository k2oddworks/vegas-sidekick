from pathlib import Path
p=Path('guides/best-cheap-vegas-shows/index.html'); s=p.read_text(encoding='utf-8')
s=s.replace('</div></div></div></section><section id="compare">','</div></div></section><section id="compare">',1)
assert s.count('id="cheap-guide-photo-upgrade"')==1
assert s.count('class="g-shot"')==3
assert s.count('class="qa-photo"')==3
assert '<div class="g-hero-grid">' in s
assert '</div></div></div></section><section id="compare">' not in s
p.write_text(s,encoding='utf-8'); print('Cheap Shows photo rebuild validated')
