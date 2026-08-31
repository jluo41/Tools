# CHANGELOG · haipipe-paper

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
