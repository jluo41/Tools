# Interactive Page Writing Run

This is the human-feedback execution profile of `haipipe-page-workflow`, not a
new Page phase, plugin, or background service. Use it when a person is shaping,
drafting, or revising a Page with the agent. It may start before Shape approval
and before evidence is ready. Published Content still has its existing gates.
For the rationale, see `../../../../../docs/page-writing-philosophy.md`.

## Identity and ownership

| Object | Meaning | When it changes |
|---|---|---|
| Run | One bounded writing goal in one Folder | New independent goal; not each paragraph or chat session |
| Version | One review episode within that goal, e.g. `v001` | Explicitly reopen after closing the previous episode |
| Step | One meaningful human input and the resulting agent response, e.g. `s002` | Each new feedback turn; internal calls are not Steps |
| Review window | The paragraphs/diagram being discussed this turn | May move within the declared Run scope |
| Shape version | The authoritative plan's own approval identity | Its existing protected-fork/approval rules; never the Step counter |

Display `v001/s002` (or `v0.0.1-s2` as a human label), but use one spelling on
disk. Never confuse a writing Version with an outline `v<G>.<S>.<E>` or a
controller receipt's `step`. A writing Run may cover a whole Section while a
turn shows two paragraphs. If the Run was commissioned for P1/P2, adding P3
requires a recorded scope extension from the person, not a quiet expansion.

Use `family: page`, `operation: interactive-writing`, and
`interaction: human-feedback`. Allocate the Run id using the actual Folder
owner's dialect. `r07_page-writing_introduction` below is illustrative, not a
new Paper namespace. Keep one logical Run and paired Result; no child Run per
sentence, paragraph, Step, or version directory.

The workflow owns the conversation history and review state. It invokes:

- `haipipe-page-context`: resolve applicable constraints, style and exemplars;
- `haipipe-page-outline`: change Bullets, Evidence Item requirements, and the
  candidate `outline/<stem>-preview.md` under SHAPE authority;
- `haipipe-writing`: produce or revise the scoped prose under those contracts;
- `haipipe-page-evidence`: commission supporting/local work and bind Results;
- `haipipe-page-content`: adopt explicitly agreed wording into Content and
  produce requested delivery, without another mandatory drafting Run;
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
├── runs/<run>.md                    goal, scope, sources, policy, Result path
└── results/<run>/
    ├── runtime.yaml                 derived current status/pointers
    ├── working.md                   short resume view of effective decisions
    └── v001/
        ├── s001-input.md            original request/feedback, saved FIRST
        ├── s001-result.md           full output, changes, checks, source identity
        ├── s002-input.md
        ├── s002-result.md
        └── close.md                 only after explicit human close
```

Use `writing-step-template.md` for the concrete records. These are ordinary
Markdown records written by the skill's agent, **not a newly implemented CLI,
automatic chat recorder, or UI approval control**. Existing source writers and
their concurrency checks remain in force. Never claim automatic capture of an
unread chat or of feedback from a disconnected session.

`working.md` holds current Version/Step, review window, pending feedback,
effective decisions with source Step ids, accepted paragraph identities, open
evidence dependencies, and next action. It is a resumable view, not the only
history. `runtime.yaml` retains the neutral Run receipt's identity, input hashes,
worker and real start/finish timestamps (unfinished/unknown timestamps are null),
and projects `family`, `operation`, `interaction`, `target`, `ticket`, `result`,
`status`, `version`, `step`. Use `ready`, `running`,
`waiting-for-feedback`, `blocked`, `complete`; waiting is normal and does not
mean failure. Do not depend on a continuously running model process.

Completed input/result records are immutable. If a response needs correction,
append a new Step referencing the earlier one. Save the initial input before
editing; if interrupted, leave that input pending and resume it, without
inventing a completed result. A final `sNNN-result.md` is written only after the
source save and narrow validation succeed. Interrupted or partial work is
described honestly in `working.md`; compare actual files before resuming.

## Each turn

1. **Resume and scope.** Read the Run, `working.md`, latest completed result,
   selected paragraphs, their Bullets/Evidence and effective style rules. On
   initial entry read the whole Section and make one Mermaid argument map;
   later local edits need only the affected slice and adjacent seam. Check
   current source identity; a changed file invalidates cached assumptions.
   Before the first edit of existing prose, retain the full target text and
   relevant planning slice in the initial input. Later Steps may reference the
   preceding immutable result; an external change needs its own new baseline.
2. **Capture the human.** Save `sNNN-input.md` with the original request and
   each feedback item verbatim, its selected quote, addressed target, source
   Version/Step, and reason. Preserve informal language. Agent interpretation
   is a separate field. If source text is ambiguous, record the ambiguity and
   ask only about that item; never silently attach it to the nearest sentence.
3. **Revise within scope.** Choose `local-edit`, `paragraph-rewrite`, or
   `structure` from the user's request, not the model's preference. Bullets and
   prose may inform one another, but an edit to one does not authorize unrelated
   changes to the other. For a Section, one functional Bullet maps to exactly
   one sentence. Update owned evidence requirements when the meaning changes;
   do not invent Results. Missing evidence has named placeholders, never a
   fabricated claim presented as supported.
4. **Save and check.** Save the candidate to the live Markdown authority,
   preserving comment/annotation records. Recheck the base identity before
   applying a patch; on concurrent drift, stop the write and rebase explicitly.
   Verify the target mapping, factual/citation boundaries, and unchanged
   out-of-scope and accepted paragraphs. Capture the exact changed plan and
   evidence slices plus complete paragraph outputs in the Step result, with
   paths and hashes. Hashes alone cannot recover wording: retain actual text.
   Record each feedback item's `applied`, `partly-applied`, `needs-decision`,
   or `not-applied` disposition and reason. `Applied` is never human acceptance.
5. **Return the saved passage.** Use `haipipe-page/ref/user-check-packet.md`'s
   routine packet: full selected paragraphs, concise reasons, updated Mermaid
   only when logic changed, then the two direct Workspace links at the very
   end. Do not polish a second chat-only version or wait for optional exports.
   Set `waiting-for-feedback` and finish the turn.

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
the whole Run, Shape or Page. An explicit “P1 is settled; revise P2” accepts P1
only. Keep accepted P1 byte-for-byte unchanged while revising P2. Reopen P1
only on an explicit scoped request; record the prior accepted snapshot and the
reopening quote. Do not silently clear its acceptance because evidence changed.

A Version closes after every commissioned target is accepted (or explicitly
removed from scope) and the person explicitly closes that writing episode.
Write `close.md` with the decision, final complete passage/map, plan/evidence
snapshot pointers, outstanding dependencies, and hashes of that Version's
input/result records (not a self-hash of `close.md`). The next Version records
the hash of this closure file. A writing Version can close with named evidence owed if the person
agrees; that is **writing-agreed**, not evidence-ready or publishable.
Unresolved factual support still blocks final Content/release. Whole-Page
`CHECK/CLOSE` is a separate later authority.

After closure, continue the same goal by creating `v002`, pointing to
`v001/close.md`, and recording what is being reopened. Never reopen by editing
v001's files. Within an open Version, simply append another Step. A new
Claude/Codex session resumes from the files under the same Run id; the model,
host and chat id are provenance, not identities. A genuinely independent goal
gets a new Run referencing its predecessor. Ordinary human feedback is an
expected evolving input of this profile, not an Execution-contract rerun.

## Fast foreground, bounded background

| Foreground, before replying | Conditional / separately commissioned |
|---|---|
| Save raw feedback; read current target and effective rules | Repository-wide history/DNA analysis |
| Revise requested text and dependent Bullet only | Discovery, regression, expensive evidence rendering |
| Verify source consistency and protected scope; save Step | Full Board build, PDF/Word export, whole-Page review |
| Read back saved draft; return full passage + direct links | Preference synthesis across Versions/Runs |

Do not run `outline-pass.py` twice, reload every style source, rebuild the full
Board, or dispatch a fresh reviewer for every wording edit. Use the existing
live Outline view, which reads Markdown, and narrow checks. If an affected
generated surface is required in this response, refresh and verify that
surface or label it stale; never claim a deferred update is visible.

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
not add a version browser, background scheduler, or a multi-paragraph atomic
promoter. The existing `promote_paragraph.py` handles only its documented
single-paragraph Result schema; do not pass these version directories to it
or manufacture one extra Run per accepted paragraph to satisfy that adapter.
CONTENT may apply a scoped, source-checked Markdown patch and record the
adoption; required owner-specific exporters remain separate workers.
