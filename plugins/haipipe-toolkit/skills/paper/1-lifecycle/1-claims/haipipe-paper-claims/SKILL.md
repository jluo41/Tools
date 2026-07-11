---
name: haipipe-paper-claims
description: "Stage orchestrator for the paper folder's 0-lifecycle/1-claims/1-claims.md + _LOG_1-claims.md: the venue-FREE claim/evidence inventory and evidence campaign brain. Three sections: Hypotheses (what we test), Claims (what must be true, with status and probe reference), Probes (the evidence plan, one per PP, full detail). Plans what evidence to collect, commissions the work via tasks/discoveries, and tracks results as they return. Markdown only. Use for claim ledger, claims, supported/weak/GAP, claim gap, evidence plan, probes, 1-claims."
argument-hint: "[paper-dir] [--backfill <probe-ref>] [--source <path>...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "4.3.0"
  last_updated: "2026-07-10"
  summary: "Claims stage orchestrator. The evidence campaign brain: plans evidence needs, commissions work (tasks/discoveries), tracks results. Three sections (Hypotheses, Claims, Probes) + Evidence Campaign summary. Drives phases (draft -> probe -> revise -> check) internally."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-paper-claims
=====================================

Stage orchestrator for the **claims** stage (stage 1, venue-FREE). The user invokes this skill; it drives the phases internally.

It answers one question:

```text
Which claims are supported, weak, or GAP, and what evidence settles each?
```

Claims is the **evidence campaign brain**. It does three jobs in sequence:

```text
1. PLAN        what must be true? (hypotheses, claims)
               what evidence would settle each? (probe plan per claim)

2. OUTSOURCE   dispatch to tasks/ and discoveries/
               each GAP claim → a probe that routes to task or discovery
               claims writes the NEED, not the execution spec

3. COLLECT     results come back from tasks/discoveries
               backfill status: GAP → weak → supported
               verified numbers go to _VALUES_
               claims RECEIVES evidence, never PRODUCES it
```

The paper does not produce evidence; claims designs the campaign, commissions the work, and tracks what returns. Unsupported or too-strong claims become probe plans routed to task/discover/insight, and confirmed verdicts are backfilled here.

Read first: `../../PHILOSOPHY.md`, `../../wiki/04-lifecycle-map.md`, `../../wiki/11-delivery-need.md`, `../../wiki/02-comment-lifecycle.md`.

## Artifact Spec

**Files produced:**
- `0-lifecycle/1-claims/1-claims.md` -- claim/evidence inventory and probe plans
- `0-lifecycle/1-claims/_LOG_1-claims.md` -- phase progress journal (per `../../wiki/02-comment-lifecycle.md`)
- `0-lifecycle/1-claims/_CITATION_1-claims.md` -- citation candidates harvested from probes/discoveries
- `0-lifecycle/1-claims/_VALUES_1-claims.md` -- verified numbers backing each supported claim
- `0-lifecycle/1-claims/_PROBE/` -- probe plan files (execution detail per PP)

**Content structure (1-claims.md) -- three sections + summary:**

```text
Hypotheses (venue-neutral)     what we test (H1, H2, H3), venue-free
Claims                         one **C<n>** per claim: statement + status + → PP reference
Probes                         one **PP<nn>** per probe: full evidence plan, organized by probe number
Evidence Campaign              dispatch order + summary (compact overview)
```

- **Hypotheses** are venue-neutral statements of what the paper tests. The same H1 can become RQ1 for JAMA or MISQ -- that reframing happens in pitch, not here.
- **Claims** are short: the testable statement, current status (supported/weak/GAP), and which probe settles it. No inline study design.
- **Probes** carry the full evidence plan per PP number: type (task/discovery), which claims it settles, dependencies, what work to do, design decisions. This is where the brain thinks.
- **Evidence Campaign** is a compact dispatch-order diagram + summary table showing all probes, status, and dependencies.

No separate Hypothesis-Claim Alignment section. The alignment is in the tags: `C1 (H1)`, `PP03 (C1/C3/C7)`.

**Formatting:**
- Heading style: `=====` for the document title, `-----` for sections. No `#`/`##`/`###`.
- Sub-items within sections: `**bold**` text (e.g. `**C1 - title - status**`, `**PP03 - title - status**`).
- One sentence per line (semantic line breaks). No dense multi-sentence paragraphs.
- Probes separated by `---` horizontal rules.

**Done-criteria:**
- [ ] All claims have evidence status (supported/weak/GAP)
- [ ] No unaddressed GAP without a probe plan in the Probes section
- [ ] No unconsumed `[FORWARD -> CLAIMS]` pointer in seed's `_LOG_0-seed.md` — each is either a PP entry in Probes or explicitly declined in `_LOG`
- [ ] Every supported claim has both stage 1 (file+number exist) and stage 2 (confirmed probe verdict)
- [ ] Hypotheses section with venue-neutral H1, H2, H3
- [ ] Every claim has its own `**C<n>**` sub-item with status and probe reference
- [ ] Every probe has its own `**PP<nn>**` sub-item with full evidence plan
- [ ] Evidence Campaign shows dispatch order and dependencies
- [ ] Verified numbers recorded in _VALUES_

## Phase Orchestration

When the user invokes `/haipipe-paper claims`, this skill drives the phases in order. The user does not call phase skills directly — but steers them with VERBS on this stage:

```
/haipipe-paper claims <paper-dir>            -> open: status + frontier; advance ONLY on the user's verb
/haipipe-paper claims <paper-dir> draft      -> run/redo DRAFT  -> STOP for user review
/haipipe-paper claims <paper-dir> probe      -> run/redo PROBE  (agent-only)
/haipipe-paper claims <paper-dir> revise     -> dispatch REVISE workers (agent-only, proof-carrying)
/haipipe-paper claims <paper-dir> check      -> open the CHECK gate
```

**Hard gates (binding).** After DRAFT: ⛔ STOP — present the draft for review and end the turn; the user's verb/"go" advances, logged as `[GATE] draft-review: approved` quoting the user. Each phase runs via its `Skill()` dispatch — a phase executed inline did not happen; the `[REVISE]` _LOG entry carries its `workers:` proof line. Never commit or conclude the stage before CHECK opens with its report. The agent never self-advances past a gate.

**Comment rules (binding).** The agent NEVER deletes, rewords, or relocates a `> USER:` comment; it replies `> CC:` underneath; only the user resolves a thread; resolved threads MOVE to `_LOG` verbatim. Working files are edited surgically — no full-file rewrite of a file carrying `> USER:` comments. Background: `../../wiki/02-comment-lifecycle.md`.

```
claims invoked
  │
  ▼
DRAFT ──→ FIRST: consume seed's forward pointers — grep `_LOG_0-seed.md` for
          `[FORWARD -> CLAIMS]` lines; each becomes a PP entry in the Probes
          section (or is explicitly declined with a `_LOG` note). An
          unconsumed pointer fails the CHECK done-criteria below.
          Then: illuminate existing claims, elicit taste,
          list hypotheses (H1, H2, H3), write claims (short, with → PP ref),
          write probes (full evidence plan per PP), write evidence campaign
          (internally calls /haipipe-paper-draft with this artifact spec)
          Ends at ⛔ STOP: user reviews, iterates, approves ([GATE] logged).
  │
  ▼
PROBE ──→ link probes/tasks/discoveries to each claim,
          backfill confirmed verdicts, spawn probe plans for GAPs,
          emit delivery needs for weak/GAP rows
          (internally calls /haipipe-paper-probe)
  │
  ▼
REVISE ─→ refine claim statements, probe plan clarity,
          evidence descriptions, and hypothesis wording
          (internally calls /haipipe-paper-revise; [REVISE] _LOG entry carries workers: proof)
  │
  ▼
CHECK ──→ present exit gate: all claims backed? no aspirational
          anchors? probe plans complete for all GAPs?
          user confirms → advance to venue
          (internally calls /haipipe-paper-check)
```

Phase visibility per the Phase Transition Contract in `../../wiki/08-stage-gate.md`: announce every phase boundary (reply line + `[PHASE]` entry in `_LOG` + phase-line 🔥 moves); skip a phase only by an explicit logged verdict (`[PROBE] skipped -- <reason>`, phase line shows `--`); CHECK is never implicit -- it opens by presenting the exit-criteria report and the approval ask.

Comment lifecycle per `../../wiki/02-comment-lifecycle.md`: comments live in 1-claims.md while active, move to _LOG on resolve, each phase starts clean.

## Location

```text
<paper>/0-lifecycle/1-claims/1-claims.md            claim/evidence inventory + probe plans
<paper>/0-lifecycle/1-claims/_LOG_1-claims.md        phase progress journal
<paper>/0-lifecycle/1-claims/_CITATION_1-claims.md   citation candidates from probes/discoveries
<paper>/0-lifecycle/1-claims/_VALUES_1-claims.md     verified numbers backing each claim
<paper>/0-lifecycle/1-claims/_PROBE/                 probe plan files (execution detail)
```

Markdown only (argument documents don't need compilation).

## Template

The canonical template is the source of truth for section order: `ref/claims-template.md`

```markdown
1-claims: <paper title> (venue-free claim/evidence inventory)
==============================================================

Date: YYYY-MM-DD
Status: DRAFT
This ledger plans what evidence to collect, commissions the work, and tracks results as they return.


Hypotheses (venue-neutral)
--------------------------

- **H1 (core).** ...
- **H2 (boundary).** ...
- **H3 (mechanism).** ...


Claims
------

**C1 - <title> (H1, <role>) - <status>**

<claim statement, one sentence per line>
Evidence: -> PP<nn> (<short description>).

**C2 - ...**

...


Probes
------

**PP01 - <title> - <status>**

Type: <task | discovery>.
Claims: <which claims this settles>.
Status: <planned | dispatched | done>.

<full evidence plan, one sentence per line>
Detail: `_PROBE/PP01_<slug>.md`

---

**PP02 - ...**

...


Evidence Campaign
-----------------

(dispatch order diagram + summary table)
```

## Probe Plans

Each claim's GAP/weak status generates a probe plan in the Probes section. The Probes section is the primary record of what evidence work to commission. The `_PROBE/` files carry the execution detail for dispatch.

Probes are categorized by urgency:
- **MUST-HAVE**: blocks the main experimental line
- **STRONGLY RECOMMENDED**: pre-empts reviewer objections
- **EXPLORATORY**: supplement material, not main claims

Also organize probes by **pipeline stage — one probe = one unit of work = one task type**. Do NOT bundle build + fit + evaluate into a single probe: decompose so each stage is independently runnable and resumable (a stalled fit must not force rebuilding the data). For an experimental (model) claim the stages map to the haipipe task types:

| stage | task type | role |
|---|---|---|
| input | `task-for-data` | build / assemble the dataset (AIData) |
| method | `discovery` + `task-for-algo` | investigate + prototype a method (feeds fit) |
| fit | `task-for-fit` | train the model -> produces predictions |
| evaluate | `task-for-eval` | score -> the metrics that SETTLE the claim |

Two rules that follow:
- **The evaluation probe settles the claim.** A claim's evidence pointer names the eval probe, which chains back fit <- data. Fit makes the model; eval makes the evidence. (A bundled fit+eval probe entangles the verdict — split them.)
- **Task settles claims; discovery is reserved for method-investigation and external data/context.** Discovery alone never settles an internal experimental claim; it feeds the method (`task-for-algo`) or supplies an external cohort/citation.

When probes return verdicts, backfill into:
- The claim's status line (GAP -> weak -> supported)
- `_VALUES_` with the verified number
- The probe's status (planned -> done) with takeaways inline

## _VALUES_ Satellite

`_VALUES_1-claims.md` holds the verified numbers backing each supported claim. One section per claim with fields: statistic, spec, source, verified. Claims.md says "supported" and points here. This keeps claims.md clean prose while numbers are auditable in one place.

## Ledger Maintenance

- New claim: add a `**C<n>**` sub-item in Claims, set status from the cited source (default `GAP`), add a probe entry in Probes.
- `--backfill <probe-ref>`: read the probe verdict; if confirmed, move the claim to `supported` with the verdict path and any caveats; if refuted/partial, keep `weak` and note scope. Record the number in `_VALUES_`.
- Emit a delivery need for every `weak`/`GAP` claim using the delivery-need interface, with the route:

```text
claim needs a verdict/robustness check   -> probe (task-for-eval; chains fit <- data)
claim needs outside context/citation     -> probe (discovery)
claim needs a dataset built              -> probe (task-for-data)
claim needs a model trained              -> probe (task-for-fit)
claim needs a new method tried           -> probe (discovery + task-for-algo)
```

Do not run evidence work here. Design the campaign, commission the work, record results.

## Evidence Gate

A claim sub-item is done when:

- it has a status; `supported` requires BOTH stage 1 (cited file exists and the number appears in it) AND stage 2 (a confirmed probe verdict that the number supports the claim);
- `weak`/`GAP` claims have a corresponding probe entry in the Probes section with a clear plan;
- no claim cites a "planned" anchor as evidence.

## Stage Gate

The claims stage is NOT complete until:

- a **Hypotheses** section with venue-neutral H1, H2, H3;
- every claim has its own `**C<n>**` sub-item with status and probe reference;
- every GAP/weak claim has a corresponding probe in the Probes section;
- the **Evidence Campaign** shows dispatch order and dependencies;
- no aspirational anchors cited as evidence.

Venue-specific items (Editor's Chair Test, [primary] designation, RQ framing) are NOT required here. They belong in pitch (the cover letter).

## Principles

1. **Claims is the evidence campaign brain.** It plans what evidence is needed, commissions the work, and tracks results. Three jobs: plan, outsource, collect.
2. **Three sections.** Hypotheses (what we test), Claims (what must be true), Probes (the evidence plan). Plus Evidence Campaign (birds-eye summary). No separate H-C Alignment section -- the tags do the work.
3. **Claims are short.** Statement + status + probe reference. The thinking lives in the Probes section, not inline in each claim.
4. **Probes carry the full plan.** Each probe is its own sub-item with type, claims, status, dependencies, and the full evidence design. This is where the brain thinks.
5. Status vocabulary: `supported`, `weak`, `GAP`.
6. A claim is `supported` only when it traces to a CONFIRMED probe verdict or an equivalently judged artifact. Never mark `supported` from intuition.
7. `weak`/`GAP` claims must have a corresponding probe. They are first-class open needs surfaced by the Paper Console.
8. The paper must not overclaim. If evidence is `I` (information) but the claim needs `K` (knowledge), keep it `weak` and route a probe.
9. **No tables for claims.** The ledger is prose only. Sub-items, not table cells. (The Evidence Campaign summary table is the exception -- it is a compact overview, not the primary record.)
10. **No aspirational anchors.** "planned Table 1" is not evidence, it is GAP.
11. **Two-stage evidence gate.** Stage 1 deterministic: the cited file exists AND the cited number actually appears in it. Stage 2 verdict: a CONFIRMED probe judges the real number supports the claim. `supported` requires both.
12. **Venue-FREE.** The claims ledger is a pure evidence inventory, reusable across venues. No [primary] claim, no Editor's Chair Test, no venue-specific RQ framing. Those live in pitch.
13. **One sentence per line.** Semantic line breaks for readability. No dense multi-sentence paragraphs.
14. **Heading style.** `=====` for the document title, `-----` for sections. Sub-items as `**bold**`. No `#`/`##`/`###`.

## Handoff

On CHECK confirm, update `STATUS.md` (`current_layer`, `maturity: claim-ledger`) and advance:

```text
promote     -> /haipipe-paper venue <paper-dir>    (pin target journal)
promote     -> /haipipe-paper pitch <paper-dir>    (if venue already pinned)
```

End the reply with the stage strip (run `../../../haipipe-paper/stage-strip.sh`).
