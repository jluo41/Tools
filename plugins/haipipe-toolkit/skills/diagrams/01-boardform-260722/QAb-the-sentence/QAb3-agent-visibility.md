# Chat about one sentence

state: ✅ SETTLED · Content-aware addresses implemented and independently accepted
owner: JL
method: address Content divisions, headings, paragraphs, and sentences without nesting prose beneath headings

## Question
How can someone call the chat about one specific sentence without creating a separate session for every sentence?

The Board already has one chat session per page. A sentence therefore needs a focus address and an entry button, not another session.
Only `## Content` receives structural addresses: `C` is a Content division, `H` is a terminal Heading node, and prose uses sibling `P.S` leaves.

## Boundary
- ✅ Covered here
  Automatic sentence addresses, the hover chat button, and the context handed to the existing page chat.
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
```

## Content
### §1 Addressing
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
#### One page session
Clicking a sentence's `💬` opens the existing chat for that Q.
It does not create a sentence session, a new session id, or a second conversation history.

#### Explicit focus packet
Clicking `💬` establishes a visible Sentence Focus card and places the cursor in the existing chat input without spending a model turn.
The focus card shows the Content and nearest Heading names without placing `H` inside the sentence address.
The next user message is augmented with that location, the full address, sentence, and directly attached apparatus before it reaches the agent.
The focus card's `×` clears sentence focus without closing the Q chat.

### §3 Layout
#### Quiet until needed
The Content division and Heading display small generated `C1` and `H1` chips.
On a pointer device, the compact `C1.P1.S1`, `＋`, and `💬` rail appears when the sentence is hovered or the control receives focus.
`＋` opens the comment form directly under that sentence, while double-click remains reserved for inline editing.
On touch devices, one muted `⋯` opens a menu containing the full address plus Comment, Chat, and Edit.

## Items to Finish
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
The client now indexes only Content. Each `.csec` receives `Cn`; each `.ph` receives terminal `Cn.Hn`; and each eligible prose line receives sibling `Cn.Pn.S1`.

Fresh-context Chrome acceptance proved that non-Content prose has no address, Heading refs terminate at `Hn`, sentence refs omit `H`, and Chat receives the Content/Heading display path.
Across the 40-page Board, three rewires preserved 106 C refs, 73 H refs, and 978 sentence refs without duplicates or any `H.P.S` address.

## Files
- `haipipe-board/assets/board.js`
  Generates addresses, adds the sentence controls, gathers direct apparatus, and bridges into the existing Q chat.
- `haipipe-board/assets/board.css`
  Provides the quiet hover/focus layout.
- `haipipe-board/SKILL.md`
  States the sentence-chat behavior and the fact that addresses are render-local.

## Law
Sentence chat reuses the page's existing session. Structural addresses exist only inside Content. `C` owns sibling terminal `H` nodes and prose `P.S` leaves: `C1.H1` and `C1.P1.S1` are valid; `C1.H1.P1.S1` is not. Addresses are generated UI metadata, not durable Markdown identity.

## Log
260729 · Fresh Chrome acceptance passed on pointer and touch: 106 C, 73 H, 978 C.P.S refs, deterministic across three rewires; exact focus path and apparatus Send packet verified.
260729 · Replaced page-global `Pn.Sn` with Content-aware `Cn.Hn` and `Cn.Pn.S1`; JL ruled that `H` terminates and never contains `P.S`.
260729 · Fresh browser acceptance passed after rebuilding the Send-handler repair: zero request on focus, exactly one on Send, exact focus packet, clean user bubble, and clear-focus behavior verified.
260729 · Refined the interaction: desktop action rail, inline Comment, clearable Chat focus, deferred model call, and touch overflow menu.
260729 · Fresh-context acceptance passed: 2,463 sentence controls verified, with deterministic rewiring, page-session reuse, complete focus packets, and no regressions.
260729 · Implemented sentence-specific chat: generated `Pn.Sn`, hover/focus controls, existing-Q-session reuse, and a focus packet containing the address, sentence, and direct apparatus.
