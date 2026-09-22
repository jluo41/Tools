# Paper Run naming and ownership

The shared `haipipe-page/ref/page-run-families.md` owns RP/RE/RD naming;
`haipipe-run` owns native Tickets and Results. This adapter adds Paper context
and judgment targets. Read `haipipe-paper-workflow/ref/run-workflow.md` for
Spec bindings and the compile/response profiles.

## Owner, worker and identity

| Work | Semantic owner / family | New identity and storage | Boundary |
|---|---|---|---|
| Page writing | exact Paper PageType + shared Page writing / `page` | `rp-struct-NN`, `rp-scratch-NN_<target>`, `rp-sec-NN`, `rp-para-NN_Pxx[-Pyy]`; Page-native Ticket/Result | structure or bounded prose session; feedback is a Step |
| Page Evidence | consuming Page's Evidence Item / `page` | `re-value-NN_<slug>`, `re-cite-NN_<slug>`, `re-display-NN_<slug>`; Page RE/native Ticket and Result | one local evidence lineage; a worker may execute it without changing its owner |
| Page delivery | shared Page delivery owner / `page` | native RD target/version identity and paired receipt | generated Page artifact; does not authorize Page release |
| Supporting work | Task, Discovery or other declared native owner | full native `rNN`, `rlNN`, or global Ticket/Result address | consumer-neutral computation or inquiry; never renamed for Paper |
| Paper judgment | Paper Ideation/Story card owner / `paper` | declared judgment grammar below | one fixed idea, proposition, obligation or Section row |

A Page Evidence worker can call Task or Display capabilities. That does not
turn its local RE into a Task-owned Run. Independently commissioned Supporting
work remains with its native owner and is a dependency. RE/RD lineage and the
underlying native Ticket represent one execution and must not be counted twice.
A local Evidence Result cannot satisfy a human RP writing prerequisite.

## Paper context

`Ba-<desk>-Main`, `Bb-<desk>-Appendix` and `Bc-<desk>-Round` are shelves.
Use `paper_lane: main | appendix | round` and the full semantic `page:` beside
the Run's native identity. `RD<NN>` is a feedback Round Page identifier, not the
Page Delivery family `rdNN_<target>`. Story/Section/Round Pages are persistent
containers, not extra Run families or Run-number allocation authorities.

An example Page-local Evidence receipt projection is:

```yaml
run: re-cite-01_prescribing-variation
family: page
operation: evidence-item
paper_lane: main
page: S-MISQ-Main-Introduction
item: E01-CITE-prescribing-variation
target: E01-CITE-prescribing-variation
ticket: <exact-native-Ticket-address>
result: results/re-cite-01_prescribing-variation/
```

Resolve the Ticket dialect from the shared Page/Run owner; the placeholders
are not allocations. Frozen inputs/hashes, worker, status and acceptance remain
required by that owner. The Page's accepted DISPLAY unit is reached through
its Result, such as `results/re-display-01_<slug>/payload/Display1-<slug>/`.

## Allocation and interaction

Load the current Page Run families before allocating. `rp-struct-01` combines
SHAPE and SURVEY; Scratch, Section and paragraph counters are independent.
Page-global `P01…PN` addresses do not restart at a Content division. Normal
feedback appends a Step; same-target reopening appends a Version; materially
changed goals/targets follow the owner's NEW_RUN rule. Sync, Page controller
passes and a SURVEY reservation do not allocate a Run. LAND materializes only
the decided work through its native owner.

Uniqueness is `(owner folder, native Run id)`. Cross-folder references carry
that full address and the exact Result/version. A reused Result is a dependency,
not another execution. Delegated Task writing retains its own native identity;
it does not stand in for required Page interaction/acceptance.

## Existing Paper-local and compact identities

Existing `pm-<page>-<target>-rNN`, `pa-...`, `pr-...`, `pjNNtNNrNN`,
`rp00_mermaid-structure`, `rpNN_pNN[-pNN]` and `rNN_page-writing...` records
retain their original paths, IDs and family fields. These are compatibility
inputs, not new allocation grammars. Do not relabel their historical worker or
owner based only on the prefix. Resolve the original Ticket/Result/receipt;
missing ownership or acceptance is an explicit gap.

New Page Evidence uses typed RE. No bulk rename or duplicate execution is
needed. An accepted historical Result may be reused by exact path/hash when
its contract still meets the present requirement. If genuinely new work is
commissioned, allocate the current native identity and record `supersedes`
only when it actually replaces the old target/result; a reuse pointer does
not claim a replacement or fabricate a new receipt. Preserve frozen Round
`sent/` and `released/` snapshots.

## Paper judgment Runs

Idea and Story cards support bounded judgment sessions. Page prose and structure
use the shared RP contract when separately commissioned. Each card the Paper Workbench shows
on those Spaces may keep its discussion in one Paper-owned judgment Run, in the same
`runs/` + `results/` pair every Page has, with human feedback Steps in the
journal exactly as `rp-para` keeps them:

```text
JUDGE_RUN_ID := ridea-NN_<slug>            one candidate idea       lives on Story00-ideation
             |  rclaim-NN_<slug>           one C5 proposition        lives on the Story page
             |  rtask-NN_<slug>            one C7 evidence obligation lives on the Story page
             |  rnarra-NN_<section-id>     one C8 Section row         lives on the Story page
```

The ticket's frontmatter names the row it discusses, which is how the card
finds it; nothing is matched by name:

```yaml
family: paper
operation: judgment
interaction: human-feedback
target: E5              # i01 · E5 · T1 (or B1) · S-<desk>-Main-1-<Title>
run: rclaim-01_beyond-rating
result: results/rclaim-01_beyond-rating
```

A judgment Run never selects an idea (the I3 receipt does), never releases a
Section (G3 does), and never allocates a Task (the Task owner does). A
Section's `rp-struct-01` consumes the released C8 row and any relevant judgment
Result; an `rnarra` session is not mandatory when no such work was commissioned.


### Judgment Result and close rule

The Paper Page owner authors `runs/<judge-id>.md` with the exact card/row,
bounded question, named human authority, initial inputs and close rule. At
allocation it creates `results/<judge-id>/runtime.yaml` in planned state.
The paired Result consists of the Version journal and runtime outcome; a
separate copied Story/Idea record is unnecessary.

Use the existing human-feedback journal grammar: `vNNN.md` contains ordered
`## Step sNNN` sections with `### Human feedback` and `### Saved result`.
The saved result records the judgment, supporting references, limits, and
proposed next route for the fixed target. Open work is append-only; a session
restart resumes it. Same-goal reopening uses the next Version, and a material
change of target or judgment question requires a new commissioned Run.

Closure requires an explicit decision by the named human about this exact
question and saved judgment. Append `## Version closure` with `### Human close`
containing the person's identity, exact decision, scoped outcome and time.
The outcome may be `settled`, `concern-recorded`, or `proposal-recorded` when
that disposition satisfies the commissioned close rule. Unresolved required
work remains waiting/blocked; an agent summary cannot supply human closure.
This decision closes only the discussion. I3 admission, G3 release, evidence
acceptance and Task allocation retain their existing authorities.

The runtime records native `run`, `family: paper`, `operation: judgment`,
`target`, `ticket`, `result`, `version`, `step`, `status`, and `outcome`, plus
actual `started_at`/`finished_at` or null while unknown/unfinished. Actor and
input provenance resolve from the Ticket and journal. Use `waiting-for-feedback`
when waiting, and `complete` only after the scoped human close is saved. Failed
or blocked work records its reason. Reopening preserves closed journals and
clears the current unfinished finish time; history retains prior close times.

The Paper/Run views read these native records. Their structural checks can
show missing journals/closure; they do not judge the merits of a claim or
infer release from a completed judgment Run.
