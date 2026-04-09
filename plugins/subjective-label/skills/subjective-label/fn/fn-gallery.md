fn-gallery: Interactive Gallery Generation
==========================================

Phase 1. Human + Strong AI interact over a sample to build the Gallery.
Run once per annotation project. Output: gallery.json + guideline.md.

---

Step 0: Load Config
--------------------

  Read {project_dir}/config.yaml.
  Extract:
    - task_description
    - label_schema  (dimensions + values + definitions)

  If config.yaml does not exist:
    Ask the user two questions:
      Q1. What is this annotation task? (one paragraph)
      Q2. What labels/values should each text receive?
    Write answers to config.yaml before continuing.

  Confirm: "Task: [task_description]. Labels: [values]. Starting gallery generation."


Step 1: Load Sample
--------------------

  Read all files from {project_dir}/sample/.
  Parse into list of {id, text} items.
  Report: "Loaded N items from sample/."

  If sample/ is empty or missing:
    Tell user: "Place your sample texts in {project_dir}/sample/ as
    sample.jsonl (one JSON per line: {id, text}) then re-run."
    Stop.


Step 2: Select Examples for Labeling
--------------------------------------

  Goal: choose 20-30 items from sample for the human to label.
  Strategy: maximize diversity + surface boundary cases.

  Algorithm:
    A. For each label value in label_schema:
         Select 2-3 items that clearly exemplify that value.
         (Use strong LLM judgment: which items are canonical examples?)

    B. Select 5-8 items that are ambiguous / could fit multiple values.
         (These are the boundary cases — most valuable for rule extraction.)

    C. Combine A + B. Remove duplicates. Target total: 20-30 items.

  Do not show the user all items at once. Present one at a time (Step 3).


Step 3: Interactive Labeling Loop
-----------------------------------

  For each selected item (from Step 2), in order:

    3a. Display the item:
        ============================================================
        Item [N/Total]
        ------------------------------------------------------------
        [item text]
        ============================================================
        Label options: [list all values from label_schema]

    3b. Ask the user:
        "What label does this get? And briefly — why?"

    3c. Wait for user response.

    3d. Confirm the label + extract rule:
        - Repeat the label back to user.
        - Identify the key phrase or pattern that drove the decision.
        - Ask: "Is it the phrase '[X]' that signals [label]? Or something else?"

    3e. If user corrects or refines — update.

    3f. Add to gallery_entries:
        {
          "id":           item id,
          "text":         item text,
          "label":        user's label,
          "reasoning":    user's explanation,
          "rule_snippet": extracted pattern / key phrase
        }

    3g. Every 5 items: pause and ask:
        "Pattern check: based on what you've labeled so far, I'm seeing this rule:
        [draft rule]. Does that match your intent?"
        Let user confirm or correct before continuing.

  After all items: proceed to Step 4.


Step 4: Extract Guideline
--------------------------

  Synthesize gallery_entries into guideline.md.

  Structure:

    1. Task Definition (from config.yaml task_description)

    2. Label Schema
       For each label value:
         - Name
         - Definition (synthesized from user's reasoning across examples)
         - Canonical example (one item from gallery)

    3. Decision Rules
       If/then patterns extracted from rule_snippets.
       Example:
         "If the clinician makes a recommendation before asking about
          patient values -> authoritative."

    4. Boundary Cases
       For each ambiguous item labeled in Step 3:
         - The item text
         - Why it could be misread
         - The correct label + tiebreaker rule

    5. Quick Reference Table
       | Signal / Pattern | Label |
       |------------------|-------|
       | ...              | ...   |

  Write to {project_dir}/gallery/guideline.md.


Step 5: Save Gallery
---------------------

  Write all gallery_entries to {project_dir}/gallery/gallery.json.
  Format: JSON array.

  Report:
    "Gallery saved: N examples across [label values].
     Guideline saved to gallery/guideline.md.

     Next step:
       /subjective-label eval   — test gallery quality on held-out set
       /subjective-label infer  — start annotating full corpus"


Step 6: Sanity Check
---------------------

  After saving, verify:
    - Every label value in schema has at least 2 gallery examples.
    - At least 3 boundary case entries exist.

  If any label value has < 2 examples:
    "Warning: label '[X]' has only [N] examples in gallery.
     Consider adding more [X] examples before running inference."
