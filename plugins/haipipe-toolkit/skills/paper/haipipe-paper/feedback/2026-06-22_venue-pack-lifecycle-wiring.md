# Venue pack <-> lifecycle wiring

Status: DONE (initial hooks added); two open questions parked here.

## What was wired

Each venue is the uniform 4-file pack at `_venue/playbook-<venue>/`. The pack exposes
4 mappings (`-> Claims/Display/Minimap/Write`) + `style-profile.md` + `exemplars/`.
The lifecycle now consults them, pinned by STATUS `venue`:

```
2-claims    step 9 "Couple to venue" -> README "-> Claims" + references/   (already existed)
1-pitch     Audience/Venue Fit       -> README "-> Claims"/framing          (added)
4-display   principle 9              -> README "-> Display"                  (added)
5-minimap   Step 2 gather            -> README "-> Minimap"                  (added)
write/edit  Inputs #6                -> style-profile.md + exemplars/        (added)
```

All hooks are CONDITIONAL ("if a `_venue/playbook-<venue>` pack exists"), so a venue
without a pack is a graceful no-op. `ref/lifecycle-map.md` reads-columns updated.

## Open question 1: pack vs TARGET_VENUE constant

`haipipe-paper-edit-write` and `minimap/ref/plan-outline.md` still carry a
`TARGET_VENUE` constant (ICLR default, ML-conference list) that drives FORMATTING
(style file, page limit, anonymity). The pack drives CONTENT/STYLE. Current decision:
they coexist (pack = content, constant = formatting). Open: should the pack also own
the formatting mechanics (one source of venue truth), or stay split?

## Open question 2: ML-conference venues have no pack

Only journal + grant + patent have packs. ICLR/NeurIPS/ICML/CVPR/ACL/AAAI/IEEE are
covered ONLY by the `TARGET_VENUE` constant (formatting), with no `-> Claims/Display/
Minimap`, no `style-profile.md`, no `exemplars/`. Open: build `playbook-iclr`,
`playbook-neurips`, ... packs the same way, or leave conferences as formatting-only?

## Open question 3: venue label -> pack resolution  (RESOLVED)

A `STATUS.md venue:` human label (e.g. "JAMA Internal Medicine") did not match a pack
folder (`playbook-jama-portfolio`). RESOLVED by the new `haipipe-paper-venue` skill, which owns
the label -> pack map and pins the slug into STATUS. Stages resolve the label through
that map.

## Note

`exemplars/` are empty placeholders across all packs; the write hook only bites once
real exemplar papers are dropped in. The hooks are in place regardless.
