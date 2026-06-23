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
| `1_data` | Data | 数 / 数据 | Build data assets: raw/source/record/case/AIData. |
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

## Boundary

Tasks execute internal work. They do not judge research claims, preserve
long-term insight memory, or write paper/application prose.

```text
task       = execute work
probe      = judge claim-level evidence
discovery  = inspect outside evidence
insight    = preserve judged knowledge
paper/app  = deliver audience-facing narrative
```
