#!/usr/bin/env python3
"""Turn A4 printables into true layered art plates.

This is intentionally different from the earlier side-art layout: artwork fills the
card/plate as a background layer, and readable parchment copy blocks sit on top.
"""
from __future__ import annotations
from pathlib import Path
import re

PRINT_DIR = Path('/home/mecha-igor/prepped/scottish-fairy-quest/printable-a4')

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

/* Framed art plate for images that are still standalone. */
figure.art-plate { clear:both; position:relative; margin:5mm 0 6mm; padding:1.8mm; break-inside:avoid; page-break-inside:avoid; border:1.2mm solid #322615; border-radius:4.5mm; background:#2e2418; box-shadow:0 2mm 6mm rgba(68,38,15,.22); overflow:hidden; }
figure.art-plate::before { content:""; position:absolute; inset:2.3mm; border:1px solid rgba(255,238,177,.7); border-radius:3mm; pointer-events:none; z-index:2; }
figure.art-plate img { display:block; width:100%; max-height:88mm; object-fit:cover; object-position:center; border-radius:2.7mm; break-inside:avoid; page-break-inside:avoid; }
figure.art-plate.title-art img { max-height:70mm; } figure.art-plate.tall img { max-height:112mm; object-fit:contain; background:#f7ecd2; }

/* True layered scene plate: image fills the plate, copy is overlaid on top. */
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
  position:absolute; left:5mm; right:5mm; bottom:5mm; z-index:2;
  max-width:136mm; margin:0 auto; padding:3.5mm 4.5mm;
  background:linear-gradient(180deg, rgba(255,250,238,.91), rgba(250,235,199,.84));
  border:1px solid rgba(91,57,22,.55); border-radius:3mm; box-shadow:0 1mm 5mm rgba(0,0,0,.25);
  backdrop-filter: blur(1px);
}
.scene-copy p:last-child, .scene-copy ul:last-child, .scene-copy ol:last-child { margin-bottom:0; }

/* Race/class/bestiary cards: the art is no longer a side thumbnail. It fills the whole card. */
.profile-card, .class-card, .creature-card {
  position:relative; clear:both; min-height:78mm; margin:6mm 0 7mm; padding:0;
  border:1.3mm solid #302315; border-radius:4.5mm; overflow:hidden;
  box-shadow:0 2mm 7mm rgba(68,38,15,.24); break-inside:avoid; page-break-inside:avoid;
  background:#332617;
}
.profile-card > img, .class-card > img, .creature-card figure.art-plate {
  position:absolute; inset:0; width:100%; height:100%; margin:0; padding:0; border:0; border-radius:0; box-shadow:none; background:transparent; z-index:0;
}
.profile-card > img, .class-card > img, .creature-card figure.art-plate img {
  width:100%; height:100%; max-height:none; object-fit:cover; object-position:center; opacity:.86; filter:saturate(.98) contrast(.96);
}
.profile-card::before, .class-card::before, .creature-card::before {
  content:""; position:absolute; inset:0; z-index:1;
  background:
    radial-gradient(circle at 78% 18%, rgba(255,245,206,.08), transparent 32mm),
    linear-gradient(90deg, rgba(255,247,224,.88) 0%, rgba(255,247,224,.74) 50%, rgba(255,247,224,.25) 76%, rgba(255,247,224,.05) 100%);
}
.class-card::before { background:linear-gradient(90deg, rgba(247,239,255,.88) 0%, rgba(255,247,224,.76) 55%, rgba(255,247,224,.18) 100%); }
.creature-card::before { background:linear-gradient(90deg, rgba(255,247,224,.9) 0%, rgba(255,247,224,.72) 54%, rgba(255,247,224,.16) 100%); }
.profile-card::after, .class-card::after, .creature-card::after, .scene-plate .inner-line {
  content:""; position:absolute; inset:2.3mm; z-index:3; border:1px solid rgba(255,238,177,.72); border-radius:3mm; pointer-events:none;
}
.profile-card > :not(img), .class-card > :not(img), .creature-card > :not(figure) { position:relative; z-index:2; }
.profile-card h4, .class-card h4, .creature-card h2 {
  width:64%; margin:5mm 0 1.8mm 5mm; padding:2mm 3mm 1.5mm;
  color:#74342d; font-variant:small-caps; letter-spacing:.02em; border:0; border-bottom:1px solid rgba(116,52,45,.34);
  background:linear-gradient(90deg, rgba(255,250,238,.93), rgba(255,250,238,.56), transparent); border-radius:2mm 0 0 2mm;
}
.creature-card h2 { clear:none; font-size:15.5pt; }
.creature-card h2::first-letter { font-size:1em; color:#74342d; }
.profile-card p, .class-card p, .creature-card > ul, .profile-card > ul, .class-card > ul, .creature-card h3, .creature-card h3 + ul, .spell-block {
  width:62%; margin-left:5mm; margin-right:0;
}
.profile-card p, .class-card p { padding:0 3mm; }
.profile-card > ul, .class-card > ul, .creature-card > ul, .creature-card h3 + ul {
  padding:2.5mm 4mm 2.8mm 8mm;
  background:linear-gradient(180deg, rgba(255,250,238,.90), rgba(250,235,199,.78));
  border:1px solid rgba(91,57,22,.38); border-radius:2.6mm; box-shadow:0 1mm 4mm rgba(0,0,0,.12);
}
.creature-card h3 { clear:none; margin-top:2.5mm; padding:1.5mm 3mm 0; font-size:11.2pt; color:#4b2e67; border:0; }
.spell-block { margin-top:3mm; margin-bottom:5mm; padding:3mm 4mm; border:1px solid rgba(75,46,103,.45); border-radius:2.8mm; background:linear-gradient(180deg, rgba(246,238,255,.90), rgba(255,249,232,.78)); break-inside:avoid; page-break-inside:avoid; box-shadow:0 1mm 4mm rgba(0,0,0,.13); }
.spell-block .spell-title { margin:0 0 1.5mm; color:#4b2e67; font-weight:700; font-variant:small-caps; letter-spacing:.03em; }
.spell-block ul { margin:0; }
.pagebreak { clear:both; page-break-after:always; }
@media screen { body { box-shadow:0 0 16mm rgba(58,38,12,.22); } }
@media print {
  html, body { background:white; }
  main.book { padding:0; }
  a { color:inherit; text-decoration:none; }
  figure.art-plate, .scene-plate, .profile-card, .class-card, .creature-card, blockquote, table { break-inside:avoid-page; page-break-inside:avoid; }
}
'''

STYLE_RE = re.compile(r'<style>.*?</style>', re.S)
FIG_P_RE = re.compile(
    r'(<figure class="art-plate(?: [^"]*)?"><img src="[^"]+" alt="[^"]+"></figure>)\s*(<p>(?!(?:<strong>Print note:|<strong>Grown-up:|<strong>Player:)).{35,}?</p>)',
    re.S,
)

def refresh_css(text: str) -> str:
    return STYLE_RE.sub('<style>\n' + CSS + '\n</style>', text, count=1)

def wrap_scene_plates(text: str) -> str:
    if 'class="scene-plate"' in text:
        return text
    def repl(m: re.Match) -> str:
        fig, para = m.group(1), m.group(2)
        # Do not wrap art already inside card sections.
        start = m.start()
        last_section = text.rfind('<section', 0, start)
        last_close = text.rfind('</section>', 0, start)
        if last_section > last_close:
            return m.group(0)
        return f'<section class="scene-plate">\n{fig}\n<div class="scene-copy">{para}</div>\n</section>'
    return FIG_P_RE.sub(repl, text)

def update_note(text: str) -> str:
    return re.sub(
        r'<blockquote class="layout-note">.*?</blockquote>',
        '<blockquote class="layout-note"><strong>Print note:</strong> This A4 edition uses layered artwork: text panels sit on top of the illustrations, with print-break rules to keep plates intact.</blockquote>',
        text,
        count=1,
        flags=re.S,
    )

for path in sorted(PRINT_DIR.glob('*-a4.html')):
    text = path.read_text(encoding='utf-8')
    text = refresh_css(text)
    text = wrap_scene_plates(text)
    text = update_note(text)
    path.write_text(text, encoding='utf-8')
    print(path.name, 'scene_plates', text.count('class="scene-plate"'), 'profile', text.count('<section class="profile-card'), 'class', text.count('<section class="class-card'), 'creature', text.count('<section class="creature-card'))
