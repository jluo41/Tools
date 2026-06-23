# Venue Pack Structure (canonical)

Every venue under `_venue/` is the SAME 4-file pack. A venue is a target with a
style: it holds the knowledge for shaping a document to that player, and real
examples to imitate. A venue is knowledge, not a skill: no `SKILL.md`, not
auto-triggered. The paper lifecycle CONSULTS it by path (`_venue/playbook-<venue>`).

`playbook-jama-portfolio` and `playbook-utd-is` are the reference implementations.

## The structure (identical for every venue)

```
playbook-<venue>/
├── README.md            hub + the 4 lifecycle-stage mappings
├── style-profile.md     distilled language style + preferences to imitate
├── exemplars/
│   └── README.md        how to add real examples (PDF/text) to imitate STYLE; status
└── references/
    └── README.md        citation candidates (secondary; verify before citing)
```

Same folders, same subfolders, same file types in every venue. Only the content differs.

## What each file holds

```text
README.md         one-line identity + Relationship + Structure + How to use
                  + "Maps to lifecycle stages" (the 4 mappings below) + references note
style-profile.md  the venue's language style to imitate + a "To enrich from exemplars" checklist
exemplars/        real same-venue documents (PDF or extracted text) = the style corpus to imitate
references/       verified citation candidates (NEVER fabricated)
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
  carry per-outlet differences as a delta inside the pack (JAMA vs JAMA IM; CN vs US
  vs EP for patents; NSF vs NSFC for grants).
- No fabrication: unknown citations/exemplars are `TODO`, never invented.
- The concrete outlet is pinned by the paper's `STATUS.md` `venue:` field; a venue
  change re-runs the primary-claim designation.

## Scope

Applies to ALL venues, journal and "special paper" alike:

```text
journals (style-imitation)   utd-is (MISQ/ISR/MS-IS) · pnas · nature-portfolio · jama-portfolio · clinical-medicine
special papers               grant   (funding proposal; the agency is the venue)
                             patent  (patent filing; the jurisdiction is the venue)
```

The structure is identical. Grant and patent packs simply document more process
inside their README (per-agency proposal structure; the patent drafting pipeline +
per-jurisdiction format), because their document form diverges further from a
standard manuscript. The 4 mappings are reinterpreted for each: e.g. for a patent,
Claims = the legal patent claims, Display = drawings, Minimap = the specification
structure; for a grant, Claims = the Specific Aims, Minimap = the proposal sections.
