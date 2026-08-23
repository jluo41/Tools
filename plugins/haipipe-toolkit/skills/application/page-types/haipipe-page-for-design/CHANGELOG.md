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
