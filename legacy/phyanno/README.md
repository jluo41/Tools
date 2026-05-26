phyanno
=======

Claude acts as a research assistant (RA) to annotate Big Five personality traits
for physicians from patient reviews, using the phyanno platform API.

---

## What this does

Each physician in an evaluation batch gets annotated across all five traits
(Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism)
through a 3-stage workflow:

1. **Human Annotation** — Claude reads all patient reviews and independently
   scores each trait (score 1–5, consistency 1–3, sufficiency 1–3, evidence text)
2. **Machine Evaluation** — Claude rates each LLM model's annotation for the same
   trait (👍 thumb_up / 😐 just_soso / 👎 thumb_down + comment)
3. **Review & Finalize** — Claude compares its own score against machine outputs,
   revises if warranted, then marks the trait complete

Running multiple Claude sessions with different usernames produces multiple
independent annotations per physician for inter-rater reliability analysis.

---

## Skills (4 entry points)

| Command | What it does |
|---------|-------------|
| `/phyanno` | Router — lists sub-commands |
| `/phyanno-run <evaluationId> <username>` | Full RA session — loop through all pending physicians in a batch |
| `/phyanno-one <npi> <taskId> <username>` | Annotate a single physician (all 5 traits) |
| `/phyanno-status <evaluationId> <username>` | Show batch progress summary |

---

## Typical RA workflow

```bash
# Each RA session uses a unique username
/phyanno-run EVAL-2024-001 claude-ra-1
/phyanno-run EVAL-2024-001 claude-ra-2   # parallel session, different username
/phyanno-run EVAL-2024-001 claude-ra-3

# Check progress
/phyanno-status EVAL-2024-001 claude-ra-1
```

---

## Plugin layout

```
phyanno/
├── .claude-plugin/plugin.json
├── skills/
│   ├── phyanno/SKILL.md           ← router
│   ├── phyanno-run/SKILL.md       ← full batch session
│   ├── phyanno-one/SKILL.md       ← single physician
│   └── phyanno-status/SKILL.md    ← progress check
├── ref/
│   ├── ref-big5.md                ← Big Five definitions + scoring rubric
│   └── ref-api.md                 ← API endpoints + exact curl commands
└── README.md
```

---

## Platform

- **API:** `https://phyreview-backend.onrender.com/api`
- **Backend:** Go + Gin (hosted on Render)
- **DB:** PostgreSQL — annotations go into `human_annotations`, `machine_annotation_evaluation`, `trait_progress`
- **Source:** `app/phyanno/` in the Physician-SPACE repo
