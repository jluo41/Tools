---
name: haipipe-page
description: >-
  The Page Face contract and router of a Folder: what the readable .md is on
  disk, how its phase-owned Folder kind or legacy Page Type is resolved, which
  Page Phase holds authority, and PREVIEW, CREATE, WORK ON, RUN. Trigger:
  create a page, update page, run page lifecycle, Page Face, Folder kind,
  legacy Page Type, Page Phase, /haipipe-page.
metadata:
  version: "0.53.0"
  last_updated: "2026-09-01"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page · one shape every page keeps

`haipipe-board` is the door you walk through to RUN a board. This skill is the
door for ONE PAGE, and the spec that page is measured against. Say
`create a new page on <topic>`, `working on <page>`, or `run <page>`; loaded
with no board open it is a pure contract, which is how the routing verb, the
chat drawer and the variant authors in other families read it.

```text
haipipe-page                     haipipe-board
──────────────────────────       ──────────────────────────────
what a page IS                   rendering it (src/page_question.py)
the section contract             serving and write-back (cli/serve.py)
where a write may land           the checker (cli/check.py)
the base/variant model           the template file (ref/page-template.md)
```

This skill never contains the renderer, the server or the checker; it calls
them. The authoritative template stays `haipipe-board/ref/page-template.md`;
this contract cites it and never forks it.

## 📁 What a page is on disk

A page is one markdown file (the PRODUCT: what the page asserts) beside one
process folder (how it came to assert it) and the plugin lanes it actually
uses. The roster of legal folder names is `haipipe-plugin/ref/roster.md`.

```text
<page>/
├── <page>.md      Opening · Diagram · Content · Aims           THIS contract
├── outline/       HUMAN process: the plan (versioned, ticked) and six record
│                  files: requirement · discussion · feedback · evidence ·
│                  files · log — parsed MEETINGS land here (JL 260831)
├── workflow/      MACHINE process: one receipt per phase pass
│              ─── the LOWER, TASK-side part ───
├── scripts/       optional owned implementation, any language; shared Task
│   └── config/    Job code stays one level up in `src/`
├── runs/          optional authored Run tickets; THE ONE execution door
├── results/       Folder-local Results only. A canonical Task Page resolves
│                  generated output at `<job>/results/<task>/<run>/`
│              ─── the UPPER, PAGE part ───
├── evidence/      what the page CITES, each lane behind its gate:
│   ├── bibex/     citations · verified:
│   ├── probe/     cards + values (PP<NN>.v<n>) · read:
│   ├── display/   units, recipes inside · accepted:
│   ├── pagex/     exact-file evidence and whole-Folder relationships;
│   │              Folder cards show Page Face + live Task status
│   └── materials/ dated captures
├── delivery/      what leaves the page: latex/ · word/ · slide/ · render/
└── studio/        the HUMAN's room on the page (JL 260831): closest to
    ├── chat/      the person · you talk here, sessions kept
    └── draw/      you draw here, one scene per owner; the chat may
                   redraw the scene's named elements on your ask
```

**The Folder symmetry**: every Folder has a Page Face and Task Face; a
`primary_face` says which is the usual entry, not which face exists.
`outline/` is the human planning/decision record and `workflow/` is the
machine-readable phase/run record. Page-heavy work commonly stores phase
receipts under `workflow/receipts/`; executable work commonly stores
`plan.yaml` and `report.yaml`. Runs is an optional presenter beneath this shared
Task Face. It pairs the local ticket with either a Folder-local Result or the
containing Task Job's `results/<task>/<run>/`; scripts, config, and notebooks
appear only when the dialect owns them. Runs is never a third universal face or
a lifecycle owner.

A unit MAY carry a `README.md`, and it is DERIVED (JL 260831): a generated
projection of the two-part tree as it actually stands (which lanes exist,
their counts, where the product and the rendered page live), regenerated
whole and never hand-edited — the structure's law lives HERE and in the
roster, so a hand-written copy per folder would be a second authority that
drifts. GitHub renders it where the board cannot reach; the 📂 tab computes
the same walk live (`live/folderstat.py`, whose `--write` becomes the
generator).

A folder is created only when it is used. Values have a surface but no folder:
each lives inside one probe card's `## Values` block and is cited as
`PP<NN>.v<n>`. Every number shown on a Page Face that comes from a Run crosses
ONE page-serving collection job (`task-type: page`, contract
`haipipe-task-for-page`); that Folder answers all related task-route cards and
ranks first among the page's `evidence/pagex/` whole-Folder links. A local Run
may validate or reshape non-authoritative intermediates, but it
cannot become a second value door. A reusable derivation, a source-data change, or any displayed
numeric result belongs in the linked executable Folder and its QA binding. The
seven `outline/` files, their ids, labels and writers are
`haipipe-plugin-outline/ref/record-shape.md`; the plan's grammar is
`ref/plan-grammar.md` beside it. A phase loads those two refs, not the plugin
skill (which owns the tab).

## 🧬 One owner claims the Page Face

A property every Page carries cannot tell one Folder kind from another. A Page
shows something, cites something, states a number; so display, literature and
value are plugins. In migrated families, the workflow phase owns the Folder
kind and its Page Face. In unmigrated families, a Page Type remains the
compatibility owner. No `folder-kind:` or `page-type:` key is the flexible base.

Resolve ① to ⑥ in order and stop at the first key that matches. Exactly one
semantic owner may claim the Page Face. An in-place Folder's
`workflow/phase.yaml current.folder-kind` is authoritative; fixed-kind Folders
use Page `folder-kind:`. `page-type:` is a compatibility fallback. If current
state and Markdown disagree, fix the Folder, never the resolver.

```text
step  machine-readable key                    Page Face owner    contract
──────────────────────────────────────────────────────────────────────────
①     workflow/phase.yaml current kind        workflow phase     phase skill
②     frontmatter `folder-kind: <key>`        workflow phase     phase skill
③     frontmatter `page-type: <key>`          compatibility key  phase or for-<key>
④     filename QBv<n>-                        venue              for-venue
⑤     filename S-<Family>-<unit>-<slug>       stage              for-stage
⑥     filename Q<group><n>[<face>]-<slug>     Q decision         base only
```

A discovery folder gets no type of its own: `task` carries which kind of
folder it reads.

### The inventory is derived, never written by hand

Phase `legacy_page_type` metadata and unmigrated contract folders
(`*/page-types/`, Paper's phase filename bridge, plus Venue) say who maintains
a legacy key. `check.py` says what resolves and boards say what is in use:

```bash
python3 <haipipe-board>/cli/pagetypes.py           # the table, with live page counts
python3 <haipipe-board>/cli/pagetypes.py --write   # rewrite the block below
python3 <haipipe-board>/cli/pagetypes.py --check   # exit 1 on any drift
```

A key with live pages and no contract, or a key the engine accepts that nothing
ships and nothing uses, is a finding; `--check` is the tooth. The block carries
the structural facts only; the counts stay in the command's output.

Since 260831 every key also has a RECORD in `ref/type-registry.md`: four
fields, one consumer each (`outline` → SHAPE · `evidence` → SURVEY and LAND ·
`prose` → WRITE · `closing` → CHECK). The phases are the functions; the
record is their arguments. A `contract` key keeps its outline SHAPE in its
own frontmatter and the registry points at it; a `key-only` record with live
pages is a `registry-gap` (usage without law), reported by the same
`--check`.

<!-- BEGIN GENERATED page-type-inventory -->
```text
key          owner         engine  resolved by
───────────────────────────────────────────────
brief        application   ✓       `page-type:` line
collection   —             ✓       `page-type:` line
dash         —             ✓       `page-type:` line
data         application   ✓       `page-type:` line
design       application   ✓       `page-type:` line
display      —             ✓       `page-type:` line
ideation     paper         ✓       `page-type:` line
information  application   ✓       `page-type:` line
insight      task          ✓       `page-type:` line
knowledge    application   ✓       `page-type:` line
labeling     —             ✓       `page-type:` line
meta         application   ✓       `page-type:` line
narrative    paper         ✓       `page-type:` line
opening      —             ✓       `page-type:` line
question     application   ✓       `page-type:` line
roadmap      paper         ✓       `page-type:` line
round        paper         ✓       `page-type:` line
section      paper         ✓       `page-type:` line
seed         paper         ✓       `page-type:` line
slide        —             ✓       `page-type:` line
stage        board         ✓       filename S-<Family>-<unit>-
task         task          ✓       `page-type:` line
venue        paper         ✓       filename QBv<n>-
view         —             ✓       `page-type:` line
wisdom       application   ✓       `page-type:` line
```
<!-- END GENERATED page-type-inventory -->

### A variant extends the base and never redefines it

A Page Face specialization defines Content and fixed extension points without
reordering the base frame. In a migrated family it lives in the workflow phase
that owns the Folder kind; an unmigrated Page Type remains a base variant under
`page-types/`. Load the semantic owner before writing. After moving a skill,
re-run `install.sh --global` so the installed symlink follows it.

## 🎭 Page phases, independent of Folder kind

A Page Face persists while its Page-workflow authority changes. The page
workflow (`page-workflows/haipipe-page-workflow`) is TWO PARTS of named
cycles, independent of the domain workflow phase that owns the Folder kind:

```text
part      cycle     phase (the skill that acts)                  gate
──────────────────────────────────────────────────────────────────────────────────
OUTLINE   SHAPE     page-workflows/haipipe-page-outline           👤 approved:
          SURVEY    page-workflows/haipipe-page-outline           👤 Decide per item row
          LAND      page-workflows/haipipe-page-evidence          ⚙ every make-row landed
          EMBED     page-workflows/haipipe-page-evidence          ⚙ back to SHAPE
DRAFT     WRITE     page-workflows/haipipe-page-draft + -revise   ⚙ cold pre-check ready
          CHECK     page-workflows/haipipe-page-check             👤 accepted:
```

The law under the OUTLINE part: every evidence number is answered by a RUN at
a real `tasks/` address; the run computes, the page interprets (EMBED). The
item table `outline/<stem>-items.md` is the one ledger
(`haipipe-plugin-outline/ref/item-table.md`).

Resolve one invocation as: Folder → base Page Face → phase-owned Folder kind
(or a legacy Page-Type compatibility contract) → current cycle →
phase-selected and page-local plugins.
The cycles form a routing grammar, not a conveyor belt: each may repeat,
SURVEY and LAND are skipped when the page promises nothing it cannot already
support, and CHECK may route to any earlier cycle. When the visible operation
is ambiguous, the authority test decides:

```text
the section list itself is being agreed        → SHAPE
a mark has no item row, or a row no Decide     → SURVEY
a decided row has no result on disk            → LAND
a landed row is not yet in the plan            → EMBED
purpose or Aims change                         → WRITE, new round (DRAFT)
the same purpose and Aims are improved         → WRITE (REVISE)
a concrete version is judged                   → CHECK
```

`RUN` is the router verb, deliberately not `ADVANCE`; it is owned by
`page-workflows/haipipe-page-workflow`, whose `ref/page-run-contract.md` holds
the packet, receipt, version, role-separation and stop rules, and whose
`ref/phase-cards.md` states every phase in the same six fields. A pass may run
inside a person's session (the page chat, which knows the phases and reads the
strip: `haipipe-plugin-chat` §🔁) or as that phase's agent; both leave the same
trace (the artifact, one log record, the receipt).

## 📑 Four sections on stage, and nothing else

The authority is `haipipe-board/ref/board-form.md` §4: the on-stage order is
`Opening → Diagram → Content → Aims`, the optional folds (`Law` · `Lesson` ·
`Glossary`) follow, and everything else a page used to carry lives in
`outline/` (log, discussion, files) or was merged (States into Aims).
`check.py` reports a surviving `## States`, `## Files`, `## Log`,
`## Discussion` or an older name as `retired-section`.

```text
#   section    conveys · the reader question                 phase authority              omit
────────────────────────────────────────────────────────────────────────────────────────────────
1   Opening    what is this page, why should I care?         DRAFT defines · REVISE clarifies   never
    ### Writing Style  how the NEXT writer should write it   inside Opening's drawer            allowed
2   Diagram    can I see the whole subject at once?          DRAFT/REVISE, within type rules    when no figure helps
3   Content    what does this page actually establish?       DRAFT defines · REVISE realizes    Q may · S never
4   Aims       what should become true, for which Content    DRAFT sets target and test;        never
               division, and what is true now for each?      any phase updates Now:
```

Each section answers one reader question, and a sentence answering another
section's question is misplaced: substance in Opening moves to Content,
inherited inputs and venue move to the Stage Contract, prose rules to
Opening's `### Writing Style`, intended outcomes to an Aim's target, current
facts to that Aim's `Now:`, and a question for a person to a `D<nn>` record.
There is no `## Boundary` section: what a page covers is the Opening's job,
stated as a `**Covered elsewhere**:` part in its drawer.

## 🎯 One Aim is one row: target, test, and Now

`## Aims` is the Aims' only home. One Aim is one row: its tick, its target,
its `Done when:` test and its `Now:` fact. The plan carries 🎯 marks that name
these rows and no rows of its own.

```markdown
## Aims
### A3 · 📚 Results
- ✅ A3.1 · The headline coefficient carries its four coordinates.
  **Done when:** a reader can quote SPEC, window, trait form and outcome.
  **Now:** met; §3.2 states all four beside the estimate.
```

- **The tick says its meaning by shape**: `✅` met · `🔨` being worked on ·
  `🧠` waiting on a ruling · `⬜` not met · `❄️` deliberately held. This is the
  Aim vocabulary, not the page `state:` line, which keeps ✅ 🟡 🔴 ⏸️.
- **A group `### A<n> · <emoji> <name>` maps to Content division n**, taking
  its number, name and emoji so the two sections line up by eye and by id
  (`check.py` `group-name-drift`, `group-no-division`); `### P · Page-level`
  holds a target that genuinely crosses divisions.
- **`Now:` is a snapshot**; the reason for a transition is a log record. A live
  ask for a person is that Aim's `Now:` marked `🧠`, pointing at its `D<nn>`.
- **A fact with no Aim id is a note**, not a status; an ask that owns no Aim
  becomes a `D<nn>` thread, never a minted Aim. An Aim is not a task: one
  division may own zero, one or many; changing an Aim's optional `Plan` does
  not change the Aim.
- **`### Decision Now` is reserved inside Aims** for a machine-proposed
  ruling: one `- [ ]` row with the ask, one option per line saying what
  choosing it commits you to, and a `→ CC recommends` line. A machine closes
  a row only after the person answered (in chat, in a lane, or by ticking)
  and records which option, who, when, and their words.

## 🚪 Preview · create · work on · run

```text
👁 PREVIEW    /haipipe-page preview <page>                 read verb, writes nothing
📄 CREATE     /haipipe-page create a new page on <topic>   [on <board>]
🔧 WORK ON    /haipipe-page working on <page>              or just the path
🔁 RUN        /haipipe-page run <page> [from <phase>]
```

**Preview**: `cli/preview.py <page>` prints one screen (title, the Opening's
visible paragraph, the Aims with their `Now:` lines, the Content divisions,
the last log record); a group or board folder prints one roster line per
page. A gist, never a substitute for the whole-file read.

**Create**: resolve the board and group (ask only when the group is genuinely
ambiguous) · pick the id and copy `haipipe-board/ref/page-template.md`, never
retype the shape · a three-to-five-word title stating the purpose · the
Opening as one visible paragraph above the first blank line · Content as
numbered parts, each with a caption, a figure and a short intro · Aims with
their `Now:` lines · `outline/<stem>-files.md` with any Related Board Page row
the current phase needs · register in `board.md` · build, check, read the
RENDER, report the finding count.

**Work on**: ONE page is the deliverable. Read the whole file and its
`outline/` first; if the files record declares Related Board Pages, load the
one-hop packet from `cli/pagecontext.py <page> --phase <PHASE>` · run the
checker and fix the mechanical findings in bulk · then read for what no
checker reaches (the weak-English axis, one question per part, an Opening that
says more than the title) · a rule nobody wrote down goes in three places (the
owning page, `ref/page-template.md`, this file) · build, check, read the
render, report before and after counts · a write outside the target page only
when the page cannot be made correct without it, named file by file · never
rewrite a sibling page's content.

**Run**: the bounded loop lives with `page-workflows/haipipe-page-workflow`.
The dispatch stays in the session you typed it in: a subagent is not handed
the `Workflow` tool. A new page is CREATEd and registered first and RUN starts
at OUTLINE; an existing page with no known next authority starts at CHECK.

```bash
python3 <toolkit>/skills/board/haipipe-board/cli/preview.py <page>
python3 <toolkit>/skills/board/haipipe-board/cli/build.py <board-folder>
python3 <toolkit>/skills/board/haipipe-board/cli/check.py <board-folder> | grep '^<PAGE>'
python3 <toolkit>/skills/board/haipipe-board/cli/check.py <board-folder> --summary
python3 <toolkit>/skills/board/haipipe-board/cli/check.py --rules
python3 <toolkit>/skills/board/haipipe-board/cli/pagetypes.py
```

`--rules` prints every finding code with its message; read the laws before
writing, not from the error text after. `watch.py` rebuilds on any `.md`
save; a `.py`, `.css` or `.js` change needs one build run.

## ✍️ What a write may touch

Load this skill and `haipipe-board/ref/writing-rules.md` directly before
writing; a copied checklist in a prompt is a second authority and drifts.

- **A change is finished when it is on the RENDERED page**, and nobody is
  asked for permission on the way: write the source, propagate a new rule to
  `ref/page-template.md` and this file, run `check.py`, then confirm the render
  rather than the markdown.
- **The write anchor rule**: a machine write lands at a section boundary,
  never at a byte offset; appending under a named `##` heading is safe.
- **The human-decision rule**: a machine updates an Aim's tick only from
  evidence it can inspect; a person's ruling is transcribed with the quote
  (`approved: ✅ JL 260831 0146 · in chat: "…"`), never decided.
- **The form rules, each owned once**: the title is three to five visible
  words in sentence case, never six (`writing-rules.md`; `title-too-long`) ·
  the first blank line in Opening is the split between the visible paragraph
  (≈450 characters, 520 ceiling, `OPENING_MAX_STAGE_CHARS`) and the drawer ·
  every figure carries a caption line above its fence · Content is numbered
  all the way down (`### 3 ·`, `**3.2 ·**`, `#### 3.2.1 ·`) · `More details`
  is a list of labelled parts, never one block · a figure row is a label and
  its value, never a clause · the `state:` line is one row under 110
  characters · a heading is a lookup key (`writing-rules.md` §A heading is a
  lookup key).
- **The Opening's first job is to define the words its own question uses**,
  one line each with a real example; speak about the subject, never from a
  reusable scaffold (`This page defines …`): if the paragraph still fits
  another page after its nouns are swapped, rewrite it.
- **Before writing back, self-check**: no promise the page does not support,
  no sentence that only fills a category, one sentence per source line,
  English only, no em-dash. This improves the draft and approves nothing; a
  fresh reviewer judges the page after the writer's context is gone.

## 🔍 How a page is judged

Evaluation asks whether the authored page satisfies its declared
requirements, never whether the reviewer likes the format, and the
requirements resolve in this order: this contract and `ref/page-template.md`
→ the phase-owned Page Face (or legacy Page-Type variant) → the current Page
Phase contract → the page's own
`### Writing Style` (and `## Stage Contract` on S) → the local division
purpose and each paragraph's job line. A more specific source refines a
broader one and never silently contradicts it; a conflict is reported and
that criterion is not judged until the owner resolves it. The rubric (four
axes, four verdicts, the review units, the batch-voice test, the report row)
is `page-workflows/haipipe-page-check` §📏; `check.py --strict` supplies the
mechanical half, the page's `✅ Quality Check` runs the rubric in the page
chat, and `haipipe-page-check-agent` runs it in a fresh context.

## 🔤 The words

Every term this family uses is defined in `ref/glossary.md` beside the path it
names: card, unit, mark, plan, bullet, tick, bank, stake, phase, record. Load
it when a reader asks what a word means or when you are about to coin one;
`writing-rules.md` forbids a phrase that is neither the source's own wording
nor defined where a reader can find it.

## 🏷 How a location is written

```text
page        QB4            #QB4
face        QB4a           a page whose id carries its parent's number
group       #group-QB      scrolls the index, opens nothing
sentence    QB8's grammar  haipipe-sentence owns everything below the section
bullet      C3.P1.B4       the plan's address; a sentence names it with realizes:
thread      D07            board-wide, cited from any page
```

Every id inside a fenced figure renders as a link.

## ✅ Closing checks

- `pagetypes.py --check` exits 0, and the generated inventory block matches
  its output.
- Every heading passes `writing-rules.md`'s five lookup-key tests;
  `grep -n '^#\+ .*, '` returns only clauses that state a second rule.
- No section states a rule a cited authority owns (`board-form.md` §4,
  `page-template.md`, `writing-rules.md`, `haipipe-plugin-outline`), except
  where this file adds what a machine may write.
- No section narrates a retirement; what a key or section used to mean lives
  in `CHANGELOG.md`.
- Every path this file names resolves on disk; each `##` section answers one
  reader question.

## 📂 Files

```text
haipipe-page/
├── SKILL.md            this contract
├── ref/glossary.md     every word this family uses, with the path it names
├── ref/type-registry.md  compatibility key records + phase-owner arguments
└── CHANGELOG.md        version history, and the only home for retired rules
```

Reads `haipipe-board/ref/page-template.md` and `ref/board-form.md` §4 as the
authority; owns no scripts. `cli/pagetypes.py`, `cli/preview.py` and
`cli/pagecontext.py` live with the machinery. The lifecycle packet and receipt
spec belong to `page-workflows/haipipe-page-workflow/ref/page-run-contract.md`.
