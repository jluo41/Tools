Reference: Public Validation Datasets
======================================

Datasets used by the Validator to benchmark the agent panel against
real human annotations. Pick the one closest to your project topic.


Mapping: topic → recommended dataset
-------------------------------------

| If your project topic is …         | Recommended dataset | Reason                                   |
|------------------------------------|---------------------|------------------------------------------|
| Emotion, sentiment intensity       | GoEmotions          | 27 fine-grained emotions, high volume    |
| Moral framing, values, ethics      | MFTC                | Moral Foundations Theory                 |
| "Humanity" / empathy / vulnerability | MFTC + GoEmotions | Neither is exact; use both, project labels |
| Stance, opinion, persuasion        | POPQuorn            | Per-annotator labels, multiple tasks     |
| Harm / safety / toxicity           | DICES               | Multi-perspective, includes demographics |
| Anything else                      | custom              | Researcher supplies held-out labeled set |


GoEmotions
----------

- Paper: Demszky et al. 2020, "GoEmotions: A Dataset of Fine-Grained Emotions"
- HF path: `go_emotions`
- Size: 58K Reddit comments
- Labels: 27 emotions + neutral (multi-label)
- Annotators: 3-5 per item
- Published human κ ceiling: ~0.46 (Cohen's κ pairwise average)
- Available splits: train / validation / test
- Recommended use: emotion-adjacent projects

Label-projection examples:
```yaml
humanity_mapping:
  high:   [love, gratitude, admiration, pride, caring, joy]
  medium: [neutral, realization, curiosity, approval]
  low:    [anger, disgust, disappointment, annoyance, sadness]
```


MFTC — Moral Foundations Twitter Corpus
----------------------------------------

- Paper: Hoover et al. 2020, "Moral Foundations Twitter Corpus"
- HF path: `mftc` (or download from authors if HF version incomplete)
- Size: 35K tweets
- Labels: 10 moral foundations (care/harm, fairness/cheating, loyalty/betrayal, authority/subversion, sanctity/degradation)
- Annotators: 3 trained annotators per item
- Published human κ ceiling: ~0.6 (Krippendorff's α reported)
- Recommended use: moral/ethical-adjacent projects; also best proxy for "humanity" dimensions


POPQuorn
--------

- Paper: Pei & Jurgens 2023, "When Do Annotator Demographics Matter?"
- HF path: `pqa` or download from authors
- Tasks: offensiveness, politeness, question-answering quality
- Annotators: 13-22 per item with demographic metadata
- Published κ: varies by task, typically 0.3-0.6
- Available: per-annotator labels (not just aggregate!) — great for Krippendorff's α
- Recommended use: tasks where annotator demographics matter; perspectivism


DICES
-----

- Paper: Aroyo et al. 2023, "DICES Dataset: Diversity in Conversational AI Evaluation for Safety"
- HF path: `dices`
- Size: ~1M annotations on conversational AI turns
- Labels: safety (bias, harm, misinfo, content)
- Annotators: diverse demographics (gender, age, ethnicity)
- Published κ: low (multi-perspective intentional) — use for studying disagreement itself
- Recommended use: safety-adjacent or when disagreement modeling matters


Custom
------

If none of the public datasets are close enough, supply your own:

- File: `{project_dir}/validation/custom_heldout.jsonl`
- Schema: `{"id": "...", "text": "...", "labels": ["...", "..."]}` — labels is an array of per-annotator labels (preferred) or a single majority label
- Metadata: `{project_dir}/validation/custom_heldout_meta.yaml`:
  ```yaml
  n_annotators: 5
  annotator_agreement_kappa: 0.55  # your own measurement
  source: "internal study 2026-Q1"
  label_values: [high, medium, low]
  ```


Cache
-----

Datasets are cached at `{project_dir}/validation/_cache/{dataset}/`.
First fetch requires network + HuggingFace authentication if dataset is gated.
Subsequent runs read from cache.


Cost note
---------

Validation runs the full Labeler Panel on N items (default 200). With 5
personas × Sonnet tier, expect ~$1-3 per validation run. Cache the panel
outputs — re-running the same held-out set should not re-call the panel
unless gallery has changed.


Registry & autonomy-license battery (S6)
-----------------------------------------

These datasets serve as the **autonomy-license battery** (see
note-update.md Part 4): run the whole engine on them, on
their NATIVE construct, and assert engine κ ≥ human ceiling via `lib/license.py`.
Passing licenses autonomous runs on new constructs adjacent to the battery.
Artifact-verified per-rater status from `discoveries/P02_external-validation-datasets`:

| dataset | native construct | per-rater? | access | notes |
|---------|------------------|-----------|--------|-------|
| **DICES** | conversational safety | ✅ 123 raters/item (350 split) | github `google-research-datasets/dices-dataset` | strongest ceiling; +rater demographics |
| **POPQuorn** | offensiveness · politeness | ✅ per-rater + demographics | github `Jiaxin-Pei/potato-prolific-dataset` | closest to short-text subjective; use `raw` splits |
| **GoEmotions** | emotion | ✅ 211k per-rater | **canonical Google CSVs** (HF mirror lossy) | `config="raw"`; largest, most familiar |
| **LeWiDi** | HS/abuse (4 corpora) | ✅ + distribution-scoring protocol | SemEval-2023 Task 11 | adopt its "score vs rating distribution" protocol |
| MFTC | moral sentiment | labels-yes / **text-NO** | — | DEMOTED: text unrecoverable (dead Twitter API) |

**registry-match**: for a new construct, match to the construct-ADJACENT sets
here (never assume one exists — skip cleanly if none). Coverage/adjacency is
reported, not assumed; the battery's diversity = the width of the autonomy license.

**Flow**: run engine on a battery dataset → project its native labels to the
construct's schema → `lib/license.py assess --agent ... --raters ...` → PASS/BELOW.
