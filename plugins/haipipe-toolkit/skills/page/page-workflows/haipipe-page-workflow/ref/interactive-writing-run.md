# Page Run · interactive writing

This is the canonical **Page Run**: the human-interaction execution profile of
`haipipe-page-workflow`, not a
controller label, plugin, or background service. Use it when a person is shaping,
drafting, or revising a Page with the agent. It may start before Shape approval
and before evidence is ready. Published Content still has its existing gates.
For the fused Structure Run, also load `structure-run.md`: SHAPE and SURVEY
are cycles of one `rp-struct-01`, including when several people participate.
For the rationale, see `../../../../../docs/page-writing-philosophy.md`.

## Identity and ownership

| Object | Meaning | When it changes |
|---|---|---|
| Run | One independently commissioned Page writing session/round at a fixed scope; its typed RP identity states the scope | New commissioned round/session, or a materially new goal/scope; not each chat turn |
| Version | One append-only candidate snapshot/journal inside that Run, e.g. `v001` | A new review episode or reopening within the same fixed Run |
| Step | One complete scoped work cycle; for a Section: draft → review/rating → diagnose → revise, e.g. `s002` | Each completed cycle; internal model/tool calls are not Steps |
| Review window | The paragraphs/diagram being discussed this turn | May move within the declared Run scope |
| Shape version | The authoritative plan's own approval identity | Its existing protected-fork/approval rules; never the Step counter |

Display `v001/s002` (or `v0.0.1-s2` as a human label), but use one spelling on
disk. Never confuse a writing Version with an outline `v<G>.<S>.<E>` or a
controller receipt's `step`. A paragraph-group Run may cover adjacent
paragraphs only when the person must judge them together as one rhetorical
move. If the Run was commissioned for P01-P02, adding P03 requires a recorded
scope extension from the person, not a quiet expansion.

## Page-level cardinality and RP names

The first structure Run is always `rp-struct-01`, even when the Page was
imported with a draft Shape. RP allocation is Page-local and type-explicit:

| IDs | Scope | What the Run settles |
|---|---|---|
| `rp-struct-NN` | Page Structure Run: SHAPE + SURVEY | Page direction, coverage/non-coverage, high-level section flow, ordered Bullets, Point roles, paragraph jobs, typed evidence decisions, Mermaid map, and the frozen `P01..PN` index; no adopted prose or material evidence execution |
| `rp-scratch-NN_<target>` | Human Scratch capture | rough thinking for one Section (`C1`) or whole paragraph group (`C1.P1`) in the current Outline grammar; B/symbol rows are not targets; the person manually triggers Finish Scratch and the AI generates the closing Summary |
| `rp-sec-NN` | Section-level | One named Section drafting/revision round and its candidate, review/rating, diagnosis, revision, and report |
| `rp-para-NN_Pxx[-Pyy]` | Paragraph-level | One fixed paragraph or contiguous paragraph group, such as `P03–P05` |

`rp-struct-01` is the initial Structure Run and contains both SHAPE and SURVEY.
It may contain many Steps while the map, Bullets, roles, and evidence routes
are being settled. Several people share this Run: record `participants` on the
Run and `contributors` on each Step; joining the review does not allocate a
new RP. `rp-struct-02` and later ids are optional independent post-closure
structural goals, not separate Survey or Mermaid Runs. Scratch is available as
a small human planning capture once the selected Outline exists; it does not
write `Draft:` prose or bypass later Structure or evidence gates. Only after
the Structure contract is closed may the workflow propose Section Runs in
`rp-sec-NN` or paragraph Runs in `rp-para-NN_Pxx[-Pyy]`.

For Section-level writing, one complete draft → review/rating → diagnose →
revise cycle is one Step inside the current Section Run, not a new Run. The
agent must review and diagnose again after revising; self-revision is not
self-acceptance. A later independently commissioned Section drafting/revision
session—such as after a substantial structure change—gets a new `rp-sec-NN`
Run. Within the same commissioned round, later feedback appends another Step.

The four RP kinds are sibling Page Runs; structure, Scratch, Section, and
paragraph Runs are not children of one another. For paragraph-level writing, keep the
paragraph or contiguous range fixed. A
later revisit of that same target normally reopens the same Run in a new
Version; a materially different target or goal gets a new `rp-para-NN` Run.
Group adjacent paragraphs only when one human decision must accept or revise
them together. Thus `rp-para-01_P03`, `rp-para-02_P04-P05`, and
`rp-para-03_P06` are valid examples. If the closed index has `N` paragraphs,
its paragraph candidates satisfy `1 <= K <= N`; the RP sequence and paragraph
serial are separate coordinates. The Page RP identity and a native Task Run
may coexist, for example `rp-para-01_P03` and `r01`.

Before paragraph selection, show the complete candidate list in frozen reading order using
Candidate numbers, never future typed RP identities. Allocate only the selected
next candidate. Sequential work is the default; parallel Page Runs require
explicit selection and non-overlapping targets. If the plan changes, recompute
only unallocated candidates. Never renumber or silently redefine an allocated
Run.

Use `family: page`, `operation: interactive-writing`, and
`interaction: human-feedback` for prose review/writing. A Scratch ticket also
uses `mode: scratch`, `target_scope: section|subsection|paragraph`, and
`interaction: human-scratch`. Allocate `rp-struct-01` first for structure, then use the
next free identity whose kind matches the selected scope. Semantic names belong
in Goal, not in the identity. Never rename a Task/Discovery Run to an RP, and
never consume its `rNN` counter when allocating a Page Run. Reject an identity
whose kind or paragraph target does not match its scope; it cannot unlock or
substitute for a canonical Run.
Within each logical Run, keep
one paired Result and create no child Run per sentence, Step, Version, or
internal agent call.

Every paragraph Run and every reader-facing review packet also carries the
frozen Mermaid Structure description for each selected paragraph. Resolve it
from the closed `rp-struct-01` index or authored
`outline/<stem>-logic.mmd`, for example `P06 · C3.P6 · Scope and acceptance`.
Do not replace this frozen description with a newly invented Goal sentence.
Missing or conflicting descriptions are visible blockers.

The workflow owns the conversation history and review state. It invokes:

- `haipipe-page-context`: resolve applicable constraints, style and exemplars;
- `haipipe-page-outline`: change Bullets, Evidence Item requirements, and the
  embedded `Draft:` fields in the selected Outline Markdown under SHAPE
  authority;
- `haipipe-writing`: produce, revise or evaluate scoped prose under the shared
  request, selected methods and rubric described below;
- `haipipe-page-evidence`: commission supporting/local work and bind Results;
- `haipipe-page-content`: after every planned Page Run and required evidence
  Task Result is complete, adopt all agreed wording and produce delivery once;
- `haipipe-page-check`: judge an exact delivered Page, not each chat edit.

Page/Execution/Discovery are work families. Human-feedback/delegated is a
different distinction. A local Page Evidence Item Run can be delegated;
searching, computation and export are not interactive writing Steps merely
because they serve a paper. They retain their own Run contracts when they are
independently commissioned. A routine build need not become a ceremonial Run.

## Small, Markdown-first storage

For Section and Paragraph Runs, the agent invokes Writing using
`../../../../writing/haipipe-writing/ref/writing-request.md`.
The Ticket freezes selected methods and the base rubric identity; the Step
adds its exact baseline, original feedback and editable scope. Use default
native writing and self-review when no external method is selected. A supplied
DNA or anti-slop packet selects its adapter once. Resolve only selected methods
under `../../../../writing/haipipe-writing/ref/method-adapter-contract.md`.

Writing returns candidate, actual changes, evaluation, method trace and
unresolved findings. The host saves the candidate under the existing source
writer/concurrency rules and stores its review in the same Version/Step.
Evaluation follows `../../../../writing/haipipe-writing/ref/evaluation.md`:
draft → review → at most one authorized revision pass by default → final
review. The Run may declare another bounded budget. A local wording Step
checks only the changed span, preservation and relevant seam. Self-review
does not pass human acceptance or replace independent Page CHECK. Missing
required inputs or exhausted revision budget remain visible in the return.

The existing worker_skill_chain and runtime worker fields select/record the
worker. The agent executes the skill instructions; these fields do not create
a scheduler or trigger background model calls. Draft feedback remains pending
until the agent completes its Step. Evaluate-only requests return findings
without changing prose; no-op acceptance/navigation creates no change card.

```text
<folder>/
├── outline/                         current editable planning authority
│   ├── <stem>-outline-v1.2.md        unapproved working Shape (if needed)
│   ├── <stem>-outline-v1.2.md        current Shape + embedded `Draft:` fields
│   └── <stem>-evidence-items.md     requirements and Supporting/Local graph
├── runs/rp-struct-01.md             initial Structure Run: SHAPE + SURVEY
├── runs/rp-struct-NN.md             structure/Bullet refinement Run
├── runs/rp-scratch-NN_<target>.md   human Scratch capture Run
├── runs/rp-sec-NN.md                Section Run
├── runs/rp-para-NN_Pxx[-Pyy].md     paragraph Run
└── results/<same-run>/
    ├── runtime.yaml                 derived current status/pointers
    ├── working.md                   short resume view of effective decisions
    ├── v001.md                      all Steps in this Run's first episode
    └── v002.md                      next episode; created only after reopening
```

Use `writing-step-template.md` for the concrete records. These are ordinary
Markdown records written by the skill's agent, **not a newly implemented CLI,
automatic chat recorder, or UI approval control**. Existing source writers and
their concurrency checks remain in force. Never claim automatic capture of an
unread chat or of feedback from a disconnected session.

One browser surface can capture human thinking: Draft Space's Scratch Mode
(`haipipe-plugin-outline` §✍️). A small `+` targets a Section or whole
paragraph group; B/symbol rows have no Scratch control. The current
grammar has no separate subsection node, so there is one plus per visible
target. It writes the rough note to the selected Outline's `##
Scratch` registry while creating/updating the paired Scratch Run. `Save`
leaves the Run open. The person manually clicks `Finish Scratch`, which asks
the AI to generate a concise non-empty Summary from the raw notes, writes
`AI generated the Scratch Summary and the person closed the Run.` to the Result,
and closes the Run. A closed Scratch Run is immutable; later thinking starts a
new Scratch Run. Scratch Mode keeps saved raw Scratch visible by default even
when the underlying body is hidden. This capture never edits `Draft:` prose.
Ordinary feedback
still enters a Page Writing Run as a pending `### Human feedback` Step, but it
is not a Draft-space composer.

## ⚡ Fast foreground rule

For ordinary wording feedback, finish one Step in under two minutes when the
current Run records are available. Read only `working.md`, the latest saved
result tail, the exact target paragraph slice, its dependent Bullet, and the
frozen Mermaid description. Write the Step journal, the required resume
projections, and the candidate preview only when its presenter needs it. Make
one bounded patch and one narrow check, then return the packet. Do not start or
wait for a sub-agent, reread the whole Page or Version, update wording-only
plan metadata, run an outline pass, build, export, test broadly, verify the
browser, or perform preference analysis. If a required record is missing,
return one named blocker instead of scanning the repository.

`working.md` holds current Version/Step, review window, pending feedback,
effective decisions with source Step ids, accepted paragraph identities, open
evidence dependencies, and next action. It is a resumable view, not the only
history. `runtime.yaml` retains the neutral Run receipt's identity, input hashes,
worker and real start/finish timestamps (unfinished/unknown timestamps are null),
and projects `family`, `operation`, `interaction`, `target`, `ticket`, `result`,
`status`, `version`, `step`. Use `ready`, `running`,
`waiting-for-feedback`, `blocked`, `complete`; waiting is normal and does not
mean failure. Do not depend on a continuously running model process.

One Version is one append-only Markdown journal. Every completed Step is a
`## Step sNNN` section in that same file and contains both `### Human feedback`
and `### Saved result`. Save the Human feedback subsection before editing,
then append the Saved result only after the scoped draft/review/diagnose/revise
cycle and narrow validation succeed. A partial clarification or an unfinished
self-revision remains a pending Step, not a new Run.
Completed Step sections are immutable: a correction appends a new Step that
references the earlier one. If interrupted, leave the current Step visibly
pending and project the Run as `Held`, never as `Waiting`. Interrupted or
partial work is described honestly in `working.md`; compare actual files
before resuming.

## Each turn

1. **Resume and scope.** Read the Run, `working.md`, latest completed result,
   selected paragraphs, their Bullets/Evidence and effective style rules. On
   initial entry read the whole Section and make one Mermaid argument map;
   later local edits need only the affected slice and adjacent seam. Check
   current source identity; a changed file invalidates cached assumptions.
   Before the first edit of existing prose, retain the full target text and
   relevant planning slice in the initial input. Later Steps may reference the
   preceding immutable result; an external change needs its own new baseline.
2. **Capture the human.** Start the current Step in `vNNN.md`, then save its
   `### Human feedback` subsection with the original request and each feedback
   item verbatim, selected quote, addressed target, source Version/Step, and
   reason. Preserve informal language. Agent interpretation is separate. If
   source text is ambiguous, record it and ask only about that item; never
   silently attach it to the nearest sentence. Do not close the Step merely
   because one chat turn was received.
3. **Complete the scoped cycle.** Choose `local-edit`, `paragraph-rewrite`, or
   `structure` from the user's request, not the model's preference. For a
   Section-level Run, produce the candidate, obtain the configured rubric review
   and any defined rating, diagnose the issues, revise within the recorded
   budget, and review/diagnose the revised candidate before reporting the result.
   Paragraph Runs use the same base rubric at their fixed scope. Save located
   findings and actual evaluator/method identity; do not invent a numerical
   rating scale. For `rp-struct-01`, SHAPE updates
   Mermaid and Outline Bullets together, while SURVEY updates typed Evidence
   Item route decisions in that same Run; neither cycle creates a second
   planning Run. For a paragraph Run, keep the fixed target
   range. Bullets and prose may inform one another, but an edit to one does
   not authorize unrelated changes to the other. Update owned evidence
   requirements when the meaning changes; do not invent Results. Missing
   evidence has named placeholders, never a fabricated claim presented as
   supported.
4. **Save the completed Step.** Save the candidate in
   selected `outline/<stem>-outline-v*.md`, update only its dependent Bullets in the working
   Shape, and preserve comment/annotation records. Recheck the narrow base and
   protected targets before writing; on concurrent drift, stop and rebase.
   Update an Evidence requirement only when this Step changes what the
   paragraph must cite, measure, or show. Append the complete candidate,
   affected planning snapshot, review/rating, diagnosis, narrow checks, and
   each feedback disposition to the same Step's `### Saved result`. Update
   `working.md` and `runtime.yaml`.
   For every material wording change, add one `#### Track changes` card with
   clean Before and After text, a short local change label in the card heading,
   and a concise Why. Do not infer a broader preference in the foreground Step.
   Add `Analysis status: deferred to post-run analysis` instead. Historical
   cards may retain their earlier preference fields. The presenter computes
   word/punctuation-level red-delete/green-add spans; never store visual diff
   markup in the candidate or Page Content.
   Do not duplicate the classification in a second table. A Step that only
   records acceptance, lifecycle state, navigation, or presenter behavior uses
   `Changes` and creates no Track Changes card.
   Do not write adopted Page Content, refresh delivery, run the whole test
   suite, or wait for export/browser verification. `Applied` is never human
   acceptance.
5. **Return the saved passage.** Use `haipipe-page/ref/user-check-packet.md`'s
   routine packet and the exact response skeleton in `writing-step-template.md`:
   heading `<Run> · <Version/Step>`; the complete saved passage grouped under
   one visible `### PNN · Cn.Pm · <Mermaid Structure description>` heading per paragraph, with each paragraph in
   its own blockquote and chat-only `S1`, `S2`, ... sentence labels; then one concise explanation
   of what changed and why. Do not emit a fixed status list or an empty Evidence
   section. Add Evidence commentary only when this Step changed or left open a
   citation, value, or figure requirement. End with the verified Draft Space,
   Evidence Space, and Current Run links, with nothing after
   them. Show an updated Mermaid only when logic changed. Do not polish a second
   chat-only version or wait for optional exports. Set `waiting-for-feedback`
   and finish the turn.

When a person enters, continues, resumes, or asks to review an open Run before
giving new feedback, return the packet's pre-Step review format instead. Show
the latest complete candidate grouped by paragraph with
`### PNN · Cn.Pm · <Mermaid Structure description>` headings and `S1...Sn`
labels, the exact review scope, the next proposed `vNNN/sNNN`, and the Bullet
   Draft Space, Evidence Space, and Current Run links. Do not append a Step
until the person supplies feedback, acceptance, or an explicit close. A
pre-Step packet is a review surface, not a new journal record.

Between Steps and Runs, follow [`interactive-execution-policy.md`](interactive-execution-policy.md).
Lightweight record-first work proceeds without a gate. Heavy builds, exports,
broad checks, delegated Task Runs, and sub-agent analysis require a scoped
approval request before dispatch.

The original feedback is not replaced by a cleaner summary. Preserve both.
If a preference changes, retain the old decision and record which newer Step
supersedes it. Repeated preferences may later be proposed as Writing rules;
only explicit authorization promotes them to the authored Requirement W rows
or shared policy. A single local preference is not automatically global law.
The Paper Round-generated `<stem>-feedback.md` is not this chat inbox.

## Acceptance, closure, continuation

Acceptance always records **who, exact words, target, source Version/Step and
accepted text/hash**. Capture acceptance as a new input/result Step even when
no prose changes. Do not append a tick to an already completed result.
“Continue,” “try again,” or “looks better” does not approve
the whole Run, Shape or Page. An explicit “P01 is settled; revise P02” accepts P01
only. Keep accepted P01 byte-for-byte unchanged while revising P02. Reopen P01
only on an explicit scoped request; record the prior accepted snapshot and the
reopening quote. Do not silently clear its acceptance because evidence changed.

Acceptance is the Run's human exit Gate, not a separate Run. The route is
`SELF` for another Step, `NEW_VERSION` for same-target reopening after closure,
`CLOSE`/the next Run for accepted completion, or `NEW_RUN` when goal/target
changes.

A Version closes after the current writing episode is recorded as an immutable
journal. A Section-level Step may therefore complete its full
draft/review/rating/diagnose/revise cycle while the Section Run remains open
for another Step. The RP Run closes only after its final candidate/report is
shown and the person explicitly closes that Run (or chooses the next scope).
Every commissioned target must be accepted or explicitly removed, its Bullets
must be settled, and every Evidence obligation must be explicit and ready
(`none` or a bound CITE, VALUE, or DISPLAY Result) before Run closure.

Run closure seals the current Version before any post-run analysis Task is
launched. Closing a Version alone does not silently mint a new Run.

Append `## Version closure` to the same `vNNN.md`, including `### Human close`,
the final complete passage/map and plan/evidence snapshot pointers. After
closure, the whole Version file is immutable. The next Version records the
closed `vNNN.md` hash before any new Step. If accepted wording still has named
evidence owed, record the acceptance but keep the Page Run open; commission or
resume the owner-native Task Run and return for evidence review. Do not mark the
Page Run complete while factual support, citation, value, or figure output is
unresolved. Whole-Page `CHECK/CLOSE` is a separate later authority.

Closing a Page Run does not modify `<page>.md` or `delivery/`. The Page release
barrier opens only when the required structure/Bullet RP Runs, Section RP Runs,
paragraph RP Runs, and every required evidence Task Result are complete and
bound. CONTENT
then applies all accepted candidates in one Page-level pass, integrates the
ready evidence, and generates web, LaTeX, and Word once before CHECK.

After Version closure, continue the same fixed goal by creating `v002.md`,
pointing to the hash of closed `v001.md`, and recording what is being reopened.
Never reopen by editing `v001.md`. Within an open Version, append another
Step only when it completes the next scoped cycle. A new Claude/Codex chat can
resume the same Run, but a later independently commissioned Section
drafting/revision session receives a new `rp-sec-NN` identity referencing its
predecessor. A paragraph revisit with the same fixed target normally
reopens the existing paragraph Run in a new Version. Ordinary human feedback
is an expected input of this profile, not an Execution-contract rerun.

## Rapid feedback mode

Use this mode for a normal follow-up feedback turn inside an open Page Run,
when the person asks to change a sentence, clause, word, punctuation mark, or
small local seam. The target is a short foreground pass, normally under two
minutes; this is a record-first operating budget, not a service-time guarantee.

- Reuse stable context already loaded in the session. Do not reread the whole
  Page, the whole Version journal, the full skill corpus, or unrelated history.
- Read only `working.md`, the latest saved-result tail, the exact target
  sentences, and the dependent Bullet/Evidence slice. If the prior Step already
  contains the complete passage, reference it as the recoverable baseline.
- Make one bounded edit transaction: append the new Step, update only affected
  preview records and dependent Bullets, update `working.md` and
  `runtime.yaml`, then run one narrow hash/scope check.
- Do not run `outline-pass.py`, a full Page parser, a repository-wide search,
  browser verification, delivery generation, full tests, or a fresh reviewer
  for a local wording change.
- Keep the saved Step complete but compact. Store the raw feedback, selected
  quote/annotation, complete candidate passage, disposition, and a concise
  Before/After card. Record only the local reason for the edit; defer feedback
  categorization and preference inference until the Page Run closes.
- If the feedback changes no plan contract or evidence requirement, do not
  rewrite the Shape or Evidence inventory. If it does, touch only the dependent
  planning slice and record that dependency in the Step.

The response returns immediately after the narrow check. Optional cleanup,
whole-Page review, and delivery work are separate commissioned actions, not
implicit background promises.

At explicit Page Run close, read
[`post-run-analysis.md`](post-run-analysis.md) and launch one independent
output-only analysis Task if the supported background mechanism is available.
That Task reads the closed Version by hash and writes its own Result. It never
blocks the next Page Run and never edits the closed journal or Page Content.

## Fast foreground, bounded background

| Foreground, before replying | Conditional / separately commissioned |
|---|---|
| Save raw feedback; read current target and effective rules | Repository-wide history/DNA analysis |
| Revise requested text and dependent Bullet only | Discovery, regression, expensive evidence rendering |
| Save Draft fields + Step; verify narrow source/protected scope | Page Content adoption; web/LaTeX/Word/PDF export |
| Read back saved draft; return full passage + direct links | Full tests, browser/export verification, whole-Page review |

Do not run `outline-pass.py` twice, reload every style source, rebuild the full
Board, or dispatch a fresh reviewer for every wording edit. Use the existing
live Draft Space, which reads the working Shape and embedded Draft fields, and narrow
checks. Delivery remains stale by design until the Page release barrier opens;
never claim a deferred update is visible.

Only actually launched work is called background work. Use the product's
supported task/job mechanism when commissioning it; no unawaited tool promise
or imaginary continuation. Background workers read a frozen source identity
and write their own Results, never shared live prose or approved Shape.
Before incorporation, compare current target/claim/style identities. Stale
work returns as a proposal or is rerun, never overwrites newer human edits.
An evidence contradiction reopens the affected writing question for the
person. Citation/number insertion and export cannot disguise a substantive
rewrite of accepted text.

## Implementation boundary

This update supplies the skill-driven protocol and record template. It does
not add an always-on scheduler or a multi-paragraph atomic promoter. At an
explicit Run close, the host may launch a supported background analysis Task;
an unlaunched Task stays visibly deferred. Sibling
paragraph-group Runs exist because their human questions are independently
closable, not to satisfy an adapter. The Runs presenter reads each Version
journal as one file. The existing `promote_paragraph.py` handles only its
documented single-paragraph Result schema; do not pass these Version journals
to it or manufacture an additional delegated Task Run per accepted paragraph
to satisfy that adapter.
CONTENT may apply a scoped, source-checked Markdown patch and record the
adoption; required owner-specific exporters remain separate workers.
