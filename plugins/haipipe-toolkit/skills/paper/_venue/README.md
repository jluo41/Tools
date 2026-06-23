# Venue Profiles (`paper/_venue/`)

A paper-internal knowledge area, not a standalone layer. Every venue is the SAME
uniform 4-file pack (`README.md` + `style-profile.md` + `exemplars/` + `references/`),
holding the knowledge for shaping a document to that target plus real examples to
imitate. Venues are knowledge, not skills, and never own lifecycle verbs. See
`_SCHEMA.md` for the canonical pack structure.

`_venue/` lives under `paper/`. The lifecycle keeps the verbs; a venue just tells it
what this player rewards and how a submission is shaped. A grant proposal and a
patent are treated as "special papers": same pack, with their own document process
documented inside the pack.

## Family map

```text
journal-is     playbook-misq · playbook-isr · playbook-ms-is
journal-life   playbook-nature-portfolio · playbook-pnas
journal-med    playbook-jama · playbook-clinical-medicine
grant          playbook-grant     (special paper: funding proposal; per-agency deltas)
patent         playbook-patent    (special paper: patent filing; per-jurisdiction deltas)
```

All nine are the same 4-file pack. Folder names use the `playbook-<name>` prefix so
every venue groups together in the listing. The paper lifecycle consults
`_venue/playbook-<venue>` directly (`haipipe-paper-claims` and the playbook-jama
README rely on it).

## Knowledge, not skills

Every venue is a knowledge folder: no `SKILL.md`, no `.claude/skills` symlink. The
lifecycle reads the pack by path. The grant/patent pipelines that used to be
invocable skills (`/patent-pipeline`, `/grant-proposal`, ...) were folded into
`playbook-grant` / `playbook-patent` as the document-process knowledge and archived
to `paper/_archive/_folded-into-venue-packs/` (recoverable if a runnable tool is
wanted again).

## What each pack carries

```text
journals   style to imitate + exemplar papers + the 4 lifecycle mappings
grant      same + a per-agency section-structure delta (NSF / NSFC / KAKENHI / ERC / ...)
patent     same + a per-jurisdiction delta (CN / US / EP) + the drafting-process steps
           (prior-art -> novelty -> claims -> spec -> review -> jurisdiction format)
```

Same structure everywhere; grant/patent packs just document more process inside the
README, because their document form diverges further from a journal manuscript.

## IS venue selection

When the venue decision is still live within IS, lean by signal (depth in each pack):

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
write   -> style-profile.md + exemplars/ imitate the venue's style
```

The concrete target is pinned in the paper's `STATUS.md` `venue:` field; the venue
change re-runs the primary-claim designation (claims couple to venue).

## History

The venue-routing workflow shells `haipipe-paper-{is,journal,conference}` and the
prose pipelines `haipipe-paper-{create,revise}` were retired from the venue area:
venue selection folds into this README, and prose process belongs to
`paper/3-write-edit/`. The 7 journal venues were each converted from a single flat
`SKILL.md` into the uniform 4-file pack (`playbook-jama` was the template), then
grant and patent were converted the same way (their old `SKILL.md` pipelines folded
in and archived). Folder names moved to the `playbook-<name>` prefix.
