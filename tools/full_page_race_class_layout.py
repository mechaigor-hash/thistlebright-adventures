#!/usr/bin/env python3
"""Make race/class entries full-page A4 feature plates.

The user specifically wants the race and class images to be page-scale layered
artwork, not cropped into small cards. This script updates the printable CSS so
.profile-card and .class-card each occupy roughly a full A4 content page, keep the
entire portrait visible with object-fit: contain, and layer text panels over the
artwork.
"""
from __future__ import annotations
from pathlib import Path
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
body {
  margin:0 auto; max-width:210mm; color:var(--ink);
  font-family:"DejaVu Serif", Georgia, "Times New Roman", serif;
  font-size:10.6pt; line-height:1.34;
  background:
    radial-gradient(circle at 8% 2%, rgba(135,83,48,.11), transparent 34mm),
    radial-gradient(circle at 94% 16%, rgba(40,94,61,.09), transparent 42mm),
    linear-gradient(90deg, rgba(122,84,34,.06), transparent 12mm, transparent calc(100% - 12mm), rgba(122,84,34,.06)),
    var(--paper2);
}
main.book { min-height:100vh; padding:0 3mm 6mm; }
p, li { orphans:3; widows:3; }
p { margin:0 0 3.2mm; } ul, ol { margin-top:1.5mm; margin-bottom:3.8mm; padding-left:6mm; } li { margin:.7mm 0; }
strong { color:#251b13; }
h1, h2, h3, h4 { text-wrap:balance; break-after:avoid; }
h1 {
  page-break-before:always; min-height:74mm; margin:0 -3mm 8mm; padding:17mm 16mm 10mm;
  color:#fff8e8; font-size:25pt; letter-spacing:.02em; line-height:1.06;
  background:linear-gradient(90deg, rgba(23,35,26,.82), rgba(46,35,65,.62)), url("../art/generated/22-book-title-spread.png") center/cover no-repeat;
  border-bottom:2.2mm solid #6f4b1f; box-shadow: inset 0 -18mm 26mm rgba(0,0,0,.27); text-shadow:0 2px 4px rgba(0,0,0,.45);
}
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

figure.art-plate { clear:both; position:relative; margin:5mm 0 6mm; padding:1.8mm; break-inside:avoid; page-break-inside:avoid; border:1.2mm solid #322615; border-radius:4.5mm; background:#2e2418; box-shadow:0 2mm 6mm rgba(68,38,15,.22); overflow:hidden; }
figure.art-plate::before { content:""; position:absolute; inset:2.3mm; border:1px solid rgba(255,238,177,.7); border-radius:3mm; pointer-events:none; z-index:2; }
figure.art-plate img { display:block; width:100%; max-height:88mm; object-fit:cover; object-position:center; border-radius:2.7mm; break-inside:avoid; page-break-inside:avoid; }
figure.art-plate.title-art img { max-height:70mm; } figure.art-plate.tall img { max-height:112mm; object-fit:contain; background:#f7ecd2; }

.scene-plate {
  position:relative; clear:both; min-height:82mm; margin:5.5mm 0 7mm; padding:0;
  border:1.5mm solid #2e2418; border-radius:4.5mm; overflow:hidden;
  box-shadow:0 2mm 7mm rgba(68,38,15,.24); break-inside:avoid; page-break-inside:avoid;
  background:#2e2418;
}
.scene-plate figure.art-plate { position:absolute; inset:0; margin:0; padding:0; border:0; border-radius:0; box-shadow:none; background:transparent; }
.scene-plate figure.art-plate::before { inset:2.4mm; z-index:3; border-color:rgba(255,238,177,.74); }
.scene-plate figure.art-plate img { width:100%; height:100%; max-height:none; min-height:82mm; object-fit:cover; border-radius:0; opacity:.96; }
.scene-plate::after { content:""; position:absolute; inset:0; z-index:1; background:linear-gradient(180deg, rgba(0,0,0,.05), rgba(0,0,0,.04) 45%, rgba(38,25,10,.44)); pointer-events:none; }
.scene-copy {
  position:absolute; left:5mm; right:5mm; bottom:5mm; z-index:2; max-width:136mm; margin:0 auto; padding:3.5mm 4.5mm;
  background:linear-gradient(180deg, rgba(255,250,238,.91), rgba(250,235,199,.84));
  border:1px solid rgba(91,57,22,.55); border-radius:3mm; box-shadow:0 1mm 5mm rgba(0,0,0,.25); backdrop-filter: blur(1px);
}
.scene-copy p:last-child, .scene-copy ul:last-child, .scene-copy ol:last-child { margin-bottom:0; }

/* FULL PAGE race/class feature plates. These preserve the whole artwork. */
.profile-card, .class-card {
  position:relative; clear:both;
  min-height:258mm;
  margin:0 0 10mm;
  padding:0;
  border:1.5mm solid #302315; border-radius:5mm; overflow:hidden;
  box-shadow:0 2.5mm 8mm rgba(68,38,15,.28);
  break-inside:avoid; page-break-inside:avoid;
  page-break-before:always; page-break-after:always;
  background:
    radial-gradient(circle at 50% 42%, rgba(255,248,224,.95), rgba(222,197,145,.76) 55%, rgba(48,35,21,.96) 100%);
}
.profile-card > img, .class-card > img {
  position:absolute; inset:0; z-index:0;
  width:100%; height:100%; max-width:none; max-height:none;
  object-fit:contain; object-position:center;
  padding:6mm 5mm 34mm;
  opacity:.98;
  filter:saturate(1.02) contrast(.98);
}
.profile-card::before, .class-card::before {
  content:""; position:absolute; inset:0; z-index:1;
  background:
    radial-gradient(ellipse at 50% 39%, rgba(255,255,255,0) 0%, rgba(255,255,255,0) 44%, rgba(255,248,226,.42) 72%, rgba(42,29,16,.28) 100%),
    linear-gradient(180deg, rgba(34,24,13,.04) 0%, rgba(34,24,13,.00) 38%, rgba(34,24,13,.38) 100%);
  pointer-events:none;
}
.profile-card::after, .class-card::after {
  content:""; position:absolute; inset:3mm; z-index:4;
  border:1px solid rgba(255,238,177,.72); border-radius:3.2mm; pointer-events:none;
}
.profile-card > :not(img), .class-card > :not(img) { position:relative; z-index:3; }
.profile-card h4, .class-card h4 {
  position:absolute; left:7mm; top:7mm;
  max-width:112mm; margin:0; padding:3mm 5mm 2.5mm;
  color:#76342c; font-size:23pt; line-height:1; font-variant:small-caps; letter-spacing:.025em;
  border:0; border-bottom:1.2px solid rgba(116,52,45,.45);
  background:linear-gradient(90deg, rgba(255,250,238,.95), rgba(255,250,238,.76), rgba(255,250,238,0));
  border-radius:3mm 0 0 3mm;
  text-shadow:0 1px 0 rgba(255,255,255,.55);
}
.profile-card p, .class-card p {
  position:absolute; left:7mm; top:25mm;
  width:82mm; margin:0; padding:3mm 4mm;
  font-size:12.4pt;
  background:linear-gradient(180deg, rgba(255,250,238,.90), rgba(250,235,199,.74));
  border:1px solid rgba(91,57,22,.36); border-radius:2.8mm;
  box-shadow:0 1mm 5mm rgba(0,0,0,.14);
}
.profile-card > ul, .class-card > ul {
  position:absolute; left:7mm; bottom:9mm;
  width:86mm; margin:0; padding:3.2mm 4.4mm 3.2mm 8mm;
  font-size:11.2pt;
  background:linear-gradient(180deg, rgba(255,250,238,.92), rgba(250,235,199,.80));
  border:1px solid rgba(91,57,22,.42); border-radius:3mm;
  box-shadow:0 1.2mm 6mm rgba(0,0,0,.18);
}
.class-card > ul { width:80mm; }
.spell-block {
  position:absolute; right:7mm; bottom:9mm;
  width:82mm; margin:0; padding:3.2mm 4.2mm;
  border:1px solid rgba(75,46,103,.48); border-radius:3mm;
  background:linear-gradient(180deg, rgba(246,238,255,.92), rgba(255,249,232,.78));
  break-inside:avoid; page-break-inside:avoid; box-shadow:0 1.2mm 6mm rgba(0,0,0,.18);
  font-size:10.7pt;
}
.spell-block .spell-title { margin:0 0 1.5mm; color:#4b2e67; font-weight:700; font-variant:small-caps; letter-spacing:.03em; }
.spell-block ul { margin:0; padding-left:5mm; }

/* Bestiary can stay layered but shorter unless requested otherwise. */
.creature-card {
  position:relative; clear:both; min-height:78mm; margin:6mm 0 7mm; padding:0;
  border:1.3mm solid #302315; border-radius:4.5mm; overflow:hidden;
  box-shadow:0 2mm 7mm rgba(68,38,15,.24); break-inside:avoid; page-break-inside:avoid; background:#332617;
}
.creature-card figure.art-plate { position:absolute; inset:0; width:100%; height:100%; margin:0; padding:0; border:0; border-radius:0; box-shadow:none; background:transparent; z-index:0; }
.creature-card figure.art-plate img { width:100%; height:100%; max-height:none; object-fit:cover; object-position:center; opacity:.86; filter:saturate(.98) contrast(.96); }
.creature-card::before { content:""; position:absolute; inset:0; z-index:1; background:linear-gradient(90deg, rgba(255,247,224,.9) 0%, rgba(255,247,224,.72) 54%, rgba(255,247,224,.16) 100%); }
.creature-card::after { content:""; position:absolute; inset:2.3mm; z-index:3; border:1px solid rgba(255,238,177,.72); border-radius:3mm; pointer-events:none; }
.creature-card > :not(figure) { position:relative; z-index:2; }
.creature-card h2 { clear:none; width:64%; margin:5mm 0 1.8mm 5mm; padding:2mm 3mm 1.5mm; color:#74342d; font-size:15.5pt; font-variant:small-caps; border:0; border-bottom:1px solid rgba(116,52,45,.34); background:linear-gradient(90deg, rgba(255,250,238,.93), rgba(255,250,238,.56), transparent); border-radius:2mm 0 0 2mm; }
.creature-card h2::first-letter { font-size:1em; color:#74342d; }
.creature-card > ul, .creature-card h3, .creature-card h3 + ul { width:62%; margin-left:5mm; margin-right:0; }
.creature-card > ul, .creature-card h3 + ul { padding:2.5mm 4mm 2.8mm 8mm; background:linear-gradient(180deg, rgba(255,250,238,.90), rgba(250,235,199,.78)); border:1px solid rgba(91,57,22,.38); border-radius:2.6mm; box-shadow:0 1mm 4mm rgba(0,0,0,.12); }
.creature-card h3 { clear:none; margin-top:2.5mm; padding:1.5mm 3mm 0; font-size:11.2pt; color:#4b2e67; border:0; }
.pagebreak { clear:both; page-break-after:always; }
@media screen { body { box-shadow:0 0 16mm rgba(58,38,12,.22); } }
@media print {
  html, body { background:white; }
  main.book { padding:0; }
  a { color:inherit; text-decoration:none; }
  figure.art-plate, .scene-plate, .profile-card, .class-card, .creature-card, blockquote, table { break-inside:avoid-page; page-break-inside:avoid; }
}
'''

NOTE = '<blockquote class="layout-note"><strong>Print note:</strong> Race and class entries now use full-page feature plates. The entire artwork is preserved with text layered on top, so portraits are not cut off inside small boxes.</blockquote>'

for path in sorted(PRINT_DIR.glob('*-a4.html')):
    text = path.read_text(encoding='utf-8')
    text = STYLE_RE.sub('<style>\n' + CSS + '\n</style>', text, count=1)
    text = re.sub(r'<blockquote class="layout-note">.*?</blockquote>', NOTE, text, count=1, flags=re.S)
    path.write_text(text, encoding='utf-8')
    print(path.name, 'profile', text.count('<section class="profile-card'), 'class', text.count('<section class="class-card'), 'scene', text.count('class="scene-plate"'))
