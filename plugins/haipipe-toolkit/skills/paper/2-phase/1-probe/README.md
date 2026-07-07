1-probe — the PROBE phase (hub + three harvesters)
====================================================

ONE probe pipeline (JL 2026-07-07 harvester ruling). Acquisition has one door;
the workers are the HARVEST step, transcribing landed evidence into the
paper-side working docs. Paper-side may FOLLOW pointers; only the gateway may
FIND things.

```
haipipe-paper-probe (hub)         BOOKKEEP → DISPATCH → TRANSLATE → VERIFY
  ACQUIRE   Agent(haipipe-probe-orchestrator-agent)  ← the ONLY door
            → gateway SWEEP (reuse|enrich|fresh) → discovery/task orchestrators
            → evidence LANDS in discoveries/ tasks/ insights/ 0-displays/
  HARVEST   per-lane, from the return's pointers, OWED→accepted in the PP card:
    haipipe-paper-probe-citation   pick_list  → _CITATION_{stage}.md
    haipipe-paper-probe-values     value_refs → _VALUES_{stage}.md
    haipipe-paper-probe-display    unit_refs  → _DISPLAY_{stage}.md + tex links
```

The PP card (`0-lifecycle/<stage>/_PROBE/PPNN_*.md`, anatomy owned by
`../../probe/haipipe-probe/SKILL.md`) is the single source of truth:
need/route at BOOKKEEP, refs + takeaways + lane lines at TRANSLATE,
verdict (full mode) for claims.

Enforcement is mechanical (`check-probe-cards.sh`, run at VERIFY and re-run by
the CHECK gate): planned/dispatched cards FAIL (probe-not-run), `harvest: OWED`
lane lines FAIL (harvest skipped), unresolved refs FAIL, tables/bibtex in
cards or working docs FAIL. A green PROBE over any of these is a defect.

Per-stage worker/mode map, seed/claims specifics, strip forms:
`haipipe-paper-probe/ref/per-stage-dispatch.md`. Harvest dispatch + literal
acceptance greps: `haipipe-paper-probe/ref/harvest-acceptance.md`.

Not user-facing: users invoke stage skills (seed, claims, ...); stages call
the hub; the hub dispatches the gateway and the harvesters.

(The per-section playbooks doc that previously occupied this file was
migration debris; it is archived at `../../_archive/README-sections-playbooks.md`.)
