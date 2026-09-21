# task

`task/` owns executable Task Folders and their Plan → Build → Execute → Report lifecycle.
The hierarchy is `tasks/bNN_<block>/jNN_<job>/tNN_<task>` with native `rNN` Runs.
A Workflow is a list of Runs: `run_specs` defines them, routes form the execution graph,
and reports bind actual Run Instances to definitions and durable receipts.
Internal Steps, review gates, and the four lifecycle commands do not allocate Runs.

Insight and Design are independent families under `skills/insight/` and `skills/design/`.
The Task Insight route is a compatibility handoff to the Insight owner.
Consumers can bind exact Task Results or settled Insight findings as their contracts allow.

## Mental Model

Every task has the same four-stage lifecycle:

```text
Plan -> Build -> Execute -> Report
```

Chinese mnemonic:

```text
规 -> 建 -> 行 -> 报
```

| Stage | Chinese | Meaning |
| --- | --- | --- |
| Plan | 规 / 规划 | Define bounded Run Specs, dependencies, gates, routes, and Result receipts. |
| Build | 建 / 构建 | Prepare the runnable object: configs, scripts, refs, runners, and environment. |
| Execute | 行 / 执行 | Run the task or record the run without changing the task definition. |
| Report | 报 / 报告 | Make the result inspectable: metrics, artifacts, run status, caveats, and next steps. |

## Task Domains

Task domains are the numbered, append-only type family under `task/`. Each
domain uses the same `规建行报` lifecycle, but owns a different IPO contract.

Chinese mnemonic:

```text
数 算 端 体 训 评 图 统 代 页
```

| Folder | Domain | Chinese | Scope |
| --- | --- | --- | --- |
| `1_data` | Data | 数 / 数据 | Build data assets: raw extraction/source/record/case/AIData. |
| `2_nn` | Algo / NN | 算 / 算法 | Design and smoke-test algorithms. |
| `3_end` | Endpoint | 端 / 端点 | Package, deploy, trigger, and postprocess endpoints. |
| `4_individual` | Individual | 体 / 个体 | Subject-level or patient-level inference, views, and reports. |
| `5_fit` | Fit | 训 / 训练 | Real model training, sweeps, and checkpoints. |
| `6_eval` | Eval | 评 / 评估 | Metrics, diagnostics, and statistical analysis. |
| `7_display` | Display | 图 / 图表 | Prepare display source data and provenance; final visual artifacts belong to the Display family. |
| `8_stata` | Stata | 统 / 统计 | Stata-engine work, including CMS/case/data/reg stages. |
| `9_agent` | Agent | 代 / 代理 | LLM-agent compute that produces task evidence. |
| `10_page` | Page service | 页 / 页面 | Produce reusable values and Supporting Run Results for a Page. |

The number is a permanent domain id, not a full pipeline order. New domains are
appended and existing ids are not renumbered.

## Page contracts

```text
task/haipipe-task/ref/
└── task-page.md                 one Task Folder and a run-bound human reading

task/haipipe-page-task/
└── SKILL.md                     display-rich reader contract for Task Pages

task/page-types/
└── haipipe-page-insight/       topic/data instance with item Runs and DIKW Results
```

The preferred public Insight entry is `/haipipe-insight task`; the older
`/haipipe-task insight` form remains a compatibility alias.

`haipipe-task` remains the canonical owner of Task Folder identity, execution,
results, and closure. `haipipe-page-task` extends the same-stem reader Page
with the required evidence-display inventory: substantive tables, figures, and
method/provenance diagrams. An Insight Page may read several Task Pages, Task
Run Results, Discovery Pages, or prior Insight Pages. It remains
consumer-neutral. Each item owns a question, local ticket, execution versions,
and DIKW/RF Result; its workflow and generated item table live with the skill.
Shared Task recipes accept instance-specific frozen inputs and output scopes.
Downstream consumers bind exact Run/Result evidence and own its contextual use.
Task does not write consumer stakes or claim that their Page content is accepted.

## Boundary (self-contained by design)

Tasks execute internal work: a task ends at Report, having produced `results/`, and stops. Whoever consumes a task's results records the link on THEIR side; this layer keeps consumer claims out of execution inputs and delegates interpretation to the owning family.

Self-contained does not mean opaque. Questions resolve through the normal
Run/Result contract: reuse an existing full Run id when it answers the scope;
otherwise open the shallowest new Run, execute it, and publish its paired Result.
A consumer records Supporting Run ids and, when a focal item is needed, its own
Local Run/Result. There is no separate question command, ticket, or answer bank.

That door is a SIDE door. The task session's primary mode is autonomous Plan → Build → Execute → Report with no question pending at all.

For the human reader, the wider mental model:

```text
⚙️ the executors — they run; the bank grows here, mostly with nobody asking
task       = execute internal work (code, runs, metrics)
discovery  = inspect outside evidence (literature, prior art)

📄 the knowledge wall — Task/Insights Board interprets, without consumer stake
insight    = D → I → K → W → RF, settled once and reused as evidence

📦 consumers bind evidence and own contextual decisions
paper      = academic expression and release
design     = commissioned design work and verification
```
