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
