# CHANGELOG · haipipe-paper

## 0.7.1 · 260904

- Keep the shared Outline presenter at the Page surface and load only its exact
  material refs inside concrete Paper Page phases.

## 0.7.0 · 260904

- Separate family-entry routing from the canonical concrete Page RUN order.
- Replace the active Probe/PageX/plugin-lane model with one shared Outline
  plugin and typed VALUE/CITE/DISPLAY local Results over Supporting/local Runs.
- Add CONTEXT to the Paper Page loop and update status/folder/desk-room
  language to current evidence identities.

## 0.6.0 · 260901
- Active Section Page IDs are full semantic names: `S-<desk>-Main-<section-name>` and `S-<desk>-Appendix-<section-name>`. Reading order belongs in the Board Map, not in an opaque ordinal. Legacy `S<D><NN>` and `SA<NN>` identifiers are archive-only compatibility forms.

## 0.5.0 · 260831
- One letter per B group (JL 260831 "Ba to be Main, Bb to be Appendix, Bc to be Round"): first desk Ba-<desk>-Main · Bb-<desk>-Appendix · Bc-<desk>-Round, a second desk continues at Bd; shared-letter (0.4.x) and combined-group layouts grandfathered. Live: Ba-MISQ-Main/Bb-MISQ-Appendix/Bc-MISQ-Round, Ba-JAMA-IM-Main/Bb-JAMA-IM-Appendix.

## 0.4.1 · 260831
- Desk name keeps its capitals in group folders (JL: "make MISQ capitalized"): Ba-MISQ-Main/-Appendix/-Round; only the arrival letter is lowercase. MISQ board also capitalized the desk in Story03-narrative-MISQ and RD01-MISQ-feedback-20260825; desk rooms (1-misq2026/) and venue bank ids (QBv1-misq) keep their own conventions.

## 0.4.0 · 260831
- Desk layer split three ways (JL 260831 "I want to make Ba-misq into three page groups"): B<x>-<desk>-Main (S<D> units) · B<x>-<desk>-Appendix (SA units) · B<x>-<desk>-Round (RD pages); page tokens unchanged; a combined B<x>-<desk> group is grandfathered.

## 0.3.0 · 260831
- Story ids replace SD/NA (JL 260831 "I don't like the SD... make sure to be self explained"): one A1-Story group holds P0-P3, the venue-free head (Story00-ideation, Story01-seed, Story02-roadmap) plus one Story<NN>-narrative-<desk> per desk (Story03 first); the A2-NA-narrative group and the SD/NA tokens are retired to the grandfathered list.

## 0.2.1 · 260831
- Group-name grammar caught up with the SA ruling (JL 260831): appendix token is `SA` (Section-Appendix), never `A<D>`; the collision rule now retires desk letter `A`; the grandfathered legacy list names `A<D>` instead of `SA`. haipipe-paper-workflow 0.6.1 and haipipe-page-for-section 0.5.5 already carried it; this door was the leftover.

## 0.2.0 — 2026-08-31

- **workflow-phases/ replaces page-types/** (JL 260831: "replace page-types to
  be workflow-phases"): the six journey-phase contracts are now
  `workflow-phases/haipipe-paper-{ideation,seed,roadmap,narrative,section,round}`,
  each carrying its P-number and gates in a `## 🧭 Journey phase` block while
  still owning its `page-type:` key. Venue is a library lane, not a phase, so
  `haipipe-paper-venue` moved to the family top level beside the `venue/`
  bank submodule. Routing table and family map updated; page keys unchanged,
  so no board page changes.

## 0.1.0 — 2026-08-28

- First versioned door (backfilled row): routing, journey figure, assembly
  contract pointer, G6 gate, folder scaffold.
