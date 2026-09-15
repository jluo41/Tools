---
name: page-structure-run
description: >-
  Canonical contract for one Page Structure Run: a shared, read-only-visible
  RP Run whose SHAPE and SURVEY cycles settle the Page map, Bullets, roles,
  and evidence routes before Section or Paragraph Runs are allocated.
metadata:
  version: "0.1.0"
  last_updated: "2026-09-14"
---

# RP Structure · one Run for the Page map

`RP Structure 01` is the human-facing name. Its stable machine id is
`rp-struct-01`. It is the one Structure Run for the initial Page: it owns the
whole-Page Mermaid, Outline Bullets, paragraph jobs, Point roles, and the
evidence decisions that make those Points truthful. There is no separate
Outline Run, Survey Run, or Mermaid Run hiding behind it.

The Structure Run calls its two planning actions **SHAPE** and **SURVEY**.
Those are Step/cycle labels inside the same Run, not Workflow rows or
additional Level-4 Runs:

```text
rp-struct-01
  ├─ SHAPE  → Page map, Mermaid, C/P/B Bullets, Point roles, Evidence Item specs
  ├─ SURVEY → evidence decisions, local/supporting route plans, acceptance needs
  └─ CLOSE  → one frozen Structure result; unlock rp-sec / rp-para candidates
```

Its Run control is explicit:

```text
Run Type    Page.interactive-writing.structure
Actor       hybrid; participants on Run, contributor on each Step
Entry Gate  open when Page/Folder identity and current Context resolve
Exit Gate   declared owner/group accepts the Shape + Survey Result
Routes      SELF/next Step · NEW_VERSION · selected writing/evidence Run ·
            NEW_RUN for changed goal/target · HOLD
Receipt     paired runtime.yaml + immutable Version/Step journal
```

## What the Run produces

SHAPE writes or refreshes the structural projections for the current Page:

- the versioned Outline plan;
- `outline/<stem>-logic.mmd` and its derived Mermaid preview;
- ordered `C<n>.P<m>.B<k>` Bullets and one context-specific `[Role]` per Bullet;
- paragraph jobs, transitions, and the boundary of the Page;
- typed Evidence Item specifications, including a concise name and expected
  ready payload.

SURVEY makes each Evidence Item honest without executing material work. For
 each Point it records whether evidence is not owed, or which route is owed
 (`VALUE`, `DISPLAY`, or `CITE`), then plans any local Page Evidence Run and
 any external Supporting Task/Discovery Run. `none` means “this Point does not
 require evidence”; it is not a missing or pending Result. LAND later allocates
 and executes the routes that SURVEY decided are owed.

The Structure Run may propose route changes while it is open. It must not
silently fabricate a Result, copy an external Run into the Page, or treat a
planned route as landed evidence.

## Several people, one Structure Run

Several people may work on the same `rp-struct-01`. The collaboration unit is
the Run, not the person:

- keep one shared Ticket and one paired `results/rp-struct-01/` folder;
- record stable `participants` on the Run metadata and `contributors` on each
  Step or saved result;
- declare a `coordinator` only when the team needs one; otherwise the Page's
  normal owner/closure rule applies;
- do not create `rp-struct-02` merely because another person joined or made a
  review pass;
- close the shared Run once the declared owner or the agreed group decision
  accepts the Shape and Survey result.

Example metadata:

```yaml
page_run: rp-struct-01
participants: [person-a, person-b, person-c]
coordinator: person-a
cycles: [SHAPE, SURVEY]
```

Each Step still has one bounded scope and one saved result. A new independent
structural goal after closure gets the next `rp-struct-NN`; a wording-only
change belongs to a later Section or Paragraph Run.

## Files and lifecycle

The Run's read-only Run Space card points to the same small set of artifacts:

```text
runs/rp-struct-01.md
results/rp-struct-01/
  runtime.yaml
  working.md
  v001.md
outline/
  <stem>-outline-v*.md
  <stem>-logic.mmd
  <stem>-evidence-items.md
```

The normal lifecycle is:

```text
start → SHAPE → SURVEY → human review → repeat as Steps → CLOSE
                                      │
                                      └─ if a decision changes, resume this Run
CLOSE → Evidence/LAND → Section or Paragraph writing candidates
```

`Run Space` presents this result-first and read-only. The workflow owns
allocation and execution; the card does not expose a second “run” button.

## Naming

New and active Page folders use the typed id `rp-struct-01`. A stored compact
name such as `rp00_mermaid-structure` is historical input only; it is not a
valid allocation and must not be used in new packets, links, or folder names.
