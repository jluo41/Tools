## 0.2.0 — 2026-08-19

- **Renamed `for-opening` to `for-seed`, and made VENUE-FREE by rule.** JL 260819:
  "maybe we can change it to Seed (which is venue free). And narrative, it is
  venue embedded, each of them should have it."
- The venue-aligned layer this contract already named (selected venue, audience,
  editor question, pitch, framing) moves to `haipipe-page-for-narrative`, one per
  venue.
- The layers were already separated here, with retargeting told to "reread the
  first layer and rewrite the second". Making them two PAGES is what makes the
  stable half provably untouched: a page whose second half is rewritten per venue
  cannot also be the readable record of what the paper is about.
- A seed that names a venue is now a defect.

haipipe-page-for-seed · Changelog
====================================

Historical notes retained from the former Opening contract. New development is
documented by the current Seed contract and repository history.

## 0.1.0 - 2026-08-17

- Added one Opening Page Type per paper.
- Opening owns paper identity, research question, source-page inventory, headline establishment and limit, venue position, editor promise, and the bounded handoff to Narrative.
- PageX reads existing Pages while Probe remains a parallel route to Task and Discovery folders; Opening owns no local Probe folder.
- Legacy Seed, Venue, and Pitch pages remain readable compatibility inputs until an explicit runtime migration.
