# Nature Portfolio Playbook (paper/_venue)

A Nature Portfolio **style + structure exemplar pack** for the paper pipeline,
covering the within-family choice among `Nature`, `Nature Methods`, and
`Nature Biotechnology`. Its main job is to hold the CONTENT of similar Nature
Portfolio papers (PDFs or extracted text) so we can **imitate their language style
and preferences**, alongside a distilled style profile and concrete lifecycle-stage
mappings. This is a style corpus, not a citation list.

## Relationship to the venue layer

- `_venue/README.md` = the venue index + selection table across venue families.
- `_venue/playbook-nature-portfolio` (here) = **HOW** to shape THIS paper's
  lifecycle artifacts for Nature Portfolio, including the within-family routing
  (flagship `Nature` vs `Nature Methods` vs `Nature Biotechnology`), with verified
  exemplars to imitate.

## Structure

```
playbook-nature-portfolio/
  README.md            this hub + the lifecycle-stage mappings + within-family routing + preflight
  style-profile.md     distilled language style + preferences to imitate
  exemplars/           stored CONTENT (PDFs / extracted text) of similar papers
  references/          official Nature Portfolio source pointers + citation candidates (verify before citing)
```

## How to use

At the claims / display / minimap stages, consult this playbook for (a) the
Nature-Portfolio-shaped target for that artifact and (b) the nearest exemplar paper
in `exemplars/`. The target venue is set in the paper's `STATUS.md` (`venue`). When
the within-family venue is still live, resolve the routing (below) before optimizing
prose. This playbook is about fit and policy; it does not replace the write/edit
stage skills.

## Within-family venue routing

The choice of `Nature` vs `Nature Methods` vs `Nature Biotechnology` is a FRAMING
decision, not a formatting one. Resolve it early.

- **Flagship `Nature`**: default here only when the paper makes a broad conceptual
  advance that matters outside the immediate specialty and can be explained to
  non-specialists without heavy field-specific scaffolding. Prioritize broad
  readership over specialist density; keep title and abstract low-jargon; preserve
  the non-specialist-friendly summary paragraph. If fit is uncertain, test whether
  the broad-readership case is real before optimizing prose too far.
- **`Nature Methods`**: prefer when the central contribution is a method, assay,
  platform, computational approach, or resource whose main claim is enabling power.
  Requires a clear technical advance over available approaches, validation and
  benchmarking against credible baselines, enough detail/protocol access for
  reproducibility, demonstrated general utility (not one narrow showcase), and a
  compelling biological or biomedical application showing why the method matters.
- **`Nature Biotechnology`**: prefer when the value is not just technical novelty but
  biotechnology significance: enabling capability, translational relevance,
  engineering depth, platform utility, or community-scale resource value. Make
  legible why the advance matters for biotechnology or medicine (not one specialist
  benchmark), why the story is substantial enough for a full article, and whether it
  is truly an `Article` or better framed as a `Resource`.

**Article-type check** (do this early, not as formatting cleanup):

- `Article`: full research story with multiple linked claims and a substantial
  evidence chain.
- `Resource`: community-useful dataset, platform, atlas, database, or screening asset
  whose lasting value is broad reuse.
- `Analysis`: integrative or comparative analytical study when the core contribution
  is the analytical insight rather than a new experimental method.
- short-format method/report categories: only when the story is tighter, more
  self-contained, and the journal explicitly supports that format.

If the manuscript keeps oscillating between `method paper` and `resource paper`,
resolve that before rewriting the abstract or Results.

---

## Maps to lifecycle stages

### -> Claims (`0-lifecycle/2-claims`)

- Exactly ONE `[primary]` claim = the BROAD CONCEPTUAL ADVANCE, stated so a
  non-specialist can see why it matters. Nature Portfolio rewards an advance that is
  legible outside the immediate specialty, not just a benchmark win.
- The within-family venue choice (`Nature` vs `Nature Methods` vs
  `Nature Biotechnology`) is itself a framing decision and shapes what the primary
  claim emphasizes: broad significance (flagship), enabling technical power
  (Methods), or biotechnology/translational significance (Biotech).
- 2-4 supporting claims: validation/benchmarking, general utility, reproducibility,
  translational or biological application.
- A method that is novel elsewhere is an **enabler** in Methods, NOT a claim, unless
  the venue is `Nature Methods`/`Nature Biotechnology` where enabling power IS the
  contribution.
- Borrow from `exemplars/`: how comparable Nature Portfolio papers state their broad
  advance in one non-specialist-readable sentence.

### -> Display (`0-displays`)

Nature Portfolio standard display set:
- **Main hero figure**, multi-panel = the HERO, tied to the `[primary]` advance; it
  carries the broad-significance message at a glance for a non-specialist reader.
- Supporting main figures for validation/benchmarking and the key application.
- Extended Data / Supplementary figures for the rigor and reproducibility detail.
- For `Nature Methods`/`Nature Biotechnology`: a benchmarking-comparison panel and a
  utility/application panel are typically load-bearing.
- Mapping rule: each claim -> one display; `[primary]` advance -> the multi-panel
  hero main figure.

### -> Minimap (`0-lifecycle/5-minimap`)

Nature article structure with the non-specialist summary expectation:
- **Title + Abstract / summary paragraph**: low-jargon; the opening summary must let
  a non-specialist grasp the advance and why it matters. End on significance.
- **Main text** (concise; the heavy detail moves to Methods/Supplement): the broad
  advance up front -> what is new -> the evidence chain -> what it enables.
- **Results**: lead with the hero finding; benchmarking and validation follow.
- **Discussion / significance**: restate the broad advance, then implications, limits.
- **Methods** (end-placed, detailed): executed rigorously by the method's standards,
  with reproducibility and protocol access.
- Mapping rule: the `[primary]` advance drives the summary-paragraph significance
  sentence, the opening of the main text, and the first significance statement in the
  discussion.

### -> Write / Edit (language style & preferences)

Imitate how Nature Portfolio papers actually read:
- Consult `style-profile.md` for the distilled style rules (low-jargon prose, the
  summary-paragraph expectation, article-type discipline, significance framing).
- Read the nearest paper in `exemplars/` and mirror its sentence shapes and section
  moves (its style), not its content.
- Apply at the write/edit stages (`3-write-edit`), and to the pitch and abstract.

---

## Nature Portfolio preflight (policy-aware)

Run this before calling a draft submission-ready. These are submission-facing
requirements, not post-acceptance cleanup.

1. **Reporting standards**: confirm whether a reporting summary will be required, and
   that the manuscript and supplement already contain what it will demand.
2. **Data and code availability**: repository names, accession IDs, download links,
   and access restrictions ready to disclose; do not defer the data/code statement.
3. **Protocol and reproducibility readiness**: for methods papers, a clear usable
   protocol path: supplement, protocol repository, or public method record.
4. **Image integrity and raw data**: unprocessed source images and raw blot/gel
   material producible on request; no figure-prep habit that could read as selective
   enhancement.
5. **AI and attribution**: disclose qualifying use of generative AI where required;
   do not treat AI-made images or undisclosed AI-written content as safe by default.
6. **Related-manuscript and preprint disclosures**: disclose preprints, overlapping
   submissions, related manuscripts, and conference-proceedings history when relevant.

Decision order: choose audience and venue family -> choose article type -> check
whether the evidence package matches the venue promise -> only then optimize framing
and prose.

---

## references/ (official sources + citation candidates)

Holds the official Nature Portfolio source pointers (the venue's authority sources
for the routing and preflight above) plus verified, real papers that could be CITED
in related work (a SECONDARY use; the primary purpose of this playbook is style
imitation via `exemplars/` + `style-profile.md`). See `references/README.md`. Always
re-verify with `citation-audit` before any citation enters the manuscript.
