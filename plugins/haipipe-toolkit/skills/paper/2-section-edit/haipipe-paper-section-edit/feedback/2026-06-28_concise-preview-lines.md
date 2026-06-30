---
status: fixed
created: 2026-06-28
updated: 2026-06-28
occurrences: 1
context: editing scaffold §7 discussion, JL flagged P3 preview as too long
fixed_in: "v2.1.0 (added preview length rule to outline spec: ONE SHORT LINE ~80-120 chars)"
regressed: ""
---

Parenthetical preview lines in the editing scaffold should be ONE SHORT LINE (~80-120 chars), not a mini-abstract restating every point in the paragraph. The preview is a scan hook, not a summary.

Bad (526 chars):
(Prior IS research treats online reviews primarily as satisfaction signals or reputation proxies; this study shows that review text encodes granular behavioral signals, perceived interpersonal traits, that predict specific clinical actions in independent data; this moves reviews from reputation infrastructure to behavioral data infrastructure; the distinction matters: satisfaction is evaluative, but perceived traits are descriptive of behavioral style and carry predictive validity for actions outside the review context.)

Good (110 chars):
(Reviews = behavioral data infrastructure, not just reputation; perceived traits carry predictive validity beyond ratings.)

Rule: preview = concept name + one distinguishing phrase. If it reads like a paragraph, compress it.
