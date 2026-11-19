# haipipe-ui · Constitution

JL's feedback on what workbench pages show, kept verbatim. It wins over SKILL.md and over any page code; where they
disagree, follow this file. Written and checked through `/haistack`. Page code lives in `servers/`, but its rules
live here: every session that changes a page reads this file first (root AGENTS.md § Page words).


## A01 · State shows by marks and layout, never by words or tallies

> "we don't want this, drop them" (JL 261113, on "Status:" sentences and "N of M" pills)
> "just like the layout and UI tell it" (JL 261113)

**Rule:** A page never says an item's state in words ("Status: running", "not signed yet") or shows a tally ("6 to fix", "3 of 7 written"); an emoji mark, a group, a fold or a button shows it.
**Why:** Pages carried "Status:" lines, "N of M" progress pills and check tallies that JL had to read and re-read.
**Class:** a state or count written as text in page code or in what page code renders.
**Cases:** ✅ shared section bars (`ui_parts.word_span`) · ⬜ Project faces rendered as text (WellDoc Proj13 "Status : Planning phase") · ⬜ Paper delivery line ("status: ready") · ⬜ every theme, every running SPACE (scanner)
**Check:** no visible "Status:"/"State:" sentence or "N of M <thing>" tally on any page a running server serves.
**Run:** `python3 plugins/haipipe-toolkit/skills/1_base/workbench/haipipe-ui/scripts/page_words.py --running --max 30`
**Status:** open
**Solved by:** `scripts/page_words.py`: reads every running workbench's visible text
**Report:** constitution/A01-state-by-marks.md


## A02 · No "JL 26xxxx" tags on a page

> "do not add the things like this in the UI, totally avoid this" (JL 261113, on a "JL 261113" tag in the Revise card)

**Rule:** No label, tooltip, button, banner or note a page shows carries a who-asked-when tag ("JL 261113", "(JL 261020: …)"); those live in code comments, commits and docs.
**Why:** Design tags written into code strings leaked onto pages.
**Class:** provenance text inside a string the page renders.
**Cases:** ⬜ Studio topic subtitles from faces ("(JL 261030)", Physician 5599, 5699) · ⬜ commit messages shown as Timeline data (allowed: content as written) · ⬜ every running SPACE (scanner)
**Check:** no visible `JL 2xxxxx` outside content a person wrote.
**Run:** `python3 plugins/haipipe-toolkit/skills/1_base/workbench/haipipe-ui/scripts/page_words.py --running --max 30`
**Status:** open
**Solved by:** `scripts/page_words.py`: flags every visible tag for triage
**Report:** constitution/A02-no-provenance-tags.md


## A03 · What waits on you pops out; an empty section is not drawn

> "if there are things for me to make decision, could they just pop out?" (JL 261114, pointing at Draft Lab)

**Rule:** What waits on the reader shows as a mark beside the item and in the 🙋 tray; a section bar carries only 🙋 N, ✓ or nothing; a section with nothing in it is not drawn, and no "nothing yet" text stands in for it.
**Why:** Pages drew empty Interaction and Delivery sections with "Nothing handed over yet" and "nothing yet" words.
**Class:** an empty-state sentence where nothing should be drawn.
**Cases:** ✅ focus_render, focus_delivery, work_frame, focus_studio (Tools 261118) · ⬜ servers not restarted since (5607, 5623, 5640, 5697, 5698, 5699) · ⬜ "Nothing asked yet" on one page
**Check:** no visible "nothing … yet" or "No subfolders." on any running page.
**Run:** `python3 plugins/haipipe-toolkit/skills/1_base/workbench/haipipe-ui/scripts/page_words.py --running --max 30`
**Status:** open
**Solved by:** `servers/workbench/page/focus_render.py` and three more: empty draws nothing
**Report:** constitution/A03-pop-out-no-empty.md


## A04 · Every link to a page lands on the focus page, never the old tabbed frame

> "the fucking old style" (JL 261118, opening http://<host>:5607/w/b12_reach_dataset_setup; relayed by Proj-JHU-REACH)

**Rule:** `/w/<block>`, `/b/<block>` and any bare `/_board/workbench?path=…` address open the focus page (`layout=focus`); the old tabbed frame opens only on an explicit `layout=frame` or its own tab, sub, view or format keys.
**Why:** `home_boards.frame_url` built the short route without `layout=focus`, and `frame_view` drew the old frame for every address that did not say focus.
**Class:** an address that reaches the retired frame by default.
**Cases:** ✅ `/w/<block>` and `/b/<block>` (`frame_url`) · ✅ Block links on Home (`home_boards.py:302`) · ✅ any bare `?path=` link anywhere (`frame_view` default) · ✅ WellDoc 5602 checked live · ⬜ REACH 5607 and other servers until restarted
**Check:** the short route's URL carries `layout=focus`; a bare address renders the focus page; `layout=frame` still renders the old frame.
**Run:** `cd plugins/haipipe-toolkit/servers && uv run -q --python 3.13 --with pytest --with pyyaml python -m pytest -q _host/tests/test_workbench_short.py workbench/tests/test_focus_runs.py -k "route"`
**Status:** solved 261118
**Solved by:** `servers/workbench/home/home_boards.py`: `frame_url` adds layout=focus; `servers/workbench/page/frame_view.py`: bare address is focus
**Report:** constitution/A04-links-land-on-focus.md
