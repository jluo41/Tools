# HAIPipe Paper Handoff — 2026-07-25

Status: **active design and implementation handoff**. This replaces the 2026-07-18 handoff.
The Paper Board is the durable source of decisions and open work; this file is the compact entry
point for a fresh Codex or Claude Code session.

## Objective

Make HAIPipe Paper a compact, Board-first lifecycle system that a fresh session can operate from
one page without reading a previous transcript:

```text
Paper Board
  → choose one S page and one ready item
  → haipipe-paper-stage resolves the stage contract
  → a bounded worker performs the work
  → the result, verification, state, and handoff return to that same page
  → CHECK stops at a visible human gate
```

The Board is the control plane. Sessions are replaceable workers. The paper, its queues, comments,
decisions, previews, and handoffs must remain understandable after any session disappears.

## Read first

Read these in order:

1. `diagram/01-haipipe-paper-260725/board.md` — topic, pipeline, and the complete list of Pages.
2. The **one Q page you will work on** — read it completely, especially `Items to Finish`,
   `Where we are`, and `Law`.
3. `../0_utils/haipipe-board/SKILL.md` — Board grammar and same-turn write-back rules.
4. `1-lifecycle/haipipe-paper-stage/SKILL.md` — only if the work touches stage execution.
5. `diagram/01-haipipe-paper-260725/CODEX-SUGGESTIONS.md` — historical consolidation and proposed
   execution sequence; useful context, but not a runtime contract.

Do not begin by loading every Q page or every stage contract. The Board index chooses the page;
the stage router chooses exactly one stage.

## Current Board

Path:

```text
Tools/plugins/haipipe-toolkit/skills/paper/diagram/01-haipipe-paper-260725/
```

Current shape:

```text
34 Q pages
├── 2  ✅ SETTLED
├── 31 🟡 PARTIAL
└── 1  🔴 OPEN
```

The Q groups are:

| Group | Owns |
|---|---|
| QA | skill package, live paper folder, family layers, compact skill anatomy |
| QB | stage, DPRC phases, human gate, page grain, venue alignment |
| QC | authored Content and LaTeX/Word/HTML projections |
| QD | PROBE evidence boundary, spending ceiling, placeholders |
| QE | stage contract form and fresh-agent acceptance |
| QF | shared Board/Paper page ownership, dependencies, state, creation |
| QG | Board control plane, executable queue, in-item handoff, page-first runner |
| QH | Content structure, sentence unit, semantic attachments, hover preview |
| QI | Display ownership, render contract, renderer families, format adapters |

Settled rulings:

- `QC2`: Board tooling owns filenames and resolves pages from stable family + unit identity.
- `QF2`: the S page's explicit `requires:` is the authoritative dependency declaration.

Everything else must be treated as provisional until its page reaches `✅ SETTLED`.

## Design laws already established

1. **Board, not CLI, is the user-facing control plane.** A CLI may remain an internal execution
   mechanism or recovery path.
2. **The section is `## Pages`.** Older `## Roster` boards remain readable only for compatibility.
3. **One independently gated lifecycle unit has one canonical S page.** Display and Section can
   have many pages because their units gate independently.
4. **Board owns the page shell and filename; Paper owns stage-specific Content composition.**
   `haipipe-paper-stage/create-page.py` composes the two.
5. **`## Content` contains the stage's real product.** Contracts, status, queues, comments, and
   provenance have their own lanes.
6. **`## Items to Finish` is the page's executable queue.** Do not create a request file for each
   change.
7. **A completed item's handoff stays on that item.** For a live stage, do not create
   `_DISPLAY_REQUEST.md`, `DISPLAY_REQUEST.md`, or a separate Handoff sidecar.
8. **Evidence enters Paper only through PROBE.** Paper does not recompute values or conduct its own
   literature search; Task and Discovery own those evidence artifacts.
9. **Display meaning stays with the consumer; reusable rendering belongs to Display; low-level
   drawing engines belong to Utils.** A Section points to a stable `display_id`.
10. **One authored Content source projects into HTML, LaTeX/PDF, and Word.** These are adapters,
    not three manuscripts maintained by hand.
11. **Only a human may pass CHECK.** An unattended worker may prepare the gate but cannot write the
    approval.
12. **One writer owns one page at a time.** Different pages may be worked concurrently.

## What exists now

- The Paper Board has the full QA–QI question architecture and builds successfully.
- Board terminology has been migrated from `Roster` to `Pages` across active boards, docs, UI, and
  Paper integration. Legacy parsing remains.
- `haipipe-board` is at working-tree version `0.22.0`.
- `haipipe-paper-stage` is a single router for all eight lifecycle stages:
  `seed · resource · claims · venue · pitch · narrative · display · section-edit`.
- `haipipe-paper-stage/create-page.py` exists and delegates page shell and managed contract creation
  to `haipipe-board/stage.py`.
- Board stage contracts support explicit `requires:`, `style-from:`, and `provides:` plus stale
  contract detection and explicit sync.
- All seven active Boards were rebuilt successfully after the `Pages` migration.
- A fresh-context agent successfully created and rebuilt a Board using `## Pages`.

The `Tools` repository is currently on `main` with substantial **uncommitted** Board and Paper
work. Preserve it. Do not reset, restore, mass-reformat, or use `git add -A`. Inspect scoped diffs
before editing.

## What is not finished

These capabilities are designed on the Board but are not yet complete:

- the frozen queue-item schema and claim/release behavior (`QG2`);
- the compact in-item handoff syntax and writer migration (`QG3`);
- the page-first stage runner and worker routing (`QG4`);
- Board actions for **Work this item** and **Work this queue** (`QG1`);
- sentence roles and sibling checks (`QBa3`);
- citation/value/Display attachment grammar and failure behavior (`QBa4`);
- citation/value/Display hover cards (`QBa5`);
- reusable Display request/result schema and package boundary (`QI1–QI3`);
- semantic table and document adapter interfaces (`QI4`, `QC3`);
- final Paper skill compaction and live paper scaffold (`QA2–QA4`);
- a real Paper stage run from a clean context (`QE2`);
- a real section rendered to HTML, LaTeX/PDF, and Word;
- an end-to-end run on an actual paper. The Paper stage skill itself records this as its acceptance
  test.

Do not report those as implemented merely because their Q pages describe the intended design.

## Recommended continuation order

```text
QG2 queue contract
  → QG3 in-item handoff
  → QG4 page-first runner
  → QG1 Board controls
  → QE2 fresh-agent acceptance

QBa3 sentence unit
  → QBa4 semantic attachments
  → QBa5 hover previews
  → QC3 multi-format projection

QI1 ownership
  → QI2 render contract
  → QI3 renderer packaging
  → QI4 adapters
  → QC3 multi-format projection

QA2 family layers
  → QA3 compact skill anatomy
  → QA4 live paper scaffold
```

Recommended next page: **`QG2-items-are-the-queue.md`**. Freeze the queue contract before writing
runner code or Board buttons. After QG2, continue to QG3; the runner must not invent either
contract.

Independent sessions may work on the QG, QH, QI, and QA chains concurrently, but two sessions must
not edit the same Q page or the same implementation file at the same time.

## Session working protocol

For every continuation session:

1. Read this handoff and `board.md`.
2. Select one Q page; announce the exact page before changing files.
3. Read that page completely and work only its unchecked `Items to Finish`.
4. Inspect existing uncommitted changes in every file you intend to edit.
5. Update the real implementation or contract; do not only rewrite the Board's proposal.
6. In the same turn, update the owning Q page:
   - check only items actually verified;
   - replace `Where we are` with current truth;
   - record a concise `Log` entry when useful;
   - change `state:` only when its finish conditions justify it.
7. Rebuild the Board.
8. If any skill changed, run a fresh-context agent test as required by repository `AGENTS.md`.
9. Stop at a human ruling, spend authorization, unresolved dependency, shared-file collision, or
   CHECK gate.

Do not create a new Q, design note, request file, or handoff file when an existing owning page can
hold the work. Add an item or comment to that page instead.

## Validation

Rebuild the Paper Board:

```bash
python3 Tools/plugins/haipipe-toolkit/skills/0_utils/haipipe-board/build.py \
  Tools/plugins/haipipe-toolkit/skills/paper/diagram/01-haipipe-paper-260725
```

Validate the Board skill after Board changes:

```bash
python3 /Users/jluo41/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  Tools/plugins/haipipe-toolkit/skills/0_utils/haipipe-board
```

Check changed source before handoff:

```bash
git -C Tools diff --check -- \
  plugins/haipipe-toolkit/skills/0_utils/haipipe-board \
  plugins/haipipe-toolkit/skills/paper
```

For a skill revision, static checks are not sufficient. Give a fresh-context agent a realistic
task, inspect whether it invoked and followed the skill correctly, revise if needed, and repeat.

## Copy-paste prompt for a new session

```text
Continue the HAIPipe Paper Board work in:
Tools/plugins/haipipe-toolkit/skills/paper/

First read:
1. /Users/jluo41/Desktop/Physician-SPACE/AGENTS.md
2. Tools/plugins/haipipe-toolkit/skills/paper/HANDOFF.md
3. Tools/plugins/haipipe-toolkit/skills/paper/diagram/01-haipipe-paper-260725/board.md

Then select exactly one existing Q page from the Board and read it completely. Start with
QG2-items-are-the-queue.md unless I name another page. Work its unchecked Items to Finish,
inspect and preserve all existing uncommitted changes, update the real implementation plus the
same Q page, and rebuild the Board.

The Board is the control plane; sessions are replaceable workers. Use ## Pages, not Roster.
Do not create request or handoff sidecars when an owning page exists. Do not infer dependencies
from Pages order. Do not claim designed capabilities are implemented without testing them.
Do not let an agent pass a human CHECK gate.

If you revise a skill, validate it through a fresh-context agent before calling it complete.
Do not commit, push, reset, restore, or mass-stage unless I explicitly ask.
```

## Handoff boundary

This file hands off the **Paper skill and its design Board**, not one live manuscript. Work for a
specific paper belongs on that paper's S pages and queue items. Update this file only when the
cross-session entry point, continuation order, or system-wide state materially changes.
