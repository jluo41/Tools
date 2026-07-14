# task

`task/` is the HAI-Pipe execution layer: a task is a runnable work unit with a
shared lifecycle and a type-specific IPO contract.

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
| Plan | 规 / 规划 | Define the objective, IPO contract, dependencies, risks, and validation gates. |
| Build | 建 / 构建 | Prepare the runnable object: configs, scripts, refs, runners, and environment. |
| Execute | 行 / 执行 | Run the task or record the run without changing the task definition. |
| Report | 报 / 报告 | Make the result inspectable: metrics, artifacts, run status, caveats, and next steps. |

## Task Domains

Task domains are the numbered, append-only type family under `task/`. Each
domain uses the same `规建行报` lifecycle, but owns a different IPO contract.

Chinese mnemonic:

```text
数 算 端 体 训 评 图 统 代
```

| Folder | Domain | Chinese | Scope |
| --- | --- | --- | --- |
| `1_data` | Data | 数 / 数据 | Build data assets: raw extraction/source/record/case/AIData. |
| `2_nn` | Algo / NN | 算 / 算法 | Design and smoke-test algorithms. |
| `3_end` | Endpoint | 端 / 端点 | Package, deploy, trigger, and postprocess endpoints. |
| `4_individual` | Individual | 体 / 个体 | Subject-level or patient-level inference, views, and reports. |
| `5_fit` | Fit | 训 / 训练 | Real model training, sweeps, and checkpoints. |
| `6_eval` | Eval | 评 / 评估 | Metrics, diagnostics, and statistical analysis. |
| `7_display` | Display | 图 / 图表 | Publication figures, tables, and source data. |
| `8_stata` | Stata | 统 / 统计 | Stata-engine work, including CMS/case/data/reg stages. |
| `9_agent` | Agent | 代 / 代理 | LLM-agent compute that produces task evidence. |

The number is a permanent domain id, not a full pipeline order. New domains are
appended and existing ids are not renumbered.

## Boundary (self-contained by design)

Tasks execute internal work: a task ends at Report, having produced `results/`, and stops. Whoever consumes a task's results records the link on THEIR side; this layer tracks no consumers, names none, and its working docs (SKILL/ref/fn) never route upward.

Self-contained is not deaf, though. Questions arrive through exactly ONE door — `/haipipe-task qa "<question>" [<leaf>]` (`haipipe-task/fn/qa.md`) — as one question in general language, with no id, no reference to whoever asked, and no stake attached. The verb answers it (① scan the leaf's `QA/` → ② digest what `results/` already hold → ③ run P-B-E-R at the shallowest depth that answers it) or REFUSES it, and hands back a path to `<leaf>/QA/<n>-<slug>.md`. It never learns who asked, or why.

That door is a SIDE door. The task session's primary mode is autonomous Plan → Build → Execute → Report with no question pending at all.

For the human reader, the wider mental model:

```text
⚙️ the executors — they run; the bank grows here, mostly with nobody asking
task       = execute internal work (code, runs, metrics)
discovery  = inspect outside evidence (literature, prior art)

📄 the consumers — they ask, and they interpret; we never see them
paper/app  = deliver audience-facing narrative
```
