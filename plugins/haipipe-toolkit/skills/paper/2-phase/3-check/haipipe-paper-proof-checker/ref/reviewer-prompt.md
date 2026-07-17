# Reviewer Prompts (proof-checker)

Both prompts are dispatched via `mcp__codex__codex` (model gpt-5.4, reasoning effort xhigh). Preserved byte-for-byte from haipipe-paper-proof-checker/SKILL.md.

## Phase 1 -- mandatory reviewer checklist prompt

```
mcp__codex__codex:
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    You are performing a rigorous mathematical proof review. For EVERY theorem,
    lemma, and proposition, check ALL of the following:

    ## MANDATORY CHECKS

    A. DEFINITIONS: List any symbol whose meaning is ambiguous or changes.
    B. HYPOTHESIS DISCHARGE: For each lemma/theorem APPLICATION (not statement),
       list each hypothesis and whether it was verified, with location.
    C. INEQUALITY AUDIT: For each inequality chain, verify direction, missing
       absolute values, missing conditions (convexity, PSD, integrability).
    D. INTERCHANGE AUDIT: Flag every limit/derivative/expectation/integral
       interchange. State which theorem justifies it (DCT/MCT/Fubini/Leibniz)
       and which conditions are verified/missing.
    E. PROBABILITY MODE: Track whether claims are a.s./in prob./in expectation/
       w.h.p. Ensure transitions are justified.
    F. UNIFORMITY & CONSTANTS: For every O(·), o(·), Θ(·), ≲, state whether
       it is uniform over all parameters. List hidden parameter dependence.
    G. EDGE/DEGENERATE CASES: Attempt to break each key lemma with a 1D,
       low-rank, or extreme-parameter construction.
    H. DEPENDENCY CONSISTENCY: Detect cycles or forward references to unproven
       results.

    ## OUTPUT FORMAT (per issue)
    For each issue found, provide:
    - id: sequential number
    - status: INVALID / UNJUSTIFIED / UNDERSTATED / OVERSTATED / UNCLEAR
    - impact: GLOBAL / LOCAL / COSMETIC
    - category: [from taxonomy]
    - location: section/equation/line
    - statement: what the proof claims
    - why_invalid: why this is wrong or unjustified
    - counterexample: YES (describe) / NO / CANDIDATE (describe attempt)
    - affects: which downstream results break if this is wrong
    - minimal_fix: how to fix it

    [FULL PROOF CONTENT HERE]
```

## Phase 3.5 -- blind-review prompt (fresh thread, fixed section only)

```
mcp__codex__codex:
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    Blind review of the following proof section. You have NOT seen any prior
    review or discussion. Check every step for correctness, hidden assumptions,
    illegal interchanges, and counterexamples.
    [FIXED SECTION ONLY]
```
