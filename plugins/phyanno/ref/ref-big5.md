# Reference: Big Five Scoring Rubric

You are an expert psychologist annotating physician personality traits from patient reviews.
The reviews describe how a physician behaved with patients — you infer personality from behavior.

---

## The Five Traits

### Openness
Receptiveness to new ideas, curiosity, creativity, flexibility in thinking.
**In physician context:** tries new treatments, explains options, tailors care to the individual,
asks questions, engages with patient's unique situation rather than following rigid protocols.

### Conscientiousness
Self-discipline, responsibility, thoroughness, reliability, attention to detail.
**In physician context:** follows up, runs complete exams, explains plans clearly, keeps
appointments on time, returns calls, careful about medication details and test results.

### Extraversion
Energy in social interaction, warmth, talkativeness, confidence, expressiveness.
**In physician context:** warm bedside manner, initiates conversation, puts patients at ease,
expressive, engaging, makes patients feel heard and welcomed.

### Agreeableness
Cooperation, empathy, compassion, trust, willingness to help others.
**In physician context:** listens carefully, validates patient concerns, never dismissive, patient
and gentle, takes patient preferences seriously, treats patients with respect and kindness.

### Neuroticism
Tendency toward negative emotions, stress reactivity, anxiety, irritability.
**In physician context:** appears rushed or stressed, dismisses concerns, shows frustration
with questions, cold demeanor, makes patients feel judged or anxious, poor bedside manner.

---

## Score Scale (integer, stored as human_annotations.score)

| Value | Label | Meaning |
|-------|-------|---------|
| 1 | Low | Minimal or weak evidence of this trait |
| 2 | Low to Moderate | Some evidence, but limited or inconsistent |
| 3 | Moderate | Clear evidence across a few reviews |
| 4 | Moderate to High | Strong, recurring evidence across many reviews |
| 5 | High | Dominant, compelling evidence throughout |

**If there is truly no evidence for a trait:** use score=1 (Low) and state in evidence:
"No direct evidence found in the available reviews."

**Do not invent evidence.** If reviews are too few or too vague, score=1 or score=2
with an honest evidence statement.

---

## Consistency Scale (integer, stored as human_annotations.consistency)

How consistently does the trait appear across multiple reviews?

| Value | Label | Meaning |
|-------|-------|---------|
| 1 | Low | Mentioned in 1 review, or contradicted by other reviews |
| 2 | Moderate | Mentioned in 2–3 reviews, some consistency |
| 3 | High | Mentioned across many reviews without contradiction |

---

## Sufficiency Scale (integer, stored as human_annotations.sufficiency)

How strong and specific is the supporting evidence?

| Value | Label | Meaning |
|-------|-------|---------|
| 1 | Low | Vague impressions, indirect inference only |
| 2 | Moderate | Some specific examples or quotes, but limited |
| 3 | High | Multiple specific, detailed, concrete examples |

---

## Evidence Writing Guidelines

Write 2–3 sentences that:
1. State your reasoning (why this score for this trait)
2. Include at least one direct quote OR paraphrased example from the reviews
3. Note if evidence was absent, weak, or contradictory

**Good example (Agreeableness, score=4):**
"Multiple reviewers describe Dr. Smith as deeply empathetic and patient. One wrote 'she
actually listened to every concern without rushing me' and another noted 'he never made me
feel stupid for asking questions.' Across 8 reviews, only one described a dismissive interaction."

**Poor example (avoid):**
"The doctor seems agreeable based on reviews." ← too vague, no quotes, no reasoning

---

## Machine Annotation Rating Guide (Stage 2)

When rating each LLM model's annotation, use:

| Rating | When to use |
|--------|------------|
| `thumb_up` | Score is appropriate, evidence is specific and correctly quoted, consistency and sufficiency ratings make sense |
| `just_soso` | Score is close but slightly off, OR evidence is correct but vague, OR minor rating disagreement |
| `thumb_down` | Score is clearly wrong, evidence is fabricated or misattributed, or major disagreement on the trait direction |

Your comment should explain the key reason in one sentence.

---

## Stage 3 Revision Threshold

Revise your Stage 1 score (submit with `submission_type: "review"`) only if:
- A model you rated `thumb_up` differs from your score by 2+ points, AND
- Its evidence cites specific quotes you may have underweighted

Do not revise for minor differences (±1 point) or when your evidence is stronger.
