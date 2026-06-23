# Venue Pack Structure (canonical)

Every journal venue under `_venue/` is the SAME 4-file pack. A venue is a target with
a style: it holds the knowledge for shaping a manuscript to that player, and real
papers to imitate. A venue is **knowledge, not a skill** — no `SKILL.md`, not
auto-triggered. The paper lifecycle CONSULTS it by path (`_venue/playbook-<venue>`).

`playbook-jama` and `playbook-misq` are the reference implementations.

## The structure (identical for every venue)

```
playbook-<venue>/
├── README.md            hub + the 4 lifecycle-stage mappings
├── style-profile.md     distilled language style + preferences to imitate
├── exemplars/
│   └── README.md        how to add real papers (PDF/text) to imitate STYLE; status
└── references/
    └── README.md        citation candidates (secondary; verify before citing)
```

Same folders, same subfolders, same file types in every venue. Only the content differs.

## What each file holds

```text
README.md         one-line identity + Relationship + Structure + How to use
                  + "Maps to lifecycle stages" (the 4 mappings below) + references note
style-profile.md  the venue's language style to imitate + a "To enrich from exemplars" checklist
exemplars/        real same-venue papers (PDF or extracted text) = the style corpus to imitate
references/       verified citation candidates for related work (NEVER fabricated)
```

## The 4 lifecycle mappings (in every README.md)

```text
-> Claims    (0-lifecycle/2-claims)  what the [primary] claim looks like for this venue;
                                     what is a contribution vs an enabler here
-> Display   (0-displays)            the venue's standard display set + hero rule
-> Minimap   (0-lifecycle/5-minimap) the venue's section structure + abstract shape
-> Write/Edit(3-write-edit)          consult style-profile.md + imitate nearest exemplar  [main purpose]
```

## Rules

- Knowledge, not a skill: no `SKILL.md`, no `.claude/skills` symlink; the lifecycle
  reads the pack by path.
- Family granularity: one pack per family when outlets share ~90% of their style;
  carry per-outlet differences as a delta inside the pack (e.g. JAMA vs JAMA IM).
- No fabrication: unknown citations/exemplars are `TODO`, never invented.
- The concrete outlet is pinned by the paper's `STATUS.md` `venue:` field; a venue
  change re-runs the primary-claim designation.

## Scope of this structure

Applies to JOURNAL venues (the style-imitation type):
`jama · misq · isr · ms-is · pnas · nature-portfolio · clinical-medicine`.

NOT yet applied to PROCEDURE venues (`playbook-grant`, `patent-*`): those are
pipelines with their own steps, still `SKILL.md` skills. Unifying them is a separate
decision (their "pack" would carry procedures, not paper-style exemplars).
