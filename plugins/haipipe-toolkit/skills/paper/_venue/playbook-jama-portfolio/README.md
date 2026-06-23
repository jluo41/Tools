# JAMA Portfolio (paper/_venue)

A JAMA-family **style + structure exemplar pack** for the paper pipeline. Its main
job is to hold the CONTENT of similar-topic JAMA papers (PDFs or extracted text) so
we can **imitate their language style and preferences**, alongside a distilled style
profile and concrete lifecycle-stage mappings. It operationalizes the general
principles in `_venue/playbook-clinical-medicine`. This is a style corpus, not a
citation list.

## Relationship to the venue layer

- `_venue/playbook-clinical-medicine` = **WHAT** clinical venues reward (principles:
  contribution-vs-enabler, primary-claim rule, observational framing). Cross-family,
  reusable.
- `paper/_venue/playbook-jama-portfolio` (here) = **HOW** to shape THIS paper's lifecycle
  artifacts for the JAMA family, with verified exemplars to imitate. Paper-pipeline
  and venue specific.

No duplication: principles live up in `_venue`; exemplars + stage mapping live here.

## Structure

```
playbook-jama-portfolio/
  README.md            this hub + the lifecycle-stage mappings
  style-profile.md     distilled language style + preferences to imitate
  exemplars/           stored CONTENT (PDFs / extracted text) of similar-topic papers
  references/          citation candidates for related work (secondary; verify before citing)
```

## How to use

At the claims / display / minimap stages, consult this playbook for (a) the
JAMA-shaped target for that artifact and (b) the nearest exemplar paper in
`references/`. The target venue is set in the paper's `STATUS.md` (`venue`).

---

## Maps to lifecycle stages

### -> Claims (`0-lifecycle/2-claims`)

- Exactly ONE `[primary]` clinical claim: associational, patient-safety or
  policy relevant, on a patient-oriented outcome.
- 2-4 supporting claims: mechanism, dose-response, heterogeneity (especially a
  vulnerable-population amplification), robustness / incremental validity.
- Observational data => associational language, never causal verbs.
- A method that is novel elsewhere (e.g. LLM-from-reviews) is an **enabler** in
  Methods, NOT a claim.
- Borrow from `references/`: how exemplar papers word their one primary clinical
  claim and which outcome they make patient-relevant.

### -> Display (`0-displays`)

JAMA-family standard display set:
- **Table 1** baseline / cohort characteristics (mandatory).
- **Cohort flow diagram** (STROBE): selection from source to analytic sample (mandatory).
- **Primary-association display** (adjusted main effect, table or figure) = the
  HERO, tied to the `[primary]` claim.
- **Subgroup / heterogeneity forest plot**: the vulnerable-population amplification.
- **Dose-response figure** when relevant.
- Mapping rule: each claim -> one display; `[primary]` claim -> hero display;
  Table 1 + flow diagram are always present.

### -> Minimap (`0-lifecycle/5-minimap`)

JAMA IMRAD + structured abstract:
- **Abstract**: Importance / Objective / Design / Setting / Participants /
  Exposures / Outcomes / Results / Conclusions.
- **Introduction** (~3 paragraphs): clinical problem (prescribing variation,
  safety) -> the gap -> this study's question.
- **Methods**: data, cohort, exposure, outcomes, analysis (STROBE).
- **Results**: R0 cohort + Table 1 -> R1 = `[primary]` claim -> one paragraph per
  supporting claim, hero claim leads.
- **Discussion**: interpretation (trade-off, not blame) -> clinical/policy
  implication -> limitations (observational, confounding) -> conclusion.
- Mapping rule: the `[primary]` claim drives the abstract Conclusions, the lead
  Results paragraph, and the first Discussion implication.

### -> Write / Edit (language style & preferences)  [the main purpose]

Imitate how JAMA papers actually read:
- Consult `style-profile.md` for the distilled style rules (abstract structure,
  associational sentence patterns, hedging, Results/Discussion openings, tone).
- Read the nearest paper in `exemplars/` and mirror its sentence shapes and section
  moves (its style), not its content.
- Apply at the write/edit stages (`3-write-edit`), and to the pitch and abstract.

---

## Outlets (per-journal delta)

The within-family tie-break. The whole JAMA Network shares the structure and style
below; pick the outlet from this table. All use the structured abstract, STROBE
(observational) / CONSORT (trials), and associational language.

| Dimension | JAMA (flagship) | JAMA Internal Medicine | JAMA Network Open | JAMA specialty (Pediatrics / Surgery / Psychiatry / ...) |
|-----------|-----------------|------------------------|-------------------|-----------------------------------------------------------|
| What it rewards | Broad, practice-changing clinical findings of wide interest across medicine | Internal-medicine practice and policy: prescribing, overuse / de-implementation, health services, safety | Methodologically sound, rigorous work of broad scope; soundness over novelty; open access | Clinical relevance within the specialty field |
| Audience | All physicians | Internists / general internal medicine / health-services | Broad + open (high readership and citation volume) | The specialty community |
| Impact / acceptance bar | Highest; very selective | High; selective | Moderate; higher acceptance, large volume, APC (open access) | Field-level |
| Typical study | Major trials, landmark cohorts that change practice | Observational claims and pragmatic trials on practice, prescribing variation, overuse | Solid observational and secondary analyses, well-reported | Field-specific clinical studies |
| When to pick it | The finding changes general practice and matters to all physicians | Prescribing / overuse / safety / health-services observational claim (the ProjB lane) | Faster, open-access home for a sound observational study; strong backup to JAMA IM | The contribution is specialty-bounded |

Tie-break for an observational prescribing-safety claim (e.g. physician trait ->
opioid prescribing): PRIMARY `JAMA Internal Medicine`, BACKUP `JAMA Network Open`
(same family, faster and open access). Once chosen, pin it as `venue_outlet:` in
`STATUS.md`.

---

## references/ (citation candidates, secondary)

Verified, real papers that could be CITED in related work (a SECONDARY use; the
primary purpose of this playbook is style imitation via `exemplars/` +
`style-profile.md`). Topics: physician characteristics -> prescribing; opioid
prescribing variation; reviews/NLP -> physician behavior; two-part models; and
satisfaction pressure -> opioid prescribing. See `references/README.md`. Always
re-verify with `citation-audit` before any enters the manuscript.
