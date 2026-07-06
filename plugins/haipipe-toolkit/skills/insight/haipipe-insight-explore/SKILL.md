---
name: haipipe-insight-explore
description: "Coverage / gap scanner of the haipipe-insight family (the KB dashboard). Reads the project's insights/ cards plus the discoveries/ and tasks/ material folders; reports what each named dataset already has (D profile, I pattern), which I patterns could support a K (generalization + confidence), which K imply an action but have no W, and which settled material was never reviewed. NO code execution, read-only. Runs as the no-args dashboard behind /haipipe-insight, or standalone. Trigger: explore, scan, coverage, what can we synthesize, what's missing, /haipipe-insight-explore."
argument-hint: "[--project <path>] [--out]"
allowed-tools: Bash, Read, Grep, Glob, Skill
metadata:
  version: "2.0.0"
  last_updated: "2026-07-05"
  summary: "Coverage / gap scanner of the haipipe-insight family."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-insight-explore
================================

The **coverage scanner** for insight, recut to the in-sample vs generalization
model (D/I describe one named dataset; K generalizes with confidence +
claim_type; W acts on K). It answers four questions:

```
per dataset      does it have a D profile? an I pattern stated inside it?
per I pattern    is a K on file saying whether it generalizes (any confidence)?
per K claim      does it imply an action, and is a W on file for it?
per material     which settled discoveries / task results were never reviewed?
```

Read-only. Writes one transient summary to stdout; `--out` additionally writes
`insights/coverage.md` (transient, overwritten each run).


Workflow
--------

```
Step 1: Resolve project root (--project or cwd-inferred)

Step 2: Scan insights/ (frontmatter only)
  - Glob insights/{D_data,I_information,K_knowledge,W_wisdom}/*.md
  - Per card collect: id, layer, dataset (D/I), claim + confidence + claim_type (K),
    rec (W), status, sources, ref_by
  - Build the chain per dataset: D → I (same `dataset:`) → K (cites the I) → W (cites the K)

Step 3: Scan material folders (read-only, shallow)
  - tasks/**/results/<run>/            → settled task runs (metrics.json present)
  - discoveries/*/discovery.yaml       → reviewed external claims (if the dir exists)
  - Cross-reference: which settled material is cited by NO card (`sources` and
    D `source_id` carry the namespaced refs)

Step 4: Compute gaps (the DIKW chain, no admission gates)
  - dataset has D but no I               → "pattern not yet stated"
  - I has a stated basis but no K        → "generalization not yet recorded
                                            (file K at ANY confidence; negative
                                            and low-confidence K count)"
  - K implies an action, no W cites it   → "action not yet recorded (a low or
                                            negative K still tunes a conservative W)"
  - K with status contested/stale        → "needs review"
  - settled material cited by no card    → "never reviewed: candidate scope for
                                            /haipipe-insight review"

Step 5: Emit summary (stdout); with --out also write insights/coverage.md
```


Output schema (stdout; `--out` mirrors to insights/coverage.md)
----------------------------------------------------------------

```markdown
# Insight Base Coverage — <project>

## Chain per dataset

| Dataset                  | D    | I    | K (confidence, type)      | W    |
|--------------------------|------|------|---------------------------|------|
| VisitOsteo_1stPair_af14d | D01  | I01  | K01 (medium, assoc.)      | W01  |
| VisitLBP_1stPair_bd02c   | D02  | —    | —                         | —    |

## Unreviewed settled material

- discoveries/P01_rx/02_agreeableness-metformin (status: ok): cited by no card
- tasks/D01_reg/03_lbp_visit results/v0618: cited by no card

## Gaps (next moves)

- D02 has no I: /haipipe-insight information --dataset VisitLBP_1stPair_bd02c --scope D02
- I01 basis unrecorded beyond K01 scope: consider a per-population K
- K01 has no W: /haipipe-insight wisdom --scope K01
- unreviewed discovery: /haipipe-insight review examples/<project>/discoveries/P01_rx/02_agreeableness-metformin
```


Hard rules
----------

- READ-ONLY on cards and material. Never writes to D/I/K/W folders, discoveries/, tasks/.
- The only write is `insights/coverage.md`, and only when `--out` is passed
  (transient, overwritten on each run).
- Counts and links MUST reflect actual files on disk (no caching).
- No admission gates: a probe does NOT need any particular verdict for its
  material to be reviewable, and an I needs no p-value to deserve a K entry;
  K records generalization at WHATEVER confidence the basis supports
  (negative and low-confidence K are first-class, see
  `../ref/dikw-boundaries.md` "Negative and uncertain K").


Risk profile
-------------

Read-only on `tasks/`, `discoveries/`, and `insights/` cards. May
write `insights/coverage.md` when `--out` is passed. Does NOT modify D/I/K/W
entries.


Specialist tail
---------------

```
status:    ok | blocked | failed
summary:   "4 datasets: 2 full chains, 1 missing I, 1 missing K; 2 settled discoveries unreviewed"
artifacts: [stdout summary, insights/coverage.md (only with --out)]
next:      Pick a gap to close: /haipipe-insight review <scope> |
           /haipipe-insight information --dataset <name> |
           /haipipe-insight wisdom --scope K<NN>
```
