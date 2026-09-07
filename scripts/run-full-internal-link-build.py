#!/usr/bin/env python3
"""Run the curated link build, skipping relationships whose source/target page is not present."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = spec_from_file_location("vs_link_build", ROOT / "scripts/full-internal-link-build.py")
mod = module_from_spec(spec)
spec.loader.exec_module(mod)

for source, target in list(mod.SHOW_RELATED.items()):
    if not (ROOT / source).exists() or not (ROOT / target).exists():
        print(f"SKIP unavailable relationship: {source} -> {target}")
        mod.SHOW_RELATED.pop(source)

mod.main()

# Final graph gap: give the Tribute guide a natural inbound route from the
# budget guide. Keep this idempotent so scheduled/repeat runs are safe.
cheap = ROOT / "guides/best-cheap-vegas-shows/index.html"
text = cheap.read_text(encoding="utf-8")
tribute = "/guides/best-tribute-shows/"
if tribute not in text:
    marker = '</div></div></section>\n<div id="vs-footer"></div>'
    card = ('<a href="/guides/best-tribute-shows/" style="display:block;padding:16px 18px;border:1px solid #ece9f6;border-radius:14px;text-decoration:none;color:inherit;background:#fff">'
            '<strong style="display:block;margin-bottom:4px">Want tribute shows specifically? →</strong>'
            '<span style="color:#6c6883;font-size:.92rem">Compare the current Vegas tribute lineup.</span></a>')
    if marker in text:
        text = text.replace(marker, card + marker, 1)
        cheap.write_text(text, encoding="utf-8")
        print("Added Best Tribute Shows inbound link from Best Cheap Vegas Shows")
    else:
        print("WARN could not locate Cheap Shows related-guide rail")
