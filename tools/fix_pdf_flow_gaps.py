#!/usr/bin/env python3
"""Improve PDF flow: remove white gaps and prevent ugly text/list page splits."""
from __future__ import annotations
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PRINT_DIR = ROOT / "printable-a4"
fix_script = ROOT / "tools" / "fix_pdf_cutoffs.py"

# Patch the reusable CSS generator, then run it.
text = fix_script.read_text(encoding="utf-8")
ordered = [
    (
        "p, li { orphans:3; widows:3; } p { margin:0 0 2.6mm; } ul, ol { margin-top:1.2mm; margin-bottom:3mm; padding-left:5.2mm; } li { margin:.45mm 0; }",
        "p, li { orphans:3; widows:3; } p { margin:0 0 2.6mm; } ul, ol { margin-top:1.2mm; margin-bottom:3mm; padding-left:5.2mm; break-inside:avoid-page; page-break-inside:avoid; } li { margin:.45mm 0; break-inside:avoid; } .keep-block { break-inside:avoid-page; page-break-inside:avoid; margin:0 0 3mm; } .keep-block > :last-child { margin-bottom:0; }",
    ),
    (
        "h2 { clear:both; margin:7mm 0 3.6mm; color:var(--green); font-size:17pt; border-top:1.2pt dashed rgba(184,138,45,.72); padding-top:4mm; }",
        "h2 { clear:both; margin:7mm 0 3.6mm; color:var(--green); font-size:17pt; border-top:1.2pt dashed rgba(184,138,45,.72); padding-top:4mm; break-after:avoid-page; page-break-after:avoid; }",
    ),
    (
        "h3 { clear:both; margin:5mm 0 2mm; color:var(--red); font-size:13pt; border-bottom:1px solid rgba(184,138,45,.6); }",
        "h3 { clear:both; margin:5mm 0 2mm; color:var(--red); font-size:13pt; border-bottom:1px solid rgba(184,138,45,.6); break-after:avoid-page; page-break-after:avoid; }",
    ),
    ("width:calc(100% + 16mm); min-height:184mm; margin:3mm -8mm 4mm;", "width:calc(100% + 16mm); min-height:180mm; margin:3mm -8mm 4mm;"),
    ("height:184mm; max-height:none;", "height:180mm; max-height:none;"),
    (
        "figure.art-plate.title-art, figure.art-plate.title-art img { min-height:154mm; height:154mm; }\nfigure.art-plate.tall, figure.art-plate.tall img { min-height:190mm; height:190mm; }",
        "figure.art-plate.title-art, figure.art-plate.title-art img { min-height:136mm; height:136mm; }\nfigure.art-plate.tall, figure.art-plate.tall img { min-height:148mm; height:148mm; }",
    ),
    ("width:calc(100% + 16mm); min-height:999mm; margin:3mm -8mm 4mm;", "width:calc(100% + 16mm); min-height:999mm; margin:3mm -8mm 4mm;"),
    ("min-height:999mm; height:999mm;", "min-height:999mm; height:999mm;"),
    ("height:999mm; max-height:none;", "height:999mm; max-height:none;"),
]
for old, new in ordered:
    if old not in text:
        print(f"warn: pattern not found in fix script: {old[:70]}")
    text = text.replace(old, new)
fix_script.write_text(text, encoding="utf-8")
subprocess.run(["python3", str(fix_script)], cwd=ROOT, check=True)

# Wrap short text groups so lists move together at page breaks.
def unwrap_existing(html: str) -> str:
    return re.sub(r'<div class="keep-block">\s*(.*?)\s*</div>', r'\1', html, flags=re.S)

def wrap_keep_blocks(html: str) -> str:
    html = unwrap_existing(html)
    html = re.sub(
        r'(<p>(?:(?!</p>).{1,220}?</p>)\s*(?:<ul>.*?</ul>|<ol>.*?</ol>))',
        r'<div class="keep-block">\1</div>',
        html,
        flags=re.S,
    )
    html = re.sub(
        r'(<h3>(?:(?!</h3>).{1,120}?</h3>)\s*(?:<ul>.*?</ul>|<ol>.*?</ol>))',
        r'<div class="keep-block">\1</div>',
        html,
        flags=re.S,
    )
    return html

for path in sorted(PRINT_DIR.glob("*-a4.html")):
    html = wrap_keep_blocks(path.read_text(encoding="utf-8"))
    path.write_text(html, encoding="utf-8")
    keep_blocks = html.count('class="keep-block"')
    print(f"flow-wrapped {path.name}: keep_blocks={keep_blocks}")
