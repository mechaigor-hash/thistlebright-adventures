#!/usr/bin/env python3
"""Repair combined A4 profile section if it was built from an older HTML snapshot."""
from pathlib import Path
import re

path = Path('/home/mecha-igor/prepped/scottish-fairy-quest/printable-a4/combined-book-a4.html')
text = path.read_text(encoding='utf-8')

race_src = {
 'Human Glenfolk':'../art/generated/26-race-human-glenfolk.png',
 'Fairy-Touched':'../art/generated/27-race-fairy-touched.png',
 'Brownie-Kin':'../art/generated/28-race-brownie-kin.png',
 'Selkie-Born':'../art/generated/29-race-selkie-born.png',
 'Rowan-Kin':'../art/generated/30-race-rowan-kin.png',
 'Dragon-Friend':'../art/generated/31-race-dragon-friend.png',
}
class_src = {
 'Thistle Knight':'../art/generated/32-class-thistle-knight.png',
 'Glen Wizard':'../art/generated/33-class-glen-wizard.png',
 'Loch Scout':'../art/generated/34-class-loch-scout.png',
 'Hearth Bard':'../art/generated/35-class-hearth-bard.png',
 'Fairy Friend':'../art/generated/36-class-fairy-friend.png',
}
spells = {
 'Thistle Knight':['<li><strong>Shield of Thistles:</strong> Give a friend +1 when you protect them.</li>','<li><strong>Brave Step:</strong> Cross one scary-but-safe obstacle first so friends feel better.</li>','<li><strong>Kind Challenge:</strong> Ask a grumpy creature for a fair contest instead of a fight.</li>','<li><strong>Lantern Guard:</strong> Spend a charm to make a scene gentler for everyone.</li>'],
 'Glen Wizard':['<li><strong>Glowbug Light:</strong> Make a soft light that shows clues.</li>','<li><strong>Pebble Ping:</strong> Your wand gently points toward nearby magic.</li>','<li><strong>Rhyme Reminder:</strong> Say a silly rhyme to remember an old fairy rule.</li>','<li><strong>Sparkle Signal:</strong> Spend a charm to send a safe sparkle message to a friend.</li>'],
 'Loch Scout':['<li><strong>Ribbon Map:</strong> Ask one question about where a path goes.</li>','<li><strong>Quiet Boots:</strong> Move gently without startling a creature.</li>','<li><strong>Stepping-Stone Hop:</strong> Give yourself +1 when balancing, climbing, or crossing.</li>','<li><strong>Trail Friend:</strong> Spend a charm to help the whole group follow you safely.</li>'],
 'Hearth Bard':['<li><strong>Ceilidh Beat:</strong> Start a rhythm that helps everyone move together.</li>','<li><strong>Giggle Verse:</strong> Turn one grumpy sentence into a silly one.</li>','<li><strong>Warm Welcome:</strong> Give a shy NPC a reason to talk.</li>','<li><strong>Encore Help:</strong> Spend a charm to let a friend reroll after you cheer them on.</li>'],
 'Fairy Friend':['<li><strong>Acorn Cup:</strong> Offer a tiny gift and ask for fairy hospitality.</li>','<li><strong>Heather Hello:</strong> Flowers wave toward a friendly creature.</li>','<li><strong>Polite Promise:</strong> Make a simple promise that opens a fairy door or path.</li>','<li><strong>Mushroom Messenger:</strong> Spend a charm to ask a mushroom, beetle, or breeze for help.</li>'],
}

def wrap_first_block(text, name, src, cls, spell_items=None):
    # Skip only if THIS exact portrait is already inside a profile/class card.
    if src in text and f'alt="{name}"' in text:
        return text, False
    pat = re.compile(rf'(<h4>{re.escape(name)}</h4>\s*)(<p>.*?</p>\s*)(<ul>.*?</ul>)', re.S)
    spell_html = ''
    if spell_items:
        spell_html = '<div class="spell-block"><p class="spell-title">Abilities / spells</p><ul>' + ''.join(spell_items) + '</ul></div>\n'
    replacement = f'<section class="{cls}">\n<img src="{src}" alt="{name}">\n\\1\\2\\3\n{spell_html}</section>'
    new_text, n = pat.subn(replacement, text, count=1)
    return new_text, bool(n)

changed = 0
for n,s in race_src.items():
    text, did = wrap_first_block(text, n, s, 'profile-card race-card')
    changed += did
for n,s in class_src.items():
    text, did = wrap_first_block(text, n, s, 'class-card', spells[n])
    changed += did
path.write_text(text, encoding='utf-8')
print('changed_blocks', changed)
