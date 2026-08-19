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
