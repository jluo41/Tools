---
name: narrative-report
description: "Generate NARRATIVE_REPORT.md — the design contract for /haipipe-paper. Reads upstream research artifacts (IDEA_REPORT, AUTO_REVIEW, CLAIMS_FROM_RESULTS, experiment results, repo source) and emits a single coherent narrative: problem statement, core claim, method, claim-evidence matrix, figure inventory, limitations. Use when transitioning from research/experiment phase to writing phase, or when the user says 'write narrative report', '生成 narrative', '/narrative-report'."
argument-hint: "[project-dir-or-topic]"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob
---

# Narrative Report Generator

The narrative report is **not** a draft of the paper. It is the **design contract**
that the paper writes from. Every claim, figure, and citation in the final PDF
should trace back to a line in this file. If something is not in the narrative,
the downstream pipeline (`/paper-plan → /paper-figure → /paper-write`) will not
invent it.

## Context: $ARGUMENTS

## When to Use

- Research / experiment phase is essentially done — results are in, story is
  approximately settled
- Before invoking `/haipipe-paper` or `/paper-plan` (they consume this file)
- After `/auto-review-loop` finishes, as the handoff to writing
- When the project has accumulated `IDEA_REPORT.md`, `AUTO_REVIEW.md`,
  experiment logs, and figures but no single document tells the story

Do **not** use when:
- Experiments are still running (the narrative would be premature)
- You only have a vague topic — use `/idea-discovery` or `/haipipe-experiment review claim` first
- A `NARRATIVE_REPORT.md` already exists and is current — edit it directly

## Inputs (in priority order)

The skill discovers whichever of these exist in the project tree:

1. **`CLAIMS_FROM_RESULTS.md`** (best) — validated claim ↔ evidence map from
   `/haipipe-experiment review claim`. If present, use as the spine of the narrative; every
   listed claim becomes a section in the report.
2. **`IDEA_REPORT.md`** — chosen idea, hypothesis, novelty justification (from
   `/idea-discovery`). Supplies the problem statement and intended contribution.
3. **`review-stage/AUTO_REVIEW.md`** (fall back to `./AUTO_REVIEW.md`) — review
   history, weaknesses fixed, remaining limitations (from `/auto-review-loop`).
   Supplies the limitations section and reframings.
4. **Experiment results** — JSON / CSV / TSV under `figures/`, `results/`,
   `outputs/`, `experiments/`. These are the raw evidence for every quantitative
   claim. Each number that ends up in the narrative must trace back to one of
   these files.
5. **`EXPERIMENT_LOG.md` / `experiment-log.txt`** — comparison-first experiment
   ledger. Useful for cross-experiment deltas and baseline-vs-method tables.
6. **Repo source** — for the method summary (what was actually built; not
   what was originally proposed). One short paragraph, not a code dump.

If multiple inputs disagree (e.g. `IDEA_REPORT` says "X improves Y by 5%" but
`CLAIMS_FROM_RESULTS` says "no improvement on test-od"), **trust the latest /
most data-grounded source** (CLAIMS_FROM_RESULTS > experiment files >
AUTO_REVIEW > IDEA_REPORT) and surface the discrepancy as a note in the report.

## Output: `NARRATIVE_REPORT.md`

The report must contain these five sections, in this order:

1. **Problem statement and core claim** — one-paragraph problem, one-sentence
   core claim. The core claim is the single sentence the paper exists to
   defend. Everything else supports it.
2. **Method summary** — what was built, at a level a reviewer can grasp in 30
   seconds. Not a manual; not an architecture deep-dive. Save the depth for
   `/paper-write`.
3. **Key quantitative results with evidence for each claim** — table or list
   with one row per claim:
   - claim (free text, declarative)
   - supporting experiment / dataset / metric
   - effect size + uncertainty
   - file path to the raw result (the future `/paper-claim-audit` will follow
     this trail)
4. **Figure / table inventory** — for each figure or table referenced in the
   above sections:
   - name, one-line caption
   - status: `auto` (data plot, generatable from results) / `manual` (needs
     drawing — architecture, qualitative) / `exists` (already in `figures/`)
   - data source path (for `auto`) or person responsible (for `manual`)
5. **Limitations and remaining follow-ups** — what the paper does **not**
   claim, what failed, what's deferred. Pulled mostly from `AUTO_REVIEW.md`'s
   "weaknesses not yet fixed" section. Be honest — this is what saves the
   paper from `/auto-paper-improvement-loop` round-2 hatchet jobs.

## Workflow

### Step 1: Discover inputs

```bash
ls CLAIMS_FROM_RESULTS.md IDEA_REPORT.md review-stage/AUTO_REVIEW.md AUTO_REVIEW.md EXPERIMENT_LOG.md experiment-log.txt 2>/dev/null
find results outputs experiments figures -maxdepth 3 -type f \
    \( -name '*.json' -o -name '*.csv' -o -name '*.tsv' -o -name '*.jsonl' \) 2>/dev/null | head -50
```

Report what was found vs missing. If `CLAIMS_FROM_RESULTS.md` is missing,
suggest running `/haipipe-experiment review claim` first — the narrative is significantly
stronger when claims are pre-validated.

### Step 2: Build the claim ↔ evidence map

- If `CLAIMS_FROM_RESULTS.md` exists, use its claims as the spine.
- Otherwise, extract claims from `IDEA_REPORT.md` + `AUTO_REVIEW.md`, then map
  each to result files. Flag any claim with no matching result file.

For each claim, pin:
- one or more raw-result file paths
- the specific number(s) that support the claim
- the baseline being compared against

### Step 3: Inventory figures

Scan `figures/` for existing PDFs / PNGs / SVGs.
For each section in the plan, decide:
- already exists → `exists`
- can be auto-generated from a result file → `auto` (note the script if any)
- needs hand drawing (architecture, qualitative concept, schematic) → `manual`

### Step 4: Write `NARRATIVE_REPORT.md`

Use the five-section structure above. Keep it tight — under ~400 lines for a
typical conference paper, under ~800 for a journal paper. Density beats
length: every line should either name a claim, name an evidence file, or set
context the reader needs to interpret the next line.

### Step 5: Handoff

Print the suggested next command:

```
📄 NARRATIVE_REPORT.md generated.

To write the paper:
    /haipipe-paper "NARRATIVE_REPORT.md" — venue: <ICLR|NeurIPS|...>

To revise:
    edit NARRATIVE_REPORT.md directly, then re-run /haipipe-paper
```

## Composing with other workflows

```
Upstream                          This skill                  Downstream
────────                          ──────────                  ──────────
/idea-discovery   ──► IDEA_REPORT ─┐
                                   ├──► /narrative-report  ──► NARRATIVE_REPORT.md ──► /haipipe-paper
implement + experiments            │                                                       │
                                   │                                                       ├──► /paper-plan
/auto-review-loop ──► AUTO_REVIEW ─┤                                                       ├──► /paper-figure
                                   │                                                       ├──► /paper-write
/haipipe-experiment review claim  ──► CLAIMS_…    ─┘                                                       ├──► /paper-compile
                                                                                           └──► /auto-paper-improvement-loop
```

Also invoked as Stage 5 of `/research-pipeline`. Standalone is fine when you
already have the upstream artifacts and only need the narrative.

## Rules

- **Claim ↔ evidence is non-negotiable.** Every quantitative line in the
  narrative must have a traceable file path. Numbers without sources will
  fail `/paper-claim-audit` later anyway — catch them here.
- **Do not invent claims the data doesn't support.** If `CLAIMS_FROM_RESULTS`
  says partial, do not round up to "yes" in the narrative.
- **Honest limitations save the paper.** Round-2 reviewers (human or auto)
  punish overclaiming far harder than they punish modest claims.
- **The narrative is editable.** Treat the first generation as a draft —
  expect a human pass before `/haipipe-paper` consumes it.
- **One narrative per paper**, not per experiment. Multi-experiment projects
  collapse into one story or split into separate papers; don't try to fit two
  stories into one narrative.
