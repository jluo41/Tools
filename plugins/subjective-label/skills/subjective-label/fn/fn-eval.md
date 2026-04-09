fn-eval: Evaluate Gallery Quality
===================================

Phase 3. Compare weak model output against human ground truth.
Goal: validate that the gallery captures the human's criteria accurately.

Rule: if the model is wrong -> fix the GALLERY, not the model.

---

Step 0: Load Assets
--------------------

  Check {project_dir}/eval/eval_set.jsonl exists.
  Check {project_dir}/output/annotations.jsonl exists.
  Check {project_dir}/gallery/gallery.json exists.

  If eval_set.jsonl missing:
    "No eval set found. Create {project_dir}/eval/eval_set.jsonl with
    human-labeled examples: {id, text, label, annotator} per line.
    Target: 20-50 items, separate from gallery sample."
    Stop.

  If annotations.jsonl missing:
    "No inference output found. Run /subjective-label infer first."
    Stop.

  Load eval_set.jsonl   -> eval_items   [{id, text, label (human)}]
  Load annotations.jsonl -> model_outputs [{id, label (model), confidence, reasoning_trace}]

  Match by id. Report N matched items.


Step 1: Compute Accuracy
-------------------------

  For each matched item:
    correct = (model_label == human_label)

  Overall accuracy = correct_count / total_count

  Per-label metrics:
    For each label_value in schema:
      precision = TP / (TP + FP)
      recall    = TP / (TP + FN)
      f1        = 2 * precision * recall / (precision + recall)

  Cohen's kappa:
    Compute kappa between model labels and human labels.
    Interpretation:
      < 0.40  Poor      — gallery needs significant work
      0.40-0.60  Moderate   — gallery usable but review failures
      0.60-0.75  Substantial — gallery is good, minor refinements
      > 0.75  Excellent  — gallery fully captures criteria


Step 2: Confusion Matrix
-------------------------

  Print confusion matrix:

    Human \ Model  | label_A | label_B | label_C | ...
    --------------|---------|---------|---------|----
    label_A       |   N     |   N     |   N     |
    label_B       |   N     |   N     |   N     |
    ...

  Identify most common confusions (off-diagonal with highest count).


Step 3: Failure Analysis
-------------------------

  For each item where model_label != human_label:

    Print:
      ID: {id}
      Text: {text}
      Human: {human_label}
      Model: {model_label}
      Model reasoning: {reasoning_trace}

    Categorize the failure:
      A. Boundary case — human and model disagree on a genuinely ambiguous item
      B. Gallery gap — no gallery example covers this pattern
      C. Rule ambiguity — guideline rule is unclear for this case
      D. Model error — model misread a clear-cut example

  Count by category.


Step 4: Diagnosis and Recommendation
--------------------------------------

  Based on failure analysis:

  If kappa > 0.75:
    "Gallery quality: Excellent. Proceed with full corpus inference."

  If kappa 0.60-0.75:
    "Gallery quality: Good. Minor refinements recommended.
     Suggested additions to gallery:
     - [list 2-3 failure items of type B or C]
     Add these as labeled examples + update guideline rules."

  If kappa < 0.60:
    "Gallery quality: Needs work. Do not run full corpus inference yet.
     Most failures are type [X]. Action:
     - [if B] Add [N] more examples for label [Y] to gallery.
     - [if C] Rewrite rule [Z] in guideline — current wording is ambiguous.
     - [if A] Review boundary definition with human annotator.
     Re-run /subjective-label gallery to update, then re-run eval."


Step 5: Save Eval Report
--------------------------

  Write {project_dir}/eval/eval_report.md.

  Structure:
    1. Summary (date, N items, kappa, overall accuracy)
    2. Per-label metrics table
    3. Confusion matrix
    4. Failure analysis (top 10 failures, categorized)
    5. Diagnosis and recommendation

  Report:
    "Eval complete. Report saved to eval/eval_report.md.
     Kappa: [value] ([interpretation])
     Next: [recommendation from Step 4]"
