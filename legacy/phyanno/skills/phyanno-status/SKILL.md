---
name: phyanno-status
description: >
  Show annotation progress for a phyanno evaluation batch. Reports total physicians,
  how many are completed, in-progress, and pending for a given username. Use when the
  user wants to check annotation status, see how much work remains, or says /phyanno-status.
---

# PhyAnno Status — Batch Progress Check

Inputs: `evaluationId`, `username`

Load before starting: `ref/ref-api.md`

---

## Protocol

### Step 1. Validate batch

```
GET /evaluations/{evaluationId}/validate?username={username}
```

Extract batch `name` and `description`.

---

### Step 2. Get physician list with progress

```
GET /evaluations/{evaluationId}/physicians?username={username}
```

Extract `physicians` array and `summary` object.

---

### Step 3. Report

Print a summary table:

```
Batch: {name}  (ID: {evaluationId})
User:  {username}

Progress: {completed} / {total} physicians  ({progress_percentage:.0f}%)

Status breakdown:
  ✓ Completed     : {completed}
  ⟳ In Progress   : {in_progress}   (started but traits_completed < 5)
  · Pending       : {pending}       (not yet started)

Physicians:
  [{order}] {doc_name} ({specialty})  NPI {npi}
      → Completed ✓  |  In Progress ({traits_completed}/5)  |  Pending
  ...

Next to annotate: {next_physician.doc_name} (NPI {next_physician.npi})
  Run: /phyanno-run {evaluationId} {username}
```

Compute in_progress and pending from the physicians list:
- completed: `progress.completed == true`
- in_progress: `progress.started_at != null && progress.completed == false`
- pending: `progress == null`
