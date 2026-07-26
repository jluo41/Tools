# Training the small classifier
state: 🟡 PARTIAL
owner: RA
method: logistic regression on frozen embeddings by default, SetFit as an optional upgrade; retrained at the end of every `/sl-iterate`

## Question
The small classifier in the middle layer of the cascade (Tier 1): what is it trained on, when is it retrained, and when should its answer be trusted?

JL named the modeling, embedding, and training line as something that has to be settled, and training is this face.
It is also the concrete implementation of QC2's option (b), letting a small model take over the labeling.
The middle layer of the QD2 cascade holds or fails on how well this classifier is trained: everything it cannot settle confidently is escalated to the Tier 2 panel, so a poorly trained classifier does not show up as wrong labels, it shows up as the panel being asked to do the work.
While the two open lines below stand, the middle layer is specified but unproven: the accept thresholds have never been exercised inside a real project folder, and there is no rule yet for when the heavier SetFit or LoRA-BERT backend is worth paying for.

## Boundary
- ✅ Covered here
  What the Tier 1 classifier is trained on, when it is retrained, and the thresholds that decide whether its prediction is used or escalated.
- ↪ Covered elsewhere
  How a sentence becomes a vector at all is QD1; how the three layers divide the work and what happens to the items this classifier cannot settle is QD2; whether the remaining thousands are labeled in full or handed to a small model is the call still open in QC2.

## Diagram
```
  already labeled items ──► frozen embedding (QD1) ──► logistic regression (trains in seconds)
                                                        │
                                                        ▼  predicts {label, prob, margin}
                          prob ≥0.70 and margin ≥0.30 ── use it (Tier 1 answers)
                          otherwise ────────────────────► escalate to the Tier 2 panel

  retrain: automatically at the end of every /sl-iterate round
  upgrade: before /sl-scale, opt in to SetFit / LoRA-BERT for a one-time high-quality training
  fallback: CV F1 < 0.6 → tighten the thresholds, or skip Tier 1 entirely (everything goes to the panel)
```

## Items to Finish
- [x] 🧱 The default backend is settled
      A logistic regression on the frozen embeddings, which trains in seconds.
      Frozen means the embedding model itself is not fine-tuned: the vectors from QD1 are used directly as features, so training only fits a classifier on top of them.
      That is what makes the middle layer cheap enough to retrain on every round instead of being something that has to be scheduled.
      A heavier backend stays available as an option, SetFit or LoRA-BERT, run once before `/sl-scale` as a one-time high-quality training and only if the researcher opts in.
- [x] ⏱️ The retrain trigger and the trust thresholds are settled
      Retraining fires automatically at the end of every `/sl-iterate` round, and a prediction is used only when the top probability is at least 0.70 and the margin at least 0.30.
      Retraining each round keeps the classifier in step with the labels confirmed so far, and under `residual` mode the next batch is drawn only from the items the current classifier still cannot settle, so every round goes after the next layer of what is left rather than re-covering what already works.
      Anything under either threshold is escalated to the Tier 2 panel instead of being answered here.
      There is also a floor: if cross-validated F1 falls below 0.6, the thresholds are tightened or Tier 1 is skipped altogether and everything goes to the panel.
- [ ] ⬆️ Decide when a SetFit or LoRA upgrade is worth it
      There is no rule yet for when the heavier backend earns its cost, and the answer moves with which route QC2 picks.
      The upgrade exists as an option (one high-quality training run before `/sl-scale`, researcher opt-in), but nothing states the conditions under which it should be taken.
      It cannot be settled on this face alone, because it depends on QC2's open choice between labeling the remaining thousands in full and training a small model to take over: the more work the classifier is asked to absorb, the more a better-trained backend is worth paying for.
      This is one of the two reasons the face sits at 🟡.
- [ ] 🧪 Run it once inside a real project folder
      The code has self-tests, but it has never been run inside a real project folder.
      The code is in `lib/classify.py` and its self-tests exist, which shows the training and prediction path executes, not that the thresholds mean anything on real data.
      Until a real run happens, the accept values of 0.70 and 0.30 and the CV F1 floor of 0.6 are numbers on paper, and nobody knows what share of items Tier 1 would actually absorb.
      This is the second reason the face sits at 🟡 rather than ✅.

## Where we are
The lightest option is the default and it is fully specified: a logistic regression on frozen embeddings, retrained automatically at the end of every `/sl-iterate` round, with a prediction accepted only at probability 0.70 and margin 0.30 or better and escalated to the Tier 2 panel otherwise.
The code is in `lib/classify.py` and it has self-tests, but it has never actually been run inside a real project folder.
The one open judgment is when the SetFit or LoRA-BERT upgrade is worth its cost, and that is tied to JL's undecided QC2 call.

- 260723 CC · 🔀 The Tier 1 contract was pulled onto the board
      The backend, the retrain trigger, and the accept thresholds were written down here as settled.
      Two things were left open on purpose: the real run had not happened, and the upgrade criterion depends on JL's QC2 decision, so the face was created at 🟡 rather than ✅.

## Files
- `lib/classify.py`
  Where the classifier is trained and where its predictions come from, so this is the file to open when anything on this face changes.
- `lib/embed.py`
  Produces the frozen vectors the classifier trains on; how a sentence becomes a vector at all is QD1's ruling, not this one.
- `ref/ref-cascade.md`
  Writes down Tier 1's contract: the accept thresholds, the retrain trigger, and the CV F1 fallback.
- `ref/ref-config.md`
  Its `classifier:` block declares the backend and the two thresholds, so changing either of them starts in the config.

## Glossary
logreg: logistic regression, the lightest classifier, trained on frozen vectors in a few seconds.
frozen embedding: using QD1's vectors directly as features, without fine-tuning the embedding model itself.
SetFit: a method that fine-tunes a sentence embedding model on a small number of examples, more accurate than logreg but heavier.
CV F1: the cross-validated F1 score, which measures how good the classifier is; below 0.6 it should not be trusted much.
residual: the sampling mode in which the next batch is drawn only from the items the current classifier still cannot settle.

## Discussion
> CC0723: This face is the engineering implementation of QC2 (b) and the inside of QD2's Tier 1 layer. It stays 🟡 because the real run has not been done and the criterion for the SetFit upgrade is bound to JL's QC2 decision.

## Log
260725 · rewritten to the current face format in English
260723 1600 · created: the Tier 1 classifier's backend, retrain trigger, and thresholds were pulled onto the board; the real run and the upgrade criterion were left 🟡
