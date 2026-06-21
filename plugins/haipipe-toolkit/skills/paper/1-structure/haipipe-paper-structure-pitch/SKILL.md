---
name: haipipe-paper-structure-pitch
description: "Create or update the paper folder's 0-pitch/PAPER_PITCH.md: a one-minute, evidence-constrained story for this concrete manuscript. Archives semantic old versions and appends PITCH_LOG.md entries when the pitch shifts. Use for paper pitch, one-minute story, hook/surprise/so-what, story trajectory, pitch provenance."
argument-hint: "[paper-dir] [--reason <slug>] [--source <path-or-note>...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "1.0.0"
  last_updated: "2026-06-20"
  summary: "Maintain 0-pitch/ as the one-minute public-facing story and provenance layer for a concrete paper folder."
---

Skill: haipipe-paper-structure-pitch
====================================

Maintain the **paper pitch** for a concrete manuscript folder.

The pitch is not a paper plan, outline, or claim matrix. It is the version a
person can understand in one minute:

```
What is this paper about?
Why should anyone care?
What is surprising?
So what changes if it is true?
Why should we believe it?
What is still fragile?
How did the story get here?
```

Illustration:
- `images/stage2-pitch-gate-image2.png` — Stage 2 as a pitch gate: either return
  to narrative/project work or proceed to Stage 3 evidence-backed narrative.

Location:

```
<paper>/
└── 0-pitch/
    ├── PAPER_PITCH.md       current one-minute story
    ├── PITCH_LOG.md         short provenance log
    └── archive/             older semantic pitch snapshots
```

Principles
----------

1. **One minute or it failed.** `PAPER_PITCH.md` should be readable in one
   minute. Keep it short enough to fit on one screen.
2. **Pitch can start as intuition.** A seed pitch may cite author judgment,
   a research review, or a rough direction.
3. **Later shifts need sources.** Every semantic shift after the seed should
   cite a source: `discoveries/`, `tasks/`, `probes/`, `insights/`, reviewer
   feedback, venue strategy, or an explicit author decision.
4. **Archive semantic versions only.** Archive when the story state changes
   (`seed -> discovery-shift`, `accuracy -> robustness`, `method-first ->
   application-first`), not for typo edits.
5. **Do not write the paper here.** Abstract, intro, section plan, and LaTeX
   belong downstream. This skill only maintains the story kernel.

Workflow
--------

### Step 1: Resolve paper folder

Accept either the paper root or any path inside it. Find the paper root by
looking upward for one of:

- `0-pitch/`
- a `0-*.tex` master and `0-sections/`
- `1-compile.sh`

If no paper folder exists, ask the user to run:

```
/haipipe-paper-structure folder <paper-root>
```

### Step 2: Ensure `0-pitch/` exists

Create missing files with the templates below:

```markdown
# Paper Pitch

## Current Pitch
One sentence that a non-specialist can repeat after one minute.

## Hook
Why should a random reader care?

## Surprise
What is the non-obvious turn, tension, or finding?

## So What
What changes if this story is true, and who can use it?

## Why Believe
- Evidence 1: [source path or intuition if seed-stage]
- Evidence 2: [source path]
- Evidence 3: [source path]

## Still Fragile
- The weakest point or most important missing evidence.

## Next Evidence Move
What discovery, task, probe, or review should happen next?
```

```markdown
# Pitch Log

## v01 -- Seed

Archived:
- none

Source:
- Author intuition / initial review / early project direction.

Pitch:
- See `PAPER_PITCH.md`.

Why this version:
- Initial public-facing story before the evidence base is stable.

Still fragile:
- No direct evidence may exist yet.

Next:
- Identify the first discovery, task, or probe that can strengthen or kill this story.
```

### Step 3: Update the current pitch

When the user gives a new pitch or asks for a pitch revision:

1. Read the current `PAPER_PITCH.md`.
2. If the change is semantic, archive the old file first:
   `0-pitch/archive/vNN_<reason>.md`.
3. Write the new `PAPER_PITCH.md`.
4. Append a compact `PITCH_LOG.md` entry.

Log entry shape:

```markdown
## v02 -> v03 -- <reason>

Archived:
- archive/v02_<reason>.md

Source:
- <author decision / discovery / task / probe / insight / review>

Change:
- Old: ...
- New: ...

Why:
- ...

Still fragile:
- ...

Next:
- ...
```

### Step 4: Handoff

After updating pitch, report:

- current pitch version
- archived snapshot path, if any
- sources cited
- whether the current pitch is seed / working / reliable / paper-ready
- next structural command, usually:

```
/haipipe-paper-structure narrative <paper-dir>
/haipipe-paper-structure architecture <paper-dir>
/haipipe-paper-structure plan <paper-dir>
```

Relationship to other structure skills
--------------------------------------

`0-pitch/PAPER_PITCH.md` is upstream of the formal writing artifacts:

```
PAPER_PITCH.md
  one-minute public-facing story
      ↓
NARRATIVE_REPORT.md
  evidence-backed design contract
      ↓
vNN-architecture-minimap.md
  strategic paper blueprint
      ↓
PAPER_PLAN.md
  section / figure / citation execution outline
```

If downstream artifacts disagree with `PAPER_PITCH.md`, either update the pitch
with a logged reason or revise the downstream artifact. Do not let abstract,
introduction, hero figure, and discussion carry different stories.
