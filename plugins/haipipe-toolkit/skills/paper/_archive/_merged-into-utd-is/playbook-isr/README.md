# ISR Playbook (paper/_venue)

An Information Systems Research **style + structure exemplar pack** for the paper
pipeline. Its main job is to hold the CONTENT of similar ISR papers (PDFs or
extracted text) so we can **imitate their language style and preferences**,
alongside a distilled style profile and concrete lifecycle-stage mappings. This is
a style corpus, not a citation list.

## Relationship to the venue layer

- `_venue/README.md` = the venue index + IS selection table (MISQ vs ISR vs MS-IS).
- `_venue/playbook-isr` (here) = **HOW** to shape THIS paper's lifecycle artifacts
  for ISR, with verified exemplars to imitate. Sibling packs: `playbook-misq`,
  `playbook-ms-is`.

ISR (published by INFORMS) sits closer to the social-science and economics end of
the IS spectrum than MISQ: it rewards tight theory-driven empirics, causal
identification, and quantitative rigor; interpretive and design-science work appear
rarely.

## Structure

```
playbook-isr/
  README.md            this hub + the lifecycle-stage mappings
  style-profile.md     distilled language style + preferences to imitate
  exemplars/           stored CONTENT (PDFs / extracted text) of similar papers
  references/          citation candidates for related work (secondary; verify before citing)
```

## How to use

At the claims / display / minimap stages, consult this playbook for (a) the
ISR-shaped target for that artifact and (b) the nearest exemplar paper in
`exemplars/`. The target venue is set in the paper's `STATUS.md` (`venue`).

---

## Maps to lifecycle stages

### -> Claims (`0-lifecycle/2-claims`)

- Exactly ONE `[primary]` claim. ISR rewards a tight theory -> hypotheses -> evidence
  chain backed by strong causal identification. The primary claim is the
  **mechanism / moderator / boundary condition** the paper specifies, OR the **first
  large-scale causal evidence** that an IT artifact or policy affects an outcome.
- 2-4 supporting claims: additional hypothesis tests, identification robustness,
  heterogeneity, and effect-size or practical-significance argument.
- A method that is novel elsewhere (e.g. an ML measure from text) is an **enabler**
  in Methods, NOT a claim, unless framed as a methodological-IS contribution that
  enables a capability and is validated on an IS phenomenon.
- "We apply theory X to a new context" with no specified mechanism is NOT a
  contribution; an incremental mechanism already established in related work is a
  common rejection reason.
- Borrow from `references/`: how exemplar ISR papers state the one-sentence
  contribution (theoretical / empirical / methodological-IS).

### -> Display (`0-displays`)

ISR-family standard display set:
- **Research model figure** (constructs + hypothesized directional relationships) =
  the HERO, tied to the `[primary]` theory claim.
- **Hypothesis-test table** (estimates, standard errors, significance per H).
- **Identification displays** carrying the causal claim:
  - DiD: parallel-trends plot and/or event-study coefficients.
  - IV: first-stage table (report F > 10).
  - RD: discontinuity plot with bandwidth sensitivity.
  - Matching: covariate **balance table** before vs after matching.
- Construct-measurement / validity table for survey work (AVE, CR, alpha,
  Fornell-Larcker / HTMT).
- Mapping rule: each claim -> one display; `[primary]` claim -> hero model figure;
  any causal claim -> its identification display.

### -> Minimap (`0-lifecycle/5-minimap`)

ISR article (~35 pages double-spaced text excluding references/appendices),
theory-forward IMRAD:
- **Abstract** (<=150 words, unstructured prose): IS phenomenon -> gap -> approach ->
  theoretical + empirical contribution.
- **Introduction**: important IS phenomenon and why it matters -> what prior work has
  established -> the specific gap (mechanism, boundary, causal direction, or no
  large-scale evidence) -> this paper's contribution.
- **Theory & Hypotheses**: derive each hypothesis from a named theoretical mechanism;
  resist long undifferentiated H1-H12 lists (reads as fishing).
- **Method**: executed rigorously by that method's own standards (psychometrics for
  surveys; clean causal identification for archival).
- **Results**: hypothesis tests and identification checks; lead with the model.
- **Discussion**: theoretical contribution restated -> implications for IS theory &
  practice -> limitations (endogeneity threats, causality honesty) -> conclusion.
- Mapping rule: the `[primary]` claim drives the abstract contribution sentence, the
  intro contribution paragraph, and the first Discussion implication.

### -> Write / Edit (language style & preferences)  [the main purpose]

Imitate how ISR papers actually read:
- Consult `style-profile.md` for the distilled style rules (hypothesis phrasing that
  traces to a mechanism then a directional prediction, honesty about causality vs
  correlation, psychometrics phrasing for surveys, intro recipe, tone).
- Read the nearest paper in `exemplars/` and mirror its sentence shapes and section
  moves (its style), not its content.
- Apply at the write/edit stages (`3-write-edit`), and to the pitch and abstract.

---

## references/ (citation candidates, secondary)

Verified, real ISR / IS papers that could be CITED in related work (a SECONDARY use;
the primary purpose of this playbook is style imitation via `exemplars/` +
`style-profile.md`). Position against IS literature, not just management or
economics journals; engaging management journals while missing key IS papers is a
common rejection reason. See `references/README.md`. Always re-verify with
`citation-audit` before any enters the manuscript.
