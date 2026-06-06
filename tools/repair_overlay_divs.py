#!/usr/bin/env python3
"""Repair missing closing overlay divs after grouping feature/scene copy."""
from pathlib import Path
import re

PRINT_DIR = Path('/home/mecha-igor/prepped/scottish-fairy-quest/printable-a4')
SECTION_RE = re.compile(r'(<section class="(?:scene-plate|profile-card[^\"]*|class-card[^\"]*|creature-card[^\"]*)">)(.*?)(</section>)', re.S)

def balance_divs(body: str) -> str:
    opens = len(re.findall(r'<div\b', body))
    closes = body.count('</div>')
    if opens > closes:
        body = body.rstrip() + ('\n</div>' * (opens - closes)) + '\n'
    return body

for path in sorted(PRINT_DIR.glob('*-a4.html')):
    text = path.read_text(encoding='utf-8')
    text2 = SECTION_RE.sub(lambda m: m.group(1) + balance_divs(m.group(2)) + m.group(3), text)
    path.write_text(text2, encoding='utf-8')
    print(path.name, 'div_balance', text2.count('<div'), text2.count('</div>'))
