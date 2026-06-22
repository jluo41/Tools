---
name: haipipe-paper-narrative
description: "Generate NARRATIVE_REPORT.md — the design contract for /haipipe-paper. Reads upstream research artifacts (IDEA_REPORT, AUTO_REVIEW, CLAIMS_FROM_RESULTS, experiment results, repo source) and emits a single coherent narrative: problem statement, core claim, method, claim-evidence matrix, figure inventory, limitations. Use when transitioning from research/experiment phase to writing phase, or when the user says 'write narrative report', '生成 narrative', '/haipipe-paper-narrative'."
argument-hint: "[project-dir-or-topic]"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob
metadata:
  version: "1.1.0"
  last_updated: "2026-05-31"
  summary: "Generate NARRATIVE_REPORT.md — the design contract for /haipipe-paper."
  changelog:
    - "1.1.0 (2026-06-05): renamed from narrative-report to haipipe-paper-narrative (haipipe-paper-* name unification)."
    - "1.0.0 (2026-05-31): baseline metadata added."
---

# Narrative Report Generator

The narrative report is **not** a draft of the paper. It is the **design contract**
that the paper writes from. Every claim, figure, and citation in the final PDF
should trace back to a line in this file. If something is not in the narrative,
the downstream pipeline (`/haipipe-paper-minimap → /haipipe-paper-display-figure → /haipipe-paper-edit-write`) will not
invent it.

If the paper folder has `0-lifecycle/1-pitch/1-pitch.tex`, read it before composing the
narrative. The pitch is the one-minute public-facing story for this concrete
paper; this narrative expands it into evidence-backed claims, figures, and
limitations. If the evidence forces a different pitch, update
`0-lifecycle/1-pitch/1-pitch.tex` through `/haipipe-paper-lifecycle pitch` and log the
shift instead of silently diverging.

## Context: $ARGUMENTS

## When to Use

- Research / experiment phase is essentially done — results are in, story is
  approximately settled
- Before invoking `/haipipe-paper` or `/haipipe-paper-minimap` (they consume this file)
- After `/auto-review-loop` finishes, as the handoff to writing
- When the project has accumulated `IDEA_REPORT.md`, `AUTO_REVIEW.md`,
  experiment logs, and figures but no single document tells the story

Do **not** use when:
- Experiments are still running (the narrative would be premature)
- You only have a vague topic — use `/idea-discovery` or `/haipipe-probe judge` first
- A `NARRATIVE_REPORT.md` already exists and is current — edit it directly

## Inputs (in priority order)

The skill discovers whichever of these exist in the project tree:

0. **`0-lifecycle/1-pitch/1-pitch.tex`** (paper folder, if present) — current
   one-minute paper story. Use it as the reader-facing framing constraint, not
   as evidence.
1. **`CLAIMS_FROM_RESULTS.md`** (best) — validated claim ↔ evidence map from
   `/haipipe-probe judge`. If present, use as the spine of the narrative; every
   listed claim becomes a section in the report.
2. **`IDEA_REPORT.md`** — chosen idea, hypothesis, novelty justification (from
   `/idea-discovery`). Supplies the problem statement and intended contribution.
3. **`review-stage/AUTO_REVIEW.md`** (fall back to `./AUTO_REVIEW.md`) — review
   history, weaknesses fixed, remaining limitations (from `/auto-review-loop`).
   Supplies the limitations section and reframings.
4. **Experiment results** — JSON / CSV / TSV under `figures/`, `results/`,
   `outputs/`, `probes/`. These are the raw evidence for every quantitative
   claim. Each number that ends up in the narrative must trace back to one of
   these files.
5. **`EXPERIMENT_LOG.md` / `probe-log.txt`** — comparison-first experiment
   ledger. Useful for cross-probe deltas and baseline-vs-method tables.
6. **Repo source** — for the method summary (what was actually built; not
   what was originally proposed). One short paragraph, not a code dump.

If multiple inputs disagree (e.g. `IDEA_REPORT` says "X improves Y by 5%" but
`CLAIMS_FROM_RESULTS` says "no improvement on test-od"), **trust the latest /
most data-grounded source** (CLAIMS_FROM_RESULTS > experiment files >
AUTO_REVIEW > IDEA_REPORT) and surface the discrepancy as a note in the report.

## Output: `NARRATIVE_REPORT.md`

The report must contain these six sections, in this order:

0. **Pitch alignment** — the current one-minute pitch, hook, surprise, so what,
   why-believe, and still-fragile bullets from `0-lifecycle/1-pitch/1-pitch.tex` if
   present. Keep this short; it is a constraint, not a full section draft.
1. **Problem statement and core claim** — one-paragraph problem, one-sentence
   core claim. The core claim is the single sentence the paper exists to
   defend. Everything else supports it.
2. **Method summary** — what was built, at a level a reviewer can grasp in 30
   seconds. Not a manual; not an architecture deep-dive. Save the depth for
   `/haipipe-paper-edit-write`.
3. **Key quantitative results with evidence for each claim** — table or list
   with one row per claim:
   - claim (free text, declarative)
   - supporting experiment / dataset / metric
   - effect size + uncertainty
   - file path to the raw result (the future `/haipipe-paper-edit-claim-audit` will follow
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
   paper from `/haipipe-paper-edit-improve-loop` round-2 hatchet jobs.

## Workflow

### Step 1: Discover inputs

```bash
ls 0-lifecycle/1-pitch/1-pitch.tex CLAIMS_FROM_RESULTS.md IDEA_REPORT.md review-stage/AUTO_REVIEW.md AUTO_REVIEW.md EXPERIMENT_LOG.md probe-log.txt 2>/dev/null
find results outputs experiments figures -maxdepth 3 -type f \
    \( -name '*.json' -o -name '*.csv' -o -name '*.tsv' -o -name '*.jsonl' \) 2>/dev/null | head -50
```

Report what was found vs missing. If `CLAIMS_FROM_RESULTS.md` is missing,
suggest running `/haipipe-probe judge` first — the narrative is significantly
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
                                   ├──► /haipipe-paper-narrative  ──► NARRATIVE_REPORT.md ──► /haipipe-paper
implement + experiments            │                                                       │
                                   │                                                       ├──► /haipipe-paper-minimap
/auto-review-loop ──► AUTO_REVIEW ─┤                                                       ├──► /haipipe-paper-display-figure
                                   │                                                       ├──► /haipipe-paper-edit-write
/haipipe-probe judge  ──► CLAIMS_…    ─┘                                                       ├──► /paper-compile
                                                                                           └──► /haipipe-paper-edit-improve-loop
```

Also invoked as Stage 5 of `/research-pipeline`. Standalone is fine when you
already have the upstream artifacts and only need the narrative.

## Rules

- **Claim ↔ evidence is non-negotiable.** Every quantitative line in the
  narrative must have a traceable file path. Numbers without sources will
  fail `/haipipe-paper-edit-claim-audit` later anyway — catch them here.
- **Do not invent claims the data doesn't support.** If `CLAIMS_FROM_RESULTS`
  says partial, do not round up to "yes" in the narrative.
- **Honest limitations save the paper.** Round-2 reviewers (human or auto)
  punish overclaiming far harder than they punish modest claims.
- **The narrative is editable.** Treat the first generation as a draft —
  expect a human pass before `/haipipe-paper` consumes it.
- **One narrative per paper**, not per probe. Multi-probe projects
  collapse into one story or split into separate papers; don't try to fit two
  stories into one narrative.
