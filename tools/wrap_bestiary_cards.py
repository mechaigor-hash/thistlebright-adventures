#!/usr/bin/env python3
"""Wrap bestiary creature entries into side-art cards for A4 print."""
from pathlib import Path
import re

CREATURE_IMG_RE = r'../art/generated/(?:0[7-9]|1[0-6])-creature-[^" ]+\.png'
pattern = re.compile(
    rf'(<h2>[^<]+</h2>\s*)'
    rf'(<figure class="art-plate"><img src="{CREATURE_IMG_RE}" alt="[^"]+"></figure>\s*)'
    rf'(<ul>.*?</ul>\s*)'
    rf'(<h3>Three gentle solutions</h3>\s*<ul>.*?</ul>)',
    re.S,
)
for p in Path('/home/mecha-igor/prepped/scottish-fairy-quest/printable-a4').glob('*-a4.html'):
    text = p.read_text(encoding='utf-8')
    if '<section class="creature-card"' in text:
        print(p.name, 'already wrapped')
        continue
    text2, n = pattern.subn(r'<section class="creature-card">\n\1\2\3\4\n</section>', text)
    if n:
        p.write_text(text2, encoding='utf-8')
    print(p.name, 'creature_cards', n)
