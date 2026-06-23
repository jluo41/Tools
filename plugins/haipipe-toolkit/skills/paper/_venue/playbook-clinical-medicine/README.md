# Clinical Medicine Playbook (paper/_venue)

A clinical-journal-family **style + structure exemplar pack** for the paper
pipeline. Its main job is to hold the CONTENT of similar clinical papers (PDFs or
extracted text) so we can **imitate their language style and preferences**,
alongside a distilled style profile and concrete lifecycle-stage mappings. This
pack is cross-family (JAMA, JAMA Internal Medicine, NEJM, The Lancet, Annals of
Internal Medicine, BMJ): it carries the principles that single-journal packs
specialize. This is a style corpus, not a citation list.

## Relationship to the venue layer

- `_venue/README.md` = the venue index + clinical selection table (which clinical
  journal fits the manuscript).
- `_venue/playbook-clinical-medicine` (here) = **WHAT** clinical venues reward
  (principles: contribution-vs-enabler, primary-claim rule, observational
  framing) AND **HOW** to shape this paper's lifecycle artifacts for the clinical
  family, with verified exemplars to imitate. Cross-family and reusable.
- `_venue/playbook-jama-portfolio` is the JAMA-specific specialization of these principles:
  it points here as its principles source and specializes the stage mappings for
  the JAMA family.

## Structure

```
playbook-clinical-medicine/
  README.md            this hub + the lifecycle-stage mappings
  style-profile.md     distilled language style + preferences to imitate
  exemplars/           stored CONTENT (PDFs / extracted text) of similar papers
  references/          citation candidates for related work (secondary; verify before citing)
```

## How to use

At the claims / display / minimap stages, consult this playbook for (a) the
clinical-shaped target for that artifact and (b) the nearest exemplar paper in
`exemplars/`. The target venue is set in the paper's `STATUS.md` (`venue`). When
the paper targets a specific JAMA-family journal, also consult `playbook-jama-portfolio` for
the journal-specific specialization.

---

## Maps to lifecycle stages

### -> Claims (`0-lifecycle/2-claims`)

- Exactly ONE `[primary]` claim = the CLINICAL contribution: actionable,
  safety-relevant, on a patient-oriented outcome. Clinical reviewers ask "so what
  for patients?" every time; the primary claim must answer it.
- Observational data => state **associations, not causes**; never use causal
  verbs ("caused", "led to", "reduced") unless the design is a trial.
- 2-4 supporting claims: mechanism, dose-response, heterogeneity (especially a
  vulnerable-population amplification, which can be a strong primary or
  co-primary), robustness.
- A method that is novel elsewhere (e.g. LLM-from-reviews) is an **enabler** in
  Methods, NOT a claim. The SAME evidence yields different headlines by venue: at
  an informatics/IS venue the measurement is the contribution; at a clinical venue
  it is the enabler and the clinical finding leads.
- Borrow from `references/`: how exemplar clinical papers word their one primary
  clinical claim and which outcome they make patient-relevant.

### -> Display (`0-displays`)

Clinical-family standard display set:
- **Table 1** baseline / cohort characteristics (mandatory).
- **Cohort flow diagram** (STROBE): selection from source to analytic sample
  (mandatory).
- **Primary-association display** (adjusted main effect, table or figure) = the
  HERO, tied to the `[primary]` clinical claim.
- **Subgroup / heterogeneity forest plot**: the vulnerable-population amplification.
- **Dose-response figure** when relevant.
- Mapping rule: each claim -> one display; `[primary]` claim -> hero display;
  Table 1 + flow diagram are always present.

### -> Minimap (`0-lifecycle/5-minimap`)

Clinical IMRAD + structured abstract:
- **Abstract**: Importance / Objective / Design / Setting / Participants /
  Exposures / Main Outcomes and Measures / Results / Conclusions and Relevance.
- **Introduction** (~3 paragraphs): clinical problem (prescribing variation,
  safety, overuse) -> the gap -> this study's question.
- **Methods**: data, cohort, exposure, outcomes, analysis (STROBE for
  observational; CONSORT for trials).
- **Results**: R0 cohort + Table 1 -> R1 = `[primary]` claim -> one paragraph per
  supporting claim, hero claim leads.
- **Discussion**: principal findings -> interpretation (trade-off, not blame) ->
  clinical/policy implication -> a dedicated limitations paragraph (observational,
  confounding, generalizability) -> conclusion.
- Mapping rule: the `[primary]` claim drives the abstract Conclusions, the lead
  Results paragraph, and the first Discussion implication.

### -> Write / Edit (language style & preferences)  [the main purpose]

Imitate how clinical papers actually read:
- Consult `style-profile.md` for the distilled style rules (structured-abstract
  shape, associational sentence patterns, hedging, Results/Discussion openings,
  tone, no blame framing).
- Read the nearest paper in `exemplars/` and mirror its sentence shapes and section
  moves (its style), not its content.
- Apply at the write/edit stages (`3-write-edit`), and to the pitch and abstract.

---

## references/ (citation candidates, secondary)

Verified, real clinical / health-services papers that could be CITED in related
work (a SECONDARY use; the primary purpose of this playbook is style imitation via
`exemplars/` + `style-profile.md`). Position against the clinical literature;
relevant reporting standards (STROBE, CONSORT) and the ICMJE Recommendations must
appear when relevant. See `references/README.md`. Always re-verify with
`citation-audit` before any enters the manuscript.
