# MS-IS Playbook (paper/_venue)

A Management Science (Information Systems department) **style + structure exemplar
pack** for the paper pipeline. Its main job is to hold the CONTENT of similar MS-IS
papers (PDFs or extracted text) so we can **imitate their language style and
preferences**, alongside a distilled style profile and concrete lifecycle-stage
mappings. This is a style corpus, not a citation list.

## Relationship to the venue layer

- `_venue/README.md` = the venue index + IS selection table (MISQ vs ISR vs MS-IS).
- `_venue/playbook-ms-is` (here) = **HOW** to shape THIS paper's lifecycle artifacts
  for the IS department of Management Science, with verified exemplars to imitate.
  Sibling packs: `playbook-misq`, `playbook-isr`.

## Structure

```
playbook-ms-is/
  README.md            this hub + the lifecycle-stage mappings
  style-profile.md     distilled language style + preferences to imitate
  exemplars/           stored CONTENT (PDFs / extracted text) of similar papers
  references/          citation candidates for related work (secondary; verify before citing)
```

## How to use

At the claims / display / minimap stages, consult this playbook for (a) the
MS-IS-shaped target for that artifact and (b) the nearest exemplar paper in
`exemplars/`. The target venue is set in the paper's `STATUS.md` (`venue`).

---

## Maps to lifecycle stages

### -> Claims (`0-lifecycle/2-claims`)

- Exactly ONE `[primary]` claim = the ECONOMIC / ANALYTICAL contribution. MS-IS asks
  "what is the economic mechanism or analytical result?" every time; the primary
  claim must answer it: a characterized equilibrium, a specified mechanism, an
  identified causal effect, or a recovered structural primitive.
- 2-4 supporting claims: comparative statics, welfare results, robustness of
  identification, structural-vs-reduced-form agreement, boundary conditions.
- A method that is novel elsewhere (e.g. LLM-from-reviews) is an **enabler** in
  Methods, NOT a claim.
- A reduced-form finding with no formal theory or micro-foundation is NOT a
  contribution; "we apply a behavioral IS model (TAM/UTAUT) to a new context"
  without economic grounding is NOT a contribution.
- For market/platform papers the primary claim usually carries a welfare statement
  (consumer surplus / total welfare), not firm profit alone.
- Borrow from `references/`: how exemplar MS-IS papers state their one-paragraph
  economic contribution.

### -> Display (`0-displays`)

MS-IS-family standard display set:
- **Analytical-model results** = the HERO when the paper is theory-led: the model
  schematic (agents, decisions, information structure) plus the numbered
  **Propositions / Theorems** table, tied to the `[primary]` analytical claim.
- **Comparative-statics figure**: how the equilibrium moves with key parameters.
- **Identification display** for empirical papers: DiD event-study plot (parallel
  trends + dynamic effects), IV first-stage / RD discontinuity plot, or structural
  estimates table (recovered primitives + counterfactual).
- **Market / platform outcome figure**: prices, two-sided participation,
  network-effect / multi-homing outcomes, welfare decomposition.
- Mapping rule: each claim -> one display; the `[primary]` claim -> hero model-result
  or hero identification display.

### -> Minimap (`0-lifecycle/5-minimap`)

MS-IS article (~35 pp text; proofs/robustness/instrument items to online appendix),
economics-style structure:
- **Structured abstract** (<200 words): Problem definition -> Academic/Practical
  Relevance -> Methodology -> Results -> Managerial Implications.
- **Introduction**: the market failure / coordination problem (analytical) or the
  economic mechanism through an IT artifact / digital market (empirical) -> what
  prior work established but did not identify or resolve -> this paper's contribution.
- **Model** (or **Empirical strategy**): assumptions stated and justified
  economically; identification strategy motivated by the same theory as the
  hypotheses.
- **Results**: equilibrium characterization + comparative statics (analytical), or
  causal estimates + mechanism channel (empirical); for hybrid papers the model
  generates predictions and the empirics test them.
- **Discussion**: managerial and policy implications derived FROM the formal /
  identified results, then limitations, then conclusion.
- Mapping rule: the `[primary]` claim drives the abstract Results sentence, the intro
  contribution paragraph, and the first managerial implication in Discussion.

### -> Write / Edit (language style & preferences)  [the main purpose]

Imitate how MS-IS papers actually read:
- Consult `style-profile.md` for the distilled style rules (economic framing,
  formal-notation discipline, identification honesty, mechanism-first phrasing, the
  analytical/empirical intro recipes, structured-abstract shape, tone).
- Read the nearest paper in `exemplars/` and mirror its sentence shapes and section
  moves (its style), not its content.
- Apply at the write/edit stages (`3-write-edit`), and to the pitch and abstract.

---

## references/ (citation candidates, secondary)

Verified, real Management Science / economics-of-IS papers that could be CITED in
related work (a SECONDARY use; the primary purpose of this playbook is style
imitation via `exemplars/` + `style-profile.md`). Position against the economics,
OR, and management-science literature, not IS only; foundational platform /
IT-economics work must appear when relevant. See `references/README.md`. Always
re-verify with `citation-audit` before any enters the manuscript.
