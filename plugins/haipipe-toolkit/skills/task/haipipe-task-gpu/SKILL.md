---
name: haipipe-task-gpu
description: >-
  Design and run GPU-bound Task queues for training, serving, sweeps, and
  evaluation. Use when work needs exclusive GPU allocation, sequential Runs,
  OOM backoff, multi-card reservation, or automatic handoff to the next Run.
  This is an execution specialist, not a model or benchmark definition.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.1.0"
  last_updated: "2026-09-19"
---

# haipipe-task-gpu

GPU scheduling is a cross-cutting execution concern. Keep the ordinary
Project → Block → Job → Task → Run hierarchy; add a GPU supervisor only when a
Task or a set of Tasks needs durable, exclusive GPU execution.

## Route

- Real model fitting/training: use `haipipe-task-for-fit`, then apply
  `haipipe-task-gpu-training` for checkpoint/resume and the long-lived
  training lifecycle; use this skill for the shared GPU queue mechanics.
- Model evaluation or LLM serving benchmarks: use the owning evaluation/LLM
  Task, then apply this skill to execution.
- GPU queue, OOM retry, no-idle sequencing, or multi-card reservation without
  a domain-specific Task: use this skill directly.

Training-specific companion:
`haipipe-task-gpu-training` owns checkpoint integrity, safe resume,
preemption, effective-batch accounting, and training-specific OOM fallback.
It composes with this skill and does not replace the generic GPU safety rules.

Do not move model identity, benchmark definitions, or quality claims into the
supervisor. The supervisor schedules authored Run Tickets and records their
receipts; the Run owns the computation and Result contract.

## Queue contract

Every queued Run must have its own matching config, Ticket, Result directory,
and `runtime.yaml`. The supervisor must:

1. Start one declared Run at a time for an exclusive GPU set.
2. Wait for that Run's receipt to become terminal (`complete`, `failed`,
   `blocked`, or `cancelled`) rather than trusting only a shell exit code.
3. Wait for the Run's CUDA processes to tear down, then launch the next Ticket
   without an arbitrary long idle sleep.
4. Preserve the failed receipt and logs. A failure may select an explicitly
   declared fallback Run, such as a lower-concurrency config, but never
   overwrites the failed Run or retries forever.
5. Write a queue log/manifest naming the order, start/end timestamps, exit
   codes, receipt paths, GPU set, and fallback decisions.

The queue may poll at a short interval (for example, two seconds). “No GPU
idle” means no intentional queue gap; model teardown, driver initialization,
weight loading, and CUDA compilation can legitimately show zero utilization.
Do not sacrifice receipt integrity or launch two exclusive workers merely to
hide those transitions.

## GPU safety

- Preflight the exact GPU indices with `nvidia-smi`/`pmon` before each Run.
- A single-card Run owns only its selected card; a tensor-parallel Run owns
  the complete declared set and waits until every card is free.
- Never kill an unowned process. If another user occupies a required card,
  record `blocked` with the process snapshot and wait or stop for human input.
- The supervisor owns only child processes it launched and should terminate
  only that process group during normal teardown.
- Keep model weights and other heavy artifacts outside `results/`; receipts,
  logs, metrics, and queue state remain auditable under the declared output
  root.

## OOM and concurrency policy

Concurrency is workload-specific. A speed sweep at fixed prompt length does
not automatically prove that the same concurrency is safe for a full quality
suite with longer or mixed requests. Calibrate under the target context and
engine, then record the selected `C*` in the next Run's config and receipt.

For an OOM or service crash:

1. Keep the failed Run and capture the server/error tail.
2. Classify whether the failure is model load, KV-cache capacity, request
   burst, or an environment/loader defect.
3. Apply a finite, predeclared fallback ladder (for example `64 → 32 → 16 →
   8`) only when the task authorizes it.
4. Compare only completed Runs with valid Result gates; a nonzero quality
   command after partial work is not a valid full score.

## Recommended shape

```text
Job: one model + artifact/quantization
└── Task: one setting + one aim
    ├── r01_capacity_calibration.sh
    ├── r02_full_quality_at_cstar.sh
    └── results/<run>/{runtime.yaml, logs, metrics, ...}

Queue supervisor: ordered Tickets + receipt polling + GPU preflight
```

Use a Task-local `sbatch/` or Job-level queue only when it spans multiple
Tasks. It must not mint hidden Runs or write results outside the normal Run
folders.

## Audit checklist

Before reporting success, verify:

- every Ticket has a matching config and Result receipt;
- the receipt records the target GPU set, preflight snapshot, command,
  start/end time, and failure/fallback information;
- no Run was launched while an unowned process occupied its GPU;
- a failed Run is not counted as a completed benchmark;
- the next queued Run is either running, intentionally blocked with evidence,
  or the queue has a terminal `QUEUE_COMPLETE` record.

Return:

```text
status:    ok | blocked | failed
summary:   queue order, current Run, and terminal/fallback outcome
artifacts: Ticket/config/receipt/queue-log paths
next:      next safe queue or report action
```
