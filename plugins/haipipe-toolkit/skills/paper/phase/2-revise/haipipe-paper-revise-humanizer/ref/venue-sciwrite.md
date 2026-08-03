# Venue-grounded, meaning-preserving revision

Use this reference for every humanizer audit. Use candidate-diff mode only when the author explicitly asks to retain the original sentence and review annotated alternatives.

## Resolve the writing contract first

1. Read the owning S page's `## Stage Contract`.
2. Read its `style-from` writing contract and the pinned venue page.
3. Read a venue section guide only through its declared source or when the S page is absent.
4. Treat examples as **move shapes, not reusable wording**.

The venue contract decides the paragraph's job, claim hierarchy, allowed causal language, reader, and section-specific conventions. It overrides a generic clarity preference.

## Four gates for every proposed edit

### 1. Meaning invariance

Do not add, remove, broaden, narrow, or reorder a claim. Do not change causal strength, a qualifier, a core construct, a number, a citation, a display reference, or an author comment. Preserve defined terms exactly; do not substitute a synonym merely to avoid repetition.

### 2. Venue and paragraph fit

Confirm that the proposal still performs the sentence's assigned paragraph job and serves the venue-facing story. Keep the paper's claim hierarchy intact. For MISQ, preserve theory-forward mechanism language and calibrated associational wording; do not turn an IS contribution into generic clinical stakes or a method pitch.

### 3. SciWrite clarity

Apply only these sentence-level checks:

- Cut dead-weight openings, redundant modifiers, and repeated information.
- Prefer a direct verb when a nominalization obscures the action.
- Repair a buried predicate or a clause stack only when the sentence remains one complete idea.
- Preserve a passive construction when the actor is irrelevant, a conventional method form, or the object is the intended emphasis.
- Keep technical terms and variable names identical across the manuscript.

The numerical/citation-integrity pass is a CHECK responsibility. It may flag a conflict but never rewrites a value, key, unit, or citation placement.

### 4. Human academic voice

Remove inflated framing, empty intensifiers, formulaic openers, connective ladders, novelty padding, unsupported significance language, and vague hedging. Keep evidence-tied hedging, authorial `we`, passive voice where warranted, equations, citations, and precise technical vocabulary.

## Candidate-diff output

In explicit original-preserving review mode:

```markdown
Original sentence remains unchanged.
> Note: Complete candidate with ~~removed text~~ and **inserted text**. · <verified model label> · YYYY-MM-DD
```

Write the whole candidate sentence, not an isolated replacement fragment. Use the smallest viable edit. Place the Note in the source `.md` beneath its existing evidence lanes, so the Board folds it under the original sentence. Never copy the Note into TeX or call it an applied revision.

## Decision test

Propose an edit only when all answers are yes:

1. Does it preserve every scientific and argumentative commitment?
2. Does it make the sentence shorter, clearer, or more direct for this venue?
3. Does it retain every protected term and evidence pointer?
4. Can a coauthor reconstruct both the original and the candidate from the one Note line?

Otherwise, leave the sentence unchanged.
