---
name: haipipe-insight-review
description: "Review/apply coordinator for the insight archive. Scans completed task/probe/discover/narrative/application material, decides which D/I/K/W cards are worth archiving, emits a reviewable INSIGHT_REVIEW.yaml, or applies that review through the layer writers. User-facing commands are review and apply. Trigger: review folder, collect insights, archive cards, construct insights, file curated memory."
argument-hint: "[review|apply|<scope-path>] [--project <path>] [--out <path>] [--auto]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.1.0"
  last_updated: "2026-06-20"
  summary: "Review/apply contract for constructing insights/."
  changelog:
    - "1.1.0 (2026-06-20): renamed user-facing flow to review/apply."
    - "1.0.0 (2026-06-20): initial review/apply contract."
---

Skill: haipipe-insight-review
================================

Construct `insights/` through an explicit review/apply contract.

This skill is the missing middle layer between finished evidence and card
writers:

```
task / probe / discover material
        ↓
review checklist / INSIGHT_REVIEW.yaml  ← this skill
        ↓
haipipe-insight-{data,information,knowledge,wisdom}
        ↓
review + index + audit
```

It does not compute, judge, or create research claims. It decides whether
already-finished material is worth archiving and routes the card filing.

Vocabulary:

```
review <scope>  = inspect a folder and write a human-readable INSIGHT_REVIEW.yaml
apply <INSIGHT_REVIEW.yaml> = turn accepted review items into D/I/K/W cards
```


Canonical References
--------------------

Read before acting:

```
ref/review-contract.md        review/apply semantics + INSIGHT_REVIEW.yaml schema
ref/insight-md-schema.md       card schema
ref/card-granularity.md        card size, merge/split, and flat-folder rules
ref/card-lifecycle.md          file/merge/update/supersede/change-log rules
ref/dikw-boundaries.md         D/I/K/W boundaries
ref/index-templates.md         derived index shape
```


Commands
--------

```bash
# Review only: inspect a scope and emit INSIGHT_REVIEW.yaml
/haipipe-insight review <project|narrative|ask-session|probe|task>

# Apply an existing review checklist
/haipipe-insight apply <INSIGHT_REVIEW.yaml>

# Convenience: review then apply when --auto is present
/haipipe-insight review <scope> --auto
```

Scope examples:

```bash
/haipipe-insight review examples/ProjA
/haipipe-insight review examples/ProjA/applications/ask/03_film_ood
/haipipe-insight review examples/ProjA/probes/0619_film_ood
/haipipe-insight review examples/ProjA/tasks/A01_eval/02_ood_split
```


Workflow
--------

Step 1: Resolve project root and scope kind.

```
scope path contains /applications/ask/  → application_ask
scope path contains /probes/            → probe
scope path contains /tasks/             → task
scope path is project root              → project
```

Step 2: Load current KB.

- Read `insights/INDEX.md` if present.
- Read K/W sub-indexes if present.
- Build a lightweight map of existing IDs, tags, sources, and statuses.
- Do not read every card body unless deduplication needs it.

Step 3: Scan scope material.

For task scope:
- Look for `results/<run>/metrics.json`, `workflow/report*.yaml`, `RUN_AUDIT.md`.
- Candidate D if a result is not represented in `sources:`.
- Candidate I if the task report explicitly states a cross-result pattern.

For probe scope:
- Read `probe.yaml`, `CLAIMS_FROM_RESULTS.md`, `INTEGRITY_AUDIT.md`, `review.md`.
- Candidate K only if the probe is judged / confirmed / refuted.
- Candidate W only if the claim or caveats imply a concrete next step.

For narrative scope:
- Read `claims.md`, `story.md`, `ignite-log.md`.
- Candidate K/W from GAP/weak claim slots that now have probe/lit support.
- Update narrative refs only after cards are filed.

For application ask scope:
- Read `plans/plan-v*.yaml`, SESSION_STATE, and `report.md` if present.
- Use `insight_yield` as the candidate card contract.

For project scope:
- Run the above scans shallowly over tasks, probes, narratives, and ask sessions.
- Prefer producing a plan over applying automatically.

Step 4: Deduplicate.

- If an existing card has the same source and same layer, skip or update.
- If material supports an existing card's same reusable unit, use
  `action: merge` instead of filing a duplicate.
- If a candidate contains multiple reusable units, use `action: blocked` with
  `granularity.decision: split` and list the split candidates needed.
- If material is a raw row, isolated seed, transient bug, or non-reusable note,
  use `action: skip`.
- If a new K contradicts an existing K, use `action: supersede`.
- If material is incomplete, use `action: blocked`.
- Never create a card just because a file exists; require an archive reason.
Apply `ref/card-granularity.md` before layer assignment is finalized.
Apply `ref/card-lifecycle.md` before choosing `file` over `merge`, `update`,
or `supersede`.

Step 5: Emit review checklist / INSIGHT_REVIEW.yaml.

Default output:

```text
<scope>/INSIGHT_REVIEW.yaml
```

For project-level manual runs:

```text
insights/INSIGHT_REVIEW.yaml
```

Step 6: Apply review items only when explicitly requested or `--auto` is present.

For each `candidate_cards[]` item:

```
action file:
  layer D → Skill("haipipe-insight-data", ...)
  layer I → Skill("haipipe-insight-information", ...)
  layer K → Skill("haipipe-insight-knowledge", ...)
  layer W → Skill("haipipe-insight-wisdom", ...)

action merge/update:
  edit target card in place:
    - update `updated`
    - add sources/ref_by/merged_from as needed
    - add evidence/caveat/confidence/status changes
    - append `## Change log`

action supersede:
  create replacement card when needed
  mark target card `status: superseded`
  set `superseded_by`
  append `## Change log` to old and replacement cards
```

Then:

- call the matching card reviewer
- rebuild relevant INDEX files
- call `index-integrity-auditor-agent`
- return filed card ids and any blocked items


Definition of Done
------------------

- [ ] `INSIGHT_REVIEW.yaml` emitted or applied.
- [ ] Every candidate has `file`, `update`, `supersede`, `skip`, or `blocked`.
- [ ] Every `file` action has a reason and source refs.
- [ ] Every `merge`, `update`, or `supersede` action has a target and `change`
      block.
- [ ] Every candidate has a `granularity` block explaining file / merge /
      split / skip / blocked.
- [ ] Duplicate or reinforcing evidence uses `merge`, not a new card.
- [ ] Over-broad candidates are split before apply.
- [ ] Meaningful card edits append `## Change log`.
- [ ] Superseded cards are linked, not deleted.
- [ ] Applied cards conform to `ref/insight-md-schema.md`.
- [ ] Per-card reviewers passed or produced explicit failure artifacts.
- [ ] INDEX files rebuilt.
- [ ] `index-integrity-auditor-agent` run after apply.
- [ ] Caller artifact can cite the new card ids.


Risk Profile
------------

Review mode writes only `INSIGHT_REVIEW.yaml`.

Apply mode may write:

```text
insights/D_data/*.md
insights/I_information/*.md
insights/K_knowledge/*.md
insights/W_wisdom/*.md
insights/INDEX.md
insights/views/*.md
insights/K_knowledge/INDEX.md
insights/W_wisdom/INDEX.md
insights/INDEX_AUDIT.md
```

It never writes code, task results, probe verdicts, or narrative conclusions.


Specialist Tail
---------------

```text
status:    ok | blocked | failed
summary:   "<N candidates · M filed · K skipped · B blocked>"
artifacts: [INSIGHT_REVIEW.yaml, insights/INDEX.md, insights/INDEX_AUDIT.md]
cards:     [D03, I02, K04, W02]
blocked:   [candidate_id:reason]
next:      "Update narrative claims.md / application report refs with filed card ids"
```
