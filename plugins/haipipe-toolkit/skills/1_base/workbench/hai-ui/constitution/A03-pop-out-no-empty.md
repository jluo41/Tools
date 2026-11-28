# A03 · What waits on you pops out; an empty section is not drawn

> "if there are things for me to make decision, could they just pop out?" (JL 261114)

## 1. Need
What needs JL shows beside the item it is about, and gathers in the 🙋 tray; nothing else asks for his eyes.

## 2. Now
The 261118 scan read 300 pages and found 54 "Nothing handed over yet" lines plus "Nothing asked yet" on servers
still running the code from before the fix (5607, 5623, 5640, 5697, 5698, 5699).

## 3. Gap
- The empty Delivery text was written in four places (focus_render, focus_delivery, work_frame, focus_studio);
  fixing one left the others.
- Servers run the code they started with, so a fix is not live until each one restarts.

## 4. Methods
1. Fix the line JL saw: leaves the other three writers; rejected.
2. Remove every empty-state writer, test each, and scan every running page: chosen.

## 5. Update
- `servers/workbench/page/block_index_page/focus_render.py`, `focus_delivery.py`, `work_frame.py`, `focus_studio.py`: empty draws nothing
- `servers/workbench/page/*/tests/test_focus_*.py`: assert the words are gone
- `hai-ui/scripts/page_words.py`: catches any "nothing … yet" left
Cases: ✅ the four writers · ⬜ servers not yet restarted · ⬜ "Nothing asked yet".

## 6. Never again
- Tests fail if a writer brings the text back; `/hai-stack sweep` scans every running page.
- Still open: a restart of each SPACE's server; until then the scan stays ❗ on purpose.
