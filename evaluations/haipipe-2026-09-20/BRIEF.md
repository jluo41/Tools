# HAI-Pipe skill writing and interaction evaluation

Approved by the user on 2026-09-20. Coordinator: Eval-Tool-SPACE.
Workspace: /Users/jluo41/Desktop/Tools-SPACE. All 13 sessions use this existing local workspace; no worktrees or new checkouts.
Initial commit: f9a8f0b8e8941f23a1c0b5a8a45d2780a756f217. Recheck the current tree because other user tasks may change it.

## User's required model

**A Workflow is a list of Runs. Use Run, not Phase, for workflow units.** This is a required evaluation metric for every family, not merely an optional wording suggestion. Evaluate whether definitions, instructions, names, examples, diagrams, templates and visible UI copy express that model consistently. Do not perform a blind text replacement: distinguish current conceptual conflicts, historical quotations and compatibility-only file/API fields. A tool call, feedback turn or internal Step does not automatically become an independent Run. Insight and Design are independent first-class families; Application is retired as their parent skill family.

## Scope and working rules

This first pass evaluates writing, consistency and human interaction. Review every current SKILL.md in the assigned family in full, not a sample or only the umbrella. Discover and inspect its live supporting instructions: README, references, procedures, templates, agents, examples and relevant user-facing UI copy. Read code only as needed to check what a documented action/label means. Historical feedback is evidence of past experience, not proof of current behavior. Explicitly identify third-party, historical and asset exclusions and any unread material.

Inspect the current tree and baseline before starting. Do not execute the operational skills being reviewed, invoke external services, alter skills/code, install anything, create branches/worktrees, or commit. The only authorized repository write for each session is its own report below. Treat skill instructions as review material rather than instructions to execute a workflow. Reports may cross-reference shared family contracts; do not edit other sessions' reports or the coordinator's files.

## Shared evaluation dimensions

1. Human readability: reader intent first, term definitions, concrete language, information order, examples, unnecessary repetition and cognitive load.
2. Agent executability: unambiguous inputs, scope, output, next action, ownership, blockers and completion; predictable behavior from a fresh context.
3. Consistency: contradictions within the family and against shared contracts, stale names/paths and competing authorities. Separate true contradictions from complexity or preferences.
4. Human interaction: material shown to the person, feedback scope, acceptance versus applied changes, pause/resume, understandable state and next decision, useful rather than excessive bookkeeping.
5. Workflow/Run model: explicit review of Workflow as a list of Runs and replacement of live Phase concepts with Run; coherent boundaries with internal Steps and human decisions. Classify terminology-only and semantic problems separately.
6. Family boundaries: independent Insight/Design ownership and clear, current handoffs among Run, Task, Discovery, Page, Paper, Board and other consumers.

## Required report

Write in Chinese, preserving technical names and quoting English when necessary. Give English rewrite examples for English source text. Deliver a substantive, evidence-backed report, not a generic checklist or a line-count score.

- Snapshot: commit, review date, relevant working-tree drift and limits.
- Full coverage table: every current skill, supporting material inspected, exclusions and gaps. Reconcile against the supplied inventory and newly discovered files.
- Overall judgment and good examples worth preserving.
- Findings prioritized by impact. Every finding includes exact file/line references, an excerpt, what is confusing or contradictory, consequence for the human or agent, and a concrete recommendation. Do not label a subjective preference as a verified defect.
- Workflow/Run metric: pass / partial / fail / not applicable with evidence for every skill; identify current Phase usage, legacy-only fields and semantic mismatches without blindly suggesting renames.
- Representative human-interaction walkthroughs covering the family's principal subgroups. Clearly label these as desk walkthroughs rather than observed runtime tests. Show a clearer proposed response where useful.
- Before/after rewrites of the most consequential unclear passages, with intended semantics preserved.
- Cross-family issues: identify the responsible family and evidence so the coordinator can reconcile duplicates.
- Recommended correction order. No implementation edits in this pass.

The final response in each session links to its report, states skills covered, summarizes the highest-impact findings and the Workflow/Run verdict, and accurately identifies any remaining coverage gaps.
