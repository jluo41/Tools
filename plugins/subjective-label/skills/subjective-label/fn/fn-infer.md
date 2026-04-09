fn-infer: Weak Model Inference
================================

Phase 2. Annotate texts using weak model + gallery as context.
Requires gallery/ to exist (run /subjective-label gallery first).

---

Step 0: Load Gallery
---------------------

  Check {project_dir}/gallery/gallery.json exists.
  Check {project_dir}/gallery/guideline.md exists.

  If missing:
    "Gallery not found. Run /subjective-label gallery first."
    Stop.

  Load gallery.json -> gallery_entries (list of labeled examples).
  Load guideline.md -> guideline_text.

  Report: "Gallery loaded: N examples. Guideline loaded."


Step 1: Load Input
-------------------

  Two modes:

  Single text mode:
    Input is provided as a string argument.
    Wrap as: [{"id": "input_001", "text": <arg>}]

  Batch mode:
    Read {project_dir}/sample/ or {project_dir}/input.jsonl.
    Parse all {id, text} items.
    Skip any id already in {project_dir}/output/annotations.jsonl.

  Report: "Loaded N items to annotate. [M already annotated, skipping.]"


Step 2: Build Prompt
---------------------

  Construct the inference prompt template:

  ---------------------------------------------------------------
  SYSTEM:
    You are an expert annotator. Follow the guideline exactly.
    When uncertain, refer to the gallery examples.

  GUIDELINE:
    {guideline_text}

  GALLERY EXAMPLES:
    {for each gallery entry:}
      Text: {text}
      Label: {label}
      Reasoning: {reasoning}
    {end for}

  TASK:
    Label the following text according to the guideline.
    Return JSON: {"label": "...", "confidence": "high|medium|low",
                  "reasoning_trace": "..."}

  TEXT TO LABEL:
    {input text}
  ---------------------------------------------------------------

  Key: gallery examples are included as few-shot context every time.
  Guideline provides the rules; gallery anchors ambiguous cases.


Step 3: Run Inference
----------------------

  For each input item:

    3a. Fill prompt template with item text.

    3b. Call model (weak model — Haiku or equivalent).
        Parse JSON response.

    3c. If JSON parse fails: retry once.
        If still fails: record {"label": "ERROR", "confidence": "low",
                                "reasoning_trace": "model returned unparseable output"}

    3d. Append to results:
        {
          "id":              item id,
          "text":            item text,
          "label":           parsed label,
          "confidence":      parsed confidence,
          "reasoning_trace": parsed reasoning
        }

    3e. Every 10 items: print progress "Annotated [N/Total]..."


Step 4: Save Output
--------------------

  Write results to {project_dir}/output/annotations.jsonl.
  One JSON object per line.

  If file already exists: append new results (do not overwrite existing).

  Report:
    "Inference complete.
     N items annotated -> output/annotations.jsonl

     Label distribution:
       [label_value]: N  ([X]%)
       ...

     Low-confidence items: N
     Errors: N

     Next step: /subjective-label eval — validate accuracy on held-out set"


Step 5: Flag Low-Confidence Items
-----------------------------------

  Extract all items where confidence == "low".
  If any exist:
    "Warning: [N] items were labeled with low confidence.
     Consider reviewing these manually:
     [list ids + first 80 chars of text]"

  These items are candidates for adding to the gallery
  if human review reveals a new pattern.
