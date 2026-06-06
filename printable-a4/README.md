# Printable A4 Portrait Versions

Open these HTML files in a browser and print to PDF using **A4 Portrait**.

This version uses a more integrated tabletop-book layout:

- parchment-style page backgrounds and framed artwork
- all standalone artwork and scene plates are page-scale rather than small horizontal boxes
- each player race gets a full-page A4 feature plate
- each player class gets a full-page A4 feature plate
- race/class artwork uses `object-fit: contain` so the portrait is preserved rather than cropped inside a small box
- each feature page has one grouped text overlay panel, preventing text-box overlap
- text overlay panels alternate left, right, and bottom placements so they do not always cover the same part of the art
- class abilities/spells are layered inside the class overlay panel
- bestiary entries use full-page layered creature artwork with stat/solution text overlaid
- `break-inside: avoid` / `page-break-inside: avoid` rules on plates, tables, callouts, and cards to prevent artwork from splitting across pages in print preview

Files:

- `player-handbook-a4.html`
- `dungeon-master-guide-a4.html`
- `bestiary-a4.html`
- `example-campaigns-a4.html`
- `combined-book-a4.html`
