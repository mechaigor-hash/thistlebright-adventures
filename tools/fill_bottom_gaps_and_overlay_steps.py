#!/usr/bin/env python3
"""Apply final full-bleed image-page cleanup.

Assumes tools/fix_pdf_cutoffs.py already contains the final CSS. This reapplies
that CSS to every printable HTML file and idempotently moves Step 1/2 headings
into the image overlay panels instead of leaving them as separate sections.
"""
from __future__ import annotations
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PRINT_DIR = ROOT / "printable-a4"

subprocess.run(["python3", str(ROOT / "tools" / "fix_pdf_cutoffs.py")], cwd=ROOT, check=True)

step_re = re.compile(
    r'\s*<hr>\s*<h3>(Step [12]: .*?)</h3>\s*'
    r'<section class="scene-plate scene-full">\s*'
    r'(<figure class="art-plate"><img src="\.\./art/generated/(?:23-player-races-kindreds|24-player-classes-paths)\.png".*?</figure>)\s*'
    r'<div class="scene-copy">',
    re.S,
)
for path in sorted(PRINT_DIR.glob("*-a4.html")):
    html = path.read_text(encoding="utf-8")
    html = step_re.sub(
        lambda m: f'\n<section class="scene-plate scene-full step-overlay">\n{m.group(2)}\n<div class="scene-copy"><h3>{m.group(1)}</h3>',
        html,
    )
    path.write_text(html, encoding="utf-8")
    print(f"{path.name}: step-overlay={html.count('step-overlay')}")
