# Reference: external datasets

Public or third-party labeled datasets are optional external-validity resources. They
do not define the project's subjective construct, replace project-specific human gold,
prove convergence, or license autonomous labeling of a new corpus.

## 1. Three distinct evidence sources

| evidence | population | construct | valid use |
|---|---|---|---|
| calibration gold `D_t` | project corpus | project construct | optimize and close `G_t` |
| sealed final test `T*` | held-out target population | frozen project construct | estimate candidate executor performance |
| external dataset | external population | native or mapped construct | probe portability and external validity |

Never merge these score series. A high score on an external dataset cannot rescue a
failed `T*` score, and a public human-agreement statistic is not the ceiling or target
for the current human's judgment.

## 2. When external validation is useful

Use an external dataset only when the study has a declared question such as:

- Does the guideline transfer to a related population?
- Which parts of the construct overlap a native public construct?
- Does executor ranking remain similar under domain shift?
- How does disagreement change across annotator populations?
- Which boundary rules fail outside the source corpus?

If no dataset is sufficiently adjacent, report that limitation and skip the analysis.
Do not force a label projection merely to produce a benchmark number.

## 3. Registry candidates

Potential registries include emotion, moral-language, stance, politeness, offensiveness,
safety, and perspectivist annotation datasets. Examples previously considered by this
plugin include GoEmotions, DICES, POPQuorn, LeWiDi, and MFTC.

Dataset availability, licensing, splits, schemas, and per-rater fields can change.
Verify them from primary documentation at execution time and record exact release,
checksum, license, access date, and transformation code. A name in this file is not a
claim that the resource is currently accessible or suitable.

## 4. Registration

Before running external validation, freeze:

```yaml
external_validation:
  id: external-01
  dataset: "provider/name"
  release: "..."
  checksum: "..."
  native_construct: "..."
  target_population: "..."
  mapping_version: "mapping-01"
  mapping_authors: ["..."]
  executor_policy: "G_star"
  metrics: ["..."]
  claims: ["..."]
```

Preserve native labels and per-rater judgments when available. Store projected labels as
derived fields with a mapping version; never overwrite the native annotation.

## 5. Mapping protocol

Any mapping from an external construct to H/L/N must be justified separately from the
project guideline. At minimum:

1. state overlap and non-overlap between constructs;
2. define treatment of unmappable and multi-label rows;
3. have the human semantic authority inspect a sample;
4. freeze the mapping before scoring;
5. report both native-task and mapped-task results where possible;
6. perform sensitivity analysis for plausible mappings.

An external projection must not add examples to `D_t`, `G*`, or `T*` unless the project
is formally reopened with a new scope and provenance.

## 6. Reporting

Report dataset and population differences, mapping assumptions, executor score with
intervals, subgroup results when supported, and examples of transfer failure. Label the
result `external` in every table and artifact.

Avoid claims such as “the engine exceeds the human ceiling” or “passes an autonomy
license.” The defensible claim is narrower: a registered executor achieved the stated
metric under a declared mapping on a particular external dataset.

## 7. Cache and privacy

Cache external data only when its license permits. Keep download receipts, checksums,
and transformation manifests. Apply the same privacy and access controls as the source
requires; public availability does not imply unrestricted redistribution.

## 8. Implementation boundary

Legacy validation utilities may assume public-data convergence or majority labels. They
are not valid substitutes for sealed project evaluation. Skills must keep external
validation optional and emit `HOLD` when the registered dataset, mapping, or metric
contract cannot be reproduced.
