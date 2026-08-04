# How the three-tier cascade divides the work
state: ✅ SETTLED
owner: CC
method: Tier 0 embedding k-NN, then Tier 1 the small classifier, then Tier 2 the large-model panel; each level down is more expensive and takes fewer items

## Question
When the whole corpus is being labeled, how do we make sure most of the easy items take a cheap route and only the few hard ones disturb an expensive model?

This is the machine answer to QC2, which asks how the remaining thousands of items get finished at all, and the two options weighed there, (a) label the whole corpus outright and (b) train a small model to take over, are merged into a single funnel here.
JL's "pick one" therefore becomes "set the thresholds": how much is handed to embedding inheritance, how much to the small classifier, and how much is allowed to reach the large model.
Setting them is hard because the two ends of the funnel are priced very differently per item (~$0.00001 at Tier 0 against ~$0.05-0.20 at Tier 2), so a gate set too loose buys speed by inheriting wrong labels while a gate set too tight sends nearly everything to the panel and the run stops being affordable.
While this stays open there is no rule saying which items a cheap method is allowed to settle, so a full-corpus run can be neither costed nor started.

## Boundary
- ✅ Covered here
  Which tier settles an item and which escalates it, the threshold at each tier's gate, the record each item keeps of the route it took, and the routing modes that skip tiers.
- ↪ Covered elsewhere
  How a sentence becomes the vector Tier 0 compares against is QD1; how the Tier 1 classifier is trained is QD3; whether to finish the remaining thousands this way at all is QC2's call, and it is still ⏸️ ON HOLD.

## Diagram
```
  ┌ Tier 0 · embedding k-NN ──────────────────────┐  ~$0.00001/item · fastest · takes 60-80%
  │  top-5 gallery neighbors share one label      │
  │  and average cosine sim >= 0.85 → inherit     │
  └────────────┬──────────────────────────────────┘ unresolved ↓
  ┌ Tier 1 · trained small classifier ────────────┐  ~$0.0001/item · fast · takes 10-30%
  │  prob >= 0.70 and margin >= 0.30 → use it     │   (how it is trained: QD3)
  └────────────┬──────────────────────────────────┘ unresolved ↓
  ┌ Tier 2 · large-model panel (3-5 personas) ────┐  ~$0.05-0.20/item · slow · takes 5-15%
  │  majority support >= 0.6 → use it             │
  │  support < 0.6 → drop into the human queue    │
  └───────────────────────────────────────────────┘
```

## Items to Finish
- [x] 🎯 The division of labor and the thresholds are pinned down
      Each tier has one written rule for when it may settle an item, with the numbers fixed at `cascade_inherit_sim` 0.85, `accept_margin` 0.30, `accept_prob` 0.70, and panel support 0.6.
      Tier 0 leans on the gallery: if the top-5 gallery neighbors all carry the same label and their average cosine similarity reaches 0.85, the item inherits that label instead of being labeled again.
      Tier 1 leans on training: the classifier's label is used when its probability reaches 0.70 and its margin over the runner-up reaches 0.30.
      Tier 2 leans on the panel: the majority vote is used when its support reaches 0.6, and anything below that is dropped into the human queue rather than forced.
      Every tier that cannot meet its own bar escalates instead of guessing, which is what makes the funnel cheap at the top without being reckless.
- [x] 🧾 Every item records `method` and `confidence`
      The annotation written for each item carries `method: tier0/1/2` together with a `confidence`, so any label can be traced back to the tier that produced it.
      Without that record the corpus is a flat pile of labels and there is no way to tell an inherited label apart from one the panel argued over.
      With it the cheapest audit in the system becomes possible: "show me everything Tier 0 decided, is any of it obviously wrong".
      That check is what keeps a loose Tier 0 threshold from quietly contaminating the whole run.
- [x] 🔀 Three routing modes are supported
      A run can be sent through `routing=panel`, `routing=single`, or `routing=cascade`, so the funnel can be bypassed when the point of the run is not cost.
      `panel` sends every item to the full panel and is what the validation set uses, because a validation number measured through the cheap tiers would be measuring the cheap tiers.
      `single` uses one labeler and is the cheapest option available.
      `cascade` is the default and the mode the full-corpus rollout runs in.

## Where we are
The three tiers, their thresholds, and the routing modes are all written down, and every checkbox on this face is closed.
What is settled here is the shape of the funnel and the number at each gate, not yet the evidence that those numbers hold on this corpus: the shares in the diagram (60-80% at Tier 0, 10-30% at Tier 1, 5-15% at Tier 2) are what the design expects the split to be.
The middle tier is the weakest part standing today, because QD3, the face that owns how the Tier 1 classifier is trained, is still 🟡 PARTIAL.
QC2, the decision this funnel exists to serve, is still ⏸️ ON HOLD, so the funnel is specified and waiting rather than running.

## Files
- `ref/ref-cascade.md`
  The reference this face was taken from: it holds each tier's invariant, its algorithm, its config block, and the routing modes, so a threshold change starts there.
- `lib/embed.py`
  Tier 0 runs on its `index` and `nearest` subcommands, which produce the top-5 gallery neighbors and the cosine similarities the 0.85 gate is applied to.
- `lib/classify.py`
  Tier 1's gate reads the probability and the `margin` that this file's `predict` emits, and the file already carries `accept_margin` 0.3 and `accept_prob` 0.7 as its defaults.
- `ref/ref-config.md`
  Where the classifier thresholds are declared as configuration (`accept_margin: 0.3, accept_prob: 0.7`), which is what makes a threshold change a config edit rather than a code edit.

## Law
- The cascade is a sieve built up by iteration: each `/sl-iterate` round adds one layer (the gallery grows so Tier 0 takes more, the classifier gets trained so Tier 1 comes up, the guideline tightens so Tier 2 agrees more).
- Tier 0 rests on the gallery, Tier 1 on training, Tier 2 on the panel; all three thresholds live in `config.yaml`, where raising them is safer and more expensive and lowering them is faster and riskier.

## Glossary
k-NN: find the k nearest neighbors and look at their labels.
margin: the gap between the classifier's highest probability and its second highest; the wider the gap, the clearer the decision boundary.
persona: one large-model labeler carrying a particular point of view; a panel is a set of different personas labeling at the same time.
gallery: the set of answers JL personally confirmed, used as the ruler; Tier 0 compares each new item against it.

## Discussion
> CC0723: Tier 0 rests on QD1 (embedding), how the Tier 1 layer is trained is QD3, and this funnel is the engineering implementation of QC2. Reading those three questions together gives the whole picture of the full-corpus rollout. The content comes from `ref/ref-cascade.md`.

## Log
260725 · rewritten to the current face format in English
260723 1600 · created: the three tiers, the thresholds, and the routing modes were brought in from `ref/ref-cascade.md` and the face was marked ✅ settled
