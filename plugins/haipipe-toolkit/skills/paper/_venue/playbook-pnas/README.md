# PNAS Playbook (paper/_venue)

A Proceedings of the National Academy of Sciences **style + structure exemplar
pack** for the paper pipeline. Its main job is to hold the CONTENT of similar PNAS
papers (PDFs or extracted text) so we can **imitate their language style and
preferences**, alongside a distilled style profile and concrete lifecycle-stage
mappings. This is a style corpus, not a citation list.

## Relationship to the venue layer

- `_venue/README.md` = the venue index + broad-scope selection (PNAS vs Nature
  portfolio vs Science vs specialist journals).
- `_venue/playbook-pnas` (here) = **HOW** to shape THIS paper's lifecycle artifacts
  for PNAS, with verified exemplars to imitate. Sibling broad-scope pack:
  `playbook-nature-portfolio`.

## Structure

```
playbook-pnas/
  README.md            this hub + the lifecycle-stage mappings
  style-profile.md     distilled language style + preferences to imitate
  exemplars/           stored CONTENT (PDFs / extracted text) of similar papers
  references/          citation candidates for related work (secondary; verify before citing)
```

## How to use

At the claims / display / minimap stages, consult this playbook for (a) the
PNAS-shaped target for that artifact and (b) the nearest exemplar paper in
`exemplars/`. The target venue is set in the paper's `STATUS.md` (`venue`).

---

## Maps to lifecycle stages

### -> Claims (`0-lifecycle/2-claims`)

- Exactly ONE `[primary]` claim = the BROADLY SIGNIFICANT advance. PNAS rewards
  significance across a field, not novelty-per-se; the primary claim must answer
  "what is now possible, measurable, or understood that was not before, and why
  does it matter beyond the immediate specialty?".
- 2-4 supporting claims: cross-disciplinary implication, methodological rigor and
  reproducibility, boundary conditions, robustness.
- A method that is novel elsewhere (e.g. LLM-from-reviews) is an **enabler** in
  Methods, NOT a claim. PNAS weights a careful, reproducible evidence chain over a
  dramatic headline.
- The **Significance Statement** (~120 words) is the key framing artifact for the
  primary claim: it states the problem in field-general terms, the advance, and the
  cross-disciplinary importance. Draft it after the claim-evidence map is stable and
  before the Abstract, which inherits its framing.
- Borrow from `references/`: how exemplar PNAS papers state their one broadly
  significant advance.

### -> Display (`0-displays`)

PNAS-family standard display set:
- **Main-result figure** (the headline evidence) = the HERO, tied to the
  `[primary]` significance claim.
- **Multi-panel figures** that carry a linked evidence chain across panels; PNAS
  Research Articles tolerate up to ~6 main figures, so plan panel roles against that
  budget rather than splitting into many single-panel figures.
- A cross-disciplinary schematic or mechanism figure when the contribution spans two
  classifications, so a reader outside the specialty can follow the logic.
- Mapping rule: each claim -> one display; `[primary]` significance claim -> hero
  main-result figure.

### -> Minimap (`0-lifecycle/5-minimap`)

PNAS Research Article (full-length, ~50,000 characters, ~6 main figures):
- **Significance Statement** (~120 words): problem in field-general terms -> the
  advance -> why it matters beyond the specialty. Non-parallel with the Abstract.
- **Abstract** (<=250 words): unstructured prose; what was done and found, legible to
  scientists outside the immediate specialty.
- **Introduction**: the broadly significant problem -> what is not yet understood ->
  this paper's advance; framing matches the primary classification.
- **Results**: lead with the main-result figure; build the evidence chain panel by
  panel.
- **Discussion**: restate the broadly significant advance -> cross-disciplinary
  implications -> limitations -> conclusion.
- **Methods**: rigorous and reproducible by the method's own standards; data and code
  availability stated explicitly.
- Mapping rule: the `[primary]` significance claim drives the Significance Statement,
  the Abstract framing, the intro advance paragraph, and the first Discussion
  implication.

### -> Write / Edit (language style & preferences)  [the main purpose]

Imitate how PNAS papers actually read:
- Consult `style-profile.md` for the distilled style rules (Significance Statement at
  lay-accessible level, broad-readership tone, significance-first framing, abstract
  shape, evidence-bounded language).
- Read the nearest paper in `exemplars/` and mirror its sentence shapes and section
  moves (its style), not its content.
- Apply at the write/edit stages (`3-write-edit`), and to the Significance Statement
  and Abstract.

---

## references/ (citation candidates, secondary)

Verified, real PNAS / broad-science papers that could be CITED in related work (a
SECONDARY use; the primary purpose of this playbook is style imitation via
`exemplars/` + `style-profile.md`). Position the advance for a cross-disciplinary
readership; foundational work in both the primary and secondary classification must
appear when the contribution spans two fields. See `references/README.md`. Always
re-verify with `citation-audit` before any enters the manuscript.
