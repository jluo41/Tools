# QA2 · Keep Paper, Page, plugins, and source work in their own authority lanes

state: ✅ SETTLED · authority boundaries validated
owner: JL
method: assign every write and decision to exactly one layer

## Opening
Which layer owns each part of paper work when most substantive design already lives on Pages?
Paper should compose accepted Pages, while the shared Page workflow controls lifecycle and plugins land evidence or generated formats.
This Page prevents the same fact, outline, or artifact from acquiring two homes.

**Where this page sits**: QA1 fixes the graph; QC2 expands the plugin boundary.

**Why it matters**: duplicate authority makes retargeting and revision impossible to audit.

## Writing Style
Describe ownership as concrete read and write permissions.
Use one owner per durable artifact.

## Diagram
**Ownership lanes**: each layer has one durable job.

```text
📄 Page Type       shape + closing rule
🔁 Page workflow   lifecycle + receipts
🗺 Paper journey   phases + gates G0–G7 · transitions only, never content
🃏 Plugins         evidence + displays + projections
📝 Paper door      route + compose + assemble
🧪 Task/Discovery  source work reached through Probe's QA lane
```

## Content
### 1 · Ownership boundary
**One authority rule**: the consumer Page owns the evidence binding used in its claim.

```text
Probe/PageX ─▶ reads an accepted Page by exact file and bounded scope
Probe/QA    ─▶ asks Task or Discovery and lands proof on the consumer Page
Paper ─▶ reads accepted Page outputs and assembles them
```

Probe is the umbrella, not a third storage layer. The PageX lane does not reopen raw source folders. The QA lane does not become a second paper outline.
Paper does not copy plugin contracts or keep a parallel build authority.
The journey machine (`haipipe-paper-workflow`) states which page holds authority in each phase and when the next may be minted; deleting it would lose no content rule, and that is the test it must keep passing.
Inside the establish loop the pens never cross: the Roadmap plans and registers, the Seed alone writes E-row flips, and the join is one string on two pages.

## Aims
### A1 · 🧱 Ownership boundary
- A1.1 · Every durable paper artifact has one owner and one read path.
  **Done when:** Paper, journey, Page, plugins, Probe's two lanes, Task, and Discovery roles do not overlap.

## States
### A1 · 🧱 Ownership boundary
- ✅ A1.1 · The live architecture assigns one owner to each artifact and binding.

## Files
- `3-QC-composition/QC1-paper-door/QC1-paper-door.md` · composition boundary
- `3-QC-composition/QC2-page-local-plugins/QC2-page-local-plugins.md` · plugin boundary
- `../../paper/haipipe-paper-workflow/SKILL.md` · journey machine, transitions only

## Log
260820 · Grouped PageX under Probe while preserving separate PageX and QA records.
260828 · Added the journey lane: `haipipe-paper-workflow` owns phases and gates, never content; recorded the establish-loop two-pens rule. Repaired the `4-QC-composition/` paths left dead by the 260820 regroup.
