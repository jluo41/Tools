---
name: phyanno-one
description: >
  Annotate a single physician's Big Five personality traits using the phyanno platform.
  Claude reads all patient reviews, then runs the 3-stage workflow (human annotation →
  machine evaluation → review & finalize) for each of the 5 traits. Use when the user
  wants to annotate one specific physician, or says /phyanno-one.
---

# PhyAnno One — Annotate a Single Physician

Inputs: `npi`, `task_id`, `username`

Load before starting: `ref/ref-api.md`, `ref/ref-big5.md`

---

## Protocol

### Step 1. Load physician data

```
GET /physician/{npi}
```

Extract:
- Physician demographics: `doc_name`, `specialty`, `gender`, `state`
- All reviews: array of `{source, date, text}` — read every review fully

Print: `Loaded {num_reviews} reviews for {doc_name} ({specialty})`

---

### Step 2. For each trait (in this order)

Traits: `openness` → `conscientiousness` → `extraversion` → `agreeableness` → `neuroticism`

For each trait:

**2a. Check existing progress (resume-safe)**
```
GET /physician/{npi}/task/{task_id}/trait/{trait}/progress?username={username}
```
- `human_annotation_completed: false` → run Stage 1
- `machine_evaluation_completed: false` → run Stage 2
- `review_completed: false` → run Stage 3
- All true → skip this trait (already done)

---

**2b. Stage 1 — Human Annotation**

Skip if `human_annotation_completed: true`.

Read the Big Five definition and scoring rubric for `{trait}` from `ref/ref-big5.md`.

Read ALL reviews carefully. Then decide:
- `score` (integer 1–5): evidence level for this trait
- `consistency` (integer 1–3): how consistently the trait appears across reviews
- `sufficiency` (integer 1–3): how much evidence supports the score
- `evidence` (string): 2–3 sentences combining your reasoning with direct quotes

Submit:
```
POST /physician/{npi}/task/{task_id}/trait/{trait}/human-annotation
Body: {
  "physician_id": 0,
  "evaluator": "{username}",
  "task_id": {task_id},
  "trait": "{trait}",
  "score": {score},
  "consistency": {consistency},
  "sufficiency": {sufficiency},
  "evidence": "{evidence}",
  "submission_type": "initial"
}
```

Print: `  Stage 1 [{trait}]: score={score}, consistency={consistency}, sufficiency={sufficiency}`

---

**2c. Stage 2 — Machine Evaluation**

Skip if `machine_evaluation_completed: true`.

```
GET /physician/{npi}/task/{task_id}/trait/{trait}/machine-annotations
```

For each model annotation in the response:
- Read the model's `score`, `evidence`, `consistency`, `sufficiency`
- Rate it: `thumb_up` (accurate + well-evidenced), `just_soso` (partially correct or vague), `thumb_down` (wrong score or poor evidence)
- Write a short `comment` explaining your rating (1 sentence)

Submit all ratings at once:
```
POST /physician/{npi}/task/{task_id}/trait/{trait}/machine-evaluation
Body: [
  {
    "model_annotation_id": {id},
    "physician_id": 0,
    "task_id": {task_id},
    "evaluator": "{username}",
    "trait": "{trait}",
    "model_name": "{model_name}",
    "rating": "thumb_up|just_soso|thumb_down",
    "comment": "{comment}"
  },
  ...
]
```

If the response is an empty array (no machine annotations yet), submit an empty array body `[]` — this marks machine_evaluation_completed and moves on.

Print: `  Stage 2 [{trait}]: rated {n} model(s)`

---

**2d. Stage 3 — Review & Finalize**

Skip if `review_completed: true`.

```
GET /physician/{npi}/task/{task_id}/trait/{trait}/history?username={username}
```

Compare your Stage 1 score against the machine annotations you just rated:
- If a model you rated `thumb_up` has a substantially different score AND its evidence is more compelling than yours → resubmit with `submission_type: "review"` (same POST as Stage 1 but with updated values and `"submission_type": "review"`)
- Otherwise → proceed to complete without changes

Complete the trait:
```
POST /physician/{npi}/task/{task_id}/trait/{trait}/complete
Body: {"evaluator": "{username}"}
```

Print: `  Stage 3 [{trait}]: finalized (revised: yes/no)`

---

### Step 3. Report summary

After all 5 traits:

```
Done: {doc_name} (NPI {npi})
  openness:          score={s}, consistency={c}, sufficiency={s}
  conscientiousness: score={s}, consistency={c}, sufficiency={s}
  extraversion:      score={s}, consistency={c}, sufficiency={s}
  agreeableness:     score={s}, consistency={c}, sufficiency={s}
  neuroticism:       score={s}, consistency={c}, sufficiency={s}
```
