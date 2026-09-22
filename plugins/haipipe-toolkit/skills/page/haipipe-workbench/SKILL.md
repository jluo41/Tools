---
name: haipipe-workbench
description: >-
  The WORKBENCH contract of a Page: every Page-material subfolder is
  rostered, while one category workbench may own several internal storage lanes.
  A workbench is defined by STORAGE, SURFACE, WRITER, and BOUNDARY.
  ref/roster.md is the single list of material names. Trigger: page
  workbench, workbench folder, workbench roster, workbench tab, add a workbench,
  /haipipe-workbench.
metadata:
  version: "1.12.2"
  last_updated: "2026-09-22"
---

# /haipipe-workbench · a page's material, as one contract

`haipipe-page` owns what the page's `.md` SAYS; this skill owns what sits BESIDE it.
A page lives in its own home folder (QPf1 on the design board), and every
Board-material subfolder is ROSTERED. A roster row may be an internal lane
owned by a category Workbench; folder count and Workbench count are not required to
match. A Workbench is defined ONCE by four things, and `ref/roster.md` is the
single list of material names.

## 🧩 The four things a workbench is

```
📦 STORAGE   what files live in <page>/<name>/, named by the page's stem
🖼 SURFACE   its tab in the Page host's right pane, framing the material live;
             served by servers/workbench-<name>/ (the WORKBENCH), never by the skill
✍️ WRITER    the ONE tool allowed to land files there
🚧 BOUNDARY  board discovery never enters a workbench folder
```

A category Workbench meets all four directly. An internal lane inherits the
category's surface while retaining its named storage, writer, and gate. A
folder absent from the roster is not Board material and the checker may warn.
Adding a new top-level Workbench is one roster update plus one drawer
registration—the shell is never edited for it.

Two words, two things: a **workbench** is the lane a Page owns on disk and the
contract an agent writes to (`haipipe-workbench-page` says what `outline/`,
`runs/`, `results/` and `delivery/` hold); a **workbench** is that lane's
served face in the browser (`plugins/haipipe-toolkit/servers/workbench-page`
renders them). They pair by name, `haipipe-workbench-<x>` with
`servers/workbench-<x>`, and never swap roles; the servers tree's `README.md`
lists the pairs.

## 📦 Storage

Material lands in its rostered lane, and artifacts carry the page's stem. A
standalone lane uses `<page-dir>/<lane>/`; a category-owned lane uses its real
nested address, such as `outline/evidence/bibex/` or `delivery/latex/`.
PRIMARY lanes hold originals a person makes (draw, chat): they are committed
and only their category-owned writer edits them. Meetings are project/SPACE
records owned by `haipipe-project-meeting`, never current Page material.
DERIVED workbenches hold projections of the page's own text (slide, latex, word,
citation workbench): they regenerate on demand, a hand edit is overwritten on
the next build, and the folder is safe to gitignore.
A flat page (no home folder yet) may use a board-level compatibility fallback;
folded pages are the norm and every current writer lands at its canonical lane.

## 🖼 Surface

The surface is a tab in the split shell's right pane. On a page's first visit,
the strip shows every applicable category Workbench in registry order and opens
the declared default. After that, the persisted open-tab set wins; the top
Workbench picker is how a reader reopens a tab they closed.
The active tab carries its own ✕: closing removes that tab only and closing the
last tab puts the whole pane away. The pane has no duplicate close control;
Escape hides it without changing the open-tab set.
That ✕ is a separate button with at least a 36-by-36-pixel touch target; its
pointer and click gestures must not activate the tab underneath it.
The open-tab set persists per page, so a reader returns to the pane the way they left it.
Neither the default tab nor a stale, no-longer-applicable entry may be restored
by repainting or selected as the close action's replacement.
Frames are hidden on switch, never destroyed — a live session or editor survives being put away.
Closing is always safe by construction: a derived view has nothing to lose, an editor saves on edit, and a chat turn survives its reader through the ring.

## ✍️ Writer

Each workbench names one writer in the roster, and everything else asks it.
Each host registers the same `{id, label, hint, order, applies, open, tab}`
shape. Board Pages use `servers/_host/assets/js/10-drawer/05-workbenches.js`; standalone Pages
receive their applicable registry from the Page server and use the compact
Page-owned pane. `order` fixes the reader-facing sequence independently of
asset load order. A host omits a Workbench whose real presenter or writer is not
available; a disabled imitation is not applicability.
Server-side builders live as one `live/` module per concern and one `/_board/<workbench>` route (`servers/workbench-studio/autodeck.py` and `/_board/autodeck` are the slide's pair).

## 🚧 Boundary

Discovery (`src/common.py`) never surfaces a workbench folder's files as pages, so a `chat/` transcript full of `.md` can never become ghost pages.
The `session:` line and the page's own text stay `haipipe-page`'s; this contract begins at the folder.

## 🗂 The roster, and each workbench's own skill

`ref/roster.md` is the single list: name · kind · storage · surface · writer · status.
Every optional surface, including the Page Runs stepper, appears in the one
Workbench picker. A surface may use its own panel layout after opening, but that
never creates a second top-level menu.
A generic Page Workbench's OPERATING knowledge lives in one of exactly two
public skills beside this one in `skills/page/`: `haipipe-workbench-page` (the 📃 Page
tab with its Run Space, the 📤 Delivery tab, and the 📂 Folder tab: everything
`servers/workbench-page` renders) or `haipipe-workbench-studio`. Internal lanes
live as references under their owning category skill; they never mint
duplicate callable skills. Page owns Citation/Bib, Value, Display, the ranked
Skill record, Run Space (`ref/run-space.md`), LaTeX, Word, Slide, and Render
(`ref/delivery.md`), and the Folder inventory (`ref/folder.md`); Studio owns
Chat and Draw. PageX is legacy migration input only.
Every other workbench skill lives in the family that owns its lanes and its
writer, never in the Page family: `skills/design/haipipe-workbench-design`
(the Design Folder; the Design Board grain is its `ref/design-board.md`),
`skills/insight/haipipe-workbench-insight` (one InsightBoard page; the board
grain is its `ref/insight-board.md`), `skills/paper/haipipe-workbench-paper`
(the Paper Board), and `subjective-label`'s `haipipe-workbench-labeling`. Each
pairs by name with `servers/workbench-<x>`; a workbench that serves two grains
keeps the board grain as a ref, never as a second top-level skill, and none
promotes an internal lane to a duplicate top-level workbench.
One lane inverts the shape: `haipipe-workbench-page/ref/folder.md` is the 📂 meta-surface over the roster itself — no subfolder, no storage, no roster row (JL 260816).
This contract stays the base every one of them loads on top of; the board pages (`QPf2`-`QPf8`) stay the design records; the engine keeps only routes and machinery.

## 🗂 Outline's three workspaces and the Run door (260913)

A unit folder has TWO PARTS. The UPPER, page part has one combined
`outline/` planning authority and one visible surface with exactly **Draft
Space + Evidence Space + Run Space**. Context and process records
stay on disk and are inspectable through Folder, but do not compete as a
visible workspace. Evidence Space is Result-first. Run Space contains
Run P, Run E, and Supporting Runs. It also has two
presentation CATEGORY folders that group lanes without changing their grammar,
writer or gate — `delivery/` (latex · word ·
slide · render — what leaves the page) and `studio/` (chat · draw — the
HUMAN's room: the person talks and sketches, and the chat may redraw on
their ask). The LOWER, Task-side material is
presented inside Outline as **Run Workspace**. A **Run P** uses three explicit
Page-local kinds: `rp-struct-NN` for Structure + Outline Bullets,
`rp-sec-NN` for Section-level writing, and `rp-para-NN_Pxx[-Pyy]` for fixed
paragraph/paragraph-group writing. The initial structure identity is
`rp-struct-01`; the presenter preserves interactive human-feedback
Version/Step history. A complete Section draft → review/rating → diagnose →
revise cycle is one Step inside its Run; a later independently commissioned
Section session gets a new `rp-sec-NN`. A **Run E** is a Page-owned Evidence attempt with
`re-value-NN_<slug>`, `re-display-NN_<slug>`, or `re-cite-NN_<slug>` as its
typed identity. One RE Result/Card may expose many `$V_xxx$`,
`\figure{D_xxx}`, `\table{D_xxx}`, and `\cite{C_xxx}` Labels. A
**Supporting Run** keeps its external owner-native identity; its owner retains
the authored Ticket and runtime internals while the Page inspects the generated
Result by logical Run address without copying it. The typed Page RP/RE and Task `rNN` counters are independent
and may both begin at 01 in one Folder. A standalone/Discovery Folder stores both projections at
its root; a canonical Task Page stores the ticket inside the Task and its
generated Result at the containing Job's `results/<task>/<run>/`. A custom
Labeling dialect keeps Ticket and Result receipt in its authority-owning
round/evaluation/production/audit folder while preserving the same logical Run
address and receipt contract. `scripts/`
(any language, with optional `config/` inside) is supporting material only when
reusable local code exists; many Runs call a skill, CLI, API, or worker with no
scripts lane. The ticket is the ONE execution door under the simple-code law.
Computational projections may be regenerated under their owner's Run rules.
Interactive writing Results also contain irreplaceable human feedback and
accepted wording: never treat them as a disposable cache or regenerate their
completed Steps/Versions. Results are never evidence merely by existing, and
become Page evidence only when an Evidence Item/RE Result binds them. There is
no Evidence storage lane under `outline/`; the Outline owns the Item contract,
while `runs/` and `results/` own execution and payloads. Rows and physical
dialects: `ref/roster.md` and `haipipe-workbench-page/ref/run-space.md`.

For a Board Page, the Evidence Item contract is in the authored
`outline/<stem>-evidence-items.md`; its Supporting Run and Local Run references
resolve directly through the owning `runs/` and `results/` records. There is no
`outline/evidence/supporting-runs/` binding lane. Actual page-local execution stays at the
sibling `runs/` (Tickets) and `results/` (paired generated Results). `⚙️ Runs`
presents Page-owned writing history plus the output side of allocated
Supporting Task Runs, while `📃 Page → Evidence Space` owns why
each output is needed and any unallocated route.

## 🔌 The two workbench kinds, and the tab bar they make (260831)

A LANE contract owns one rostered folder's LAW—storage grammar, the one
writer, and the gate. For generic Page material it is an internal reference
owned by its category, never a second Workbench skill.
A CATEGORY workbench owns one SURFACE over a whole category. It may delegate a
lane to another contract or own it directly: `haipipe-workbench-page` owns the
CITE, VALUE, and DISPLAY Evidence Item contracts and their read-only
presentation; the Run producer owns the Result payload. PageX is retired and
must be moved to the migration archive. A storage lane therefore does not
require a duplicate Workbench or Skill. Outline now presents exactly three
reader-facing Spaces—Draft, Evidence, and Run—while Context stays off-stage;
Delivery and Studio remain category surfaces:

```text
📃 Page      haipipe-workbench-page       Draft + Evidence + Run over the
                                       outline/ process; FIRST/default tab
🎨 Design    haipipe-workbench-design     Goal · Design · Insight · Run · Delivery
                                       Spaces over one current Design Page-Folder
📤 Delivery  haipipe-workbench-page       latex · word · slide · render — the
                                       🎞 segment carries the deck's ✨ pen
🎨 Studio    haipipe-workbench-studio     chat + draw AS ONE PAGE: the drawing
                                       above, the chat below, both live — the
                                       scene the chat redraws changes in front
                                       of the person talking. Both tools keep
                                       every rule and pen they had
📂 Folder    haipipe-workbench-page       the roster itself, the meta-surface
                                       (ref/folder.md; Delivery is ref/delivery.md)
```

The reader-facing Workbench picker follows one fixed sequence for applicable
entries:
📃 Page · 🎨 Studio · 🎨 Design · 📤 Delivery · 📂 Folder · 🏷 Labeling.
Optional entries still keep their assigned place when applicable;
an unassigned third-party entry follows these in stable registration order.
On every source-backed Board Page, Run Space remains visible inside Outline
even when neither lane has an allocated Run; each lane has a truthful empty
state and does not create empty `runs/` or `results/` folders. `🏷 Labeling` is a
domain extension and follows its own applicability rules. Skill is an internal
Outline record reached through Folder inspection, backed by the nested
`outline/skill/` store, so it has no duplicate top-level
picker row. Neither Evidence nor Probe has a skill or a top-level picker entry:
Evidence is an internal Outline workspace and Probe is retired history.
No lane sells its own strip row; the shell's
old 💬, 🖌 and 🎞 rows folded 260831 (stored tab sets migrate on load). The
260815 refusal of "full chat under the canvas" bound the DRAW tab; the
studio room is both tools', by JL's 260831 ask.
