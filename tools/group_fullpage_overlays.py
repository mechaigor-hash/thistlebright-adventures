#!/usr/bin/env python3
"""Fix full-page A4 overlays.

Problems fixed:
- race/class text boxes were independently positioned and could overlap
- all feature text was on the left
- some art still appeared as smaller boxes

This groups all race/class copy into one overlay panel per page, assigns an
alternating panel position, and makes scene/standalone art plates page-scale.
"""
from __future__ import annotations
from pathlib import Path
from html.parser import HTMLParser
import re

PRINT_DIR = Path('/home/mecha-igor/prepped/scottish-fairy-quest/printable-a4')
STYLE_RE = re.compile(r'<style>.*?</style>', re.S)

CSS = r'''
@page { size: A4 portrait; margin: 12mm 11mm 14mm; }
* { box-sizing: border-box; }
:root {
  --ink:#2a2118; --muted:#5d5144; --green:#285e3d; --purple:#4b2e67;
  --red:#8b352d; --gold:#b88a2d; --line:#c8ae78; --paper:#fbf2dc; --paper2:#fffaf0;
}
html { background:#d8c59a; }
body { margin:0 auto; max-width:210mm; color:var(--ink); font-family:"DejaVu Serif", Georgia, "Times New Roman", serif; font-size:10.6pt; line-height:1.34; background:var(--paper2); }
main.book { min-height:100vh; padding:0 3mm 6mm; }
p, li { orphans:3; widows:3; } p { margin:0 0 3.2mm; } ul, ol { margin-top:1.5mm; margin-bottom:3.8mm; padding-left:6mm; } li { margin:.7mm 0; }
strong { color:#251b13; } h1, h2, h3, h4 { text-wrap:balance; break-after:avoid; }
h1 { page-break-before:always; min-height:74mm; margin:0 -3mm 8mm; padding:17mm 16mm 10mm; color:#fff8e8; font-size:25pt; letter-spacing:.02em; line-height:1.06; background:linear-gradient(90deg, rgba(23,35,26,.82), rgba(46,35,65,.62)), url("../art/generated/22-book-title-spread.png") center/cover no-repeat; border-bottom:2.2mm solid #6f4b1f; box-shadow: inset 0 -18mm 26mm rgba(0,0,0,.27); text-shadow:0 2px 4px rgba(0,0,0,.45); }
h1:first-child { page-break-before:auto; }
h2 { clear:both; margin:8mm 0 4.5mm; color:var(--green); font-size:18pt; border-top:1.4pt dashed rgba(184,138,45,.72); padding-top:5mm; }
h2::first-letter { font-size:1.28em; color:var(--red); }
h3 { clear:both; margin:6mm 0 2.4mm; color:var(--red); font-size:14pt; border-bottom:1px solid rgba(184,138,45,.6); }
h4 { margin:0 0 1.6mm; color:var(--purple); font-size:12.8pt; letter-spacing:.015em; }
hr { clear:both; border:0; height:4mm; margin:7mm 0; background:radial-gradient(circle, rgba(139,53,45,.95) 1.1mm, transparent 1.2mm) center/7mm 4mm repeat-x; opacity:.6; }
blockquote, table { break-inside:avoid; page-break-inside:avoid; }
blockquote { clear:both; margin:5mm 0; padding:4mm 5mm 4mm 7mm; border:1px solid rgba(139,53,45,.38); border-left:4mm solid rgba(139,53,45,.72); background:linear-gradient(90deg, rgba(255,244,217,.96), rgba(250,236,199,.72)); border-radius:1.5mm 5mm 5mm 1.5mm; box-shadow:0 1mm 3mm rgba(79,50,18,.12); }
table { width:100%; border-collapse:collapse; margin:4mm 0 5mm; font-size:9.4pt; box-shadow:0 .8mm 2.6mm rgba(75,45,17,.12); }
th,td { border:1px solid #c9b88b; padding:3px 5px; vertical-align:top; } th { background:#d9e6c0; color:#243e28; } tr:nth-child(even) td { background:rgba(224,235,202,.62); }
img { max-width:100%; height:auto; }

/* Any non-feature artwork is now page-scale rather than a small strip/card. */
figure.art-plate {
  clear:both; position:relative; min-height:252mm; margin:0 0 10mm; padding:2mm;
  break-inside:avoid; page-break-inside:avoid; page-break-before:always; page-break-after:always;
  border:1.4mm solid #302315; border-radius:5mm; background:#2e2418; box-shadow:0 2.5mm 8mm rgba(68,38,15,.26); overflow:hidden;
}
figure.art-plate::before { content:""; position:absolute; inset:3mm; border:1px solid rgba(255,238,177,.72); border-radius:3.2mm; pointer-events:none; z-index:2; }
figure.art-plate img { display:block; width:100%; height:248mm; max-height:none; object-fit:contain; object-position:center; border-radius:3mm; background:radial-gradient(circle, rgba(255,248,224,.95), rgba(222,197,145,.76) 55%, rgba(48,35,21,.96)); }

/* Scene plates: full-page image with one grouped overlay, no tiny art boxes. */
.scene-plate { position:relative; clear:both; min-height:258mm; margin:0 0 10mm; padding:0; border:1.5mm solid #2e2418; border-radius:5mm; overflow:hidden; box-shadow:0 2.5mm 8mm rgba(68,38,15,.26); break-inside:avoid; page-break-inside:avoid; page-break-before:always; page-break-after:always; background:#2e2418; }
.scene-plate figure.art-plate { position:absolute; inset:0; min-height:auto; margin:0; padding:0; border:0; border-radius:0; box-shadow:none; background:transparent; page-break-before:auto; page-break-after:auto; }
.scene-plate figure.art-plate::before { display:none; }
.scene-plate figure.art-plate img { width:100%; height:100%; max-height:none; object-fit:contain; object-position:center; border-radius:0; opacity:.98; background:radial-gradient(circle, rgba(255,248,224,.95), rgba(222,197,145,.76) 55%, rgba(48,35,21,.96)); }
.scene-plate::after, .profile-card::after, .class-card::after, .creature-card::after { content:""; position:absolute; inset:3mm; z-index:4; border:1px solid rgba(255,238,177,.72); border-radius:3.2mm; pointer-events:none; }
.scene-copy { position:absolute; z-index:3; left:50%; transform:translateX(-50%); bottom:9mm; width:126mm; padding:3.5mm 4.5mm; background:linear-gradient(180deg, rgba(255,250,238,.92), rgba(250,235,199,.82)); border:1px solid rgba(91,57,22,.55); border-radius:3mm; box-shadow:0 1.2mm 6mm rgba(0,0,0,.25); }
.scene-copy p:last-child, .scene-copy ul:last-child, .scene-copy ol:last-child { margin-bottom:0; }

/* Full-page feature plates with ONE overlay group, alternating position. */
.profile-card, .class-card, .creature-card { position:relative; clear:both; min-height:258mm; margin:0 0 10mm; padding:0; border:1.5mm solid #302315; border-radius:5mm; overflow:hidden; box-shadow:0 2.5mm 8mm rgba(68,38,15,.28); break-inside:avoid; page-break-inside:avoid; page-break-before:always; page-break-after:always; background:radial-gradient(circle at 50% 42%, rgba(255,248,224,.95), rgba(222,197,145,.76) 55%, rgba(48,35,21,.96) 100%); }
.profile-card > img, .class-card > img, .creature-card figure.art-plate { position:absolute; inset:0; z-index:0; width:100%; height:100%; max-width:none; max-height:none; margin:0; padding:0; border:0; border-radius:0; box-shadow:none; page-break-before:auto; page-break-after:auto; background:transparent; }
.profile-card > img, .class-card > img, .creature-card figure.art-plate img { width:100%; height:100%; max-height:none; object-fit:contain; object-position:center; padding:5mm; opacity:.98; filter:saturate(1.02) contrast(.98); background:radial-gradient(circle, rgba(255,248,224,.95), rgba(222,197,145,.76) 55%, rgba(48,35,21,.96)); }
.profile-card::before, .class-card::before, .creature-card::before { content:""; position:absolute; inset:0; z-index:1; background:radial-gradient(ellipse at 50% 38%, rgba(255,255,255,0) 0%, rgba(255,255,255,0) 46%, rgba(255,248,226,.32) 76%, rgba(42,29,16,.32) 100%); pointer-events:none; }
.feature-copy { position:absolute; z-index:3; top:12mm; width:82mm; max-height:232mm; overflow:hidden; padding:4mm 5mm; background:linear-gradient(180deg, rgba(255,250,238,.93), rgba(250,235,199,.82)); border:1px solid rgba(91,57,22,.50); border-radius:3.2mm; box-shadow:0 1.5mm 7mm rgba(0,0,0,.24); }
.copy-left .feature-copy { left:8mm; }
.copy-right .feature-copy { right:8mm; }
.copy-bottom .feature-copy { left:50%; right:auto; top:auto; bottom:9mm; transform:translateX(-50%); width:126mm; max-height:84mm; }
.feature-copy h2, .feature-copy h3, .feature-copy h4 { clear:none; margin:0 0 2mm; padding:0 0 1.5mm; color:#76342c; font-size:21pt; line-height:1.04; font-variant:small-caps; letter-spacing:.025em; border:0; border-bottom:1px solid rgba(116,52,45,.40); background:none; }
.feature-copy p { position:static; width:auto; margin:0 0 3mm; padding:0; font-size:11.5pt; background:none; border:0; box-shadow:none; }
.feature-copy ul { position:static; width:auto; margin:0 0 3mm; padding-left:5.5mm; font-size:10.8pt; background:none; border:0; box-shadow:none; }
.feature-copy li { margin:.7mm 0; }
.spell-block { position:static; width:auto; margin:3mm 0 0; padding:3mm 4mm; border:1px solid rgba(75,46,103,.48); border-radius:3mm; background:linear-gradient(180deg, rgba(246,238,255,.92), rgba(255,249,232,.78)); break-inside:avoid; page-break-inside:avoid; box-shadow:0 1.2mm 5mm rgba(0,0,0,.13); font-size:10.2pt; }
.spell-block .spell-title { margin:0 0 1.5mm; color:#4b2e67; font-weight:700; font-variant:small-caps; letter-spacing:.03em; }
.spell-block ul { margin:0; padding-left:5mm; font-size:10.2pt; }
.pagebreak { clear:both; page-break-after:always; }
@media screen { body { box-shadow:0 0 16mm rgba(58,38,12,.22); } }
@media print { html, body { background:white; } main.book { padding:0; } a { color:inherit; text-decoration:none; } figure.art-plate, .scene-plate, .profile-card, .class-card, .creature-card, blockquote, table { break-inside:avoid-page; page-break-inside:avoid; } }
'''

NOTE = '<blockquote class="layout-note"><strong>Print note:</strong> Artwork now uses full-page feature plates. Text is grouped into one overlay panel per plate and alternates left/right/bottom to avoid covering the same part of every image.</blockquote>'

SECTION_RE = re.compile(r'<section class="(profile-card race-card|class-card|creature-card)(?: copy-(?:left|right|bottom))?">(.*?)</section>', re.S)

def wrap_feature_copy(html: str) -> str:
    # Idempotently unwrap any previous feature-copy wrapper inside the section body.
    html = html.replace('<div class="feature-copy">', '').replace('</div>\n</section>', '</section>')
    positions = ['copy-left', 'copy-right', 'copy-bottom', 'copy-right', 'copy-left', 'copy-bottom']
    counter = {'n': 0}

    def repl(m: re.Match) -> str:
        cls, body = m.group(1), m.group(2)
        pos = positions[counter['n'] % len(positions)]
        counter['n'] += 1
        if cls == 'creature-card':
            pos = positions[(counter['n'] + 1) % len(positions)]
        # Preserve the leading image/figure as the background layer; everything else becomes one overlay.
        img = ''
        rest = body
        img_m = re.match(r'\s*(<img [^>]+>|<figure class="art-plate">.*?</figure>)\s*(.*)', body, re.S)
        if img_m:
            img, rest = img_m.group(1), img_m.group(2)
        return f'<section class="{cls} {pos}">\n{img}\n<div class="feature-copy">\n{rest.strip()}\n</div>\n</section>'

    return SECTION_RE.sub(repl, html)

for path in sorted(PRINT_DIR.glob('*-a4.html')):
    text = path.read_text(encoding='utf-8')
    text = STYLE_RE.sub('<style>\n' + CSS + '\n</style>', text, count=1)
    text = re.sub(r'<blockquote class="layout-note">.*?</blockquote>', NOTE, text, count=1, flags=re.S)
    text = wrap_feature_copy(text)
    path.write_text(text, encoding='utf-8')
    print(path.name, 'feature_copy', text.count('feature-copy'), 'left', text.count('copy-left'), 'right', text.count('copy-right'), 'bottom', text.count('copy-bottom'))
