insight — RETIRED 2026-07-12
=============================

**This layer is retired. Nothing here is live. Do not resurrect it.**

JL ruling 2026-07-12: the insight layer (D/I/K/W cards) is fully retired. Everything that was
`skills/insight/` — the 7 `/haipipe-insight*` skills, the 4 `card-creator-*` agents, the 4
`card-reviewer-*` agents, the `index-integrity-auditor-agent`, and all `ref/` schemas — now
lives read-only under `_archive/`, and is de-registered (no symlinks in `~/.claude/skills/`
or `~/.claude/agents/`).


Why
---

The DIKW ladder was a design promise that was never practiced. Verified on disk at retirement:

```
zero  K cards ever written, in any project
zero  W cards ever written, in any project
zero  insights/INDEX.md files exist  (the gateway SWEEP's mandated first stop never resolved)
five  projects hold an insights/ dir — all empty, .gitkeep-only, or holding hand-written notes
```

Retiring it therefore cost **zero reuse at runtime**. The layer was pure overhead: a third
warehouse the gateway swept on every probe and never found anything in.


Where the functions went
------------------------

(Re-stated 2026-07-14 against `Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/` v3. The 2026-07-12 version of this
section pointed the retired functions at machinery that has ITSELF since been retired — the PPNN
card's `## Verdict`, the `_ASK/` stub, the gateway SWEEP. Corrected below.)

```
D  dataset profile      → the profiling task's results/ + report.yaml, digested into that leaf's
                          QA/<n>-<slug>.md · and the paper's own _VALUES_ slot map
I  in-sample pattern    → same homes, as prose. The overclaim guard survives in the claims
                          ledger: in-sample-only evidence keeps a claim `weak` and raises a
                          question the paper's PROBE phase must answer
K  generalization claim → SPLIT IN TWO, which is the whole point of the v3 model:
                            the general, reusable FACT      → the executor's QA/<n>-<slug>.md
                                                              (paper-agnostic, no claim ids)
                            the paper-specific JUDGMENT     → that paper's own 1-claims.md
                                                              (supported|refuted|inconclusive +
                                                               confidence + claim_type + gates)
                          A K card tried to be both at once. That is why it never got written.
                          External claims already had a home: a discovery's verdict.md (alive).
W  recommendation       → the claims-ledger GAP/weak → a SECTION in the paper's own
                          1-probes/PPNN_<topic>.md → its `commission:` → the executor's `qa` verb
                          (an executable W, not an advisory one), and applications/ at delivery
                          scale. The standalone, cited, reusable W card form is DROPPED.
```

Cross-consumer reuse of a settled FACT — the one thing K cards were supposed to provide — is now
served by the bank's own readable corpus: `grep {tasks,discoveries}/**/QA/*.md`. Each executor
leaf's `QA/<n>-<slug>.md` files are general by construction, so a fact one paper commissioned is
directly readable by the next — each writing its OWN `reading:` against its OWN claim. The
consumer never re-runs the work, and never inherits the first paper's frame.
See `../probe/haipipe-probe/SKILL.md` (the constitution).

💀 Note for archaeologists: `haipipe-probe-orchestrator-agent` (the gateway whose SWEEP this
section used to name) was itself RETIRED 2026-07-14. There is no gateway. Dispatch goes direct to
`haipipe-task-orchestrator-agent` / `haipipe-discovery-orchestrator-agent`.


Legacy `insights/` folders on disk
----------------------------------

Dead history, exactly like the retired `probes/` folders: **nothing reads them, nothing writes
them, nothing deletes them.** If a project's `insights/` holds real hand-written content (one
does — `ProjB-Bench-2-EventGlucose/insights/_raw/`), move it somewhere alive; do not treat it as
a card store.
