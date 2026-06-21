# Paper Lifecycle Play

This folder is the teaching and walkthrough layer for the HAI-Pipe paper
lifecycle. It is intentionally separate from executable skill instructions.

Use `play/` when the goal is internalization: walking through the lifecycle one
scene at a time, looking at diagrams, and understanding how paper artifacts
relate to project artifacts before writing begins.

## Structure

```text
play/
  _overview/
  stage00_topic-appears/
  stage01_create-paper-folder/
  stage02_seed-pitch/
```

Each stage folder contains:

- `README.md`: the teaching script for that stage
- `images/`: diagrams and image-generation outputs for that stage

`_overview/` contains cross-stage diagrams used to explain the whole paper
lifecycle and its relation to ARIS/project workflows.

The corresponding paper artifact structure is:

```text
paper/Paper-<Slug>/
  lifecycle/
    stage00_topic-appears/
      current.md
      runs/
      feedback/
      assets/
    stage01_create-paper-folder/
      current.md
      runs/
      feedback/
      assets/
```

## Core Rule

Paper lifecycle artifacts are not scattered in the paper root. Each stage owns a
durable lifecycle branch:

```text
lifecycle/stageXX_slug/current.md
```

`current.md` is the active state. `runs/` stores dated snapshots. `feedback/`
stores comments and review notes. `assets/` stores stage-local diagrams or
supporting files.

## Stage Sequence Covered Here

1. `stage00_topic-appears`: decide whether a topic is project-only, paper
   prospectus, or paper seed.
2. `stage01_create-paper-folder`: create the paper container and hand it to
   project narrative without starting manuscript obligations.
3. `stage02_seed-pitch`: write the one-minute paper story and use it as a gate
   back to narrative/project work or forward to paper shaping.
