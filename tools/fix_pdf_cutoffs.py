#!/usr/bin/env python3
"""Patch A4 HTML print CSS to stop bottom clipping in generated PDFs.

The previous full-page feature card rules were slightly taller than an A4 page
once main padding/margins were counted, and text overlays used overflow:hidden.
That made the bottom lines of some panels vanish. This patch keeps the book
image-heavy, but gives every card safe A4 clearance and never hides text.
"""
from __future__ import annotations
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PRINT_DIR = ROOT / "printable-a4"
STYLE_RE = re.compile(r"<style>.*?</style>", re.S)

SAFE_CSS = r'''
@page { size: A4 portrait; margin: 0; background: #fffaf0; }
* { box-sizing: border-box; }
:root {
  --ink:#2a2118; --muted:#5d5144; --green:#285e3d; --purple:#4b2e67;
  --red:#8b352d; --gold:#b88a2d; --line:#c8ae78; --paper:#fbf2dc; --paper2:#fffaf0;
}
html { background:#d8c59a; }
body { margin:0 auto; max-width:210mm; color:var(--ink); font-family:"DejaVu Serif", Georgia, "Times New Roman", serif; font-size:10.2pt; line-height:1.28; background:var(--paper2); }
main.book { min-height:100vh; padding:6mm 8mm 8mm; background:var(--paper2); }
p, li { orphans:3; widows:3; } p { margin:0 0 2.6mm; } ul, ol { margin-top:1.2mm; margin-bottom:3mm; padding-left:5.2mm; break-inside:avoid-page; page-break-inside:avoid; } li { margin:.45mm 0; break-inside:avoid; } .keep-block { break-inside:avoid-page; page-break-inside:avoid; margin:0 0 3mm; } .keep-block > :last-child { margin-bottom:0; }
strong { color:#251b13; } h1, h2, h3, h4 { text-wrap:balance; break-after:avoid; }
h1 { page-break-before:always; min-height:68mm; margin:0 -2mm 7mm; padding:15mm 14mm 9mm; color:#fff8e8; font-size:24pt; letter-spacing:.02em; line-height:1.04; background:linear-gradient(90deg, rgba(23,35,26,.82), rgba(46,35,65,.62)), url("../art/generated/22-book-title-spread.png") center/cover no-repeat; border-bottom:2.2mm solid #6f4b1f; box-shadow: inset 0 -18mm 26mm rgba(0,0,0,.27); text-shadow:0 2px 4px rgba(0,0,0,.45); }
h1:first-child { page-break-before:auto; }
h2 { clear:both; margin:7mm 0 3.6mm; color:var(--green); font-size:17pt; border-top:1.2pt dashed rgba(184,138,45,.72); padding-top:4mm; break-after:avoid-page; page-break-after:avoid; }
h2::first-letter { font-size:1.22em; color:var(--red); }
h3 { clear:both; margin:5mm 0 2mm; color:var(--red); font-size:13pt; border-bottom:1px solid rgba(184,138,45,.6); break-after:avoid-page; page-break-after:avoid; }
h4 { margin:0 0 1.3mm; color:var(--purple); font-size:12pt; letter-spacing:.015em; }
hr { clear:both; border:0; height:3.5mm; margin:6mm 0; background:radial-gradient(circle, rgba(139,53,45,.95) 1mm, transparent 1.1mm) center/7mm 3.5mm repeat-x; opacity:.6; }
blockquote, table { break-inside:avoid; page-break-inside:avoid; }
blockquote { clear:both; margin:4mm 0; padding:3.5mm 4.5mm 3.5mm 6mm; border:1px solid rgba(139,53,45,.38); border-left:3.4mm solid rgba(139,53,45,.72); background:linear-gradient(90deg, rgba(255,244,217,.96), rgba(250,236,199,.72)); border-radius:1.5mm 5mm 5mm 1.5mm; box-shadow:0 1mm 3mm rgba(79,50,18,.12); }
table { width:100%; border-collapse:collapse; margin:3.5mm 0 4mm; font-size:9pt; box-shadow:0 .8mm 2.6mm rgba(75,45,17,.12); }
th,td { border:1px solid #c9b88b; padding:3px 5px; vertical-align:top; } th { background:#d9e6c0; color:#243e28; } tr:nth-child(even) td { background:rgba(224,235,202,.62); }
.layout-note { display:none; }
blockquote, .spell-block, .feature-copy, .scene-copy { font-family:"DejaVu Serif", Georgia, serif; }
blockquote strong, .spell-title { letter-spacing:.025em; }
img { max-width:100%; height:auto; }

/* Standalone art plates: page-scale but short enough to leave safe A4 room. */
figure.art-plate {
  clear:both; position:relative; width:calc(100% + 16mm); min-height:180mm; margin:3mm -8mm 4mm; padding:0;
  break-inside:avoid; page-break-inside:avoid; page-break-before:auto; page-break-after:auto;
  border:0; border-radius:0; background:#2e2418; box-shadow:none; overflow:hidden;
}
figure.art-plate::before { display:none; }
figure.art-plate img { display:block; width:100%; height:180mm; max-height:none; object-fit:cover; object-position:center; border-radius:0; background:#2e2418; }
figure.art-plate.title-art, figure.art-plate.title-art img { min-height:136mm; height:136mm; }
figure.art-plate.tall, figure.art-plate.tall img { min-height:148mm; height:148mm; }

/* Scene plates: large image + overlay, but no fixed content clipping. */
.scene-plate { position:relative; clear:both; width:calc(100% + 16mm); min-height:190mm; margin:3mm -8mm 4mm; padding:0; border:0; border-radius:0; overflow:hidden; box-shadow:none; break-inside:avoid; page-break-inside:avoid; page-break-before:auto; page-break-after:auto; background:#2e2418; }
.scene-plate figure.art-plate { position:relative; inset:auto; width:100%; min-height:190mm; height:190mm; margin:0; padding:0; border:0; border-radius:0; box-shadow:none; background:transparent; page-break-before:auto; page-break-after:auto; }
.scene-plate figure.art-plate::before { display:none; }
.scene-plate figure.art-plate img { width:100%; height:190mm; max-height:none; object-fit:cover; object-position:center; border-radius:0; opacity:.99; background:#2e2418; }
.scene-plate.scene-full { min-height:270mm; }
.scene-plate.scene-full figure.art-plate { min-height:270mm; height:270mm; }
.scene-plate.scene-full figure.art-plate img { height:270mm; }
.scene-plate::after, .profile-card::after, .class-card::after, .creature-card::after { display:none; }
.scene-copy { position:absolute; z-index:3; left:50%; transform:translateX(-50%); bottom:5mm; width:148mm; max-height:none; overflow:visible; padding:3mm 4mm; background:linear-gradient(180deg, rgba(255,250,238,.96), rgba(250,235,199,.88)); border:1px solid rgba(91,57,22,.58); border-left:2.4mm solid rgba(139,53,45,.75); border-radius:1.5mm 3mm 3mm 1.5mm; box-shadow:0 1.2mm 6mm rgba(0,0,0,.25); font-size:9.7pt; line-height:1.23; }
.scene-copy p:last-child, .scene-copy ul:last-child, .scene-copy ol:last-child { margin-bottom:0; }

/* Full-page feature plates with ONE overlay group. Shorter than A4 after padding. */
.profile-card, .class-card, .creature-card { position:relative; clear:both; width:calc(100% + 16mm); min-height:282mm; margin:0 -8mm 0; padding:0; border:0; border-radius:0; overflow:hidden; box-shadow:none; break-inside:avoid; page-break-inside:avoid; page-break-before:auto; page-break-after:auto; background:#2e2418; }
.profile-card > img, .class-card > img { position:relative; display:block; z-index:0; width:100%; height:282mm; max-width:none; max-height:none; margin:0; padding:0; border:0; border-radius:0; object-fit:cover; object-position:center; opacity:.99; background:#2e2418; }
.creature-card figure.art-plate { position:relative; width:100%; min-height:282mm; height:282mm; margin:0; padding:0; border:0; border-radius:0; box-shadow:none; page-break-before:auto; page-break-after:auto; background:transparent; }
.creature-card figure.art-plate img { width:100%; height:282mm; max-height:none; object-fit:cover; object-position:center; padding:0; opacity:.99; background:#2e2418; }
.profile-card::before, .class-card::before, .creature-card::before { content:""; position:absolute; inset:0; z-index:1; background:linear-gradient(180deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0) 38%, rgba(255,248,226,.22) 62%, rgba(42,29,16,.20) 100%); pointer-events:none; }
.feature-copy { position:absolute; z-index:3; left:50% !important; right:auto !important; top:auto !important; bottom:5mm !important; transform:translateX(-50%); width:158mm; max-height:none; overflow:visible; padding:3mm 4mm; background:linear-gradient(180deg, rgba(255,250,238,.97), rgba(250,235,199,.90)); border:1px solid rgba(91,57,22,.55); border-top:1.8mm solid rgba(139,53,45,.78); border-radius:1.5mm 3.2mm 3.2mm 1.5mm; box-shadow:0 1.5mm 7mm rgba(0,0,0,.24); }
.copy-left .feature-copy, .copy-right .feature-copy, .copy-bottom .feature-copy { left:50% !important; right:auto !important; top:auto !important; bottom:5mm !important; transform:translateX(-50%); width:158mm; max-height:none; overflow:visible; }
.example-panel { margin:5mm 0 6mm; padding:4mm 6mm; border:1px solid rgba(139,53,45,.42); border-left:3.4mm solid rgba(139,53,45,.78); border-radius:2mm 6mm 6mm 2mm; background:linear-gradient(180deg, rgba(255,250,238,.97), rgba(247,231,190,.91)); box-shadow:0 1.4mm 5mm rgba(77,45,16,.16), inset 0 0 0 1px rgba(255,255,255,.48); break-inside:avoid; page-break-inside:avoid; }
.example-panel h3:first-child { margin-top:0; }
.example-panel p:last-child, .example-panel table:last-child, .example-panel blockquote:last-child { margin-bottom:0; }
.feature-copy h2, .feature-copy h3, .feature-copy h4 { clear:none; margin:0 0 1.4mm; padding:0 0 1mm; color:#76342c; font-size:16.5pt; line-height:1.0; font-variant:small-caps; letter-spacing:.02em; border:0; border-bottom:1px solid rgba(116,52,45,.35); background:none; }
.feature-copy p { position:static; width:auto; margin:0 0 2mm; padding:0; font-size:9.5pt; line-height:1.2; background:none; border:0; box-shadow:none; }
.feature-copy ul { position:static; width:auto; margin:0 0 2mm; padding-left:5mm; font-size:8.9pt; line-height:1.16; background:none; border:0; box-shadow:none; }
.feature-copy li { margin:.25mm 0; }
.spell-block { position:static; width:auto; margin:2mm 0 0; padding:2mm 3mm; border:1px solid rgba(75,46,103,.48); border-radius:2.5mm; background:linear-gradient(180deg, rgba(246,238,255,.92), rgba(255,249,232,.78)); break-inside:avoid; page-break-inside:avoid; box-shadow:0 1.2mm 5mm rgba(0,0,0,.13); font-size:8.7pt; line-height:1.14; }
.spell-block .spell-title { margin:0 0 1mm; color:#4b2e67; font-weight:700; font-variant:small-caps; letter-spacing:.03em; }
.spell-block ul { margin:0; padding-left:4mm; font-size:8.6pt; line-height:1.12; }
.pagebreak { clear:both; page-break-after:always; }
@media screen { body { box-shadow:0 0 16mm rgba(58,38,12,.22); } }
@media print { html, body { background:var(--paper2); } main.book { padding:6mm 8mm 8mm; } a { color:inherit; text-decoration:none; } figure.art-plate, .scene-plate, .profile-card, .class-card, .creature-card, blockquote, table { break-inside:avoid-page; page-break-inside:avoid; } }
'''

for path in sorted(PRINT_DIR.glob("*-a4.html")):
    text = path.read_text(encoding="utf-8")
    if not STYLE_RE.search(text):
        raise SystemExit(f"No <style> block found in {path}")
    text = STYLE_RE.sub("<style>\n" + SAFE_CSS + "\n</style>", text, count=1)
    path.write_text(text, encoding="utf-8")
    print(f"patched {path.name}")
