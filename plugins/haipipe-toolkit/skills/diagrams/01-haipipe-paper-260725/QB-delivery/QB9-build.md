# Delivery Build: candidates a human reviews before anything becomes the submission

state: 🟡 PARTIAL
owner: JL
method: keep projection, distribution, compilation, checking, and explicit promotion in one build-and-diffusion boundary

## Opening

How does accepted paper authority become a submission without a machine deciding it is ready?

A candidate is a complete generated copy of the paper in one format, written to its own isolated folder. Promotion is the separate, explicit act of making a reviewed candidate become the submission bytes. Keeping those two apart is what this concern is for.

**Where this page sits**: QB6 Main and QB7 Appendix own the authored content and their own human gates.
QF1 owns the record of what actually ran, its receipts, and its failure-to-reopen path.
This page owns the machinery in between, including diffusion and distribution, which JL folded in on 260729.

**Why generate and promote are two commands**: a build that writes straight to the submission has no reviewable state.
The moment the two are one action, the only way to see what you are about to submit is to have already submitted it.
Isolating the candidate is what makes review possible at all, and it is why `3-dist/` is numbered working machinery rather than a deliverable.

**What is deliberately not done**: G5, the promotion gate, has never been run.
That is not an omission, it is the design working: G4 is blocked on a real baseline defect, and a blocked gate refuses the one after it.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `QB4-overall.md` and are not restated here.

**The gates are named here and recorded on QF1**: this page may define what G0 through G5 mean; it may not carry the run log.
A dated result belongs on QF1, and a rule about what a gate requires belongs here.

**Never write that a candidate "is" the submission**: it becomes one only through an explicit human PROMOTE.
The two words are the whole safety property, so keep them apart in every sentence.

**Report a blocked gate as a pass of the design**: a refused G5 is the mechanism working.
Writing it as a failure invites someone to route around it.

## Diagram

**Generate, then promote**: two commands, and the isolation between them.

```text
  ✍️ GATED S pages
        │  adapter (QB11a LaTeX · QB11b Word)
        ▼
  📦 3-dist/<format>/<run-id>/     ← isolated · immutable · numbered
        │
        │  G0 validate  G1 select  G2 G3 check  G4 compile
        ▼
  👤 a human reviews a G0–G4-passing candidate
        │
        │  🚨 explicit PROMOTE  ── the ONLY way across this line
        ▼
  📤 the unnumbered submission projection

  🚫 a failed G0–G4 gate REFUSES G5 ── that is the design working
  ⚠️ today: G4 baseline-blocked · G5 never run
```

## Content

### 1 · The delivery contract

**What Build owes**: gated content in, a reviewable candidate out, and nothing promoted without a person.

```text
  📥 CONSUMES                📤 PROJECTS TO           🚪 GATE
  GATED S pages         ━━▶  3-dist/<format>/   ━━▶  a human reviews a
  external Display and       compiled PDFs           G0–G4-passing
  Venue dependencies         Word handoffs           IMMUTABLE candidate
  🚫 without taking          promotion receipt       and explicitly
     ownership of them                               authorizes G5
```

📜 Establishes the boundary from accepted authority to shipped artifact, and the one act only a person may perform.

| Field | Contract |
|---|---|
| Reader result | A reviewable format candidate and, only after explicit approval, a submission or handoff artifact. |
| Artifact | `3-dist/<format>/<run-id>/`, declared submission targets, compiled PDFs, Word handoffs, and promotion receipt. |
| Authority | S-page Content and gates; `2-src/projection.yaml` is wiring only. |
| Completion gate | A human reviews a G0-G4-passing immutable candidate and explicitly authorizes G5. |
| Consumes | GATED S pages plus external Display/Venue dependencies without taking ownership of them. |
| Engine route | `haipipe-paper-deliver` and `haipipe-paper-project`, with QB11a/QB11b adapters, conform, compile, and ship leaves. |
| Execute evidence | `QF1` records each bounded run; G0-G5 are gates within that execution, not another content authority. |
| Open gaps | MISQ G4 is baseline-blocked by one active stale Display input; G5 was deliberately not run. |

#### 1.1 · A gate refuses the next one, rather than warning about it
(a warning is something a tired person clicks past at midnight before a deadline)
G5 is unreachable while any of G0 through G4 fails, and that is enforced rather than advised.
The property this buys is that the submission bytes can only ever come from a candidate that passed every check, whoever was in a hurry.

### 2 · The first candidate-only execution

**What one real run proved**: how far the path goes today, and exactly where it stops.

```text
  G0 ✅ 28 targets inventoried ── 20 projected · 8 explicitly unreachable
  G1 ✅ main-1 only ── every other unit correctly refused
  G2 ✅  G3 ✅ ── candidate byte-exact against the selected S-page Content
  G4 🛑 blocked ── the BASELINE master reaches an absent input:
        displays/S-Display-4a-main-regression/float.tex
  G5 ⬜ never run ── correct, because G4 did not pass

  🔑 the candidate did NOT introduce the blocker
  ✅ no submission file was replaced
```

🧪 Establishes what the first bounded run demonstrated, and why the stop is a baseline defect rather than a projection defect.

#### 2.1 · The blocker belongs to the baseline, not to the candidate
(it matters because it decides which page has to be reopened to clear it)
The absent Display input is reached by the baseline master, so the candidate reproduced an existing defect rather than creating one.
Repair belongs to the owning section or display work, and QF1 carries the failure-to-reopen link.
The older `displays/Table/table-gradient-results.tex` TODO is commented out in TeX and is now correctly excluded from the static closure.

## Aims

### A1 · 📜 The delivery contract
- A1.1 · Generation and promotion are separate commands, and only a person crosses the line.
  **Done when:** no code path writes a declared submission target without an explicit human PROMOTE, and every promotion leaves a receipt.
- A1.2 · `3-dist/` is numbered working machinery rather than a deliverable.
  **Done when:** the delete test holds: removing `3-dist/` loses no authored content, only regenerable candidates.

### A2 · 🧪 The first candidate-only execution
- A2.1 · The one active baseline Display input is repaired and G4 is rerun.
  **Done when:** the baseline master reaches no absent input and a MISQ candidate passes G4.
- A2.2 · G3 checks structured Display and value bindings, not only citation and question markers.
  **Done when:** a candidate whose stated value no longer matches its bound run fails G3.
- A2.3 · G5 is exercised once, on a reviewed immutable candidate.
  **Done when:** one promotion runs end to end and leaves a receipt, after a human reviewed a G4-passing candidate.

### P · 🏁 Page-level
- P1 · The path is proven on more than one manuscript unit.
  **Done when:** a unit other than main-1 passes G1 through G4.

## States

### A1 · 📜 The delivery contract
- ✅ A1.1 · Built and exercised. Runtime 0.1.3 ships separate `validate`, `generate`, `check`, and `promote`; disposable tests prove path containment, submission isolation, approval refusal, backup, and rollback.
- ✅ A1.2 · Ruled 260729 and held: `3-dist/` was admitted as a numbered non-submission projection area.

### A2 · 🧪 The first candidate-only execution
- 🔨 A2.1 · Blocked at the baseline, not at the projection. G4 receipts record one active absent Display input; repair belongs to its owning section or display work.
- ⬜ A2.2 · Not started. The 260730 trial recorded structured-value comparison as a later G3 extension.
- ❄️ A2.3 · Held on purpose. G5 is unreachable while G4 fails, so this thaws only after A2.1.

### P · 🏁 Page-level
- 🔨 P1 · Active. Of 28 inventoried targets only main-1 passes G1, so the path is demonstrated once rather than established.

## Files

- `paper/3-deliver/1-build/haipipe-paper-project/` · the runtime with the four separate commands
- `2-src/projection.yaml` · wiring only, never content authority
- `2-src/projection-receipts/` · what each bounded run recorded
- `3-dist/tex/f53ccf5c5fc965bbc0c74f478e9015ac8ded949e91e7bc35a667c54cc38ffa98/` · the receipted main-1 candidate
- `QB11a-section-to-latex.md` · the LaTeX adapter this concern calls
- `QB11b-section-to-word.md` · the Word adapter this concern calls

## Law

Build includes diffusion/distribution.
Generation and promotion are separate commands.
Only an explicit human `PROMOTE` decision may replace declared submission targets, and a failed G0–G4 gate refuses G5.

## Glossary

- **Candidate**: an isolated, content-addressed format projection under `3-dist/`.
- **Promotion**: the explicit, receipt-backed transaction that makes reviewed candidate bytes the submission bytes.

## Log

260802 · Migrated to the QB4 page contract: Writing Style added, Content numbered into two divisions with face figures and captions, Aims regrouped as A1/A2/P with `Done when`, States mirrored per Aim.
260730 · Recovered the candidate and workspace after a cleanup bug; replaced recursive cleanup with a no-workspace-delete partial-directory protocol and added containment tests.
260730 · Runtime 0.1.3 rechecked Main-1: G0-G3 pass with verified metadata and independent pre-render evidence extraction; G4 receipt records one active baseline Display blocker; G5 not run.
260729 · JL combined diffusion/distribution with Build.
