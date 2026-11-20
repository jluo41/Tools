# haipipe-studio · Constitution

JL's feedback on Studio topics, kept verbatim. It wins over SKILL.md and its rendered sections; where they
disagree, follow this file. Written and checked through `/haistack`.


## A01 · A topic about real work is a manual too

> "make the studio like a things like manual to show how things work. we can help people to understand what is the progress/" (JL 261118, a note-sync setup)

**Rule:** When an sNN is about real, running work (a setup, a service, a pipeline), its drawing is a manual: Design A shows how the thing works, step by step, with the real names; and the topic shows where the work stands.
**Why:** The First principle ("a Studio is never a report") left no place for progress, so the LiveSync topic showed how it works but not how far the setup had got.
**Check:** Design A names the real parts (containers, URLs, databases, files); the topic carries a progress list (`spec["progress"]`).
**Class:** a Studio about running work explains the work but leaves its state out
**Cases:** ✅ b01_livesync s01 (A7) · ⬜ other Studio topics about a service or setup, not yet audited
**Run:** `grep -q 'sync.example.test' ../NOTES-SPACE/examples-notes/Project-Notes-Sync/work/b01_livesync/s01-how-livesync-works/s01-how-livesync-works.excalidraw && grep -q 'notes_vault' ../NOTES-SPACE/examples-notes/Project-Notes-Sync/work/b01_livesync/s01-how-livesync-works/s01-how-livesync-works.excalidraw && grep -q 'progress, live' ../NOTES-SPACE/examples-notes/Project-Notes-Sync/work/b01_livesync/s01-how-livesync-works/s01-how-livesync-works.excalidraw`
**Report:** constitution/A01-manual-for-real-work.md
**Status:** solved 261118
**Solved by:** `examples-notes/Project-Notes-Sync/work/b01_livesync/s01-how-livesync-works/`: manual plus 10 progress steps


## A02 · Progress is seen on the card, without opening the drawing

> "What I mean is the haipipe-studio things, so that we want to make it work as we expected so when we reading the studio, we know the progress/" (JL 261118)
> "current the studio is not valid" (JL 261118, when the progress sat only inside Design B)

**Rule:** A topic with progress passes it as `spec["progress"]` = [(mark, words)], and `five_parts.now` draws it at the top of 2 Now, so the card preview (Idea and Now only) shows it; ✅ done, 🔶 running or stuck, ⬜ not yet.
**Why:** The card crops to the first 1350 x 820 of the canvas; progress drawn in Design B was invisible on the Studio row until Open Draw.
**Check:** rebuild the topic, open `<topic>.png`: the Now part lists every step with its mark; `/wb <Block>` Studio card shows the same.
**Class:** the card preview crops to Idea and Now, so anything drawn later is unseen on the Studio row
**Cases:** ✅ five_parts.now draws spec["progress"] (every five-part topic) · ✅ b01_livesync s01 · ⬜ draw.py topics (no Now part)
**Run:** `grep -q 'spec.get("progress")' plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/five_parts.py && grep -q 'setup progress, live' ../NOTES-SPACE/examples-notes/Project-Notes-Sync/work/b01_livesync/s01-how-livesync-works/s01-how-livesync-works.excalidraw`
**Report:** constitution/A02-progress-on-the-card.md
**Status:** solved 261118
**Solved by:** `scripts/five_parts.py`: `now()` draws `spec["progress"]` when given


## A03 · Progress is read live, never typed in

> "please make the report to be as helpful as possible?" (JL 261118)

**Rule:** Each progress step that a machine can check is read from the real thing on every rebuild (a container's state, a URL's HTTP code, a database count, a file's presence), with the time it was read; only steps no machine can see are typed, and secrets are read from their `.env`, never drawn.
**Why:** The first LiveSync drawing said "0 docs, stuck" by hand; minutes later the upload ran and the drawing was wrong.
**Check:** rebuild twice a minute apart while the work moves: the numbers and the "live <time>" change; `grep PASSWORD <topic>.excalidraw` finds nothing.
**Class:** a number typed into a drawing goes stale, and a secret read to draw it can leak into the canvas
**Cases:** ✅ b01_livesync s01 probe() · ⬜ Job results topics (job_results.py reads disk already, not audited)
**Run:** `! grep -rIil --include='*.excalidraw' password ../NOTES-SPACE/examples-notes/Project-Notes-Sync && grep -q 'live 26' ../NOTES-SPACE/examples-notes/Project-Notes-Sync/work/b01_livesync/s01-how-livesync-works/s01-how-livesync-works.excalidraw`
**Report:** constitution/A03-progress-read-live.md
**Status:** solved 261118
**Solved by:** `s01-how-livesync-works/sketch_how_livesync_works.py`: `probe()` and `steps()` feed B and Now


## A04 · Design is drawn as pictures, never as small tables and long stickies

> "this is not vidid, should update this this again>" (JL 261118, a screenshot of s01's whole canvas)
> "have you check the constintution that we want to make the vivid diagram??? /haistack to related skills to update the workflow." (JL 261119, after s04-upload-path got a third plan as boxes and text)
> "why you missed this again??" (JL 261119)

**Rule:** Design leads with pictures of the real things (a computer, a database, a cloud, a phone), each lit by its live state, and big numbers (a count, a score like 8/10); tables only for real data rows; a sticky holds two short lines, at most 14 characters each. Read this file before any edit to a Studio drawing, even adding one node.
**Why:** 261118: s01's Design A was four tiny tables and B ten stickies. 261119: s04 (b11 j02) was edited with plan 3 and Sudip's email as more boxes and text; the agent went straight to sketch_path.py without opening this file, nothing in the builder warned, and the icons lived only inside s01's own sketch.
**Class:** a Design made of small text boxes and tables reads as a form, not a picture; and an agent reaches the drawing without passing this file
**Cases:** ✅ b01_livesync s01 A, B, C · ✅ b11 j02 s04-upload-path A, B (261119) · ✅ writer: `five_parts.build` warns under 20 picture shapes · ✅ writer: `templates/sketch.py.tmpl` starts A from icons · ✅ shared `scripts/icons.py` · ✅ door: `excalidraw/SKILL.md` and `excalidraw-studio/SKILL.md` point here · ⬜ older five-part topics drawn as tables: they now print ❗ A04 on their next rebuild, each fixed then
**Check:** the rendered canvas shows icons and a big number in Design; the builder prints no ❗ A04; check.py passes
**Run:** `python3 -c "import json,sys;f=['../NOTES-SPACE/examples-notes/Project-Notes-Sync/work/b01_livesync/s01-how-livesync-works/s01-how-livesync-works.excalidraw','../OTHER-SPACE/examples-0-cowork/Project-Example/cowork/b11_account/j02_access/s04-upload-path/s04-upload-path.excalidraw'];sys.exit(any(sum(x['type'] in ('ellipse','line') for x in json.load(open(p))['elements'])<20 for p in f))" && grep -q '❗ A04' plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/five_parts.py && grep -q 'from icons import' plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/templates/sketch.py.tmpl && grep -q 'haipipe-studio/CONSTITUTION.md' plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw/SKILL.md && grep -q 'haipipe-studio/CONSTITUTION.md' plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-studio/SKILL.md`
**Report:** constitution/A04-design-as-pictures.md
**Status:** solved 261119 (reopened 261119, first solved 261118)
**Solved by:** `scripts/icons.py`: shared icons; `scripts/five_parts.py`: ❗ A04 warning; `templates/sketch.py.tmpl`: A from icons; excalidraw doors point here
