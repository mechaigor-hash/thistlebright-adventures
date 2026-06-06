#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from weasyprint import HTML
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PRINT = ROOT / 'printable-a4'
PDF = ROOT / 'pdf'
PDF.mkdir(exist_ok=True)
order = ['player-handbook','bestiary','dungeon-master-guide','example-campaigns','combined-book']
for name in order:
    src = PRINT / f'{name}-a4.html'
    out = PDF / f'{name}.pdf'
    print(f'Generating {out.name}')
    HTML(filename=str(src), base_url=str(PRINT)).write_pdf(str(out))
    info = subprocess.check_output(['pdfinfo', str(out)], text=True, errors='ignore')
    pages = next((line.split(':',1)[1].strip() for line in info.splitlines() if line.startswith('Pages:')), '?')
    size = next((line.split(':',1)[1].strip() for line in info.splitlines() if line.startswith('Page size:')), '?')
    print(f'{out.name}: pages={pages} size={size} bytes={out.stat().st_size}')
