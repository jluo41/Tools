# How work is driven from a page
state: 🟡 PARTIAL
owner: JL
method: one seam at a time, each ruled for its own reason

## Question
Where does a person see, start, steer and resume paper work, and what does a worker read when it gets there? The Board is the control plane and a coding session is an ephemeral worker, so everything a worker needs has to be ON the page, and everything it produces has to come back to the same page.

`QA7` settles who may write which region. This face is the other half: given a page, how work actually leaves it and comes back. The Board is the control plane and a coding session is an ephemeral worker, so everything a session needs must be ON the page, and everything it produces must return to the same page.

Four questions follow from that one stance: what the control plane is, what the queue is, where a finished item's result lives, and what the runner does when the Board hands it an item.

## Boundary
- ✅ Covered here
  The Board as control plane, the executable queue, where a completed item's handoff lives, and the page-first runner.
- ↪ Covered elsewhere
  Who may write which region is `QA7`; the collaboration as a whole is `QA6`. The live layer's mechanism, one session per question, the drawer, the terminal and in-page locking, is ruled on the tool's own board at `../01-boardform-260722/` (`QD1`-`QD3`, `QE4`).

## Diagram
```
 THE PAGE IS DURABLE. THE SESSION IS NOT.

 ① THE CONTROL PLANE
 ┌ DURABLE — on disk, survives everything ────────────────────┐
 │ the S page: context · Content · queue · comments · gate ·  │
 │             state · completed handoffs                     │
 └────────────────┬───────────────────────────────────────────┘
                  │  "Work this item" / "Work this queue"
 ┌ EPHEMERAL — may disappear mid-sentence ────▼───────────────┐
 │ Claude Code / Codex  ──►  worker sub-agent                 │
 │ works ONE bounded item    a narrow packet ──► evidence     │
 └────────────────┬───────────────────────────────────────────┘
                  │  progress · blockers · results · handoff
                  ▼        back to THE SAME PAGE
 THE TEST: kill the session mid-item. A NEW worker reads the page and
 resumes. Nothing important was ever only in a terminal transcript.

 ② ## Items to Finish IS THE QUEUE
    - [ ] I4 · Rebuild the primary regression columns
          phase: revise      kind: display-render
          from: S-Main-7 · P2.S3      ◄ the sentence that asked
          request / acceptance / status / owner / blocked-by / handoff
    ready ─► claimed ─► done      blocked names its dependency
    it lives HERE and not in a tracker: a queue in another system is a
    second copy of the truth, which is exactly seam ⑦'s failure.

 ⑦ THE RESULT LIVES ON THE ITEM THAT ASKED FOR IT
    ✗ request.md + HANDOFF.md + report.md   a SECOND queue that drifts
    ✅ handoff: artifact · preview · verification · consumer
    evidence still lives in its BANK-owned QA file. The handoff POINTS,
    never copies.

 ⑧ THE RUNNER IS PAGE-FIRST
    work --page <S-face> [--item I4]        and nothing else
    it DERIVES stage · phase · dependencies · worker · stop condition
    stops at:  🧠 a human decision   💸 spend authorization
               ⚠️ unresolved dependency   ⚠️ failed verification
               🚪 the CHECK gate
    DPRC stays the safety model and stops being the user's remote
    control: phases become QUEUE SEMANTICS, not vocabulary a person
    has to hold in their head.

 WHAT THIS FACE DOES NOT DECIDE
    one session per question · the drawer · the real CLI · locking
    ⤷ all ruled on the BOARDFORM board at QD1-QD3 and QE4.
```

## Content
### The Board is the control plane
(QBd1-board-control-plane · was ✅ SETTLED)

#### Durable and ephemeral
```
BOARD / S page          durable: context, Content, queue, comments, gate, state
Claude Code / Codex     ephemeral: works one bounded item and may disappear
worker sub-agent        ephemeral: receives a narrow task packet and returns evidence
```

#### Interaction direction
Work starts from `Work this item` or `Work this queue` on an S page.
Progress, blockers, results, and handoffs return to that same page.
The CLI may remain as an internal recovery surface, but the user should not need to monitor it.

#### Where that seam stood
The architectural direction is accepted.
The Board currently renders the state but does not yet drive the page-first worker loop.

### Items to Finish is the queue
(QBd2-items-are-the-queue · was 🟡 PARTIAL)

#### Proposed item
```markdown
- [ ] I4 · Rebuild the primary regression columns
      phase: revise
      kind: display-render
      from: S-Main-7 · P2.S3
      request: Use the binary exposure as primary.
      acceptance: Prose, caption, columns, estimand, and labels agree.
      status: ready
      owner: --
      blocked-by: --
      handoff: --
```

#### State vocabulary
`ready` can be claimed.
`claimed` has one current owner.
`blocked` names the unresolved dependency.
`done` requires verification and a checked box.

#### Concurrency
One worker owns one S page at a time.
Different S pages may run in parallel because they do not edit the same queue or Content.

#### Where that seam stood
The queue location and candidate schema are selected.
Claim recovery and the exact minimal field set remain open.

### Handoff stays on the item
(QBd3-handoff-on-the-item · was ✅ SETTLED)

#### Existing Display
A request for `display04` goes directly into `S-Display-4`.
The worker updates the same Display unit and closes the item on that page.
The requesting Section keeps the stable `display_id`.

#### New Display
A not-yet-allocated Display begins as one item on the Display stage page.
When accepted, the creator makes `S-Display-N`, moves the item verbatim into it, and removes it from the unallocated queue.
The new S page is the Display, not a request sidecar.

#### Handoff contents
```
handoff:
  artifact: live output path
  preview: inspectable rendering
  verification: what was checked
  consumer: page or adapter that uses it next
```

#### Where that seam stood
The no-sidecar ruling is explicit.
Current paper skills still contain `_DISPLAY_REQUEST.md` routes and have not been migrated.

### A page-first stage runner
(QBd4-page-first-runner · was ✅ SETTLED)

#### Entry
```text
work --page <S-face-path> [--item <local-id>]
```

#### Loop
```
resolve page and explicit stage key
load stages/index.yml and only that stage contract
read requires, style-from, Content, queue, comments, and state
select and claim one allowed item
dispatch the worker declared for its kind
verify the returned result
update Content, item handoff, Where we are, state, and Board
continue only when the user asked to work the queue
```

#### Stop
Stop at a human decision, spend authorization, unresolved dependency, CHECK gate, or failed verification.
DPRC remains a safety model, but phases become queue semantics rather than the user's remote-control language.

#### Where that seam stood
The loop is designed and recorded.
The live stage skill remains stage-first and has not been compacted around this entry.

## Items to Finish
- [x] 🧭 Choose the Board as the remote control plane
      The durable working state lives on pages rather than in session memory.
- [ ] 🖱 Define the two Board actions
      `Work this item` and `Work this queue` need exact stop and refresh behavior.
- [ ] 🔍 Make progress visible
      Claimed owner, blocker, result, verification, and handoff must be visible on the page.
- [ ] 🧪 Resume from a new session
      A fresh session should continue a page without reading the previous transcript.
- [x] 📋 Reuse Items to Finish
      No second task list is created beside the page.
- [ ] 📐 Freeze the minimal fields
      Keep enough structure for recovery without turning Markdown into a verbose database.
- [ ] 🔒 Define claim and release behavior
      A dead session must not leave an item permanently claimed or allow two page writers.
- [ ] 🧪 Drain a three-item queue
      Verify ready, blocked, and human-decision items stop and resume correctly.
- [x] 🚫 Reject `_DISPLAY_REQUEST.md`
      Existing Display work goes to its owning page and new work starts on the Display stage page.
- [x] 📎 Reject a separate Handoff file
      The originating item carries its own result and downstream pointer.
- [ ] 📐 Define the compact handoff syntax
      It must remain readable Markdown and support more than Display work.
- [ ] 🧹 Migrate future writers
      Stop skills from generating request sidecars or writing completed work only to chat.
- [x] 🧭 Choose page-first invocation
      The Board provides a page and optional item, not a sequence of internal phase commands.
- [ ] 📐 Give every page an explicit stage key
      The runner must not infer execution logic from filenames, Pages order, or Board family.
- [ ] 🧰 Declare worker routes in each stage contract
      The root runner knows the loop, not the craft of every stage.
- [ ] 🧪 Forward-test three item kinds
      Test one Section edit, one existing Display revision, and one evidence-bearing request.

## Where we are
Merged 260726 from 4 faces that each ruled one seam of the same joint (JL). Every division, item and Law below is the original's, unchanged; only the framing above is new.

## Files
- `haipipe-board/`
  The durable interaction surface.
- `haipipe-paper-stage/`
  The execution engine behind an S page.
- `haipipe-board/ref/q-template.md`
  The current Items to Finish grammar.
- `haipipe-paper-stage/SKILL.md`
  The future queue loop.
- `stages/4-display/stage.md`
  Still declares the retired inbox.
- `haipipe-paper-draft-display/SKILL.md`
  Still files Display request rows.
  The runner to narrow.
- `stages/index.yml`
  The stage registry.
- `stages/*/stage.md`
  The permitted worker routes and stop conditions.

## Law

