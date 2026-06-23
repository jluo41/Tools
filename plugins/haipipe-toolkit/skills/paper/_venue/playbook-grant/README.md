# Grant Playbook (paper/_venue)

A playbook-grant **style + structure exemplar pack** for the paper pipeline. It
treats a grant proposal as a special kind of paper: the proposal is the "paper",
the funding agency is the "venue". Its main job is to hold the CONTENT of similar
FUNDED proposals (PDFs or extracted text) so we can **imitate their persuasive
style and reviewer preferences**, alongside a distilled style profile and concrete
lifecycle-stage mappings. This is a style corpus, not a citation list.

## Relationship to the venue layer

- `_venue/README.md` = the venue index (which journal / agency a paper targets).
- `_venue/playbook-grant` (here) = **HOW** to shape THIS proposal's lifecycle
  artifacts for a funding agency, with verified funded proposals to imitate.
  Sibling packs: `playbook-misq`, `playbook-isr`, `playbook-ms-is`.
- The deep agency knowledge (KAKENHI, NSF, NSFC 面上/青年/优青/杰青/海外优青/重点,
  ERC, DFG, SNSF, ARC, NWO, generic) is carried in the `playbook-grant/` skill;
  this pack distills its structure and tone into lifecycle-stage targets.

## Structure

```
playbook-grant/
  README.md            this hub + the lifecycle-stage mappings
  style-profile.md     distilled grant-writing style + preferences to imitate
  exemplars/           stored CONTENT (PDFs / extracted text) of FUNDED proposals
  references/          citation candidates for prior work (secondary; verify before citing)
```

## How to use

At the claims / display / minimap stages, consult this playbook for (a) the
grant-shaped target for that artifact and (b) the nearest funded proposal in
`exemplars/`. The target agency (and sub-program) is set in the proposal's
`STATUS.md` (`venue`), which selects the per-agency delta in the minimap.

---

## Maps to lifecycle stages

### -> Claims (`0-lifecycle/2-claims`)

- Exactly ONE `[primary]` claim = the central CONTRIBUTION of the grant, expressed
  as the Specific Aims / hypotheses. Every agency asks "what is the contribution,
  and why does it matter to us?"; the primary claim must answer it: the single most
  important aim, the gap it closes, and the Significance + Innovation framing.
- 2-4 supporting claims: the remaining aims, each independently valuable so that if
  one aim fails the others still deliver; preliminary-data feasibility; PI track
  record; broader impact / societal significance.
- A method that is novel elsewhere (e.g. a known technique applied here) is an
  **enabler** in the Approach, NOT a contribution.
- Frame the gap for THIS agency: what is unknown, why now, and why it matters
  (scientific significance plus the agency's mission: Broader Impacts for NSF,
  社会的意義 for KAKENHI, 国际前沿 for NSFC, high-risk/high-gain for ERC).
- Borrow from `references/`: how funded proposals state their one-paragraph aim and
  significance.

### -> Display (`0-displays`)

Grant-family standard display set:
- **Conceptual framework / overview diagram** (aims and how they connect, shared
  resources, outputs) = the HERO, tied to the `[primary]` aim. The single most
  important figure in a proposal.
- **Preliminary-data figures** (pilot results that de-risk each aim).
- **Timeline / Gantt chart** (year-by-year or quarter-by-quarter milestones and
  deliverables).
- **Budget-justification table** (cost categories mapped to aims; narrative only,
  amounts left as `[AMOUNT]` placeholders).
- Mapping rule: each aim -> one display; `[primary]` aim -> hero overview diagram.

### -> Minimap (`0-lifecycle/5-minimap`)

A grant follows a feasibility-forward arc, NOT the paper IMRAD arc:

```
Problem -> Why Now -> What We Propose -> Why It Will Work -> What We Will Deliver
```

The proposal SECTION STRUCTURE differs per agency. Set the agency in `STATUS.md`,
then apply the matching delta below.

| Agency | Section structure (the delta) |
|--------|-------------------------------|
| **NSF** | Project Summary (1p: Overview / Intellectual Merit / Broader Impacts) + Project Description (15p, Aim-based) + References Cited + Results from Prior Support |
| **NSFC 面上** | 立项依据 (rationale and significance) / 研究内容 / 研究目标 / 研究方案 / 可行性分析 / 创新性 / 预期成果 / 研究基础 (emphasis on scientific problem and accumulation) |
| **NSFC 青年** | same backbone as 面上, weighted toward independence and growth potential (age <=35) |
| **KAKENHI** | 概要 (summary) / 研究目的 (objective) / 研究計画・方法 (plan and methods) / 準備状況 (preparation) plus explicit 年次計画 |
| **ERC** | Extended Synopsis (5p, self-contained) + Scientific Proposal Part B2 (15p) with a WP / deliverables / milestones table |
| **GENERIC** | user-supplied section names, page limits, and review criteria |

- Mapping rule: the `[primary]` aim drives the Project Summary / 概要 / Extended
  Synopsis, the significance section, and the first deliverable in the timeline.

### -> Write / Edit (language style & preferences)  [the main purpose]

Imitate how funded proposals actually read:
- Consult `style-profile.md` for the distilled style rules (significance-first
  framing, aim-statement phrasing, reviewer-skimmable structure, persuasive but
  rigorous tone, per-agency tone notes).
- Read the nearest funded proposal in `exemplars/` and mirror its sentence shapes
  and section moves (its style), not its content.
- Apply at the write/edit stages (`3-write-edit`), and to the Specific Aims and
  summary, which the panel reads first.

#### Agencies (structure, from the `playbook-grant/` skill)

| Agency | Structure backbone | Review lens |
|--------|--------------------|-------------|
| **KAKENHI** | 研究目的 / 研究計画・方法 / 準備状況 / 人権の保護 | 学術的重要性, 独創性, 計画の妥当性, 遂行能力 |
| **NSF** | Project Summary / Project Description (Aims) / References / Biosketch / Budget Justification / Data Management Plan | Intellectual Merit, Broader Impacts |
| **NSFC** | 立项依据 / 研究内容 / 研究目标 / 研究方案 / 可行性分析 / 创新性 / 预期成果 / 研究基础 | 科学意义, 创新性, 可行性, 研究队伍 |
| **ERC** | Extended Synopsis (5p) + Scientific Proposal Part B2 (15p) | Ground-breaking nature, Methodology, PI track record |
| **DFG** | State of the Art / Objectives / Work Programme / Bibliography / CV | Scientific quality, Originality, Feasibility, PI qualification |
| **SNSF** | Summary / Research Plan / Timetable / Budget | Scientific relevance, Originality, Feasibility, Track record |
| **ARC** | Project Description / Feasibility / Benefit / Budget | Research quality, Feasibility, Benefit to Australia |
| **NWO** | Summary / Proposed Research / Knowledge Utilisation | Scientific quality, Innovative character, Knowledge utilisation |
| **GENERIC** | user-supplied sections, page limits, criteria | user-supplied |

---

## references/ (citation candidates, secondary)

Verified, real prior work that could be CITED in the proposal's background /
related work (a SECONDARY use; the primary purpose of this playbook is style
imitation via `exemplars/` + `style-profile.md`). Position the gap against the
existing literature and against competing FUNDED projects (KAKEN, NSF Award
Search, NSFC databases). See `references/README.md`. Always re-verify with
`citation-audit` before any enters the proposal bibliography; never fabricate a
citation, a grant, or a PI credential.
