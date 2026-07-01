---
name: haipipe-paper-claims
description: "Create or update the paper folder's 0-lifecycle/2-claims/2-claims.md + _LOG_2-claims.md: the venue-FREE claim/evidence inventory that tracks which claims are supported, weak, or GAP, each tied to an evidence source (probe verdict / task / discovery / insight). Emits delivery needs for GAP/weak claims and backfills confirmed probe verdicts. Venue-neutral hypotheses (H1, H2, H3) live here; venue-specific RQ framing, Editor's Chair Test, and [primary] designation live in pitch (the cover letter). Markdown only. Use for claim ledger, claims, supported/weak/GAP, claim gap, evidence map, 2-claims."
argument-hint: "[paper-dir] [--backfill <probe-ref>] [--source <path>...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "3.0.0"
  last_updated: "2026-07-01"
  summary: "Maintain 0-lifecycle/2-claims/2-claims.md + _LOG as the venue-FREE claim/evidence inventory. Markdown only (argument documents don't need .tex compilation; only display compiles to PDF)."
  changelog:
    - "3.0.0 (2026-07-01): claims is now venue-FREE. Editor's Chair Test, [primary] designation, and venue-shaped RQs migrated to pitch (the cover letter). Claims keeps venue-neutral hypotheses (H1, H2, H3) and a pure evidence inventory reusable across venues."
    - "2.0.0 (2026-06-29): switched from .tex to .md + _LOG. Argument documents are markdown; only display compiles to PDF. Claims create PP probe plans in 1-probe-plans/ for evidence gaps."
    - "v1.3.0: added editor's chair test, RQs in claims (not pitch), RQ→Claim→Answer alignment table, probe plans buffer convention, extracted template to ref/claims-template.tex"
    - "v1.2.0: added illuminate protocol + cross-refs to stage-gate, tex-quality"
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

This stage follows three shared protocols. Read them once:
- `ref/stage-illuminate.md` -- illuminate + elicit taste before drafting
- `ref/stage-gate.md` -- exit criteria + confirm-before-advance gate
- `ref/tex-quality.md` -- self-contained compilable tex with Pn.Sm tags

Location
--------

```text
<paper>/0-lifecycle/2-claims/2-claims.tex   standalone-compilable stage contract
```

TeX-first; this skill owns the ledger body.

Principles
----------

1. One row per claim. Each row has a status and a source ref.
1b. **Venue-neutral hypotheses live here.** Claims holds hypotheses (H1, H2,
   H3) as venue-neutral statements of what the paper tests. Venue-specific RQ
   framing, the Editor's Chair Test, and [primary] designation live in pitch
   (the cover letter). The same hypotheses yield different RQ wording for
   different venues, but the underlying claim-evidence inventory stays the same.
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
9. **Venue-FREE.** The claims ledger is a pure evidence inventory, reusable
   across venues. It does NOT designate a [primary] claim, does NOT carry an
   Editor's Chair Test, and does NOT shape RQs to a venue. Those venue-aligned
   items live in pitch (the cover letter). If the paper retargets from venue A
   to venue B, the claims ledger stays unchanged; only pitch and narrative
   rewrite.

Workflow
--------

### Step 0: Illuminate + Elicit

Before modifying the ledger, follow `ref/stage-illuminate.md`. Present the
current claim set and its evidence status. Identify taste-bearing decisions:
which hypotheses are testable? What evidence gaps exist? What is the
strongest claim? Ask the user. (Venue coupling -- which claim is primary,
what frame -- happens later in pitch.)

### Step 1: Resolve paper folder

Accept the paper root or any path inside it (look upward for `0-lifecycle/`).
If none exists, ask the user to run `/haipipe-paper-lifecycle folder <paper-root>`.

### Step 2: Ensure `0-lifecycle/2-claims/2-claims.tex` exists

The full template is in `ref/claims-template.tex` (standalone-compilable,
~130 lines). Copy it to `0-lifecycle/2-claims/2-claims.tex` and fill in.

Reading order of the template:

```text
1. Hypotheses                  ← venue-neutral H1, H2, H3 (what we test)
2. Claim-Evidence Matrix       ← one row per claim, status at a glance
3. Per-Claim Detail            ← four-slot paragraphs (S1-S4) per claim
4. Discussion-Only Interp.     ← interpretive, not Results (optional)
5. Robustness                  ← Methods, not claimed (optional)
6. Pending Evidence            ← probes/tasks not yet run
7. Hypothesis-Claim Alignment  ← H→Claims validation (no venue framing)
```

The hypotheses are venue-neutral statements of what the paper tests. The same
H1 can become RQ1 worded for JAMA or RQ1 worded for MISQ -- that reframing
happens in pitch (the cover letter), not here.

For `weak`/`GAP` claims the subsection states the gap and the route instead of a
statistic. Never write a "planned Table" as if it were evidence.

### Probe plans buffer (1-probe-plans/)

When the claims ledger identifies GAP/weak claims that need evidence, buffer
probe plans in `1-probe-plans/` rather than dispatching immediately. Each probe
plan is one file (`PPNN_<slug>.md`) with frontmatter (id, status, claim,
source_ref) and structured fields (claim under test, evidence needed, expected
route, constraints, datasets). The buffer index (`1-probe-plans/README.md`)
tracks status (planned / dispatched / verdicted) and the dependency chain.

Probe plans are categorized by urgency:
- **MUST-HAVE**: blocks submission (GAP claims)
- **STRONGLY RECOMMENDED**: pre-empts reviewer objections
- **EXPLORATORY**: supplement material, not main claims

When probes return verdicts, backfill into the claims ledger (Step 3).

### Step 3: Maintain the ledger

- New claim: add a row, set status from the cited source (default `GAP`).
- `--backfill <probe-ref>`: read the probe verdict; if confirmed, move the row to
  `supported` with the verdict path and any caveats; if refuted/partial, keep
  `weak` and note scope.
- Emit a delivery need for every `weak`/`GAP` row using the delivery-need
  interface, with the route:

```text
claim needs a verdict/robustness check   -> /haipipe-probe open <need>
claim needs outside context/citation     -> /haipipe-discovery <question>
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

- a **Hypotheses** section with venue-neutral H1, H2, H3 (principle 1b); and
- a **Hypothesis-Claim Alignment** section that maps each H to its claims and
  checks for orphan claims (no H) or unanswered hypotheses (claims all GAP);
  and
- every claim row has a per-claim detail subsection (not just a matrix row).

Venue-specific items (Editor's Chair Test, [primary] designation, RQ framing)
are NOT required here. They belong in pitch (the cover letter).

Present exit criteria per `ref/stage-gate.md`. Ask for user confirm before
advancing. Update `STATUS.md` Gate Ledger on confirm.

### Step 4: Handoff

Report the ledger summary (counts by status) and the next command.

Render the **stage strip** showing the current position in the lifecycle
(see `ref/lifecycle-map.md`):

```text
claims stable      -> /haipipe-paper narrative <paper-dir>
open needs remain  -> /haipipe-probe | /haipipe-discovery | /haipipe-task
```

Update `STATUS.md` (`current_layer`, `maturity: claim-ledger` when the ledger is
explicit).
