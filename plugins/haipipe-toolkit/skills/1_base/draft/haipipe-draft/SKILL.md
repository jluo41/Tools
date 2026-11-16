---
name: haipipe-draft
description: "The draft behind every Page: create, edit, build and serve a self-contained Page Folder from a file, without a Board; owns the Page Face contract, which Run Spec holds authority, and a draft Task's seven steps (Studio, Plan, Write, Evidence, Display, Revise, Delivery). Planning is haipipe-draft-logic. Trigger: draft, draft folder, file to page, create a page, Page Face, page Run Spec, draft steps, /haipipe-draft, /haipipe-page."
metadata:
  version: "0.143.0"
  last_updated: "2026-11-13"
  aliases: [haipipe-page]
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-draft · the draft behind every Page

> Scripts here need Python 3.11+: where a command says `python3`, run it as `uv run --python 3.13 --with pyyaml python ...` (or a SPACE `.venv/bin/python`); see `plugins/haipipe-toolkit/skills/README.md` § Running a skill's scripts.

> ⛔ **Generated files: never modify them directly; change the code that writes them (or its source), then rerun it** (hard rule, JL 260928; the SPACE's AGENTS.md § Working rules). Here that means everything under `delivery/` (web copy, `.tex`, `.pdf`, `.docx`, `evidence-selection.json`): change the source, then rebuild. `## Content` is generated too: `cli/page.py adopt` writes it from the Draft's `## 3 · Draft`, so a sentence is always edited in the Draft (add its line there if the Draft lacks it), never in `## Content`, `.tex` or `.docx`.

> ⛔ **No content hashes** (hard rule, JL 260928; the SPACE's AGENTS.md § Working rules). A version is its number and date (`v1.5 260928 1241`); staleness is file time or `git diff`. Never write, check, compare or pin a sha256 in a Page, Result, receipt, ledger or manifest. The two exceptions, decided 2026-11-15: haipipe-insight's receipt `tables_sha256` (rerun compare) and haipipe-design's `method-sha` and inputs `manifest.yaml` sha256 (the Job fence); nothing else pins a hash.

## 🗺 Route table · what to do for which request

| The request | Do | Read |
|---|---|---|
| change a sentence in the Page, the Word or the PDF; rebuild it | edit `## 3 · Draft`, then `page.py adopt`, `export` | § ✏️ Fast path |
| deliver a draft Task on the person's ok | `bump`, `adopt`, `cards.py bib`, `export`, `health` | § ✏️ Fast path |
| wording feedback on an open Page Run | one bounded patch, under two minutes | § ⚡ Fast feedback Step |
| file to page (make this file a Page Folder) | `page.py setup <input.md>` | § File → Page Folder → work, `ref/standalone.md`, [ref/file-to-page.md](ref/file-to-page.md) |
| host or open a Page | `fn/serve.md` decides the server | [ref/open-page.md](ref/open-page.md) |
| one draft-Task step (structure, write, revise, deliver, check) | read the plan's `approved:` first | [ref/draft-steps.md](ref/draft-steps.md) (§ The Plan gate) |
| name, open or close a Page Run; adopt | `page.py open-run`, `close-run`, `adopt` | [ref/page-runs.md](ref/page-runs.md), `ref/page-run-families.md` |
| what needs the person (propose Runs) | `/haipipe-draft runs <page>` | `fn/runs.md`, § 🧑 fn/Runs proposes human interaction |
| create, work on or run a Page | the verbs | § 🚪 Preview · create · work on · run |
| the Folder on disk; move a Page to the current layout | `page.py check-page-folder`, `draft-layout` | `ref/folder.md`, [ref/page-folder-layout.md](ref/page-folder-layout.md) |
| who owns a Page Face; the reader sections; Aims | resolve ① to ⑥ | [ref/page-face.md](ref/page-face.md) |
| which Run Spec holds authority; an ambiguous operation | the authority test | [ref/run-workflow.md](ref/run-workflow.md) |
| write or revise prose | load `haipipe-draft-writing` | § ✍️ What a write may touch, `ref/writing-rules.md` |
| say a Page or draft Task is finished | `page.py health --final <task>` | § ✅ Closing checks, [ref/closing-checks.md](ref/closing-checks.md) |
| what a word means | | `ref/glossary.md` |

## 📝 Draft and Page · two names for two things (JL 261011)

A **draft** is the work: its logic, its sentences and its evidence, all kept in the
folder's `draft/`. A **Page** is what a reader opens: the face `<stem>.md` and its
built output in the Block's `delivery/`. This skill owns both; it was `haipipe-page`
until 2026-10-11, and `/haipipe-page` still opens it.

```text
draft/<stem>-draft-v<N>.md   ## 1 · Structure   the logic: one Bullet per point
                             ## 3 · Draft       the sentences, one line per Bullet
draft/<stem>-evidence-items.md                  the evidence: typed Evidence Items
<stem>.md                    Opening · Content · Aims   the Page face
<Block>/delivery/<jNN>/<tNN>/<lane>/            the Page's built output
```

`## Content` on the face is a copy `page.py adopt` makes from `## 3 · Draft`; the face
adds only the Opening and the Aims. Every folder at every level (Block, Job, Task,
report) has a face; a folder that writes prose also holds a draft. A Task is not a
Page: a compute Task has a face and no draft, and a Section Task holds one (b32
s01). A Task whose face says `task-type: draft` is a draft Task: every theme's workbench
opens it on the base's draft layout, `servers/workbench/workbench-task-draft/` (b32 s03). The Page server (`servers/workbench/workbench-task-draft/reader`) and
`haipipe-page-insight` keep their names because they serve or own a Page face; a Task Page's own rules are
`haipipe-task`'s `ref/task-page.md` (haipipe-page-task merged into it, 2026-10-21).

## 🪜 A draft Task's seven steps · 🚦 The Plan gate: [ref/draft-steps.md](ref/draft-steps.md)

## ✏️ Fast path · change a sentence and rebuild

For "change X in the Page / the Word / the PDF" and "rebuild it", load nothing
else. Three commands, then report the before and after sentence:

From Tools-SPACE drop `Tools/`; with no SPACE `.venv`, use `uv run --no-project --python 3.13 --with pyyaml --with markdown python`.
```bash
# 1. edit the sentence in draft/<page>-draft-v<N>.md, section `## 3 · Draft`
.venv/bin/python Tools/plugins/haipipe-toolkit/skills/1_base/draft/haipipe-draft/cli/page.py adopt  <page-folder>   # 2. Content ← Draft; writes `content:`
.venv/bin/python Tools/plugins/haipipe-toolkit/skills/1_base/draft/haipipe-draft/cli/page.py export <page-folder> --author "<Your Name>"   # 3. web, LaTeX, Word
```

Delivering a draft Task on the person's ok (t01_introduction v0.5, 261021), run from the repository root, no hand
step:

```bash
P=Tools/plugins/haipipe-toolkit/skills/1_base/draft/haipipe-draft/cli/page.py
C=Tools/plugins/haipipe-toolkit/skills/1_base/evidence/haipipe-evidence/scripts/cards.py
grep -nE "⟦|\[(E[0-9]+[^]]* pending|open |block )" <page-folder>/draft/<stem>-draft-v<N>.md   # 0. a ⟦check⟧, ⟦pending⟧, [E## pending], [open …] or [block …] mark left in § 3 would print: stop and ask
.venv/bin/python $P bump   <page-folder>                    # 1. draft v<N> → the next, the old one to draft/previous/
.venv/bin/python $P adopt  <page-folder>                    # 2. Content ← Draft; a new Page's placeholder is laid out first
.venv/bin/python $C bib    <page-folder>/evidence/cards.yaml --draft <page-folder>/draft/<stem>-draft-v<new>.md --write
.venv/bin/python $P export <page-folder> --author "<Your Name>"   # 4. web, then LaTeX, then Word (no --dry-run)
.venv/bin/python $P health <page-folder>                    # 5. the Folder agrees with itself
```

- The gate is the person's ok on the text ("make it v0.5"), which is the bump; `approved:` and an open Structure Run
  stay as they are, since the person closes a Run (Run bookends).
- Read both PDFs: no citation may print as "?" (a key missing from the `.bib`) and no S number, paragraph label or
  `⟦…⟧` mark may show.
- The face's `state:` line then holds only the state word and what is still open (cards, options, entries to adopt),
  never a version or date.
- Rendering the pages as images, sending, and reading a returned copy back are later, optional steps of
  `haipipe-delivery` (`render`, `pull`), after the files above exist.

A face may name the build that prints it: `delivery-builder: <script>` (relative to the face). Then `page.py export`
runs that script for the LaTeX and Word lanes instead of printing the Page as a Section, and checks that it left
`latex/<stem>.pdf` and `word/<stem>.docx`; the web lane is built as usual. A paper's cover letter uses it, so its
Delivery is the letter as uploaded (JL 261102: "this is not the version to submit to the submiision website").

**When adopt refuses because the paragraphs changed** (a paragraph added, cut, split or merged), run `page.py adopt --relayout <task>`: it lays `## Content` out again from the Draft and writes the `content: draft v<N> · adopted …` line. Never type Content by hand to get past the refusal (JL 261102: the cover letter's Content was typed by hand, no `content:` line was written, and its PDF printed draft v0.1 beside a v0.3 plan). Until Content is adopted, `page.py health` says so (`content`: "Content prints draft v0.1; the current draft is v0.3"; a FAIL under `--final`) and every Delivery tab shows the same warning above the file, so an old print is never read as the latest.

`page.py renumber <page-folder>` renumbers the sentences s1, s2, … in reading order in every file that names one (the
Draft, `evidence/cards.yaml`, the Revise cards, rules and comments; a person's own notes stay as written) after a
sentence is added, moved or merged (`--merged s15=s14`); `--dry-run` says what would change. A Draft whose ids restart
in each paragraph is renumbered by position through the Section (`page.py health` fails it: a sentence id appears
once in its Draft). A sentence id is written `s8`; an older `S8` is read as the same sentence, and
`page.py sentence-case <draft> --records [--dry-run]` rewrites one Draft and its records to `s`.

Code keeps every record here, so an agent types none (JL 260928: agents keep
text, code keeps records). `adopt` writes the header line `content: draft v<N> ·
adopted <yymmdd HHMM>`; `export` reruns each lane's one Delivery Run
(`run-delivery-webpage` · `_latex` · `_word`) and writes its ticket. Do not type
versions, dates, Run ids or "delivery rebuilt" into `state:` (it holds the state
word and open items only), do not append to the Draft's `status:` line (the
person's word), and allocate no new Run, Draft version, receipt or hash. The
person's request for the change is the ask that the Run bookends rule needs;
an open Writing Run's close records still wait for the person to end that Run.
The Page's own files are now current; a paper's full manuscript (`<paper>/delivery/`)
picks the change up at its next paper build (`delivery/build.py`, `haipipe-paper-assemble`).

This is the executable door for ONE PAGE, with or without a Board. Say
`haipipe-draft <file>`, `make this HTML file a Page Folder`,
`create a new page on <topic>`, `working on <page>`, or `run <page>`.
The canonical skill and grammar live in `skills/1_base/draft/haipipe-draft`; the
standalone server, the reader appearance and the live workspaces are served
from the workbench's `servers/` tree (`servers/workbench/workbench-task-draft/reader`, `servers/workbench/workbench-task-draft`).
An ordinary file is imported into a new Folder; an existing Page Face or
Page Folder is opened in place. Never silently wrap an existing Page again.

```text
haipipe-draft (this skill)                 the workbench host (servers/_host)
──────────────────────────────────        ──────────────────────────────────
Page Folder and source authority          one server over a Board or SPACE root
parser, renderer, template, assets        Home, /b/ and /w/ short routes
cli/: page.py, check.py (the Board          the live reader /_board/page and
  checker), draw.py, the Run CLIs           every workbench, all reading this src
agents and ref/folder.md (the folder)    no renderer of its own
```

The Page owns its parser, renderer, template, the Board checker and the Run CLIs
(they moved here when the `haipipe-block` skill was retired, JL 261005). Its
standalone server and live workspaces sit in the plugin-level `servers/` tree,
and the host loads the very same modules; there is one Page renderer. The authoritative template is `ref/page-template.md`.

## ⚡ Fast feedback Step

When the person gives wording feedback on an already open Page Run, use the
fast foreground path by default. Read only the Run resume view, the latest
Version tail, the named paragraph slice, its dependent Bullet, and the frozen
Structure description. Make one bounded patch, update the required small Run
projections, perform one narrow check, and return the review packet. Target
under two minutes. Do not reread the whole Page, update the plan for a
wording-only change, rebuild anything, run broad tests, verify the browser, or
start or wait for a sub-agent. If a required record is missing, report the one
blocker instead of scanning the repository.

## 🤝 Two top-level doors, one Folder

`haipipe-draft` and `haipipe-task` are peer entry doors. For a Page whose
`folder-kind: task`, both operate on the same physical `tNN_<task>/` Folder:

```text
Task door  executable work, P-B-E-R, native rNN, Result readiness
Page door  human interaction, typed RP/RE, evidence binding, Content, CHECK, release
```

Enter through Task when the primary product is independently testable output;
enter through Page when it is reader meaning or human acceptance. Page may
propose Task work but never allocates its native Run. Task may return a Result
but never accepts Page wording, closes a Page Run, or releases the Page.

For Task Folders, load `../../task/haipipe-task/ref/task-page.md` as the
detailed bridge. It owns the cross-face handshake, staleness propagation, and
the rule that the Folder closes only when both Task readiness and Page
readiness are current.

## 🏃 Page Run families inside Outline (Run names, Run bookends under `../haipipe-draft-workflow/ref/interactive-writing-run.md`, adoption, RP kinds): [ref/page-runs.md](ref/page-runs.md)

## 🧑 fn/Runs proposes human interaction

`fn/runs.md` is the read-only proposal function for Page-owned interaction.
It identifies bounded places where the human must shape, compare, revise, or
accept the Page, and proposes those as Page Run candidates. A proposal is not
an allocated Run and receives no typed RP identity, Ticket, Result, or
Runs-inventory row
until the person selects it. An existing matching open Page Run is resumed
instead of duplicated.

Code, search, Discovery, data, rendering, build, and other output-producing
work remains a normal Task Run, even when a later human gate reviews that
output. The Page may point to the needed Task work but never mints or rewrites
its owner-native identity. Use `/haipipe-draft runs <page> [focus]` to propose;
a direct bounded editing request counts as selecting the matching interaction.

The first Run of a Page is always a Structure Run (`run-structure-…`), even when imported content
already suggests a Shape. It iterates until the person explicitly
closes the Structure, Outline Bullets, and Page-global paragraph index
`P01..PN`. Later structure/Bullet revisions open another `run-structure-…`. Only
after the structure contract is closed may `fn/Runs` propose Section-level
Runs (`run-section-…`) or paragraph groups (`run-paragraph-p03-p05`). Every
paragraph Run name
must expose its exact paragraph number or contiguous range; semantic titles
stay in Goal instead of lengthening the identity.

### Three update boundaries

Interactive Page work has three different commit boundaries. Do not collapse
them into one expensive operation:

```text
Writing Step      complete one scoped draft/review/diagnose/revise cycle
                  → change only the Draft file (candidate and dependent Bullets)
Page Run close    settle its fixed structure, Section, or paragraph scope
                  plus its Evidence contract
Page release      after every Page Run and required evidence Task Result is ready,
                  adopt Content once and generate web/LaTeX/Word once
```

A routine Step never writes adopted Page Content, rebuilds delivery, runs the
whole test suite, or waits for browser/export verification. While the Run is open it changes
only the Draft file: the complete candidate and its affected Bullets (Run bookends, JL 260928). The verbatim
feedback, review/rating, diagnosis and Version/Step records are written once at the Run's close, from the
conversation (`haipipe-draft-workflow/ref/interactive-writing-run.md`). Update an Evidence requirement
during a Step only when the cycle changes what the paragraph must cite, measure,
or show.
Between Steps or Runs, use
`haipipe-draft-workflow/ref/interactive-execution-policy.md`:
heavy builds, exports, broad checks, delegated Task Runs, and sub-agent
analysis require an explicit scoped approval before dispatch.

A paragraph Page Run closes only after its text and Bullets are accepted and
its Evidence contract is explicit: each Bullet names `none` or a ready bound
CITE, VALUE, or DISPLAY Result. Discovery, figure production, citation lookup,
and other independently executable support remain Task Runs. Do not mark the
Page Run complete while required evidence is unresolved.

Closing one paragraph Run does not adopt it into `<page>.md` and does not
refresh `delivery/`. CONTENT waits behind the Page release barrier: all planned
Page Runs are complete and every required Task Result is ready and bound. Then
one Page-level CONTENT pass applies the accepted candidates, integrates the
evidence, builds the declared web/LaTeX/Word outputs, and routes one exact
version to CHECK. While the barrier is open, the Draft Space is current
and delivery is explicitly stale by design. For an interactive Page, the
person's explicit next-step instruction is the authority for this pass. That
instruction does not replace the plan's sign: a pass runs only on a plan whose
`approved:` starts with ✅, written from the person's own words in chat by
`page.py sign` (§ The Plan gate). The sign is that one word, never a second
approval loop or a button.

## ✅ Page configuration and completion checklist

For CREATE, a Page configuration/completion audit, or a whole-Page completion
claim, read `ref/page-checklist.md`. For a draft Task, its § 6 lists the file each of the seven steps leaves, and
`page.py health` warns on every missing one (`steps`; JL 261102). Assess the reader-facing Opening and
Content explicitly, then assess any backstage Outline, target, contract, and
Evidence records separately. Report configuration, content, review and hosting
separately: a created Folder, successful build, or default wrapper is not a
completed Page. Apply only checks relevant to the requested operation; a narrow
edit is not a whole-Page audit.

## File → Page Folder → work

For file intake, standalone building, or source editing, read
`ref/standalone.md` and use `cli/page.py`. For a hosting request, read
`fn/serve.md` first; it decides whether this Page server or the Board server
owns the URL. Choose the intake depth explicitly:

- `init` is a technical import only. It preserves the file and produces a
  visibly incomplete scaffold. Never stop here when the user asked for a Page
  they can immediately inspect or work on.
- `setup` is the normal Markdown file-to-working-Page route. It preserves the
  imported source, reads its H1/H2/prose structure, creates a Page-specific
  Opening and backstage requirement/target records, and writes an unapproved semantic Shape plus reader-move
  embedded Drafts in the Outline Markdown, Context/Files records, and
  a completed setup Task Run. A
  non-Section Bullet may map to several sentences; punctuation does not decide
  outline grain. Paragraph identity is one Page-global `P1..PN` sequence and
  does not reset at a new `C`. Inspect the generated roles and heads, then read the Bullet
  column alone. Correct any move whose place in the argument is unclear before
  handoff; generated does not mean human-approved.

This is not a request to obtain human Shape/Content acceptance. Do not require
a Board, group, Paper, evidence Run, PDF, or scholarly prose rewrite just to
import or host a file. Preserve the input verbatim in an editable copy and
report any unsupported dependencies.

```bash
python3 <toolkit>/skills/1_base/draft/haipipe-draft/cli/page.py init --file <input> --dest <page-folder>
python3 <toolkit>/skills/1_base/draft/haipipe-draft/cli/page.py setup <input.md> [--dest <page-folder>]
python3 <toolkit>/skills/1_base/draft/haipipe-draft/cli/page.py setup <existing-page-folder>
python3 <toolkit>/skills/1_base/draft/haipipe-draft/cli/page.py migrate-addresses <existing-page-folder>
python3 <toolkit>/skills/1_base/draft/haipipe-draft/cli/page.py migrate-drafts <existing-page-folder>
python3 <toolkit>/skills/1_base/draft/haipipe-draft/cli/page.py outline-tidy <page.md | page-folder> [--dry-run]
python3 <toolkit>/skills/1_base/draft/haipipe-draft/cli/page.py draft-layout <page-folder | board | tasks-dir> [--sort-runs] [--archive-evidence] [--dry-run]
python3 <toolkit>/skills/1_base/draft/haipipe-draft/cli/page.py health|structure <page-folder | version-job>... [--json]   # structure: print it verbatim when asked (must-check M-D14)
python3 <toolkit>/skills/1_base/draft/haipipe-draft/cli/page.py adopt <page-folder>... [--plan <draft.md>] [--dry-run]
python3 <toolkit>/skills/1_base/draft/haipipe-draft/cli/page.py check-page-folder <page-folder | board-folder>... [--json]
python3 <toolkit>/skills/1_base/draft/haipipe-draft/cli/page.py inspect <page-folder>
python3 <toolkit>/skills/1_base/draft/haipipe-draft/cli/page.py build <page-folder>
python3 <toolkit>/skills/1_base/draft/haipipe-draft/cli/page.py export <page-folder>... [--lane web|latex|word|all] [--author "<Your Name>"]
python3 <toolkit>/skills/1_base/draft/haipipe-draft/cli/page.py open-run <page-folder> --kind <kind> [--slug] [--target] [--goal] [--by]
python3 <toolkit>/skills/1_base/draft/haipipe-draft/cli/page.py close-run <page-folder> <run> [--summary] [--by]
python3 <toolkit>/skills/1_base/draft/haipipe-draft/cli/page.py run-names <page-folder>... [--dry-run]
python3 <toolkit>/skills/1_base/draft/haipipe-draft/cli/page.py serve <page-folder>
```

The rest of § File → Page Folder → work (after `setup`, hosting, the standalone server, Scratch, the Draft authority, the two response modes): [ref/file-to-page.md](ref/file-to-page.md)

## 📁 What a page is on disk

The Task folder on one page, its parts and their writers, and the header lines a server reads: `ref/folder.md`
(it replaces the retired `haipipe-folder` skill, JL 261016).

For a Task that writes, **Task Folder = `tNN_<task>/`;
a Task may hold a draft**. The same-stem Markdown, `draft/`, `workflow/`, `scripts/`,
and `runs/` belong to that one Folder. Do not create a Page Folder beneath the
Task Folder; the parent `jNN_<job>/` remains only the Job container.

**A draft Task keeps three sibling folders, one writer each** (JL 261016: "in the folder of the draft-task, we
should have the subfolder of draft, evidence, and display"): `draft/` (the words; this skill), `evidence/`
(`cards.yaml` and `proposals.md`; haipipe-evidence) and `display/` (one unit per figure or table; haipipe-display).
Display reads `evidence/`; the draft reads both and writes neither. A Page made before 2026-10-16 keeps its evidence
in `draft/<stem>-evidence-items.md` and `results/` until it is moved.

```text
tNN_<task>/
├── tNN_<task>.md
├── draft/       haipipe-draft      plan · scratch · text
├── evidence/    haipipe-evidence   cards.yaml (CITE, VALUE) · proposals.md
└── display/     haipipe-display    Display<n>-<slug>/ (built_on: evidence cards)
```

The rest of § 📁 What a page is on disk (the full tree, the Folder symmetry, Page Evidence, the derived README) and § 📄 The Draft Markdown and Runs beside the content: [ref/page-folder-layout.md](ref/page-folder-layout.md)

## 🧬 One owner claims the Page Face (Page Types are self-owned, Paper Pages, a variant extends the base): [ref/page-face.md](ref/page-face.md)

## 🧭 The plan's steps

The plan (page context, the Structure Run, Scratch) is `haipipe-draft-logic` since 2026-10-16 (s41-D12); this skill keeps the door.
Pages: `../haipipe-draft-logic/ref/context.md`, `structure.md`, `scratch.md`, `context-record.md`; the generator `cli/context-record.py` stays here.

## 🎭 Page Run Workflow, independent of Folder kind · 🧬 Writing DNA handoff: [ref/run-workflow.md](ref/run-workflow.md)

## 📑 Two sections on stage, and nothing else · 🎯 Backstage target records: [ref/page-face.md](ref/page-face.md)

## 🚪 Preview · create · work on · run

```text
👁 PREVIEW    /haipipe-draft preview <page>                 read verb, writes nothing
📄 CREATE     /haipipe-draft create a new page on <topic>   [on <board>]
🔧 WORK ON    /haipipe-draft working on <page>              or just the path
🧑 RUNS       /haipipe-draft runs <page> [focus]            propose human interaction
🔁 RUN        /haipipe-draft run <page> [from <operation>]
🪜 STEP       /haipipe-draft <task> structure | write | revise | deliver | check     one step tab's prompt
```

A STEP verb is one tab's prompt (the seven steps above); text after the colon and its `user feedback:` line
are the person's notes for that step.

The RUN `from` selector accepts the existing Page controller operation names
(CONTEXT, OUTLINE, EVIDENCE, CONTENT, CHECK); its parser/API may retain the
field name `run`. This help wording does not add a Run-id selector.

**Preview**: `cli/preview.py <page>` prints one screen (title, the Opening's
visible paragraph, the Aims with their `Now:` lines, the Content divisions,
the last log record); a group or board folder prints one roster line per
page. A gist, never a substitute for the whole-file read.

### 🔗 Open the rendered Page · 👀 User check packet: [ref/open-page.md](ref/open-page.md)

**Create from file**: follow `ref/standalone.md`; no Board/group is required.

**Create authored Page**: resolve a Board/group only when membership was
requested · pick the id and copy `ref/page-template.md`, never
retype the shape · a three-to-five-word title stating the purpose · the
Opening as one visible paragraph above the first blank line · Content as
numbered parts, each with a caption, a figure and a short intro · Aims with
their `Now:` lines · `draft/records/<stem>-files.md` with any Related Board Page row
the current Run needs · register in `board.md` only if requested · build, check, read the
RENDER, report the finding count.

**Interactive work on**: when the person asks what interaction is needed, use
`fn/runs.md` and do not allocate before selection. A direct bounded
sentence/paragraph feedback request is already a selection: resume a matching
open Page Run or allocate the next typed Page-local RP for an independent goal.
When the person enters or resumes an open Run before giving feedback, return
the pre-Step review packet with the complete selected paragraphs separated by
visible `### PNN · Cn.Pm` blocks, `s1...sn` labels, proposed next Step number,
review scope, and the three direct links;
do not create a journal Step yet. After feedback arrives, resume current
decisions and affected sources; make the narrow patch in the Draft file only
(feedback and result records wait for the Run's close), refresh the live Draft Space, and return the saved passage. Do
not write Page Content, refresh delivery, wait for export/browser verification,
or use the broad repair/build loop below for that request.

**General Page work on**: ONE page is the deliverable. Read the whole file and its
`draft/` first; if the files record declares Related Board Pages, load the
one-hop packet from `cli/pagecontext.py <page> --run <run>` · run the
checker and fix the mechanical findings in bulk · then read for what no
checker reaches (the weak-English axis, one question per part, an Opening that
says more than the title) · a rule nobody wrote down goes in three places (the
owning page, `ref/page-template.md`, this file) · build, check, read the
render, report before and after counts · a write outside the target page only
when the page cannot be made correct without it, named file by file · never
rewrite a sibling page's content.

**Run**: human-feedback writing uses the persistent profile above. For automated
Run work, the bounded loop lives with `haipipe-draft-workflow`.
The dispatch stays in the session you typed it in: a subagent is not handed
the `Workflow` tool. A new page is CREATEd first (Board registration is optional) and RUN starts
at CONTEXT; an existing page with no known next authority starts at CHECK.

```bash
python3 <toolkit>/skills/1_base/draft/haipipe-draft/cli/preview.py <page>
python3 <toolkit>/skills/1_base/draft/haipipe-draft/cli/check.py <board-folder> | grep '^<PAGE>'
python3 <toolkit>/skills/1_base/draft/haipipe-draft/cli/check.py <board-folder> --summary
python3 <toolkit>/skills/1_base/draft/haipipe-draft/cli/check.py --rules
```

`--rules` prints every finding code with its message; read the laws before
writing, not from the error text after.

## ✍️ What a write may touch

For substantive Page prose, load this skill and
`haipipe-draft/ref/writing-rules.md` directly before writing; a copied checklist
in a prompt is a second authority and drifts. Technical file intake and code
edits use `ref/standalone.md` instead; do not apply scholarly title, sentence,
language or figure rules to imported HTML/code or its generated wrapper.

- **Formal delivery finishes on the rendered Page.** Build/check and inspect
  the required projection before calling it current. A routine Writing Step
  saves/reads only the live Draft Space candidate. A Page Run close seals
  its text, Bullets, and Evidence contract but leaves Content and delivery
  unchanged. Only the Page-level release after all required Runs are complete
  adopts Content and refreshes web/LaTeX/Word. Human approval and write scope
  remain binding.
- **An accepted process ruling lands in its owning skill when a skill update
  is requested.** Apply it only to Pages within the authorized scope; a skill
  update does not regenerate every Paper. Local writing preferences stay in
  the Writing history until promotion to a wider rule is explicitly approved.
  The Page receipt names the exact skill version used.
- **The write anchor rule**: a machine write lands at a section boundary,
  never at a byte offset; appending under a named `##` heading is safe.
- **The human-decision rule**: a machine updates an Aim's tick only from
  evidence it can inspect; a person's ruling is transcribed with the quote
  (`approved: ✅ JL 260831 0146 · in chat: "…"`), never decided.
- **The form rules, each owned once**: the title is a functional label, not a
  headline. Use three to five visible words in sentence case, never six
  (`writing-rules.md`; `title-too-long`), and name the Page's subject plus the
  work or deliverable it owns. Keep it objective and concrete: do not put a
  joke, marketing phrase, surprise, accusation, or unqualified finding in the
  title. Prefer `[subject]: [operation or deliverable]`, such as
  `NPI2Photo: screening physician photo URLs`; put results, caveats, and
  interpretation in Opening or Content, where scope and denominators can be
  stated. Before writing, ask whether a new reader can tell what the Page does
  from the title alone and whether the wording claims more than the evidence
  supports ·
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
  fresh reviewer judges formal Page completion, not each local feedback Step.

## ✍️ Drafting prose

Drafting and revising prose, the sentence contract and the WRITE step are `haipipe-draft-writing`; read its `SKILL.md` first.
Judging the text is `haipipe-draft-review`. `cli/wdiff.py` (word-level change record) stays here.

**No semicolons in draft sentences (JL 261104: "don't use ';' make them as the normal sentences").** Write two or
three plain sentences instead, and put a parenthetical's two facts in two parentheses or two sentences. Only a list
whose form someone else fixes keeps its semicolons: citations in parentheses, and journal statements such as an
affiliation list. `haipipe-draft-review` `cli/anti_slop.py` flags the rest (rule `semicolon`). Statistics inside one parenthesis keep theirs, `(SE = 1.07; 95 percent CI, 0.69 to 4.90; p = 0.009)` (JL 261104: "could we use ';' here? as long as it is not the sentence").

**No transition set off by commas (JL 261104: "don't use things like ' , however ,', Try to make a sentence to be smooth").** Write `But a request names...`, not `A request, however, names...`. The same holds for `, therefore,` and its kin. `cli/anti_slop.py` flags them (rule `parenthetical-transition`).

## 🔍 How a page is judged

Evaluation asks whether the authored page satisfies its declared
requirements, never whether the reviewer likes the format, and the
requirements resolve in this order: this contract and `ref/page-template.md`
→ the Folder-owned Page Face or declared Page Type → the selected Run profile
and Page controller operation → the page's own
authored W records in `draft/records/<stem>-requirement.md` (and `## Stage Contract` on S) → the local division
purpose and each paragraph's job line. A more specific source refines a
broader one and never silently contradicts it; a conflict is reported and
that criterion is not judged until the owner resolves it. The rubric (four
axes, four verdicts, the review units, the batch-voice test, the report row)
is `haipipe-draft-review/ref/page-check.md` §📏; `check.py --strict` supplies the
mechanical half, the page's `✅ Quality Check` runs the rubric in the page
chat, and `haipipe-draft-check-agent` runs it in a fresh context.

## 🔤 The words

Every term this family uses is defined in `ref/glossary.md` beside the path it
names: Context record, plan, Bullet, Evidence Item, Supporting Run, Local
Input, local Run, Result, availability, next action, Run, and receipt. Load
it when a reader asks what a word means or when you are about to coin one;
`writing-rules.md` forbids a phrase that is neither the source's own wording
nor defined where a reader can find it.

## 🏷 How a location is written

```text
page        QB4            #QB4
face        QB4a           a page whose id carries its parent's number
group       #group-QB      scrolls the index, opens nothing
sentence    QB8's grammar  haipipe-draft-writing owns everything below the section
bullet      C3.P7.B4       division 3, Page paragraph 7, Bullet 4; a sentence names it with realizes:
thread      D07            board-wide, cited from any page
```

Every id inside a fenced figure renders as a link.

## 🗣 Showing prose changes in a reply (JL 261113)

A reply never shows proposed or changed Draft prose as a paragraph (a quote, an indented block, a fenced
passage). JL 261113: "never return the things like this … Make it the same to the index in the UI, sentence by
sentence, and also show what changes you made compared to previous. You can report paragraph by paragraph."
Report it paragraph by paragraph, one line per sentence with the address the workbench shows (`C<n>.P<m> ·
<title>`, then `B<k> · s<n>` as in § 3 of the Draft), a mark (✅ kept, ✏️ changed, ➕ new, ➖ cut, ↪ moved) and,
for a changed sentence, its before and after in full, against a named version. The format and its example are
`response-format` § Prose changes: sentence by sentence, by address. The revise record (`draft/records/<stem>-revise.md`)
names each sentence by the same address, so chat, record and page agree.

## ✅ Closing checks

**The final gate (JL 261102: "I think /haipipe-draft should do this final checklist before saying it is finished").** Before any reply says a draft Task is finished, done, complete or ready, run `page.py health --final <task>` and paste its rows. It is `health` with nothing left to wait: Content that differs from the current draft, a stale export and a missing step file fail instead of warning, and its `printed` check reads the built `latex/<stem>.pdf` back (pdftotext) and fails if any § 3 sentence is not in it. Only a person's own step (the sign) stays a warning, named so it is not forgotten and never ticked by the agent. A FAIL means the reply says what is still open, never "finished".

The `health` rows (`paragraph`, `expect`, `title`) and the other closing checks: [ref/closing-checks.md](ref/closing-checks.md)

## 📂 Files

```text
haipipe-draft/
├── SKILL.md            this contract
├── fn/serve.md         host one Page Folder and route Board hosting
├── fn/runs.md          propose Page Runs needing human interaction
├── fn/check-page-folder.md  is a Page Folder on the latest layout? names the fix
├── ref/page-checklist.md  configuration, four-section and delivery acceptance
├── ref/page-run-families.md  RP/RE/RD and Evidence Item/Result/Card/Label contract
├── ref/glossary.md     every word this family uses, with the path it names
├── src/evidence_labels.py  shared token grammar and Result-label resolver
├── ref/user-check-packet.md  the four-surface reader-facing completion packet
├── ref/draft-steps.md  a draft Task's seven steps and the Plan gate
├── ref/page-runs.md   Page Run names, bookends, adoption, RP kinds
├── ref/file-to-page.md  after setup: hosting, standalone server, Scratch, Draft authority
├── ref/page-folder-layout.md  the full Page Folder tree and the Draft Markdown
├── ref/page-face.md   who owns the Page Face, the reader sections, Aims
├── ref/run-workflow.md  Page Run Workflow, Writing DNA, the authority test
├── ref/open-page.md   open the rendered Page, the user check packet
├── ref/closing-checks.md  the health rows and the other closing checks
├── cli/wdiff.py        word-level diff and the anchored change record (test: tests/test_wdiff_roundtrip.py)
└── CHANGELOG.md        version history, and the only home for retired rules
```

Owns `ref/page-template.md`, `cli/page.py`, `src/` and the shared `live/`
Page presenters. Board `ref/board-form.md` §4 remains the shared frame
reference during extraction. Board `cli/preview.py` and
`cli/pagecontext.py` live with the machinery. The lifecycle packet and receipt
spec belong to `haipipe-draft-workflow/ref/page-run-contract.md`.
