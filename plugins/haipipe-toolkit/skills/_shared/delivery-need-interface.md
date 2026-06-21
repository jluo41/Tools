# Delivery Need Interface

This reference defines the shared contract between delivery lifecycles
(`paper/`, `application/`) and evidence workers (`probe/`, `discover/`,
`task/`, `insight/`).

The operating model is evidence-centered:

```text
delivery lifecycle owns story/message/claims
delivery lifecycle discovers a gap
delivery lifecycle records a need
evidence worker answers the need
delivery lifecycle backfills the answer
```

Do not create a project-level narrative layer to mediate this flow. Story is
delivery-specific. Evidence is project-level and reusable.

## Need Record

Use this shape in TeX comments, markdown tables, YAML blocks, or status files.
Keep the fields recognizable even if the surrounding file format differs.

```yaml
need_id: N-<SOURCE>-<CLAIM>-<NNN>
source:
  kind: paper|application
  path: <delivery-root-relative-path>
  stage: <lifecycle-stage>
claim_id: <claim-or-message-slot>
need_type: probe|display|discovery|task|insight
question: <specific question that would close the gap>
expected_artifact: <verdict|display|table|source review|run result|insight card>
status: open|running|resolved|blocked|dropped
owner: <skill-or-human>
linked_artifacts:
  - <project-relative-path>
backfill_targets:
  - <delivery-root-relative-path>
```

## Minimal TeX Form

For paper lifecycle TeX files, prefer short comments near the claim or display:

```tex
% NEED N-PAPER-C3-001
% source: 0-lifecycle/2-claims/2-claims.tex
% claim_id: C3
% need_type: probe
% question: Is there a robust threshold effect in opioid prescribing?
% expected_artifact: verdict + dose-response display
% status: open
% linked_artifacts:
% backfill_targets: 0-lifecycle/2-claims/2-claims.tex; 0-lifecycle/4-figures-tables/4-figures-tables.tex; 0-lifecycle/5-minimap/5-minimap.tex
```

## Status Semantics

- `open`: the delivery artifact has named a missing evidence need.
- `running`: a probe/discovery/task/insight worker has accepted it.
- `resolved`: linked artifacts exist and the delivery file has been backfilled.
- `blocked`: the evidence worker cannot answer without human/data/action.
- `dropped`: the delivery owner intentionally removed the claim or display need.

## Worker Responsibilities

Paper/application:

- Own the story, audience, claim wording, section placement, and display use.
- Record open needs when a claim, paragraph, message, figure, or table lacks
  support.
- Call evidence workers directly from open needs.
- Backfill resolved evidence into the lifecycle stage that raised the need.

Probe/discover/task/insight:

- Treat a delivery need as input context, not ownership transfer.
- Write project-level evidence artifacts under their own folders.
- Return a verdict, artifact path, caveat, and backfill target.
- Never rewrite the delivery story unless explicitly asked after returning the
  evidence.

## Routing Hints

```text
need_type: probe      -> /haipipe-probe open <need-id-or-source>
need_type: discovery  -> /haipipe-discover <question>
need_type: task       -> /haipipe-task <task-contract>
need_type: display    -> /haipipe-task-for-display or paper display stage
need_type: insight    -> /haipipe-insight <closed-probe-or-evidence>
```

## Dashboard Rule

Any `enter` or `status` command for a delivery lifecycle must surface open
needs before suggesting next work. The user usually does not know whether the
next step is paper writing, probe, discovery, task, or insight until the open
needs are visible.
