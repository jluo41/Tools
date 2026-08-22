## 0.15.0 — 2026-08-21

- **The 260818 two-field split finally reaches all four rules files.** R10 ruled
  that the agent writes `checked:` and a person writes `approved:`, and for three
  days it was written into `approve-rules.md` ALONE. `checked:` appeared in that
  one file out of the whole tree, while `approve-rules/README.md` § "What a pass
  looks like" — the section the approver is TOLD to read for the grammar — still
  gave the single-field `<verb>: ✅ auto <YYMMDD>` shape R10 had retired, and the
  approver's own `description:` still promised `approved:` / `verified` / `read:`
  / `accepted:`. Dispatching it would have written a person's tick, which four
  shipped contracts forbid. Now: README carries the two-field shape plus the
  per-artifact table of which human field each `checked:` sits under;
  `display-rules.md` gains R15, `cite-rules.md` R8 (bibtex syntax, `checked =
  {auto …}`), `value-rules.md` R9; the agent goes to 0.3.0 with `checked:` named
  in its description, its opening, its procedure step 4, a fifth ⛔ row, and a
  `human_tick:` row in the return contract.
- **`value-rules.md` R6 stopped failing legal cards.** It named a four-word
  ladder (`planned · commissioned · answered · read`) against the plugin's eight,
  so a `deferred`, `failed`, `concern` or `answered-local` card FAILED R6 on its
  first run. R6 now names all eight and points at `check-probe.py`, which had the
  right set the whole time.
- Glyph: README's four-files block called value-rules 🔢; 🧮 replaced it as the
  value mark on 260819 and 🔢 is the legacy alias.

## 0.14.0 — 2026-08-19

- **The producer's shared law moved out of the creator agent** into
  `ref/producer-contract.md`: packet, procedure, house rules, return shape.
  Every phase agent (and the fallback) now loads only CONTRACTS — no agent
  reads another agent's file any more, which was the one roster relationship
  JL could not hold ("is this for the board or for the page?").
  `haipipe-page-creator-agent` 0.10.0 keeps only its two verbs.
- **`haipipe-page-orchestrator-agent` → `haipipe-page-auditor-agent`**: it
  validates the packet, stores receipts, and runs the lifecycle auditor; it
  cannot dispatch the loop (subagents get no Workflow tool), so "orchestrator"
  named a power it lacks. The check agent's base stays the reviewer file until
  the judge side earns the same carve-out.
- Same-night thin-wrapper sweep: the reviewer's two route lists became pointers to page-run-contract.md § Legal routes (its old list allowed the illegal CHECK→COMPILE) and its no-card finding now routes to PROBE; the creator dropped the six-phase operation table (producer-contract.md holds it), restated its no-build rule as behavior rather than tooling, moved "drawing the unit" to EVIDENCE's walk, and un-mangled the `## Question` sentence; the approver's tick grammar became a pointer to approve-rules/README.md; the auditor's producer-roster paragraph was rewritten from the PRODUCER_AGENTS map; this folder's README redrew its roster, dispatch diagram, and Registration section from the now-existing `<toolkit>/agents/` symlinks.

## 0.13.0 — 2026-08-19

- **Two agents renamed to say what they are** (JL: "is this for the board or
  for the page? I am confused"): `haipipe-board-creator-agent` →
  `haipipe-page-creator-agent` (0.9.0) and `haipipe-board-approver-agent` →
  `haipipe-page-approver-agent`. Both are 100%% page-scoped — the creator never
  touches board.md, and every tick the approver checks lives on one page's
  artifacts. `haipipe-board-reviewer-agent` alone keeps `board`, because its
  board-wide jobs (mechanical checker, opening cold reads) are real. Old
  receipts naming the old actor strings stay auditable; CHANGELOG history is
  untouched. The broken root symlink `agents/haipipe-board-page-orchestrator-
  agent.md` (target renamed long ago) was deleted.

board agents: Changelog
========================

Agent-scoped history. Versions match the agent frontmatter.

## approver 0.1.0 - 2026-08-18

New agent, on JL's ruling that a human's job is to BREAK, not to approve.

- The cut: a rule that survives being written down belongs to an agent; a
  judgment re-made every time, because it depends on what a person wants,
  belongs to that person. Measured against this session: JL's six
  interventions on 260818 were all whole-artifact breaks and proposals, and
  not one was a mechanical check.
- Passes four of the five ticks against `approve-rules/<kind>-rules.md`:
  `approved:` `verified` `read:` `accepted:`. It refuses the fifth, the Page
  Type's RULING, which has no rules file because deciding a page's own
  question is the point of the page.
- The default is PASS. A person's 🛑 arrives afterwards, outranks every rule
  pass beneath it, and needs no rule to justify itself.
- It signs `auto`, never a person's name, and it may not pass work it
  produced.
- It PROMOTES a break into a rule in the person's own words, with a
  `promoted <date> from <who>'s break on <what>` stamp, so the same break
  never recurs. A break that cannot be written down is reported as a steer
  and adds nothing.
- Four questions it must refuse every time are named in the file, because
  answering one of them confidently is the failure mode it exists to avoid.

## orchestrator 0.3.0 - 2026-08-18

Dispatched as itself for the first time, and it cannot do the one thing it
was named for.

- Run `260818-1444-QPw00` on `QPw00-page-loop`: `blocked` at procedure step 2,
  0 steps, no receipt. The file declares seven tools and the running instance
  was handed four: `Grep`, `Glob` and `Workflow` were absent. **A subagent is
  not handed the Workflow tool**, so no charter wording can make this agent the
  dispatcher.
- It declined to shim the controller under `node`, and that was the right
  refusal: the controller needs `agent()`, `log()` and `phase()` as globals, and
  supplying `agent()` itself would have collapsed producer, builder and judge
  into one actor.
- DEMOTED to packet builder and receipt keeper. The MAIN session invokes the
  Workflow; this agent validates the packet before and stores plus audits the
  result after.
- The charter injected into the running instance was a PRE-0.2.0 copy of the
  file on disk, so same-session edits to an agent definition do not reach an
  agent dispatched in that session. Its third divergence was live: "Resolve
  paths before dispatch" reads as "make it absolute", which is the exact defect
  the 0.2.0 board-relative rule exists to stop.

## orchestrator 0.2.0 - 2026-08-18

The one documented call in this agent would not have worked.

- The procedure showed `Workflow({scriptPath: "..."}, <packet>)`, two positional
  arguments. The Workflow tool takes ONE object and the packet belongs in its
  `args` field. A second positional argument is dropped, so the controller
  would have returned `blocked · missing required raw-material packet field`
  with an empty packet: a call-shape error wearing a caller error's message.
  This agent has never been dispatched as itself, which is why nothing caught it.
- `page` MUST be BOARD-RELATIVE, stated with the run it broke
  (`260805-0216-QB8e`, absolute path plus the 260816 regroup).
- The producer roster is now all SIX phases, matching creator 0.7.0.

## reviewer 0.8.0 - 2026-08-18

The judge could not name three of the seven phases it is allowed to route to.

- `route:` was `CLOSE | REVISE | EVIDENCE | DRAFT | HOLD`, while the controller's
  own `REVIEW_RESULT` schema
  (`haipipe-board/ref/page-lifecycle.workflow.js`) accepts OUTLINE, PROBE and
  COMPILE as well. A judge that found a page built on an unapproved shape had no
  legal way to say so, and the nearest available word was DRAFT, which reopens
  the promise instead of the plan.
- `mechanical.errors` is now stated as PAGE-SCOPED in the return contract. The
  controller forces REVISE while that number is above zero, so a board-scoped
  count made CLOSE unreachable for every page whenever any one page had an
  error. On `BoardSkillBoard-260722` that was four foreign errors blocking all
  69 pages.

## creator 0.7.0 - 2026-08-18

The producer covered THREE of the six producer phases, and the controller
dispatches it for all six.

- `ref/page-lifecycle.workflow.js:300` hardcodes `agentType:
  'haipipe-board-creator-agent'` for EVERY producer step, while this agent's
  return contract declared `phase: DRAFT | EVIDENCE | REVISE`. So a run that
  routed to OUTLINE, PROBE or COMPILE dispatched an agent whose own schema could
  not name the phase it had just performed. Found by tracing what
  `/haipipe-page run QPw00` would do, before running it.
- The agent now covers OUTLINE, DRAFT, PROBE, EVIDENCE, REVISE and COMPILE.
- Operation names and phase names are now the SAME WORD, and the load table is
  an identity map. `create-page` and `revise-opening` stay as the two
  operations that are not phase names.
- ⚠️ `operation: probe` REVERSED meaning. It meant EVIDENCE, because PROBE was
  renamed to EVIDENCE on 260816; PROBE was split back out on 260817 as its own
  phase ③, so `probe` now means raise-the-card and `evidence` means land-what-
  came-back. A caller written before 260818 that sends `probe` meaning EVIDENCE
  will now get a card raised instead of an answer landed.
- Procedure step 6 names where each of the three non-body phases writes:
  OUTLINE writes only `outline/`, PROBE writes only `probe/PP<NN>-<slug>/`,
  EVIDENCE writes `bibex/`, a card's `answered` state and a frozen `intake/`.
  Each leaves its person-reserved tick UNTICKED.

## 0.6.0 / 0.7.0 / 0.1.0 - 2026-08-04

- Creator 0.6.0 gains one-phase `draft`, `probe`, and `revise` operations and
  emits the shared Page RUN receipt without rebuilding or judging.
- Reviewer 0.7.0 verifies one immutable source/render version and returns the
  authority route `CLOSE | REVISE | PROBE | DRAFT | HOLD`, including human-gate
  evidence and protection against producer self-approval.
- Adds Page orchestrator 0.1.0, the non-interactive dispatch target that runs
  the Workflow, stores its exact `_runs/page/` receipt, and invokes the
  deterministic lifecycle auditor without touching Page prose.

## 0.5.1 / 0.6.1 - 2026-08-04

- Repoints the Skill Page Type contract after the move to `page-types/`.
- The creator now loads DRAFT for a new Page promise and REVISE for an Opening change under fixed Aims.
- The reviewer loads the generic CHECK phase and any additional phase whose output it was asked to judge.

## 0.5.0 / 0.6.0 - 2026-08-03

**Board bucket review, 260803** (JL: "go ahead to solve yourself, dont ask me"). Ledger: `skills/_console/260803-board-bucket-review.md`.

- **Both agents failed a correct skill page for obeying its own contract.** The creator's house rules and the reviewer's check both demanded `A<n>` ids and a one-to-one Aim-to-State map, unconditionally. `haipipe-page-for-skill` overrides exactly that for Skill and Agent pages, and both agents predate the override. A creator that obeyed its own step 2 then broke its own house rule; the reviewer then reported a fault on a page that was right. Both rules are now conditional on the page kind.
- **The creator could be asked to create a page it cannot create.** Its declared output was "one new Q/S page", it has no Bash tool by design, and a Skill page can only come from `skillpage.py new`; a plain `Write` over a generated page destroys its managed spans, which cost one page its Aims, States and Log on 260803. It now refuses `create-page` for `Skill-`, `Agent-` and `Meeting-`, and may still revise an Opening or write the authored half.
- The creator no longer calls `## Question` a permanent alias; it leaves it, names it in the report, and says the checker flags it.
- Both source lists reach `haipipe-page-for-venue`, which shipped after both agents were last dated.

## 0.5.0 / 0.4.0 - 2026-08-02

**Both agents now load `haipipe-page-for-skill` for a skill page.**

That variant shipped earlier the same day and neither consumer was told about it. Six writers used it only because the dispatching session named it by hand in every packet, so the next dispatch without that sentence would have judged and written `Skill-<n>` and `Agent-<n>` pages against the base contract that explicitly does not fit them.

The two Opening rules are OPPOSITE, which is why silence here is not a small gap: the base ends its Opening on what the page decides, and a skill page decides nothing, so applying the base marks correct roster prose as wrong and passes the form letter the variant exists to catch.

- `haipipe-board-reviewer-agent` 0.4.0 -> 0.5.0: source 3, loaded WHENEVER a page under review is a skill page. The list renumbers to five.
- `haipipe-board-creator-agent` 0.3.0 -> 0.4.0: source 2, with an instruction to CHECK THE FILENAME before writing a word. The list renumbers to five.

The general lesson, which cost nothing here only because a person asked: shipping a variant is not done when the variant exists. It is done when every agent that loads the base knows when to reach past it.

## [0.4.0] · 2026-08-01 · haipipe-board-reviewer-agent

- Adds a Board-order batch voice gate after page-local review.
- Detects repeated sentence stems, repeated rhetorical sequences, cosmetic
  synonym swaps, and Openings that survive a sibling-subject substitution.
- Allows a locally clear page to fail when the changed batch reads like a form
  letter.

## [0.3.0] · 2026-08-01 · haipipe-board-creator-agent

- Adds explicit `create-page` and `revise-opening` operations while preserving
  the one-agent, one-page write boundary.
- Makes the creator load `haipipe-page` directly, read a revision target
  completely, edit only Opening, and self-check without approving its own work.
- Keeps prose requirements in the canonical skill and reference instead of
  copying a sentence formula into each assignment packet.

## [0.3.0] · 2026-08-01 · haipipe-board-reviewer-agent

- Loads the canonical page evaluation contract and resolves base, variant,
  page-local, Stage Contract, division, and paragraph-job requirements.
- Returns one evidence-bearing `MEETS | NEEDS WORK | N/A | NOT VERIFIABLE`
  verdict per present section and Content unit.
- Reports requirement conflicts instead of silently choosing a source.

## [0.2.1] · 2026-08-01 · haipipe-board-creator-agent

- Writes the canonical plural section label `## States`; each row remains one
  singular State record for one Aim.

## [0.2.1] · 2026-08-01 · haipipe-board-reviewer-agent

- Reviews `## Aims` against the canonical plural `## States` section.

## [0.2.0] · 2026-08-01 · haipipe-board-creator-agent

- Replaced the retired Boundary and Items-to-Finish writing contract with
  Opening scope, Content-linked Aims, and one factual State row per Aim.
- Reserved Decision Now and page-level gates for the human while allowing
  evidence-backed Aim State updates.

## [0.2.0] · 2026-08-01 · haipipe-board-reviewer-agent

- Reviews the one-to-one Aim-to-State id map and distinguishes individual Aim
  status from the page-level human gate.

## [0.1.0] · 2026-07-31 · haipipe-board-creator-agent

- Added the family's second agent, and the producer half of the creator and
  reviewer pair the rest of this toolkit already uses.
- Scoped it to exactly ONE page per invocation, so the caller fans out N of
  them in parallel instead of `haipipe-board` writing pages one by one
  (JL 260731).
- Made the parallel safety structural rather than advisory: no Bash tool, so it
  cannot run `build.py`; `board.md` is off limits, so the one file every writer
  would collide on stays the caller's; and no sibling page may be read, so two
  agents cannot start duplicating each other's judgment.
- Gave it the `siblings` field in its assignment packet, which is what lets a
  page write an honest Opening scope without reading the board, and what stops
  two pages claiming the same decision.
- Left every shared write with the caller: registering in `board.md`, the lane
  block, one rebuild, one check, and dispatching the reviewer.

## [0.1.0] · 2026-07-26 · haipipe-board-reviewer-agent

- Added the Board family's first agent.
- Made the role read-only: it runs the mechanical checker, cold-reads prose,
  checks for stale claims, and returns findings without editing the Board.
- Kept Board discovery, synchronization, repair, and rebuilding with the
  original session and `haipipe-board` skill.
