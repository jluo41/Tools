## 0.26.1 — 2026-09-04

- Define one canonical dependency order for every Page phase: Page base,
  router, phase, owning workflow, exact Page Type, phase policy, optional Run
  workers, then the Outline presenter.
- Distinguish phase `route` from cycle `next_cycle` in producer receipts.

## 0.26.0 — 2026-09-04

- Replace the two-part OUTLINE/DRAFT model with five numbered Page phases:
  `00 CONTEXT`, `01 OUTLINE`, `02 EVIDENCE`, `03 CONTENT`, and `04 CHECK`.
- Add the canonical detailed workflow table with exact inputs, skill chain,
  Outline workspace, L3 mutations, L4 Runs, exits, and backward routes.
- Make CONTEXT, OUTLINE, and EVIDENCE share `haipipe-plugin-outline` through
  Context, Bullet, and Evidence workspaces while preserving distinct phase
  authority.
- Replace active DRAFT/REVISE dispatch with one CONTENT/WRITE phase; Draft,
  Revise, Build, and Pre-check are internal movements.
- Remove PageX Bindings from the active evidence graph. Cross-Folder evidence
  now enters through Supporting Run Results; related Pages remain context.
- Keep stored DRAFT, REVISE, COMPILE, and PROBE receipts as compatibility
  inputs rather than new workflow outputs.

## 0.25.2 — 2026-09-03

- Route LAND through the current Outline-owned Evidence Workspace and remove
  the retired standalone Evidence plugin from the active chain.
- Align the person-reserved citation verification path with
  `outline/evidence/bibex/`.

## 0.25.1 — 2026-09-02

- Add the compact Evidence Item `Label` to SHAPE's cross-phase contract;
  immutable item ids and full readable names remain unchanged.

## 0.25.0 — 2026-09-02

- Add PageX to the Phase × Run Map as a SURVEY-planned, LAND-validated source
  binding. It has exact path plus accepted authority and is not counted in L4
  Run cardinality or typed Result cardinality.
- Tighten LAND closure to require valid Supporting Results and PageX bindings,
  one frozen Local Input, and one accepted local Result for every make-item.

## 0.24.0 — 2026-09-01

- Publish the concrete Phase × Run Map, including which L3 Task content each
  cycle modifies, exact skill-chain slots, and L4 cardinalities. SHAPE/SURVEY
  mint no Run; LAND executes Supporting Runs then one local Evidence Item Run.
- Remove `haipipe-page-for-task` from the active Page chain and route semantic
  policy directly to the owning workflow-phase skill.

## 0.23.0 — 2026-09-01

- TWO PARTS, six cycle WORDS (JL 260901): the OUTLINE part SHAPE → SURVEY →
  LAND → EMBED → SHAPE until the plan and its runs agree; the DRAFT part WRITE
  (draft → revise → compile chained, an inner loop of teeth + a fresh-context
  pre-check, budget 3, a finding surviving two rounds = HOLD) then CHECK. The
  ①-⑦ numbering and the PREPARE name retire from every contract; a cycle is
  never a letter code (`C<n>` is a Content division, `W` the Wisdom handoff).
- The law under the first part: every evidence number is answered by a RUN at
  a real tasks/ address; the run computes, the page interprets at EMBED; the
  item table `outline/<stem>-items.md` is the one ledger.
- PROBE retired with `/haipipe-probe` (both in `_old/`): MATCH → SURVEY's Run
  column, dispatch + the stake wall → LAND's outbound card, the cost ladder →
  the outcome words. `ref/phase-cards.md` rewritten per cycle; the run refs
  carry `cycle:` beside `phase:`, legal routes re-cut (DRAFT/REVISE → OUTLINE,
  no PROBE), PROBE reads as EVIDENCE in old receipts.
- A person's "no" at CHECK is routed like a finding and promoted into a rule.

## 0.22.5 — 2026-08-31

- Point phase-authored change records at `outline/<stem>-log.md`; a CHECK
  result still cannot mutate the version it just approved.

## 0.22.4 — 2026-08-31

- Make RUN Folder-first, including authoritative in-place identity from
  `workflow/phase.yaml`; Page Type/filename routing is compatibility-only.
- Point value evidence at the canonical Probe `proof/` directory, not the
  retired `answer/` spelling.

## 0.22.3 — 2026-08-31

- Make the owner RULING a deterministic phase-contract field instead of a
  universal fifth Page tick: `none` adds no gate, `domain-gate` reuses the
  workflow receipt, and `local` keeps a Page-local ruling. Legacy Pages retain
  their conservative auto-hardened gate.
- Put normalized `page_ruling` into the RUN packet and controller, keep the
  human-gate packet/receipt invariant, and make the owed ledger variable while
  preserving `sum(ticks_owed) == len(owed_ledger())`.

## 0.22.2 — 2026-08-31

- Canonicalize new Probe writes to `evidence/probe/`; flat `probe/` is a
  migration alias only.
- For phase-owned Folders, derive the Page owner RULING from the phase's Gate
  and Closure: mechanical gates add no human tick, while a human domain gate
  reuses one receipt instead of demanding duplicate approval.

## 0.22.1 — 2026-08-31

- `ref/phase-cards.md` ① and ④ aligned with `haipipe-page-outline` 0.12.0 and
  `haipipe-page-draft` 0.10.0: ① writes the plan, the open `D<nn>` records and
  one log record and exits on FIVE checks (⓪ ARC added; ④ SHAPE carries the
  head and Note law); ④ writes sentences ending `<!-- realizes: … -->` with a
  `> Value:` lane per number and no hole token, and one log record with the
  diff folded (the `States section` and `<HOLE>` are gone).
- §🧭 no longer forbids the in-session outline pass: a pass in the page chat
  that leaves the plan, one log record with the receipt folded under it and
  the strip is a pass; the section forbids a traceless edit and a
  self-judged version.

## 0.22.0 — 2026-08-28

- Two pre-dispatch duties before CHECK, priced on the SD02-roadmap live run
  (three serialized checks, ~27% of spend settling as tax): ① cure every debt
  the version itself registers before buying a cold judge — CHECK against a
  known-dirty version returns the page's own registration as a route; ② the
  producing phase's exit sweep is a mechanical pre-dispatch step, not advice —
  the one skipped sweep left a stale States clause and forced a third CHECK.

## 0.21.0 — 2026-08-21

- **`mode: copilot | auto` is in the packet, and the controller acts on it.**
  JL's "we will mainly check the outline and the evidences IF WE WANT" (260819)
  had never been a field: the loop had one shape, built for the attended case,
  so an unattended run met five person-reserved ticks and deadlocked on the
  first. One rule set, two readings — copilot BLOCKS on an unanswered human
  half, auto DEFERS it onto the ledger (`--owed`, 0.20.0) and keeps moving.
  Deliberately NOT two rule sets: every defect in the 260821 audit was one rule
  living in two files.
- **Auto defers four ticks and HARDENS the fifth.** `approved:` `verified`
  `read:` `accepted:` each have a rules file under `agents/approve-rules/`, so
  an approver can establish everything around them and write `checked:`. The
  Page Type RULING has none, on purpose, so `mode: auto` forces
  `human_gate.required` TRUE whatever the packet declared — a run nobody watched
  is exactly the run that must not certify itself. Auto's terminal HOLD is the
  DESIGN, not a failure, and its `reason` says so in those words.
- **The hardened gate is written BACK into the packet**, because
  `src/page_lifecycle.py` asserts every receipt's `human_gate.required` equals
  the packet's. A gate hardened only in memory would have failed the audit on
  its own receipt — the same class of bug the `parsed.page` normalization was
  written to prevent, and the comment there is what caught it before it shipped.
- Both the phase producer and the CHECK judge are TOLD the mode, because neither
  can infer it and both decide whether an unticked gate is a HOLD. `mode` is
  echoed on all five run results, so no stored receipt can be read without
  knowing which reading of the ticks produced it.
- Rejected values block the run rather than defaulting, and `copilot` is the
  default: the safe reading is the one you get by saying nothing.

## 0.20.0 — 2026-08-21

- **✋ stopped being only a number.** `cli/pagephase.py --owed` prints the LEDGER:
  one row per human tick this page still owes, each carrying the approver's
  `checked:` beside the question only a person can answer. `QPw00g-human-gate`
  has carried "no surface joins the five ticks" as an open ruling since 260819;
  this is that join. It reads only — it writes nothing and ticks nothing.
- **Why it is one mechanism and not two modes.** The same artifact serves both
  readings: in copilot you watch the list shrink and answer as you go; in auto
  the run does not stop and the list is what you are handed at the end. The
  alternative — a second rule set for unattended runs — is exactly the shape
  every defect in the 260821 audit had.
- **The count was short by one, on every unclosed page.** `ticks_owed` carried
  four entries while `phase-cards.md` § "The five person-reserved ticks,
  gathered" has always listed FIVE: the Page Type's RULING was never counted.
  `sum(ticks_owed.values())` now equals `len(owed_ledger(st))`, verified across
  144 real pages on two boards, and `tests/test_page_phase_ledger.py` (7 cases)
  asserts it — a count and a list that disagree are how a person stops trusting
  both.
- **Two smaller corrections that fell out of writing the rows.** `accepted:` now
  counts only DRAWN units, because an undrawn unit owes a render (EVIDENCE's
  machine work), not a person's act. And a bibtex `verified = {}` reads as OWED,
  which is what cite-rules R7 says it is — the explicit unverified form — where
  the old count matched on the field's mere presence.
- What each row ASKS is quoted from the matching rules file's `🚫 NOT rules`
  section, so the ledger points at the four rules files rather than restating a
  rule. The RULING's row says it has no rules file, by design.

## 0.19.0 — 2026-08-20

- **`ref/measured-cost.md`**: what each phase actually costs, from the 260820
  QC1 and QC2 runs (JL: "could you document for each of them, how long it takes
  for us?"). Minutes, tokens and tool calls per phase, with the finding that
  wall-clock tracks tool calls at ~14s each rather than tokens, so "why is this
  slow" almost always means "it is opening a lot of files". Also records the
  parallel display lane as the one real speedup: 16.8 min fanned out against
  43.2 min in sequence for the same four units.

## 0.18.1 — 2026-08-20

- **The bar reuses §🔁's phase emoji** (JL 260820: the circled digits were
  unreadable at terminal size). One symbol set across the loop diagram and both
  strip forms; ⑦ CHECK carries 🔍 in the bar only, since ✅ is the DONE marker.

## 0.18.0 — 2026-08-20

- **The phase strip also rides in the closing block**: a page-focused
  `status.py` prints the ⏱️ row, so a reply says which phase the page is in
  without a second command (JL 260820). Both forms read
  `haipipe-board/src/page_phase.py`, one computation, two surfaces.

## 0.17.0 — 2026-08-20

- **The phase strip** (JL 260820: "I want to have a status strip to show what
  phases we are in for the page workflow"): new `haipipe-board/cli/pagephase.py`,
  one row per phase ①-⑦ derived from disk (outline tick, card states, display
  previews, latex mtime) plus the newest `_runs/page/` receipt. `→ now` is the
  first failing exit test, a REPORT only; routing stays with the authority
  test. Documented beside the report-your-phase duty in §🧑. Sits with
  `status.py` (session) and `pagestatus.py` (group): three questions, three
  strips.

## 0.16.0 — 2026-08-20

- **§The fused ④+⑤ pass** (JL 260820: "按照你的这个方法去做吧"): a DRAFT
  whose promise is unchanged continues into REVISE in the same context, two
  receipt steps, typed return phase DRAFT route CHECK; a reopened DRAFT still
  runs alone. Measured saving ≈ one 50k-token agent boot per round.
- **Dispatch reads the ⚡ Brief first**: the controller's producer prompt
  points at the brief atop each phase contract; full contracts on demand.

- **§Effort tier per phase in the run contract** (JL: "看看哪里可以去优化"):
  measured on QPw00's first full loop, DRAFT at the session tier spent 77% of
  114k output tokens on thinking while executing an approved plan. OUTLINE and
  CHECK inherit the session tier; PROBE/EVIDENCE/DRAFT/REVISE/COMPILE run at
  'high' via `PHASE_EFFORT` in page-lifecycle.workflow.js.

## 0.15.0 — 2026-08-19

- **§🧭 gains the 🧑 LOOK gate** (JL: "the first check should be the outline
  check … it is good to have the human to have a look at outline and then do
  the probes and evidences"): every ① OUTLINE pass ends at HOLD with the plan
  rendered, and a person looks at the outline BEFORE ② PROBE or ③ EVIDENCE
  dispatch. The person's rulings are evidence the next ① pass folds in; the
  `approved:` tick stays the round's formal close, later and heavier.
- **260819 coherence sweep across SKILL.md and the three refs.** SKILL.md: §🔁
  redrawn as the PREPARE loop (①⇄②⇄③ with the 🧑 LOOK) then ④⑤⑦; the mark
  roster is 🎯 📮 🧮 📚 🖼; the hole ladder renumbered ②PROBE ③EVIDENCE
  ④DRAFT with the stake in the approved plan; render/pick/build moved to
  EVIDENCE everywhere it still said REVISE; a new page defaults to OUTLINE in
  §🧾; the card count is eight; the Files tree lists all three refs.
  producer-contract.md: `artifacts`/`evidence`/`findings` typed as JSON lists,
  `human_gate` added to the return shape, `actor:` signs the dispatched role,
  step 8 owns recipe/assets/preview, the duplicated stop sentence deleted, and
  the STAND-IN rule added. page-run-contract.md: orphaned receipt fragment
  removed, packet YAML dedented, COMPILE edges marked legacy-receipts-only,
  the human-gate match rule stated, and a field-by-field receipt table
  transcribed from `src/page_lifecycle.py`. phase-cards.md: the 🧑 LOOK gate
  drawn between ① and ②, coverage stated in both directions, and ② gating on
  the LOOK rather than `approved:`.

## 0.14.3 — 2026-08-19

- **The "no agent reads another agent's file" clause scoped to PRODUCERS** —
  the Display6 build agent caught it overclaiming: ⑦'s judge still reads its
  reviewer base until the judge ref is carved out. §👷 and
  `ref/producer-contract.md` now state the exception instead of hiding it, and
  `haipipe-page-check-agent` names the canonical `skills/board/agents/` home
  rather than the root symlink dir.

## 0.14.2 — 2026-08-19

- **The value mark is 🧮** (JL: "🧮 maybe this one?" — he never liked 🔢).
  🔢 stays accepted as the legacy alias, so pre-260819 plans remain legal.
  The abacus was the proof mark retired earlier on 260819 and is revived with
  its new meaning: a recomputable number, which is what `checks/values.py`
  does to every one of them.

## 0.14.1 — 2026-08-19

- §🧭 and §👷 caught up with their own carve-out: the shared producer law lives
  in `ref/producer-contract.md`, and the fold-back pass belongs to
  `haipipe-page-outline-agent` — both sections still said the creator agent
  held them. Found by the OUTLINE fold-back agent's receipt, which named the
  defect while obeying the corrected reading.

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

## 0.12.0 — 2026-08-19

- **⑦ gets its phase agent too: `haipipe-page-check-agent`** (JL: "could we
  rename haipipe-board-reviewer-agent to haipipe-page-check-agent?"). Executed as
  a SPLIT rather than a file rename, because the reviewer also owns board-scoped
  jobs (review board, cold reads, validate Q pages) that a page-phase name would
  misname: the new thin agent is the page-⑦ judge and the RUN controller's CHECK
  dispatch; `haipipe-board-reviewer-agent` (0.9.0) stays as its base and the
  whole-board reviewer. §👷's roster row and `page-run-contract.md`'s example
  receipt updated; the controller test now asserts the new dispatch name.

## 0.11.0 — 2026-08-19

- **New section §👷: one producer agent per phase.** JL: "for the creator-agent,
  it should have the outline-agent, etc." Five thin phase agents born under
  `page-workflows/agents/`; the RUN controller's dispatch now maps phase → agent
  (`PRODUCER_AGENTS` in `ref/page-lifecycle.workflow.js`), with
  `haipipe-board-creator-agent` (0.8.0) repurposed to the shared base plus the
  create-page / revise-opening verbs. The thin-wrapper law keeps all content in
  the contracts.
- The controller's Produce meta sentence finally says "any phase except CHECK" —
  the Display1 refresh agent caught that the 260817 fix never landed in the meta
  block, only in the prose.

## 0.10.0 — 2026-08-19

- **New section §🧭: ONE OUTLINE pass per PREPARE round.** JL asked whether the
  outline needs its own agent the way each display unit has one. Ruling: it is a
  dispatch pattern of `haipipe-board-creator-agent`, not a new agent type — the
  plan is the merge point every evidence return converges on, so the pass runs
  exactly once per round, folds the returns in, re-runs the four checks, and
  leaves a receipt. Display units fan out; outlines cannot.

## 0.9.2 — 2026-08-19

- **phase-cards.md: seven stale phase numbers fixed.** PROBE's, DRAFT's, REVISE's
  and CHECK's 🔀 ROUTES rows and the gathered-ticks table still used the
  pre-260819 numbering (④ EVIDENCE, ③ PROBE, ④c/④v); §🧑 counted "the three ③
  evidence ticks" while the gathered table and the ③d card itself place
  `accepted:` at ⑦ — it is now "the two ③ lane ticks".
- **page-run-contract.md caught up with the PREPARE loop**: the Legal-routes
  block now matches `LEGAL_ROUTES`; the reopen rule drops EVIDENCE→DRAFT; "The
  four ticks" is five; the fault-test happy path runs through the PREPARE loop.
- All found by the display agent rebuilding `QPw00-Display3-who-does-what`,
  which recorded them as contradictions instead of resolving them silently.

## 0.9.1 — 2026-08-19

- **A new Page starts at OUTLINE, not DRAFT.** Both `ref/page-run-contract.md` and
  this contract still said DRAFT, which was correct only while DRAFT owned the
  outline; OUTLINE has been phase ① since 260817.
- **The producer takes every phase except CHECK.** The prose said "exactly one
  DRAFT, PROBE, or REVISE phase", which was true of the four-phase loop and became
  false at the 260817 split: on paper it sent OUTLINE, EVIDENCE and COMPILE to the
  read-only judge. `ref/page-lifecycle.workflow.js` carried the same sentence.
- All three were found by the display agent rebuilding `QPw00-Display1-run-loop`:
  the figure drew what the prose said, and the prose disagreed with the controller.

## 0.9.0 — 2026-08-19

- **ONE agent per display unit**, with the skill chain written down: the agent
  `haipipe-display-unit-agent`, the one door `haipipe-display`, then one of the
  five renderers by the README's `kind:` row. JL 260819: "each display you can have
  a subagent to call the specific skills to work on it, right?"
- The fan-out unit is the UNIT, not the page. Four units on `QPw00-page-loop` went
  stale when the loop's phase order changed and four agents rebuilt them in
  parallel; each owns one folder and cannot collide with a sibling.
- The two things such an agent may never do are named: tick `accepted:` (a person's
  at ⑦ CHECK) and edit the citing sentence (⑤ REVISE's).
- **"An input moved" is not "the figure is wrong."** A dispatch may require the
  agent to DECIDE first; a re-freeze is not a redraw.
- What every dispatch must carry, since a fresh context knows none of it: the
  unit's path, why it is stale, the facts plus the files that are the AUTHORITY,
  the rebuild commands, and the check that must stop reporting it.

## 0.8.0 — 2026-08-19

- **A RUN stops for a person inside the PREPARE loop, and nowhere else.** JL
  260819: "we will mainly check the outline and the evidences if we want. But if
  not, you can just go ahead for the draft and revise and the compile." ④ DRAFT,
  ⑤ REVISE and ⑥ COMPILE run unattended; ⑦ CHECK still judges.
- **Every step reports its `phase:` to whoever is watching**, not only into the
  receipt (JL: "could you then tell me which phase you are in every time you do
  it?").

## 0.7.0 — 2026-08-18

RUN's step 2 may not be delegated, and the loop was made runnable on QPw00.

- **A subagent is not handed the `Workflow` tool.** `haipipe-page-orchestrator-agent`
  declared it, was dispatched as itself for the first time on 260818, and
  returned `blocked` at RUN step 2 with 0 steps and no receipt. Step 2 now says
  the dispatch is the MAIN session's, with the one-object call shape spelled
  out, and that agent is a packet builder and receipt keeper from its 0.3.0.
- Five blockers were cleared the same day so a real run could reach a verdict:
  the producer agent covered 3 of 6 producer phases and now covers all 6
  (creator 0.7.0); the judge could not NAME OUTLINE, PROBE or COMPILE as routes
  and now can (reviewer 0.8.0); `mechanical_errors` scope was undefined and is
  now page-scoped in the snapshot prompt and the judge's return contract; the
  receipt's `page` is normalized to board-relative by the controller; and the
  auditor now falls back to the file name when a recorded path went stale,
  reporting `page-path-stale` instead of the false `source-artifact-missing`.
- `ref/page-run-contract.md` updated on both defects with the measured
  before/after, including the QB8e audit that now reaches
  `artifact-version-mismatch`, the finding the false one was hiding.

## 0.6.0 — 2026-08-18

`ref/phase-cards.md` added, and the QPw roster corrected twice by JL.

- JL asked "if I want to work with the page workflow's each phase, what should
  each phase do" (260818 1402). Every phase contract already answered it and no
  two answered in the same fields: OUTLINE and PROBE use
  `owns · may do · exits · may not`, REVISE uses a three-line same-promise test,
  CHECK uses `reads · writes · does not`, and EVIDENCE uses a six-step loop two
  phases wide. All correct, none readable next to another.
- New `ref/phase-cards.md`: every phase stated ONCE in the SAME six fields,
  `❓ ASKS · 📥 READS · 📤 WRITES · 🚪 EXITS · ✋ TICK · 🔀 ROUTES`, in loop
  order, with ④ EVIDENCE split into its three parallel lanes. Ten cards, five
  person ticks; the other five phases run machine-only end to end. The card is a
  SUMMARY: when it disagrees with a phase contract, the contract wins.
- All six phase contracts gained a pointer to it.
- New `## 🪪 Each phase in SIX fields` section here, naming which contract used
  which fields, so the divergence is recorded rather than tidied away.
- The roster now splits the two halves out loud. JL read the tail and could not
  place it: "Please explain what is 7, 8, 9??? I still don't get it? should we
  delete them? or merge them into one?" They are not phases ⑦⑧⑨; read in
  sequence they say "CHECK, then agents, then receipts, then the gate", which is
  not a thing that happens. They are the run's three axes: 🎭 who acts,
  📜 what proves it ran, ⚖️ who says yes.
- Merging them was rejected on the one-decision-one-page test: each carries its
  own open ruling (the orchestrator was never dispatched · receipts store
  absolute paths so the audit fails today · no surface joins the five ticks), so
  one merged page would hold three unrelated Decision Now blocks in 864 lines.
- JL then ruled the numbering itself out: "if they are not follow, then it is
  not with w etc. You might want to put them into the QPw00". So they became
  subordinates of `QPw00`, the run, on the `QPw4c/4v/4d` precedent, with
  mnemonic letters: `QPw7` → `QPw00a` (agents), `QPw8` → `QPw00r` (receipts),
  `QPw9` → `QPw00g` (gate). `QPw1`-`QPw6` is now exactly the six phases with
  nothing after it. Old ids redirect from `board.md` `## Links`.
- The gate's tick count was FOUR here and is FIVE: the missed one is `read:` on
  a probe card.


## 0.5.0 — 2026-08-18

Two run-contract defects proved by driving the auditor (260818).

- `ref/page-run-contract.md`: the receipt's `page` MUST be stored
  BOARD-RELATIVE. Auditing the only live run, `260805-0216-QB8e`, returns
  `ERROR source-artifact-missing` because the 260816 regroup added the `<N>-`
  numeric prefix to every group folder, so a run recorded as CLOSE with audit
  PASS no longer audits at all. The page itself is fine. An absolute path also
  breaks on a clone, a rename, or a different checkout.
- Added the interim rule: an auditor SHOULD fall back to resolving the page by
  stem under `board` and MUST report the fallback rather than passing silently.
- `mechanical_errors` MUST be page-scoped. On `BoardSkillBoard-260722` all six
  current errors belong to `QPf5`, `QPf6`, and `QPw00`'s unfrozen intakes, so
  board-scoped counting makes CLOSE unreachable for every page on that board.
  This is defect ④ of the same run, now written into the contract.
- `human_gate` is a POINTER and never the tick (JL 260818), for two independent
  reasons: the controller writes receipts, so a stored tick is a machine
  approving itself; and a tick can revert while receipts are append-only.
- Added the Board page backlinks: `QPw00` argues the loop, `QPw1` to `QPw6` one
  page per phase, `QPw00a` the agent roster, `QPw00r` the receipts, `QPw00g` the gate.
# Changelog · haipipe-page-workflow

## 0.4.0 — 2026-08-17

Expands the auditable route grammar to OUTLINE→DRAFT→PROBE→EVIDENCE→REVISE→
COMPILE→CHECK and aligns receipts, builders, and the legacy PROBE alias.

## 0.3.0 — 2026-08-17

**§🃏 settles where an evidence card is born**, which three member skills had
been answering three different ways (`haipipe-page-draft` said DRAFT,
`haipipe-page-evidence` said "already PROPOSED by DRAFT",
`haipipe-plugin-outline` said PROBE). One rule now, and it reads down the loop:
the MARK at OUTLINE, the AIM at DRAFT, the CARD at PROBE, the ANSWER at
EVIDENCE, the SENTENCE at REVISE.

- The display unit is the one exception and it goes LATER, not earlier: EVIDENCE
  creates it, because declaring a unit nothing can fill yet is how a page shipped
  "1 display declared · 0 unit folders on disk".
- The member table's PROBE row points at `../haipipe-page-probe`, which now
  exists, instead of borrowing `../haipipe-page-evidence` "until split out".

## 0.2.0 — 2026-08-16

The loop is DERC, and it ends at a deliverable (JL 260816).

- `PROBE` became `EVIDENCE`; the member list, the loop figure, and the routing
  tables were rewritten. `PROBE` still parses as a phase and route token.
- The four members now read as one arc rather than four authorities:
  DRAFT plans and owes an outline, EVIDENCE lands every promised claim's card,
  REVISE renders and rebuilds latex + word, CHECK judges what was built.
- `ref/page-run-contract.md` carries the alias rule beside its transition table.

## 0.1.1 · 2026-08-16

- The receipt section now names its shipped reader: the 🪜 Workflow menu's
  `📄 Page phases` stepper (`65-plugin-pageflow.js` + `GET /_board/pageruns`),
  read-only, fed by `_runs/page/` and nothing else.

## 0.1.0 · 2026-08-15

- Born by MOVING, not adding: `haipipe-page`'s RUN verb and its
  `ref/page-run-contract.md` relocated here, so the page workflow has one
  nameable head skill beside its four member contracts, matching the
  one-folder-one-workflow shape `page-workflows/` now names (JL 260815,
  ruled in the Page-Workflow session).
- `haipipe-page` keeps CREATE and WORK ON and points here for RUN; two doors
  to one loop is the drift this move exists to prevent.
- The run contract's relative paths gained one `../` for the deeper folder;
  its content is otherwise untouched.
