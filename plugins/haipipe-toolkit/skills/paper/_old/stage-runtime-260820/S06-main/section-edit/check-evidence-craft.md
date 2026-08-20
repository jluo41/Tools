# Check-evidence craft

Craft file for stage section-edit, loaded by the CHECK phase when the run is pre-submission (its content is section-prose-side, so it lives here rather than with claims).
Source: converted from `workers/haipipe-paper-check-evidence/SKILL.md` on 2026-08-05 (thin-paper phase 2); it is DATA, not a registered skill.

The pre-submission evidence walk: does each cited paper EXIST, is its metadata right, does it actually support the sentence citing it; does each number re-derive from its source; does each display match the claim it carries.

It runs only when the gate is pre-submission — the same shape as the proof-checker pack (`../../S09-build/proof-checker/`), which fires only when a section carries `\begin{proof}`. It never runs alone as the CHECK gate.

Why it is conditional: resolving every DOI at every section gate is unaffordable, and a pass that is too expensive to run is a pass that silently never runs.


What it does NOT do
--------------------

- It does NOT edit prose. It reports, and it seeds `> CHECK:` comments at the exact spot. Fixes go back through REVISE. CHECK verifies; the human decides; REVISE changes.
- It does NOT fill a hole. An unresolved `\cite{TOADD} [Q-X-n]` is DRAFT's marker and EVIDENCE's debt, not a defect for this pass.
- It does NOT batch. See the cadence rule below.


The cadence rule (binding)
---------------------------

**One item at a time. One human approval per fix. No batching.**

This is not politeness. A batch of twenty "corrections" gets waved through as a block, and the one wrong correction inside it ships. The pass is deliberately slow because its whole value is the attention it forces.


Axis 1 — citations
-------------------

Three independent checks per cited work. They fail in different ways and catching one says nothing about the others:

```
① EXISTENCE       does this paper exist at all?
                  failure mode: a hallucinated paper — no canonical record anywhere

② METADATA        real paper, copied wrong
                  year    the VENUE year, not the preprint year, once published
                  title   arXiv v1 vs v3 titles drift
                  authors the ORDER is part of the citation, not a detail
                  venue   journal vs workshop vs preprint server

③ CONTEXT         real paper, correctly copied, WRONG USE
                  it does not support the sentence citing it
```

③ is the one a knowledgeable reviewer catches first and the one no mechanical check can find.

**Source-of-truth hierarchy.** Go to the publisher record or the canonical preprint page. Google Scholar is a discovery aid, never the verification source — its metadata is scraped and is often wrong, and a wrong record confirmed twice still reads as confirmation.

**Wrong-context patterns worth hunting deliberately:**

```
famous-author proxy    a big name cited for a claim their paper does not make
"standard practice"    a citation carrying a general-practice claim it never established
method-claim mismatch  cited for method X; the paper used method Y
self-citation          the easiest to get wrong, because self-trust skips the check
```

**The lit-review / intro asymmetry.** A citation in the literature section is usually right — it was written while reading the paper. The same citation reused in the introduction is often wrong — it was written from memory. Weight the intro's citations more suspiciously.

**Revise-drift is the #1 citation regression.** Prose edits break citations mechanically: a sentence SPLIT leaves the cite on the wrong half; sentences MERGED lose one; a sentence REWORDED keeps its cite while changing the claim it makes. So a re-audit after any substantive REVISE is mandatory, not optional.


Axis 2 — values
----------------

Every number re-derived from its source. Not re-read — re-derived.

```
sample size      len(df[filter]) from the parquet
rate / share     groupby().agg() from the source table
delta            RE-DERIVE the subtraction from raw rates
                 NEVER trust a claimed delta — it is the most common silent error
coefficient/AME  re-run the analysis script's pipeline
p-value          re-derive from the SAME regression, not a similar one
```

Failure taxonomy, because these are distinct and the fix differs:

```
rounding_drift         6.47 written as 6.5, then 6.5 propagated as if exact
unit_error             % vs pp — a percentage-point difference reported as a percentage
stale_snapshot         correct for an older run; the current results say otherwise
config_mismatch        right number, wrong specification
figure_drift_from_body the figure and the sentence disagree
```

**Method claims are values.** "Holm-Bonferroni corrected", "cluster-robust SEs", "clustered at the physician" each assert HOW a number was computed. Verify by grepping the actual analysis code:

```
unsupported_method_claim   the prose claims X; no implementation of X exists
wrong_method_claim         the prose claims X; the code does Y
```

**When prose and source disagree, the source wins.** Never reconcile two prose numbers against each other and never take the majority reading across sections — both may be wrong. The parquet or the script decides.


Axis 3 — displays
------------------

Most of this is already covered by the CHECK gate's own display walk (content matches the claim, `\ref` resolves). This pass adds the two it does not:

```
caption accuracy    does the caption describe what the figure actually shows,
                    including axes, units, and the sample it was computed on
render quality      open the COMPILED PDF. Clipped labels, unreadable point sizes,
                    and overlapping ticks survive every source-level check.
```

**Closed-format sources** (`.pptx`, `.key`, `.ai`): flag for human action, never edit. There is no reproducible path from an agent edit to a regenerated asset.


Output
-------

```
status:    ok | blocked
axes:      citation <n checked, n flagged> │ values <...> │ displays <...>
comments:  <n> `> CHECK:` comments seeded, at file:line
verdict:   PASS | WARN (flagged items, none blocking) | FAIL (a fabricated
           citation or an unre-derivable number — these block a submission)
next:      <suggested command>
```

Every flagged item gets a `> CHECK:` comment at its exact spot in the working `.md`, so the human's pass is guided by the file rather than by hunting from a report.

An item the human declines to fix does not evaporate: record it as a `{CONCERN:<risk>} [Q-<Stage>-<n>]` so it stays visible at every later gate and must be discharged in the limitations text before the final gate.


Where the rest lives
---------------------

Phase dispatch and the CHECK gate itself are owned by `board/page-workflows/haipipe-page-check` (CHECK loads this file last, after the type contract); the proof-checker pack with the same conditional shape is `../../S09-build/proof-checker/`; the pass that applies the fixes this walk asks for is `revise-place-craft.md`.
