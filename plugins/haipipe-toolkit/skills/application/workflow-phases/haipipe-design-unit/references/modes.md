# Conditional design modes

Load only the mode selected in the frozen config. These rules supplement the
common input/output contract; they never allocate Runs or authorize adoption.

- **compose**: realize the stated goal and constraints. Exploration is bounded
  by the commission; do not require five drafts or a forecast for a simple edit.
- **revise**: read exact base content and feedback; preserve named invariants.
  Produce a new DU. Never edit, rename, or erase the base Result.
- **brainstorm**: the commissioned set contains newly authored, mutually distinct
  candidates. Pin any avoid list and check actual text against it. Each member
  has a short trying/from provenance note (in rationale.md or equivalent):
  from insight names an authorized source, from knowledge names a mechanism,
  intuition is labeled brief-only or informed. Inspiration is not a warrant.
  No experiment allocation, comparator requirement, or forecast is implied.
- **theory-driven**: pin a theory source; distinguish its proposed mechanism
  from an observed effect. The caller explicitly chooses the exploration
  budget, novelty criterion, and rationale/forecast deliverables before release.
  A brief-only audience basis is admissible; name missing knowledge as a gap.
- **challenge**: identify the exact authorized claim being challenged; articulate
  the alternative and what would distinguish it. Do not manufacture measured
  evidence for the alternative.

Additional rationale, ideation summaries, or forecast files are conditional
deliverables. State their required checks in config before work. A forecast
carries assumptions, uncertainty, and failure conditions and is never evidence
of actual effectiveness. Record useful design choices, not private thought logs.

Venue rules remain in application/venue/venue-<kind>/. The caller supplies the
selected pack's path/hash and compiles applicable rules. A UI/visual unit may
delegate rendering to its proper renderer; those tool calls remain internal
unless separately commissioned with their own reusable Result.
