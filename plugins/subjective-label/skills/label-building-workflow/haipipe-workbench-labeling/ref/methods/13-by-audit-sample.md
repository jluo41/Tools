By audit sample
===============

One labeling method card. Guide › Method shows it among its step's cards; its papers are
the rows of `../labeling-papers.md` whose `group` is `by audit sample`. A claim names its
source in brackets; "(ours)" marks the workbench's own judgment.

family: Steps 5 and 6 · Check and deliver: is it right, and what is released
move: Before release, the person labels a blind random sample of the final labels, and
  their agreement decides the release.
comes from: Artstein 2008, agreement measures
reads: the candidate final labels
returns: the audit's agreement and the release decision
test now: T5 audit
test in use: T5 audit


What the literature says
------------------------

rationale: Agreement between independent codings, measured with chance-corrected
  coefficients, shows whether labels are reliable [Artstein 2008].
context: Inter-coder agreement in computational linguistics [Artstein 2008].
steps: 1. Draw a random sample. 2. The person labels it blind. 3. Measure agreement
  against the release rule.
strengths: Catches what routing missed: labels that were confidently wrong (ours).
limitations: A small sample bounds agreement only loosely (ours).


Applied to AI
-------------

agent: sampler-agent draws; moderator-agent runs it; validator-agent analyzes
steps: 1. Draw from the frozen audit design. 2. Label blind. 3. Analyze.
returns: the audit receipt
verify: the person did not see the candidate label first (T1)
risk: An audit drawn only from easy items flatters the release (ours).
evidence on ai: No study tests this audit with model-labeled corpora (ours).
skill: subjective-label-audit
