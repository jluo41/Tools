---
name: haipipe-page
description: >-
  The PAGE contract and router of a Board: what one page IS on disk (page.md
  with four on-stage sections beside its outline/ process folder and plugin
  lanes), how its Page Type is resolved, which Page Phase holds authority,
  and four verbs: PREVIEW, CREATE, WORK ON, RUN. Trigger: create a page, new
  page, update a page, preview a page, what does this page say, run page
  lifecycle, Page Type, Page Phase, /haipipe-page.
metadata:
  version: "0.45.0"
  last_updated: "2026-08-31"
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
├── outline/       the plan (versioned, ticked) and six record files:
│                  requirement · discussion · feedback · evidence · files · log
│                                                              haipipe-plugin-outline
├── pagex/         Probe's accepted-Page lane: files borrowed from other Pages
├── probe/         Probe's Task/Discovery lane: cards, proof, and values
├── bibex/         citation cards, source notes, the page's own .bib
├── display/       zero or more independently accepted display units
├── latex/ word/   generated projections, when requested
└── …              every other lane on the plugin roster
```

A folder is created only when it is used. Values have a surface but no folder:
each lives inside one probe card's `## Values` block and is cited as
`PP<NN>.v<n>`. When a page's numbers come from code, ONE collection job
(task-type `page`, contract `task/haipipe-task-for-page`) answers all its
task-route cards and ranks first in the page's `task/` lane. The seven `outline/` files, their ids, labels and writers are
`haipipe-plugin-outline/ref/record-shape.md`; the plan's grammar is
`ref/plan-grammar.md` beside it. A phase loads those two refs, not the plugin
skill (which owns the tab).

## 🧬 One key claims a page

A property every page carries cannot tell one kind of page from another. A page
shows something, cites something, states a number; so display, literature and
value are PLUGINS. A Page Type earns its key by stating how that page CLOSES.
**No `page-type:` key is the default and the most flexible case**: the page
owes the base section order and nothing more.

Resolve ① to ⑤ in order and stop at the first key that matches. EXACTLY ONE
step may claim a page; a page no key matches, or one carrying two keys that
disagree, is fixed on the page, never in the resolver. Step ③'s key is
required on every type that has one and beats the filename. `route: outward |
inward` is a plugin key naming an evidence lane; it picks no contract.

```text
step  machine-readable key                    Page Type          contract
──────────────────────────────────────────────────────────────────────────
①     filename QBv<n>-                        venue              for-venue
③     frontmatter `page-type: <key>`          the key names it   for-<key>
④     filename S-<Family>-<unit>-<slug>       stage              for-stage
⑤     filename Q<group><n>[<face>]-<slug>     Q decision         base only
```

A Discovery Folder resolves `folder-kind: discovery` to its Discovery workflow
phase. Its Task Face does not select the empirical `page-type: task`
compatibility grammar.

### The inventory is derived, never written by hand

The shipped `*/page-types/` folders say who MAINTAINS a key, `check.py`'s
`PAGE_TYPE_VALUES` says what RESOLVES, and the boards say what is IN USE:

```bash
python3 <haipipe-board>/cli/pagetypes.py           # the table, with live page counts
python3 <haipipe-board>/cli/pagetypes.py --write   # rewrite the block below
python3 <haipipe-board>/cli/pagetypes.py --check   # exit 1 on any drift
```

A key with live pages and no contract, or a key the engine accepts that nothing
ships and nothing uses, is a finding; `--check` is the tooth. The block carries
the structural facts only; the counts stay in the command's output.

Since 260831 every key also has a RECORD in `ref/type-registry.md`: four
fields, one consumer each (`outline` → ① OUTLINE · `evidence` → ②/③ ·
`prose` → ④ DRAFT · `closing` → ⑦ CHECK). The phases are the functions; the
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
principle    application   ✓       `page-type:` line
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

A Page Type used by one consumer family is a VARIANT of the base: it defines
Content and may populate fixed extension points in Aims, and it never
redefines, adds, removes or reorders the frame sections. A variant ships under
the `page-types/` folder of the skill set that owns it, so the folder names
the owner. Load the matching variant before writing or fixing any page of its
type; when a variant moves, re-run `install.sh --global` or its symlink
silently stops resolving.

## 🎭 Phases, independent of type

A page persists while the authority acting on it changes. The current phase is
not a Page Type and is not inferred from the edit operation.

```text
phase       authority                                          load
──────────────────────────────────────────────────────────────────────────────────
OUTLINE 🚧  agree the SHAPE; exit only on a person's tick       page-workflows/haipipe-page-outline
PROBE       turn each outline mark into a card and ask          page-workflows/haipipe-page-probe
EVIDENCE    land every promised claim's card, key or unit       page-workflows/haipipe-page-evidence
DRAFT       write the page from the plan and landed evidence    page-workflows/haipipe-page-draft
REVISE      improve the realization while purpose and Aims hold page-workflows/haipipe-page-revise
COMPILE     rebuild latex · pdf · word from that prose          page-workflows/haipipe-page-revise
CHECK       judge one version and route its next authority      page-workflows/haipipe-page-check
```

Resolve one invocation as: base page contract → matching Page Type → current
Page Phase → the page-local plugins and family craft the artifact requires.
The phases form a routing grammar, not a conveyor belt: each may repeat,
PROBE and EVIDENCE may be skipped when the page promises no claim it cannot
support, and CHECK may route to any earlier phase. When the visible operation
is ambiguous, the authority test decides:

```text
the section list itself is being agreed  → OUTLINE
purpose or Aims change                   → DRAFT
a marked hole has no card open for it    → PROBE
a card is open and its answer must land  → EVIDENCE
the same purpose and Aims are improved   → REVISE
a concrete version is judged             → CHECK
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
→ the Page Type variant → the current Phase contract → the page's own
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
├── ref/type-registry.md  one record per Page Type key; the phases' arguments
└── CHANGELOG.md        version history, and the only home for retired rules
```

Reads `haipipe-board/ref/page-template.md` and `ref/board-form.md` §4 as the
authority; owns no scripts. `cli/pagetypes.py`, `cli/preview.py` and
`cli/pagecontext.py` live with the machinery. The lifecycle packet and receipt
spec belong to `page-workflows/haipipe-page-workflow/ref/page-run-contract.md`.
