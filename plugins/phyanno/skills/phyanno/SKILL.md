---
name: phyanno
description: >
  Physician personality annotation skill. Claude acts as a research assistant (RA) to
  annotate Big Five personality traits (Openness, Conscientiousness, Extraversion,
  Agreeableness, Neuroticism) from patient reviews using the phyanno platform API.
  Use when the user wants to run an annotation session, annotate a batch of physicians,
  check annotation progress, or says /phyanno. Routes to phyanno-run, phyanno-one,
  or phyanno-status.
---

# PhyAnno — Physician Annotation Skill (Router)

Claude acts as an RA annotator: reads patient reviews, scores Big Five personality
traits, evaluates LLM model outputs, and submits everything through the phyanno API.

Invocation: `/phyanno <command> [args]`

## Sub-commands

| Command | What it does |
|---------|-------------|
| `/phyanno` | Show this menu |
| `/phyanno-run <evaluationId> <username>` | Run full RA session — auto-loop through all pending physicians in a batch |
| `/phyanno-one <npi> <taskId> <username>` | Annotate a single physician (all 5 traits, all 3 stages) |
| `/phyanno-status <evaluationId> <username>` | Show batch progress summary |

## Routing

Parse `$ARGUMENTS` for the first token:

- `run`    → invoke `/phyanno-run`
- `one`    → invoke `/phyanno-one`
- `status` → invoke `/phyanno-status`
- (none)   → show this menu, ask what the user wants

## Core Model

Each annotation task follows a **3-stage workflow per trait**:

```
For each of 5 traits [openness, conscientiousness, extraversion, agreeableness, neuroticism]:
  Stage 1 — Human Annotation : Claude reads reviews → scores trait independently
  Stage 2 — Machine Evaluation : Claude rates each LLM model's annotation
  Stage 3 — Review & Finalize : Claude compares own score vs. models → confirms or revises
```

See `ref/ref-big5.md` for the scoring rubric.
See `ref/ref-api.md` for all API endpoints.
