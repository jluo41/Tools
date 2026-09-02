---
name: haipipe-discovery-workflow
description: >-
  The Discovery family workflow and Folder-kind router. It resolves one
  folder-kind discovery Task Page through the D1 Inquiry phase and its five
  executable cycles: SCOPE, optional PREPARE, ACQUIRE, SYNTHESIZE, and CLOSE.
  It keeps authoritative L3 Page/Task changes separate from one-Subject L4
  Paper/Source Runs. Use when routing, presenting, or validating a Discovery
  Folder, its BJTR lifecycle, or its cross-face closure.
metadata:
  version: "0.2.0"
  last_updated: "2026-09-02"
---

# /haipipe-discovery-workflow · D1 Inquiry, five explicit cycles

`haipipe-discovery` is the user door. This skill is the ownership machine
beneath it: it resolves the Folder kind, publishes the complete Workflow
Table, and prevents Page, Task, Run, and Evidence authorities from collapsing.

## Order

```text
D1 Inquiry

┌──────── Frame ────────┐  ┌── Evidence ──┐  ┌──── Article ────┐
SCOPE ──> PREPARE? ───────> ACQUIRE ─────────> SYNTHESIZE ───────> CLOSE
                                  ▲                 │
                                  └── need more ────┘
```

D1 is the sole formal Phase. The five names above are Cycles, not another
phase hierarchy. A revised question that changes the evidence population
opens a new `tNN_` Task rather than silently changing the existing Subject
population.

## Canonical Workflow Table

| Row ID | Part | Phase | Cycle | Purpose | Input / policy | L3 Task/Page content modified | L4 Run profile | Output | Exit gate | Next route | Human gate |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `d1.scope` | Frame | D1 Inquiry | SCOPE | Freeze the question, article promise, source boundary, and admission rule. | BJTR parent, question, `discovery_type`, Page grammar | `discovery.yaml` intent and root Page opening/boundary | none | scoped Discovery Task Page | BJTR path, manifest, Page, type, and admission rule agree | `d1.prepare`, `d1.acquire`, `HOLD` | none |
| `d1.prepare` | Frame | D1 Inquiry | PREPARE | Author reusable search, extraction, or synthesis support only when needed. | frozen scope and `instrument` declaration | optional `scripts/`; no empty lane | none | declared instrument or explicit omission | declared path exists and is reusable, or `instrument.needed: false` | `d1.acquire`, `HOLD` | none |
| `d1.acquire` | Evidence | D1 Inquiry | ACQUIRE | Resolve Triggers, admit canonical Subjects, and produce one truthful analysis Result per Subject. | scope/admission rule, Trigger provenance, Paper Run contract | Task progress/receipt links only; root Page claims remain unchanged | Discovery · `paper-analysis`/`source-analysis` · `N_admitted`; exactly one Subject per Run | reused or newly paired Run/Results plus returned/logged Trigger dispositions | every admitted Subject has one valid same-stem Ticket/Result pair; zero-Subject and unchanged duplicate Triggers open no Run | `d1.acquire`, `d1.synthesize`, `HOLD` | none |
| `d1.synthesize` | Article | D1 Inquiry | SYNTHESIZE | Promote completed Results into the promised article and its citation projection. | accepted Results, Page Type promise, Evidence citation contract | root Page Content/Aims, optional typed record, derived `evidence/bibex/<task>.bib` | none | evidence-backed Page synthesis with Result links, cite keys, disagreements, and limits | every factual claim resolves to a complete Result/cite key and the `discovery_type` promise is met | `d1.acquire`, `d1.close`, `HOLD` | none; record citation-verification debt |
| `d1.close` | Article | D1 Inquiry | CLOSE | Reconcile the two Faces and publish the final outcome/receipt. | synthesized Page, `discovery.yaml`, checker, Evidence citation aggregate | `discovery.yaml report/status`, Page state/Aims, final handoff pointers | none | successful close or truthful inconclusive, blocked, or returned receipt | checker passes; material unresolved work is held visibly; Page and Task states agree; any epistemic outcome has verified promoted citations | `CLOSE`, `d1.acquire`, `d1.synthesize`, `HOLD` | Evidence `verified` on promoted citations for `ok` or `inconclusive` |

`N_admitted` is planned evidence-population cardinality, never an actual count.
Actual inventory comes only from allocated Run Tickets and runtime receipts.
`CLOSE` and `HOLD` are named terminal routes: `CLOSE` publishes a reconciled
receipt; `HOLD` preserves a visible blocker without claiming completion.

Terminal classification is not discretionary:

- **`ok`** — the promised article is established, every load-bearing Aim is
  met, no material Run remains unresolved, and every promoted citation is
  person-verified. Non-load-bearing limitations may remain recorded as such.
- **`blocked`** — an operational or gate dependency is missing, including
  unresolved intake, retrieval/Bib failure, or citation-verification debt on
  an otherwise epistemic (`ok`/`inconclusive`) close path.
- **`inconclusive`** — the admitted evidence completed successfully but cannot
  establish the substantive answer; its promoted citations are verified. It
  is never a label for missing work.

## L3/L4 promotion law

```text
ACQUIRE commissions one-Subject L4 Runs
        ↓
Run writes its paired Result only
        ↓
SYNTHESIZE validates and promotes completed Results
        ↓
authoritative L3 Page/typed record/Evidence citation projection changes
```

A Run never directly writes the Topic argument. Search queries, API calls,
redirect resolution, worker turns, synthesis passes, Bib assembly, and
checker calls are operations or Cycles, not additional Runs.

## Page-workflow boundary

Discovery may reuse the shared Page frame, Outline craft, and checking teeth.
Inside a Discovery Task Folder, however, `runs/` is reserved for Discovery
Paper/Source analysis. Generic Page Division-Writing or Evidence-Item Runs do
not enter that Folder's Run inventory. D1 SYNTHESIZE owns the root Page
promotion and D1 CLOSE owns cross-face closure.

## Routing

- Resolve `folder-kind: discovery` to
  `workflow-phases/haipipe-discovery-inquiry/SKILL.md`.
- Route user verbs and maintenance commands to `haipipe-discovery`.
- Route one-Subject identity and pairing to `haipipe-run` plus
  `haipipe-discovery/ref/paper-run-contract.md`.
- Route citation/Bib storage, verification, and aggregate presentation to
  `haipipe-plugin-evidence`; there is no separate Bibex plugin.
- Route Search to ACQUIRE craft; route Review/Idea to SYNTHESIZE craft. A
  synthesis specialist may route back to ACQUIRE when evidence is missing.

## Human Actions

| Action | When | Why | If not completed |
|---|---|---|---|
| Verify each promoted citation in the Evidence surface | before CLOSE may publish `status: ok` or `status: inconclusive` | `verified` is an artifact-local person judgment, not something the deterministic Bib builder can assert | publish `blocked` for verification debt or remain on `HOLD`; never claim an epistemic outcome from unverified citations |

This conditional Evidence gate is not a standing approval between D1 cycles.
A material ambiguity in SCOPE still returns to the requester before the scope
is frozen. Downstream consumers decide whether to act on a Discovery result
under their own workflow.

## Stop rules

- Stop ACQUIRE before Run allocation when no canonical Subject is admitted.
- Stop before terminal close when a material Run is unresolved or a
  load-bearing Page claim lacks a completed Result.
- Never infer a historical Run from a source list, note, typed record, or PDF.
- Never route a Discovery Page through `page-type: task`; Task Face and Page
  compatibility grammar are separate axes.

## Files

- `haipipe-discovery/SKILL.md` — user door, cycle verbs, and maintenance.
- `workflow-phases/haipipe-discovery-inquiry/SKILL.md` — D1 Folder contract.
- `haipipe-discovery/ref/lifecycle-map.md` — hierarchy × workflow × type.
- `haipipe-discovery/ref/paper-run-contract.md` — L4 specialization.
- `../board/haipipe-folder/SKILL.md` — neutral two-Face ownership law.
