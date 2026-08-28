# Paper Page architecture: compose a paper from accepted Pages

spine: Ideation ranks a direction's ideas and sends one to a Seed; Seed fixes the venue-free paper identity; Roadmap plans the campaign and registers what comes back, lap by lap; Narrative orders claims for one desk; Section executes one Narrative row; Round routes feedback; the venue bank is a library this board points at rather than holds.
dialect: paper
paper-root: _fixture
close: The Page Types, the Paper composition boundary, and the validation route agree with the shipped six-phase journey; the venue bank has its own board and is not registered here; retired stage-era designs were deleted 260822 and are not registered as live Pages.
session: 8d4c966d-8db2-443b-9194-8dcb8a14b600

## Topic

This Board explains the current Paper architecture.
The useful design work now lives on typed Pages, so the Paper door stays small.
It selects Pages, runs their shared lifecycle, assembles accepted outputs, and does not maintain a second stage engine.
Since 260824 the family also has a journey: `haipipe-paper-workflow` (0.6.0, JL 260828) names six phases after their authority pages and owns the gates between them, never the content.

- **QA · Architecture** fixes the Page graph, the journey, and ownership boundaries.
- **QBt · Page Types** carries one current specimen for each of the seven Paper Page Types.
- **QC · Composition and validation** explains the thin Paper door, Page-local plugins, and the tests that prove their route.

The old Delivery, Delivery Element, stage Engine, and engine-skill mirror groups were retired 260820 and DELETED 260822 under the family's retired-means-deleted policy.
They are historical design evidence in git history only, not active Paper routes and not folders on this board.

## Pipeline

```text
P0 Ideation (ideate)    💭 SD00 · repo minted with this page · G0 novelty + pilot + PROCEED
P1 Seed (establish)     🌱 SD01 · venue-free · E-board with novelty column
P2 Roadmap (route)      🗺 SD02 · BLOCK rows serving E-rows · ✋ released · receipts land lap by lap
   ↺ P1↔P2 = the establish loop · exits only through the Seed at G4
P3 Narrative (tell)     🧭 NA · one per desk · §1 IS the venue decision
P4 Section (realize)    📄 one per map row · assemble = a verb at G6, not a phase
P5 Round (respond)      🔁 in the desk's B group · routes each concern once → Seed/Narrative/Section

📚 Venue = library, never a phase: the QBv bank is consulted at P3 §1
gates G0–G7 live in haipipe-paper-workflow; a person or CHECK declares them, never a timer

Probe (every Page, every phase)
  ├── existing Board Pages ── PageX ── runs in OUTLINE ──┐
  └── Task / Discovery ────── QA Probe ── PROBE/EVIDENCE ─┴─▶ owning Page evidence

`/haipipe-paper status [family]` = regenerated measurement over Pages and
plugin units, a command retired from being a sixth Page Type (dash) on 260820
```

Probe is the evidence-acquisition family with two typed lanes.
PageX reads bounded context from existing accepted Pages during OUTLINE.
QA Probe asks unresolved Task or Discovery questions during PROBE/EVIDENCE and lands the answer on the consuming Page.
The lanes remain physically separate as `pagex/` and `probe/`.

## Board Structure

```text
PaperSkillBoard-260725/
├── 1-QA-architecture/       current graph, journey, and boundaries
├── 2-QBt-page-types/        seven live Paper Page Type specimens
├── 3-QC-composition/        Paper composition and validation
├── _fixture/                minimal paper-graph validation material
├── _fieldtest/              friction logs from field-repair sessions
├── _tools/                  board-local adapters and shots
└── board/                   generated site, never hand-edited
```

The retained numeric prefixes preserve stable historical paths.
`## Pages` is the live registry.

## Related Folders

@ ../../paper/ | Current Paper family
- README.md
- haipipe-paper/SKILL.md
- haipipe-paper-workflow/SKILL.md
- page-types/
@ ../../board/haipipe-page/ | Shared Page contract
- SKILL.md
@ ../../board/page-plugins/ | Shared Page plugins
- haipipe-plugin-pagex/SKILL.md
- haipipe-plugin-probe/SKILL.md

## Pages

### QA · Architecture
The smallest graph that explains where paper decisions and evidence live.

```text
QA1  Page graph and journey
QA2  ownership boundary
```
QA1-paper-page-graph.md
QA2-ownership-boundary.md

### QBt · Page Types
One live specimen for each Page Type owned by the Paper family, listed in journey order; ids are historical and stable.

```text
QBt6 Ideation   direction's ideas, page zero        (id re-minted 260828)
QBt1 Seed       stable identity + E-board
QBt7 Roadmap    campaign plan and intake, one page
QBt2 Venue      external desk · library, never a phase
QBt3 Narrative  venue-aligned claim and section map
QBt4 Section    one executable Narrative row
QBt5 Round      one feedback cycle
```
QBt6-for-ideation.md
QBt1-for-seed.md
QBt7-for-roadmap.md
QBt2-for-venue.md
QBt3-for-narrative.md
QBt4-for-section.md
QBt5-for-round.md

### QC · Composition and validation
How the thin Paper door composes typed Pages, delegates evidence/build work to Page-local plugins, and proves that route works.

```text
QC1  Paper routing and assembly
QC2  PageX, Probe, Bibex, Display, LaTeX, and Word boundaries
QC3  minimal paper graph fixture
QC4  fresh-context agent behavior
```
QC1-paper-door.md
QC2-page-local-plugins.md
QC3-minimal-fixture.md
QC4-fresh-agent-run.md

## Links

## Log

260820 · Replaced the stage-era Board registry with the six-type Page architecture.
260820 · Kept all sixteen Venue Pages live and archived the former QA, Delivery, QBt, Engine, and Execute groups intact.
260820 · Grouped PageX under Probe while preserving separate PageX and Task/Discovery QA records.
260820 · Merged validation into QC because the fixture and fresh-agent run prove the same composition contract.
260820 · Retired Dash (QBt6) as a sixth Page Type: JL proposed merging it into Narrative, but only one of its four families (section) was Narrative-shaped, so the merge was rejected in favor of dropping it outright. It survives as `/haipipe-paper status [family]`, a command, not a Page Type. QBt6 moved to `_archive/5-QBt6-dash-retired-260820/`.

260824 · The venue bank LEFT this board for `../../paper/venue/bank/`. It was a live library (seventeen desk pages, bound by real paper boards through pagex) parked inside an architecture explainer that had gone a generation stale, and it refreshes on each desk's clock rather than this board's. `_tools/sync-exemplars.py` went with it, because only venue pages run it. What stays here is the explainer, which is itself a generation behind and is being rebuilt: it still describes five Page Types where the family now has eight, and no journey at all.

260828 · Field repair brought the explainer back level with the shipped family (journey 0.6.0). The registry now carries seven Page Types: QBt6-for-ideation (the QBt6 id re-minted; its Dash-era meaning ended 260820 and the `_archive/` that held it was deleted 260822 with the rest of the stage era) and QBt7-for-roadmap join the five, with Roadmap having absorbed the short-lived Collection page this morning (roadmap 0.3.1, journey 0.6.0). The Pipeline is now the six-phase journey with the establish loop and gates G0–G7; the close line and Topic drop the `_archive/` claim, since retired means deleted; QBt3/QBt4 move off the grandfathered `0-SD-seed/` and `SC/SA` grammar onto `A1-SD-story/ · A2-NA-narrative/ · B<x>-<desk>/`; QA2/QC3/QC4's dead `4-QC-composition/` paths are re-pointed at `3-QC-composition/`. QC4's receipt stays scoped to the five-type run it actually observed; the journey's own field record (G0 G2 G3 G4 fired live, G5–G7 never) is registered beside it. Frictions in `_fieldtest/friction-log-260828.md`.
