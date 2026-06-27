---
status: open
created: 2026-06-26
updated: 2026-06-26
occurrences: 1
context: lifecycle spine / post-acceptance (raised during npjDM2025 v260626 npj tech-check round)
fixed_in: ""
regressed: ""
---
JL: "I think we should also pay attention to a new lifecycle stage of 'techcheck' or 'camera-ready'. How do you think about this?"

The current spine ends at `review` (peer review + rebuttal). Nothing owns the
POST-ACCEPTANCE production phase: journal technical check, camera-ready prep,
galley proofs. This surfaced while running the npjDM2025 v260626 npj tech-check
round entirely ad hoc (improvised `1-feedback/vYYMMDD/` folder,
`tech-check-revision-plan.md`, deliverable bundle, rebuttal/cover-letter split) --
which is exactly the work a named stage would standardize.

## Design notes (CC, for the future revision pass)
- DISTINCT KIND of work: compliance, not creation. Driven by the venue's
  production rules, not by claims/evidence. Checklist-shaped, round-based, venue-coupled.
- Likely model: a POST-ACCEPTANCE phase appended after `review`, e.g. `production`
  (umbrella) with `tech-check` (journals), `camera-ready` (conferences), and `proofs`
  as venue flavors. NOT a peer of the creative stages (it never touches the science).
- REUSES existing round machinery (`1-feedback/vYYMMDD` is already round-based).
- Would own: (a) a venue-specific compliance checklist in `_venue/playbook-<venue>`
  (npj: IRDM order, declaration statements, figure DPI, reference style, no
  sub-subheadings, equation numbering); (b) a standard round folder (Raw-Comment ->
  revision-plan -> per-point fixes -> bundle: clean + marked-up manuscript, SI PDF,
  individual figures, cover letter, rebuttal); (c) a done-gate (all points addressed
  + clean compile + bundle assembled).
- Naming: prefer a venue-neutral umbrella ("production" or "camera-ready") so it
  covers journals (tech-check / proofs) and conferences (camera-ready) both.
- Proposed spine: seed -> pitch -> claims -> narrative -> display -> minimap -> write/edit -> review -> production
- Caveat: keep it OUT of the creative gates; most of its content is a `_venue`
  checklist, not heavy new skill logic.
