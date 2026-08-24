## 0.4.3 — 2026-08-24

- **Ideation-first story order** (JL 260824): narratives start at SD02, after
  SD00-ideation and SD01-seed; the map row names the telling's desk-room files.

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

haipipe-page-for-narrative · Changelog
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