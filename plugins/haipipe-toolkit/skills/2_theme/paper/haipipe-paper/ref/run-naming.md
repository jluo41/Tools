# Paper Run naming and ownership

The shared `haipipe-page/src/run_names.py` owns Page Run naming;
`haipipe-run` owns native Tickets and Results. This adapter adds Paper context
and judgment targets. Read `haipipe-paper-workflow/ref/run-workflow.md` for
Spec bindings and the compile/response profiles.

## Owner, worker and identity

| Work | Semantic owner / family | New identity and storage | Boundary |
|---|---|---|---|
| Page writing | exact Paper PageType + shared Page writing / `page` | `run-<kind>-<slug>` (kind: structure, scratch, section, paragraph, revise, auto-write, evidence-embed, context, check); Page-native Ticket/Result | structure or bounded prose session; feedback is a Step |
| Page Evidence | consuming Page's Evidence Item / `page` | `run-value-<slug>`, `run-citation-<slug>`, `run-display-<slug>`; Page-native Ticket and Result | one local evidence lineage; a worker may execute it without changing its owner |
| Page delivery | shared Page delivery owner / `page` | one fixed Run per lane: `run-delivery-webpage`, `run-delivery-latex`, `run-delivery-word`; no receipt | generated Page artifact; does not authorize Page release |
| Supporting work | Task, Discovery or other declared native owner | full native `rNN`, `rlNN`, or global Ticket/Result address | consumer-neutral computation or inquiry; never renamed for Paper |
| Paper judgment | Paper Ideation/Story card owner / `paper` | `run-paper-<judgment>-<slug>`, below | one fixed idea, claim, Task Roadmap row or Section row |
| Board and version work | the run card's skill / `paper` | `runs/run-<type>-<target>/` in that level (`run.yaml`, ticket, `passes/`, the `haipipe-run` folder), made by `paper_ladder.py run` (`run-add-venue-<venue>`, `run-release-section-<tNN>`, `run-send-version-<jNN>`) | one file, its passes p01, p02 … inside; the full list is the run cards |

A Page Evidence worker can call Task or Display capabilities. That does not
turn its local evidence Run into a Task-owned Run. Independently commissioned Supporting
work remains with its native owner and is a dependency. The evidence Run and the
underlying native Ticket represent one execution and must not be counted twice.
A local Evidence Result cannot satisfy a human Page writing prerequisite.

## Paper context

Every Run is `run-<type>-<target>`, with no date (JL 261007: "one soft run can
have multiple passes, so we don't need the MMDD"; "unify the run to be
run-xxx-xxx"). A Run lives with its level (`haipipe-paper/ref/paper-ladder.md`):
a Board's and a version's own Runs in their `runs/`, a Section's in the Section
Task's `runs/` through the Page workflow. Use `paper_lane: main | appendix |
letters` (from the Task's number band: `t0N_`, `t2N_`, `t3N_`) and the full
semantic `page:` beside the Run's native identity. A comments batch is a report
(`reports/qNN_<kind>-<MMDD>/`), not a Run family or a Run-number authority. The
older dated form `run-<kind>-<MMDD>-<slug>` is still read; `page.py run-names`
drops its day.

An example Page-local Evidence receipt projection is:

```yaml
run: run-citation-prior-work
family: page
operation: evidence-item
paper_lane: main
page: t01_introduction
item: E01-CITE-prior-work
target: E01-CITE-prior-work
ticket: <exact-native-Ticket-address>
result: results/run-citation-prior-work/
```

Resolve the Ticket dialect from the shared Page/Run owner; the placeholders
are not allocations. Frozen inputs, worker, status and acceptance remain
required by that owner. The Page's accepted DISPLAY unit is reached through
its Result, such as `results/run-display-<slug>/payload/Display1-<slug>/`.

## Allocation and interaction

Load the current Page Run names before allocating. The first `run-structure-…`
Run combines SHAPE and SURVEY; Scratch, Section and paragraph counters are independent.
Page-global `P01…PN` addresses do not restart at a Content division. Normal
feedback appends a Step; same-target reopening appends a Version; materially
changed goals/targets follow the owner's NEW_RUN rule. Sync, Page controller
passes and a SURVEY reservation do not allocate a Run. LAND materializes only
the decided work through its native owner.

Uniqueness is `(owner folder, native Run id)`. Cross-folder references carry
that full address and the exact Result/version. A reused Result is a dependency,
not another execution. Delegated Task writing retains its own native identity;
it does not stand in for required Page interaction/acceptance.

## Older short names

Older short names (`rp-`, `re-`, `rd01_`, `pm-`, `pa-`, `pr-`, `pjNN…`, `ridea-`,
`rclaim-`, `rtask-`, `rnarra-`) are retired (JL 261001). No new Run uses them.
`page.py run-names` renames a Page's old Runs once.

## Paper judgment Runs

Idea and Story cards support bounded judgment sessions. Page prose and structure
use the shared Page Run contract when separately commissioned. Each card the Paper Workbench shows
on those Spaces may keep its discussion in one Paper-owned judgment Run, in the same
`runs/` + `results/` pair every Page has, with human feedback Steps in the
journal exactly as a Page `run-paragraph-…` Run keeps them:

```text
JUDGE_RUN_ID := run-paper-idea-<slug>        one candidate idea        in the Board's runs/
             |  run-paper-claim-<slug>       one claim                  in the Board's runs/
             |  run-paper-task-<slug>        one Task Roadmap row       in the Board's runs/
             |  run-paper-narrative-<slug>   one Section Narrative row  in the version's runs/

slug is two to four lowercase words, no date. A name already taken at that
level gets -2, -3.
```

The ticket's frontmatter names the row it discusses, which is how the card
finds it; nothing is matched by name:

```yaml
family: paper
operation: judgment
interaction: human-feedback
target: E5              # i01 · E5 · T1 (or B1) · t01_<title>
run: run-paper-claim-beyond-rating
result: results/run-paper-claim-beyond-rating
```

A judgment Run never selects an idea (the I3 receipt does), never releases a
Section (G3 does), and never allocates a Task (the Task owner does). A
Section's first `run-structure-…` Run consumes the released Section Narrative row and any relevant judgment
Result; a `run-paper-narrative-…` session is not mandatory when no such work was commissioned.


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
