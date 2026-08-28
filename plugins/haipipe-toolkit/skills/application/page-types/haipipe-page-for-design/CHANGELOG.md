## 0.6.0 — 2026-08-24

- WARRANT and GRANT separated — a division still warrants from a P page, while a direction card GRANTS InsightBoard pages by path, which 0.5.0's boundary wrongly forbade. Runtime shape corrected (DS<NN> file name, render/ present) and the PageX example made layout-aware.

## 0.5.0 — 2026-08-24

- The design-as-bets family joined the page: `direction/` cards and `design/` units as plugins, units as divisions with per-division acceptance. The citation boundary as then written forbade grants; 0.6.0 corrected it.

## 0.4.0 — 2026-08-21

- The two-boards restructure: token DS, cites P pages, renders live in the page's `render/` plugin.

## 0.3.0 — 2026-08-20

- Renamed from `haipipe-page-for-intervention`; the machine key is now
  `page-type: design`. JL retired the double naming, because one concept
  wearing two words is what made readers ask whether Design and Artifact
  were the same thing. `page-type: design` was free: zero pages declared it
  after its 260819 retirement, and `check.py` already whitelisted the word.
- Absorbed the retired `page-type: artifact`. Acceptance moved from the page
  down to a per-division `accepted:` row, so one unit may be accepted while a
  sibling is mid-revision without a second Page.
- Cut the Page at ACCEPTED. Deploy, shipment records, and measurement rounds
  are no longer this Page's concern; the task layer owns execution and the
  InsightBoard owns the re-read.
- Moved the runtime home to `<DesignTopic>-DesignBoard/1-D-design/` under the two-board split.

## 0.2.0 — 2026-08-20

- Made this the user-facing Design Page while preserving the globally unique
  machine key `page-type: intervention`.
- Changed cardinality from exactly one Intervention to many Design Pages, each
  scoped to one audience × behavior job × primary venue.
- Added Insight Use Map, message/unit map, repeated message divisions, rails,
  variants, and visible-projection acceptance.

- 0.6.1 (260827): the division gains its second terminal — `emitted: <YYMMDD> · <BR00 need id> · <what was missing>`, equal in rank to accepted:, the on-page half of haipipe-design-workflow's EMIT edge; exactly one terminal per division.
