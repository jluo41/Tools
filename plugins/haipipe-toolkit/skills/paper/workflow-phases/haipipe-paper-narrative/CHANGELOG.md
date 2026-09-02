## 0.7.1 · 260901
- Corrected the abstraction boundary: the Section-control table is view 2 inside the existing `## Diagram`, not a new surface between Diagram and Content. The Page's large structure remains unchanged.

## 0.7.0 · 260901
- Narrative now requires a reader-order Diagram followed immediately by one Narrative Control Table: one live Section per row, with reader job, outline shape, must-say, must-not-say, evidence gate or cut rule, and reader exit.
- The table is an executive compression of claims, arc, reader journey, detailed Section rows, and handoffs; disagreement between those surfaces reopens Narrative.
- Optional evidence must carry an explicit cut rule and may not appear necessary for the sufficient paper.

## 0.6.1 · 260831
- Narratives close the story group as Story<NN>-narrative-<desk> (JL 260831); a separate A2-NA-narrative group with NA numbering is grandfathered.

## 0.6.0 — 2026-08-31

- **Renamed and moved** (JL 260831: "replace page-types to be workflow-phases"):
  `paper/page-types/haipipe-page-for-narrative/` is now `paper/workflow-phases/haipipe-paper-narrative/`.
  The skill is one paper JOURNEY PHASE and still owns its `page-type:` key;
  a new `## 🧭 Journey phase` block places the phase and its gates, and the
  description carries the P-number. Contract body unchanged.

## 0.5.0 — 2026-08-24

- **Narratives move out of the story group** (JL 260824, journey 0.5.0):
  home is now `A2-NA-narrative/NA<NN>-narrative-<desk>`, one page per desk in
  arrival order, token NA. The story group becomes the venue-free P0-P3 head
  (ideation, seed, roadmap, collection); SD-numbered narratives grandfathered.

## 0.4.4 — 2026-08-24

- **Ideation 0.5.0 vocabulary** (JL 260824): the story-group figure's SD00
  line reads "the ideas · the story's page zero". No mechanics changed.

## 0.4.3 — 2026-08-24

- **Ideation-first story order** (JL 260824): narratives start at SD02, after
  SD00-ideation and SD01-seed.

## 0.4.2 — 2026-08-24

- **The map row names the telling's DESK ROOM files**
  (`<N>-<desk><year>/sections/...`), because each telling owns a
  self-contained room with its own displays/ copies and reference.bib per the
  door's room law; board address is `0-paperboard/`. (Entry added in the
  260824 family audit, which found the version named in the summary with no
  log row here.)

## 0.4.1 — 2026-08-23

- Runtime home renamed to `paperboard/A1-SD-story/` under the 260823 scaffold
  grammar; `0-SD-seed/` boards are grandfathered. Content otherwise unchanged —
  this keeps the file in agreement with seed 0.4.0. (Entry added in the 260823
  family review, which found the SKILL bumped to 0.4.1 with no log row here.)

## 0.4.0 — 2026-08-21

- **One folder for the story** (JL 260821: "put the narrative and seed into one
  single folder"): Narratives live beside the Seed in the `0-SD-seed/` group as
  `SD<NN>-narrative-<venue>` pages, sharing `group-token: SD`. Same shape as an
  InsightBoard's MT group: SD00 says what the paper IS, SD01+ say how it is
  TOLD. Group law: the story group decides the telling; no manuscript prose.
- **The claim law**: every claim row names its Seed E-row parent. ✅ parent
  licenses any role; 🔨 caps the role at provisional; no parent is a defect
  with two exits (add the E-row to the Seed, or drop the claim). A claim may
  narrow its parent and never broaden it.
- **Division 1 is the paper's venue DECISION**, matching Venue 0.3.0's
  consumer-neutral bank: it binds the shared QBv page through pagex/, owns
  category choice and fit, and quotes no desk rule without the binding.
- **Staleness wired one hop**: a Seed E-row flip reopens citing claims; a bank
  Venue Page refresh reopens division 1. Marks travel by citation.
- Frontmatter gains version, summary, and the shared `group-token: SD`.

## 0.3.0 — 2026-08-19

- **ONE narrative page per VENUE**, new `per: venue` key (JL 260819: "narrative,
  it is venue embedded, each of them should have it").
- It now owns the venue-aligned layer that arrived from `for-opening` → `for-seed`:
  selected venue, audience, editor question, pitch, framing. That contract had
  already labelled the layer venue-aligned; making it a page of its own stops a
  retarget from touching the paper's stable identity.
- Retargeting CREATES a narrative page rather than rewriting one. A narrative page
  that does not name its venue is a defect.

haipipe-paper-narrative · Changelog
======================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match
SKILL.md frontmatter `version:`. Newest first.

**v0-series rule:** inherited from `haipipe-board`; this skill stays on `0.x.x` and
never reaches `1.0.0` without JL's explicit say-so.

## 0.2.0 - 2026-08-17

- Recast Narrative as the story architecture between Opening and Section.
- It reads the accepted Opening, venue blueprint, and existing source Pages through PageX; it owns claim roles, argument arc, reader journey, Section map, source allocation, display moments, and Section handoffs.
- It no longer absorbs Seed, Claims, Venue, or Pitch and does not own evidence discovery or section prose.
- `for-argument` and `for-paper-map` are deliberately not separate types; both responsibilities live inside Narrative.
- PageX and Probe remain parallel: PageX reads existing Pages, while Probe reaches Task and Discovery folders through their owning evidence Pages.

## 0.1.1 - 2026-08-10

Narrative now owns the claim-to-display selection gate. It reads the candidate cards paired with
Value and Literature probes, selects only those serving a named claim and rhetorical role, and
allows only those selected cards to request a formal Paper Display. Evidence remains on its probe
and candidate card; formal rendering, acceptance, and placement remain on the Paper Display unit.

## 0.1.0 - 2026-08-09

First cut of the NARRATIVE page, on JL's 260809 paper-group redesign.

- Absorbs seed, claims and pitch (JL 260809) and adds the section-by-section outline every Section page executes.
- Keeps the venue-free core (the claim ledger) as its own division, so a retarget rereads it instead of rewriting it.
- The real page already carried all four: its Opening asks what argument order makes C1 the peak while C2 and C3 establish consequence and boundary.
- Ships under `paper/page-types/` because the paper family owns it (JL 260809,
  page-types are the page versions of a skill set).
- Loads `haipipe-page` for the base frame and `haipipe-page-for-stage` for the
  family grammar; restates neither.
