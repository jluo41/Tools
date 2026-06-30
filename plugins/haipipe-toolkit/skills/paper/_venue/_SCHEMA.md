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
├── <outlet>/            per-journal section-level style guides (see below)
│   ├── <outlet>-abstract/style.md
│   ├── <outlet>-introduction/style.md
│   ├── <outlet>-theory/style.md          (IS journals; Nature uses results)
│   ├── <outlet>-methods/style.md
│   ├── <outlet>-results/style.md
│   ├── <outlet>-discussion/style.md
│   └── <outlet>-related-work/style.md    (Nature family; IS weaves into theory)
├── exemplars/
│   └── README.md        how to add real examples (PDF/text) to imitate STYLE; status
└── references/
    └── README.md        citation candidates (secondary; verify before citing)
```

Same folders, same subfolders, same file types in every venue. Only the content differs.

## Per-outlet per-section style guides

Each family pack contains per-outlet subdirectories with section-level style guides
mined from real exemplar PDFs. The outlet name matches the journal within the family.

```text
playbook-utd-is/
  MISQ/MISQ-{abstract,introduction,theory,methods,results,discussion}/style.md
  ISR/ISR-{abstract,introduction,theory,methods,results,discussion}/style.md
  MS-IS/MS-IS-{abstract,introduction,theory-model,methods,results,discussion}/style.md

playbook-nature-portfolio/
  NMI/NMI-{abstract,introduction,results,methods,discussion,related-work}/style.md
  nature-medicine/natmed-{abstract,introduction,results,methods,discussion,related-work}/style.md
  nature-communications/natcomm-{abstract,introduction,results,methods,discussion,related-work}/style.md
  npj-digital-medicine/npjdm-{abstract,introduction,results,methods,discussion,related-work}/style.md
```

Each `style.md` contains: word budget, arc structure, signature moves, exemplar
sentences (shape-quoted from real papers), anti-patterns, paragraph structure. Mined
from PDFs stored in `_WorkSpace/HAIToolLib/1-ExemplarLib/<family>/<outlet>/`.

Resolution path for section-edit:
```
STATUS.md venue: "MISQ 2026"
  → pack: playbook-utd-is
  → outlet: MISQ
  → section being edited: theory
  → path: _venue/playbook-utd-is/MISQ/MISQ-theory/style.md
```

Section-type mapping (section-edit name → outlet dir suffix):
```
abstract        → abstract
introduction    → introduction
theory          → theory          (IS) / not used (Nature)
lit-review      → theory          (IS) / related-work (Nature)
methods         → methods
results         → results
discussion      → discussion
related-work    → related-work    (Nature) / woven into theory (IS)
theory-model    → theory-model    (MS-IS analytical papers)
```

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
