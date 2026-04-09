ref-assets: Asset Formats and Directory Layout
===============================================

---

Directory Layout
----------------

  {project_dir}/
    config.yaml             task definition + label schema
    sample/                 raw input texts (Phase 1)
      sample.jsonl          one {"id": "...", "text": "..."} per line
    gallery/                core artifact (Phase 1 output)
      gallery.json          labeled examples array
      guideline.md          extracted annotation rules
    output/                 inference results (Phase 2)
      annotations.jsonl     one result per line
    eval/                   evaluation (Phase 3)
      eval_set.jsonl        human ground truth
      eval_report.md        accuracy + failure analysis


config.yaml Format
------------------

  task_description: |
    One paragraph describing the annotation task, its purpose,
    and how results will be used.

  label_schema:
    - dimension: nudge_type
      values:
        - name: authoritative
          definition: "Doctor makes recommendation without asking patient values first."
        - name: informational
          definition: "Doctor states prognosis only. No recommendation."
        - name: advisory
          definition: "Doctor states prognosis AND asks about patient values."
        - name: responsive
          definition: "Doctor asks patient values before stating prognosis."
        - name: none
          definition: "Neutral turn. No prognostic communication."

  model:
    gallery_model: claude-sonnet-4-6     # strong model for gallery generation
    inference_model: claude-haiku-4-5   # weak model for inference


sample.jsonl Format
-------------------

  One JSON object per line. Required fields: id, text.

  {"id": "001", "text": "Given the scan results, I think we should..."}
  {"id": "002", "text": "Her survival chances are less than 20%."}

  Optional fields: speaker, source, metadata (any extra context).


gallery.json Format
-------------------

  JSON array of labeled example objects.

  [
    {
      "id":           "001",
      "text":         "I think we should stop aggressive treatment.",
      "label":        "authoritative",
      "reasoning":    "Doctor makes a direct recommendation without first asking
                      what the patient would have wanted.",
      "rule_snippet": "explicit recommendation before value elicitation"
    },
    ...
  ]

  Required fields: id, text, label, reasoning, rule_snippet.


annotations.jsonl Format
------------------------

  One JSON object per line.

  {"id": "042", "text": "...", "label": "advisory", "confidence": "high",
   "reasoning_trace": "Clinician stated prognosis then asked about patient values..."}

  confidence values: "high" | "medium" | "low"


eval_set.jsonl Format
---------------------

  {"id": "e001", "text": "...", "label": "responsive", "annotator": "human_expert"}
  {"id": "e002", "text": "...", "label": "none",       "annotator": "human_expert"}
