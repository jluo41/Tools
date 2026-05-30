---
name: haipipe-insight-explore
description: "Coverage / readability scanner of the haipipe-insight family. Reads the project's probes/ and existing insights/ folders; reports which probes are CONFIRMED and ready for synthesis, what's already in the insight base, and which gaps a session could close. NO code execution. Use to plan the next /haipipe-application ask, or as a standalone read-only audit. Trigger: explore, scan, coverage, what can we synthesize, what's missing, /haipipe-insight-explore."
argument-hint: "[--project <path>]"
allowed-tools: Bash, Read, Grep, Glob, Skill
---

Skill: haipipe-insight-explore
================================

The **coverage scanner** for E_insight. Maps:

```
probes/           which ones are confirmed and ready to feed observations?
insights/D_data/   which probes already have D entries?
insights/I_information/       which observations already feed a pattern?
insights/K_knowledge/      which patterns elevated to knowledge?
insights/W_wisdom/         which knowledge prompted action items?
```

Read-only. Writes one transient summary to stdout (and optionally
`insights/coverage.md`).


Workflow
--------

```
Step 1: Resolve project root (--project or cwd-inferred)

Step 2: Scan probes/
  - For each probes/<NN>_<slug>/probe.yaml:
    - status = result.status (pending | confirmed | inconclusive | refuted | exploratory)
    - has CLAIMS_FROM_RESULTS.md? has INTEGRITY_AUDIT.md?
    - bucketize: ready_for_synthesis (confirmed) | not_ready | failed

Step 3: Scan insights/
  - For each layer (D / I / K / W):
    - List entries (D*.md, I*.md, K*.md, W*.md)
    - Read each entry's source_experiment / scoped fields
  - Build cross-reference:
    - which probes already produced D entries
    - which D entries feed I entries
    - which I entries feed K entries
    - which K entries spawned W entries

Step 4: Compute gaps
  - probes confirmed but no D entry yet      → "ready for observations"
  - D entries without a P link                     → "candidate pattern source"
  - I entries without a K link                     → "candidate knowledge source"
  - K entries without a W link                     → "candidate action source"
  - K entries with conflicting evidence            → "needs review"

Step 5: Emit summary (stdout) + optionally write insights/coverage.md
```


Output schema (stdout + optional insights/coverage.md)
-------------------------------------------------------

```markdown
# Insight Base Coverage — <project>

Scanned at: <ISO>

## Probes

| ID | Slug              | Status       | D entry?  | Notes               |
|----|-------------------|--------------|-----------|---------------------|
| 02 | lhm_vs_baseline   | confirmed    | D01       | -                   |
| 04 | film_test_id      | confirmed    | (none)    | READY FOR SYNTHESIS |
| 07 | param_matched     | inconclusive | (none)    | not ready           |
| 12 | lhm_retest        | pending      | (none)    | runs in progress    |

## Insight base summary

- D_data:  3 entries (D01, D02, D03)
- I_information:      2 entries (I01, I02)
- K_knowledge:     1 entry  (K01)
- W_wisdom:        0 entries

## Gaps (synthesis opportunities)

- probe 04 (confirmed) → no D entry yet
- D02 not yet referenced by any I entry
- I02 references D01, D02 but no K entry has elevated it
- K01 has no W entry yet

## Suggested next moves

- `/haipipe-insight-data 04`        (write D entry for confirmed probe 04)
- `/haipipe-insight-information --scope D02,D03`  (extract pattern from these)
- `/haipipe-insight-knowledge --scope I02`        (elevate I02 → knowledge)
```


Hard rules
----------

- READ-ONLY. Never writes to D/I/K/W folders.
- Only optional write is `insights/coverage.md` (transient, overwritten
  on each run).
- Counts and links MUST reflect actual files on disk (no caching).


Risk profile
-------------

Read-only on `probes/` and `insights/`. May write
`insights/coverage.md`. Does NOT modify D/I/K/W entries.


Specialist tail
---------------

```
status:    ok | blocked | failed
summary:   "3 probes confirmed, 2 still need D entries; 1 P→K elevation pending"
artifacts: [stdout summary, insights/coverage.md (if --out)]
next:      Pick a gap to close: /haipipe-insight-data <ID> | /haipipe-insight-information ...
```
