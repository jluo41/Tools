---
name: haipipe-insight-explore
description: "Coverage / readability scanner of the haipipe-insight family. Reads the project's experiments/ and existing insights/ folders; reports which experiments are CONFIRMED and ready for synthesis, what's already in the insight base, and which gaps a session could close. NO code execution. Use to plan the next /haipipe-insight-session, or as a standalone read-only audit. Trigger: explore, scan, coverage, what can we synthesize, what's missing, /haipipe-insight-explore."
argument-hint: [--project <path>]
allowed-tools: Bash, Read, Grep, Glob, Skill
---

Skill: haipipe-insight-explore
================================

The **coverage scanner** for E_insight. Maps:

```
experiments/           which ones are confirmed and ready to feed observations?
insights/D_observations/   which experiments already have O entries?
insights/I_patterns/       which observations already feed a pattern?
insights/K_knowledge/      which patterns elevated to knowledge?
insights/W_wisdom/         which knowledge prompted action items?
```

Read-only. Writes one transient summary to stdout (and optionally
`insights/coverage.md`).


Workflow
--------

```
Step 1: Resolve project root (--project or cwd-inferred)

Step 2: Scan experiments/
  - For each experiments/<NN>_<slug>/experiment.yaml:
    - status = result.status (pending | confirmed | inconclusive | refuted | exploratory)
    - has CLAIMS_FROM_RESULTS.md? has INTEGRITY_AUDIT.md?
    - bucketize: ready_for_synthesis (confirmed) | not_ready | failed

Step 3: Scan insights/
  - For each layer (D / I / K / W):
    - List entries (O*.md, P*.md, K*.md, W*.md)
    - Read each entry's source_experiment / scoped fields
  - Build cross-reference:
    - which experiments already produced O entries
    - which O entries feed P entries
    - which P entries feed K entries
    - which K entries spawned W entries

Step 4: Compute gaps
  - experiments confirmed but no O entry yet      → "ready for observations"
  - O entries without a P link                     → "candidate pattern source"
  - P entries without a K link                     → "candidate knowledge source"
  - K entries without a W link                     → "candidate action source"
  - K entries with conflicting evidence            → "needs review"

Step 5: Emit summary (stdout) + optionally write insights/coverage.md
```


Output schema (stdout + optional insights/coverage.md)
-------------------------------------------------------

```markdown
# Insight Base Coverage — <project>

Scanned at: <ISO>

## Experiments

| ID | Slug              | Status       | O entry?  | Notes               |
|----|-------------------|--------------|-----------|---------------------|
| 02 | lhm_vs_baseline   | confirmed    | O01       | -                   |
| 04 | film_test_id      | confirmed    | (none)    | READY FOR SYNTHESIS |
| 07 | param_matched     | inconclusive | (none)    | not ready           |
| 12 | lhm_retest        | pending      | (none)    | runs in progress    |

## Insight base summary

- D_observations:  3 entries (O01, O02, O03)
- I_patterns:      2 entries (P01, P02)
- K_knowledge:     1 entry  (K01)
- W_wisdom:        0 entries

## Gaps (synthesis opportunities)

- experiment 04 (confirmed) → no O entry yet
- O02 not yet referenced by any P entry
- P02 references O01, O02 but no K entry has elevated it
- K01 has no W entry yet

## Suggested next moves

- `/haipipe-insight-data 04`        (write O entry for confirmed experiment 04)
- `/haipipe-insight-information --scope O02,O03`  (extract pattern from these)
- `/haipipe-insight-knowledge --scope P02`        (elevate P02 → knowledge)
```


Hard rules
----------

- READ-ONLY. Never writes to D/I/K/W folders.
- Only optional write is `insights/coverage.md` (transient, overwritten
  on each run).
- Counts and links MUST reflect actual files on disk (no caching).


Risk profile
-------------

Read-only on `experiments/` and `insights/`. May write
`insights/coverage.md`. Does NOT modify D/I/K/W entries.


Specialist tail
---------------

```
status:    ok | blocked | failed
summary:   "3 experiments confirmed, 2 still need O entries; 1 P→K elevation pending"
artifacts: [stdout summary, insights/coverage.md (if --out)]
next:      Pick a gap to close: /haipipe-insight-data <ID> | /haipipe-insight-information ...
```
