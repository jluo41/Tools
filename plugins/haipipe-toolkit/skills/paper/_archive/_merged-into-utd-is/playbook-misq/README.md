# MISQ Playbook (paper/_venue)

A MIS Quarterly **style + structure exemplar pack** for the paper pipeline. Its main
job is to hold the CONTENT of similar MISQ papers (PDFs or extracted text) so we can
**imitate their language style and preferences**, alongside a distilled style profile
and concrete lifecycle-stage mappings. This is a style corpus, not a citation list.

## Relationship to the venue layer

- `_venue/README.md` = the venue index + IS selection table (MISQ vs ISR vs MS-IS).
- `_venue/playbook-misq` (here) = **HOW** to shape THIS paper's lifecycle artifacts
  for MISQ, with verified exemplars to imitate. Sibling packs: `playbook-isr`,
  `playbook-ms-is`.

## Structure

```
playbook-misq/
  README.md            this hub + the lifecycle-stage mappings
  style-profile.md     distilled language style + preferences to imitate
  exemplars/           stored CONTENT (PDFs / extracted text) of similar papers
  references/          citation candidates for related work (secondary; verify before citing)
```

## How to use

At the claims / display / minimap stages, consult this playbook for (a) the
MISQ-shaped target for that artifact and (b) the nearest exemplar paper in
`exemplars/`. The target venue is set in the paper's `STATUS.md` (`venue`).

---

## Maps to lifecycle stages

### -> Claims (`0-lifecycle/2-claims`)

- Exactly ONE `[primary]` claim = the THEORETICAL contribution. MISQ asks "what is
  the theoretical contribution?" every time; the primary claim must answer it: a new
  construct, a specified mechanism, a resolved theoretical tension, or (design
  science) abstracted design principles.
- 2-4 supporting claims: empirical findings, methodological rigor, boundary
  conditions, robustness.
- A method that is novel elsewhere (e.g. LLM-from-reviews) is an **enabler** in
  Methods, NOT a claim.
- "We apply TAM to a new context" with no modification is NOT a contribution.
- Borrow from `references/`: how exemplar MISQ papers state their one-paragraph
  theoretical contribution.

### -> Display (`0-displays`)

MISQ-family standard display set:
- **Research model / theoretical framework figure** (constructs + hypothesized
  relationships) = the HERO, tied to the `[primary]` theory claim.
- **Hypothesis-test table** (estimates, significance per H).
- For design science: **artifact figure** + a **design-principles table**.
- Construct-measurement / validity table (survey work).
- Mapping rule: each claim -> one display; `[primary]` theory claim -> hero model figure.

### -> Minimap (`0-lifecycle/5-minimap`)

MISQ Research Article (typical 40-50 pp), theory-forward IMRAD:
- **Abstract** (<=150 words): phenomenon -> gap -> approach -> theoretical + empirical contribution.
- **Introduction**: IS phenomenon that matters -> what IS research has not explained
  -> this paper's contribution.
- **Theory & Hypotheses**: one primary theory used rigorously (resist stacking 3-4);
  each hypothesis traces to a mechanism.
- **Method**: executed rigorously by that method's own standards (CMB for surveys, etc.).
- **Results**: hypothesis tests, lead with the model.
- **Discussion**: theoretical contribution restated -> implications for IS theory &
  practice -> limitations -> conclusion.
- Mapping rule: the `[primary]` theory claim drives the abstract contribution
  sentence, the intro contribution paragraph, and the first Discussion implication.

### -> Write / Edit (language style & preferences)  [the main purpose]

Imitate how MISQ papers actually read:
- Consult `style-profile.md` for the distilled style rules (contribution-statement
  phrasing, hypothesis patterns, IS-community framing, abstract shape, tone).
- Read the nearest paper in `exemplars/` and mirror its sentence shapes and section
  moves (its style), not its content.
- Apply at the write/edit stages (`3-write-edit`), and to the pitch and abstract.

---

## references/ (citation candidates, secondary)

Verified, real MISQ / IS papers that could be CITED in related work (a SECONDARY
use; the primary purpose of this playbook is style imitation via `exemplars/` +
`style-profile.md`). Position against IS literature; foundational IS work
(DeLone & McLean, Venkatesh, Orlikowski, Walsham) must appear when relevant. See
`references/README.md`. Always re-verify with `citation-audit` before any enters
the manuscript.
