---
name: haipipe-paper-claims
description: "Stage orchestrator for the paper folder's 0-lifecycle/1-claims/1-claims.md + _LOG_1-claims.md: the venue-FREE claim/evidence inventory and evidence campaign brain, and THE HOME OF EVERY CLAIM'S STATUS (supported | refuted | inconclusive, with confidence and claim_type). Three sections: Hypotheses (what we test), Claims (what must be true, with status and → PP reference), Probes (the evidence plan, one per PP, full detail). Plans what evidence to collect, raises the questions the PROBE phase commissions to the task/discovery bank, and receives each answer as a probe section's `reading:`. Markdown only. Reads the RESOURCE stage's 1-resource.md: input/method/fit are settled there; claims owns evaluate/task-for-eval and marks a claim without its resource BLOCKED-ON-RESOURCE. Use for claim ledger, claims, supported/weak/GAP, blocked-on-resource, claim gap, evidence plan, probes, 1-claims."
argument-hint: "[paper-dir] [--backfill <PPNN>] [--source <path>...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "5.1.1"
  last_updated: "2026-07-14"
  summary: "Claims stage orchestrator. The evidence campaign brain: plans evidence needs, raises the questions, receives what returns. Three sections (Hypotheses, Claims, Probes) + Evidence Campaign summary. Drives phases (draft -> probe -> revise -> check) internally. Receives from the RESOURCE stage: claims owns evaluate/task-for-eval only; input/method/fit are settled in 1-resource.md, and a claim without its resource is BLOCKED-ON-RESOURCE. v5.1 (probe redesign, Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14; mirrors haipipe-application-claims 5.2.0): THE CLAIM LEDGER IS NOW THE ONLY HOME OF A CLAIM'S STATUS. R7 killed the probe '## Verdict' block and the 'verdicted' state, so supported|refuted|inconclusive + confidence + claim_type land HERE, per-claim, per-paper, private — a probe section's `reading:` FEEDS this ledger and no longer carries a judgment of its own. Probe files live at 1-probes/PPNN_<topic>.md (one file per TOPIC, one SECTION per question); the per-stage _PROBE/ folder and the 1-probe-plans/ index are RETIRED. The PROBE phase runs the five-step loop (ORGANIZE -> MATCH -> DISPATCH -> POINT -> INTERPRET) and commissions to the task/discovery orchestrators direct (the probe gateway is retired). --backfill reads the section's `reading:`, not a verdict block. Ledger PP entries carry a DERIVED `State:` (planned|commissioned|answered|read), never the deleted `dispatched`. v5.1.1: every shared-convention pointer was off by one `../` — `../../PHILOSOPHY.md` / `../../wiki/<page>.md` resolved to 1-lifecycle/, which holds neither. The stage skills sit TWO levels under skills/paper/ (1-lifecycle/<N>-<stage>/<skill>/), so the correct depth is `../../../`. Every required-read at the top of this skill silently failed. Repointed."
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
               what evidence would settle each? (the evidence plan, one per PP)

2. OUTSOURCE   each GAP claim raises a QUESTION; the PROBE phase collects it into
               1-probes/PPNN_<topic>.md as a SECTION, MATCHes it against the bank's
               QA corpus, and commissions only what is missing to tasks/ or discoveries/
               claims writes the NEED, never the execution spec

3. COLLECT     answers come back as a section's `reading:` at INTERPRET
               THE STATUS LANDS HERE: supported | refuted | inconclusive
               verified numbers go to _VALUES_
               claims RECEIVES evidence, never PRODUCES it
```

**THE CLAIM'S STATUS LIVES IN THIS LEDGER, AND NOWHERE ELSE** (R7, 2026-07-14). A probe file does not judge — it carries the evidence's MEANING for this paper (its `reading:`), and that is all. The judgment — `supported | refuted | inconclusive`, plus `confidence` and `claim_type` — is written HERE, per-claim, private to this paper, by the author reading the answered QA file. Two papers reading the SAME bank fact may reach different judgments about their own claims, and that is correct: the fact is shared, the judgment is not.
💀 The probe `## Verdict` block and the `verdicted` state are DELETED. Do not write either, and do not wait for one.

Read first: `../../../PHILOSOPHY.md`, `../../../wiki/04-lifecycle-map.md`, `../../../wiki/11-delivery-need.md`, `../../../wiki/02-comment-lifecycle.md`.

**Inputs (binding).** Claims READS `0-lifecycle/1-resource/1-resource.md` — the venue-free RESOURCE contract that now sits between seed and claims — before it writes anything.
Its `N<n>` demand rows and their Q/A answers say what EXISTS and whether it can CARRY a claim.
Claims may NOT assert a claim whose demand row has no resource: that claim is `BLOCKED-ON-RESOURCE` (or the demand was a scope cut at the resource gate, and the claim does not exist at all).
Preconditions are settled THERE, not here — the "Feasibility & constraints (preconditions, not claims)" material that used to squat in this ledger is the resource stage's business now.

## Artifact Spec

**Files produced:**
- `0-lifecycle/1-claims/1-claims.md` -- claim/evidence inventory + the evidence plan + the campaign
- `0-lifecycle/1-claims/_LOG_1-claims.md` -- phase progress journal (per `../../../wiki/02-comment-lifecycle.md`)
- `0-lifecycle/1-claims/_CITATION_1-claims.md` -- citation candidates harvested from the answering QA files
- `0-lifecycle/1-claims/_VALUES_1-claims.md` -- verified numbers backing each supported claim
- `1-probes/PPNN_<topic>.md` -- the probe FILES (paper root, one per TOPIC, one SECTION per question). NOT a per-stage `_PROBE/` folder, NOT a `1-probe-plans/` index: both are RETIRED.

**Content structure (1-claims.md) -- three sections + summary:**

```text
Hypotheses (venue-neutral)     what we test (H1, H2, H3), venue-free
Claims                         one **C<n>** per claim: statement + status + → PP reference
Probes                         one **PP<nn>** per probe: full evidence plan, organized by probe number
Evidence Campaign              dispatch order + summary (compact overview)
```

- **Hypotheses** are venue-neutral statements of what the paper tests. The same H1 can become RQ1 for JAMA or MISQ -- that reframing happens in pitch, not here.
- **Claims** are short: the testable statement, current status (supported/weak/GAP/BLOCKED-ON-RESOURCE), and which probe settles it. No inline study design.
- **Probes** carry the full evidence plan per PP number: type (task/discovery), which claims it settles, dependencies, what work to do, design decisions. This is where the brain thinks.
- **Evidence Campaign** is a compact dispatch-order diagram + summary table showing all probes, status, and dependencies.

No separate Hypothesis-Claim Alignment section. The alignment is in the tags: `C1 (H1)`, `PP03 (C1/C3/C7)`.

**The judgment fields (written HERE, at INTERPRET, when a probe section's `reading:` lands):**

```text
status       supported | refuted | inconclusive      (the enum; nothing else is a status)
confidence   how strongly the evidence carries the claim
claim_type   associational | causal | in-sample | generalizing   (never upgraded by confidence —
             the author's OWN overclaim check; never say "causes" from associational evidence)
```

The ledger's own progress vocabulary (`supported` · `weak` · `GAP` · `BLOCKED-ON-RESOURCE`) is what a claim wears while the campaign runs; the enum above is what SETTLES it.

**Formatting:**
- Heading style: `=====` for the document title, `-----` for sections. No `#`/`##`/`###`.
- Sub-items within sections: `**bold**` text (e.g. `**C1 - title - status**`, `**PP03 - title - status**`).
- One sentence per line (semantic line breaks). No dense multi-sentence paragraphs.
- Probes separated by `---` horizontal rules.

**Done-criteria:**
- [ ] All claims have evidence status (supported/weak/GAP/BLOCKED-ON-RESOURCE)
- [ ] No unaddressed GAP without an evidence plan in the Probes section and a question SECTION in 1-probes/
- [ ] No claim asserted whose resource demand row (in `0-lifecycle/1-resource/1-resource.md`) has no resource — that claim is `BLOCKED-ON-RESOURCE`, and it names the `N<n>` it waits on
- [ ] No pointer that RESOURCE explicitly DECLINED to claims (per `0-lifecycle/1-resource/_LOG_1-resource.md`) is left unconsumed here — each is either a PP entry in Probes or explicitly declined in `_LOG`. Seed's `[FORWARD -> ...]` pointers themselves are NOT checked here: RESOURCE is their sole consumer, and a pointer resource consumed is DONE
- [ ] Every supported claim has both stage 1 (file+number exist) and stage 2 (a probe SECTION whose `reading:` is written and whose `target:` QA file RESOLVES on disk)
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

**Comment rules (binding).** The agent NEVER deletes, rewords, or relocates a `> USER:` comment; it replies `> CC:` underneath; only the user resolves a thread; resolved threads MOVE to `_LOG` verbatim. Working files are edited surgically — no full-file rewrite of a file carrying `> USER:` comments. Background: `../../../wiki/02-comment-lifecycle.md`.

```
claims invoked
  │
  ▼
DRAFT ──→ FIRST: read 0-lifecycle/1-resource/1-resource.md — the N demand rows and
          their Q/A answers. A claim whose demand row has no resource is
          BLOCKED-ON-RESOURCE, never GAP, and never a build probe here.
          Seed's `[FORWARD -> ...]` pointers are NOT consumed here. RESOURCE is
          their SOLE consumer (it greps `_LOG_0-seed.md` at its own DRAFT, glyph-
          and legacy-tolerant, and turns each into an N row, a Q, or an explicit
          DECLINE). Read `_LOG_1-resource.md` for the ones resource DECLINED to
          claims — those, and ONLY those, are ours: each becomes a PP entry in
          Probes, or is declined again with a `_LOG` note. Re-consuming a pointer
          resource already took DOUBLE-DISPATCHES the same build.
          Then: illuminate existing claims, elicit taste,
          list hypotheses (H1, H2, H3), write claims (short, with → PP ref),
          write probes (full evidence plan per PP), write evidence campaign
          (internally calls /haipipe-paper-draft with this artifact spec)
          Ends at ⛔ STOP: user reviews, iterates, approves ([GATE] logged).
  │
  ▼
PROBE ──→ haipipe-paper-probe runs the five-step loop over the questions DRAFT raised:
          ①ORGANIZE them into 1-probes/ ②MATCH the bank's QA corpus ③DISPATCH only
          what is missing ④POINT target: at the answering QA file ⑤INTERPRET
          COLLECT: the reading lands, THE CLAIM'S STATUS FLIPS HERE, numbers to _VALUES_
          (internally calls /haipipe-paper-probe)
  │
  ▼
REVISE ─→ refine claim statements, evidence-plan clarity,
          campaign ordering, and hypothesis wording
          (internally calls /haipipe-paper-revise; [REVISE] _LOG entry carries workers: proof)
  │
  ▼
CHECK ──→ present exit gate: all claims backed? no aspirational
          anchors? an evidence plan for every GAP? every settled claim
          traced to a RESOLVING target:?
          user confirms → advance to venue
          (internally calls /haipipe-paper-check)
```

Phase visibility per the Phase Transition Contract in `../../../wiki/08-stage-gate.md`: announce every phase boundary (reply line + `[PHASE]` entry in `_LOG` + phase-line 🔥 moves); skip a phase only by an explicit logged verdict (`[PROBE] skipped -- <reason>`, phase line shows `--`); CHECK is never implicit -- it opens by presenting the exit-criteria report and the approval ask.

Comment lifecycle per `../../../wiki/02-comment-lifecycle.md`: comments live in 1-claims.md while active, move to _LOG on resolve, each phase starts clean.

## Location

```text
<paper>/0-lifecycle/1-claims/1-claims.md            claim/evidence inventory + the evidence plan
<paper>/0-lifecycle/1-claims/_LOG_1-claims.md        phase progress journal
<paper>/0-lifecycle/1-claims/_CITATION_1-claims.md   citation candidates from the answering QA files
<paper>/0-lifecycle/1-claims/_VALUES_1-claims.md     verified numbers backing each claim
<paper>/1-probes/PPNN_<topic>.md                     the probe FILES (one per topic, one SECTION per question)
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

**PP01 - <title> - <state>**

Type: <task | discovery>.
Claims: <which claims this settles>.
State: <planned | commissioned | answered | read>   (DERIVED from the probe file, never asserted)

<full evidence plan, one sentence per line>
Detail: `1-probes/PP01_<topic>.md` (the question's SECTION)

---

**PP02 - ...**

...


Evidence Campaign
-----------------

(dispatch order diagram + summary table)
```

## The evidence plan (the Probes section)

Each claim's GAP/weak status generates an entry in the Probes section. That section is the primary record of what evidence work to commission. The probe FILE at `1-probes/PPNN_<topic>.md` is where the QUESTION is actually posed — as a SECTION — and bound by PATH to its answer.

Probes are categorized by urgency:
- **MUST-HAVE**: blocks the main experimental line
- **STRONGLY RECOMMENDED**: pre-empts reviewer objections
- **EXPLORATORY**: supplement material, not main claims

Also organize probes by **pipeline stage — one probe = one unit of work = one task type**. Do NOT bundle build + fit + evaluate into a single probe: decompose so each stage is independently runnable and resumable (a stalled fit must not force rebuilding the data). For an experimental (model) claim, claims owns exactly ONE of those stages:

| stage | task type | role |
|---|---|---|
| evaluate | `task-for-eval` | score -> the metrics that SETTLE the claim |

The other three stages -- input (`task-for-data`), method (`task-for-algo`), fit (`task-for-fit`) -- are **settled in the RESOURCE stage**, not here (`0-lifecycle/1-resource/1-resource.md`). They BUILD what must exist. This is the cleavage rule: a question that CHANGES what exists on disk -> RESOURCE; a question that READS what exists and MOVES A CLAIM'S STATUS -> CLAIMS. A claim CITES the resource answer (its `N<n>` demand row and that row's Q/A) rather than re-planning the build inside the argument document. If the resource is not there, the claim is `BLOCKED-ON-RESOURCE` — it does not get a build probe here.

Two rules that follow:
- **The evaluation probe settles the claim.** A claim's evidence pointer names the eval probe, which chains back fit <- data. Fit makes the model; eval makes the evidence. (A bundled fit+eval probe entangles the verdict — split them.)
- **Task settles claims; discovery is reserved for method-investigation and external data/context.** Discovery alone never settles an internal experimental claim; it feeds the method (`task-for-algo`) or supplies an external cohort/citation.

When a probe section's `reading:` lands, write here:
- The claim's status line — `supported | refuted | inconclusive` + confidence + claim_type. THIS is where a claim's status lives.
- `_VALUES_` with the verified number.
- The evidence pointer: the section's `target:`, the path of the answering QA file, which must RESOLVE on disk.

## _VALUES_ Satellite

`_VALUES_1-claims.md` holds the verified numbers backing each supported claim. One section per claim with fields: statistic, spec, source, verified. Claims.md says "supported" and points here. This keeps claims.md clean prose while numbers are auditable in one place.

## Ledger Maintenance

- New claim: add a `**C<n>**` sub-item in Claims, set status from the cited source (default `GAP`), add a probe entry in Probes.
- `--backfill <probe-ref>`: **THIS LEDGER IS THE ONLY HOME OF A CLAIM'S STATUS.** There is no probe verdict to read — `## Verdict` and the `verdicted` state are DELETED (R7). Read the probe SECTION's `reading:` (its interpretation, in this paper's vocabulary) and, for a `mode: full` section, the answered QA file it points at. Write `supported | refuted | inconclusive` + confidence + claim_type HERE, per-claim, private to this paper. The EVIDENCE POINTER is the section's `target:` — the path of the answering QA file (`tasks|discoveries/<discovery-group>/<discovery-folder>/QA/<n>-<slug>.md`), which must RESOLVE on disk. Record the number in `_VALUES_`.
- Emit a delivery need for every `weak`/`GAP` claim using the delivery-need interface, with the route:

```text
claim needs its status settled           -> a question SECTION (task-for-eval; chains fit <- data)
claim needs outside context/citation     -> a question SECTION (discovery-shaped)

claim needs a dataset built              -> NOT A CLAIMS PROBE. It is a DEMAND, and it
claim needs a model trained                 belongs to RESOURCE (task-for-data /
claim needs a new method tried              task-for-fit / task-for-algo, in
                                            0-lifecycle/1-resource/1-resource.md).
                                            Until it lands, the claim is
                                            BLOCKED-ON-RESOURCE.
```

Do not run evidence work here. Design the campaign, commission the work, record results.

## Evidence Gate

A claim sub-item is done when:

- it has a status; `supported` requires BOTH stage 1 (the cited file exists and the number appears in it) AND stage 2 (a probe SECTION whose `target:` RESOLVES to a QA file on disk and whose `reading:` says that number carries the claim — judged HERE, per the judgment fields above);
- `weak`/`GAP` claims have a corresponding probe entry in the Probes section with a clear plan;
- a claim whose resource is UNOBTAINABLE or not yet built is `BLOCKED-ON-RESOURCE`, NOT a "GAP with a plan". It carries no probe entry here; it names the resource row it waits on (`-> N<n>` in `1-resource.md`) and the reason it is unfalsifiable. (Live case: Paper-CGMtoAge's H2 and H3 both depend on a dataset whose access application has not been filed. Calling those GAPs would pretend a plan exists.)
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
5. Status vocabulary: `supported`, `weak`, `GAP`, `BLOCKED-ON-RESOURCE`. A `GAP` has a plan; a `BLOCKED-ON-RESOURCE` claim is UNFALSIFIABLE until its resource lands, and saying so is the honest state.
6. A claim is `supported` only when it traces to a QA file in the bank, through a probe section's `target:` and `reading:`. Never mark `supported` from intuition, and never wait for a probe file to say so — probe files no longer judge. **The judgment is OURS; the fact is not:** the bank's QA files speak general language and belong to every consumer, and this ledger interprets them for THIS paper. Never push our claim ids back into the bank.
7. `weak`/`GAP` claims must have a corresponding probe. They are first-class open needs surfaced by the Paper Console.
8. The paper must not overclaim. If the evidence is in-sample only (a pattern inside one dataset, with no generalization basis) while the claim asserts it holds beyond that sample, keep it `weak` and route a probe.
9. **No tables for claims.** The ledger is prose only. Sub-items, not table cells. (The Evidence Campaign summary table is the exception -- it is a compact overview, not the primary record.)
10. **No aspirational anchors.** "planned Table 1" is not evidence, it is GAP.
11. **Two-stage evidence gate.** Stage 1 deterministic: the cited file exists AND the cited number actually appears in it. Stage 2 judgment: a probe section whose `target:` RESOLVES, whose `reading:` interprets it, and whose judgment (written here) says the number carries the claim. `supported` requires both.
15. **This stage never executes bank work inline** (LAW 1). It raises questions; `haipipe-paper-probe` binds them. A claims session that opens `tasks/.../results/` and starts writing has already broken the wall, whatever it ends up writing.
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
