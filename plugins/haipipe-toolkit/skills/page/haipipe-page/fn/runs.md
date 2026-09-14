---
name: haipipe-page-runs
description: >-
  Propose bounded Page Runs that need human interaction, and route code,
  search, data, build, and other output-producing work to normal Task Runs.
argument-hint: "<page> [focus]"
allowed-tools: Bash, Read, Grep, Glob
---

# Runs · propose the human interaction a Page needs

Use `/haipipe-page runs <page> [focus]` when the person asks what Page work
should be discussed, shaped, compared, or approved together. This function is
the Page-owned planner for **Page Runs**. It does not execute the work and it
does not turn code/output work into a Page Run.

```text
fn/Runs
  ├── human shapes or decides the Page itself  → propose a Page Run
  └── code/search/data/build produces output   → route to a normal Task Run
```

## Read before proposing

Resolve and read the Page Face, current Outline and candidate Content, then
enumerate allocated Page Run Tickets and their paired Results. Read
`../SKILL.md` and
`../../page-workflows/haipipe-page-workflow/ref/interactive-writing-run.md`.
When task-side work is relevant, read the owning Task/Discovery Run profile;
do not infer its identity or lifecycle from the Page.

## PROPOSE is read-only

1. Detect the Page stage. If `rp00_mermaid-structure` does not exist, propose
   only the Mermaid Structure candidate. If it exists but is open, resume it and propose no
   paragraph Run. Paragraph candidates become legal only after its explicit
   Version closure.
2. Find concrete unresolved places where a person's feedback changes the Page:
   scope, structure, wording, comparison, acceptance, or another Page-owned
   decision.
3. Split different human questions or acceptance boundaries. Group adjacent
   paragraphs only when they form one rhetorical move that the person must
   judge together.
4. Compare each goal with existing Page Runs. **Resume an existing matching
   open Page Run** instead of proposing a duplicate.
5. Exclude work whose primary product is code or another independently testable
   output. Report it separately as suggested Task work and route it to its
   owner-native skill.
6. Return every currently unallocated candidate in reading order:

| Candidate | Human decision needed | Goal | Scope / review window | Why now | Next action |
|---|---|---|---|---|---|
| `1` | `<question>` | `<bounded interaction goal>` | `<Page addresses>` | `<current gap>` | `start` or `resume <existing rpNN>` |

**A proposal is not an allocated Run.** Do not create Tickets, Results,
runtime receipts, folders, or placeholder rows while proposing. **Do not mint
`rpNN` before selection.** Candidate numbers are presentation labels only and
may be recomputed on the next read.

## Mermaid Structure first, then numbered paragraphs

The first Page Run is mandatory for every Page, including an imported Page that
already has a draft Shape:

| Candidate | Human decision needed | Goal | Scope / review window | Why now | Next action |
|---|---|---|---|---|---|
| `1` | Agree the Page's visual structure | Mermaid Structure | Whole-Page Mermaid argument map and paragraph index | Paragraph work needs a closed reading order | `start` or `resume rp00_mermaid-structure` |

Selection allocates exactly `rp00_mermaid-structure`. Human and agent may take
many Steps and Versions to settle the visual structure. Do not propose or allocate any
paragraph Page Run until the person explicitly closes this Run. Its closure
must freeze the Page-global reading order as `P01`, `P02`, ... `PN` and map
each serial number to the plan address such as `C2.P3`.

Starting or resuming `rp00` must create or refresh
`outline/<stem>-logic.mmd` from the current plan. This is the Run's primary
review artifact: it shows the complete Page argument flow and every `P01..PN`
node. While `rp00` is open, Bullet Workspace renders the map expanded above
the plan; if the file is absent, the presenter names that absence as a blocker
instead of silently showing only Bullets. Every structural feedback Step
updates the plan, paragraph index, and Mermaid source together before asking
for more feedback.

After that closed index defines `N` paragraphs, partition them into `K`
independently closable paragraph groups:

```text
1 <= K <= N
Page Runs after Mermaid Structure = K
total Page Runs = 1 Mermaid Structure + K paragraph-group Runs
```

Ten paragraphs may therefore produce 10, 8, or 6 paragraph Page Runs. Every
candidate and allocated Run must show the exact paragraph serial or contiguous
range. Split
paragraphs that ask different questions, use different evidence, change
different meanings, or can be accepted separately. Group adjacent paragraphs
only when the human must evaluate them together as one rhetorical move.

List all unallocated paragraph-group candidates, but allocate only the selected
next candidate. Sequential execution is the default: close or pause the active
group before starting the next. Parallel Page Runs require explicit selection
and non-overlapping targets. If the agreed plan changes, recompute only the
unallocated candidates; never renumber or silently redefine allocated `rpNN`
Runs. Candidate positions are planning labels, not promises of future `rpNN`
identities.

Use short canonical identities after selection:

```text
rp00_mermaid-structure  whole-Page Mermaid Structure + P01..PN index
rp01_p01                paragraph P01
rp02_p02-p03            paragraphs P02-P03, judged together
rp03_p04                paragraph P04
```

Do not add a semantic slug to paragraph Run identities. Put the descriptive
name in the Goal column. `rpNN_pNN[-pNN]` makes both the Run order and paragraph
order visible on a narrow screen.

For every selected paragraph Run, copy the frozen Mermaid Structure description
from the Page-global paragraph index into the Goal and review packet. The
description is a stable reader-facing label, such as `Scope and acceptance`;
it is not a new paragraph title and must not be regenerated from draft prose.

Example after a ten-paragraph Mermaid Structure Run closes:

| Candidate | Paragraph group | Human decision |
|---|---|---|
| `1` | P01 | Accept the opening move |
| `2` | P02-P03 | Judge the linked context-and-gap move together |
| `3` | P04 | Accept the independent claim |
| `4` | P05-P06 | Judge the paired evidence interpretation |
| `5` | P07 | Accept the transition |
| `6` | P08-P10 | Judge the closing synthesis as one unit |

If there is no bounded Page interaction to commission, return `No Page Run
proposed` and name any normal Task work separately. Never edit the Page merely
to manufacture a proposal.

## What qualifies for each lane

| Primary product | Lane | Reason |
|---|---|---|
| Human feedback history plus agreed Page wording/plan | Page Run | The durable result is the interaction and its scoped decisions. |
| Code, computation, extraction, data, search, Discovery, rendering, build, or delegated paragraph output | Task Run | The durable result is an independently testable output. |
| Human review of a Task Result | Task Run plus a later gate | A human gate does not reclassify the producing work. |
| Automated CONTEXT-to-CHECK controller invocation | Page workflow pass | A router invocation is not a Level-4 Run. |

The Page function may say that Task work is needed, but it must not allocate,
rename, or wrap that work. The owner mints the native `rNN`, global, or
family-specific identity and retains its Ticket, runtime, command, and Result
contract.

## START or RESUME after selection

Selection can be explicit (`start candidate 1`) or implicit in a direct,
bounded request to revise/discuss named Page text. Before writing, re-read the
current Run inventory and source identities.

```text
matching open goal       → resume the same rpNN and append the next Step
matching closed goal     → reopen the same rpNN in the next vNNN.md
genuinely independent goal → allocate the next free rpNN
```

For the first goal, create `runs/rp00_mermaid-structure.md`. For a selected paragraph
group, create `runs/rpNN_pNN[-pNN].md` and the paired
`results/<same-run>/runtime.yaml`, `working.md`, and `v001.md`. Capture the
selecting request as `## Step s001`. Within one open Version, every later
human-feedback turn appends another `## Step sNNN` to that same Markdown file;
do not create one file or Run per Step.

Use the next free Page-local `rpNN` only at allocation time, except that the
first selected Mermaid Structure candidate always receives
`rp00_mermaid-structure`. `rp00` is reserved for this goal; paragraph Run
allocation starts at `rp01`. Its sequence is independent from Task `rNN`; `rp01`
and `r01` may coexist. If the human changes
the requested goal enough that it is independently closable, propose or start
a new Page Run rather than silently expanding the old scope.

Paragraph groups are sibling Page Runs, not children of the Mermaid Structure Run or of one
whole-Page Run. Each sibling owns its own Versions, Steps, review window, and
explicit closure.

## Return after work starts

Once selected work is saved, follow the interactive-writing contract and the
Page user-check packet. Report the actual `rpNN`, current `vNNN/sNNN`, saved
scope, feedback disposition, and next human decision. For `rp00`, show the
current Mermaid Structure and `P01..PN` mapping first. Do not present an
unselected proposal as `Ready`, `Waiting`, or `Held` in the Runs inventory.
