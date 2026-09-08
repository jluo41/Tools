# RETIRED 2026-09-08 · TaskSkillBoard-260726

This historical design board is no longer a runtime contract. The former
question/QA and Probe records, their generated pages, and their collector
links have been removed. The live Task authority is now:

- `skills/task/haipipe-task/SKILL.md`
- `skills/run/haipipe-run/SKILL.md`
- `skills/board/page-plugins/haipipe-plugin-runs/SKILL.md`

Questions use the shared evidence loop:

```text
Supporting Run(s) → consumer Local Run → immutable Result
```

Nothing in this historical directory is read by the Task router. Recovery of
the retired design is through git history; new work must not recreate its
question folders, answer files, or collector route.

## Retained non-QA records

The following records remain because they document the concepts that survived
the migration. They are prose provenance only, not executable instructions:

```text
QB · Task Folder lifecycle
     Plan → Build → Execute → Report

QC · Run identity
     one Run address paired with one generated Result

QE · Fresh-context acceptance
     a new agent discovers the shipped Task and Run contracts
```

The old QD material (what used to leave the bank) is deleted. Its replacement
is the consumer-owned Supporting/Local evidence row in the Page Outline and
Evidence Workspaces.

## Current model

```text
Block (bNN) → Job (jNN) → Task Page (tNN) → Run (rNN) → Result

Task       Plan → Build → Execute → Report
Discovery  Scope → Acquire → Synthesize → Close
```

Scripts are optional engines selected by a Run ticket. They are not a second
evidence bank, and a Result is never replaced by a digest or answer file.

## Links

```text
Task contract       ../../task/haipipe-task/SKILL.md
Run contract        ../../run/haipipe-run/SKILL.md
Task hierarchy      ../../task/haipipe-task/ref/hierarchy.md
Task structure      ../../task/haipipe-task/ref/task-structure.md
Task agents         ../../task/agents/
Runs presenter      ../../board/page-plugins/haipipe-plugin-runs/SKILL.md
Page evidence       ../../board/page-workflows/haipipe-page-evidence/SKILL.md
```
