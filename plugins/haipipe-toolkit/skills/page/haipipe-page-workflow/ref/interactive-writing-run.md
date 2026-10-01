# Page Run · interactive writing

This is the canonical **Page Run**: the human-interaction execution profile of
`haipipe-page-workflow`, not a
controller label, workbench, or background service. Use it when a person is shaping,
drafting, or revising a Page with the agent. It may start before Shape approval
and before evidence is ready. Published Content still has its existing gates.
For the fused Structure Run, also load `structure-run.md`: SHAPE and SURVEY
are cycles of one `run-structure-<MMDD>-<slug>`, including when several people participate.
For the rationale, see `../../../../../docs/page-writing-philosophy.md`.

## 🔖 Run bookends · the Draft changes during a Run; records wait for its close

JL 260928, in the Section sessions of a paper: "if I am editing the Section,
here I say a run is start ... When I say a run is over, then you start to do the
summary and recording the results ... in the middle, we focus on the content";
"don't change the log in the middle way, during the run, do it until we
finished the run." A chat-driven writing Run (`rp-struct`, `rp-sec`, `rp-para`)
has two bookends the person calls, and this section overrides every per-turn
recording instruction later in this file:

```text
OPEN     the person starts the Run          name it once: Run id, target, Draft file; write nothing else
MIDDLE   every feedback turn                edit ONLY the Draft file (Draft prose + dependent Bullets)
CLOSE    the person says the Run is over    self-review when asked, then write the Run's records once
AFTER    the person asks for delivery       adopt the Draft into Page Content, then web → LaTeX → Word
```

**Middle.** The only file that changes is the Draft file:
`draft/<stem>-draft-v<N>.md` (`outline/<stem>-outline-v*.md` in the older
layout). Untouched until the close: Page Content in `<stem>.md`,
`results/<run>/` (`vNNN.md`, `working.md`, `runtime.yaml`), `runs/` tickets,
`draft/records/` log, context, discussion and feedback records, evidence-item
notes, receipts, and `delivery/`. A ruling routed from another session while
the Run is open is applied to the Draft the same way and recorded at the close.
The conversation is the mid-Run record: each reply quotes the feedback it acts
on and shows the changed passage, so the close can write both verbatim. The
Section's Claude session or Codex thread, named in the page header, persists
that conversation; a session that ends before the close leaves it for the next
session to read and close.

**Close.** One pass, in this order, then report what was written:

1. the Run ticket in `runs/` and the Version journal `results/<run>/vNNN.md`: one `## Step` per completed cycle, each with verbatim `### Human feedback`, `### Saved result` and Track changes cards, then `## Version closure` with the person's closing words and the session id as the source;
2. `working.md` and `runtime.yaml`, with real start and finish timestamps;
3. ONE entry for the whole Run in `draft/records/<stem>-log.md`;
4. decision threads closed or opened, evidence-item notes, and superseded Runs marked.

**After.** Only when the person asks: adopt the closed Draft into Page Content,
then run the delivery lanes, web page first, then LaTeX, then Word. A lane that
its own gate blocks (for example strict evidence selection) reports the blocker
and stops; nothing is forced.

A feedback turn that arrives with no Run open opens one: name it once and
follow the same bookends. Scratch (`Finish Scratch`) and Revise (each `Save`)
are button-driven: the person's press is the record, so they keep their own
save behavior.

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

The first structure Run is always `run-structure-<MMDD>-<slug>`, even when the Page was
imported with a draft Shape. RP allocation is Page-local and type-explicit:

| IDs | Scope | What the Run settles |
|---|---|---|
| `run-structure-<MMDD>-<slug>` | Page Structure Run: SHAPE + SURVEY | Page direction, coverage/non-coverage, high-level section flow, ordered Bullets, Point roles, paragraph jobs, typed evidence decisions, the structure list, and the frozen `P01..PN` index; no adopted prose or material evidence execution |
| `run-scratch-<MMDD>-<slug>` | Human Scratch capture | rough thinking for one Section (`C1`) or whole paragraph group (`C1.P1`) in the current Outline grammar; B/symbol rows are not targets; the person manually triggers Finish Scratch and the AI generates the closing Summary |
| `run-section-<MMDD>-<slug>` | Section-level | One named Section drafting/revision round and its candidate, review/rating, diagnosis, revision, and report |
| `run-paragraph-<MMDD>-<slug>` | Paragraph-level | One fixed paragraph or contiguous paragraph group, such as `P03–P05` |
| `run-revise-<MMDD>-<slug>` | Revise | Two frozen texts of one target compared; one change ledger row per material change with Before, After, kind, Why, and Decision; the accepted text returns to the owning writing Run as a Version (`haipipe-page-revise`) |

`run-structure-<MMDD>-<slug>` is the initial Structure Run and contains both SHAPE and SURVEY.
It may contain many Steps while the map, Bullets, roles, and evidence routes
are being settled. Several people share this Run: record `participants` on the
Run and `contributors` on each Step; joining the review does not allocate a
new RP. `run-structure-<MMDD>-<slug>` and later ids are optional independent post-closure
structural goals, not separate Survey Runs. Scratch is available as
a small human planning capture once the selected Outline exists; it does not
write Draft prose or bypass later Structure or evidence gates. Only after
the Structure contract is closed may the workflow propose Section Runs in
`run-section-<MMDD>-<slug>` or paragraph Runs in `run-paragraph-<MMDD>-<slug>`.

For Section-level writing, one complete draft → review/rating → diagnose →
revise cycle is one Step inside the current Section Run, not a new Run. The
agent must review and diagnose again after revising; self-revision is not
self-acceptance. A later independently commissioned Section drafting/revision
session—such as after a substantial structure change—gets a new `run-section-<MMDD>-<slug>`
Run. Within the same commissioned round, later feedback appends another Step.

The four RP kinds are sibling Page Runs; structure, Scratch, Section, and
paragraph Runs are not children of one another. For paragraph-level writing, keep the
paragraph or contiguous range fixed. A
later revisit of that same target normally reopens the same Run in a new
Version; a materially different target or goal gets a new `run-paragraph-<MMDD>-<slug>` Run.
Group adjacent paragraphs only when one human decision must accept or revise
them together. Thus `run-paragraph-<MMDD>-<slug>`, `run-paragraph-<MMDD>-<slug>`, and
`run-paragraph-<MMDD>-<slug>` are valid examples. If the closed index has `N` paragraphs,
its paragraph candidates satisfy `1 <= K <= N`; the RP sequence and paragraph
serial are separate coordinates. The Page RP identity and a native Task Run
may coexist, for example `run-paragraph-<MMDD>-<slug>` and `r01`.

Before paragraph selection, show the complete candidate list in frozen reading order using
Candidate numbers, never future typed RP identities. Allocate only the selected
next candidate. Sequential work is the default; parallel Page Runs require
explicit selection and non-overlapping targets. If the plan changes, recompute
only unallocated candidates. Never renumber or silently redefine an allocated
Run.

Use `family: page`, `operation: interactive-writing`, and
`interaction: human-feedback` for prose review/writing. A Scratch ticket also
uses `mode: scratch`, `target_scope: section|subsection|paragraph`, and
`interaction: human-scratch`. Allocate `run-structure-<MMDD>-<slug>` first for structure, then use the
next free identity whose kind matches the selected scope. Semantic names belong
in Goal, not in the identity. Never rename a Task/Discovery Run to an RP, and
never consume its `rNN` counter when allocating a Page Run. Reject an identity
whose kind or paragraph target does not match its scope; it cannot unlock or
substitute for a canonical Run.
Within each logical Run, keep
one paired Result and create no child Run per sentence, Step, Version, or
internal agent call.

Every paragraph Run and every reader-facing review packet also carries the
frozen Structure description for each selected paragraph. Resolve it
from the closed `run-structure-<MMDD>-<slug>` index in the Outline, for example `P06 · C3.P6 · Scope and acceptance`.
Do not replace this frozen description with a newly invented Goal sentence.
Missing or conflicting descriptions are visible blockers.

The workflow owns the conversation history and review state. It invokes:

- `haipipe-page-context`: resolve applicable constraints, style and exemplars;
- `haipipe-page-structure`: change Bullets, Evidence Item requirements, and the
  embedded Drafts in the selected Outline Markdown under SHAPE
  authority;
- `haipipe-writing`: produce, revise or evaluate scoped prose under the shared
  request, selected methods and rubric described below;
- `haipipe-page-evidence`: commission supporting/local work and bind Results;
- `haipipe-page-writing`: after every planned Page Run and required evidence
  Task Result is complete, adopt all agreed wording and produce delivery once;
- `haipipe-page-check`: judge an exact delivered Page, not each chat edit.

Page/Execution/Discovery are work families. Human-feedback/delegated is a
different distinction. A local Page Evidence Item Run can be delegated;
searching, computation and export are not interactive writing Steps merely
because they serve a paper. They retain their own Run contracts when they are
independently commissioned. A routine build need not become a ceremonial Run.

## Small, Markdown-first storage

For Section and Paragraph Runs, the agent invokes Writing using
`../../../writing/haipipe-writing/ref/writing-request.md`.
The Ticket freezes selected methods and the base rubric identity; the Step
adds its exact baseline, original feedback and editable scope. Use default
native writing and self-review when no external method is selected. A supplied
DNA or anti-slop packet selects its adapter once. Resolve only selected methods
under `../../../writing/haipipe-writing/ref/method-adapter-contract.md`.

Writing returns candidate, actual changes, evaluation, method trace and
unresolved findings. The host saves the candidate into the Draft file under
the existing source writer/concurrency rules; its review goes into the
Version/Step written at the Run's close.
Evaluation follows `../../../writing/haipipe-writing/ref/evaluation.md`:
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
├── draft/                           current editable planning authority
│   ├── <stem>-draft-v1.2.md          current Shape + embedded Drafts (Draft-first)
│   ├── previous/                     superseded versions (v1.1, v1.0, …)
│   └── <stem>-evidence-items.md     requirements and Supporting/Local graph
├── runs/`run-structure-<MMDD>-<slug>`.md             initial Structure Run: SHAPE + SURVEY
├── runs/`run-structure-<MMDD>-<slug>`.md             structure/Bullet refinement Run
├── runs/`run-scratch-<MMDD>-<slug>`   human Scratch capture Run
├── runs/`run-section-<MMDD>-<slug>`.md                Section Run
├── runs/`run-paragraph-<MMDD>-<slug>`     paragraph Run
├── runs/`run-revise-<MMDD>-<slug>`    Revise Run: before · after · decisions
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
(`haipipe-workbench-page` §✍️). A small `+` targets a Section or whole
paragraph group; B/symbol rows have no Scratch control. The current
grammar has no separate subsection node, so there is one plus per visible
target. It writes the rough note to the selected Outline's `##
Scratch` registry while creating/updating the paired Scratch Run. `Save`
leaves the Run open. The person manually clicks `Finish Scratch`, which asks
the AI to generate a concise non-empty Summary from the raw notes, writes
`AI generated the Scratch Summary and the person closed the Run.` to the Result,
and closes the Run. A closed Scratch Run is immutable; later thinking starts a
new Scratch Run. Scratch Mode keeps saved raw Scratch visible by default even
when the underlying body is hidden. This capture never edits Draft prose.
Ordinary feedback
still enters a Page Writing Run as a pending `### Human feedback` Step, but it
is not a Draft-space composer.

## ⚡ Fast foreground rule

For ordinary wording feedback, finish one Step in under two minutes when the
current Run records are available. Read only `working.md`, the latest saved
result tail, the exact target paragraph slice, its dependent Bullet, and the
frozen Structure description. Under the Run bookends, write only the Draft
file; the Step journal and resume projections are written once at the close. Make
one bounded patch and one narrow check, then return the packet. Do not start or
wait for a sub-agent, reread the whole Page or Version, update wording-only
plan metadata, run an outline pass, build, export, test broadly, verify the
browser, or perform preference analysis. If a required record is missing,
return one named blocker instead of scanning the repository.

`working.md` holds current Version/Step, review window, pending feedback,
effective decisions with source Step ids, accepted paragraph identities, open
evidence dependencies, and next action. It is a resumable view, not the only
history. `runtime.yaml` retains the neutral Run receipt's identity, input paths,
worker and real start/finish timestamps (unfinished/unknown timestamps are null),
and projects `family`, `operation`, `interaction`, `target`, `ticket`, `result`,
`status`, `version`, `step`. Use `ready`, `running`,
`waiting-for-feedback`, `blocked`, `complete`; waiting is normal and does not
mean failure. Do not depend on a continuously running model process.

One Version is one append-only Markdown journal. Every completed Step is a
`## Step sNNN` section in that same file and contains both `### Human feedback`
and `### Saved result`. The journal is written at the Run's close from the
conversation (Run bookends): one Step per completed draft/review/diagnose/revise
cycle, in order. A partial clarification or an unfinished self-revision at the
close is written as a pending Step, not a new Run.
Once written, Step sections are immutable: a later correction appends a new
Step that references the earlier one. A session that stops before the close
writes nothing; its persisted conversation is the record the next session
reads to resume or close the Run. Compare actual files before resuming.

## Each turn

1. **Resume and scope.** Read the Run, `working.md`, latest completed result,
   selected paragraphs, their Bullets/Evidence and effective style rules. On
   initial entry read the whole Section and make one structure list;
   later local edits need only the affected slice and adjacent seam. Check
   current source identity; a changed file invalidates cached assumptions.
   Before the first edit of existing prose, retain the full target text and
   relevant planning slice in the initial input. Later Steps may reference the
   preceding immutable result; an external change needs its own new baseline.
2. **Capture the human.** In the reply, quote the original request and each
   feedback item verbatim, with the selected quote, addressed target, and
   reason; at the Run's close these become the Step's `### Human feedback` in
   `vNNN.md` (Run bookends). Preserve informal language. Agent interpretation is separate. If
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
   rating scale. For `run-structure-<MMDD>-<slug>`, SHAPE updates
   structure list and Outline Bullets together, while SURVEY updates typed Evidence
   Item route decisions in that same Run; neither cycle creates a second
   planning Run. For a paragraph Run, keep the fixed target
   range. Bullets and prose may inform one another, but an edit to one does
   not authorize unrelated changes to the other. Update owned evidence
   requirements when the meaning changes; do not invent Results. Missing
   evidence has named placeholders, never a fabricated claim presented as
   supported.
4. **Save the completed Step.** Save the candidate in the Draft file
   (`draft/<stem>-draft-v<N>.md`; `outline/<stem>-outline-v*.md` in the older
   layout), update only its dependent Bullets in the working Shape, and
   preserve comment/annotation records. Recheck the narrow base and
   protected targets before writing; on concurrent drift, stop and rebase.
   That Draft write is the only write during the Run. The candidate,
   affected planning snapshot, review/rating, diagnosis, narrow checks, each
   feedback disposition, a changed Evidence requirement, and the Track
   changes cards below go into the Step's `### Saved result` at the close,
   with `working.md` and `runtime.yaml` (Run bookends).
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
   one visible `### PNN · Cn.Pm · <Structure description>` heading per paragraph, with each paragraph in
   its own blockquote and chat-only `S1`, `S2`, ... sentence labels; then one concise explanation
   of what changed and why. Do not emit a fixed status list or an empty Evidence
   section. Add Evidence commentary only when this Step changed or left open a
   citation, value, or figure requirement. End with the verified Draft Space,
   Evidence Space, and Current Run links, with nothing after
   them. Show an updated structure list only when the logic changed. Do not polish a second
   chat-only version or wait for optional exports. Finish the turn; the Run
   is waiting for feedback, with no status write until the close.

When a person enters, continues, resumes, or asks to review an open Run before
giving new feedback, return the packet's pre-Step review format instead. Show
the latest complete candidate grouped by paragraph with
`### PNN · Cn.Pm · <Structure description>` headings and `S1...Sn`
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
accepted text**. Acceptance is its own Step even when no prose changes;
like every Step it is written at the Run's close (Run bookends). Do not append
a tick to an already completed result.
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
The person decides when the Run is over. Every commissioned target must be
accepted or explicitly removed and its Bullets settled; every Evidence
obligation is named in the closure record as `none`, bound, or still owed. An
owed item stays owed on the Page's evidence items, and its gate blocks the
later LaTeX and Word lanes, not the close.

Run closure seals the current Version before any post-run analysis Task is
launched. Closing a Version alone does not silently mint a new Run.

Append `## Version closure` to the same `vNNN.md`, including `### Human close`,
the final complete passage/map and plan/evidence snapshot pointers. After
closure, the whole Version file is immutable. The next Version names the
closed `vNNN.md` (its number and close date) before any new Step. Accepted wording whose named
evidence is still owed is recorded as accepted with the owed items listed;
commission or resume the owner-native Task Run for them. Do not call factual
support, citation, value, or figure output resolved while it is owed.
Whole-Page `CHECK/CLOSE` is a separate later authority.

Closing a Page Run does not by itself modify `<page>.md` or `delivery/`. When
the person asks right after the close (the practiced sequence: "close this run,
and then go to the run-delivery"), adopt the closed Draft into Page Content and
run the lanes web page → LaTeX → Word; each lane's own gate (strict evidence
selection for LaTeX and Word) decides whether it builds, and a blocked lane
reports its blocker. Without that request, the Page release barrier holds until
the required structure/Bullet RP Runs, Section RP Runs, paragraph RP Runs, and
every required evidence Task Result are complete and bound; CONTENT then applies all accepted
candidates in one Page-level pass and generates web, LaTeX, and Word once
before CHECK.

After Version closure, continue the same fixed goal by creating `v002.md`,
naming closed `v001.md` as its prior Version, and recording what is being reopened.
Never reopen by editing `v001.md`. Within an open Version, append another
Step only when it completes the next scoped cycle. A new Claude/Codex chat can
resume the same Run, but a later independently commissioned Section
drafting/revision session receives a new `run-section-<MMDD>-<slug>` identity referencing its
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
- Read only the exact target sentences in the Draft file and the dependent
  Bullet/Evidence slice; the conversation so far is the recoverable baseline.
- Make one bounded edit transaction: change the target sentences and dependent
  Bullets in the Draft file, then run one narrow scope check. No Step,
  `working.md` or `runtime.yaml` write until the close (Run bookends).
- Do not run `outline-pass.py`, a full Page parser, a repository-wide search,
  browser verification, delivery generation, full tests, or a fresh reviewer
  for a local wording change.
- Keep the reply complete but compact: the raw feedback, selected
  quote/annotation, complete candidate passage, disposition, and a concise
  Before/After, so the close can write the Step from it. Give only the local
  reason for the edit; defer feedback categorization and preference inference
  until the Page Run closes.
- If the feedback changes no plan contract or evidence requirement, do not
  rewrite the Shape or Evidence inventory. If it does, touch only the dependent
  planning slice and record that dependency in the Step.

The response returns immediately after the narrow check. Optional cleanup,
whole-Page review, and delivery work are separate commissioned actions, not
implicit background promises.

At explicit Page Run close, read
[`post-run-analysis.md`](post-run-analysis.md) and launch one independent
output-only analysis Task if the supported background mechanism is available.
That Task reads the closed Version by its number and writes its own Result. It never
blocks the next Page Run and never edits the closed journal or Page Content.

## Fast foreground, bounded background

| Foreground, before replying | Conditional / separately commissioned |
|---|---|
| Quote raw feedback in the reply; read current target and effective rules | Repository-wide history/DNA analysis |
| Revise requested text and dependent Bullet only | Discovery, regression, expensive evidence rendering |
| Save Draft fields only; verify narrow source/protected scope | Run records (at close); Page Content adoption; web/LaTeX/Word/PDF export |
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
