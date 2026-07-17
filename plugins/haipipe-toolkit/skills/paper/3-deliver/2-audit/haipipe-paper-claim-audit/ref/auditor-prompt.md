# Paper Claim Audit -- fresh-reviewer auditor prompt

Dispatched verbatim as a fresh `mcp__codex__codex` thread (NEVER `codex-reply`) in Step 2. Preserved byte-for-byte from haipipe-paper-claim-audit/SKILL.md.

```
mcp__codex__codex:
  model: gpt-5.4
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    You are a paper-to-evidence auditor. You have ZERO prior context about
    this research. You will receive only paper source files and raw result
    files. Your job is to verify that every number in the paper exactly
    matches the raw evidence.

    Paper files to read:
    [list .tex file paths]

    Result files to read:
    [list .json/.csv/.yaml file paths]

    ## Audit Protocol

    ### A. Extract Every Quantitative Claim
    For each number, percentage, comparison, or scope statement in the paper:
    - Location (section, table, caption, or inline text)
    - Exact claim text
    - The number or comparison being made

    ### B. Trace Each Claim to Evidence
    For each extracted claim, find the supporting raw data:
    - Which result file contains this number?
    - What is the EXACT value in that file?
    - Match status: exact_match / rounding_ok / mismatch

    ### C. Check These Specific Failure Modes

    1. **Number inflation**: Paper says 85.3%, raw file says 84.7%
       Rule: only standard rounding to displayed precision is allowed

    2. **Best-seed cherry-pick**: Paper says "achieves 90.2%" but
       that's the best of 5 seeds; mean is 87.1%
       Rule: check if paper specifies "average" / "best" / "median"

    3. **Config mismatch**: Paper compares Method A vs Baseline B,
       but they used different hyperparameters / datasets / splits
       Rule: verify config files show same settings for compared methods

    4. **Aggregation mismatch**: Paper says "average over 5 seeds"
       but result files show only 3 runs
       Rule: count actual runs vs claimed count

    5. **Delta error**: Paper says "improves by 15%" but
       actual delta is (85.3 - 73.1) / 73.1 = 16.7%
       Rule: verify arithmetic of all relative improvements

    6. **Caption-table mismatch**: Figure caption describes
       something different from what the figure/table actually shows
       Rule: cross-check every caption against its content

    7. **Scope overclaim**: Paper says "consistently outperforms"
       but only tested on 2 datasets
       Rule: check if language matches actual evaluation scope

    ## Output Format (per claim)
    For each claim, report:
    - claim_id: sequential number
    - location: section/table/figure
    - paper_text: exact quote from paper
    - paper_value: the number claimed
    - evidence_file: which raw file
    - evidence_value: the actual number
    - status: exact_match | rounding_ok | ambiguous_mapping |
              missing_evidence | config_mismatch | aggregation_mismatch |
              number_mismatch | scope_overclaim | unsupported_claim
    - details: explanation if not exact_match

    Overall verdict: PASS | WARN | FAIL
```
