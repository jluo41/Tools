# hai-studio · Constitution

JL's feedback on Studio topics, kept verbatim. It wins over SKILL.md and its rendered sections; where they
disagree, follow this file. Written and checked through `/hai-stack`.


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

> "What I mean is the hai-studio things, so that we want to make it work as we expected so when we reading the studio, we know the progress/" (JL 261118)
> "current the studio is not valid" (JL 261118, when the progress sat only inside Design B)

**Rule:** A topic with progress passes it as `spec["progress"]` = [(mark, words)], and `five_parts.now` draws it at the top of 2 Now, so the card preview (Idea and Now only) shows it; ✅ done, 🔶 running or stuck, ⬜ not yet.
**Why:** The card crops to the first 1350 x 820 of the canvas; progress drawn in Design B was invisible on the Studio row until Open Draw.
**Check:** rebuild the topic, open `<topic>.png`: the Now part lists every step with its mark; `/wb <Block>` Studio card shows the same.
**Class:** the card preview crops to Idea and Now, so anything drawn later is unseen on the Studio row
**Cases:** ✅ five_parts.now draws spec["progress"] (every five-part topic) · ✅ b01_livesync s01 · ⬜ draw.py topics (no Now part)
**Run:** `grep -q 'spec.get("progress")' plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/five_parts.py && grep -q 'setup progress, live' ../NOTES-SPACE/examples-notes/Project-Notes-Sync/work/b01_livesync/s01-how-livesync-works/s01-how-livesync-works.excalidraw`
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
> "have you check the constintution that we want to make the vivid diagram??? /hai-stack to related skills to update the workflow." (JL 261119, after s04-upload-path got a third plan as boxes and text)
> "why you missed this again??" (JL 261119)

**Rule:** Design leads with pictures of the real things (a computer, a database, a cloud, a phone), each lit by its live state, and big numbers (a count, a score like 8/10); tables only for real data rows; a sticky holds two short lines, at most 14 characters each. Read this file before any edit to a Studio drawing, even adding one node.
**Why:** 261118: s01's Design A was four tiny tables and B ten stickies. 261119: s04 (b11 j02) was edited with plan 3 and Sudip's email as more boxes and text; the agent went straight to sketch_path.py without opening this file, nothing in the builder warned, and the icons lived only inside s01's own sketch.
**Class:** a Design made of small text boxes and tables reads as a form, not a picture; and an agent reaches the drawing without passing this file
**Cases:** ✅ b01_livesync s01 A, B, C · ✅ b11 j02 s04-upload-path A, B (261119) · ✅ writer: `five_parts.build` warns under 20 picture shapes · ✅ writer: `templates/sketch.py.tmpl` starts A from icons · ✅ shared `scripts/icons.py` · ✅ door: `hai-draw/SKILL.md` points here · ⬜ older five-part topics drawn as tables: they now print ❗ A04 on their next rebuild, each fixed then
**Check:** the rendered canvas shows icons and a big number in Design; the builder prints no ❗ A04; check.py passes
**Run:** `python3 -c "import json,sys;f=['../NOTES-SPACE/examples-notes/Project-Notes-Sync/work/b01_livesync/s01-how-livesync-works/s01-how-livesync-works.excalidraw','../OTHER-SPACE/examples-0-cowork/Project-Example/cowork/b11_account/j02_access/s04-upload-path/s04-upload-path.excalidraw'];sys.exit(any(sum(x['type'] in ('ellipse','line') for x in json.load(open(p))['elements'])<20 for p in f))" && grep -q '❗ A04' plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/five_parts.py && grep -q 'from icons import' plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/templates/sketch.py.tmpl && grep -q 'hai-studio/CONSTITUTION.md' plugins/haipipe-toolkit/skills/1_base/draw/hai-draw/SKILL.md && grep -q 'hai-studio/CONSTITUTION.md' plugins/haipipe-toolkit/skills/1_base/draw/hai-draw/SKILL.md`
**Report:** constitution/A04-design-as-pictures.md
**Status:** solved 261119 (reopened 261119, first solved 261118)
**Solved by:** `scripts/icons.py`: shared icons; `scripts/five_parts.py`: ❗ A04 warning; `templates/sketch.py.tmpl`: A from icons; the hai-draw door points here

## A05 · A topic's title names its band first

> "so what is this type of studio? could you tell me? Block Structure? Could you make it like Block Structure: Blueprint, so we know what type of this studio" (JL 261127, b17 Studio)
> "I told you to udpate the name: ... to be: Block Structure: Work ... to be: Block Job UI Preview: Work, etc." (JL 261127)

**Rule:** In a Block whose face names its Studio bands, every topic sits in a named band and its title reads `sNN · <band name>: <which one>`.
**Why:** b17's topics read "Work Block (Blueprint) Structure", "Work Job UI preview": a reader could not tell their kind at a glance, nor which topics belong together.
**Class:** a topic's title does not say what kind of topic it is; any Block, any band, any writer (new_topic.py, a hand-written face, a renumber).
**Cases:** ✅ b17 (15 topics) · ✅ new_topic.py writes the band name · ⬜ b11, b12, b15, b16 (their sessions rename theirs)
**Check:** every topic of a Block with named Studio bands is in a named band, its title starting with that band's name.
**Run:** `python3 plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/topic_titles_check.py examples`
**Status:** open
**Solved by:** `scripts/new_topic.py`: band name before the title; `scripts/topic_titles_check.py`: the check

## A06 · Studio types specify content; bands group topics

**Rule:** A Studio Type specifies its instances' top views and left tabs. Its right side states the requirement
for each element; an instance's right side shows the real content. A Band groups topics and does not require a
same-named Studio Type. Work Blocks (Blueprint) share the ordered `studio-bands.json` registry, reference common type
definitions and author only their own additional types. Actual Work Blocks show their topics without requiring
a Studio Type group. Empty groups are omitted. Task methods belong to the Task type and owning skill; general
page usage belongs to `workbench` and theme guidance to Theme Guide. Topic folders and identifiers are preserved.

A type's right-side requirement may include its corresponding expandable example,
bound by name to an existing instance view item, without copying the instance's content.
These examples stay beside their requirements; they do not add a separate Examples top view.
Check is a final top view; element-scoped left items identify `Top › Left`, and the
right side includes both the selected element's and its parent view's requirements,
verification methods and source. An example or generated Check card is not a passed
check. See `ref/type-examples.md` and `ref/check-view.md`.

**Check:** Page rendering, topic creation and structure diagrams read the same registry. Removing a type definition
does not remove a populated Band. Type requirements come from `elements.md` and are rendered without copying
an instance's content. A Blueprint's local bands cannot rename the shared groups.
**Run:** `PYTHONPATH=plugins/haipipe-toolkit/servers/_host ~/.cache/haipipe/host-venv/bin/python -m unittest discover -s plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests -p test_studio_bands.py`
**Run:** `~/.cache/haipipe/host-venv/bin/python -m unittest discover -s plugins/haipipe-toolkit/skills/1_base/project/hai-studio/tests -p test_studio_bands.py`


## A07 · A name that is not fixed is written in 〈 〉

> "for the things we are not sure, we use < xxxx> to replace this ... like this, please update the AGENTS.md" (JL 261127, s71's Job types tabs)
> "update the AGETNS.md so everyone will follow it, and Ithink you should also add this to the /hai-studio" (JL 261127)

**Rule:** A slot each instance fills in, or a thing not decided yet, reads `〈Job type 1〉`, `〈quick page 2〉`, `bNN_〈block〉/`; a real, agreed name carries no brackets (AGENTS.md "Page words").
**Why:** s71's tabs read "Task group type 1", "Task type 2": bare words that look like real names, so a reader could not tell a placeholder from a decision.
**Class:** a placeholder shown as if it were settled; tabs, view buttons, tree rows and file patterns of every Studio Type topic and of any topic that shows a slot.
**Cases:** ✅ s71 Block Structure (eight type slots, the example slot) · ✅ the folder patterns (`bNN_〈block〉/`) · ⬜ s72-s79 as their sessions write them · ⬜ a proposed name not yet agreed (Work's group types) is a judgement, not machine-checked
**Check:** no tab or view of a Studio Type topic is a bare numbered slot name.
**Run:** `python3 plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/placeholder_check.py examples`
**Status:** open
**Solved by:** `AGENTS.md`: the rule; `scripts/placeholder_check.py`: the check


## A08 · A Skills topic: the skills on top, a skill's whole top level on the left, a folder as folds

> "I think the top will just be the related skills? and in the left, is showing the skill content? like the first one will be the SKILL.md, but you will also have other things, right?" (JL 261127)
> "if it is a folder, in the right content, could we make the right content to have the fold, and content as well?" (JL 261127)
> "for things here, it should be more, right? should we add <other>, etc." (JL 261127, on a left that showed only SKILL, Rules, ref, scripts)
> "I think in the left, the left tab should be the same as the file names, or folder names" (JL 261127, on tabs named SKILL, Rules, other)

**Rule:** A Skills topic covers one work kind, a related group of level skills, or a shared capability. These are content relationships within the Skills band, not additional UI groups. Its top buttons are its actual skills. A shared skill may appear in several topics, always reading the same source path. A skill's left tabs are its whole top level, each named as the file or folder is on disk, in one order: `SKILL.md`, `CONSTITUTION.md`, `ref/`, `scripts/`, its other folders (with their slash), then its loose files. No alias (Rules, other). A tab that is a folder shows one fold per file on the right, closed; an opened fold is the file itself. A topic that has its own drawing shows it as a last top button, Draw.
**Why:** The first layout put file kinds on top (SKILL, Rules, Refs, Scripts) and skills on the left, so reading one skill took four buttons; the next listed every file on the left (44 tabs for one skill); the next showed four tabs and hid a skill's other folders and loose files; the next named tabs Rules and other, words that are on no disk.
**Class:** a list of a skill's files that is not the skill's own top level; every Skills topic (s5N and s6N in a Work Block (Blueprint)), every blueprint Block, the type s76.
**Cases:** ✅ b17 s51 Work · ✅ s52 Blueprint · ✅ s53 CoWork · ✅ s54 Discovery · ✅ s60 Studio · ✅ s61 Trace · ✅ s62 Project · ✅ s55 Knowledge · ✅ s76 the type
**Check:** each Skills topic's studio-views.json is what `skills_views.py` writes from its skills' folders today.
**Guard:** `scripts/checks/run.py --target 〈topic-or-Block〉` checks real bindings and generator freshness through the existing owners; the Skills writer checks its completed output. Check-view freshness does not certify its prose criteria or runtime UI behavior. Invalid or uncovered targets never pass.
**Run:** `PYTHONPATH=plugins/haipipe-toolkit/servers/_host ~/.cache/haipipe/host-venv/bin/python plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/skills/scripts/skills_views.py examples/Project-Ladder/blueprint/b17_theme_work --check`
**Status:** fixed
**Run:** `PYTHONPATH=plugins/haipipe-toolkit/servers/_host ~/.cache/haipipe/host-venv/bin/python plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/skills/scripts/skills_checklist.py examples/Project-Ladder/blueprint/b17_theme_work --check` (each topic against s76, part by part; the result shows in the Block's Checklist)
**Solved by:** `scripts/skills_views.py` (writes and checks the views file), `scripts/skills_checklist.py` (each topic against its type), `gallery/skills/TYPE.md`, `servers/workbench/studio/tabs/folder_folds.py` (a folder as folds)


## A09 · A skill's text states the rule, never who asked for it

> "<!-- render b35-s01 how-many: generated from ... --> what is this? JL 261029: \"studio 一定要切记 ...\" <--- what is this? they are not good enough?" (JL 261127, reading SKILL.md in s60)
> "no, remove them. make them as clean as possible, clean, easy to follow, and tell them what to check." (JL 261127)
> "In the skill.md, never show the annotation, or things like (JL 261112: \"this is not vivid, I want the vivid ones\")" (JL 261127)
> "I am not sure why this is related to hai-studio??" (JL 261127, on ref/topic-scripts.md: three stale rows)

**Rule:** SKILL.md and the ref files say what to do and what to check, in plain steps. No who-and-when note, no quoted request, no decision id as a source, no marker comment line. The words that made a rule stay here, in CONSTITUTION.md, and in code comments. SKILL.md is a short entry: the Studio Type first, then the topic, the commands, what to check, which ref to read; every file it names is on disk, and every ref file and script is named in it.
**Why:** SKILL.md had grown to 591 lines with 41 who-and-when notes and 6 render marker lines, which the Skills topic showed as text; it named files in a way that hid 9 of its scripts; two of its five generated regions had drifted from their source.
**Class:** skill text that records its own history where a reader needs the rule; hai-studio's SKILL.md and ref/, shown live by b17 s60; any skill a Skills topic shows.
**Cases:** ✅ SKILL.md (591 lines to about 190) · ✅ ref/ (3 new, 9 cleaned, 2 stale ones deleted) · ⬜ ref/gallery.md (generated with marker lines by gallery_scan.py and b35 s05's render; skipped by the check) · ⬜ the other skills
**Check:** the skill's SKILL.md and ref files carry no such note or marker and name exactly what is on disk.
**Run:** `python3 plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/skill_text_check.py`
**Status:** fixed
**Solved by:** `scripts/skill_text_check.py`; the long sections moved to `ref/topic-delivery.md`, `ref/studio-section.md`, `ref/job-results.md`, `ref/topic-look.md`, `ref/topic-builder.md`

## A10 · A topic is started from its type and held to it

> "why no studio is following their studio type???" (JL 261127, s60 lacked the Draw button its type s76 had)
> "with the new studio type, to use hai-studio to create that studio type, how to make it really follow it?" (JL 261127)

**Rule:** A topic that names a Studio Type has that type's top buttons and left tabs, no fewer and no more. It is started from the type (`type_follow.py new`), and held to it by a check that reads only the type's `elements.md`, so it works for a type written later. A part the type gives a `when:` line may be absent; a name in 〈 〉 stands for zero or more real names.
**Why:** A topic's buttons were written once; when the type changed nothing said the topic was behind. The Check button lists criteria and compares nothing.
**Class:** an instance that drifts from its class with no check between them; every topic that names a type, in every Block.
**Cases:** ✅ b17 s51 to s54, s60, s61 (Skills) · ✅ s11 · ⬜ s01 to s04 (differ from s71) · ⬜ s12 to s15 (parts not filled in) · ⬜ s05, s55, s62 (name no type)
**Check:** every topic that names a type passes the follow check.
**Run:** `~/.cache/haipipe/host-venv/bin/python plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/type_follow.py check examples/Project-Ladder/blueprint/b17_theme_work`
**Status:** open
**Solved by:** `scripts/type_follow.py`; `scripts/checks/follow.py`

## A11 · Inside a topic every view is top, left, right

> "I think for the hai-studio, we by default what to have the top-left-right format, for the page" (JL 261127, a Page view that showed one long learning.md)

**Rule:** In a topic the kinds of thing are buttons on top, the parts of the picked one are tabs on the left, one part is on the right. A view's one Markdown file with two or more `##` sections gets a left tab per section, made by the page; nothing is copied into part files. Only a thing with one part is shown full width.
**Why:** A long file shown whole is a wall to scroll; the reader cannot see what it holds before reading it.
**Class:** a view that shows one long document full width; every topic, with or without its own views file.
**Cases:** ✅ a view with one Markdown file (`md_sections.py`) · ⬜ a view with several Markdown files keeps each whole
**Check:** a view whose one item is a Markdown file with two or more sections shows a left tab per section.
**Run:** `cd plugins/haipipe-toolkit && PYTHONPATH=servers/_host uv run --quiet --python 3.13 --with pytest --with pyyaml --with pillow python -m pytest servers/workbench/studio/tabs/tests/test_md_sections.py -q -p no:cacheprovider`
**Status:** solved 261127
**Solved by:** `servers/workbench/studio/tabs/md_sections.py`; `studio_views.read_views`

## A12 · A blueprint Block designs a type; the skill keeps it; a topic names it

> "could you explain where to find its type? from the hai-studio or from where? from the blueprint-block? I think blueprint-block is working to provide the types into the hai-studio" (JL 261127)

**Rule:** A Studio Type is designed in a blueprint Block's Studio Type band and delivered into `hai-studio/gallery/<name>/elements.md`. A topic names its type by that name, never by the type topic's number or path. A kept type is never edited; the blueprint is changed and delivered again.
**Why:** Types lived only in one blueprint Block and topics pointed at its path: a Block in another SPACE could not use a type, and renumbering a type topic (the Skills type went from 76 to 75 in one day) broke every pointer.
**Class:** a class that only its own workshop can reach; every type, every blueprint Block, every SPACE that installs the skill.
**Cases:** ✅ seven b17 types delivered · ✅ b17 Skills and Block Structure topics name `skills`, `block-structure` · ⬜ b17 s11 to s15 and their type still use a path (their own builder writes it) · ⬜ the other themes' blueprints deliver no type yet
**Check:** every blueprint type with an `elements.md` has the same file under `gallery/`, and no kept type is without a blueprint.
**Run:** `uv run --quiet --python 3.13 --with pyyaml python plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/types_deliver.py --check`
**Status:** open
**Solved by:** `scripts/types_deliver.py`; `servers/workbench/studio/tabs/studio_types.type_home`

## A13 · A Skill topic shows how good its skills are

> "we can also add the top view named Evaluation and check the quality of this skill, right?" (JL 261127, on the Skills type)

**Rule:** Every Skill topic has a top button Evaluation after its skills, one item per skill: the skill measured from its own files on every open, each criterion with its own mark and what was found. No score and no tally. What no file can show is listed as a person's call, never as passed.
**Why:** A Skill topic showed a skill's files and nothing about whether the skill is sound; its weak points were found only when an agent tripped on them.
**Class:** a thing shown without its quality; every Skill topic of every blueprint Block.
**Cases:** ✅ b17 s51 to s55, s60 to s63 · ✅ the Skills type
**Check:** each Skill topic's views file has an Evaluation view with one live item per skill.
**Run:** `~/.cache/haipipe/host-venv/bin/python plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/skills/scripts/skills_views.py examples/Project-Ladder/blueprint/b17_theme_work --check`
**Status:** solved 261127
**Solved by:** `servers/workbench/studio/tabs/skill_evaluation.py`; `gallery/skills/scripts/skills_views.py`

## A14 · Everything of one Studio Type is in its gallery folder

> "for the hai-studio, for each studio type, will we have a gallery to store it?" (JL 261127) · "okay, I agree, please think about it and update it accoridngly" (JL 261127)

**Rule:** `gallery/<name>/` holds everything of one Studio Type: its delivered `elements.md`, a `TYPE.md` that says how a topic of the type is built, the scripts that write and check one, their tests, and one real example. A script that serves every type stays in `scripts/`. Adding a type adds a folder and touches nothing else.
**Why:** A type's definition, its scripts and its reference sat in three folders, mixed with other types'; to build a Skills topic an agent looked in three places, and a new type put a piece in each.
**Class:** the parts of one thing spread by kind of file instead of kept together; every Studio Type.
**Cases:** ✅ skills · ✅ block-structure · ✅ block-job-ui-preview (TYPE.md; its builder lives in the type topic) · ⬜ resources, methods, applications, questions (elements.md only, no example yet)
**Check:** a type with scripts has a TYPE.md that names each of them; SKILL.md names `gallery/`.
**Run:** `python3 plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/skill_text_check.py`
**Status:** open
**Solved by:** `gallery/`; `scripts/skill_text_check.py`
