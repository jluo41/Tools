---
name: phyanno-run
description: >
  Run a full phyanno RA annotation session. Claude loops through all pending
  physicians in an evaluation batch, annotating each one fully (5 traits × 3 stages)
  and marking them complete. Use when the user wants to run a batch annotation session,
  process multiple physicians automatically, or says /phyanno-run.
---

# PhyAnno Run — Full Batch RA Session

Inputs: `evaluationId` (e.g. `EVAL-2024-001`), `username` (e.g. `claude-ra-1`)

Load before starting: `ref/ref-api.md`, `ref/ref-big5.md`

---

## Protocol

### Step 1. Validate batch

```
GET /evaluations/{evaluationId}/validate?username={username}
```

- If 404 → stop: "Evaluation batch not found."
- If 403 → stop: "Batch is closed."
- Confirm active and report batch name to user.

---

### Step 2. Loop until all physicians done

Repeat:

**2a. Get next pending physician**
```
GET /evaluations/{evaluationId}/next-physician?username={username}
```
- If `completed: true` → all done. Report final summary. Stop.
- Else extract: `physician_id`, `npi`, `physician.doc_name`

**2b. Start the physician task**
```
POST /evaluations/{evaluationId}/start
Body: {"username": "{username}", "physician_id": {physician_id}}
```
→ Returns `task_id`. Save it.

**2c. Annotate the physician**

Invoke the full **Annotate One Physician** protocol (from `phyanno-one`) with:
- npi = `{npi}`
- task_id = `{task_id}`
- username = `{username}`
- evaluation_id = `{evaluationId}` (for progress updates)

**2d. After all 5 traits done, mark physician complete**
```
POST /evaluations/{evaluationId}/progress
Body: {
  "username": "{username}",
  "physician_id": {physician_id},
  "traits_completed": 5,
  "completed": true
}
```

**2e. Report and continue**

Print one line: `✓ [{order_index}] {doc_name} (NPI {npi}) — all 5 traits annotated.`

Then loop back to Step 2a.

---

## Progress Updates (during trait annotation)

After completing each trait, also post an interim update so the UI shows progress:
```
POST /evaluations/{evaluationId}/progress
Body: {
  "username": "{username}",
  "physician_id": {physician_id},
  "current_trait": "{trait}",
  "traits_completed": {n},
  "completed": false
}
```
Where `n` is 1 after the first trait, 2 after the second, etc.

---

## Error Handling

- If any API call fails with 5xx, retry once after 5 seconds.
- If it fails again, log the error and skip to the next physician.
- At the end, report any skipped physicians.
