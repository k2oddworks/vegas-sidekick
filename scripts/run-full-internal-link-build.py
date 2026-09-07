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
