# Page RUN contract

`RUN` is the bounded router for one persistent Page. It does not mean
`ADVANCE`: Page work is non-linear, so the next authority may repeat, branch,
return to CONTEXT, OUTLINE, EVIDENCE, or CONTENT, close, or hold.

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
start_phase: CHECK             # CONTEXT | OUTLINE | EVIDENCE | CONTENT | CHECK
                               # PROBE → EVIDENCE and DRAFT/REVISE/COMPILE →
                               # CONTENT when reading historical inputs
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
                               # Page Face owner; omit only for legacy Pages
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

The person-reserved fields are identical in both modes, and no machine writes
one in either. Waiting behavior differs only for review confirmations; a
branching choice still blocks when it has no durable answer:

```text
  🧑 copilot   the human half BLOCKS.  A person is here; an unticked gate is a
               legitimate HOLD, and the receipt names which tick and which file.
  🤖 auto      review confirmation may DEFER. The loop may keep moving on the
               machine half (`checked:`, agents/approve-rules/) and the debt
               accumulates on the ledger. A semantic branch choice never
               defers into an invented route. `cli/pagephase.py <page-dir> --owed`
```

This is JL's 260818 ruling made executable — *"human not to approve, they to
break"*: where policy allows, the RUN proceeds on `checked: ✅` while a review
confirmation remains owed. That rule never chooses a SURVEY branch. A person's
🛑 still outranks everything and stops the run in either mode.

**AUTO MAY DEFER REVIEW TICKS; `page_ruling` OWNS THE CLOSING GATE.** `approved:`
`Verified`/legacy `verified`, `read:` and `accepted:` each have a rules file under
`agents/approve-rules/`, so an approver can establish everything around them.
The Page Face owner supplies one of three policies:

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

`Decide` is not a review tick. It chooses `make`, `defer`, or `drop`, changes
the route, and therefore cannot be pushed onto the owed ledger as though work
had been selected. Auto HOLDs at SURVEY on an unsigned Decide unless a prior
explicit durable owner decision/default policy supplies the branch. It never
turns an owed Decide into `make`.

An auto run may therefore reach HOLD **by design, not by failure** when a required
owner or caller gate remains open, when CITE verification is required before
EMBED, or when Decide is unresolved. A `page_ruling: none` Folder with no separately
declared gate may CLOSE after its mechanical and semantic checks pass.

`mode` is echoed on every run result, so a stored receipt can never be read
without knowing which reading of the ticks produced it.
The caller resolves the phase-owned Folder contract before dispatch:
`workflow/phase.yaml current.folder-kind` for an in-place Folder, then Page
`folder-kind:` for a fixed identity. A legacy Page-Type/filename route is fallback
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
then begins at CONTEXT/PREPARE. For an existing Page whose next need is
unknown, RUN begins at CHECK so a fresh judge routes the visible version.

## Phase receipt

Every attempted phase returns one receipt. The controller normalizes it to this
shape and preserves all receipts in order:

```json
{
  "step": 4,
  "round": 1,
  "phase": "CHECK",
  "cycle": "CHECK",
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
  "route": "CONTENT",
  "next_cycle": "WRITE",
  "requested_route": "CONTENT",
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

`reason` names the authority exercised, not merely the file operation. Current
receipts keep `reopens_promise: false`: the former DRAFT/REVISE round split is
now internal to CONTENT/WRITE. The field and its old invariants remain in the
auditor only for immutable historical receipts.

## Receipt step, field by field

What `../../../haipipe-board/src/page_lifecycle.py` (`audit_run`) actually
enforces on every receipt, transcribed from the code; the right column is the
finding code a breach raises.

```text
field                 the auditor's rule                           finding code
────────────────────────────────────────────────────────────────────────────────
step                  exactly its 1-based position in receipts:    step-sequence
                      1, 2, 3 … no gap, no reuse
round                 first receipt: a positive integer; current   round-start ·
                      runs normally keep it fixed. Historical      round-sequence ·
                      reopen receipts retain their old +1 rule;    max-rounds-exceeded
                      never above limits.max_rounds
phase                 current: CONTEXT OUTLINE EVIDENCE CONTENT    unknown-phase ·
                      CHECK; historical DRAFT REVISE COMPILE and   route-phase-mismatch ·
                      PROBE remain readable; must equal the
                      previous receipt's route; nothing may        receipt-after-terminal
                      follow a CLOSE or HOLD receipt
cycle / next_cycle    cycle names the work performed; route names  controller rejects a
                      the next Page phase; next_cycle names the     missing or mismatched
                      cycle inside that phase. CLOSE/HOLD omit it   next cycle before storage
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
reopens_promise       current receipts use false; true is valid    reopen-without-draft ·
                      only under the historical DRAFT grammar      draft-without-reopen
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
from CONTEXT  → CONTEXT | OUTLINE | HOLD
from OUTLINE  → CONTEXT | OUTLINE | EVIDENCE | CONTENT | HOLD
from EVIDENCE → CONTEXT | EVIDENCE | OUTLINE | HOLD
from CONTENT  → CONTEXT | CONTENT | OUTLINE | EVIDENCE | CHECK | HOLD
from CHECK    → CLOSE | CONTEXT | OUTLINE | EVIDENCE | CONTENT | HOLD
```

**HOLD is terminal in the current controller.** It returns one named unresolved
gate, missing input, tool failure, concurrency mismatch, or exhausted limit;
continuation starts a new Page RUN at the receipt's named phase/cycle. The
auditor retains one narrow compatibility exception for pre-current receipts:
a pending CONTEXT/OUTLINE/EVIDENCE HOLD that has neither `cycle` nor
`next_cycle` may be followed by another historical receipt. The executable
controller never emits that shape. A current HOLD always omits `next_cycle`
and no receipt follows it.

Compatibility rows for DRAFT, REVISE, and COMPILE remain in the executable
`LEGAL` table and auditor only because removing them would make stored receipts
unauditable. They are not current routes and are not offered by the controller.

`PROBE` retired on 260901: its MATCH half is OUTLINE's SURVEY cycle (the item
table's Run column), its dispatch half is EVIDENCE's LAND cycle (a card only
when a question leaves the page). A stored receipt naming PROBE reads as
EVIDENCE through the auditor's alias, so every pre-260901 run stays auditable.
A current producer's receipt carries `cycle:` beside `phase:` and
`next_cycle:` beside a nonterminal Page-phase `route:`. The controller rejects
`route: SHAPE` or `route: LAND`: those are cycles, not Page phases. Historical
receipts predating the split remain readable without `next_cycle`.

Only CHECK may CLOSE. CLOSE is a route, not a sixth Page Phase. HOLD is also a
terminal route: it preserves a named unresolved gate, missing input, tool
failure, concurrency mismatch, or exhausted limit without pretending quality
was achieved.

## Role separation

```text
controller   chooses and records the next legal route; edits no Page prose
producer     one agent for CONTEXT, OUTLINE, EVIDENCE, or CONTENT; performs
             exactly one phase and may not approve its own version
builder      rebuilds, runs mechanical checks, and identifies the version
judge        performs CHECK read-only against that exact version
human        supplies any ruling required by the Page Face owner
```

The producer, builder, and judge for one version must have distinct actor
identities. The builder may report deterministic defects but does not make
semantic claims. The controller may stop a run for safety, but cannot turn that
stop into CLOSE.

## Effort tier per phase

The dispatch runs each phase at the effort its question deserves. Historical
measurements motivated folding the old writing phases into one CONTENT pass.

```text
CONTEXT · OUTLINE · CHECK       inherit the session tier: policy resolution,
                                synthesis, and verdict carry the hard judgment
EVIDENCE · CONTENT              'high': they execute an approved plan and their
                                own exit checks catch a shallow pass
```

The controller sets this in the Workflow dispatch (`PHASE_EFFORT` in
page-lifecycle.workflow.js); a phase absent from the map inherits. A caller
may override for one run by saying so in the packet, and the receipt's actor
line is unaffected either way.

## CONTENT · the WRITE cycle

CONTENT is one lifecycle phase. Its internal movements are Draft, Revise,
Build, and Pre-check. Those movements are not independent lifecycle phases and
do not create extra L4 Run identities. A normal commission creates one
`Page · Division Writing` Run per division and promotes its accepted Result
into Page Content before CHECK judges the whole built Page.

```text
L3 phase receipt       one CONTENT receipt per lifecycle pass
L4 writing work        one indexed Run per commissioned division
internal movements     Draft → Revise → Build → Pre-check
backward routes        CONTEXT for stale policy; OUTLINE for wrong plan;
                       EVIDENCE for missing/invalid Result
forward route          CHECK only after all commissioned Results are promoted
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
      historical edges=CHECK->REVISE->CHECK->REVISE->CHECK->CLOSE
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
would change the just-checked version. CONTEXT owns the generated context
projection; OUTLINE owns its versioned plan and route design; EVIDENCE owns
allocated Run ids, local Result pointers, and embedded evidence bindings;
CONTENT owns Page prose and declared delivery outputs.
Terminal CHECK evidence stays in the audit bundle or the Page Face owner's declared
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
happy paths     CONTEXT→OUTLINE→CONTENT→CHECK→CLOSE
                CONTEXT→OUTLINE→EVIDENCE→OUTLINE→CONTENT→CHECK→CLOSE
legal loops     OUTLINE→EVIDENCE→OUTLINE; CONTENT→CONTENT;
                CHECK→CONTEXT; CHECK→OUTLINE; CHECK→EVIDENCE; CHECK→CONTENT
compatibility   stored PROBE/DRAFT/REVISE/COMPILE receipt trails remain auditable
faults          producer=self-judge; version changed after CHECK; illegal route
gates           required human approval absent; explicit HOLD
bounds          max steps reached; non-terminal trace; failed or blocked worker
integrity       packet/run mismatch; broken version continuity; symbolic hashes
```

Passing only the common route is not evidence that the router works. Branch and
fault coverage are part of the Page lifecycle contract.
