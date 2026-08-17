---
name: haipipe-page-for-insight
description: >-
  The Page Type contract for one reusable DIKW insight on a Task/Insights Board. It turns traceable Task or Discovery evidence into a consumer-neutral chain from Data to Information to Knowledge and, when justified, Wisdom. Use when results exist but their reusable meaning is missing, when several task outputs must be synthesized around one question, when Paper or Application needs a settled Insight Page through PageX, or when an existing insight must be refreshed after a source rerun. Trigger: insight page, DIKW, Task Board insight, data meaning, result synthesis, knowledge page, wisdom page, page-type insight, /haipipe-page-for-insight.
metadata:
  version: "0.1.0"
  last_updated: "2026-08-17"
  summary: "One consumer-neutral Page traces a question through D→I→K→W; Probe reaches Task/Discovery evidence here, while Paper and Application consume the settled Page through PageX."
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "question → sources → Data → Information → Knowledge → Wisdom → handoff"
---

# /haipipe-page-for-insight · turn executed work into reusable knowledge

Load `haipipe-page` first. Load `haipipe-plugin-probe` when inspecting Task or Discovery sources, and `haipipe-plugin-pagex` when reusing another settled Page.

This type covers one insight question or topic. Declare `page-type: insight` and a required target:

```yaml
page-type: insight
insight-target: data | information | knowledge | wisdom
```

The target says how far this Page promises to reason. It does not permit skipping the trace below it.

## Boundary

```text
Task Page       one Task Folder, its runs, and the human reading of one run
Insight Page    one reusable DIKW chain, possibly across several Task Pages
Paper           selects settled K and expresses it as an academic argument
Application     selects settled K/W and expresses it as an intervention
```

An Insight Page is consumer-neutral. Never write “the paper needs”, “the message should”, or another downstream stake into its evidence or conclusion. Consumers add their own interpretation after PageX.

## Fixed Content outline

Use these divisions in order:

```text
### 1 · Question and Scope
### 2 · Source Map
### 3 · Data
### 4 · Information
### 5 · Knowledge
### 6 · Wisdom
### 7 · Reusable Handoff
```

- **Question and Scope** states one answerable question, population/unit, time window, and explicit exclusions.
- **Source Map** names Task Pages, Task `QA/` answers, Discovery Pages, or other Insight Pages. It never points a consumer straight into `results/`.
- **Data** records dated observations with run or source anchors. No interpretation.
- **Information** states patterns derived from named Data rows, including null and contradictory patterns.
- **Knowledge** states supported propositions, their strength, rival explanations, and boundary conditions.
- **Wisdom** states actionable implications only when the evidence warrants them. A lower target writes `not targeted` rather than manufacturing advice.
- **Reusable Handoff** is a compact, consumer-neutral packet: finding, strength, boundary, source Pages, last refresh, and what remains unknown.

## DIKW trace law

Every upward statement names what supports it:

```text
D<n> observation ─▶ I<n> pattern ─▶ K<n> proposition ─▶ W<n> implication
```

No level may cite a later level as its evidence. A W row may be useful and still fail if it has no K parent. Preserve negative and null results; they may produce valid K or W rows.

## Probe and PageX

This is the primary Page Type allowed to turn raw project evidence into reusable knowledge.

```text
Task / Discovery folder ── Probe ──▶ Insight Page
settled Insight Page ───── PageX ──▶ another Insight, Paper, or Application
```

- Use Probe to inspect Task/Discovery sources and land evidence on this Page.
- Use PageX to reuse a settled Page without reopening its source investigation.
- Never copy a Task `results/` tree into the Board.
- When a source reruns, mark dependent rows stale and reopen the Page before a consumer treats them as settled.

## Runtime shape

```text
<InsightPage>/
├── <InsightPage>.md
├── probe/       Task/Discovery evidence cards and bindings
├── pagex/       references to other settled Pages
└── display/     optional evidence visualizations
```

The Page owns the interpretation, not source code or results. `display/` shows evidence; it does not become another evidence authority.

## Closing checks

- The promised `insight-target` is reached or explicitly rejected with a reason.
- Every D row has a resolvable, dated source.
- Every I/K/W row traces to the immediately preceding level.
- Contradictions, nulls, and scope limits remain visible.
- The handoff contains no Paper/Application-specific framing.
- Source reruns have not left a settled but stale reading.
- A downstream Page can consume Division 7 through PageX without opening the Task Folder.

This variant owns no scripts.
