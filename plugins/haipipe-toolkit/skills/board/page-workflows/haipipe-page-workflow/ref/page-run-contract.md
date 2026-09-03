# Page RUN contract

`RUN` is the bounded router for one persistent Page. It does not mean
`ADVANCE`: Page work is non-linear, so the next authority may repeat, branch,
return to DRAFT in a new round, close, or hold.

The executable controller lives in
`../../../haipipe-board/ref/page-lifecycle.workflow.js`. The deterministic auditor
lives in `../../../haipipe-board/src/page_lifecycle.py`. This file owns the packet
and receipt they share.

## Raw-material packet

The caller supplies facts and authority, not a proposed paragraph formula.

```yaml
run_id: 260804-2130-QB5
board: /absolute/path/to/board-folder
page: /absolute/path/to/QB5-page-loop.md
start_phase: CHECK             # OUTLINE | DRAFT | EVIDENCE | REVISE | CHECK;
                               # COMPILE parses for legacy receipts only (folded
                               # into REVISE 260819); PROBE parses as EVIDENCE
                               # for receipts older than 260901
intent: audit and improve the automatic Page loop
mode: copilot                  # copilot (default) | auto — see § below
sources:                       # exact files the run may rely on
  - /absolute/path/to/source.md
related_context:               # derived from this Page's Files for start_phase
  command: pagecontext.py <page> --phase CHECK
  traversal: one-hop
  packet: "# Related Board Pages ..."  # exact bounded Markdown handed to the phase
constraints:                   # settled rulings that no phase may reopen silently
  - Page is not a configuration
page_ruling: none              # none | domain-gate | local; resolved from the
                               # Folder's owning phase; omit only for legacy Pages
human_gate:
  required: false              # controller hardens domain-gate/local, plus a
  rule: all Aims met or explicitly held   # legacy Page in auto; see § below
limits:
  max_steps: 12
  max_rounds: 3
```

Required fields are `run_id`, `board`, `page`, `start_phase`, and `intent`.
`mode` defaults to `copilot`; any value but `copilot` or `auto` blocks the run.

## 🔀 `mode` · copilot and auto are ONE rule set read two ways (260821)

The selected person-reserved ticks are identical in both modes, and no machine
writes one in either. What changes is what happens while a tick is UNANSWERED:

```text
  🧑 copilot   the human half BLOCKS.  A person is here; an unticked gate is a
               legitimate HOLD, and the receipt names which tick and which file.
  🤖 auto      the human half DEFERS.  The loop keeps moving on the machine half
               (`checked:`, agents/approve-rules/) and the debt accumulates on
               the ledger, handed over once at the end instead of interrupting
               once per selected tick.  `cli/pagephase.py <page-dir> --owed`
```

This is JL's 260818 ruling made executable — *"human not to approve, they to
break"*: the RUN proceeds on `checked: ✅` alone, and a plan nobody objected to is
not blocked. A person's 🛑 still outranks everything and still stops the run in
either mode.

**AUTO DEFERS PLUGIN TICKS; `page_ruling` OWNS THE CLOSING GATE.** `approved:`
`verified` `read:` and `accepted:` each have a rules file under
`agents/approve-rules/`, so an approver can establish everything around them.
The owning workflow phase supplies one of three policies:

```text
  none         no owner RULING; the Page loop adds no gate
  domain-gate  reuse the phase Gate/Closure receipt; do not ask twice
  local        require a Page-local RULING
```

`domain-gate` and `local` force `human_gate.required` true even when the caller
omitted it; a missing `page_ruling` preserves the legacy rule that auto hardens a
local gate. The controller writes the normalized policy and gate BACK into the
packet because the deterministic auditor asserts that every receipt's
`human_gate.required` equals the packet's. A hardened gate the echoed packet did
not know about would fail the audit on its own receipt.

An auto run may therefore reach HOLD **by design, not by failure** when a required
owner or caller gate remains open. A `page_ruling: none` Folder with no separately
declared gate may CLOSE after its mechanical and semantic checks pass.

`mode` is echoed on every run result, so a stored receipt can never be read
without knowing which reading of the ticks produced it.
The caller resolves the phase-owned Folder contract before dispatch:
`workflow/phase.yaml current.folder-kind` for an in-place Folder, then Page
`folder-kind:` for a fixed identity. A legacy Page Type/filename is fallback
only. A missing source, malformed current block, conflicting kind, unknown
policy, or ambiguous authority is a named HOLD, never a guessed input.

Before every phase dispatch, the controller resolves `### 🔗 Related Board
Pages` with `../../../haipipe-board/cli/pagecontext.py`. Only rows matching that
phase or `ALL` enter the packet. A `§n` scope brings the target Page identity,
Opening, requested Content division, and matching Aims/States group; `page`
brings the whole target. Traversal stops after that one hop even when the target
declares more related Pages. A malformed row, dead target, Page-id mismatch, or
missing scope is a named HOLD. If CHECK routes to a different authority, the
controller rematerializes context for the new phase rather than reusing CHECK's
packet.

For a new Page, CREATE scaffolds and registers the persistent Page first; RUN
then begins at OUTLINE (the SHAPE cycle), the head of the loop since 260817. Beginning at DRAFT was correct only while DRAFT owned the outline. For an existing Page whose next need is unknown, RUN
begins at CHECK so a fresh judge routes the visible version.

## Phase receipt

Every attempted phase returns one receipt. The controller normalizes it to this
shape and preserves all receipts in order:

```json
{
  "step": 4,
  "round": 1,
  "phase": "CHECK",
  "actor": "haipipe-page-check-agent",
  "role": "judge",
  "builder_actor": "fresh-page-builder",
  "status": "ok",
  "version_before": "source-sha256:render-sha256",
  "version_after": "source-sha256:render-sha256",
  "checked_version": "source-sha256:render-sha256",
  "source_sha256": "64-lowercase-hex-characters",
  "render_sha256": "64-lowercase-hex-characters",
  "mechanical_errors": 0,
  "mechanical_warnings": 0,
  "verdict": "revise",
  "route": "REVISE",
  "requested_route": "REVISE",
  "reopens_promise": false,
  "reason": "A3.1 lacks visible evidence",
  "artifacts": [],
  "evidence": ["QB5-page-loop.md#A3"],
  "findings": ["A3.1 is asserted but not demonstrated"],
  "human_gate": {"required": false, "status": "not-required", "evidence": []}
}
```

⚠️ **`human_gate` is a POINTER, never the tick itself** (JL 260818). It records
that a gate was satisfied and WHERE to look; `evidence` holds paths to the
durable ticks. And it must MATCH the packet: `human_gate.required` must equal
the packet's `human_gate.required` on EVERY step, or the auditor rejects the
receipt (`human-gate-contract-mismatch`). Two independent reasons forbid
storing the tick here:

```text
the WRITER       the controller writes receipts, so a tick stored in one is
                 a machine writing its own approval
MUTABILITY       a tick can go BACKWARD: a changed display `intake/` drops
                 `accepted: ✅` to ⬜. receipts are an append-only chain, and
                 a value that reverts cannot live in one
```

The selected ticks and their joined ledger are argued on `QPw00g-human-gate`.

The minimum auditable identity is the SHA-256 of the Markdown source joined to
the SHA-256 of its rendered HTML. The auditor requires lowercase 64-character
hex digests and verifies that `version_after` is exactly
`source_sha256:render_sha256`. `builder_actor` identifies who produced that
snapshot. Every receipt's `version_before` must equal the preceding receipt's
`version_after`. CHECK is valid only when `version_before`, `version_after`, and
`checked_version` are identical. Any content edit creates a new version that
must be checked again.

`reason` names the authority exercised, not merely the file operation. A route
to DRAFT from REVISE or CHECK is legal ONLY as a reopen (EVIDENCE lost its DRAFT
edge on 260819: it routes back to OUTLINE, and the plan's gate is the one door
into DRAFT): the receipt
names the reopened purpose or Aim, sets `reopens_promise: true`, and increments
the round, which is the same "only when purpose or an Aim reopened" rule the
base and QB5 (the loop page, QB9 until 260805) state; a cross-phase route to DRAFT that reopens nothing is an
illegal route, not a free visit. Repeated DRAFT within the same unsettled
promise does not increment.

## Receipt step, field by field

What `../../../haipipe-board/src/page_lifecycle.py` (`audit_run`) actually
enforces on every receipt, transcribed from the code; the right column is the
finding code a breach raises.

```text
field                 the auditor's rule                           finding code
────────────────────────────────────────────────────────────────────────────────
step                  exactly its 1-based position in receipts:    step-sequence
                      1, 2, 3 … no gap, no reuse
round                 first receipt: a positive integer; after     round-start ·
                      that, +1 ONLY when the previous receipt      round-sequence ·
                      routed DRAFT from a phase other than         max-rounds-exceeded
                      DRAFT/OUTLINE with reopens_promise true,
                      else unchanged; never above
                      limits.max_rounds
phase                 one of OUTLINE DRAFT EVIDENCE REVISE         unknown-phase ·
                      COMPILE CHECK (PROBE reads as EVIDENCE in     route-phase-mismatch ·
                      pre-260901 receipts); must equal the
                      previous receipt's route; nothing may        receipt-after-terminal
                      follow a CLOSE or HOLD receipt
route                 in LEGAL_ROUTES[phase]; only CHECK may       illegal-route ·
                      CLOSE; the final receipt must route          producer-closed ·
                      CLOSE or HOLD                                trace-not-terminal
actor                 non-empty; on a producer phase it must       missing-actor ·
                      differ from builder_actor                    producer-is-builder
builder_actor         non-empty; a CHECK judge may equal           missing-builder-actor ·
                      neither it nor the producer of the           judge-is-builder ·
                      checked version                              self-approval
role                  producer on every phase but CHECK; judge     producer-role ·
                      on CHECK (controller allowed only to         check-role ·
                      record a blocked/failed HOLD, never to       controller-judged
                      judge or close)
status                blocked or failed must route to HOLD         failed-work-not-held
version_before        required; <64-hex-source>:<64-hex-render>;   missing-version ·
                      must equal the preceding receipt's           invalid-version-format ·
                      version_after                                version-continuity
version_after         required; same format; must equal            snapshot-version-mismatch
                      source_sha256:render_sha256
checked_version       CHECK only: version_before, version_after    checked-version-mismatch
                      and checked_version identical
mechanical_errors /   non-negative integers, booleans rejected;    invalid-mechanical-count ·
mechanical_warnings   CLOSE requires mechanical_errors = 0         close-with-mechanical-errors
verdict               CHECK only: CLOSE requires pass; a pass      close-without-pass ·
                      may only CLOSE or HOLD; revise must route    pass-routed-to-work ·
                      to a producing phase; blocked must HOLD      revise-without-worker ·
                                                                   blocked-not-held
reason                non-empty, names the authority exercised     missing-reason
evidence              a LIST                                       missing-evidence-list
artifacts             a LIST                                       missing-artifacts-list
human_gate            a dict whose `required` equals the           human-gate-contract-mismatch ·
                      packet's on EVERY step; CLOSE under a        human-gate-fabricated
                      required gate needs status=passed and
                      non-empty evidence
reopens_promise       true requires route=DRAFT; a non-DRAFT,      reopen-without-draft ·
                      non-OUTLINE phase routing to DRAFT           draft-without-reopen
                      requires it true
```

Run-level, from the same auditor: the packet must be present with `run_id`,
`board`, `page`, `start_phase`, `intent`, and its `run_id`/`board`/`page` must
equal the run's (`missing-packet`, `missing-packet-field`,
`packet-run-mismatch`); `page_ruling` must be `none`, `domain-gate`, `local`, or
the compatibility value `legacy-default` (`unknown-page-ruling`), and
`domain-gate`/`local` require `human_gate.required: true`
(`owner-gate-not-required`); `limits.max_steps`/`max_rounds` are positive
integers and the receipt count stays within them (`invalid-limit`,
`max-steps-exceeded`); `final_version` is required in the same
`<source>:<render>` format and, on CLOSE, must equal the terminal CHECK's
`checked_version` (`missing-final-version`, `invalid-final-version-format`,
`changed-after-check`); run `status` must be `closed` exactly when the final
route is CLOSE (`status-route-mismatch`).

## Legal routes

```text
from OUTLINE  → OUTLINE | EVIDENCE | DRAFT | HOLD        (SHAPE ⇄ SURVEY, then LAND, or the DRAFT part)
from EVIDENCE → EVIDENCE | OUTLINE | HOLD                (LAND → EMBED → back to SHAPE)
from DRAFT    → DRAFT | OUTLINE | REVISE | CHECK | HOLD  (a claim without a run → SURVEY)
from REVISE   → REVISE | COMPILE† | OUTLINE | EVIDENCE | DRAFT | CHECK | HOLD
from COMPILE† → COMPILE† | CHECK | REVISE | HOLD
from CHECK    → CLOSE | OUTLINE | EVIDENCE | DRAFT | REVISE | HOLD

**The OUTLINE-part pause (260819, renamed 260901).** A `HOLD` from OUTLINE or EVIDENCE while
the packet's human gate is required and the step's own gate is still open
(`status: pending`) is a PAUSE between passes of one converging round, not a
terminal: the next receipt's phase must be legal FROM the paused phase, and
`receipt-after-terminal` does not fire, and a cold CHECK may follow the pause directly: the judge reads and routes any version, it produces nothing. `CLOSE` is always terminal, and a HOLD
outside the OUTLINE part, or with a settled gate, stays terminal. Because one round
appends one receipt per pass, a packet's `max_steps` must be declared with the
loop in mind: it bounds the passes a run may spend, so `1` fits only a
single-pass errand, never an OUTLINE-part round.

† COMPILE edges are for legacy receipts only (folded into REVISE 260819).
  The rows stay, in this table and in the auditor's `LEGAL_ROUTES`, because
  removing them would make a stored receipt naming COMPILE unauditable.

`PROBE` retired on 260901: its MATCH half is OUTLINE's SURVEY cycle (the item
table's Run column), its dispatch half is EVIDENCE's LAND cycle (a card only
when a question leaves the page). A stored receipt naming PROBE reads as
EVIDENCE through the auditor's alias, so every pre-260901 run stays auditable.
A producer's receipt carries `cycle:` beside `phase:` since 260901.
```

Only CHECK may CLOSE. CLOSE is a route, not a fifth Page Phase. HOLD is also a
terminal route: it preserves a named unresolved gate, missing input, tool
failure, concurrency mismatch, or exhausted limit without pretending quality
was achieved.

## Role separation

```text
controller   chooses and records the next legal route; edits no Page prose
  producer     one agent per phase since 260819 (haipipe-page-<phase>-agent,
               COMPILE handled by the REVISE agent); performs exactly one phase;
               may not approve its own version
builder      rebuilds, runs mechanical checks, and identifies the version
judge        performs CHECK read-only against that exact version
human        supplies any ruling required by the Page Type or local contract
```

The producer, builder, and judge for one version must have distinct actor
identities. The builder may report deterministic defects but does not make
semantic claims. The controller may stop a run for safety, but cannot turn that
stop into CLOSE.

## Effort tier per phase

The dispatch runs each phase at the effort its question deserves, measured on
QPw00's first full loop (260819-20): DRAFT at the session tier spent 77% of
114k output tokens on thinking while executing an already-approved plan.

```text
OUTLINE · CHECK                 inherit the session tier: synthesis and the
                                verdict are where the hard judgment lives
EVIDENCE · DRAFT ·              'high', one tier down: they execute a plan a
REVISE · COMPILE                person already approved, and their own exit
                                checks (four checks, mechanical checker,
                                receipt continuity) catch a shallow pass
```

The controller sets this in the Workflow dispatch (`PHASE_EFFORT` in
page-lifecycle.workflow.js); a phase absent from the map inherits. A caller
may override for one run by saying so in the packet, and the receipt's actor
line is unaffected either way.

## The fused DRAFT+REVISE pass · the WRITE cycle

When DRAFT is entered with the promise UNCHANGED — through the boundary after
the OUTLINE part, or re-entered without `reopens_promise` — the controller dispatches
ONE producer that performs DRAFT and then continues into REVISE (COMPILE
folded in) in the same context: this is the WRITE cycle. Measured on QPw00 (260819-20), the separate
REVISE boot re-loaded the same contracts and re-read the same page for about 50k
tokens that bought no independence: DRAFT and REVISE are both unattended, both
producers, and CHECK judges them cold either way.

```text
fused     one agent · one context · TWO receipt steps in the run file
          (DRAFT, then REVISE with version_before = DRAFT's version_after)
          typed return: phase DRAFT, requested route CHECK
not fused a DRAFT that reopens the promise runs alone, because its REVISE
          must meet the changed promise in a fresh context
unchanged the walls (Opening, outline/, outline/evidence/display/,
          outline/evidence/bibex/, runs/, results/), the
          builder/judge separation, and every human tick
```

## Durable audit bundle

The Workflow result is written to:

```text
<board>/_runs/page/<page-id>/<run-id>.json
```

`_runs/` is outside Page discovery and never renders as a Board Page. The
bundle contains the original packet, ordered receipts, final version, terminal
route, and limit values. It is checked with:

```bash
python3 <toolkit>/skills/board/haipipe-board/cli/pageflow.py audit <receipt.json>
```

The CLI resolves `board` and `page` from the receipt, locates the rendered Page
under `<board>/board/`, and independently recomputes both SHA-256 digests. A
well-formed receipt still fails if the files currently on disk do not equal its
`final_version`. Thus version evidence is not accepted merely because an agent
wrote the same claimed hash into several fields.

⚠️ **`page` MUST be stored BOARD-RELATIVE.** This was proved on 260818 by
auditing the only live run that exists, and the controller now normalizes it:

```text
$ pageflow.py audit _runs/page/QB8e/260805-0216-QB8e.json     BEFORE 260818
ERROR source-artifact-missing  Page source does not exist:
      <board>/QS-sentence/QS2-sentence-details-lifecycle/QS2-…md
FAIL  page-lifecycle: 1 finding

the file is FINE. it sits at 6-QS-sentence/QS2-…, because the 260816
regroup added the `<N>-` numeric prefix to every group folder.
```

Two fixes landed the same day, and the second is the one that matters:

```text
① the CONTROLLER normalizes  page-lifecycle.workflow.js strips a leading
                             `<board>/` before it writes any receipt, so every
                             NEW receipt stores a relative path
② the AUDITOR falls back     when the recorded path does not resolve, it looks
   AND SAYS SO               for the file NAME under `board`. A unique match is
                             audited, and reported as `page-path-stale`; two
                             matches refuse, because guessing is worse than
                             stopping. The audit still FAILS: the receipt is
                             defective, and saying so precisely beats saying
                             something false.
```

```text
$ pageflow.py audit _runs/page/QB8e/260805-0216-QB8e.json     AFTER 260818
ERROR page-path-stale            records <abs>/QS-sentence/…; resolves uniquely
                                 to 6-QS-sentence/…. Audited against that.
ERROR artifact-version-mismatch  current identity differs from final_version
FAIL  page-lifecycle: 2 finding(s)
      edges=CHECK->REVISE,REVISE->CHECK,CHECK->REVISE,REVISE->CHECK,CHECK->CLOSE
```

The second finding is the one the first was hiding: the page has been edited
since it closed, which is a true statement about a closed version and is exactly
what an audit is for.

So a run recorded as `CLOSE` with `audit PASS` no longer audits at all, and the
cause is a legitimate board reorganization rather than any mutation of the page.
An absolute path also breaks on a clone, a rename, or a different checkout.

```text
🚫 page: /Users/…/BoardSkillBoard-260722/QS-sentence/QS2-…/QS2-….md
✅ page: <group-folder>/QS2-…/QS2-….md      resolved against `board`
   and a group renumber is then a resolvable move, not a dead path
```

Until that lands, an auditor SHOULD fall back to resolving the receipt's page by
its stem under `board`, and MUST report the fallback rather than passing silently.

⚠️ **`mechanical_errors` MUST be PAGE-scoped**, and it was undefined until
260818. This is defect ④ of the same run and it was never theoretical: on
`BoardSkillBoard-260722` every error belonged to some OTHER page, so under
board-scoped counting no page on that board could ever pass. Board-level
findings are reported as context and never as a gate.

```text
where it is now stated
  ref/page-lifecycle.workflow.js   snapshot() step 2 carries the literal
                                   `check.py <board> | grep '^<page-file>'`
  agents/haipipe-board-reviewer-   the return contract's `route:` block
    agent.md 0.8.0
measured 260818 after the fix      board 4 errors, ALL foreign
                                   (QPf5 ×2, QPf6 ×2) · QPw00 ZERO
```

Do not append a CHECK result to the Folder's outline log after approval: that
would change the just-checked version. OUTLINE owns its versioned plan; DRAFT,
EVIDENCE, and REVISE may update `outline/<stem>-log.md` as part of the version
they produce; EVIDENCE owns allocated Run ids and local Result pointers in
`outline/<stem>-evidence-items.md`; COMPILE owns only derived build outputs.
Terminal CHECK evidence stays in the audit bundle or the Page Type's declared
review surface.

## What the audit can prove

The audit can prove that the declared process was followed: the preserved
packet matches the run, routes and version handoffs were legal, rounds changed
for the right reason, producer/builder/judge stayed separate, CHECK observed an
immutable version, human gates were not fabricated, and bounded loops stopped
honestly.

It cannot prove that an arbitrary claim is true merely because the process
passed. High confidence comes from combining three kinds of evidence:

1. deterministic mechanics from `check.py` and the lifecycle auditor;
2. fresh-context semantic judgment against the Page's declared requirements;
3. direct evidence or an explicit human gate for claims a machine cannot settle.

The final record therefore says what passed, what evidence was inspected, and
what residual risk remains. It never says “quality guaranteed” without naming
the gate and its evidence.

## Required fault tests

The shipped harness must exercise at least these cases:

```text
  happy paths     OUTLINE→EVIDENCE→OUTLINE→DRAFT→REVISE→CHECK→CLOSE
                  OUTLINE→DRAFT→CHECK→CLOSE
  legal loops     OUTLINE→EVIDENCE→OUTLINE (the OUTLINE part);
                  CHECK→REVISE→CHECK; CHECK→EVIDENCE;
                  CHECK→OUTLINE; CHECK→DRAFT(new round)
faults          producer=self-judge; version changed after CHECK; illegal route
gates           required human approval absent; explicit HOLD
bounds          max steps reached; non-terminal trace; failed or blocked worker
integrity       packet/run mismatch; broken version continuity; symbolic hashes
```

Passing only the common route is not evidence that the router works. Branch and
fault coverage are part of the Page lifecycle contract.
