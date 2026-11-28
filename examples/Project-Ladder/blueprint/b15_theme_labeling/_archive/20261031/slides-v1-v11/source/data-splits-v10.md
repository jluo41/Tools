Train and Test in the two loops
==============================

Version 10 follows the user's two-partition design. A separate validation partition is not required for this version. Train means data used to develop the guideline, not data used to update model weights.

| Route | Train / learning | Test |
| --- | --- | --- |
| Meaning development | Explore cases with the human, decide rules and exceptions, reconcile contradictions, and confirm reference labels. | No case content or judgments return to rule development. During the Meaning Loop, a separate labeling route applies the current guideline and records versioned reference judgments. |
| Expression development | Call executor models, inspect errors against approved reference labels, revise expression while preserving meaning, and choose a candidate. | Apply the frozen candidate and score its predictions against protected references for independent assessment. |

Both sets receive labels. Test inputs are visible to the executor assigned to label them; reference answers stay with the scorer. Test content, references and item-level errors do not enter the guideline developer's context, retrieval or reports. Calling both roles "AI" does not remove this access boundary.

Reference labels and executor predictions are different artifacts. Human review during the Meaning Loop establishes versioned reference labels under the current standard. Train-driven changes to meaning trigger re-review of affected Test labels; Test cases cannot be the reason for changing the rule. Final Test references must match the final frozen meaning and be locked before candidate predictions are inspected. A rule approval does not automatically approve every item prediction. Uncertain or unresolved cases retain their review status and must not silently disappear from the evaluation denominator.

Candidate expression, executor settings, metrics and thresholds are fixed before Test. Training-set scores support development but are not independent evidence of generalization. Final Test can compare several prespecified executors under the same frozen guideline; choosing a deployment model after inspecting those results makes that choice exploratory, rather than independently tested. If Test findings guide another guideline revision, that set becomes development evidence and a fresh independent test is needed for the next generalization claim.

Slide changes
-------------

Pages 6, 7, 12, 13, 17 and 19 are replaced. Page 21 separates guideline development from labeling during the Meaning Loop, then states that expression development uses only Train references and routes Test references to final assessment. The other fourteen slides and their notes remain unchanged. The full PDF and PowerPoint have 21 pages; the seven-page excerpt contains the changed pages. Static Workbench mockups use synthetic examples and unrun placeholders.

Build from deck-content-v10.json and imagegen assets using build-v10.mjs, then inspect the rendered pages and run release-v10.py. The release validates slide images and unchanged notes using direct byte comparisons. Earlier versions are historical and retain their original design.
