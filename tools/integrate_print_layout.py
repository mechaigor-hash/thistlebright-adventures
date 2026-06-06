#!/usr/bin/env python3
"""Rebuild printable A4 HTML with integrated, layered artwork.

The earlier printables treated images as standalone blocks, which made them split
across page boundaries in browser print previews. This post-processes the HTML
into more D&D-style parchment pages: framed art panels, text-wrapped profile
cards, class ability boxes, and explicit print break rules.
"""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PRINT_DIR = ROOT / "printable-a4"

CSS = r'''
@page { size: A4 portrait; margin: 12mm 11mm 14mm; }
* { box-sizing: border-box; }
:root {
  --ink:#2a2118;
  --muted:#5d5144;
  --green:#285e3d;
  --purple:#4b2e67;
  --red:#8b352d;
  --gold:#b88a2d;
  --line:#c8ae78;
  --paper:#fbf2dc;
  --paper2:#fffaf0;
  --wash:rgba(255,244,217,.84);
}
html { background:#d8c59a; }
body {
  margin:0 auto;
  max-width: 210mm;
  color:var(--ink);
  font-family: "DejaVu Serif", Georgia, "Times New Roman", serif;
  font-size:10.6pt;
  line-height:1.34;
  background:
    radial-gradient(circle at 8% 2%, rgba(135,83,48,.11), transparent 34mm),
    radial-gradient(circle at 94% 16%, rgba(40,94,61,.09), transparent 42mm),
    linear-gradient(90deg, rgba(122,84,34,.06), transparent 12mm, transparent calc(100% - 12mm), rgba(122,84,34,.06)),
    var(--paper2);
  padding:0;
}
main.book {
  min-height:100vh;
  padding:0 3mm 6mm;
}
p, li { orphans:3; widows:3; }
p { margin:0 0 3.2mm; }
ul, ol { margin-top:1.5mm; margin-bottom:3.8mm; padding-left:6mm; }
li { margin:.7mm 0; }
strong { color:#251b13; }
h1, h2, h3, h4 { text-wrap:balance; break-after:avoid; }
h1 {
  page-break-before:always;
  min-height:74mm;
  margin:0 -3mm 8mm;
  padding:17mm 16mm 10mm;
  color:#fff8e8;
  font-size:25pt;
  letter-spacing:.02em;
  line-height:1.06;
  background:
    linear-gradient(90deg, rgba(23,35,26,.82), rgba(46,35,65,.62)),
    url("../art/generated/22-book-title-spread.png") center/cover no-repeat;
  border-bottom:2.2mm solid #6f4b1f;
  box-shadow: inset 0 -18mm 26mm rgba(0,0,0,.27);
  text-shadow:0 2px 4px rgba(0,0,0,.45);
}
h1:first-child { page-break-before:auto; }
h2 {
  clear:both;
  margin:8mm 0 4.5mm;
  color:var(--green);
  font-size:18pt;
  border-top:1.4pt dashed rgba(184,138,45,.72);
  padding-top:5mm;
}
h2::first-letter { font-size:1.28em; color:var(--red); }
h3 {
  clear:both;
  margin:6mm 0 2.4mm;
  color:var(--red);
  font-size:14pt;
  border-bottom:1px solid rgba(184,138,45,.6);
}
h4 {
  margin:0 0 1.6mm;
  color:var(--purple);
  font-size:12.8pt;
  letter-spacing:.015em;
}
hr {
  clear:both;
  border:0;
  height:4mm;
  margin:7mm 0;
  background:
    radial-gradient(circle, rgba(139,53,45,.95) 1.1mm, transparent 1.2mm) center/7mm 4mm repeat-x;
  opacity:.6;
}
blockquote {
  clear:both;
  break-inside:avoid;
  margin:5mm 0;
  padding:4mm 5mm 4mm 7mm;
  border:1px solid rgba(139,53,45,.38);
  border-left:4mm solid rgba(139,53,45,.72);
  background:
    linear-gradient(90deg, rgba(255,244,217,.96), rgba(250,236,199,.72)),
    radial-gradient(circle at 100% 0, rgba(184,138,45,.18), transparent 28mm);
  border-radius:1.5mm 5mm 5mm 1.5mm;
  box-shadow:0 1mm 3mm rgba(79,50,18,.12);
}
table {
  width:100%;
  border-collapse:collapse;
  margin:4mm 0 5mm;
  font-size:9.4pt;
  break-inside:avoid;
  box-shadow:0 .8mm 2.6mm rgba(75,45,17,.12);
}
th,td { border:1px solid #c9b88b; padding:3px 5px; vertical-align:top; }
th { background:#d9e6c0; color:#243e28; }
tr:nth-child(even) td { background:rgba(224,235,202,.62); }
img { max-width:100%; height:auto; }
/* Any art not claimed by a profile/class block becomes a manuscript plate. */
figure.art-plate {
  clear:both;
  position:relative;
  margin:5mm 0 6mm;
  padding:1.8mm;
  break-inside:avoid;
  page-break-inside:avoid;
  border:1.2mm solid #322615;
  border-radius:4.5mm;
  background:#2e2418;
  box-shadow:0 2mm 6mm rgba(68,38,15,.22);
  overflow:hidden;
}
figure.art-plate::before {
  content:"";
  position:absolute;
  inset:2.3mm;
  border:1px solid rgba(255,238,177,.7);
  border-radius:3mm;
  pointer-events:none;
  z-index:2;
}
figure.art-plate img {
  display:block;
  width:100%;
  max-height:88mm;
  object-fit:cover;
  object-position:center;
  border-radius:2.7mm;
  break-inside:avoid;
  page-break-inside:avoid;
}
figure.art-plate.title-art img { max-height:70mm; }
figure.art-plate.tall img { max-height:112mm; object-fit:contain; background:#f7ecd2; }
.profile-card, .class-card, .creature-card {
  position:relative;
  clear:both;
  min-height:62mm;
  margin:5.5mm 0;
  padding:5mm 5mm 4mm 55mm;
  border:1px solid rgba(105,75,32,.45);
  border-radius:5mm 2mm 5mm 2mm;
  background:
    linear-gradient(90deg, rgba(255,250,237,.95), rgba(250,238,210,.86)),
    radial-gradient(circle at 92% 8%, rgba(184,138,45,.16), transparent 36mm);
  box-shadow:0 1.3mm 5mm rgba(84,55,24,.15);
  overflow:hidden;
  break-inside:avoid;
  page-break-inside:avoid;
}
.profile-card:nth-of-type(even), .class-card:nth-of-type(even), .creature-card:nth-of-type(even) {
  padding-left:5mm;
  padding-right:55mm;
}
.profile-card::after, .class-card::after, .creature-card::after {
  content:"";
  position:absolute;
  inset:2.2mm;
  border:1px solid rgba(184,138,45,.38);
  border-radius:3.8mm 1.4mm 3.8mm 1.4mm;
  pointer-events:none;
}
.profile-card h4, .class-card h4, .creature-card h2 {
  font-variant:small-caps;
  color:#76342c;
  border:0;
  border-bottom:1px solid rgba(184,138,45,.6);
  padding:0 0 1mm;
  margin:0 0 1.6mm;
}
.creature-card h2 { clear:none; font-size:15.5pt; }
.creature-card h2::first-letter { font-size:1em; color:#76342c; }
.creature-card h3 { clear:none; margin:3mm 0 1mm; font-size:11.2pt; color:#4b2e67; }
.profile-card img, .class-card img, .creature-card figure.art-plate {
  position:absolute;
  left:0;
  top:0;
  width:50mm;
  height:100%;
  object-fit:cover;
  object-position:center;
  margin:0;
  border-radius:4.6mm 22mm 22mm 4.6mm;
  border-right:1.2mm solid rgba(184,138,45,.72);
  box-shadow: inset -10mm 0 14mm rgba(255,250,237,.65);
}
.creature-card figure.art-plate { padding:0; border:0; box-shadow:none; background:transparent; }
.creature-card figure.art-plate::before { display:none; }
.creature-card figure.art-plate img { width:100%; height:100%; max-height:none; object-fit:cover; border-radius:4.6mm 22mm 22mm 4.6mm; }
.profile-card:nth-of-type(even) img, .class-card:nth-of-type(even) img, .creature-card:nth-of-type(even) figure.art-plate {
  left:auto;
  right:0;
  border-right:0;
  border-left:1.2mm solid rgba(184,138,45,.72);
  border-radius:22mm 4.6mm 4.6mm 22mm;
}
.creature-card:nth-of-type(even) figure.art-plate img { border-radius:22mm 4.6mm 4.6mm 22mm; }
.profile-card ul, .class-card ul { padding-left:4.8mm; margin-bottom:1mm; }
.spell-block {
  margin-top:3mm;
  padding:3mm 4mm;
  border:1px solid rgba(75,46,103,.45);
  border-radius:2.8mm;
  background:linear-gradient(180deg, rgba(246,238,255,.9), rgba(255,249,232,.86));
  break-inside:avoid;
  page-break-inside:avoid;
}
.spell-block .spell-title {
  margin:0 0 1.5mm;
  color:#4b2e67;
  font-weight:700;
  font-variant:small-caps;
  letter-spacing:.03em;
}
.spell-block ul { margin:0; }
.chapter-opener {
  break-inside:avoid;
  page-break-inside:avoid;
}
.pagebreak { clear:both; page-break-after:always; }
@media screen {
  body { box-shadow:0 0 16mm rgba(58,38,12,.22); }
  main.book { padding-top:0; }
}
@media print {
  html, body { background:white; }
  main.book { padding:0; }
  a { color:inherit; text-decoration:none; }
  figure.art-plate, .profile-card, .class-card, blockquote, table { break-inside:avoid-page; page-break-inside:avoid; }
}
'''

RACE_NAMES = [
    "Human Glenfolk", "Fairy-Touched", "Brownie-Kin", "Selkie-Born", "Rowan-Kin", "Dragon-Friend"
]
CLASS_NAMES = ["Thistle Knight", "Glen Wizard", "Loch Scout", "Hearth Bard", "Fairy Friend"]

STYLE_RE = re.compile(r"<style>.*?</style>", re.S)
IMG_RE = re.compile(r'<img src="([^"]+)" alt="([^"]*)">')


def replace_css(text: str) -> str:
    text = STYLE_RE.sub('<style>\n' + CSS + '\n</style>', text, count=1)
    text = text.replace('<body>', '<body><main class="book">')
    text = text.replace('</body>', '</main></body>')
    return text


def wrap_standalone_images(text: str) -> str:
    # Wrap every remaining plain image. Profile transforms run first; after wrapping,
    # we immediately unwrap any portrait that is the first child of a profile/class
    # section so CSS can layer it as a side plate rather than a separate figure.
    def repl(m):
        src, alt = m.group(1), m.group(2)
        cls = 'art-plate title-art' if 'title' in src or 'cover' in src or 'book-title' in src else 'art-plate'
        if 'sheet' in src or 'map' in src:
            cls += ' tall'
        return f'<figure class="{cls}"><img src="{src}" alt="{alt}"></figure>'
    text = IMG_RE.sub(repl, text)
    text = re.sub(r'(<section class="(?:profile-card race-card|class-card)">\s*)<figure class="art-plate(?: [^"]*)?"><img ([^>]+)></figure>', r'\1<img \2>', text)
    return text


def profile_pattern(name: str) -> re.Pattern:
    # Capture h4, image, paragraph, then one ul; non-greedy and stops before next heading/blockquote/hr.
    return re.compile(
        rf'(<h4>{re.escape(name)}</h4>\s*)'
        rf'(<img src="([^"]+)" alt="([^"]*)">\s*)'
        rf'(.*?)'
        rf'(<ul>.*?</ul>)',
        re.S,
    )


def class_pattern(name: str) -> re.Pattern:
    return re.compile(
        rf'(<h4>{re.escape(name)}</h4>\s*)'
        rf'(<img src="([^"]+)" alt="([^"]*)">\s*)'
        rf'(.*?)'
        rf'(<ul>.*?</ul>)\s*'
        rf'<p><strong>Abilities / spells block:</strong></p>\s*'
        rf'(<ul>.*?</ul>)',
        re.S,
    )


def transform_profiles(text: str) -> str:
    for name in RACE_NAMES:
        pat = profile_pattern(name)
        def repl(m):
            h4, _imgtag, src, alt, between, ul = m.groups()
            return f'<section class="profile-card race-card">\n<img src="{src}" alt="{alt}">\n{h4}{between}{ul}\n</section>'
        text = pat.sub(repl, text)
    for name in CLASS_NAMES:
        pat = class_pattern(name)
        def repl(m):
            h4, _imgtag, src, alt, between, details_ul, spells_ul = m.groups()
            return (f'<section class="class-card">\n<img src="{src}" alt="{alt}">\n{h4}{between}{details_ul}\n'
                    f'<div class="spell-block"><p class="spell-title">Abilities / spells</p>{spells_ul}</div>\n</section>')
        text = pat.sub(repl, text)
    return text


def add_intro_note(text: str) -> str:
    if 'layout-note' in text:
        return text
    note = ('<blockquote class="layout-note"><strong>Print note:</strong> This A4 edition uses layered parchment panels. '
            'Artwork is anchored to its text block so race/class portraits and scene art should not split across printed pages.</blockquote>')
    return text.replace('</h1>', '</h1>\n' + note, 1)


def process(path: Path) -> tuple[int,int,int]:
    original = path.read_text(encoding='utf-8')
    text = replace_css(original)
    text = transform_profiles(text)
    text = wrap_standalone_images(text)
    text = add_intro_note(text)
    path.write_text(text, encoding='utf-8')
    return text.count('class="profile-card'), text.count('class="class-card'), text.count('<figure class="art-plate')


def main():
    for path in sorted(PRINT_DIR.glob('*-a4.html')):
        p, c, f = process(path)
        print(f'{path.name}: profile_cards={p} class_cards={c} art_plates={f}')

if __name__ == '__main__':
    main()
