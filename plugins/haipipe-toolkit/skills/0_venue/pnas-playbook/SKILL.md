---
name: pnas-playbook
description: Use when choosing PNAS as a venue, deciding between PNAS and Nature-portfolio journals, or preparing a PNAS-specific manuscript for fit, article-type framing, Significance Statement drafting, and pre-submission checks.
metadata:
  version: "1.0.0"
  last_updated: "2026-05-31"
  summary: "Use when choosing PNAS as a venue, deciding between PNAS and Nature-portfolio journals, or preparing a PNAS-specific manuscript for fit, article-type framing, Significance Statement drafting, and pre-submission checks."
  changelog:
    - "1.0.0 (2026-05-31): baseline metadata added."
---

# PNAS Playbook

## Overview

Use this skill when the venue decision is between PNAS and another broad-scope journal (Nature family, Science, or top field-specific journals), or when a manuscript already targets PNAS and needs venue-specific framing before a heavy revision pass.

This skill is about fit, Significance Statement quality, classification, and submission policy. It does not replace `haipipe-paper-edit-write-scientific`, `haipipe-paper-edit-optimizer`, or `haipipe-paper-edit-submission-audit`.

## When To Use

Use this skill when:
- the user asks whether a story fits PNAS vs Nature, Science, or a specialist top journal
- the paper has a broad-science tone but the venue is undecided
- the contribution spans two fields (methodological + biological, physical + social, etc.)
- a manuscript is close to PNAS submission and needs a venue-specific preflight
- the Significance Statement needs drafting or review

Do not use this skill when:
- the task is generic sentence-level editing
- the venue is a conference or a specialty journal without broad-readership framing
- the manuscript structure itself is still unstable and needs `haipipe-paper-edit-optimizer` first

## Venue Fit vs Alternatives

### When PNAS is the right fit

PNAS is the right target when the paper is:
- **Broadly significant but not requiring mass-appeal framing.** Nature's flagship requires a story legible to non-specialists; PNAS accepts stories legible to scientists outside the immediate specialty but does not demand tabloid-style accessibility.
- **Cross-disciplinary.** Contributions that span two NAS classifications (e.g., computational methods + biology, or physics + biology) fit PNAS naturally because PNAS organizes submissions by explicit cross-disciplinary classification.
- **Methodologically solid and reproducible.** PNAS weights rigor and reproducibility heavily relative to "novelty-per-se." A paper with a careful evidence chain and broad applicability may fit PNAS better than Nature even when the headline is less dramatic.
- **Research Article scope (not a brief letter).** PNAS Research Articles tolerate more figures (up to ~6 main) and longer text (~50,000 characters) than Nature Article format allows.

### When Nature Portfolio is a better fit

Prefer the Nature playbook when:
- the advance is framed around broad-readership significance, not cross-disciplinary rigor
- the contribution is primarily methods (Nature Methods) or biotech (Nature Biotechnology)
- the story depends on a concise, non-specialist-friendly summary paragraph

### When Science is a better fit

Route to a Science-specific submission (out of scope for this playbook) when:
- the story has strong societal / policy implications beyond the scientific result
- the paper is short-form and punchy, not a full-length rigorous article
- the target is a Science Advances paper (open-access sibling)

### When a specialist journal is a better fit

If the paper's significance is largely within-field and the cross-disciplinary hook is thin, a top specialist journal will generally give better review quality and acceptance odds than PNAS.

## Significance Statement Discipline

PNAS requires a Significance Statement at submission. It is ~120 words, visible on the title page, and read by the handling editor and reviewers before the Abstract.

Treat it as a claim instrument, not a summary.

### What the Significance Statement must do

1. **State the problem in field-general terms** -- a second-year graduate student in any NAS classification should understand the stakes.
2. **State the advance** -- what is now possible, measurable, or understood that was not before.
3. **State why it matters beyond the immediate specialty** -- cross-disciplinary implication, not field-internal importance.

### What the Significance Statement must not do

- Do not repeat the Abstract. Reviewers compare them; parallelism is a red flag.
- Do not hedge. "May contribute to understanding X" is weaker than "establishes X."
- Do not overstate. Evidence-bounded language (see `PRINCIPLES.md` #5) applies doubly here -- the Significance Statement is cited when claims are later disputed.

### Drafting order

Write the Significance Statement **after** the claim-evidence map is stable (see `examples/claim_evidence_map.md`) but **before** the Abstract. The Abstract inherits its framing; reversing the order produces a Significance Statement that merely restates Abstract-language.

## Classification

PNAS organizes submissions by classification. Get this right at submission -- it determines editor routing.

- **Primary classification** (required): pick the field that carries the core contribution.
- **Secondary classification** (optional but recommended for cross-disciplinary work): signal the second field so the editor can route to a cross-trained reviewer pool.

The three top-level groups are: Physical Sciences, Social Sciences, Biological Sciences. Each contains ~20 subfields. If a paper genuinely spans two top-level groups, primary/secondary classification carries more framing weight than any other single submission decision.

## Article-Type Check

Do this early. Do not treat article type as formatting cleanup.

- **Research Article**: the default; full research story with multiple linked claims, ~6 figures, ~50,000 characters.
- **Brief Report**: short, focused, single-claim contribution. Use only when the story genuinely does not support a full article.
- **Perspective**: synthesis or forward-looking commentary; by invitation or strong framing case.
- **Opinion / Letter**: commentary on published work; rarely a primary submission target.

If the manuscript keeps oscillating between `research article` and `brief report`, resolve before rewriting the Abstract or Results.

## PNAS Preflight

Run this before calling a draft submission-ready:

1. **Significance Statement**: current, non-parallel with Abstract, evidence-bounded, ~120 words, written after claim-evidence map stabilized.
2. **Classification**: primary and (if cross-disciplinary) secondary classifications chosen; framing of Introduction matches primary classification.
3. **Data and code availability**: PNAS requires explicit statements. Confirm repository names, accession IDs, download links, and any access restrictions are ready.
4. **Reporting standards**: check domain-specific reporting requirements (MIAME, MIAPE, ARRIVE, CONSORT, etc. as applicable); do not wait until revision.
5. **Author contributions**: PNAS requires CRediT-style statements; draft before submission, not after acceptance.
6. **Ethics statements**: IRB, IACUC, consent, dual-use research of concern (DURC) as applicable -- all finalized.
7. **Suggested reviewers / non-preferred reviewers**: PNAS accepts both. Prepare a short list of each with justification.
8. **Cover letter**: ~1 page, explicitly naming why PNAS (cross-disciplinary fit) and what the advance is; not a restatement of the Significance Statement.

## Submission Tracks

PNAS historically had three tracks (Direct, Contributed, Communicated). In practice:

- **Direct Submission** is the default and the only route for non-NAS-member authors.
- **Contributed** is available only to NAS members, with strict annual limits. If a co-author is an NAS member, discuss with them whether to use a contributed slot; it has faster turnaround but member-track oversight.
- Communicated submission is no longer available.

## Handoff To Other Skills

After this playbook settles venue fit, classification, article type, and Significance Statement framing, hand off to:

- `haipipe-paper-structure-bootstrap` -- if the project is new or needs a source-of-truth refresh
- `haipipe-paper-edit-optimizer` -- if the paper's claim structure, evidence chain, or terminology needs revision under PNAS framing
- `haipipe-paper-edit-write-scientific` -- for drafting or section-level rewriting with PNAS classification in mind
- `haipipe-paper-structure-figure-planner` -- PNAS allows ~6 main figures; plan panel roles against that budget
- `citation-verifier` -- bibliography hygiene
- `haipipe-paper-edit-submission-audit` -- final pre-submission gate; confirm this playbook's preflight items are satisfied

Do not skip `haipipe-paper-edit-submission-audit` just because this playbook ran. They check different things: this playbook checks venue-specific fit; `haipipe-paper-edit-submission-audit` checks that the manuscript's internal claim-evidence-figure-text alignment is stable.
