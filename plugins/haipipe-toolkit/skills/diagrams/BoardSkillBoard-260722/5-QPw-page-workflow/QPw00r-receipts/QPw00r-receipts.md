# Receipts: one record per attempted phase, chained by hash, and what the audit can and cannot prove
state: 🟡 IN PROGRESS · the contract ships; its ONE live run returned 11 defects against it · open: 7
owner: CC
method: state the chain, the seven invariants that make it auditable, and the honest limit of what a passed audit means; a claim the audit cannot reach is named as one
session: ec8c7879-3e0f-484e-a3fe-b41b1bfb50fc

## Opening
When a run says it did seven phases, what on disk proves it, and what does that proof NOT cover?

Every attempted phase returns one receipt, the controller normalizes it to one shape, and the receipts are preserved in order under `<board>/_runs/page/<page-id>/<run-id>.json`.
The chain is what makes them evidence rather than a log: a version id is two SHA-256 digests joined by a colon, and every receipt must begin from the preceding receipt's ending version.
Seven invariants turn the highest-risk failures into machine-detectable ones, and `pageflow.py audit` independently REHASHES the files on disk, so a well-formed receipt still fails when the artifacts no longer match it.
The honest limit matters as much as the proof: the audit can show the declared process was followed and can never show that a claim is true because the process passed.

## Writing Style
How this page must be written. Read it before editing, and edit to it.

**Every proof claim names its limit in the same breath**: this page's subject is evidence, so an unqualified "the audit proves" is the defect it exists to prevent.
Say what passed, what was inspected, and what residual risk remains.

**The chain is described by its arithmetic, never by adjectives**: say which field must equal which field, because that is the whole mechanism.
"Tamper-evident" says nothing a reader can check; `version_after` of step N equals `version_before` of step N+1 says the design.

**A defect found by the live run is named with its run id**: one run exists and it produced a defect list, so a rule that came from it must say so.
Reasoned and proven are different words here, exactly as on `QPw00a`.

**Language and sentences**: English only, in the source and in the render.
Write one sentence per line, so a paragraph is consecutive lines rather than one long line.
No em-dashes: use a colon, a semicolon, a comma, parentheses, or simply start a new sentence.

## Diagram
The receipt, the chain that binds two of them, and the auditor that does not trust either.

```text
🧾 RECEIPTS · <board>/_runs/page/<page-id>/<run-id>.json
             outside Page discovery · NEVER renders as a Board Page

one receipt per ATTEMPTED phase, normalized by the controller:
  step · round · phase · actor · role · builder_actor · status
  version_before · version_after · checked_version
  source_sha256 · render_sha256          64 lowercase hex, each
  mechanical_errors · mechanical_warnings
  verdict · route · requested_route · reopens_promise · reason
  artifacts · evidence · findings
  human_gate: {required, status, evidence}   ← a POINTER, never the tick

THE CHAIN, which is the whole mechanism:
  step N     version_after  ─────┐
                                  │ must be IDENTICAL
  step N+1   version_before ◀────┘
  and for CHECK: version_before = version_after = checked_version

THE AUDITOR does not trust the receipt:
  python3 haipipe-board/cli/pageflow.py audit <receipt.json>
  → resolves board and page FROM the receipt
  → locates the rendered page under <board>/board/
  → INDEPENDENTLY RECOMPUTES both SHA-256 digests
  🚫 a well-formed receipt FAILS if the files on disk no longer equal
     its final_version, so a hash written into several fields is not evidence

ROLE SEPARATION, enforced by distinct actor identities:
  controller  chooses and records the next legal route · edits no prose
  producer    performs OUTLINE DRAFT PROBE EVIDENCE REVISE COMPILE
  builder     rebuilds, runs mechanical checks, identifies the version
  judge       performs CHECK read-only against that exact version
  human       supplies any ruling the Page Type requires
```
📌 CLOSE and HOLD are both terminal ROUTES rather than phases, and HOLD preserves a named unresolved gate without pretending quality was achieved.

## Content

### 1 · One receipt per attempted phase, and attempted is the load-bearing word
**The completeness rule**: a phase that failed, was blocked, or was stopped still returns a receipt.

```text
what gets a receipt
  a phase that ran and produced a version            ✅
  a phase that ran and produced nothing              ✅
  a phase whose worker died                          ✅
  a phase the controller stopped for safety          ✅  status says so
  a phase nobody attempted                           ⛔ no receipt, and the
                                                     coverage gap is the finding
```
📌 The controller may stop a run for safety and cannot turn that stop into CLOSE, which is why status and route are separate fields.

#### 1.1 · The legal routes are enumerated, so an illegal one is detectable rather than arguable
(seven from-phases, each with its own allowed set)
From OUTLINE only OUTLINE, DRAFT, or HOLD; from CHECK the full set plus CLOSE, which no other phase may reach.
A cross-phase route to DRAFT is legal ONLY as a reopen: the receipt names the reopened purpose or Aim, sets `reopens_promise: true`, and increments the round.
A route to DRAFT that reopens nothing is an illegal route rather than a free visit, and repeated DRAFT inside the same unsettled promise does not increment.

#### 1.2 · Receipts from the 260816 rename stay auditable
(`phase: PROBE` written between 260816 and 260817 means what is now EVIDENCE)
The auditor carries a legacy-shape compatibility rule for exactly those receipts, and the alias resolves against the RECEIPT'S OWN DATE rather than a global mapping.
A global alias would have relabelled every future PROBE as EVIDENCE, which is a defect the 260817 round caught before it shipped.

### 2 · The version id is the mechanism, and the auditor recomputes it
**The identity rule**: a version is the SHA-256 of the markdown source joined by a colon to the SHA-256 of its rendered HTML.

```text
version_after  of step N   ==   version_before of step N+1
CHECK: version_before == version_after == checked_version

🚫 what this catches
   a version edited after it was checked
   a receipt claiming a hash the files do not have
   two sessions writing the same page concurrently
```
📌 The auditor resolves the board and page from the receipt and rehashes the artifacts itself, so version evidence is never accepted because an agent wrote the same claimed hash into several fields.

#### 2.1 · A rebuild is not a mutation, and that distinction is still owed
(the 11th defect found by the one live run, `260805-0216-QB8e`)
`pageflow.py audit` reports `artifact-version-mismatch` on the RENDER hash alone, because a later innocent rebuild changes the HTML while the source hash still matches.
The receipt treats source and render as one identity, so unless the contract says the SOURCE hash is the version's identity and the render hash is advisory, every rebuild retroactively breaks every closed run.
This is written here as an owned defect rather than described as a risk, and it is `A2.2`.

### 3 · Seven invariants make the loop auditable
**The detection rule**: the highest-risk failures become machine-detectable rather than matters of judgment.

```text
① the preserved packet matches the run identity, first phase, gate, limits
② only legal routes are accepted, and only CHECK may CLOSE
③ a non-DRAFT route to DRAFT names the reopened purpose or Aim and
  increments the round exactly once
④ producer, mechanical builder, and judge have DIFFERENT actor identities
⑤ every version id is two lowercase SHA-256 digests joined by `:`, and every
  receipt begins from the preceding receipt's ending version
⑥ CHECK observes identical before, after, and checked ids; the auditor
  rehashes, and any later change requires a new CHECK
⑦ a required human gate closes ONLY with durable evidence that a person ruled
  and max steps or rounds terminate as NON-CONVERGENCE, never as a pass
```
📌 Invariant ⑦ is why the human gate cannot live inside a receipt: the receipt is written by the controller, so a gate stored there would be a machine writing its own approval.

#### 3.1 · Branch and fault coverage are part of the contract, not extra credit
(a green common path does not demonstrate a router)
The harness must exercise the happy paths, the legal loops including CHECK back to REVISE and CHECK to a new DRAFT round, and injected faults: self-approval, mutation after CHECK, illegal route, packet mismatch, broken version continuity, symbolic hashes, missing human evidence, failed worker, non-terminal trace, and exhausted limits.
Each injected fault must be rejected for the SPECIFIC invariant it violates, because a harness that rejects everything for one reason has one test rather than eleven.

### 4 · What the audit can prove, and what it cannot
**The honesty rule**: the record says what passed, what was inspected, and what residual risk remains.

```text
✅ CAN PROVE     the declared process was followed: the packet matches the run,
                routes and version handoffs were legal, rounds changed for the
                right reason, producer and builder and judge stayed separate,
                CHECK observed an immutable version, human gates were not
                fabricated, and bounded loops stopped honestly

🚫 CANNOT PROVE  that any claim on the page is TRUE because the process passed

confidence comes from THREE kinds of evidence together
  ① deterministic mechanics from check.py and the lifecycle auditor
  ② fresh-context semantic judgment against the page's requirements
  ③ direct evidence, or an explicit human gate, for what a machine cannot settle
```
📌 The final record never says quality guaranteed without naming the gate and its evidence, which is the same rule `QPw6` applies to a pass claim.

#### 4.1 · A CHECK result may not be appended to the page's own Log
(doing so changes the version that was just checked)
OUTLINE owns its versioned plan, DRAFT and EVIDENCE and REVISE may update the page Log as part of the version they produce, PROBE owns its card folders, and COMPILE owns only derived build outputs.
Terminal CHECK evidence stays in the audit bundle or in the Page Type's declared review surface.

### 5 · The one live run, and the defects it returned against this contract
**The evidence rule**: one run has happened, it closed with an audit that passed then and fails today, and its second product was a defect list against the contract that ran it.

```text
run     260805-0216-QB8e     route CLOSE · audit PASSED THEN, and FAILS
                                     TODAY for a DIFFERENT reason than it did
                                     this morning. Until 260818 it returned
                                     `source-artifact-missing`, which was FALSE:
                                     the file was fine, the receipt's `page` was
                                     ABSOLUTE and the 260816 regroup had renamed
                                     the group folder. The auditor now falls back
                                     to the file name, reports `page-path-stale`,
                                     and reaches the finding the false one hid:
                                     `artifact-version-mismatch`, because the
                                     page HAS been edited since it closed
and 11 defects against THIS contract, of which the sharpest six:
  ① the controller is not invocable outside a Workflow harness and the
    contract never says what a bare caller may do
  ② the producer prompt omits the judge's findings, so a strict REVISE guesses
  ③ "the local closing rule" is ambiguous for a mid-life Q page whose
    decision rows wait on a person by design
  ④ mechanical_errors scope is undefined, and board-scoped counting would let
    one foreign dead link forbid CLOSE forever
    ✅ CLOSED 260818: page-scoped is now stated in the controller's snapshot
       prompt and in haipipe-board-reviewer-agent's return contract
  ⑤ warnings do not gate CLOSE, so the semantic judge is the only defence
    on a WARN-only page
  ⑥ fresh judges oscillate, and max_steps is the only brake
```
📌 A contract whose first live use produced eleven findings against itself is working; the failure would have been a run that reported clean.
Two of the eleven closed on 260818, when the loop was made runnable on `QPw00`: the `page` path is normalized by the controller before any receipt is written, and `mechanical_errors` is page-scoped in both the builder's prompt and the judge's return contract.

#### 5.1 · Three of the eleven are still open and are Aims on this page
(the snapshot with no receipt home, the missing `audit` key, and the rebuild-is-not-a-mutation ruling)
The pre-run snapshot has no receipt home, so it survives only in session history.
The bundle carries no `audit` key at all, which means "audit PASS" for that run exists nowhere on disk, and that is the same shape as the snapshot problem wearing a second face.

## Aims

### Decision Now
- [ ] 🗣 Rule whether the SOURCE hash alone is a version's identity
      📍 `Part` §2.1, a rebuild is not a mutation
      🔔 `Why now` this is defect ⑪ from the only live run and it is load-bearing: while source and render are one identity, any later innocent rebuild of the HTML retroactively breaks every closed run's audit, and this board has been rebuilt several times today alone
      ⭐ `A ·` the SOURCE hash is the version identity and the render hash is advisory, recorded and reported but never a mismatch on its own: a rebuild is not a content change, and the render is reproducible from the source
      `B ·` keep both hashes binding and re-audit after every rebuild, which is stricter and means the audit result of a closed run expires whenever anyone rebuilds the board for an unrelated page
      🛑 `Blocks` A2.2, and every closed run's audit on this board
      🤖 `If nobody answers` A takes effect, because B makes a closed audit expire for reasons unrelated to the page it audited


### A1 · 🧾 One receipt per attempted phase, and attempted is the load-bearing word
- ⬜ A1.1 · Every attempted phase in every run on this board returned a receipt.
  Done when no run bundle has a step gap between its first and last receipt.
  **Now:** Not measured. One run bundle exists, `260805-0216-QB8e`, and no gap check has been run over it.
- ⬜ A1.2 · No illegal route has been accepted.
  Done when the auditor rejects a route outside the enumerated set for invariant ②.
  **Now:** Not started. No illegal route has been injected to test the rejection.


### A2 · 🔗 The version id is the mechanism, and the auditor recomputes it
- ✅ A2.1 · The auditor rehashes rather than trusting the receipt.
  Done when a receipt carrying a correct-looking but wrong hash is rejected by `pageflow.py audit`.
  **Now:** Met. `pageflow.py audit` resolves the page from the receipt and recomputes both digests independently.
- 🧠 A2.2 · The rebuild-is-not-a-mutation question is ruled and written into the contract.
  Done when the contract says whether the SOURCE hash alone is the version identity, and the auditor stops reporting `artifact-version-mismatch` on an innocent rebuild.
  **Now:** Waiting on the Decision Now row above.


### A3 · 🛡 Seven invariants make the loop auditable
- ⬜ A3.1 · Each of the seven is separately detectable.
  Done when each injected fault is rejected for the specific invariant it violates rather than for a generic failure.
  **Now:** Not measured. The invariants are written and no per-invariant rejection test exists.
- ⬜ A3.2 · The fault-injection harness exists and runs.
  Done when all eleven named fault cases run in a test suite on this board.
  **Now:** Not started. Eleven fault cases are named in the contract and none is implemented as a test.


### A4 · ⚖️ What the audit can prove, and what it cannot
- ✅ A4.1 · No run record on this board claims quality without naming its gate.
  Done when every terminal record names what passed, what was inspected, and the residual risk.
  **Now:** Met for the one run that exists: its record names its route, its audit result, and eleven residual defects.
- ✅ A4.2 · No CHECK result has been appended to a page's own Log after approval.
  Done when no page Log on this board carries a CHECK entry written after its closing version.
  **Now:** Met. No page Log on this board carries a post-approval CHECK entry.


### A5 · 🔬 The one live run, and the defects it returned against this contract
- ⬜ A5.1 · The pre-run snapshot has a receipt home.
  Done when a run bundle carries its pre-run snapshot rather than leaving it in session history.
  **Now:** Not started, and it is item ⑩ of the run's own defect list.
- ⬜ A5.2 · The bundle carries an `audit` key.
  Done when a closed run's audit result exists on disk rather than only in a session transcript.
  **Now:** Not started. The `260805-0216-QB8e` audit PASS exists only in session history.


## Files
### 📋 Contracts · what CARRIES a rule to other pages
- `page-workflows/haipipe-page-workflow/ref/page-run-contract.md`
  The packet, the receipt shape, the legal routes, role separation, the audit bundle, and the fault tests. The authority on all six.
- `page-workflows/haipipe-page-workflow/SKILL.md`
  The RUN router that produces these receipts.
### ⚙️ Engines · what RUNS this subject
- `haipipe-board/ref/page-lifecycle.workflow.js`
  The bounded Workflow the controller drives.
### 🧪 Checks · what CATCHES a page breaking a rule
- `haipipe-board/cli/pageflow.py`
  The lifecycle auditor. `audit <receipt.json>` rehashes the artifacts rather than trusting the receipt.
### 📤 Output files · what a BUILD writes
- `_runs/page/<page-id>/<run-id>.json`
  The durable bundle: the original packet, ordered receipts, final version, terminal route, and limits.
- `board/QPw/QPw00r-receipts.html`
  ⚠️ Generated by `cli/build.py`. Never hand-edit it; the markdown is the only source.

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `constrained by · ALL` · [QPw00 §10](5-QPw-page-workflow/QPw00-page-loop/QPw00-page-loop.md)
  The audit division of the loop page, which states the seven invariants this page carries in full.
- `reads · ALL` · [QPw00a §1](5-QPw-page-workflow/QPw00a-page-agents/QPw00a-page-agents.md)
  The three agent units whose actor identities invariant ④ requires to be distinct.
- `continues · CHECK` · [QPw6 §1](5-QPw-page-workflow/QPw6-check/QPw6-check.md)
  The phase whose receipt carries the strictest version rule, since its three version fields must be identical.

## Law
- 🔗 **A version is two hashes joined by a colon**: the SHA-256 of the source and the SHA-256 of its rendered HTML
  Every receipt must begin from the preceding receipt's ending version, and that continuity is what makes an ordered set of receipts evidence rather than a log.
- 🧾 **The auditor does not trust the receipt**: it resolves the page from the receipt and recomputes both digests
  A well-formed receipt still fails when the files on disk no longer equal its `final_version`, so writing one claimed hash into several fields proves nothing.
- ✋ **A required human gate closes only with durable evidence**: max steps and rounds terminate as non-convergence, never as a pass
  The controller writes the receipt, so a gate stored inside one would be a machine writing its own approval, which is why `QPw00g` exists as a separate surface.
- ⚖️ **The audit proves PROCESS, never TRUTH**: a passed audit does not make a claim on the page correct
  Confidence needs deterministic mechanics, fresh-context semantic judgment, and either direct evidence or an explicit human gate, and the record names which of the three it has.
- 📝 **A CHECK result is never appended to the page's own Log**: doing so changes the version that was just checked
  Terminal CHECK evidence stays in the audit bundle or the Page Type's declared review surface.

## Glossary
- 🧾 **receipt**: the normalized record of one attempted phase, preserved in order inside a run bundle.
- 🔗 **version id**: `source_sha256:render_sha256`, both 64 lowercase hex characters.
- 🛡 **invariant**: one of the seven conditions the auditor checks, each separately detectable.
- ⏸ **HOLD**: a terminal route preserving a named unresolved gate, missing input, tool failure, or exhausted limit.
- ⚖️ **non-convergence**: what an exhausted step or round limit terminates as, and never a pass.

## Log
- 260818 · [DRAFT-CC] page created, closing the ⬜ debt line that `board.md` carried for the `_runs/` receipt contract since 260816. Written from `haipipe-page-workflow/ref/page-run-contract.md` and the seven invariants already stated in `QPw00 §10.2`. Five divisions: the one-receipt-per-ATTEMPTED-phase rule with the enumerated legal routes, the version chain and the auditor that recomputes it, the seven invariants with the branch and fault coverage they require, the honest limit of what an audit proves, and the single live run `260805-0216-QB8e` with the eleven defects it returned against this contract. Three of those eleven became Aims here rather than prose: the snapshot with no receipt home, the missing `audit` key, and the rebuild-is-not-a-mutation ruling, which is load-bearing enough to be the Decision Now row since every rebuild of this board currently expires every closed audit.

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0