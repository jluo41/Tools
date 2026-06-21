# Stage 01: Create Paper Folder

## What This Scene Does

Stage 01 creates the concrete paper container. In project-backed HAI-Pipe work,
that container usually lives under:

```text
examples/<Project>/paper/Paper-<Slug>/
```

When a remote exists, this folder should be its own repo and attached to the
project as a submodule. When a remote does not exist yet, a local folder can
stand in temporarily.

## Problem It Solves

It separates a paper-facing artifact from the project knowledge base. The paper
folder can start early, but manuscript obligations start late.

## Artifacts It Reads

Project-side:

- project README or seed
- known narrative notes
- task/probe/discovery inventory

Paper-side:

- Stage 00 classification decision

## Files It Changes

Prospectus mode creates this shape:

```text
Paper-<Slug>/
  README.md
  lifecycle/
    README.md
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

`stage00_topic-appears/current.md` holds the paper-shaped discovery constraint.

`stage01_create-paper-folder/current.md` records the folder creation decision and
hands the topic to project narrative.

## When It Moves Forward

Move forward when:

- the paper folder exists;
- maturity is declared as `prospectus` or `manuscript`;
- the parent project is linked;
- the next owner is explicit.

For an early prospectus, the next owner is usually project narrative.

## When It Loops Back

Loop back to Stage 00 if the folder was created but the direction is too vague
to constrain discovery.

Loop back to project lifecycle if the topic needs narrative/discovery/probe/task
work before a seed pitch is possible.

## Relation To Project Lifecycle

Stage 01 does not trigger probes directly. It hands the paper prospectus to
project narrative. Narrative decides what needs to be discovered, probed, run as
a task, or archived as insight.

## Images

- `images/stage1-paper-prospectus-folder-image2.png`: paper folder as a thin
  prospectus container.
- `images/stage0-stage1-project-lifecycle.png`: how the Stage 0/1 paper
  prospectus hands work back to the project lifecycle.
- `images/stage0-stage1-project-lifecycle.svg`: editable source for the same
  diagram.

