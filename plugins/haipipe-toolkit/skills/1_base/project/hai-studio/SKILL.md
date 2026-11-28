---
name: hai-studio
description: "Owns Studio topics at every level: their faces, sNN numbering, drawings and session passes; also the Page's Studio screen. Use to add or redraw a Studio topic, preview a drawing or save a session. Trigger: studio topic, studio tab, keep this session, /hai-studio, /workbench-studio."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.35.0"
  last_updated: "2026-11-27"
  # version history: ./CHANGELOG.md
---

# /hai-studio · the topics a Block owns

Read [CONSTITUTION.md](CONSTITUTION.md) first; it wins over this file.

A Studio topic is an `sNN-<topic>/` folder beside the Jobs or Tasks it serves: one open idea, drawn, that ends in one
delivery. This skill owns the folder, its face, its number, its builder, its rounds, and the Studio Types that say
what a topic of each kind must show.


## 1. Start with the Studio Type

Before adding or changing a topic, find its type. The type decides what the topic shows; nothing else in this file
comes before it. This file lists no types: each kind of Block keeps its own, as topics in its Studio Type band.

```text
the topic ─▶ names its type ─▶ the type's elements.md ─▶ what the topic must show
            studio-views.json    its top buttons and left tabs   the same top and left, the real thing on the right
```

1. **Find it**: the topic's `studio-views.json` names its type (`check_type`, the type topic's path). For a new
   topic, open the Block's page, Studio section, Studio Type band, and take the type its sibling topics name.
2. **Read it**: the type's `elements.md` lists every top button and left tab a topic of the type has, and for each:
   what it is, why, what it must show, where it comes from and how to check it.
3. **Same top and left, different right**: the type topic shows the requirement on its right side; your topic shows
   the real thing there. Add no button or tab the type does not list.
4. **Start from it, then hold to it**: `type_follow.py new <type topic> <topic>` gives a new topic the type's own
   buttons and tabs, each still showing its requirement; replace them one at a time with the real thing.
   `type_follow.py check <Block or topic>` says what differs from the type. This works for any type, also one
   written today.
5. **No type fits**: write the type first, in the same band, then the topic. How a type is written, and the four
   questions that give its top, left and right: [ref/studio-type.md](ref/studio-type.md).
6. **A name every topic fills in is written in 〈 〉** (`〈skill〉`, `bNN_〈block〉/`); a real, agreed name has no brackets.

Inside a topic every view reads the same way: the kinds of thing on top, the parts of the picked one on the left,
one part on the right. A view with one Markdown file gets a left tab per `##` section, made by the page; only a
thing with one part is shown full width (`ref/studio-section.md`).

A Block with no Studio Type band (an ordinary Work Block) follows sections 2 to 4 only. To change a type: edit its
`elements.md`, then run `type_requirements.py <type topic>`. A type whose topics a script writes has its own
reference: Skills topics [ref/skills-topic.md](ref/skills-topic.md), UI preview topics `ref/ui-preview-topic.md`.
Examples beside a requirement: [ref/type-examples.md](ref/type-examples.md). The Check button:
[ref/check-view.md](ref/check-view.md).


## 2. A Studio is never a report

A Studio is where an idea is still open. Report says what was found and how far the work is; the Studio shows what
we are still thinking.

1. **Ideas, not status**: the open question, its options side by side, which way we lean, what is unknown.
2. **Divergent**: two to four options, a "what if", a sketch; never one tidy list of what was done.
3. **Pictures first**: a drawing, a mind map, an illustrated slide; few words on each.
4. **No bookkeeping on screen**: decided, started, counts and dates belong in a round's record and in Report.
5. **When it settles, it leaves**: an agreed idea goes to its delivery; the Studio keeps the next open one.
6. **It must pull you in**: opened, it catches the eye in seconds: one clear focal point, a picture before words, a
   question the reader wants answered. A wall of text, a table of rows or a grid of equal boxes fails.

```text
Studio: "What is a Block?"  A topic │ B stage │ C promise to a reader (leaning) │ still open: …
Report: "Q01 answered: a Block is one delivery for one reader."
```


## 3. What a topic is

1. **Where it sits**: at the level that uses its delivery. A Block's topic beside its `jNN_` folders, a Job's beside
   its `tNN_` folders, a Task's beside `runs/`. There is no `studio/` folder.
2. **How many**: at most 9 at a Block, 5 at a Job, 3 at a Task, counting folders. More means the level is two.
3. **Its number**: one numbering for the whole Block; the next free number in its band; never reused.
4. **Its address**: `bNN.jNN-sNN`, always followed by its names: `b17-s04:theme_work @ workbench_page_structure`.
5. **One idea, one delivery**: its face names the delivery first (`**For:**`) and its type in one word
   (`**Delivery type:**`: skill, ui, code, draft, display or data). A mixed delivery is several topics.
6. **Two sides**: its drawing (`.excalidraw`) and its mind map (`.mindmap.md`, drawn and edited through
   [`../hai-mindmap/SKILL.md`](../hai-mindmap/SKILL.md)).

```text
<Block, Job or Task>/sNN-<topic>/
├── sNN-<topic>.md            the face: For, Delivery type, Covers, Topic, Feeds, Decided, Open
├── sNN-<topic>.excalidraw    the drawing (a builder's, with the person's marks kept)
├── sNN-<topic>.png           its preview
├── build_sNN_<topic>.py      the builder, when a script draws it
├── sNN-<topic>.mindmap.md    its mind map
├── studio-views.json         its top buttons and left tabs, when the topic has its own (a Skills topic, a type)
├── passes/pNN-<MMDD>/        one round each: a working session or a meeting
├── result/                   its own working output; messy is fine
└── delivery/                 the agreed version: deck/ and the thing it hands over; render.yaml says where it goes
```


## 4. Add, redraw, save

Run from the SPACE root.

```bash
S=plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts
X=plugins/haipipe-toolkit/skills/1_base/draw/hai-draw/scripts
python $S/new_topic.py topic <level> --slug <topic> --title '<title>' --band <band> [--builder]   # add
python <level>/sNN-<topic>/build_sNN_<topic>.py                                                   # redraw
python $S/render_png.py <drawing>.excalidraw <drawing>.png                                        # preview
python $X/check.py <drawing>.excalidraw                                                           # the drawing's rules
python $S/new_topic.py session <level> sNN --title '<session>' [--kind meeting]                   # save a round
python $S/render_delivery.py <level>/sNN-<topic> [--apply]                                        # render its delivery
```

1. **Load `/hai-draw` before drawing or redrawing**: how a drawing reads is that skill's.
   `--builder` draws the five parts with `five_parts.py`; without it `quick_draw.py` makes a light sketch;
   `topic_map.py` draws a topic's frames from its face; all write through `canvas.py` (`ref/topic-builder.md`).
2. **Change the builder, never its output**; what a person drew, edited or deleted survives a rebuild.
3. **After drawing, read it as a reader, then call `hai-studio-reviewer-agent`** (`ref/reader-review.md`).
4. **A person moves `**Stage:**`** (explore → shaping → agreed → closed).

| To | Run |
|---|---|
| write a Skills topic's buttons and tabs | `skills_views.py <topic> [--skills <skill dir> …]` |
| write a type's requirement pages, with their examples | `type_requirements.py <type topic>` (examples resolved by `requirement_examples.py`) |
| write a topic's Check button | `check_views.py <topic>` |
| write a Block Structure topic's Job and Task type pages | `block_types_pages.py <topic>` |
| draw a Job's current results as a topic | `job_results.py <block>` (`ref/job-results.md`) |
| propose topics for a Block that has work but no topics | `block_inventory.py <block>` (`ref/infer-topics.md`) |
| rebuild a topic's slides | `topic_slides.py <topic>` |
| bring older topics up to today's rules | `studio_update.py audit` then `update [--apply]` |
| move topics out of an old `studio/` folder | `studio_move.py <path> [--apply]` |
| fold an old `reports/` folder into topics | `reports_to_topics.py <path>` |
| list every kind of topic with a real example | `gallery_scan.py` (`ref/gallery.md`) |
| shrink a folder's Studio pictures | `shrink_media.py <folder> [--dry]` |
| add an icon for a Design | `icons.py --gallery` (the pictures: `ref/icons/icons.png`) |
| draw an item of a downloaded icon library | `icon_library.py --list <word>`, then `item("<name>", …)` in the builder (`ref/icon-libraries.md`) |


## 5. What to check

Run the row that matches what you changed, with the host Python, from the SPACE root. A change is done only when its
row passes. Showing a Check button does not run a check.

| After you changed | Run | It passes when |
|---|---|---|
| any topic of a blueprint Block | `python plugins/haipipe-toolkit/checks/run.py --target <topic or Block>` | every line reads PASS; coverage is in [checks/README.md](../../../../checks/README.md) |
| a topic's title or number | `topic_titles_check.py <Block>` | the title starts with its band's name |
| a type's `elements.md` | `type_requirements.py <type topic> --check` | its requirement pages are not stale |
| a type's or a topic's names | `placeholder_check.py examples` | no bare slot name |
| a topic that names a type, or the type | `type_follow.py check <Block or topic>` | no ❗: its buttons and tabs are the type's (⬜ marks a part not filled in yet) |
| a Skills topic, or a skill it shows | `skills_views.py <Block> --check` then `skills_checklist.py <Block> --check` | the tabs are the skill's folder today; no ❗ line |
| a Check button's source | `check_views.py <topic> --check` | the Check page matches its type |
| a Block Structure topic's types | `block_types_check.py <Block>` | every example Job and Task names a listed type |
| a drawing | `$X/check.py <drawing>.excalidraw`, then the reader review | no missing part; the reviewer returns `answers` |
| a topic's delivery | `render_delivery.py <topic>` | every piece reads `same` |
| this skill's `SKILL.md` or a `ref/` file | `skill_text_check.py` | no who-and-when note, no marker line; every named file exists, every ref and script is named |
| this skill's scripts | the tests in `tests/` | all pass |

Then open the owning Block's page and look at the topic itself: a check that passes on files is not a page that
reads right.


## 6. Read when you need it

| Read | For |
|---|---|
| [ref/topic-contract.md](ref/topic-contract.md) | the topic contract and the list of its files |
| `ref/topic-folder.md` · `ref/topic-face.md` · `ref/topic-numbering.md` | the folder, the face, numbers and bands |
| `ref/topic-delivery.md` | one delivery per topic, delivery types, the render out, each Theme's render |
| `ref/topic-builder.md` · `ref/topic-look.md` | drawing with a builder; what `canvas.py` enforces; change notes |
| `ref/reader-review.md` | the reader's questions and the reviewer loop |
| `ref/topic-rounds.md` | saving a session or a meeting |
| [ref/studio-type.md](ref/studio-type.md) | writing a Studio Type: its `elements.md`, the four questions |
| [ref/skills-topic.md](ref/skills-topic.md) | a Skills topic: skills on top, a skill's folder on the left, its drawing |
| `ref/ui-preview-topic.md` | a UI preview topic: live pages and quick pages |
| [ref/type-examples.md](ref/type-examples.md) · [ref/check-view.md](ref/check-view.md) | a type's examples; the Check button |
| `ref/proposal-topic.md` · `ref/slide-draft-topic.md` | a proposal section topic; a slide draft |
| `ref/job-results.md` · `ref/infer-topics.md` · `ref/gallery.md` | a Job's results topic; topics inferred from work; real examples |
| `ref/studio-section.md` | what the page's Studio section shows: groups, Runs, Timeline, Folder |
| `ref/topic-transcripts.md` | transcript originals inside a Task topic |
| `ref/screen.md` · `ref/chat.md` · `ref/draw.md` · `ref/workbench-table.md` | the Page's Studio tab: the live editor above the chat |


## 7. Who owns what

| Owner | Owns |
|---|---|
| `hai-studio` | the topic folder, its face, numbering, Studio Types, builders and their writer, previews, rounds; the Page's Studio tab |
| `hai-draw` | how a topic's drawing looks and reads: its principles, `draw.py`, `check.py`; loaded before drawing |
| `hai-draw job` | a Job as one topic: why, in and out, what it concluded, its tables |
| `hai-draw report` · `hai-draw slide` | a report's drawing and a scratch; a slide draft's frames and deck |
| `hai-mindmap` | a topic's mind map |
| `hai-report` | the Questions a topic answers |
| a Theme's own skill | rendering that Theme's delivery (`ref/topic-delivery.md`) |

`/workbench-studio` still triggers this skill.
