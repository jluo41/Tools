This file holds the Page Face contract: which owner claims it, the two reader sections and the backstage Aim records, moved from `SKILL.md`.

## 🧬 One owner claims the Page Face

A property every Page carries cannot tell one Folder kind from another. A Page
shows something, cites something, states a number; so display, literature and
value are workbenches. A Run Workflow/Run Spec owner or declared family skill owns
the Folder kind and its Page Face. A fixed Page Type may own a Page directly. No
`folder-kind:` or `page-type:` key is the flexible base.

Resolve ① to ⑥ in order and stop at the first key that matches. Exactly one
semantic owner may claim the Page Face. An in-place Folder's
`workflow/folder.yaml current.folder-kind` is authoritative; fixed-kind Folders
use Page `folder-kind:`. `page-type:` is the declared Page Type when no current
Folder kind exists. If current
state and Markdown disagree, fix the Folder, never the resolver.

```text
step  machine-readable key                    Page Face owner    contract
──────────────────────────────────────────────────────────────────────────
①     workflow/folder.yaml current kind        Run Workflow       Run Spec owner
②     frontmatter `folder-kind: <key>`        Run Spec/family     Run Spec/family skill
③     frontmatter `page-type: <key>`          Page Type           Page Type owner
④     filename QBv<n>-                        venue              for-venue
⑤     filename S-<Family>-<unit>-<slug>       stage              for-stage
⑥     filename Q<group><n>[<face>]-<slug>     Q decision         base only
```

A Discovery Folder resolves `folder-kind: discovery` to its Discovery workflow
Run Spec owner. Its Task Face does not select the Task Folder technical-report
grammar: the Discovery Run Spec owner owns that Page Face, while `haipipe-task` owns only
`folder-kind: task`.

### Page Types are self-owned

Each current Page Type declares its own shape and owner in its Page-Face or
workflow skill. `check.py` validates the `page-type:` value against the
engine's current set and the resolver loads the owning contract directly.
There is no central inventory, compatibility layer, alias table, or Page Type
without an owning contract. A retired key must be migrated or removed from the
Page; it is not kept alive by a second document.

### Paper Pages

For a Paper Page, follow the [Paper routing contract](../../../../2_theme/paper/haipipe-paper/SKILL.md#-routing)
and load the exact self-owned Ideation, Story, Section, Round or Venue skill.
For `page-type: ideation`, that is `haipipe-paper-ideation`; it delegates idea
semantics to `haipipe-ideation` and keeps Page projection/release here. General
Page work does not load Ideation or every Paper skill. Read the
[Paper–Page adapter](../../../../2_theme/paper/haipipe-paper/ref/page-integration.md) when a
Paper Run or release is planned. At a Paper G4 Section CHECK, the Page CHECK
owner also applies the section-scoped `SUB-*` rows from the Paper
submission-readiness reference; cover-letter and whole-manuscript rows stay at
Paper level. The same owner is loaded only once.

### A variant extends the base and never redefines it

A Page Face specialization defines Content and fixed extension points without
reordering the base frame. In a migrated family it lives with the Run owner
or canonical family skill that owns the Folder kind; an unmigrated Page Type
remains a base variant under `page-types/`. Load the semantic owner before
writing. After moving a skill, re-run `install.sh --global` so the installed
symlink follows it.
For `folder-kind: task`, the canonical Folder owner remains `haipipe-task`;
its `ref/task-page.md` § Displays adds the Task Page's display-rich table,
figure, and diagram contract. It refines the Task Page surface and never
creates a second Page frame or execution owner.

## 📑 Two sections on stage, and nothing else

The reader-facing Page order is `Opening → Content`. Outline, Aims, Stage
Contract, Files, Discussion, Log, and other process records live in the Page
Folder and are shown only by their owning Draft, Evidence, Run, Delivery, or
Folder surfaces. `check.py` may still inspect those records, but their presence
must not add another main Page section.

```text
#   section    conveys · the reader question                 Run authority              omit
────────────────────────────────────────────────────────────────────────────────────────────────
1   🚪 Opening what is this page, why should I care?         CONTENT defines and clarifies      never
2   Content    what does this page actually establish?       CONTENT writes and builds          Q may · S never
```

Each section answers one reader question, and a sentence answering another
section's question is misplaced: substance in Opening moves to Content.
Inherited inputs and venue move to backstage contract records, page-owned prose
rules to authored W records in `draft/records/<stem>-requirement.md`, intended
outcomes to backstage target records, current facts to their Run/CHECK
receipts, and a question for a person to a `D<nn>` record.
There is no `## Boundary` section: what a page covers is the Opening's job,
stated as a `**Covered elsewhere**:` part in its drawer.

There is no reader-facing `## Outline` projection. The current plan's `▤ Outline
table` remains available in Draft Space with `Address · Bullet · Feedback ·
Evidence · Supporting Run · Local Run`; C/P rows are planning group headers and
B rows are the checkable claim/evidence rows. The compact reading projection
shows the Point statement, not the plan's process-only `Note:` annotations.
The `draft/` folder remains the authority for every plan, writing rule,
evidence, feedback, requirement, discussion, file, and log record.

The live Outline/Draft Space makes each paragraph address (`C<n>.P<m>`;
`P` increases once across the whole Page and never resets at a new `C`)
an expand/collapse control and keeps its Bullets inside that group. It is a
read-only projection: each Bullet keeps its bracketed role label and any
compact Evidence route, while Bullet heads, candidate wording, comments, and
new Bullets are not editable from the rendered page. Page/Run workflow writers
update the selected Outline Markdown; the next GET re-reads that one file.
Markdown remains authoritative: a workflow write against an approved
Shape creates the next unapproved working Shape and preserves the approved
file; subsequent writes reuse that working version. Generated Page HTML is
never an edit target.

The visible reader labels are `🚪 Opening` and `📚 Content`; they must not reuse
one icon because they answer different reader questions. Draft/Outline is a
separate owning Space, not a third reader section. Opening is reader prose, not
an internal ledger: a bare claim, Evidence, or Run address is forbidden there.
Name the subject in plain English first and keep any address only as a
secondary compact handle, such as `primary total-MME association
(Claim1.TotalMME)`.

A manuscript `page-type: section` tightens the reader surface: `🚪 Opening`
renders exactly one paragraph and has no reader drawer. Its page-owned prose
rules live as authored `W<n>` records in `draft/records/<stem>-requirement.md`, after
its generated venue `V<n>` records. The Outline workbench exposes both through
one `📏 Requirement` lens to CONTEXT, OUTLINE, CONTENT, and CHECK. The Section
product source carries no `### Writing Style`; post-paragraph notes and Stage
Contract remain source-side and do not appear on the manuscript review
surface. Other Page Types retain the ordinary Opening drawer when they need it.

## 🎯 Backstage target records: one Aim is one row

The Page Face does not render targets as a third reader section. When a
workflow uses Aim records, the legacy `## Aims` syntax remains the record
shape: one Aim is one row with its tick, target, `Done when:` test, and `Now:`
fact. The plan carries 🎯 marks that name these backstage rows and no rows of
its own.

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
