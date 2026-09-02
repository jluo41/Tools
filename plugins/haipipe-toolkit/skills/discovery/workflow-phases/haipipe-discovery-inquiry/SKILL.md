---
name: haipipe-discovery-inquiry
description: >-
  D1 Folder contract for one Discovery inquiry. It owns folder-kind discovery,
  the four-role article Page Face, the Paper/Source Run Task Face, selected
  plugins, five workflow cycles, cross-face closure, and evidence handoff. Use when resolving,
  scaffolding, checking, or closing one BJTR Discovery Task Page Folder.
metadata:
  version: "0.2.0"
  last_updated: "2026-09-02"
  workflow: haipipe-discovery-workflow
  phase: D1
  folder_kind: discovery
  primary_face: page
  page_ruling: none
  outline:
    mode: grammar
    source: "this SKILL.md"
    shape: "four ordered role headings: Question and boundary, Type payload, Evidence map, Limits and next move; each adds a subject-specific title and owns the same-name Aim group"
---

# /haipipe-discovery-inquiry · D1 owns one evidence question

## Position

D1 is the sole Folder Phase of `haipipe-discovery-workflow`. Its internal
SCOPE → PREPARE? → ACQUIRE ↔ SYNTHESIZE → CLOSE cycles grow one stable
Level-3 Task Page; each admitted canonical paper or source is one Level-4
Run. The five names are Cycles, not additional Phases.

## Folder Kind

`folder-kind: discovery` resolves here. The Folder lives at
`discoveries/bNN_<block>/jNN_<job>/tNN_<task>/`, with readable address
`bNN.jNN.tNN`. It has both faces; “Task” names its work altitude and does not
select the empirical `page-type: task` compatibility grammar.

## Input

- One bounded external-world question.
- A canonical `discovery_type` and source/admission boundary.
- Zero or more preserved records or candidate sources.
- For each ACQUIRE Run, one resolved canonical Subject and its Trigger.

## Page Face

The root same-stem Page writes `folder-kind: discovery` and follows the shared
Opening → optional Diagram → Content → Aims frame. Content has four ordered
roles; the words before the second ` · ` are fixed and the rest is specific to
the inquiry:

```text
1 · Question and boundary · <the exact inquiry and evidence population>
2 · Type payload · <the source map, reading, summary, verdict, landscape, or ideas>
3 · Evidence map · <the claims, Result Cards, cite keys, disagreements, and gaps>
4 · Limits and next move · <what is not established and the next lawful route>
```

Each division opens with a captioned face diagram. A1–A4 repeat the complete
same-name division title after their emoji. Migration may leave Type payload
active and historical evidence mapping explicitly held; it may not claim that
linked legacy files already satisfy Result-backed synthesis.

## Task Face

`discovery.yaml` owns intent, lifecycle status, and the closing report. SCOPE
bounds the question; PREPARE optionally creates a reusable instrument;
ACQUIRE admits and analyzes canonical Subjects; SYNTHESIZE promotes completed
Results into the root Page, optional typed record, and derived Evidence Bib;
CLOSE checks and reconciles both Faces.

### Run Profile

- **ALLOWED**: `paper-analysis`, `source-analysis`.
- **TARGET**: one canonical paper, dataset, report, webpage, media item, or
  other source Subject.
- **TICKET**: executable `runs/rNN_<author-or-source><year>_<slug>.sh`.
- **INPUTS**: Trigger provenance, resolved Subject identity, question, and
  admission rationale.
- **WORKER**: the selected research/source-analysis skill.
- **RESULT**: same-stem Result Card, `facts.md`, `runtime.yaml`, optional PDF,
  and one authoritative one-entry Bib.
- **ACCEPT**: identity, pairing, provenance, facts, cite key, and status pass
  `paper_runs.py check`.
- **PROMOTION**: completed Results may be synthesized many-to-many into the
  Page and derived Evidence Bib.
- **REOPEN**: a changed Result, material unresolved Run, or expanded evidence
  population reopens the affected Page Aims.

## Plugins

- **required**: Folder/Page surface and the one Evidence plugin; Evidence owns
  citation/Bib storage, verification, and the derived Discovery aggregate.
- **conditional**: Runs presenter when the first Run is admitted; PageX for
  cross-Folder consumers; Outline for Page planning.
- **forbidden**: a separate Bibex or reading plugin, empty Runs/Results lanes,
  or a Task Page compatibility grammar layered over the Discovery Page Face.

## Gate and Closure

The Folder closes only when `paper_runs.py check` passes, every material
admitted Run is resolved or explicitly held, the Page answers its question at
the promised `discovery_type`, and Page state agrees with `discovery.yaml`.
`report:` supports `reported`; `ok` additionally requires the Result-backed
Evidence map, the Evidence citation aggregate, and all load-bearing Page Aims
to be met. Non-load-bearing limitations may remain recorded, but a held
load-bearing Aim forbids `ok`. Every promoted citation must also carry the
Evidence-local person judgment `verified` before CLOSE may claim an epistemic
`status: ok` or `status: inconclusive` outcome.
Missing operational work or that conditional artifact gate yields `blocked`;
`inconclusive` is reserved for completed admissible evidence that cannot
establish the substantive answer. Neither receipt may claim `ok`.

## Handoff

Consumers receive the root Page, exact Result/Card links, cite keys, derived
Evidence Bib, disagreements, and unresolved limits. A consumer never treats a
legacy source index as a Result receipt.

## Files

- `../../haipipe-discovery/SKILL.md` — executor and user verbs.
- `../../haipipe-discovery/ref/page-types.md` — type-specific payload promises.
- `../../haipipe-discovery/ref/paper-run-contract.md` — Level-4 artifacts.
- `../../haipipe-discovery/scripts/paper_runs.py` — deterministic gate.
- `../../haipipe-discovery-workflow/SKILL.md` — workflow map and routing.
- `../../../board/page-plugins/haipipe-plugin-evidence/SKILL.md` — citation
  authority and the one Evidence surface.
