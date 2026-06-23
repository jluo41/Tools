# Patent Playbook (paper/_venue)

A patent-filing **style + structure exemplar pack** for the paper pipeline, which
treats a PATENT FILING as a special kind of paper: the patent is the "paper" and the
patent office / jurisdiction (CNIPA / USPTO / EPO) is the "venue". Its main job is to
hold the CONTENT of similar granted patents (PDFs or extracted text) so we can
**imitate their claim and specification language**, alongside a distilled style
profile and concrete lifecycle-stage mappings. This is a style corpus, not a prior-art
list.

## Relationship to the venue layer

- `_venue/README.md` = the venue index (journals vs the patent track).
- `_venue/playbook-patent` (here) = **HOW** to shape THIS filing's lifecycle artifacts
  for a patent office, with verified granted patents to imitate. It folds the legacy
  patent procedure skills (`playbook-patent`, `prior-art-search`,
  `patent-novelty-check`, `specification-writing`, `patent-review`,
  `jurisdiction-format`) into ONE knowledge pack.

## Structure

```
playbook-patent/
  README.md            this hub + the lifecycle-stage mappings
  style-profile.md     distilled claim/spec language style + preferences to imitate
  exemplars/           stored CONTENT (PDFs / extracted text) of similar granted patents
  references/          prior-art citation candidates (secondary; verify before citing)
```

## How to use

At the claims / display / minimap stages, consult this playbook for (a) the
patent-shaped target for that artifact and (b) the nearest granted patent in
`exemplars/`. The target jurisdiction (CN / US / EP) and patent type (invention vs
utility model) are set in the filing's `STATUS.md` (`venue`).

---

## Maps to lifecycle stages

### -> Claims (`0-lifecycle/2-claims`)

- The PATENT CLAIMS are the legal core. They define the scope of protection: the
  specification supports the claims, not the other way around.
- Exactly ONE `[primary]` independent claim = the broadest statement of the core
  inventive concept. The bar is legal, not academic: **novelty** (no single prior-art
  reference discloses every element) and **non-obviousness / inventive step** (no
  motivated combination of references renders it obvious).
- Independent claims (method + system + product) state the inventive concept; each
  dependent claim narrows it and provides a fallback position during prosecution.
- Utility model (实用新型, CN only): apparatus/device claims ONLY, no method claims;
  the inventive-step bar is lower.
- Patent novelty is absolute and worldwide: any public disclosure before the priority
  date counts. Research novelty ("has anyone published this?") is NOT patent novelty.
- A method that is merely standard practice elsewhere is an **enabler** in the
  specification, NOT a claimed contribution.
- Borrow from `exemplars/`: how granted patents phrase claim 1 and structure the
  independent / dependent hierarchy.

### -> Display (`0-displays`)

Patent DRAWINGS / figures are the display set:
- **FIG. 1, FIG. 2 ...** block diagrams, flowcharts, schematics that show the
  structure or steps of the claimed invention.
- Every component / step carries a **reference numeral** (e.g. 102, 202) that is
  consistent across every figure and every mention in the specification.
- Mapping rule: the `[primary]` independent claim -> the hero figure (FIG. 1) that
  depicts the core inventive concept; each dependent feature -> a figure or a labeled
  element it relies on.
- No experimental plots, no result charts: drawings show what is claimed, not how
  well it performs.

### -> Minimap (`0-lifecycle/5-minimap`)

Patent SPECIFICATION STRUCTURE (the "paper" outline), in filing order:
- **Title** (发明名称): matches the broadest claim; no "improved" / "new" / "novel",
  no trademarks.
- **Technical Field** (技术领域): the broad domain, then the specific area.
- **Background** (背景技术): closest prior-art approaches and their specific TECHNICAL
  deficiencies; not a literature review, not commercial or social framing.
- **Summary** (发明内容): technical problem -> technical solution (supports every claim
  element) -> advantages (qualitative, structural; NO numerical results).
- **Brief Description of Drawings** (附图说明): one line per FIG.
- **Detailed Description** (具体实施方式): at least one complete embodiment with
  reference numerals; enables a POSITA to make and use the invention; covers
  alternatives for broader claim interpretation.
- **Claims** (权利要求书): independent + dependent.
- **Abstract** (摘要): field -> problem -> core solution -> advantage, within the
  jurisdiction word limit.

Per-jurisdiction delta (set in `STATUS.md`):

| Element | CN (CNIPA) | US (USPTO) | EP (EPO) |
|---|---|---|---|
| Claim form | "其特征在于" two-part | single-clause "comprising" | two-part "characterised in that" (Rule 43(1)) |
| Spec order | 名称/领域/背景/内容/附图/实施方式 | Title/Field/Background/Summary/Drawings/Detailed/Abstract | Title/Field/Background Art/Disclosure/Embodiments/Drawings/Reference Signs List |
| Reference signs list | within 附图说明 | inline | MANDATORY separate list (Rule 42) |
| Abstract limit | <=300 Chinese chars | <=150 words / 2500 chars | ~150 words, no merits |
| Drawings label | 图1 | FIG. 1 | FIG. 1 / Figure 1 |
| Utility model | available (10 yr, apparatus claims only, formal exam) | not available | not available |
| Invention patent | 20 yr, substantive exam | 20 yr, substantive exam | 20 yr, substantive exam |

- Mapping rule: the `[primary]` independent claim drives the Title, the Summary's
  technical-solution sentence, and the Abstract's core-solution sentence.

### -> Write / Edit (language style & preferences)  [the main purpose]

Imitate how granted patents actually read:
- Consult `style-profile.md` for the distilled style rules (single-sentence claim
  convention, antecedent basis, "comprising", means-plus-function caution, spec tone,
  per-jurisdiction language notes).
- Read the nearest granted patent in `exemplars/` and mirror its claim phrasing and
  specification section moves (its style), not its content.
- Apply at the write/edit stages (`3-write-edit`), and to the title and abstract.

#### Drafting process (the filing's lifecycle)

The consolidated patent pipeline IS the filing's lifecycle, and it is folded into this
pack as KNOWLEDGE (it replaces the six legacy procedure skills):

1. **Prior-art search**: search patent databases (Google Patents, Espacenet) and
   academic literature; classify by IPC/CPC; flag overlap risk and freedom-to-operate.
2. **Patentability / novelty**: anticipation analysis (single-reference test) then
   obviousness analysis (motivated combination); assess under 102/103 (US), Art 22
   (CN), Art 54/56 (EP).
3. **Claims drafting**: design the independent / dependent hierarchy; ONE primary
   independent claim defines the broadest defensible scope.
4. **Specification**: write Title, Technical Field, Background, Summary, Brief
   Description of Drawings, Detailed Description, Abstract; verify every claim element
   has written-description support.
5. **Examiner-style review**: examiner persona issues an office action on clarity,
   written description, enablement, novelty, non-obviousness, claim scope; fix
   CRITICAL/MAJOR before proceeding.
6. **Jurisdiction format**: compile into the target office's filing format(s); never
   mix jurisdiction formats; claim content identical across jurisdictions, only the
   format differs.

---

## references/ (prior-art candidates, secondary)

Verified, real patents and papers that could be CITED as prior art (a SECONDARY use;
the primary purpose of this playbook is style imitation via `exemplars/` +
`style-profile.md`). Prior art positions the Background and bounds the claims; it
includes everything published before the priority date, worldwide, not just patents.
Never fabricate a patent number or citation. See `references/README.md`. Always
re-verify with `citation-audit` before any enters the filing.
