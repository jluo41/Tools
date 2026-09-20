---
name: haipipe-task-gpu-training
description: >-
  Run long-lived GPU training Tasks with durable checkpoints, safe resume,
  finite OOM fallback, preemption handling, and auditable training receipts.
  Use with haipipe-task-for-fit; do not use for LM serving or engine
  benchmarks.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.1.0"
  last_updated: "2026-09-19"
---

# haipipe-task-gpu-training

This is the training-execution companion to `haipipe-task-for-fit`. It owns
the lifecycle of a real GPU training Run; it does not define the model,
dataset, loss, benchmark, or scientific claim.

## Boundary and routing

- Use `haipipe-task-for-fit` to define the training Job, dataset/version,
  model configuration, optimizer, checkpoints, and metrics.
- Use this skill when the fit Task needs exclusive GPU allocation, a durable
  queue, checkpoint/resume, preemption handling, a sweep, or OOM backoff.
- Also read `../haipipe-task-gpu/SKILL.md` for the shared GPU preflight,
  process-ownership, teardown, and receipt rules.
- Do not use this skill for LLM serving, inference throughput, engine
  compatibility, or MTP benchmarks; use the LLM/evaluation owner plus the
  generic GPU skill instead.

Keep the normal hierarchy:

```text
Job: model + training data/configuration
└── Task: one training setting + one aim
    ├── r01_train_baseline.sh
    ├── r02_train_resume.sh
    └── results/<run>/{runtime.yaml, metrics, logs}
```

The supervisor may order Runs, but it must not mint hidden Runs or move
checkpoints into an untracked location.

## Training Run contract

Before launch, each Run must record:

- immutable dataset/version and split identifiers;
- model initialization or parent checkpoint;
- seed, dtype, sequence length, micro-batch, gradient accumulation, and
  effective batch size;
- optimizer, learning-rate schedule, stopping rule, and evaluation cadence;
- exact environment/commit and declared GPU set;
- checkpoint root, retention policy, and whether resume is allowed.

At terminal state, write `runtime.yaml` with the command, config path,
checkpoint path, GPU preflight, start/end times, exit code, final metrics,
and one of `complete`, `failed`, `blocked`, or `cancelled`.

Heavy checkpoints belong in the model-instance/checkpoint store, not inside a
small `results/` directory. The Result must contain pointers and hashes so a
later evaluation can identify the exact weights.

## Lifecycle

1. Preflight the exact GPU set and verify that the checkpoint/output roots are
   writable and have sufficient space.
2. Start the training process as a supervised process group and write a
   launch receipt before the first optimizer step.
3. Monitor progress, GPU health, disk usage, checkpoint freshness, and the
   declared evaluation signals. A long run must emit periodic heartbeats.
4. On normal completion, verify the final checkpoint and metrics before
   marking the Run complete.
5. On interruption or preemption, terminate only the owned process group,
   flush the latest safe checkpoint, and mark the Run resumable or failed
   with evidence.
6. Wait for CUDA teardown before handing the GPU to the next Run.

Never treat a shell exit code alone as a valid training result. A zero exit
code without a readable checkpoint and metrics receipt is incomplete.

## Resume and checkpoint rules

- Resume only from a verified checkpoint whose model/config/dataset identity
  matches the Run, unless the Run explicitly declares a warm-start change.
- Preserve the optimizer, scheduler, scaler, RNG, and dataloader state when
  claiming an exact resume. If only model weights are restored, record it as
  a warm start, not a resume.
- Do not overwrite a healthy checkpoint with a newer partially written file;
  use an atomic temporary path and a completion marker or hash.
- A resumed attempt gets its own log and receipt and links to the parent
  receipt. It must not erase the failed or interrupted attempt.

## OOM, preemption, and sweep policy

For OOM or an environment failure:

1. Preserve the failed receipt and capture the error and GPU snapshot.
2. Classify the cause: model fit, activation/KV memory, batch/sequence
   shape, filesystem, or environment.
3. Apply only a finite, predeclared fallback ladder. Prefer lowering the
   micro-batch while preserving effective batch with gradient accumulation;
   if effective batch or sequence length changes, create a distinct Run and
   do not silently compare it with the original.
4. Stop after the declared ladder. A repeated OOM is `failed` or `blocked`,
   not an infinite retry loop.

Parallelize a sweep only when GPU sets are disjoint and each Run has its own
output/checkpoint namespace. Otherwise use an ordered queue. Do not kill an
unowned process to make a card available.

## Minimum audit before reporting success

- dataset, config, seed, environment, and GPU set are recorded;
- the final checkpoint can be loaded and its hash is recorded;
- metrics cover the declared train/validation/test phases;
- no partial or resumed attempt is mislabeled as the original Run;
- the queue log records fallback, resume, preemption, and teardown events;
- the next Run is running, safely queued, or the queue has a terminal record.

Return:

```text
status:    ok | blocked | failed
summary:   training Run, checkpoint/resume state, and terminal outcome
artifacts: config, ticket, checkpoint, metrics, runtime receipt, queue log
next:      next safe Run, resume action, or required human decision
```
