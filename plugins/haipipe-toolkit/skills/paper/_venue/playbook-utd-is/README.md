# UTD-IS Family Playbook (paper/_venue)

A UTD-IS family **style + structure exemplar pack** for the paper pipeline. One pack
covering the three flagship-tier Information Systems journals on the UTD-24 list:
**MISQ** (MIS Quarterly), **ISR** (Information Systems Research, INFORMS), and
**MS-IS** (Management Science, IS department, INFORMS). Its main job is to hold the
CONTENT of similar IS papers (PDFs or extracted text) so we can **imitate their
language style and preferences**, alongside a distilled style profile and concrete
lifecycle-stage mappings. This is a style corpus, not a citation list.

The three journals share roughly 90% of their style and structure (theory-forward
IMRAD, one primary contribution, IS-literature positioning), so they live in one
family pack. Where they diverge (what each rewards, dominant method, theory bar) the
difference is carried as a **per-journal delta** (see Outlets below). That delta IS
the within-family tie-break: pick the family first, then pick the outlet from the
delta table.

## Relationship to the venue layer

- `_venue/README.md` = the venue index + the IS selection table (folded into Outlets
  below).
- `_venue/playbook-utd-is` (here) = **HOW** to shape THIS paper's lifecycle artifacts
  for the UTD-IS family, with verified exemplars to imitate, plus the per-journal
  delta for choosing the outlet.
- This pack supersedes the three single-journal packs (MISQ, ISR, MS-IS), now
  archived under `paper/_archive/_merged-into-utd-is/`; this family pack is the
  merged, delta-served version.

## Structure

```
playbook-utd-is/
  README.md            this hub + family lifecycle mappings + the per-journal delta
  style-profile.md     shared IS style + per-journal style notes + enrich checklist
  exemplars/           stored CONTENT (PDF / text) of similar papers, tagged by journal
                       (misq/ , isr/ , ms-is/)
  references/          citation candidates for related work (secondary; verify before citing)
```

## How to use

At the claims / display / minimap stages, consult this playbook for (a) the
family-shaped target for that artifact (shared by all three journals) and (b) the
per-journal note where the outlets diverge, plus the nearest exemplar paper in
`exemplars/<journal>/`. The concrete outlet is set in the paper's `STATUS.md`
(`venue:`); use the Outlets delta below to pick MISQ vs ISR vs MS-IS when the
decision is still live.

---

## Maps to lifecycle stages (family level)

The four mappings below state what all three journals share. Per-journal divergences
are flagged inline and consolidated in the Outlets delta.

### -> Claims (`0-lifecycle/2-claims`)

Shared across the family:
- Exactly ONE `[primary]` claim, naming the single contribution. 2-4 supporting
  claims (additional tests, robustness, heterogeneity, boundary conditions).
- A method that is novel elsewhere (e.g. an LLM/ML measure from text or reviews) is
  an **enabler** in Methods, NOT a claim, unless framed as a methodological-IS
  contribution that enables a capability and is validated on an IS phenomenon.
- "We apply theory X (TAM/UTAUT/...) to a new context" with no specified mechanism or
  modification is NOT a contribution; an incremental restatement of an
  already-established mechanism is a common rejection reason.
- Borrow from `references/` and `exemplars/`: how exemplar papers in the chosen
  journal state their one-line contribution.

Per-journal note (what the `[primary]` claim IS):
- **MISQ**: the THEORETICAL contribution. A new construct, a specified mechanism, a
  resolved theoretical tension, or (design science) abstracted design principles.
- **ISR**: a tight theory -> hypotheses -> evidence chain. The mechanism / moderator /
  boundary condition specified, OR the first large-scale causal evidence that an IT
  artifact or policy affects an outcome.
- **MS-IS**: the ECONOMIC / ANALYTICAL contribution. A characterized equilibrium, a
  specified mechanism, an identified causal effect, or a recovered structural
  primitive; for market/platform papers the claim usually carries a welfare statement
  (consumer surplus / total welfare), not firm profit alone.

### -> Display (`0-displays`)

Shared across the family:
- Mapping rule: each claim -> one display; the `[primary]` claim -> the hero display;
  any causal claim -> its identification display.
- **Hypothesis-test table** (estimates, standard errors, significance per H) when the
  paper is hypothetico-deductive.
- Construct-measurement / validity table for survey work (AVE, CR, alpha,
  Fornell-Larcker / HTMT).
- **Identification displays** carrying any causal claim: DiD parallel-trends plot
  and/or event-study coefficients; IV first-stage table (report F > 10); RD
  discontinuity plot with bandwidth sensitivity; matching covariate balance table
  (before vs after).

Per-journal note (what the HERO display is):
- **MISQ**: the **research model / theoretical framework figure** (constructs +
  hypothesized relationships), tied to the `[primary]` theory claim; for design
  science add an **artifact figure** + a **design-principles table**.
- **ISR**: the **research model figure** (constructs + directional relationships),
  plus the identification display for any causal claim.
- **MS-IS**: when theory-led, the **analytical-model schematic** (agents, decisions,
  information structure) + the numbered **Propositions / Theorems** table and a
  **comparative-statics figure**; when empirical, the **identification display**
  (DiD event-study / IV first-stage / RD / structural-estimates table); for
  market/platform papers a **market-outcome figure** (prices, two-sided
  participation, network-effect / multi-homing, welfare decomposition).

### -> Minimap (`0-lifecycle/5-minimap`)

Shared across the family: theory-forward IMRAD; an Introduction that opens on an
important IS phenomenon and why it matters, states what prior work established, names
the specific gap, then states this paper's contribution; a Theory & Hypotheses (or
Model) section where each hypothesis (or assumption) traces to a named mechanism,
resisting long undifferentiated H1-H12 lists (reads as fishing); Method executed
rigorously by its own standards; Results that lead with the model/primary result; a
Discussion that restates the contribution first, then implications for IS theory and
practice, then a dedicated limitations paragraph, then conclusion. The `[primary]`
claim drives the abstract contribution sentence, the intro contribution paragraph,
and the first Discussion implication.

Per-journal note (length, abstract shape, structure):
- **MISQ**: Research Article, typical 40-50 pp. **Abstract <= 150 words**,
  unstructured prose, arc phenomenon -> gap -> approach -> theoretical + empirical
  contribution. Theory & Hypotheses uses one primary theory rigorously (resist
  stacking 3-4). Method by its own standards (CMB for surveys; clean identification
  for archival; Hevner/Gregor for design science).
- **ISR**: ~35 pp double-spaced text (excluding references/appendices). **Abstract
  <= 150 words**, unstructured prose, arc IS phenomenon -> gap -> approach
  (data / identification) -> theoretical + empirical contribution. Limitations cover
  endogeneity threats and causality honesty.
- **MS-IS**: ~35 pp text (proofs/robustness/instrument items to online appendix).
  **Structured abstract < 200 words**: Problem definition -> Academic/Practical
  Relevance -> Methodology -> Results -> Managerial Implications. Body is
  economics-style: **Model** (assumptions stated and justified economically) or
  **Empirical strategy** (identification motivated by the same theory as the
  hypotheses); Results = equilibrium characterization + comparative statics
  (analytical) or causal estimates + mechanism channel (empirical); Discussion leads
  with managerial/policy implications derived FROM the formal/identified results.

**Minimap skeleton (shape `ref/minimap-template.tex` to this).** Render the paper
in miniature with the neutral macros (`\pspine` / `spts` / `\cl` / `\dcall` /
`\nnote` / `\pfb`); the section order + abstract form are this venue's:

```text
Abstract            unstructured prose <=150w (MISQ/ISR) | structured <200w (MS-IS);
                    arc: phenomenon -> gap -> approach -> theoretical + empirical contribution
1 Introduction      3 paragraphs: phenomenon/stakes -> gap (vs prior work) -> question + contribution-AS-THEORY
2 Theory & Framing  the construct + ONE named proposition; weave numbered H1..Hk INTO it
                    (each H -> a named mechanism; resist long H1-H12 lists) + boundary / IS positioning
3 Methods           design + data/identification by the venue's own standards (state associational vs causal)
4 Results           R0 sample -> the PRIMARY result first -> supporting results -> rivals ruled out
5 Discussion        contribution restated -> IS theory/practice implications -> limitations -> conclusion
  Supplement        eAppendix SYNCED to 0-sections (proofs / robustness / instrument items, online-only)
```

The `[primary]` claim drives the abstract contribution sentence, the intro
contribution paragraph, and the first Discussion implication. Numbered hypotheses
are woven into the Theory proposition, never a separate section. Live worked
example: `examples/ProjB-PhyTrait-OpioidRx/paper/Paper-Personality2Opioid-MISQ2026/0-lifecycle/5-minimap/5-minimap.tex`.

### -> Write / Edit (language style & preferences)  [the main purpose]

Imitate how IS papers in the chosen journal actually read:
- Consult `style-profile.md` for the shared IS style rules and the per-journal style
  note (MISQ theory-forward/pluralistic; ISR tight theory -> hypotheses -> causal
  empirics; MS-IS economic/analytical/formal-model).
- Read the nearest paper in `exemplars/<journal>/` and mirror its sentence shapes and
  section moves (its style), not its content.
- Apply at the write/edit stages (`3-write-edit`), and to the pitch and abstract.

---

## Outlets (per-journal delta)

This is the within-family tie-break. Pick the family first, then the outlet from the
table. (Folds in the IS selection signals from `_venue/README.md`.)

| Dimension | MISQ (MIS Quarterly) | ISR (INFORMS) | MS-IS (Management Science, IS) |
|-----------|----------------------|---------------|---------------------------------|
| What it rewards | Theoretical depth and a clear theoretical contribution; methodological pluralism | Tight theory -> hypotheses -> evidence chain with strong causal identification and quantitative rigor | Economic mechanism / analytical result; welfare and decision relevance |
| Dominant method | Pluralistic: survey, archival, qualitative/interpretive, design science | Quantitative: causal-identification archival (DiD/IV/RD/matching), surveys, experiments, computational/ML-for-IS; interpretive and design science appear rarely | Analytical models (formal/game-theoretic), causal-identification empirics, structural estimation, hybrid model + empirics |
| Theory bar | Highest theoretical bar; one primary theory used rigorously; new construct / mechanism / resolved tension | Named theoretical mechanism for each hypothesis; tight hypothetico-deductive logic | Economic micro-foundation or formal model; reduced form acceptable only when identification is credible and theory tightly frames the mechanism |
| Typical contribution type | New construct, specified mechanism, resolved theoretical tension, abstracted design principles | Specified mechanism / moderator / boundary, OR first large-scale causal evidence; methodological-IS capability validated on an IS phenomenon | Characterized equilibrium, identified causal effect, recovered structural primitive, welfare result |
| When to pick it | Theory-forward and pluralistic method; design science / IT-artifact evaluation; behavioral or organizational IS | Tight hypothetico-deductive survey/experiment; causal identification on a large-scale IS dataset; computational methods on large-scale data | Causal identification with an economics framing; markets / platforms / economic mechanisms; formal analytical modeling; computational methods on large-scale data |

IS selection signals (from `_venue/README.md`), lean by depth of signal:

| Signal | Lean MISQ | Lean ISR | Lean MS-IS |
|--------|-----------|----------|------------|
| Theory-forward, pluralistic method | ✓ | | |
| Tight hypothetico-deductive, survey/experiment | | ✓ | |
| Causal identification, economics framing | | | ✓ |
| Design science, IT artifact evaluation | ✓ | | |
| Computational methods, large-scale data | | ✓ | ✓ |
| Behavioral theory, organizational IS | ✓ | ✓ | |
| Markets, platforms, economic mechanisms | | | ✓ |

Tie-break order when two journals are still in play: let the DOMINANT METHOD and the
TYPE OF PRIMARY CLAIM decide. Formal model or welfare statement -> MS-IS. New
construct / theoretical tension with pluralistic method -> MISQ. Tight
mechanism -> hypotheses -> clean causal identification -> ISR (or MS-IS if the framing
is explicitly economic). Once chosen, pin it in `STATUS.md` `venue:`; the venue
change re-runs the primary-claim designation (claims couple to venue).

---

## references/ (citation candidates, secondary)

Verified, real IS papers that could be CITED in related work (a SECONDARY use; the
primary purpose of this playbook is style imitation via `exemplars/` +
`style-profile.md`). Position against IS literature, not just management, economics,
or CS; engaging adjacent journals while missing key IS papers is a common rejection
reason. Foundational IS work (DeLone & McLean, Venkatesh, Orlikowski, Walsham) must
appear when relevant for MISQ/ISR; foundational platform / IT-economics work must
appear when relevant for MS-IS. See `references/README.md`. Always re-verify with
`citation-audit` before any enters the manuscript.
