---
name: haipipe-paper-claims
description: "Stage orchestrator for the paper folder's 0-lifecycle/1-claims/1-claims.md + _LOG_1-claims.md: the venue-FREE claim/evidence inventory that tracks which claims are supported, weak, or GAP, each tied to an evidence source (probe verdict / task / discovery / insight). Emits delivery needs for GAP/weak claims and backfills confirmed probe verdicts. Venue-neutral hypotheses (H1, H2, H3) live here; venue-specific RQ framing, Editor's Chair Test, and [primary] designation live in pitch (the cover letter). Markdown only. Use for claim ledger, claims, supported/weak/GAP, claim gap, evidence map, 1-claims."
argument-hint: "[paper-dir] [--backfill <probe-ref>] [--source <path>...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "3.1.2"
  last_updated: "2026-07-03"
  summary: "Claims stage orchestrator. Defines WHAT (hypothesis matrix, claim-evidence ledger, probe plans) and drives phases (draft -> probe -> revise -> check) internally. User invokes claims, not phases."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-paper-claims
=====================================

Stage orchestrator for the **claims** stage (stage 1, venue-FREE). The user invokes this skill; it drives the phases internally.

It answers one question:

```text
Which claims are supported, weak, or GAP, and what evidence settles each?
```

Every claim the paper wants to make is a row with a status and a source. The paper does not produce evidence; it selects judged evidence and tracks what is still missing. Unsupported or too-strong claims become delivery needs routed to probe/discover/task/insight, and confirmed verdicts are backfilled here.

Read first: `../../PHILOSOPHY.md`, `../../wiki/04-lifecycle-map.md`, `../../wiki/11-delivery-need.md`, `../../wiki/02-comment-lifecycle.md`.

## Artifact Spec

**Files produced:**
- `0-lifecycle/1-claims/1-claims.md` -- claim/evidence inventory
- `0-lifecycle/1-claims/_LOG_1-claims.md` -- phase progress journal (per `../../wiki/02-comment-lifecycle.md`)
- `0-lifecycle/1-claims/_EVIDENCE_1-claims.md` -- evidence backing per claim
- `0-lifecycle/1-claims/_PROBE/` -- probe plans for evidence gaps

**Content structure (1-claims.md):**
- Hypotheses -- venue-neutral H1, H2, H3 (what the paper tests)
- Claim-Evidence Matrix -- one row per claim with status at a glance
- Per-Claim Detail -- four-slot paragraphs (S1 claim+verdict, S2 verified statistic, S3 interpretation, S4 caveat+source)
- Discussion-Only Interpretations -- interpretive claims not in Results (optional)
- Robustness -- methods-level robustness checks (optional)
- Pending Evidence -- probes/tasks not yet run
- Hypothesis-Claim Alignment -- H-to-Claims validation, orphan check

**Done-criteria:**
- [ ] All claims have evidence status (supported/weak/GAP)
- [ ] No unaddressed GAP without a probe plan in _PROBE/
- [ ] Every supported claim has both stage 1 (file+number exist) and stage 2 (confirmed probe verdict)
- [ ] Hypotheses section with venue-neutral H1, H2, H3
- [ ] Hypothesis-Claim Alignment section maps each H to its claims
- [ ] Every claim row has a per-claim detail subsection (not just a matrix row)
- [ ] Evidence sources linked in _EVIDENCE_

## Phase Orchestration

When the user invokes `/haipipe-paper claims`, this skill drives the phases in order. The user does not call phase skills directly.

```
claims invoked
  │
  ▼
DRAFT ──→ illuminate existing claims, elicit taste,
          list hypotheses (H1, H2, H3), build claim-evidence matrix,
          write per-claim detail subsections (S1-S4)
          (internally calls /haipipe-paper-draft with this artifact spec)
  │
  ▼
PROBE ──→ link probes/tasks/discoveries to each claim,
          backfill confirmed verdicts, spawn probe plans for GAPs,
          emit delivery needs for weak/GAP rows
          (internally calls /haipipe-paper-probe)
  │
  ▼
REVISE ─→ refine claim statements, evidence descriptions,
          and hypothesis wording for clarity
          (internally calls /haipipe-paper-revise)
  │
  ▼
CHECK ──→ present exit gate: all claims backed? no aspirational
          anchors? hypothesis-claim alignment complete?
          user confirms → advance to venue
          (internally calls /haipipe-paper-check)
```

Comment lifecycle per `../../wiki/02-comment-lifecycle.md`: comments live in 1-claims.md while active, move to _LOG on resolve, each phase starts clean.

## Location

```text
<paper>/0-lifecycle/1-claims/1-claims.md           claim/evidence inventory
<paper>/0-lifecycle/1-claims/_LOG_1-claims.md       phase progress journal
<paper>/0-lifecycle/1-claims/_EVIDENCE_1-claims.md  evidence backing per claim
<paper>/0-lifecycle/1-claims/_PROBE/                probe plans for evidence gaps
```

Markdown only (argument documents don't need compilation).

## Template

The canonical template is the source of truth for section order: `ref/claims-template.md`

Reading order of the template:

```text
1. Hypotheses                  <- venue-neutral H1, H2, H3 (what we test)
2. Claim-Evidence Matrix       <- one row per claim, status at a glance
3. Per-Claim Detail            <- four-slot paragraphs (S1-S4) per claim
4. Discussion-Only Interp.     <- interpretive, not Results (optional)
5. Robustness                  <- Methods, not claimed (optional)
6. Pending Evidence            <- probes/tasks not yet run
7. Hypothesis-Claim Alignment  <- H->Claims validation (no venue framing)
```

The hypotheses are venue-neutral statements of what the paper tests. The same H1 can become RQ1 worded for JAMA or RQ1 worded for MISQ -- that reframing happens in pitch (the cover letter), not here.

For `weak`/`GAP` claims the subsection states the gap and the route instead of a statistic. Never write a "planned Table" as if it were evidence.

## Probe Plans Buffer

When the claims ledger identifies GAP/weak claims that need evidence, buffer probe plans in `_PROBE/` rather than dispatching immediately. Each probe plan is one file (`PPNN_<slug>.md`) with frontmatter (id, status, claim, source_ref) and structured fields (claim under test, evidence needed, expected route, constraints, datasets). The buffer index (`_PROBE/README.md`) tracks status (planned / dispatched / verdicted) and the dependency chain.

Probe plans are categorized by urgency:
- **MUST-HAVE**: blocks submission (GAP claims)
- **STRONGLY RECOMMENDED**: pre-empts reviewer objections
- **EXPLORATORY**: supplement material, not main claims

When probes return verdicts, backfill into the claims ledger.

## Ledger Maintenance

- New claim: add a row, set status from the cited source (default `GAP`).
- `--backfill <probe-ref>`: read the probe verdict; if confirmed, move the row to `supported` with the verdict path and any caveats; if refuted/partial, keep `weak` and note scope.
- Emit a delivery need for every `weak`/`GAP` row using the delivery-need interface, with the route:

```text
claim needs a verdict/robustness check   -> /haipipe-probe open <need>
claim needs outside context/citation     -> /haipipe-discovery <question>
claim needs a run or data artifact        -> /haipipe-task <contract>
```

Do not run evidence work here. Record needs and backfill verdicts.

## Evidence Gate

A claim row is done when:

- it has a status; `supported` requires BOTH stage 1 (cited file exists and the number appears in it) AND stage 2 (a confirmed probe verdict that the number supports the claim);
- it has its per-claim detail paragraph (the four slots), not just a matrix row;
- `weak`/`GAP` rows carry an open need + route; no row cites a "planned" anchor.

## Stage Gate

Beyond the per-row gate, the claims stage is NOT complete until the ledger also carries these REQUIRED items:

- a **Hypotheses** section with venue-neutral H1, H2, H3 (principle 1b); and
- a **Hypothesis-Claim Alignment** section that maps each H to its claims and checks for orphan claims (no H) or unanswered hypotheses (claims all GAP); and
- every claim row has a per-claim detail subsection (not just a matrix row).

Venue-specific items (Editor's Chair Test, [primary] designation, RQ framing) are NOT required here. They belong in pitch (the cover letter).

## Principles

1. One row per claim. Each row has a status and a source ref.
1b. **Venue-neutral hypotheses live here.** Claims holds hypotheses (H1, H2, H3) as venue-neutral statements of what the paper tests. Venue-specific RQ framing, the Editor's Chair Test, and [primary] designation live in pitch (the cover letter). The same hypotheses yield different RQ wording for different venues, but the underlying claim-evidence inventory stays the same.
2. Status vocabulary: `supported`, `weak`, `GAP`.
3. A claim is `supported` only when it traces to a CONFIRMED probe verdict or an equivalently judged artifact. Never mark `supported` from intuition.
4. `weak`/`GAP` rows must carry an open need and a route. They are first-class open needs surfaced by the Paper Console.
5. The paper must not overclaim. If evidence is `I` (information) but the claim needs `K` (knowledge), keep it `weak` and route a probe.
6. **Matrix plus per-claim detail.** The ledger is a compact MATRIX (ID, claim, status) followed by ONE subsection per claim; each subsection is a paragraph with four slots: (S1) claim + verdict, (S2) the verified statistic with spec and N, (S3) one-line interpretation, (S4) caveat + the source file. The matrix is the index; the subsections carry the evidence.
7. **No aspirational anchors.** "planned Table 1" is not evidence, it is GAP; a `supported` row cites a real value and the file it came from (e.g. `trait_l5 +12.90*** in main-ols_..._mme_ttl.csv`), never a future table.
8. **Two-stage evidence gate.** Stage 1 deterministic: the cited file exists AND the cited number actually appears in it (catches planned/hallucinated anchors, no model). Stage 2 verdict: a CONFIRMED probe judges the real number supports the claim. `supported` requires both; existence is not support.
9. **Venue-FREE.** The claims ledger is a pure evidence inventory, reusable across venues. It does NOT designate a [primary] claim, does NOT carry an Editor's Chair Test, and does NOT shape RQs to a venue. Those venue-aligned items live in pitch (the cover letter). If the paper retargets from venue A to venue B, the claims ledger stays unchanged; only pitch, narrative, display, and section-edit rewrite.

## Handoff

On CHECK confirm, update `STATUS.md` (`current_layer`, `maturity: claim-ledger`) and advance:

```text
promote     -> /haipipe-paper venue <paper-dir>    (pin target journal)
promote     -> /haipipe-paper pitch <paper-dir>    (if venue already pinned)
```

End the reply with the stage strip (run `../../../haipipe-paper/stage-strip.sh`).
