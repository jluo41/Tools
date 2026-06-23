# Venue Profiles (`paper/_venue/`)

A paper-internal knowledge area, not a standalone layer. Each JOURNAL venue is a
uniform 4-file pack (`README.md` + `style-profile.md` + `exemplars/` + `references/`),
holding the knowledge for shaping a manuscript to that target plus real papers to
imitate. Venues are knowledge, not skills, and never own lifecycle verbs. See
`_SCHEMA.md` for the canonical pack structure.

`_venue/` lives under `paper/`. The lifecycle keeps the verbs; a venue just tells it
what this player rewards and how a submission is shaped. PROCEDURE venues
(`playbook-grant`, `patent-*`) are still `SKILL.md` pipelines, not yet unified into
the pack form.

## Family map

```text
journal-is     playbook-misq · playbook-isr · playbook-ms-is
journal-life   playbook-nature-portfolio · playbook-pnas
journal-med    playbook-jama · playbook-clinical-medicine
grant          playbook-grant                         (MID: + NSF/NSFC/KAKENHI structure)
patent         playbook-patent (hub) · patent-novelty-check · prior-art-search
               · specification-writing · patent-review · jurisdiction-format   (HEAVY)
```

Folder names keep the `<name>-playbook` convention on purpose: the paper lifecycle
consults `_venue/playbook-<venue>` directly (`haipipe-paper-claims` and the jama
README rely on it). Journal venues are knowledge folders, so they have no
`.claude/skills` symlink; only the procedure venues (`grant`, `patent-*`) are still
invocable skills. Family grouping lives here in the map, not in folder prefixes.

## Weight spectrum

```text
LEAN  profile only, rides the host lifecycle unchanged
      misq · isr · ms-is · pnas · nature-portfolio · jama · clinical-medicine
MID   profile + a little form-specific machinery
      grant
HEAVY profile + a full procedure set
      patent
```

"有的多有的少" = the profile is always there; procedure grows with how far the
output form diverges from a standard manuscript.

## IS venue selection

When the venue decision is still live within IS, lean by signal (depth in each
`*-playbook`):

| Signal | Lean MISQ | Lean ISR | Lean MS-IS |
|--------|-----------|----------|------------|
| Theory-forward, pluralistic method | ✓ | | |
| Tight hypothetico-deductive, survey/experiment | | ✓ | |
| Causal identification, economics framing | | | ✓ |
| Design science, IT artifact evaluation | ✓ | | |
| Computational methods, large-scale data | | ✓ | ✓ |
| Behavioral theory, organizational IS | ✓ | ✓ | |
| Markets, platforms, economic mechanisms | | | ✓ |

For Nature-portfolio vs PNAS vs clinical, read `playbook-nature-portfolio`,
`playbook-pnas`, `playbook-clinical-medicine` (life-science / broad-impact /
clinical respectively).

## How the lifecycle consults a venue

```text
claims  -> README "-> Claims"            what the primary claim / contribution is here
display -> README "-> Display"           the venue's standard display set + hero rule
minimap -> README "-> Minimap"           section structure + abstract shape
write   -> style-profile.md + exemplars/ imitate the venue's sentence style
```

The concrete target is pinned in the paper's `STATUS.md` `venue:` field; the venue
change re-runs the primary-claim designation (claims couple to venue).

## History

The venue-routing workflow shells `haipipe-paper-{is,journal,conference}` and the
prose pipelines `haipipe-paper-{create,revise}` were retired from the venue area:
venue *selection* folds into this README, and prose *process* belongs to
`paper/3-write-edit/`. The 7 journal venues were each converted from a single flat
`SKILL.md` into the uniform 4-file pack (`playbook-jama` was the template).
