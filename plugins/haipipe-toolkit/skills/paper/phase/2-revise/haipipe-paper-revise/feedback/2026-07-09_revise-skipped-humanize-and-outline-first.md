---
status: fixed
created: 2026-07-09
updated: 2026-07-09
occurrences: 1
context: section-edit §4-llmtrait / Paper-Personality2Opioid-MISQ2026
fixed_in: "haipipe-paper-revise 1.5.0 + haipipe-paper-section-edit 4.0.0 + haipipe-paper-draft 3.7.0 + haipipe-paper-check 1.8.0 (2026-07-09 normalization)"
regressed: ""
---
"the revise phase didn't really work." (JL, 2026-07-09)

Earlier in the same session, before the redo request: "I think the revise is really bad, it doesnt function, some sentence is so so long, why you don't fix them? and also did you detect the AI-ish sentences? Please redo the revise."

## Context (observed this session, §4-llmtrait REVISE)

The REVISE ran as a narrow inline content edit and skipped the phase's core jobs:

- **No sentence-splitting.** Long multi-clause sentences shipped unfixed (P2.S1 ~50 words, P2.S2 ~45 words, P3.S4 ~40 words). JL had to hand-flag "this is too long" three times in the outline before they were split.
- **No de-AI / humanizer pass.** AI gerund-tails survived ("ensuring that", "reducing concerns", "indicating that", "enabling ... and ensuring"); the formulaic "First / Second / Third / Fourth" block in P7 survived. JL: "did you detect the AI-ish sentences?" — no, the pass never ran.
- **Revise workers never dispatched.** `haipipe-paper-revise-humanizer` (de-AI) and `haipipe-paper-revise-content` were not invoked. The section-edit hub hand-edited the prose itself instead of routing to the 2-revise workers.
- **Outline-first violated.** The tex was edited directly; the outline `.md` (the primary working doc JL reads and comments in) went stale, so JL was reviewing the OLD long sentences while the tex already differed.
- **Comment-first skipped on the first pass.** Changes were applied (and committed) before any `%% {CC-...}` review comments were inserted for eyeball. JL had to ask for comments separately.

## Suggested fix direction (for a later revision pass, NOT now)

The revise phase (and section-edit's REVISE step that drives it) should:
1. Edit the outline `.md` FIRST, then sync to tex — never tex-first (the outline is the doc the human reads/comments).
2. Actually DISPATCH the 2-revise workers (`-humanizer` for de-AI, `-content` for what-it-says) instead of hand-editing.
3. Run the humanizer as a MANDATORY sub-step, with a hard checklist from PREFERENCES.md: split long/multi-clause sentences into short complete sentences; no semicolons/em-dashes; no gerund-tails; no rigid "First/Second/Third/Fourth" enumerations.
4. Insert comment-first `%% {CC-...}` annotations BEFORE applying, so the human eyeballs before anything is baked in/committed.

## Cross-refs
- `haipipe-paper-revise-humanizer` — the de-AI pass that was never run.
- `haipipe-paper-section-edit` — owns the REVISE orchestration (outline-first + worker dispatch + comment-first) that was bypassed.
