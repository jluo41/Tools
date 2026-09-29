# Workbench, Runs, and Skills

This repository uses **Workbench** for the page-level working surface. A
package may provide a Workbench without requiring a Board. When a Board is
present, it can link to that Workbench; the Board does not own its work.

## Design principle

```text
Page / real folder
└── Workbench
    └── Space
        └── View (the subspace within that Space)
            └── Run Type (one kind of bounded work)
                ├── declared Skills (one or more, with distinct roles)
                └── Run instances (zero or more, each with a Ticket and Result)
```

A Space and View organize the interface. Each Run Type has one home View so its
Runs have a predictable place in the panel. The panel is a projection of the
Run Type catalogue and the Page's real Run Tickets; it does not allocate work.

**Skills attach to a Run Type, not exclusively to a View.** A Run Type may
declare several Skills, and one Skill may guide several Run Types or Views.
A package may have one context Skill dedicated to each View, alongside shared
workflow, domain, and procedure Skills. Those shared Skills remain part of the
Run Type's declared set. A View's context Skill alone does not describe the
whole Run Type.

A concrete Run is one execution of a Run Type for a bounded target. Its
Ticket and Result live in the Page's `runs/` and `results/` folders. When a
runtime records Skill provenance, it should bind the resolved Skill identities
and versions for that Run and distinguish **declared** Skills from Skills
actually loaded or invoked. A catalogue or panel can show declared Skills;
neither proves that a historical Run used them. Code workers and human actors
remain separate from Skills.

For example, the `subjective-label` package has `Quality → Test` as one View.
Its `test-reserve` Run Type uses Building rules, while `test-gold-lock` uses
Scanning rules. Both appear in the same View, so the View cannot determine the
complete Skill set. The package's [Run Type–Skill table](plugins/subjective-label/skills/label-building/ref/ref-space-mapping.md#run-type-skills)
declares the specific bindings and implementation status.
