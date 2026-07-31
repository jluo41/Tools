# Delivery: Build
state: 🟡 PARTIAL
owner: JL
method: keep projection, distribution, compilation, checking, and explicit promotion in one build-and-diffusion boundary

## Question
How does accepted paper authority become isolated format candidates and, only after review, the submission and handoff artifacts?

## Boundary
- ✅ Covered here
  Build plus diffusion/distribution: manifest wiring, LaTeX/Word adapters, isolated candidates, handoffs, and explicit promotion.
- ↪ Covered by Main and Appendix
  Authoritative manuscript content and human page gates.
- ↪ Covered by Present
  Slides and posters.
- ↪ Covered by QE0
  The concrete execution record, including receipts, compile outcome, and failure-to-reopen path.

## Diagram
```text
S pages ── adapter ──▶ 3-dist/<format>/<run-id>/  candidate
                           │ validate/check/compile
                           │ explicit human PROMOTE
                           ▼
                  unnumbered submission projection
```

## Content
| Field | Contract |
|---|---|
| Reader result | A reviewable format candidate and, only after explicit approval, a submission or handoff artifact. |
| Artifact | `3-dist/<format>/<run-id>/`, declared submission targets, compiled PDFs, Word handoffs, and promotion receipt. |
| Authority | S-page Content and gates; `2-src/projection.yaml` is wiring only. |
| Completion gate | A human reviews a G0-G4-passing immutable candidate and explicitly authorizes G5. |
| Consumes | GATED S pages plus external Display/Venue dependencies without taking ownership of them. |
| Engine route | `haipipe-paper-deliver` and `haipipe-paper-project`, with QC5/QC6 adapters, conform, compile, and ship leaves. |
| Execute evidence | `QE0` records each bounded run; G0-G5 are gates within that execution, not another content authority. |
| Open gaps | MISQ G4 is baseline-blocked by one active stale Display input; G5 was deliberately not run. |

### First candidate-only execution
`QE0` owns the full execution record and its failure-to-reopen link.
The MISQ manifest passes G0 with 28 inventoried targets: 20 projected outputs and 8 explicit unreachable paths.
Only `main-1` passes G1.
Its current receipted candidate at `3-dist/tex/f53ccf5c…/sections/01_introduction.tex` is byte-exact against the selected S-page Content and passes independent G2/G3 checks.

G4 stops before compilation because the baseline master actively reaches one absent input:

```text
displays/S-Display-4a-main-regression/float.tex
```

The candidate did not introduce that path. The older `displays/Table/table-gradient-results.tex` TODO is commented out in TeX and is now correctly excluded from the static closure.
No submission file was replaced, and G5 remains not run.

## Items to Finish
- [x] Admit `3-dist/` as a numbered non-submission projection area.
- [x] Create `haipipe-paper-project` with separate `validate`, `generate`, `check`, and `promote`.
- [x] Populate and G0-validate the MISQ manifest.
- [x] Exercise Main-1 through G0-G3 without promotion.
- [ ] Repair the one active baseline Display input in its owning section/display work, then rerun G4.
- [ ] Extend G3 from citation/question markers to structured Display/value bindings.
- [ ] Exercise G5 only after a human reviews an immutable, G4-passing candidate.

## Where we are
Runtime 0.1.3 and the MISQ manifest exist.
Disposable tests prove deterministic reuse, path containment, submission isolation, approval refusal, backup, and rollback behavior.
The real trial is blocked only at baseline G4. Generate, G0-G3 check, and blocked-G4 receipts exist; no promotion receipt exists.

## Files
- `paper/3-deliver/1-build/haipipe-paper-project/`
- `2-src/projection.yaml`
- `2-src/projection-receipts/`
- `3-dist/tex/f53ccf5c5fc965bbc0c74f478e9015ac8ded949e91e7bc35a667c54cc38ffa98/`
- `QC5-sentence-to-latex.md`
- `QC6-sentence-to-word.md`

## Law
Build includes diffusion/distribution.
Generation and promotion are separate commands.
Only an explicit human `PROMOTE` decision may replace declared submission targets, and a failed G0–G4 gate refuses G5.

## Glossary
- **Candidate**: an isolated, content-addressed format projection under `3-dist/`.
- **Promotion**: the explicit, receipt-backed transaction that makes reviewed candidate bytes the submission bytes.

## Log
260730 · Recovered the candidate and workspace after a cleanup bug; replaced recursive cleanup with a no-workspace-delete partial-directory protocol and added containment tests.
260730 · Runtime 0.1.3 rechecked Main-1: G0-G3 pass with verified metadata and independent pre-render evidence extraction; G4 receipt records one active baseline Display blocker; G5 not run.
260729 · JL combined diffusion/distribution with Build.
