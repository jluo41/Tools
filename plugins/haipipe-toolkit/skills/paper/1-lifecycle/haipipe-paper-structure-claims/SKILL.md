---
name: haipipe-paper-structure-claims
description: "Create or update the paper folder's 0-lifecycle/2-claims/2-claims.tex: the claim ledger that tracks which claims are supported, weak, or GAP, each tied to an evidence source (probe verdict / task / discovery / insight). Emits delivery needs for GAP/weak claims and backfills confirmed probe verdicts. This is the paper's claim/evidence contract heart. Use for claim ledger, claims, supported/weak/GAP, claim gap, evidence map, 2-claims."
argument-hint: "[paper-dir] [--backfill <probe-ref>] [--source <path>...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "1.0.0"
  last_updated: "2026-06-22"
  summary: "Maintain 0-lifecycle/2-claims/2-claims.tex as the claim/evidence ledger."
---

Skill: haipipe-paper-structure-claims
=====================================

Maintain the **claim ledger** of a concrete paper folder. This is the paper's
claim/evidence contract, the delivery-side mirror of a probe.

It answers one question:

```text
Which claims are supported, weak, or GAP, and what evidence settles each?
```

Every claim the paper wants to make is a row with a status and a source. The
paper does not produce evidence; it selects judged evidence and tracks what is
still missing. Unsupported or too-strong claims become delivery needs routed to
probe/discover/task/insight, and confirmed verdicts are backfilled here.

Read first: `../../PHILOSOPHY.md`, `../../ref/lifecycle-map.md`,
`../../ref/delivery-need.md`.

Location
--------

```text
<paper>/0-lifecycle/2-claims/2-claims.tex   standalone-compilable stage contract
```

TeX-first; this skill owns the ledger body.

Principles
----------

1. One row per claim. Each row has a status and a source ref.
2. Status vocabulary: `supported`, `weak`, `GAP`.
3. A claim is `supported` only when it traces to a CONFIRMED probe verdict or an
   equivalently judged artifact. Never mark `supported` from intuition.
4. `weak`/`GAP` rows must carry an open need and a route. They are first-class
   open needs surfaced by the Paper Console.
5. The paper must not overclaim. If evidence is `I` (information) but the claim
   needs `K` (knowledge), keep it `weak` and route a probe.

Workflow
--------

### Step 1: Resolve paper folder

Accept the paper root or any path inside it (look upward for `0-lifecycle/`).
If none exists, ask the user to run `/haipipe-paper-structure folder <paper-root>`.

### Step 2: Ensure `0-lifecycle/2-claims/2-claims.tex` exists

Ledger body:

```latex
\section*{Claim Ledger}

\begin{tabular}{p{0.08\linewidth}p{0.34\linewidth}p{0.12\linewidth}p{0.34\linewidth}}
\toprule
ID & Claim & Status & Evidence Source / Open Need \\
\midrule
C1 & <claim, as the paper would state it> & supported & probes/0605_.../verdict.md \\
C2 & <claim> & weak & probe needed: /haipipe-probe open <need> \\
C3 & <claim> & GAP & task needed: /haipipe-task <contract> \\
\bottomrule
\end{tabular}
```

### Step 3: Maintain the ledger

- New claim: add a row, set status from the cited source (default `GAP`).
- `--backfill <probe-ref>`: read the probe verdict; if confirmed, move the row to
  `supported` with the verdict path and any caveats; if refuted/partial, keep
  `weak` and note scope.
- Emit a delivery need for every `weak`/`GAP` row using the delivery-need
  interface, with the route:

```text
claim needs a verdict/robustness check   -> /haipipe-probe open <need>
claim needs outside context/citation     -> /haipipe-discover <question>
claim needs a run or data artifact        -> /haipipe-task <contract>
```

Do not run evidence work here. Record needs and backfill verdicts.

### Step 4: Handoff

Report the ledger summary (counts by status) and the next command:

```text
claims stable      -> /haipipe-paper narrative <paper-dir>
open needs remain  -> /haipipe-probe | /haipipe-discover | /haipipe-task
```

Update `STATUS.md` (`current_layer`, `maturity: claim-ledger` when the ledger is
explicit).
