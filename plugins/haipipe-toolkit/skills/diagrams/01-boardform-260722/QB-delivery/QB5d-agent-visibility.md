# Chat about one location

state: 🟡 PARTIAL · sentence focus settled; section/subsection focus designed, not implemented
owner: JL
method: generate render-local paths for page headings plus fine Content addresses, then reuse one page Chat session for either focus

## Question
How can someone copy or call Chat about one section, subsection, heading, or sentence without creating a separate session for every location?

The Board already has one chat session per page. A sentence therefore needs a focus address and an entry button, not another session.
Every rendered `##` section and `###` subsection now also needs a human-readable generated path.
Inside Content, the existing fine address remains: `C` is a Content division, `H` is a terminal Heading node, and prose uses sibling `P.S` leaves.

## Boundary
- ✅ Covered here
  Generated section/subsection paths, automatic Content sentence addresses, Copy and Chat actions, and the context handed to the existing page chat.
- ↪ Covered elsewhere
  Sentence-local human comments are `QA6`; tracked edits are `QAb2`; typed evidence lanes are `QAb1`; one session per page is `QD1`.

## Diagram

```
QAb3 Content
  C1 · Addressing
    H1 · Generated, not stored        → QAb3.C1.H1
    first prose sentence              → QAb3.C1.P1.S1
    second prose sentence             → QAb3.C1.P2.S1

sentence action rail
  The Board already has one chat session per page.  C2.P1.S1 ＋ 💬
                                                              │
                                                              ▼
existing QAb3 chat session
  FOCUS  QAb3.C2.P1.S1                               ×
  C2 · Chat behavior
  H1 · One page session
  The Board already has one chat session per page.
  Attached · 2                                       ▸

  Ask about this sentence…                            Send

heading focus
  📍 Where we are
     Current decision        QAb3 / Where we are / Current decision  ⧉ 🤖
                                                                       │
                                                                       ▼
  existing QAb3 chat session
  FOCUS  section/subsection path · source file · visible heading/body
```

## Content
### §1 Addressing
#### Section and subsection paths
Every rendered `##` section and `###` subsection receives a generated human-readable breadcrumb, for example `QAa5 / Where we are / Current decision`.
Copy includes the page id, breadcrumb, and Markdown source path so Claude Code can locate it without guessing.
The breadcrumb is render-local UI metadata, just like the existing Content addresses; renaming or moving a heading recomputes it and never rewrites the source merely to preserve an obsolete index.

#### Generated, not stored
The browser assigns addresses after each Board render and again after a live refresh.
Nothing is added to the Markdown, so renumbering never produces source-file churn.
The full sentence address is page id plus Content, Paragraph, and Sentence, for example `QAb3.C2.P1.S1`.

#### C, H, P, and S
`C` counts `###` divisions only inside `## Content`.
`H` counts `####` headings inside its `C` and terminates there, for example `QAb3.C1.H1`.
`P` is a sibling of `H`, not its child; prose therefore uses `QAb3.C1.P1.S1`, never `QAb3.C1.H1.P1.S1`.
Board writing keeps one source sentence per line, so each current paragraph ends in an S-one leaf; the explicit sentence level leaves room for a future paragraph containing more than one sentence.

### §2 Chat behavior
#### One focus packet
Section, subsection, and sentence actions all reuse the existing page Chat session.
A heading-focus packet carries page id, section and subsection names, source file, and the visible block; a sentence-focus packet keeps its current `C.P.S` address and direct apparatus.

#### One page session
Clicking a sentence's `💬` opens the existing chat for that Q.
It does not create a sentence session, a new session id, or a second conversation history.

#### Explicit focus packet
Clicking `💬` establishes a visible Sentence Focus card and places the cursor in the existing chat input without spending a model turn.
The focus card shows the Content and nearest Heading names without placing `H` inside the sentence address.
The next user message is augmented with that location, the full address, sentence, and directly attached apparatus before it reaches the agent.
The focus card's `×` clears sentence focus without closing the Q chat.

### §3 Layout
#### Heading actions
Every visible section and subsection heading shows a quiet generated path chip plus Copy and Chat actions on hover or keyboard focus.
Copy places the human breadcrumb and source path on the clipboard.
Chat opens the existing drawer with that same path visible in the Focus card and does not spend a model turn until the user sends a message.

#### Quiet until needed
The Content division and Heading display small generated `C1` and `H1` chips.
On a pointer device, the compact `C1.P1.S1`, `＋`, and `💬` rail appears when the sentence is hovered or the control receives focus.
`＋` opens the comment form directly under that sentence, while double-click remains reserved for inline editing.
On touch devices, one muted `⋯` opens a menu containing the full address plus Comment, Chat, and Edit.

## Items to Finish
- [ ] Generate paths for every rendered `##` section
- [ ] Generate paths for every rendered `###` subsection
- [ ] Copy page id, breadcrumb, and Markdown source path from a heading
- [ ] Open the existing page Chat with a section/subsection focus packet
- [ ] Recompute heading paths after live Board refresh
- [x] Restrict structural addresses to `## Content`
- [x] Generate `Cn.Pn.S1` automatically for eligible Content sentences
- [x] Generate terminal `Cn.Hn` addresses for `####` headings
- [x] Keep `H` and `P` as siblings; never emit `H.P.S`
- [x] Show Content and Heading names in Sentence Focus without changing its address
- [x] Show a compact sentence address and chat button on hover/focus
- [x] Reuse the existing Q chat session
- [x] Send the address, sentence text, and direct apparatus as the chat focus
- [x] Recompute addresses after live Board refresh
- [x] Add the desktop `Cn.Pn.S1 ＋ 💬` action rail
- [x] Open Comment directly beneath the sentence
- [x] Show a clearable Sentence Focus card without spending a model turn
- [x] Collapse Comment, Chat, and Edit into `⋯` on touch
- [x] Pass fresh-context acceptance for the Content-aware grammar

## Where we are
The existing client indexes Content successfully: each `.csec` receives `Cn`; each `.ph` receives terminal `Cn.Hn`; and each eligible prose line receives sibling `Cn.Pn.S1`.

Fresh-context Chrome acceptance proved that non-Content prose has no address, Heading refs terminate at `Hn`, sentence refs omit `H`, and Chat receives the Content/Heading display path.
Across the 40-page Board, three rewires preserved 106 C refs, 73 H refs, and 978 sentence refs without duplicates or any `H.P.S` address.

Reopened 260730 because the page design now requires coarser focus above Content: every section and subsection heading must expose a copyable breadcrumb and be able to focus the same page Chat.
The sentence implementation remains accepted; heading focus is designed here and not implemented.

## Files
- `haipipe-board/assets/board.js`
  Generates addresses, adds the sentence controls, gathers direct apparatus, and bridges into the existing Q chat.
- `haipipe-board/assets/board.css`
  Provides the quiet hover/focus layout.
- `haipipe-board/SKILL.md`
  States the sentence-chat behavior and the fact that addresses are render-local.

## Law
All location Chat actions reuse the page's existing session. Fine structural addresses remain Content-only: `C` owns sibling terminal `H` nodes and prose `P.S` leaves, so `C1.H1` and `C1.P1.S1` are valid while `C1.H1.P1.S1` is not. Every page section and subsection may also expose a coarser human-readable breadcrumb with its source path. Both forms are generated UI metadata, not durable Markdown identity.

## Log
260730 · Reopened for section/subsection focus: every heading gains a generated breadcrumb plus Copy and Chat actions while the accepted Content sentence grammar remains unchanged
260729 · Fresh Chrome acceptance passed on pointer and touch: 106 C, 73 H, 978 C.P.S refs, deterministic across three rewires; exact focus path and apparatus Send packet verified.
260729 · Replaced page-global `Pn.Sn` with Content-aware `Cn.Hn` and `Cn.Pn.S1`; JL ruled that `H` terminates and never contains `P.S`.
260729 · Fresh browser acceptance passed after rebuilding the Send-handler repair: zero request on focus, exactly one on Send, exact focus packet, clean user bubble, and clear-focus behavior verified.
260729 · Refined the interaction: desktop action rail, inline Comment, clearable Chat focus, deferred model call, and touch overflow menu.
260729 · Fresh-context acceptance passed: 2,463 sentence controls verified, with deterministic rewiring, page-session reuse, complete focus packets, and no regressions.
260729 · Implemented sentence-specific chat: generated `Pn.Sn`, hover/focus controls, existing-Q-session reuse, and a focus packet containing the address, sentence, and direct apparatus.
