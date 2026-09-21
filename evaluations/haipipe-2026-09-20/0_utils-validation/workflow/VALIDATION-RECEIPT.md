# Fresh-context skill invocation receipt

Date: 2026-09-20. Agent: /root/validate_workflow. Artifact root: /tmp/validate-workflow-260920-3cbuakfo.

This invocation began from the three realistic requests and the shipped skills. Root AGENTS.md, README Skill development, and the package README were read. No evaluation reports, prior conversations, git diffs, network tools, or provider calls were used. Repository source files were not edited. A source hash snapshot is saved in source-snapshot.json. The scratch Task is synthetic; its tickets were copied from the owner template but no worker ticket was executed.

## Selection and requests

1. Selected workflow-table v0.4.5 for a current Design Workflow list, five-Space matrix, Run types, human decisions, routing, expected counts, and pass/invalid-review behavior. Loaded its schema/catalog/coverage references plus the current Design owner, workflow, Run Profile, unit worker contract summary, neutral Run, and Design state mapping.
2. Selected task-table v0.6.0 for the actual status tree. Used a native Task owner layout beneath "Project with spaces/tasks" with two task folders, each carrying a same-stem Page, config, ticket and runtime receipt. One receipt is planned, one failed. The utility generated every status and report from disk.
3. Selected diagram-ascii v0.5.0 for plain text with no emoji. Saved design-process.txt in the explicitly authorized scratch directory. Its Run boxes identify individual rdNN instances, while comments, model calls, self-checks and other internal steps remain inside their Run.

## Results and verdicts

- Workflow output: design-workflow.md and design-workflow.json. Three Run Specs, five Spaces, 15 explicit Cells (six empty); all routes resolve and all Cell coordinates are well formed. Four deduplicated literal skill coverage rows resolve paths, versions, and wc line counts. No Design runtime folder was supplied, so Runs Overview and Human Queue correctly remain unassessed; no live activity or person was invented.
- Current owner count: C + N + J; 1 + N + J only for the one-release/no-earlier-hold path. Ordinary first-pass success = 3; hold then release plus first-pass generation/review = 4. These are planned examples, not runtime inventory.
- Candidate pass: independent Verify plus clean records makes the exact candidate ready for Delivery, with no new approval or Run. Invalid/unresolved review: failed Verify receipt, route verify, person queues review again. Valid fail review: complete receipt, route generate, person queues revise. No automatic retry or agent-side Commission HOLD was inferred.
- Task output: Project with spaces/tasks/TASK-TABLE.md, task-status-tree.txt, task-status-summary.txt, task-runs.md, task-table.tsv. Native <task>/results/<run>/ receipts were read correctly. One task Not run 0/1 (Run Ready), one Failed 0/1 (Run Failed); counts are 1 Block, 1 Job, 2 Tasks, 2 configs, 2 tickets, 2 receipts. No S-results finding was emitted.
- Path portability: Python 3.9.6 and the renderer file resolved. Renderer was invoked by its absolute installed skill path independently of the target tree. Both subprocess argv and the documented quoted shell G invocation with TABLE_TASK_SKILL_DIR exported succeeded on a target directory containing spaces; quoted-shell-status.md preserves the latter output.
- Drift gate: mutated copy exits 1 (drift-negative.log); the same copy with --expect-fail exits 0 and still reports DRIFT (drift-proof.log); original generated report exits 0 and matches (drift-clean.log).
- Diagram: ASCII-only, no tabs or emoji; clearly labels Run identities and internal steps. Delivery remains a read-only projection. No image or network rendering was used.
- Behavioral verdict: requested artifacts and status rendering PASS. Source guidance alignment requires repairs noted below; the successful renderer behavior does not erase those documentation contradictions.

## Commands and evidence

commands.json records exact argument vectors, exit codes, and log paths for all eight renderer calls. artifact-checks.json records artifact consistency assertions. The additional literal shell invocation was:

```sh
TABLE_TASK_SKILL_DIR='/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/table-task'
export TABLE_TASK_SKILL_DIR
G="$TABLE_TASK_SKILL_DIR/ref/render_task_table.py"
python3 "$G" '/tmp/validate-workflow-260920-3cbuakfo/Project with spaces/tasks' --surface tree --depth task > '/tmp/validate-workflow-260920-3cbuakfo/quoted-shell-status.md'
```

## Friction observed while following the skills

1. Design count assumption: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/table-workflow/SKILL.md:156 gives 1 + N + J without the no-earlier-hold condition. Its ref/workflow-table-schema.md:181 fixes Commission cardinality at 1 and line 228 repeats that total. The domain Run Profile /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design-workflow/references/run-profile.md:11 also gives 1 Commission, and line 95 says "One Commission per item" immediately after permitting a new release decision following a hold. Current owner /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design-workflow/SKILL.md:46 instead explicitly counts C Commission records, including held records, and limits only releases to one. Following the compact utility example alone undercounts a hold then release path by one.
2. Task Result placement: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/table-task/SKILL.md:100 and :230 direct readers to <job>/results/<task>/<run>. Its ref/task-table-schema.md:128-129 calls that the nested law and says the current <task>/results/<run> form receives S-results; line 140 calls Task-local results a finding. Current Task owner /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task/haipipe-task/ref/hierarchy.md:187 and :236 expressly require Task-local results. The native-layout fixture proves the renderer accepts and projects that layout without a finding, so this is stale utility guidance rather than an observed renderer failure.
3. Minor status wording: /Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/table-task/SKILL.md:267-268 says an initial restructured tree says Ready on every Task row, although the same skill's status rollup calls all-ready Tasks Not run. The rendered planned Task correctly says Not run 0/1; Ready belongs to the Run row. A future reader could confuse task status with Run status.

The independent invocation did not patch any of these sources.


## Bounded correction recheck — 2026-09-20

Verdict: PASS. All three reported documentation frictions are resolved in the current shipped files. The initial observations above remain preserved as baseline history.

1. Commission cardinality now matches the owner. table-workflow/SKILL.md:148 and :156-161 explicitly give C decisions, at most one release per Item, C + N + J, preserved hold records, and C=1 only on the no-earlier-hold path. Its ref/workflow-table-schema.md:181 sets cardinality C; :228-231 defines the same count and special case. The domain Run Profile:11-14 and :93-99 now agree with haipipe-design-workflow/SKILL.md:46-49: a held decision is preserved and later release creates another Commission Run. The existing generated Workflow answer already used this owner-correct interpretation and needs no semantic change.
2. Task storage guidance now agrees with its owner and observed renderer behavior. table-task/SKILL.md:100 and :230 point to <task>/results/<run>/runtime.yaml. ref/task-table-schema.md:128-130 calls Job-level receipts legacy, flags that placement S-results, and prefers Task-local receipts when both exist; :141 describes the same finding. These statements align with Task hierarchy:187/:236. The prior native-layout fixture's actual generated report contains both Task-local receipts with no S-results finding; that evidence remains applicable to this documentation correction.
3. Task versus Run status is now explicit. table-task/SKILL.md:267-271 says unexecuted tickets yield Task Not run and Run Ready, matching the documented rollup and the previously generated planned fixture output (Task Not run 0/1, Run Ready).

Recheck evidence: recheck-source-excerpts.txt preserves the exact corrected lines, and recheck-source-snapshot.json records their hashes. Existing generated outputs and commands.json retain the behavioral evidence. No full rendering suite was repeated, because no mismatch remained that required new execution. Repository files remained read-only, and no network/provider calls were made.
