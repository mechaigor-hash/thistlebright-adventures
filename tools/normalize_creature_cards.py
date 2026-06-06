#!/usr/bin/env python3
"""Move creature-card art out of the text overlay so it renders as background art.

Some bestiary cards had <figure> inside <div class="feature-copy">. The current
full-page CSS expects the figure to be a direct child of .creature-card; otherwise
WeasyPrint can render the card as a dark block with the text panel off-page.
"""
from __future__ import annotations
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PRINT_DIR = ROOT / "printable-a4"

SECTION_RE = re.compile(r'(<section class="creature-card[^"]*">)(.*?)(</section>)', re.S)
FIG_RE = re.compile(r'\s*(<figure class="art-plate"><img src="[^"]+" alt="[^"]+"></figure>)\s*', re.S)

def fix_section(m: re.Match) -> str:
    open_tag, body, close_tag = m.groups()
    # Already normalized: figure before feature-copy.
    if re.match(r'\s*<figure class="art-plate">', body):
        return m.group(0)
    div_start = body.find('<div class="feature-copy">')
    if div_start < 0:
        return m.group(0)
    fig_m = FIG_RE.search(body)
    if not fig_m:
        return m.group(0)
    fig = fig_m.group(1)
    body_without_fig = body[:fig_m.start()] + '\n' + body[fig_m.end():]
    return f'{open_tag}\n{fig}\n{body_without_fig.strip()}\n{close_tag}'

for path in sorted(PRINT_DIR.glob('*-a4.html')):
    text = path.read_text(encoding='utf-8')
    new, count = SECTION_RE.subn(fix_section, text)
    path.write_text(new, encoding='utf-8')
    cards = new.count('<section class="creature-card')
    direct = len(re.findall(r'<section class="creature-card[^>]*>\s*<figure class="art-plate">', new, re.S))
    print(f'{path.name}: creature_cards={cards}, direct_figures={direct}, sections_seen={count}')
