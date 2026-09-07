#!/usr/bin/env python3
"""Compatibility wrapper for the generic show-data sync engine.

Prefer:
    python3 scripts/sync-show-from-data.py carrot-top
"""

import runpy
import sys
from pathlib import Path

ENGINE = Path(__file__).with_name("sync-show-from-data.py")
sys.argv = [str(ENGINE), "carrot-top", *sys.argv[1:]]
runpy.run_path(str(ENGINE), run_name="__main__")
