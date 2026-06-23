---
name: haipipe-paper-claims
description: "Create or update the paper folder's 0-lifecycle/2-claims/2-claims.tex: the claim ledger that tracks which claims are supported, weak, or GAP, each tied to an evidence source (probe verdict / task / discovery / insight). Emits delivery needs for GAP/weak claims and backfills confirmed probe verdicts. This is the paper's claim/evidence contract heart. Use for claim ledger, claims, supported/weak/GAP, claim gap, evidence map, 2-claims."
argument-hint: "[paper-dir] [--backfill <probe-ref>] [--source <path>...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "1.1.0"
  last_updated: "2026-06-22"
  summary: "Maintain 0-lifecycle/2-claims/2-claims.tex as the claim/evidence ledger: matrix + per-claim detail, two-stage evidence gate, no aspirational anchors."
---

Skill: haipipe-paper-claims
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
6. **Matrix plus per-claim detail.** The ledger is a compact MATRIX (ID, claim, status) followed by ONE `\subsection*` per claim; each subsection is a banner-tagged paragraph in the `%% ---- Pn.Sm ----` format with four slots: (S1) claim + verdict, (S2) the verified statistic with spec and N, (S3) one-line interpretation, (S4) caveat + the source file. The matrix is the index; the subsections carry the evidence.
7. **No aspirational anchors.** "planned Table 1" is not evidence, it is GAP; a `supported` row cites a real value and the file it came from (e.g. `trait_l5 +12.90*** in main-ols_..._mme_ttl.csv`), never a future table.
8. **Two-stage evidence gate.** Stage 1 deterministic: the cited file exists AND the cited number actually appears in it (catches planned/hallucinated anchors, no model). Stage 2 verdict: a CONFIRMED probe judges the real number supports the claim. `supported` requires both; existence is not support.
9. **Couple to venue.** Read STATUS `venue` and consult the matching `_venue/playbook-<venue>` (e.g. `playbook-clinical-medicine`, `playbook-nature-portfolio`, `playbook-utd-is`). Designate ONE PRIMARY claim aligned to what the venue rewards, mark it `[primary]` in the matrix, and demote the rest to supporting. The primary claim drives the pitch thesis and the hero display. A result that is novel elsewhere but already established for this venue's readers is an enabler (it belongs in Methods), not a contribution claim. A venue change re-runs this designation.

Workflow
--------

### Step 1: Resolve paper folder

Accept the paper root or any path inside it (look upward for `0-lifecycle/`).
If none exists, ask the user to run `/haipipe-paper-lifecycle folder <paper-root>`.

### Step 2: Ensure `0-lifecycle/2-claims/2-claims.tex` exists

Ledger body = a compact MATRIX (index) then ONE `\subsection*` per claim (detail).
Tables get a banner but no `Pn.Sm`; prose paragraphs use the sentence format.

```latex
\section*{Claim-Evidence Matrix}
% =========================================================
% Para [claims.ledger] Result -- claim / status at a glance
% =========================================================
\begin{tabularx}{\textwidth}{@{}p{0.05\textwidth}X p{0.14\textwidth}@{}}
\toprule
ID & Claim & Status \\
\midrule
C1 & <claim, as the paper states it> & supported \\
C2 & <claim>                         & weak \\
\bottomrule
\end{tabularx}

\section*{Per-claim Detail}

\subsection*{C1. <short title> (supported)}
% =========================================================
% Para [claims.c1] Result -- <the point>
% =========================================================
%% ---- P1.S1 ----
<claim statement>.
%
%% ---- P1.S2 ----
<verified statistic, spec, N> (e.g. trait\_l5 $+12.90$***, $N=765{,}701$).
%
%% ---- P1.S3 ----
<one-line interpretation>.
%
%% ---- P1.S4 ----
Source: <real file, e.g. main-ols\_..._mme\_ttl.csv>; <caveat if any>.
```

For `weak`/`GAP` claims the subsection states the gap and the route instead of a
statistic. Never write a "planned Table" as if it were evidence.

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

### Evidence gate (done means)

A claim row is done when:

- it has a status; `supported` requires BOTH stage 1 (cited file exists and the number appears in it) AND stage 2 (a confirmed probe verdict that the number supports the claim);
- it has its per-claim `\subsection*` paragraph (the four slots), not just a matrix row;
- `weak`/`GAP` rows carry an open need + route; no row cites a "planned" anchor.

### Stage gate (claims complete means)

Beyond the per-row gate, the claims stage is NOT complete until the ledger also
carries these REQUIRED items:

- a venue-coupled `[primary]` claim designation (principle 9); and
- a **Venue Fit** block that justifies, with EVIDENCE, why the primary/supporting
  claims fit the target venue. It states (a) what that venue rewards (from
  `_venue/playbook-<venue>`) and (b) 2-3 precedent papers the venue has actually
  published in this claim space (from `paper/_venue/playbook-<venue>/references`,
  citation-audited before the manuscript). A claim set that does not say WHY it
  fits the venue, and show that the venue's reviewers/editors reward this claim
  type, is not done. (Claims must fit the venue; venue is chosen first.) Place this
  block at the END of the ledger, AFTER all claims are stated (it synthesizes
  across them); do not put it up front before the claims. Format it as BULLET POINTS
-- a short list of fit reasons plus a short list of risks / where it may not fit --
not a single paragraph (bullets read faster than prose here).
- `2-claims.pdf` recompiled and current (a stale PDF is a defect; recompile after
  every edit without being asked).

### Step 4: Handoff

Report the ledger summary (counts by status) and the next command:

```text
claims stable      -> /haipipe-paper narrative <paper-dir>
open needs remain  -> /haipipe-probe | /haipipe-discover | /haipipe-task
```

Update `STATUS.md` (`current_layer`, `maturity: claim-ledger` when the ledger is
explicit).
