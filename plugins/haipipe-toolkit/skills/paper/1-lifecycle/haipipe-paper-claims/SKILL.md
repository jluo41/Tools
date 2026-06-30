---
name: haipipe-paper-claims
description: "Create or update the paper folder's 0-lifecycle/2-claims/2-claims.md + _LOG_2-claims.md: the claim ledger that tracks which claims are supported, weak, or GAP, each tied to an evidence source (probe verdict / task / discovery / insight). Emits delivery needs for GAP/weak claims and backfills confirmed probe verdicts. Markdown only (argument documents don't need .tex compilation). This is the paper's claim/evidence contract heart. Use for claim ledger, claims, supported/weak/GAP, claim gap, evidence map, 2-claims."
argument-hint: "[paper-dir] [--backfill <probe-ref>] [--source <path>...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "2.0.0"
  last_updated: "2026-06-29"
  summary: "Maintain 0-lifecycle/2-claims/2-claims.md + _LOG as the claim/evidence ledger. Markdown only (argument documents don't need .tex compilation; only display compiles to PDF)."
  changelog:
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
1b. **Research questions live in claims, not pitch.** RQs are venue-coupled:
   their wording depends on what the target editor rewards. The pitch is
   venue-independent (the one-minute story before you pick a venue). Claims
   are venue-coupled (tailored to the target). Therefore RQs belong in the
   claims ledger, stated BEFORE the claim-evidence matrix, with an explicit
   RQ-to-claim mapping table. Each RQ maps to 1-2 claims; each claim maps
   back to exactly one RQ. The mapping is the skeleton of the Results section.
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

### Step 0: Illuminate + Elicit

Before modifying the ledger, follow `ref/stage-illuminate.md`. Present the
current claim set and its venue coupling. Identify taste-bearing decisions:
which claim is PRIMARY for this venue? What frame (clinical/method/policy)?
Ask the user.

### Step 1: Resolve paper folder

Accept the paper root or any path inside it (look upward for `0-lifecycle/`).
If none exists, ask the user to run `/haipipe-paper-lifecycle folder <paper-root>`.

### Step 2: Ensure `0-lifecycle/2-claims/2-claims.tex` exists

The full template is in `ref/claims-template.tex` (standalone-compilable,
~130 lines). Copy it to `0-lifecycle/2-claims/2-claims.tex` and fill in.

Reading order of the template:

```text
1. Editor's Chair Test         ← venue question (stated once, from playbook)
2. Research Questions          ← venue-shaped RQs + RQ→Claim mapping
                                 (includes "why this RQ for this venue" column)
3. Claim-Evidence Matrix       ← one row per claim, status at a glance
4. Per-Claim Detail            ← four-slot paragraphs (S1-S4) per claim
5. Discussion-Only Interp.     ← interpretive, not Results (optional)
6. Robustness                  ← Methods, not claimed (optional)
7. Pending Evidence            ← probes/tasks not yet run + backup venue
8. Editor's Chair Alignment    ← RQ→Claims→Answer validation table
                                 + venue fit (scale, strength, risk)
                                 + diagnostic rules
```

Key design: sections 1 and 8 form a bracket. The editor's chair question at
the top GENERATES RQs (top-down). The alignment table at the bottom VALIDATES
claims against the same question (bottom-up). Venue Fit is folded into
section 8 (one section validates everything).

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

- a **Research Questions** section with RQ-to-claim mapping (principle 1b); and
- a venue-coupled `[primary]` claim designation (principle 9); and
- an **Editor's Chair Alignment** section at the END of the ledger (template
  section 8) that contains ALL of: (a) the three-column RQ → Claims → Editor's
  Chair Answer validation table, (b) venue fit bullets (scale, strength, risk —
  what the venue rewards and where reviewers may push back), and (c) the
  diagnostic rules (no RQ = orphan; no answer = wrong venue; RQ without claim =
  GAP). This single section validates the whole ledger against the venue. There
  is no separate Venue Fit section — it is folded in here.
- `2-claims.pdf` recompiled and current (a stale PDF is a defect; recompile after
  every edit without being asked).

Present exit criteria per `ref/stage-gate.md`. Ask for user confirm before
advancing. Update `STATUS.md` Gate Ledger on confirm.

Compile `2-claims.pdf` per `ref/tex-quality.md` after every ledger edit.

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
