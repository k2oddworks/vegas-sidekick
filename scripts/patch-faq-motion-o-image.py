from pathlib import Path
import re

# Mystere: repair O related-card image and match Carrot Top FAQ icon motion.
mystere = Path('shows/cirque/mystere/index.html')
s = mystere.read_text(encoding='utf-8')
s = s.replace('/images/o-hero.jpg', '/images/o-hero.webp')

# Add the Carrot Top-style rotation transition to FAQ icon if not already present.
s = re.sub(
    r"(\.faq summary::before\{[^}]*)(\})",
    lambda m: (m.group(1) if 'transition:' in m.group(1) else m.group(1) + ';transition:transform .2s,background .2s') + m.group(2),
    s,
    count=1,
)
s = re.sub(
    r"\.faq details\[open\] summary::before\{content:'−'(?P<rest>[^}]*)\}",
    lambda m: ".faq details[open] summary::before{content:'−';transform:rotate(180deg)" + m.group('rest') + "}",
    s,
    count=1,
)
mystere.write_text(s, encoding='utf-8')

# VEGAS! The Show: match Carrot Top FAQ icon motion.
vegas = Path('shows/music/vegas-the-show/index.html')
s = vegas.read_text(encoding='utf-8')
s = re.sub(
    r"(\.faq summary::before\{[^}]*)(\})",
    lambda m: (m.group(1) if 'transition:' in m.group(1) else m.group(1) + ';transition:transform .2s,background .2s') + m.group(2),
    s,
    count=1,
)
s = re.sub(
    r"\.faq details\[open\] summary::before\{content:'−'(?P<rest>[^}]*)\}",
    lambda m: ".faq details[open] summary::before{content:'−';transform:rotate(180deg)" + m.group('rest') + "}",
    s,
    count=1,
)
vegas.write_text(s, encoding='utf-8')

print('Patched O image and FAQ icon motion on Mystere + VEGAS! The Show')
