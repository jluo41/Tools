board — Changelog
=================

Family-level changes. Skill implementation history remains in
`haipipe-board/CHANGELOG.md`; agent history remains in `agents/CHANGELOG.md`.

## 2026-09-04 - Task Blocks become Boards

- Define Board as a kind-selected Page container rather than only a
  question/stage collection.
- Add the explicit `task-block` dialect: Block = Board, Job = Group, Task =
  Page, and Run remains an execution record.
- Align Task scaffolding, hierarchy references, Board parsing/rendering, and
  structural checks around one disk-tree authority with relative Task paths.

## 2026-08-21 — skills audit sweep · rulings that never left the file they landed in

A full read of `board/` + `probe/` (30 SKILL.md, 4 rules files, 6 phase agents,
the controller, the roster, the checkers). Every serious defect had the same
shape: a decision made once, written into ONE file, and never propagated. Fixed
in this sweep, worst first:

- **The 260818 two-field tick split reached one file out of four.** `checked:`
  existed only in `approve-rules.md` R10, while `approve-rules/README.md` — the
  section the approver is told to read for the grammar — still gave the retired
  single-field shape, and the agent's own `description:` still promised
  `approved:` / `verified` / `read:` / `accepted:`. Dispatching it would have
  written a person's tick. Rules files, README and agent (0.3.0) now agree.
- **`value-rules.md` R6 failed legal cards**: four states named against the
  plugin's eight, so any `deferred`, `failed`, `concern` or `answered-local` card
  failed on its first run.
- **`cli/pagecontext.py` could serve four of seven phases.** `--phase OUTLINE`
  errored and `--phase PROBE` silently returned EVIDENCE's scope, because a
  260816 rename alias outlived the 260817 split that made them different
  authorities — while the workflow contract requires that call before EVERY
  phase dispatch. `src/page_context.py` now carries all seven, the alias map is
  empty rather than wrong, and the row regex is derived from the constant it had
  drifted from.
- **Three files told a cold agent to read a page-type deleted on 260819.** The
  reviewer and creator agents pointed at `haipipe-page-for-skill/SKILL.md` and
  `haipipe-plugin-meeting` at `haipipe-page-for-meeting/SKILL.md`. The skill
  page's inverted Opening rule survives in `cli/skillpage.py` and `cli/check.py`,
  which is where they point now.
- **`board/README.md` was three rulings behind**: "six Page Types" (twelve ship),
  "the FIVE variants this skill set owns" naming four of which three were
  deleted, and `page-workflows/` as four members when six ship. Also gained the
  approver bullet, the `approve-rules/` tree, and a note that skill-name
  uniqueness rests entirely on `install.sh` pruning `_archive/`.
- **`haipipe-page-probe` restated `haipipe-probe` §①②③ near-verbatim** and had
  already grown a sixth bullet mark (`🔗 PageX`) that the mark authority never
  carried. Three mirrored sections → one delta section (0.10.0).
- **`haipipe-probe` did not implement its own newest ruling**: 0.14.0 recorded
  "only `haipipe-probe-q-executor-agent` may cross" and §③ still described a
  direct bank call, never naming the agent (0.17.0). Its `state:` list was also
  short by `answered-local`, the word `haipipe-plugin-probe` claims to borrow
  from it.
- **`ref/roster.md`** had no `outline/` row while `<page>/outline/` had been real
  storage since 260817 — against the file's own opening law — and its `probe/`
  row carried three retired words (`raised→working→bound`, `binding:`).
  `live/plugview.py`'s empty-state panel taught the same retired ladder.

Not fixed, reported only: `measured-cost.md` §OUTLINE (fast path, main session)
still contradicts `haipipe-page-workflow` §🧭 (an in-thread outline edit leaves
no receipt) inside one skill folder; `phase-cards.md` still calls `approved:` a
blocking exit; the controller's `LEGAL.OUTLINE` allows an OUTLINE→DRAFT edge no
contract names; `probe/haipipe-probe/test/run-checker-tests.sh` points at a
script that no longer exists. Three `haipipe-board` tests fail at HEAD, unchanged
by this sweep (`test_aims_state`, `test_home`, `test_status`).


## 2026-08-15 · The display plugin gets its skill; the roster catches up

`page-plugins/haipipe-plugin-display/` joins draw, latex, and word (JL 260815:
"we might have the page-plugins in skills/board/page-plugins"). Display is the
first FAMILY-WRITER variant: its writer is a routing decision across five
renderer kinds plus the human `accepted:` tick, which is exactly the knowledge
a roster row cannot hold and QPf5 could only hold with the board open. The
skill owns the page-side delta (unit address, kind→renderer routing, the
five-step walk, the `> Display:` evidence lane) and cites the display family's
unit contract verbatim, never forking it. The roster's stale `display/` row
(DERIVED · planned · declared) is corrected to MIXED · 🟢 built 260815, and
`probe/` gets its missing row (🟡 surface built; QPf9 aims open).

## 2026-08-15 · The slide variant retires; a deck is plugin material

`page-types/haipipe-page-for-slide/` leaves the family (JL, ruled on the design
board's QPf3): a page's talk lives at `<page>/slide/<page>-deck.html`, authored
by Claude through `/_board/autodeck` and regenerated on demand. `haipipe-page`
0.26.0 drops the `page-type: slide` resolution key. The board engine's reflow
deck writer (`live/deck.py`, `/_board/deck`) retired with it.

## 2026-08-09 · Five paper variants, and the dash rule corrected

The paper family gains four DASH variants (`for-dash-section`, `-value`,
`-display`, `-literature`) and `for-narrative`. Sixteen variants now ship across
three skill sets.

- A DASH is the rollup over one family that holds only what no single page in it
  can hold. It rules nothing, so it still takes NO human gate and is still never
  counted as settled.
- **It does declare `requires: S-Open-Venue`** (JL 260809: every dash considers
  the venue structure). This corrects `haipipe-page-for-stage`, which said a dash
  never takes `requires:`. That sentence conflated deciding nothing with needing
  nothing: a dash cannot rank a family without the blueprint, which is the only
  shared yardstick its members have. One of four real dashes already declared it.
- `for-narrative` is venue-ALIGNED and keeps the venue-free claim ledger as its
  own division, so a retarget rereads that division instead of rewriting it.

## 2026-08-09 · `page-types/` becomes per skill set

JL moved the five paper-specific variants to `paper/page-types/` and stated the
rule: **page-types are the page versions of a skill set**, so a variant ships
under the `page-types/` folder of whoever owns it.

```text
board/page-types/    for-stage · for-skill · for-meeting · for-slide · for-design
paper/page-types/    for-venue · for-section · for-display · for-literature · for-value
subjective-label/skills/page-types/    for-labeling
```

- `for-stage` stays on the board side deliberately: a stage page is a BOARD
  mechanism (the chain, the managed contract span, the human gate) that the
  paper and application families both instantiate. The five that left describe a
  paper's own artifacts.
- Supersedes two rules, both recorded so neither returns: "ships under its
  CONSUMER, never here", and "ships WHERE THE BOARD FAMILY MAINTAINS IT"
  (JL 260803), which held only while one family owned every variant.
- `subjective-label` had already done this before the rule was written, which is
  why its variant needed no argument to stay outside the board.
- ⚠️ **Moving a variant does not move its installed symlink.** Between the move
  and the reinstall, five skills resolved to a directory that no longer existed
  and silently failed to load. Re-run `install.sh --global` (repo root) after any
  folder move; it repoints and reports.
- Rosters corrected in `haipipe-page` 0.23.0, `haipipe-board` 0.126.0,
  `board/README.md`, and `paper/README.md`, which had also called `haipipe-paper`
  the family's only registered skill.

## 2026-08-09 · The page and sentence units drop the `board-` prefix

JL ruled the shorter names, so the three altitudes now read board, page,
sentence, one word each. Seventeen names moved on one stem:

```text
haipipe-board-page                     ->  haipipe-page
haipipe-board-page-for-<10 types>      ->  haipipe-page-for-<10 types>
haipipe-board-page-{draft,probe,revise,check}
                                       ->  haipipe-page-{draft,probe,revise,check}
haipipe-board-page-orchestrator-agent  ->  haipipe-page-orchestrator-agent
haipipe-board-sentence                 ->  haipipe-sentence
```

`haipipe-board-routing` keeps its prefix, on JL's explicit call, as do
`haipipe-board`, `haipipe-board-creator-agent`, and
`haipipe-board-reviewer-agent`.

- `haipipe-page-for-labeling` moved with the stem even though the
  subjective-label plugin maintains it, because a variant named after a base
  skill that no longer exists is a dangling name.
- Folders were renamed with the skills, so every folder still equals its
  `name:`. Skill discovery is recursive, so no install path changed shape.
- 158 live files were rewritten. `_old/` and `_archive/` keep the old names on
  purpose: an archived mirror page records the unit as it was named then, and
  the paper board's two `## Links` rows into `_archive/` were pointed back at
  those historical filenames.
- The five `Skill-*`/`Agent-*` mirror pages naming a renamed unit were renamed
  and re-synced with `skillpage.py sync --all`.
- No new checker finding. `01-boardform` went dead-href 16 to 0 and dead-link 9
  to 0; `01-haipipe-paper` went dead-href 43 to 40 and dead-link 36 to 33.

What this costs, recorded so nobody relitigates it: across the toolkit the
convention is `haipipe-<family>-<unit>`, so `/haipipe-page` and
`/haipipe-sentence` now read as peers of `/haipipe-paper` and `/haipipe-task`
rather than as units under the Board door. The names are shorter; the family
membership is no longer visible in the name and lives only in the description
and the folder.

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
- Replaces the four stage-shaped phase names with `haipipe-page-draft`, `-probe`, `-revise`, and `-check` under `page-phases/`.
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

- **New unit: `haipipe-page-for-skill/`**, the VARIANT of `haipipe-page`
  for the two skill and agent page kinds, `Skill-<n>` and `Agent-<n>`. It loads the base and never
  restates it, then adds what a skill page needs: an Opening that introduces a unit
  instead of asking a rhetorical question, the derived-versus-authored split across
  the three managed spans, `state:` as a health judgment rather than a version, Aims
  as the unit's own open work including defects other pages route in, and the
  retirement procedure.
- It ships BESIDE the base rather than under a consumer family, which is the declared
  exception to the variant rule: for these two kinds the consumer IS the board family.
- Opened because five skill and agent pages on `BoardSkillBoard-260722` had Openings from one
  template and JL caught it by eye. The base could not have prevented it: its
  noun-substitution test was already on the books, but its Opening shape asks what the
  page decides, and a skill page decides nothing.
- Versions: `haipipe-board` 0.110.0, `haipipe-page` 0.11.0,
  `haipipe-page-for-skill` 0.1.0.

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
- Kept the design Board at `skills/diagrams/BoardSkillBoard-260722/`.
- Added the family-level, read-only `haipipe-board-reviewer-agent`.
