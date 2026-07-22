---
name: sl-validate
description: "Benchmark current gallery against a public dataset with known human annotations (GoEmotions / MFTC / POPQuorn / DICES). Computes Cohen's κ and Krippendorff's α between the agent panel and the human consensus. Use when the researcher says /sl-validate, wants to check convergence, or wants a trust metric before deploying at scale."
---

Skill: sl-validate
==================

Proves the agent panel matches a human panel on data with known ground truth.
Convergence signal = agent-vs-human κ reaches human-κ ceiling.

Protocol
--------

Step 1. Load context.
  Read: ref/ref-datasets.md, ref/ref-architecture.md, ref/ref-output-style.md
  Read {project_dir}/.state.json, config.yaml, gallery/
  If no gallery entries yet: tell researcher to run /sl-iterate first. Stop.

Step 2. Choose validation dataset.
  Ask researcher which public dataset to validate against:
    - GoEmotions (27 emotion categories, human κ ~0.46)
    - MFTC (moral foundations, human κ ~0.6)
    - POPQuorn (per-annotator subjective labels, κ varies)
    - DICES (conversation safety, human κ low / multi-perspective)
    - custom: researcher provides their own held-out labeled set
  Default: whichever dataset is closest to current project's topic
  (see ref-datasets.md mapping).

Step 3. Invoke Validator (subagent_type: validator-agent).
  Pass:
    project_dir: <path>
    dataset: <dataset_name>
    n_items: <default 200>
    target_dimension: <how to map dataset labels to project labels>

  Validator runs:
    (a) Load dataset held-out split (or download + cache).
    (b) Invoke Labeler Panel on the held-out items using current gallery.
    (c) Aggregate panel labels per item (majority vote + tie-break).
    (d) Compute:
          - Cohen's κ (agent panel vs human consensus)
          - Krippendorff's α (if per-annotator human labels available)
          - Per-label F1
          - Confusion matrix
          - Disagreement profile (which items the agent panel missed)
    (e) Compare against dataset's published human-κ ceiling.

Step 4. Write report.
  {project_dir}/validation/{dataset}_{iter}_report.md  (result-first, ≤1 screen)
  Append row to {project_dir}/validation/trajectory.jsonl
  (iteration, dataset, κ, α, F1, gap-to-ceiling)
  Refresh REPORT.md: update the validate row (agent κ vs ceiling → converged/below).
  Record construct-validity verdict (is the dataset a valid analog?) — see ref/ref-datasets.md.

Step 5. Report to researcher.
  "Iteration {N} validation:
     agent-vs-human κ = {value} (ceiling: {ceiling})
     gap = {diff}
   Verdict:
     - CONVERGED  (gap < 0.05): ready to /sl-scale
     - IMPROVING  (κ going up): run another /sl-iterate
     - STALLED    (κ flat): Analyzer flagged X systematic failure mode; recommend adjustment"


Autonomy-license mode (S6) — the correct role of public datasets
----------------------------------------------------------------

Public datasets are NOT a substitute for the target-construct gold (that would be
the construct-transfer flaw F2). Their real role is the **autonomy license**
(note-update.md Part 4 / ref-datasets registry):

  mode: license
    1. For each battery dataset (DICES / POPQuorn / GoEmotions / LeWiDi), run the
       WHOLE engine on its NATIVE construct; project its labels to a HIGH/LOW/NONE
       (or matching) schema.
    2. `lib/license.py assess --agent <engine preds> --raters <per-rater> --labels ... --type ...`
       → human ceiling (Krippendorff α) vs agent-vs-consensus κ → PASS / BELOW.
    3. PASS across the battery licenses AUTONOMOUS runs on new constructs ADJACENT
       to it (report coverage; a construct far from the battery gets a weaker license).

  mode: registry-match
    For a new construct, find construct-ADJACENT battery sets; skip cleanly if none.

A target construct (e.g. physician openness) with NO public analog is NOT
validated by borrowing one — it inherits trust from the license (scoped to
adjacency) and is measured per-project by reliability + held-out generalization
(lib/converge.py), never by claiming a public set's construct is its own."
