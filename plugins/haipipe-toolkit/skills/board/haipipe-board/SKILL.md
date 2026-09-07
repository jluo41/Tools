---
name: haipipe-board
description: >-
  Open, create, inspect, build, serve, update, or close one Board. A Board is
  a declared work-object container that groups readable Pages and renders a
  browsable board/ site. Route work on one Page to haipipe-page and work on
  one sentence to haipipe-sentence. Trigger: board, open a board, add a
  question, close the board, 开板, 加一题, 关板, /haipipe-board.
metadata:
  version: "0.170.1"
  last_updated: "2026-09-06"
  # version history: ./CHANGELOG.md
---

# /haipipe-board · operate one Board

A Board is one source folder and one generated site. Its declared kind decides
how child work objects become Groups and Pages. Markdown is authoritative;
`board/` is always derived.

## 🧭 Route by scope

| Scope | Authority | What it owns |
|---|---|---|
| Folder | `haipipe-folder` | Page Face + Task Face base contract |
| Board | `haipipe-board` | container, Groups, Page roster, build, serve, aggregate close |
| Page | `haipipe-page` | readable frame, Folder-kind resolution, Page lifecycle entry |
| Page lifecycle | `haipipe-page-workflow` | `RUN`, phase routing, packet, receipt, stop conditions |
| Sentence | `haipipe-sentence` | comment, edit, card |
| Page lane | the matching plugin | Outline, Studio, Runs, Delivery, Folder, or domain lane |

One-Page work always routes through `haipipe-page`, even when invoked from the
Board. `haipipe-page` exposes the `RUN` verb; `haipipe-page-workflow` owns its
grammar. This skill supplies the renderer, checker, server, and deterministic
lifecycle machinery, but owns no Page phase.

## 🗂 Choose the Board kind

| `board-kind` | Membership | Projection |
|---|---|---|
| omitted / generic | Board Pages discovered from the Board tree | Q decisions and S lifecycle Pages grouped by `board.md ## Pages` |
| `task-block` | direct `jNN_*/tNN_*` Task tree | Block = Board, Job = Group, Task = Page, Run = execution record |
| `discovery-block` | direct `jNN_*/tNN_*` Discovery tree | Block = Board, Job = Group, Discovery Task = Page, Paper/Source Run = execution record |

A Task Block does not create another Task Page Type. Each Task Page declares
`folder-kind: task`; `haipipe-task` owns both faces of that Folder. A Discovery
Block keeps `folder-kind: discovery`; the Board only projects its BJTR tree and
does not replace Discovery's Page contract. Read `ref/board-form.md` when
creating or changing Board structure.

## 📁 Keep one source tree

```text
<board-folder>/
├── board.md                       Board identity, map, grouping, order
├── <N>-Q<group>-<slug>/           generic Board Group
│   └── <page>/<page>.md           one Page Folder
│       ├── outline/               Context, Bullet, Evidence workspaces
│       ├── workflow/              Page-phase receipts
│       ├── studio/                Chat and Draw
│       ├── runs/                  optional Run tickets
│       └── delivery/              rendered deliverables
├── diagram/                       Board-owned design context when applicable
└── board/                         generated site; never hand-edit
```

Boards created for a task, project, or paper normally live under that owner's
`diagram/<NN>-<topic>-<YYMMDD>/`. Skill-design Boards live under the plugin's
`skills/diagrams/`. The date records creation and never changes. Group-folder
numbers mirror `## Pages` order; Page identity never depends on that number.

Only create folders for lanes actually used. Do not create a parallel Board
registry: `board.md ## Pages` is the presentation registry, and the filesystem
under the declared Board kind is the membership authority.

## 🧾 Write the Board head once

```markdown
# <plain-language Board title>
board-kind: task-block   # omit for a generic Board
spine: <the one problem this Board organizes>
close: <the observable condition that closes the Board>

## Topic
<bounded context for a new reader>

## Pipeline
<actual dependencies among Groups and Pages>

## Board Map
<optional ASCII relationship map; never a second roster>

## Pages
### QA · <group title>
<optional group introduction>
QA1-example.md
```

`## Pages` groups and orders Pages. It does not copy their titles, state, or
body. A Task Block may list only Job headings because the Task tree already
provides membership and default order. When it explicitly lists a Task, use
the Board-relative `jNN_<job>/tNN_<task>/tNN_<task>.md` path.

## 🔨 Use the smallest verb

| Request | Action |
|---|---|
| “preview this Board/Page” | `cli/preview.py`; read-only |
| “open this existing Board” | VIEW: rebuild, open the HTTP Board URL, report status |
| “create a Board” | OPEN: agree spine, close condition, and Page list before writing |
| “add a question/group” | update `board.md` and the source tree, then rebuild |
| “build/rebuild” | `cli/build.py <board-folder>` |
| “serve” | `cli/serve.py --root <repo-root>` using the repository server configuration |
| “update one Page” | route to `haipipe-page` |
| “run one Page” | route to `haipipe-page`, then `haipipe-page-workflow` |
| “comment/edit/card” | route to `haipipe-sentence` |
| “draw” | route to `haipipe-plugin-studio` |
| “compile/export” | route to `haipipe-plugin-delivery` |
| “close” | verify every Page and the Board `close:` condition |

Read `ref/operations.md` only for the selected operation. Do not load every
command recipe for an ordinary Board discussion.

## 🔁 Keep source and projection together

Every substantive change belongs to one Page or to `board.md`. In the same
round:

1. update the owning source;
2. update the owning Page's Aims and current `Now:` facts when their truth
   changed;
3. write the dated process record under `outline/<stem>-log.md`;
4. rebuild the Board;
5. run the checker and inspect the rendered result.

Do not write `## States`, `## Files`, `## Discussion`, or `## Log` on a new
Page. Current process records live under `outline/`; the Page surface remains
`Opening → Outline → Content → Aims` plus allowed optional folds.

A decision that blocks work is first written to the owning Page's
`Aims › Decision Now`; chat only points to that durable row. A decision the
agent is authorized to make should be made and recorded, not parked as a human
question.

## ✅ Close only observable work

| Page kind | Page may become ✅ when |
|---|---|
| Q decision | every Aim is met or explicitly held |
| S lifecycle Page | its declared human gate passed |
| canonical Task Page | P-B-E-R is terminal and the current `READING` gate passed |

The Board closes only when every Page is ✅ or explicitly ⏸️ and `close:` is
true. A successful Run, generated report, or finished Page draft never closes a
Task Block by itself.

## 🧭 Keep the session attached

In a direct Board session, end every user-visible reply with the exact block
printed by:

```bash
python3 <skill>/status.py <board-folder> \
  --focus <board|group:ID|PAGE_ID> \
  --mode <discussion|sourcing|implementation|review|status> \
  --status <ready|working|blocked|done> \
  --next "<one concrete next action>"
```

Page focus adds the Page lifecycle row. Board and Group focus do not aggregate
Page phases.

```markdown
🧭 BOARD · QUEUE/FOCUS (deep-link)
✅ done · implementation
⏱️ LAND · 🧭✅ 🧩✅ 🃏⏳ ✏️⬜ 🔍⬜ · ✋4
→ one concrete next action
```

An enclosing first-class workflow may provide one combined closing block. In
that case do not append a second Board block, but keep a deep `board:` link to
the active Page.

## 🌐 Resolve the surrounding SPACE narrowly

Before changing a Board, read its parent owner, repository root, and the
matching SPACE registry entry. A nearest `project.yaml` is the durable Project
identity; the Board kind groups Boards inside that Project. The SPACE registry
owns SPACE roots and public configuration, not Board membership.

Repository `.server_config/` is the primary hosting configuration. Never print
credentials or copy machine-local values into shared source. Update SPACE
configuration only when a SPACE-level fact changed; ordinary Board or Page
work does not mutate it.

The read-only SPACE Home is Project-first: nearest `project.yaml`, then legacy
SPACE-root `examples*/<project>/`, supplies the Project grouping; Board kind is
nested inside it. Canonical Blocks below `tasks/` render as Task Boards and
canonical Blocks below `discoveries/` render as Discovery Boards; one Block is
one Board, never one card for the entire bank. Canonical `*-DesignBoard`
folders render as Design Boards.
Fixture trees are excluded, and non-Project Boards remain visible in explicit
SPACE and Tools/Skills buckets. Home still discovers `board.md` from disk and
never writes a Board roster into Project or SPACE metadata.

## 🚫 Preserve these invariants

- Markdown is the only source; never hand-edit generated `board/` files.
- A build must remain readable after every `<script>` is removed.
- A compact Page Run link must land on the exact card in `Outline → Evidence
  Workspace → Runs`, preserving its Evidence Item and Run address even while
  the Page or plugin is still loading. A pending default refresh must not
  consume, discard, or overwrite that deep-link state; the normal route must
  not trap a mobile reader in a long popover.
- A compact Page Feedback link must land on the exact record in `Outline →
  Context Workspace → Feedback`; a rendered Feedback token is always
  interactive, never an inert badge.
- A compact Page Evidence chip must land on the exact item card in `Outline →
  Evidence Workspace → Evidences` through the same one-URL route
  (`lens` + `seg` + `focus`), scrolled into view and highlighted. The compact
  Page opens no Evidence popover and keeps no second copy of the item's
  fields; `none` and `missing` cells stay inert text with their reason on
  hover. The typed Evidence chip inside the Outline plugin's Bullet
  Workspace takes the same route to the same card, switching lens in
  place; it opens no popover either. A `Routed:` value may name several
  rows separated by spaces, commas, or semicolons, and every Feedback
  chip's focus id must equal a register record id.
- Archive moves source under `_archive/`; it never deletes the record.
- One Board has one `board.md`; do not create a second roster or `STATUS.md`.
- Page-local folders are plugins; a new folder name needs a real plugin owner.
- Compatibility readers may parse historical shapes, but no current writer may
  generate them.
- Historical rationale belongs in `CHANGELOG.md`, not this operating contract.

## 📚 Load details progressively

| Resource | Read when |
|---|---|
| `ref/board-form.md` | creating or restructuring a Board, Group, or Page roster |
| `ref/operations.md` | previewing, viewing, building, serving, moving, or closing |
| `ref/page-template.md` | creating a generic Q or S Page |
| `ref/writing-rules.md` | writing or reviewing Page prose |
| `ref/board-example.md` | a minimal current source-tree example is useful |
| `ref/page-lifecycle.workflow.js` | maintaining the deterministic Page runner; workflow law remains in `haipipe-page-workflow` |

Compatibility-only readers and schemas live under `ref/legacy/`. They are not
current authoring contracts.

## 🧪 Validate the result

```bash
python3 <skill>/cli/build.py <board-folder>
python3 <skill>/cli/check.py <board-folder> --summary
python3 <skill>/cli/pagetypes.py --check
python3 <skill>/cli/foldercontracts.py --check
python3 -m unittest discover -s <skill>/tests
```

After changing this skill, use a fresh-context agent to operate a realistic
Board from these instructions. A self-read in the authoring conversation is
not an acceptance test.

## 📂 Implementation map

```text
haipipe-board/
├── SKILL.md                 compact door and routing contract
├── ref/                     current schemas and conditional procedures
├── cli/                     current commands
├── src/                     build and audit implementation
├── live/                    server capabilities
├── assets/ + vendor/        generated-site dependencies
├── checks/ + tests/         acceptance and regression coverage
├── legacy/                  non-authoring compatibility utilities only
├── status.py                Board attachment renderer
└── CHANGELOG.md             history
```
