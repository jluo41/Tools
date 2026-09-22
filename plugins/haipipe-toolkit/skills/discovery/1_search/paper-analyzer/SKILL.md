---
name: paper-analyzer
description: Use when deeply analyzing a single paper and producing structured notes on claims, methods, figures, evaluation, strengths, limitations, and related work.
metadata:
  version: "0.2.2"
  last_updated: "2026-09-22"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
  haipipe:
    vendored_from: https://github.com/Boom5426/Nature-Paper-Skills@44cff42
    vendored_on: "2026-09-22"
    local_changes: adapted SKILL.md (HAI Pipe adapter) and added CHANGELOG
---
# Paper Analyzer

## Overview

Produce an evidence-anchored note for one paper. Keep author claims, reported results, and reader inferences distinct. Do not assign a single paper-quality score: record what was inspected, what the paper reports, and how directly it bears on the declared question.

# Workflow

## Step 1: Identify Paper
Accept an arXiv ID (e.g., "2402.12345"), full ID ("arXiv:2402.12345"), paper title, DOI, or file path. Resolve the exact title and canonical identifier before analysis. If identity is ambiguous, leave the note in draft and record the unresolved identity rather than choosing the closest-looking result.

## Step 2: Fetch and record source access
```bash
curl -L "https://arxiv.org/pdf/[PAPER_ID]" -o /tmp/paper_analysis/[PAPER_ID].pdf
curl -L "https://arxiv.org/e-print/[PAPER_ID]" -o /tmp/paper_analysis/[PAPER_ID].tar.gz
curl -s "https://arxiv.org/abs/[PAPER_ID]" > /tmp/paper_analysis/arxiv_page.html
```

Record whether you inspected metadata, abstract, selected sections, or the full text. Do not describe an abstract-only or metadata-only pass as a full-paper analysis. Note the question this paper is being assessed against; when there is no declared question, state that relevance to a particular project was not assessed.

## Step 3: Extract evidence before appraising

For each material statement, record a page/section/table locator and keep these
categories separate:

- **Author claim** — a claim the authors explicitly make, with its locator.
- **Reported result** — population, comparison, outcome, estimate or metric, and
  uncertainty exactly as reported; do not infer a result from a figure title.
- **Reader inference** — your interpretation, labeled as such and tied to the
  specific reported evidence it uses.
- **Limit** — author-stated limitation or reader-inferred boundary; identify
  which kind it is and cite the relevant text or design detail.

Use these evidence states for each appraisal criterion, and always supply a
locator or explain why one is unavailable:

- `supported`: inspected text directly supplies the evidence the criterion
  asks for.
- `partially-supported`: some relevant evidence is present, but a named detail
  needed to answer the criterion is missing or incomplete.
- `not-supported`: the relevant text was inspected and does not support the
  criterion, or reports evidence against it; state which applies.
- `not-assessed`: the needed source content or criterion was not inspected, or
  identity/access remains unresolved. This is not a negative finding.
- `not-applicable`: the criterion does not apply to this paper's design or
  stated claim type; name that reason rather than counting it as a failure.

Apply the states against these fixed checks: method transparency covers the
study/design or theoretical assumptions, data/population where applicable,
and enough procedure detail to trace the claim; evaluation coverage covers
whether each primary claim is matched by a reported analysis/proof and whether
the named comparison, outcomes, and uncertainty are available for empirical
claims; claim-to-result traceability requires a locator for each material
conclusion and the result/proof it relies on. Mark a missing detail
`partially-supported` when other required details are present; use
`not-supported` when inspected text gives no evidence for the criterion or
reports evidence against it. Do not treat an inaccessible or unread section as
evidence of absence.

For relevance to a declared question, use `direct` only when the studied
population, method/exposure, and outcome match the question's stated scope;
use `adjacent` when the work informs a named method or mechanism but misses a
scope element; use `out-of-scope` only when a stated inclusion condition fails.
If scope fit cannot be decided from inspected material, use `unresolved` and
keep it out of the admitted evidence set until reviewed.

The generated note carries one shared `assessment` receipt for all criterion
states in its Evidence-grounded assessment section. Before changing it to
`reviewed`, identify the evaluator (`person:<stable-id>` or
`agent:<name>/<model>/<session-id>`), the exact rubric version, and an ISO 8601
timestamp with timezone. Link the evidence to a full readable/compact owning
Discovery Run when available; for a standalone analysis, record the exact
source snapshot URI and SHA-256 instead. Preserve the old receipt if the
assessment is repeated under a changed rubric or input.

## Step 4: Generate a draft note
```bash
python scripts/generate_note.py --paper-id "$PAPER_ID" --title "$TITLE" --authors "$AUTHORS" --domain "$DOMAIN"
```

## Step 5: Index bibliographic metadata
```bash
python scripts/update_graph.py --paper-id "$PAPER_ID" --title "$TITLE" --domain "$DOMAIN"
```

This writes identity and relationship metadata only. It does not certify that
the note was completed or assign a quality value; update the note's
`analysis_status` only after filling the evidence-grounded appraisal.
Keep assessment status in the note; the graph is only a bibliographic index.
The generator sets `status: draft` and `analysis_status: not-assessed`. Change
both to `reviewed` only after the canonical identity and reading scope are
recorded, every appraisal row has an allowed state plus an evidence locator or
an explicit reason it could not be assessed, and the shared assessment receipt
is complete. A row marked `not-assessed` may remain, but its reason must be
stated. Re-indexing metadata does not change the note's assessment status.

# Scripts
- `scripts/generate_note.py` — Generate structured note template
- `scripts/update_graph.py` — Index paper identity and relationship metadata

# Note Structure
The generated note is an unassessed draft with prompts for source access, located evidence, reported methods/results, author-stated and reader-inferred limits, question fit, and criterion-level evidence states. The generator does not score paper quality.

# Dependencies
- Python 3.8+, PyYAML, requests
- Network access (arXiv)

---
> Based on [evil-read-arxiv](https://github.com/evil-read-arxiv) — an automated paper reading workflow. MIT License.
