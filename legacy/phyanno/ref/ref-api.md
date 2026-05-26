# Reference: PhyAnno API

**Base URL:** `https://phyreview-backend.onrender.com/api`

Use `curl` via the Bash tool for all API calls. All requests/responses are JSON.

---

## Batch Management

### Validate evaluation batch
```bash
curl -s "https://phyreview-backend.onrender.com/api/evaluations/{evaluationId}/validate?username={username}"
```
Response: `{"valid": true, "evaluation": {"id", "evaluation_id", "name", "description", "is_active"}}`

### Get physician list with progress
```bash
curl -s "https://phyreview-backend.onrender.com/api/evaluations/{evaluationId}/physicians?username={username}"
```
Response: `{"physicians": [...], "summary": {"total", "completed", "progress_percentage"}}`

Each physician entry: `{"id", "evaluation_id", "physician_id", "npi", "order_index", "physician": {"first_name", "last_name", "specialty", "doc_name"}, "progress": {"completed", "traits_completed", "started_at", "completed_at"}}`

### Get next pending physician
```bash
curl -s "https://phyreview-backend.onrender.com/api/evaluations/{evaluationId}/next-physician?username={username}"
```
Response (pending): `{"completed": false, "next_physician": {"id", "evaluation_id", "physician_id", "npi", "order_index", "physician": {...}}}`
Response (all done): `{"completed": true, "message": "All physician evaluations completed"}`

### Start physician evaluation → get task_id
```bash
curl -s -X POST "https://phyreview-backend.onrender.com/api/evaluations/{evaluationId}/start" \
  -H "Content-Type: application/json" \
  -d '{"username": "{username}", "physician_id": {physician_id}}'
```
Response: `{"task_id": 42, "message": "Evaluation task started"}`

### Update evaluation progress
```bash
curl -s -X POST "https://phyreview-backend.onrender.com/api/evaluations/{evaluationId}/progress" \
  -H "Content-Type: application/json" \
  -d '{"username": "{username}", "physician_id": {physician_id}, "current_trait": "{trait}", "traits_completed": {n}, "completed": false}'
```

### Mark physician complete
Same endpoint as above, with `"completed": true` and `"traits_completed": 5`:
```bash
curl -s -X POST "https://phyreview-backend.onrender.com/api/evaluations/{evaluationId}/progress" \
  -H "Content-Type: application/json" \
  -d '{"username": "{username}", "physician_id": {physician_id}, "traits_completed": 5, "completed": true}'
```

---

## Physician & Task Data

### Get physician info + all reviews
```bash
curl -s "https://phyreview-backend.onrender.com/api/physician/{npi}"
```
Response: `{"id", "npi", "first_name", "last_name", "specialty", "doc_name", "num_reviews", "reviews": [{"id", "review_index", "source", "date", "text"}, ...]}`

### Get task info + existing model annotations
```bash
curl -s "https://phyreview-backend.onrender.com/api/physician/{npi}/task/{task_id}?username={username}"
```
Response: `{"task": {"id", "physician_id", "status", "assigned_to"}, "model_annotations": [...]}`

---

## Per-Trait Annotation Workflow

### Check trait progress
```bash
curl -s "https://phyreview-backend.onrender.com/api/physician/{npi}/task/{task_id}/trait/{trait}/progress?username={username}"
```
Response: `{"human_annotation_completed": bool, "machine_evaluation_completed": bool, "review_completed": bool, ...}`

Trait values: `openness` | `conscientiousness` | `extraversion` | `agreeableness` | `neuroticism`

### Stage 1: Submit human annotation
```bash
curl -s -X POST "https://phyreview-backend.onrender.com/api/physician/{npi}/task/{task_id}/trait/{trait}/human-annotation" \
  -H "Content-Type: application/json" \
  -d '{
    "physician_id": 0,
    "evaluator": "{username}",
    "task_id": {task_id},
    "trait": "{trait}",
    "score": {1-5},
    "consistency": {1-3},
    "sufficiency": {1-3},
    "evidence": "{2-3 sentence evidence string}",
    "submission_type": "initial"
  }'
```
Response: `{"message": "Annotation submitted successfully", "submission_type": "initial", "submission_number": 1}`

For Stage 3 revision, change `submission_type` to `"review"`.

### Stage 2: Get machine annotations for this trait
```bash
curl -s "https://phyreview-backend.onrender.com/api/physician/{npi}/task/{task_id}/trait/{trait}/machine-annotations"
```
Response: array of `{"id", "model_name", "trait", "score": "Low|Moderate|High|...", "consistency": "Low|Moderate|High", "sufficiency": "Low|Moderate|High", "evidence": "..."}`

Note: machine annotation `score` is a **string** (not integer). Human annotation `score` is an **integer** 1–5.

### Stage 2: Submit machine evaluation ratings
```bash
curl -s -X POST "https://phyreview-backend.onrender.com/api/physician/{npi}/task/{task_id}/trait/{trait}/machine-evaluation" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "model_annotation_id": {id},
      "physician_id": 0,
      "task_id": {task_id},
      "evaluator": "{username}",
      "trait": "{trait}",
      "model_name": "{model_name}",
      "rating": "thumb_up|just_soso|thumb_down",
      "comment": "{one sentence explanation}"
    }
  ]'
```
If no machine annotations exist, post an empty array `[]`:
```bash
curl -s -X POST "https://phyreview-backend.onrender.com/api/physician/{npi}/task/{task_id}/trait/{trait}/machine-evaluation" \
  -H "Content-Type: application/json" \
  -d '[]'
```

### Stage 3: Get annotation history (for review)
```bash
curl -s "https://phyreview-backend.onrender.com/api/physician/{npi}/task/{task_id}/trait/{trait}/history?username={username}"
```
Response: `{"human_annotation": {...}, "machine_evaluations": [...]}`

### Stage 3: Complete trait
```bash
curl -s -X POST "https://phyreview-backend.onrender.com/api/physician/{npi}/task/{task_id}/trait/{trait}/complete" \
  -H "Content-Type: application/json" \
  -d '{"evaluator": "{username}"}'
```
Response: `{"message": "Trait completed successfully"}`

---

## Notes

- `physician_id` in request bodies is **ignored** by the backend — it resolves from the NPI in the URL. Use `0` as a placeholder.
- `task_id` in request bodies must match the URL parameter.
- The backend is hosted on Render free tier; first request may take ~30s to cold-start. Retry once if you get a timeout.
