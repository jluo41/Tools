---
name: haipipe-labeling-expression
description: >-
  The 🛠 expression Task of a labeling Job: rounds e01, e02 … under one signed meaning mNN. One prompt runs a round:
  Rewrite (the wording the models follow, from Train errors only) → Run (the executors label Train and Test) →
  Evaluate (score by set and model, sort errors into four kinds, write the round report). It never asks the person
  and never changes a rule or a reference label: those go back to the meaning Task's next report. Release freezes a
  version once its criteria pass, and the person signs it. It runs the prompts the workbench's expression page copies.
  Trigger: expression round, rewrite the wording, run the executors, evaluate, round report, release,
  /haipipe-labeling-expression.
metadata:
  version: "0.2.0"
  last_updated: "2026-11-04"
  # version history: ./CHANGELOG.md
---

# /haipipe-labeling-expression · one round under a fixed meaning

The second loop of a labeling Job (b15 s58; JL 261101: "loop within the meaning loop and expression loop, and loop
from expression to the meaning"). Meaning decides what the label means; expression only finds the words the models
follow, and sends anything about rules or labels back.

```text
signed mNN ─▶ Rewrite eNN ─▶ Run ─▶ Evaluate ─▶ round report eNN ─┬─▶ wording issue: Rewrite e(N+1)
                                                                    └─▶ wrong label, rule gap: 🧭 meaning's next report
```

## First: the meaning is signed

`meaning_versions.approved_meaning(<Job>)` (engine `E = skills/2_theme/labeling/engine/`) returns the meaning Task,
its newest signed mNN and the sign. None: stop and reply that expression waits for the sign in 🧭 meaning's Update,
with that page's link. A round always names its mNN; a newer signed mNN starts a new round, never a changed one.

## The layout (the workbench's expression page reads it)

```text
<expression Task>/runs/                   task-type: labeling-expression
├── rNN_rewrite_mNN_eNN/    result/expression.md (the wording), changes.md (one line per change from e(N-1))
├── rNN_run_mNN_eNN/        result/runs.json [{model, train, test, state}], result/predictions/<model>.jsonl
├── rNN_evaluate_mNN_eNN/   result/round_report.md (its first line is the route), errors.json, performance.json
└── rNN_release_eNN/        result/criteria.json [{name, state}], final_labels.jsonl + .md; signed.yaml is your sign
```

## A round: "round eNN" (Rewrite's prompt runs all three; Run's and Evaluate's prompts rerun one)

1. **Rewrite.** Read guideline mNN (`meaning/mNN.mindmap.md`) and its reference labels (the meaning Task's last
   Update, `labels.jsonl`). Write `expression.md`: the instruction, the rules in their order, examples from Train
   items only; then `changes.md`. Change no rule: a rule that cannot be worded clearly is a rule gap for the round report.
2. **Run.** The Run's ticket calls `E/label.py` with the round's `expression.md` as the guideline version and the
   Job's executors from its config, on Train and Test; the reference labels never enter a prompt. It writes
   `runs.json` and one predictions file per model. The person's round prompt is the ask to run it; models that cost
   run on no other ask.
3. **Evaluate.** Score each model on Train and Test against the reference labels (`E/kappa.py`), coverage beside.
   Sort every Train error into one of four kinds:
   - expression issue → the next round's Rewrite;
   - wrong label (the reference label looks wrong) → a card for 🧭 meaning;
   - rule gap (no rule decides it) → a card for 🧭 meaning;
   - executor limit (a model fails where the wording is clear) → recorded, no change.
   Write `errors.json` (kind → count), `performance.json`, and `round_report.md`, whose first line is its route:
   `<n> wrong label, <n> rule gaps → meaning, Loop <N+1>`, or `wording only → e<N+1>`.
4. **Stop at the round report.** Nothing asks the person; 🧭 meaning's next Report reads it as a source. Reply: the
   expression Task's Work › Evaluate link.

## Release: "step Release"

Freeze mNN · eNN · its reference labels · the model settings, and check the criteria into `criteria.json`: quality and
coverage floors on Test, no regression on the strongest model, cost per accepted item. A failed criterion routes back
(wording: expression; a rule or label: meaning). Then the Job's outcome: `E/meaning_update.py final --labels <the
meaning Task's last labels.jsonl> --predictions <the Run's result/predictions> --out <this Run>/result` writes
`final_labels.jsonl` and `.md`, each item's label, who decided it and what each executor said (a disagreement is a
flag, never a change). The person signs on the page (Release: Sign release eNN), which writes `result/signed.yaml`
through `meaning_versions.sign_release` and is refused until every criterion is met; no agent signs.

## The rules

1. **Train only for the wording.** Errors and examples come from Train; Test is scored, never read for wording.
2. **Never a rule, never a label.** Both belong to meaning; expression only reports them.
3. **One round, one meaning.** A round runs under the signed mNN it names.
4. **Model disagreement is a flag** (deck v12, slide 12), never a label.
