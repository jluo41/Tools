# Page Run · interactive writing

This is the canonical **Page Run**: the human-feedback execution profile of
`haipipe-page-workflow`, not a
new Page phase, plugin, or background service. Use it when a person is shaping,
drafting, or revising a Page with the agent. It may start before Shape approval
and before evidence is ready. Published Content still has its existing gates.
For the rationale, see `../../../../../docs/page-writing-philosophy.md`.

## Identity and ownership

| Object | Meaning | When it changes |
|---|---|---|
| Run | `rp00_mermaid-structure`, or one numbered paragraph group after it closes | New independent human question or acceptance boundary; not each chat session |
| Version | One review episode within that goal, e.g. `v001` | Explicitly reopen after closing the previous episode |
| Step | One meaningful human input and the resulting agent response, e.g. `s002` | Each new feedback turn; internal calls are not Steps |
| Review window | The paragraphs/diagram being discussed this turn | May move within the declared Run scope |
| Shape version | The authoritative plan's own approval identity | Its existing protected-fork/approval rules; never the Step counter |

Display `v001/s002` (or `v0.0.1-s2` as a human label), but use one spelling on
disk. Never confuse a writing Version with an outline `v<G>.<S>.<E>` or a
controller receipt's `step`. A paragraph-group Run may cover adjacent
paragraphs only when the person must judge them together as one rhetorical
move. If the Run was commissioned for P01-P02, adding P03 requires a recorded
scope extension from the person, not a quiet expansion.

## Page-level cardinality

The first Page Run is always the whole-Page **Mermaid Structure** interaction,
even when the Page was imported with a draft Shape. Human and agent iterate
until the person explicitly closes the Mermaid argument map and Page-global
paragraph index. Do not propose or allocate paragraph Runs before this closure.

The closure numbers all `N` paragraphs in reading order as `P01..PN` and maps
each serial to its plan address. Then partition them into `K` sibling
paragraph-group Page Runs:

```text
rp00_mermaid-structure  Mermaid Structure + P01..PN index
rp01_p01                one paragraph
rp02_p02-p03            one contiguous paragraph group
1 <= K <= N
```

Ten paragraphs may need 10, 8, or 6 paragraph Page Runs, in addition to the
Mermaid Structure Run. Split paragraphs when they ask different questions, rely on
different evidence, change different meanings, or can be accepted separately.
Group adjacent paragraphs only when one human decision must accept or revise
them together.

Before paragraph selection, show the complete candidate list in frozen reading order using
Candidate numbers, never future `rpNN` identities. Allocate only the selected
next candidate. Sequential work is the default; parallel Page Runs require
explicit selection and non-overlapping targets. If the plan changes, recompute
only unallocated candidates. Never renumber or silently redefine an allocated
Run.

Use `family: page`, `operation: interactive-writing`, and
`interaction: human-feedback`. Allocate the first identity as
`rp00_mermaid-structure`. After it closes, allocate paragraph identities as
`rpNN_pNN[-pNN]`; `rp` means Run of Page. Semantic names belong in Goal, not in
the identity. `rp00` is reserved and may not be allocated to another Page goal.
Paragraph allocation starts at `rp01`. This sequence is independent from
delegated Task Runs, so `rp01` and `r01` may coexist in the same Page Folder.
Never rename a Task/Discovery Run to `rpNN`, and never consume its
`rNN` counter when allocating a Page Run. Paragraph groups are sibling Runs.
There are no Page Run aliases. Reject any `interactive-writing` identity other
than `rp00_mermaid-structure` or `rpNN_pNN[-pNN]` from `rp01`; it cannot unlock
or substitute for a canonical Run.
Within each logical Run, keep
one paired Result and create no child Run per sentence, Step, Version, or
internal agent call.

Every paragraph Run and every reader-facing review packet also carries the
frozen Mermaid Structure description for each selected paragraph. Resolve it
from the closed `rp00_mermaid-structure` index or authored
`outline/<stem>-logic.mmd`, for example `P06 · C3.P6 · Scope and acceptance`.
Do not replace this frozen description with a newly invented Goal sentence.
Missing or conflicting descriptions are visible blockers.

The workflow owns the conversation history and review state. It invokes:

- `haipipe-page-context`: resolve applicable constraints, style and exemplars;
- `haipipe-page-outline`: change Bullets, Evidence Item requirements, and the
  candidate `outline/<stem>-preview.md` under SHAPE authority;
- `haipipe-writing`: produce or revise the scoped prose under those contracts;
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

```text
<folder>/
├── outline/                         current editable planning authority
│   ├── <stem>-outline-v1.2.md        unapproved working Shape (if needed)
│   ├── <stem>-preview.md            current candidate sentences + comments
│   └── <stem>-evidence-items.md     requirements and Supporting/Local graph
├── runs/rp00_mermaid-structure.md   whole-Page Mermaid Structure interaction
├── runs/rpNN_pNN[-pNN].md           one numbered paragraph group
└── results/<same-run>/
    ├── runtime.yaml                 derived current status/pointers
    ├── working.md                   short resume view of effective decisions
    ├── v001.md                      all Steps in this review episode, in order
    └── v002.md                      next episode; created only after reopening
```

Use `writing-step-template.md` for the concrete records. These are ordinary
Markdown records written by the skill's agent, **not a newly implemented CLI,
automatic chat recorder, or UI approval control**. Existing source writers and
their concurrency checks remain in force. Never claim automatic capture of an
unread chat or of feedback from a disconnected session.

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

One Version is one append-only Markdown journal. Every Step is a `## Step
sNNN` section in that same file and contains both `### Human feedback` and
`### Saved result`. Save the Human feedback subsection before editing, then
append the Saved result after the source save and narrow validation succeed.
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
2. **Capture the human.** Append `## Step sNNN` to `vNNN.md`, then save its
   `### Human feedback` subsection with the original request and each feedback
   item verbatim, selected quote, addressed target, source Version/Step, and
   reason. Preserve informal language. Agent interpretation is separate. If
   source text is ambiguous, record it and ask only about that item; never
   silently attach it to the nearest sentence.
3. **Revise within scope.** Choose `local-edit`, `paragraph-rewrite`, or
   `structure` from the user's request, not the model's preference. Bullets and
   prose may inform one another, but an edit to one does not authorize unrelated
   changes to the other. For a Section, one functional Bullet maps to exactly
   one sentence. Update owned evidence requirements when the meaning changes;
   do not invent Results. Missing evidence has named placeholders, never a
   fabricated claim presented as supported.
4. **Save the fast foreground.** Save the candidate in
   `outline/<stem>-preview.md`, update only its dependent Bullets in the working
   Shape, and preserve comment/annotation records. Recheck the narrow base and
   protected targets before writing; on concurrent drift, stop and rebase.
   Update an Evidence requirement only when this feedback changes what the
   paragraph must cite, measure, or show. Append the complete candidate,
   affected planning snapshot, narrow checks, and each feedback disposition to
   the same Step's `### Saved result`. Update `working.md` and `runtime.yaml`.
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
   citation, value, or figure requirement. End with the verified Bullet
   Workspace, Evidence Workspace, and Current Run links, with nothing after
   them. Show an updated Mermaid only when logic changed. Do not polish a second
   chat-only version or wait for optional exports. Set `waiting-for-feedback`
   and finish the turn.

When a person enters, continues, resumes, or asks to review an open Run before
giving new feedback, return the packet's pre-Step review format instead. Show
the latest complete candidate grouped by paragraph with
`### PNN · Cn.Pm · <Mermaid Structure description>` headings and `S1...Sn`
labels, the exact review scope, the next proposed `vNNN/sNNN`, and the Bullet
Workspace, Evidence Workspace, and Current Run links. Do not append a Step
until the person supplies feedback, acceptance, or an explicit close. A
pre-Step packet is a review surface, not a new journal record.

Between Steps and Runs, follow `ref/interactive-execution-policy.md`.
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

A Version closes after every commissioned target is accepted (or explicitly
removed from scope), its Bullets are settled, every Evidence obligation is
explicit and ready (`none` or a bound CITE, VALUE, or DISPLAY Result), and the
person explicitly closes that writing episode.

For an interactive Page Run, this Version closure is the Page Run close event.
The close seals the Version before any post-run analysis Task is launched.

Append `## Version closure` to the same `vNNN.md`, including `### Human close`,
the final complete passage/map and plan/evidence snapshot pointers. After
closure, the whole Version file is immutable. The next Version records the
closed `vNNN.md` hash before any new Step. If accepted wording still has named
evidence owed, record the acceptance but keep the Page Run open; commission or
resume the owner-native Task Run and return for evidence review. Do not mark the
Page Run complete while factual support, citation, value, or figure output is
unresolved. Whole-Page `CHECK/CLOSE` is a separate later authority.

Closing a Page Run does not modify `<page>.md` or `delivery/`. The Page release
barrier opens only when `rp00_mermaid-structure`, every planned paragraph Page
Run, and every required evidence Task Result are complete and bound. CONTENT
then applies all accepted candidates in one Page-level pass, integrates the
ready evidence, and generates web, LaTeX, and Word once before CHECK.

After closure, continue the same goal by creating `v002.md`, pointing to the
hash of closed `v001.md`, and recording what is being reopened. Never reopen by
editing `v001.md`. Within an open Version, append another Step. A new
Claude/Codex session resumes from the files under the same Run id; the model,
host and chat id are provenance, not identities. A genuinely independent goal
gets a new Run referencing its predecessor. Ordinary human feedback is an
expected evolving input of this profile, not an Execution-contract rerun.

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
| Save preview + Step; verify narrow source/protected scope | Page Content adoption; web/LaTeX/Word/PDF export |
| Read back saved draft; return full passage + direct links | Full tests, browser/export verification, whole-Page review |

Do not run `outline-pass.py` twice, reload every style source, rebuild the full
Board, or dispatch a fresh reviewer for every wording edit. Use the existing
live Bullet Workspace, which reads the working Shape and preview, and narrow
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
