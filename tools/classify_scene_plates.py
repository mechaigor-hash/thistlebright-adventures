#!/usr/bin/env python3
"""Classify scene plates so only scene-before-feature pages become full-page art."""
from __future__ import annotations
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PRINT_DIR = ROOT / "printable-a4"
SCENE_RE = re.compile(r'<section class="scene-plate">\s*<figure class="art-plate"><img src="[^"]+" alt="[^"]+"></figure>\s*<div class="scene-copy">.*?</div>\s*</section>', re.S)
FEATURE_NEXT_RE = re.compile(r'^\s*<section class="(?:profile-card|class-card|creature-card)')

def classify(html: str):
    html = html.replace('class="scene-plate scene-full"', 'class="scene-plate"')
    matches = list(SCENE_RE.finditer(html))
    pieces = []
    last = 0
    full_count = 0
    for m in matches:
        pieces.append(html[last:m.start()])
        block = m.group(0)
        tail = html[m.end():]
        if FEATURE_NEXT_RE.match(tail):
            block = block.replace('class="scene-plate"', 'class="scene-plate scene-full"', 1)
            full_count += 1
        pieces.append(block)
        last = m.end()
    pieces.append(html[last:])
    return ''.join(pieces), full_count, len(matches)

for path in sorted(PRINT_DIR.glob('*-a4.html')):
    html, full_count, total = classify(path.read_text(encoding='utf-8'))
    path.write_text(html, encoding='utf-8')
    print(f'{path.name}: scene_full={full_count}, scene_total={total}')
