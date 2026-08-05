board — Changelog
=================

Family-level changes. Skill implementation history remains in
`haipipe-board/CHANGELOG.md`; agent history remains in `agents/CHANGELOG.md`.

## 2026-08-04 · Phase-scoped Related Board Pages

- Adds one typed Files group for precise Page-to-Page context by relation,
  current Page Phase, Page id, and whole-Page or Content-division scope.
- Adds a one-hop reader and checker integration so cycles stay bounded and dead
  targets, wrong ids, missing scopes, malformed rows, and path escape fail
  before an agent silently works without required context.
- Carries the rule through QB4, the template, Board form, Page and Board skills,
  the Page RUN raw-material packet, generated Skill mirror Pages, and focused
  fault tests.

## 2026-08-04 · Page RUN, receipts, and lifecycle audit

- Adds the third Page verb, `RUN`, as a bounded non-linear router rather than a
  linear `ADVANCE` command.
- Adds the common packet/receipt contract, Board-owned Workflow and deterministic
  auditor, branch/fault tests, and the Page orchestrator agent.
- Preserves the core separation: producer writes, builder versions, reviewer
  judges, controller routes, and a human alone supplies any required human gate.

## [0.7.0] — 2026-08-04

- Adopts the Page Type × Page Phase structure ruled on QB9.
- Moves the stable `for-stage`, `for-skill`, and `for-venue` variants under `page-types/` without changing their globally unique skill names.
- Replaces the four stage-shaped phase names with `haipipe-board-page-draft`, `-probe`, `-revise`, and `-check` under `page-phases/`.
- Wires the base Page and Board door to resolve type and phase independently, and keeps `ADVANCE` deferred until a real router needs it.
- Keeps `haipipe-probe` as the shared Q-consumer, Q-executor, A-executor, and A-consumer crossing protocol.

## [0.6.0] — 2026-08-03

**A full diagnose-first review of the bucket** (`/haipipe-skill-diagnose`), 27 findings across 6 skills and 2 agents, all fixed in one round.

One root cause produced most of them: **the specs were changed this week and the changes were not carried back to the door, the agents, or the READMEs.** The door still taught the old page-creation procedure, both agents still enforced the pre-override Aim form, and both READMEs still drew a folder layout that moved on 260801.

Two rulings were taken rather than asked (JL: "go ahead to solve yourself, dont ask me"):
- A page-kind VARIANT ships **where the board family MAINTAINS it**, replacing "under its consumer, never here", which no longer described either variant.
- The status strip follows the CODE, not the older spec; `SKILL.md` and three tests were the leftovers.

Also: `skills/_console/` did not exist, though `/haipipe-skill-diagnose` has written its ledgers there since v1.3.0. Created, with a README. The test suite went from 4 failed / 87 passed to **91 passed**.

## [0.5.0] — 2026-08-02

- **New unit: `haipipe-board-page-for-skill/`**, the VARIANT of `haipipe-board-page`
  for the two skill and agent page kinds, `Skill-<n>` and `Agent-<n>`. It loads the base and never
  restates it, then adds what a skill page needs: an Opening that introduces a unit
  instead of asking a rhetorical question, the derived-versus-authored split across
  the three managed spans, `state:` as a health judgment rather than a version, Aims
  as the unit's own open work including defects other pages route in, and the
  retirement procedure.
- It ships BESIDE the base rather than under a consumer family, which is the declared
  exception to the variant rule: for these two kinds the consumer IS the board family.
- Opened because five skill and agent pages on `01-boardform-260722` had Openings from one
  template and JL caught it by eye. The base could not have prevented it: its
  noun-substitution test was already on the books, but its Opening shape asks what the
  page decides, and a skill page decides nothing.
- Versions: `haipipe-board` 0.110.0, `haipipe-board-page` 0.11.0,
  `haipipe-board-page-for-skill` 0.1.0.

## [0.4.0] — 2026-08-02

- **`haipipe-board-index/` is removed from the family and merged into
  `haipipe-board-routing/`** (JL: "maybe merge, I will do B"). The family is now
  one door, two specs, and one verb, plus two agents.
- Three of the retired unit's five verbs were other units' work written a second
  time: `propose` and `materialize` are `haipipe-board`'s `open` action,
  `regroup` wrapped `haipipe-board/cli/regroup.py`, and `check` was a subset of
  `haipipe-board/cli/check.py`. `src/lanes.py` was the only code held nowhere
  else and moved to `haipipe-board-routing/src/lanes.py`.
- What the merge bought, and the reason it beat deleting the unit outright: a
  finding about a whole GROUP had no landing rule and stayed in chat, because
  routing resolved pages only while the block such a finding belongs in was
  owned by the other unit. One unit owning both altitudes settles it.
- Versions: `haipipe-board` 0.109.0, `haipipe-board-routing` 0.9.0.

## [0.3.0] — 2026-07-26

- Compressed the direct Board closing block from ten fenced lines to three
  Markdown lines while retaining Board, queue/focus, status/mode, next action,
  and a clickable deep link.

## [0.2.1] — 2026-07-26

- Defined direct-versus-composed Closing Block precedence so a Paper session
  carries one block with a deep Board link rather than two competing tails.
- Corrected the checker boundary: checkbox/state alignment belongs to Q
  rulings; an S page's emoji is its independent lifecycle gate.

## [0.2.0] — 2026-07-26

- Added a visible session-attachment contract: every Board-attached reply ends
  with a deterministic strip showing Board, queue, focus, mode, next action,
  deep link, and file.
- Kept live status in each session transcript rather than a shared status file;
  durable outcomes continue to sync into Board pages.

## [0.1.1] — 2026-07-26

- Unified the Board family on one state contract: the first emoji is the four-value machine status and optional following text is human-readable detail.
- Aligned the mechanical checker with runtime Board routes and the renderer's normalized state token.

## [0.1.0] — 2026-07-26

- Promoted Board from `skills/0_utils/haipipe-board/` to the first-class
  `skills/board/haipipe-board/` family beside paper, probe, and task.
- Kept the design Board at `skills/diagrams/01-boardform-260722/`.
- Added the family-level, read-only `haipipe-board-reviewer-agent`.
