---
name: haipipe-narrative
description: "Compatibility redirect for the retired project-level narrative workflow. Use when a user invokes `/haipipe-narrative`, asks for project-level story/angle/ignite/handoff, or references the old narrative/probe/discovery/task stack. Story now belongs to the active delivery lifecycle: paper owns paper-specific seed/pitch/claims/narrative/displays/minimap, and application owns audience/message/report/UI lifecycle. Shared reusable evidence lives in probes/discoveries/tasks/insights. This skill should route users to `/haipipe-paper enter <paper-path>`, `/haipipe-application ...`, `/haipipe-probe`, or `/haipipe-insight` rather than creating/updating `narratives/`."
argument-hint: "[status|enter|open|post|handoff|args...]"
allowed-tools: Bash, Read, Grep, Glob, Skill
metadata:
  version: "3.0.0"
  last_updated: "2026-06-21"
  summary: "Retired narrative layer compatibility redirect."
  changelog:
    - "3.0.0 (2026-06-21): retired project-level narrative ownership; redirect story work to paper/application lifecycle and evidence work to probe/discover/task/insight."
    - "2.3.0 (2026-06-20): narrative becomes a session control envelope; Insight is reusable synthesis after Probe-post; paper/application are downstream delivery layers."
---

# haipipe-narrative

This is a compatibility skill. The project-level narrative layer is retired.

Do not create or update `narratives/<NN>_<slug>/story.md`, `claims.md`,
`ignite-log.md`, or `decision-tree.md` as the source of truth for paper or
application work.

Legacy files in this skill folder, including `MENTAL_MODEL.md`, `DESIGN.md`,
and `haipipe-narrative/ref/narrative-schema.md`, document the old project-level
narrative model. Do not read or apply them for normal redirect/status work.
Read them only if the user explicitly asks to migrate or audit an old
`narratives/` folder.

## Current Model

```text
delivery lifecycle owns story/message/claims
delivery lifecycle records open needs
evidence workers answer open needs
delivery lifecycle backfills the answer
```

Delivery-side owners:

```text
paper/<PaperName>/0-lifecycle/
  0-seed -> 1-pitch -> 2-claims -> 3-narrative
  -> 4-figures-tables -> 5-minimap

applications/<AppName>/ or application sessions
  intent/audience -> claims/message/report/ui -> delivery artifact
```

Evidence-side shared assets:

```text
probes/        claim-level verdicts
discoveries/   outside evidence
tasks/         executable work/results
insights/      reusable meaning/caveats/K/W cards
```

Shared interface:

```text
../../_shared/delivery-need-interface.md
```

## Routing

When invoked, identify what the user actually needs:

| User intent | Route |
|---|---|
| enter/status/dashboard for a paper | `/haipipe-paper enter <paper-path>` |
| paper story, angle, claims, sections, figures, minimap | paper lifecycle stage |
| application message/report/UI story | `/haipipe-application <kind> ...` |
| claim needs testing | `/haipipe-probe open <need-or-question>` |
| outside literature/context is missing | `/haipipe-discover <question>` |
| run/output/display needs materialization | `/haipipe-task ...` or display task |
| reusable meaning/caveat after evidence exists | `/haipipe-insight <artifact>` |

If the current directory is inside a paper root, prefer:

```text
Skill("haipipe-paper-enter", args="<detected-paper-root>")
```

If the request names an application output, prefer:

```text
Skill("haipipe-application", args="<original intent>")
```

If the request is only "what story do we have?", answer by explaining that the
story is delivery-specific and ask for the target delivery artifact, unless a
paper/application root is detectable.

## Response Pattern

Start with a concise redirect:

```markdown
## 🔁 Redirect

Project-level narrative is retired. I am routing this to the active delivery
lifecycle because story/claims now live there.
```

Then dispatch or recommend one concrete command.

## Hard Rules

- Do not treat `narratives/` as the source of truth for new work.
- Do not maintain a shared story ledger for multiple papers.
- Do not route paper claim gaps through narrative.
- Do not call this a deletion of narrative as a concept: narrative survives as
  `paper/0-lifecycle/3-narrative` or the application message/report story.
- Do keep project-level evidence reusable through probes, discoveries, tasks,
  and insights.

## Return Contract

```text
status: redirected|blocked
target: paper|application|probe|discover|task|insight|unknown
next: <single recommended command>
```
