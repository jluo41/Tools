# Chat about one location: the address a machine is handed

state: 🟡 PARTIAL · both halves built and every Aim closed; the state line is JL's to move
owner: JL
method: generate render-local paths for page headings plus fine Content addresses, then reuse one page Chat session for either focus

## Opening
How do you point an agent at one part of a page without opening a new conversation for it?
A location is anything a reader can see: a section, a heading, or one sentence.
Each gets an address the browser works out at render time, such as `QB8.C1.P1.S1`.
The page's existing chat takes that address as its focus, so nothing new is opened.
The address is not durable on purpose, which is the trade this page makes.

**Why it is not durable**: it says where something appears in THIS render, so insert a paragraph and it changes.

**Where the trade bites**: a durable id would survive an edit, and would then have to be written into the markdown and kept in step by hand.
A render address costs nothing to maintain and is wrong the moment you save it, so it may focus a chat and may never key a record.
`QB8e` is where that limit lands: it needs to archive and restore an attached record, and it cannot use one of these.

**Covered elsewhere**: `QB8` owns the sentence itself and everything written onto it, which is the card on its words, the typed lanes, a person's remark, and the change record left by an edit. One session per page is `QD1`.


## Diagram

```
QD8 Content
  C1 · Addressing
    H1 · Generated, not stored        → QD8.C1.H1
    first prose sentence              → QD8.C1.P1.S1
    second prose sentence             → QD8.C1.P2.S1

sentence action rail
  The Board already has one chat session per page.  C2.P1.S1 ＋ 💬
                                                              │
                                                              ▼
existing QD8 chat session
  FOCUS  QD8.C2.P1.S1                               ×
  C2 · Chat behavior
  H1 · One page session
  The Board already has one chat session per page.
  Attached · 2                                       ▸

  Ask about this sentence…                            Send

heading focus
  📍 States
     Decision Now            QD8 / States / Decision Now  ⧉ 🤖
                                                                       │
                                                                       ▼
  existing QD8 chat session
  FOCUS  section/subsection path · source file · visible heading/body
```

## Content
### §1 Addressing
**Two address families, one page**: what each names, and how deep it goes.

```
🧭 THE BREADCRUMB · every ## section and ### subsection
   QB8 / States / Decision Now · QB-delivery/QB8-overview.md
   spoken, pasted, copied · human-readable all the way down

🎯 THE FINE ADDRESS · inside ## Content only
   C1        a ### division
   C1.H1     a #### heading · TERMINAL, nothing hangs below it
   C1.P1.S1  a prose sentence · P is H's SIBLING, never its child
   C1.H1.P1.S1  never legal

🔄 both are GENERATED at every render and stored nowhere
```
📌 Establishes what an address IS before the page says what it is for.

#### Section and subsection paths
Every rendered `##` section and `###` subsection receives a generated human-readable breadcrumb, for example `QB8 / States / Decision Now`.
Copy includes the page id, breadcrumb, and Markdown source path so Claude Code can locate it without guessing.
The breadcrumb is render-local UI metadata, just like the existing Content addresses; renaming or moving a heading recomputes it and never rewrites the source merely to preserve an obsolete index.

#### Generated, not stored
The browser assigns addresses after each Board render and again after a live refresh.
Nothing is added to the Markdown, so renumbering never produces source-file churn.
The full sentence address is page id plus Content, Paragraph, and Sentence, for example `QD8.C2.P1.S1`.

#### C, H, P, and S
`C` counts `###` divisions only inside `## Content`.
`H` counts `####` headings inside its `C` and terminates there, for example `QD8.C1.H1`.
`P` is a sibling of `H`, not its child; prose therefore uses `QD8.C1.P1.S1`, never `QD8.C1.H1.P1.S1`.
Board writing keeps one source sentence per line, so each current paragraph ends in an S-one leaf; the explicit sentence level leaves room for a future paragraph containing more than one sentence.

### §2 Chat behavior
**One session, two kinds of focus**: what a click sends, and what it does not.

```
🖱 click 💬 on a sentence  →  the page's EXISTING chat session
🖱 click 🤖 on a heading   →  the same session, coarser focus

   FOCUS CARD  address · display name · the text · its apparatus   ×
   🚫 no model turn is spent on the click itself
   📤 the packet reaches the agent with the NEXT message
   ✂️ × or Esc clears the focus and leaves the chat open
```
📌 Establishes that focusing is free, which is the whole reason it can be a click.

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
**Quiet until wanted**: where each control lives, and what reveals it.

```
🖱 pointer   hover a heading  → breadcrumb chip · ⧉ text · 🤖 chat
             hover a sentence → C1.P1.S1 · ＋ · 💬
📱 touch     no hover exists, so ONE ⋯ expands to all of it
🎨 chips     at the END of the heading, never the front:
             a leading C1 before "1 · Content" read as "C11 · Content"
📐 collapse  to zero WIDTH, not opacity, or a breadcrumb reflows
             the heading it decorates while invisible
```
📌 Establishes why none of this sits on the prose permanently.

#### Heading actions
Every visible section and subsection heading shows a quiet generated path chip plus Copy and Chat actions on hover or keyboard focus.
Copy places the human breadcrumb and source path on the clipboard.
Chat opens the existing drawer with that same path visible in the Focus card and does not spend a model turn until the user sends a message.

#### Quiet until needed
The Content division and Heading display small generated `C1` and `H1` chips.
On a pointer device, the compact `C1.P1.S1`, `＋`, and `💬` page list appears when the sentence is hovered or the control receives focus.
`＋` opens the comment form directly under that sentence, while double-click remains reserved for inline editing.
On touch devices, one muted `⋯` opens a menu containing the full address plus Comment, Chat, and Edit.

## Aims
### The section and subsection breadcrumb half
- [x] Generate paths for every rendered `##` section
      `QB8 / States`, built from the heading's own label with its emoji, its `1/7` count, and its `· 6 sections` suffix stripped, because an address is spoken and pasted.
- [x] Generate paths for every rendered `###` subsection
      `QB8 / States / Decision Now`, for a `div.sh` outside Content and for a `details.csec` division inside it.
- [x] Copy page id, breadcrumb, and Markdown source path from a heading
      Clicking the chip copies `QB8 / States / Decision Now · QB-delivery/QB8-overview.md`; a subsection also gains its own `⧉`, which copies that subsection's text the way `##` headings already do.
- [x] Open the existing page Chat with a section/subsection focus packet
      `🤖` calls `window.__boardHeadingChat`, which reuses this page's session and fills the same Focus card with the breadcrumb and the source path.
- [x] Recompute heading paths after live Board refresh
      `wireHeadingPaths` runs inside `__boardWireSentenceChats`, the hook the rewire already calls, so a live swap regenerates both address families together.

### The Content address grammar
- [x] Restrict structural addresses to `## Content`
- [x] Generate `Cn.Pn.S1` automatically for eligible Content sentences
- [x] Generate terminal `Cn.Hn` addresses for `####` headings
- [x] Keep `H` and `P` as siblings; never emit `H.P.S`
- [x] Recompute addresses after live Board refresh
- [x] Pass fresh-context acceptance for the Content-aware grammar

### The human gate
- [ ] 🧠 JL accepts this face and moves its state line
      **Done when:** JL has read the built page and either flips it to ✅ SETTLED or names what is missing. Every other Aim here is ticked and both halves are live; only the state line is a person's to move.

### The sentence rail and chat focus
- [x] Show Content and Heading names in Sentence Focus without changing its address
- [x] Show a compact sentence address and chat button on hover/focus
- [x] Reuse the existing Q chat session
- [x] Send the address, sentence text, and direct apparatus as the chat focus
- [x] Add the desktop `Cn.Pn.S1 ＋ 💬` action page list
- [x] Open Comment directly beneath the sentence
- [x] Show a clearable Sentence Focus card without spending a model turn
- [x] Collapse Comment, Chat, and Edit into `⋯` on touch

## States
The existing client indexes Content successfully: each `.csec` receives `Cn`; each `.ph` receives terminal `Cn.Hn`; and each eligible prose line receives sibling `Cn.Pn.S1`.

Fresh-context Chrome acceptance proved that non-Content prose has no address, Heading refs terminate at `Hn`, sentence refs omit `H`, and Chat receives the Content/Heading display path.
Across the 40-page Board, three rewires preserved 106 C refs, 73 H refs, and 978 sentence refs without duplicates or any `H.P.S` address.

Reopened 260730 because the page design now requires coarser focus above Content: every section and subsection heading must expose a copyable breadcrumb and be able to focus the same page Chat.
Heading focus was designed here on 260730 and built on 260731, so every item on this face is now ticked.

- 260731 CC · 🧭 Heading focus is built, and it reuses every contract the sentence rail already had
  Every rendered `##` section and `###` subsection heading now carries a page list at its END, invisible until that heading is hovered: the generated breadcrumb, `⧉` for a subsection's text, and `🤖` for chat.
  `QB8` yields 17 of them, from `QB8 / Opening` down to `QB8 / States / Decision Now`.
  Two decisions inside it are worth stating because they were not obvious.
  The page list collapses to zero WIDTH rather than to `opacity:0`, which the `C1` chips use, because a breadcrumb is long enough to reflow the heading it decorates if it keeps its box while invisible.
  And `⧉` on a `##` heading keeps copying the section's TEXT, JL's 260725 ruling, so copying the ADDRESS moved onto the chip itself; the two copies are next to each other and say which is which on hover.
  Driven in Chrome rather than read: the chip put `QB8 / States / Decision Now · QB-delivery/QB8-where-we-are.md` on the clipboard, `⧉` put that subsection's text there, and `🤖` opened this page's own session with the Focus card showing the breadcrumb and the source path.

### The human gate
- 🧠 JL accepts this face and moves its state line. All 19 build items are ticked and both halves run; this is the only thing left.

### Decision Now
- [ ] 🧠 Flip this face to ✅ SETTLED
      All 19 items are ticked and both halves are live, but the state line is JL's to move, so it still reads 🟡 PARTIAL.
- [ ] 🧭 Rule the two ⧉ buttons
      A `##` heading copies its section's text with `⧉` while its chip copies the address; a `###` heading now has both too.
      A · keep both, as built: text and address are genuinely different things to want, and each says which it is on hover.
      B · make `⧉` copy the address everywhere and drop text copying, which is what this face's `#### Heading actions` paragraph literally says today.
      → CC recommends A, because the 260725 text copy is the one people actually use to paste a section into a chat, and B would delete it to satisfy a sentence written before it existed.

- 260731 JL · 👁 The `Cn`/`Hn` chips left the front of the heading
  A leading chip fused with authored numbering: `C1` before `1 · Content: establish the substance` read as "C11 · Content".
  JL: "make the C1 to be the end of the sentence, and only shown when we hover it, just like the sentence".
  Shipped the same round (haipipe-board 0.58.0): `board.js` appends `.caddr`/`.haddr` at the end of the summary or heading, and `board.css` holds them at opacity 0 until the heading is hovered, the sentence rail's contract.
  On touch there is no hover, so chips stay hidden there exactly as the sentence chip does.

## Files
- `haipipe-board/assets/js/40-sentence/10-address.js`
  Generates the render-local Content addresses, adds the sentence controls, gathers direct apparatus, and bridges into the existing page chat.
- `haipipe-board/assets/js/40-sentence/20-breadcrumb.js`
  Generates the section and subsection breadcrumbs and holds `wireHeadingPaths`, `__boardWireSentenceChats`, and `__boardHeadingChat`.
- `haipipe-board/assets/css/`
  Provides the quiet hover/focus layout.
- `haipipe-sentence/SKILL.md`
  Holds the sentence contract these addresses serve, the dotted address and the per-location chat focus; `haipipe-board/SKILL.md` routes one-sentence work to it.

## Law
All location Chat actions reuse the page's existing session. Fine structural addresses remain Content-only: `C` owns sibling terminal `H` nodes and prose `P.S` leaves, so `C1.H1` and `C1.P1.S1` are valid while `C1.H1.P1.S1` is not. Every page section and subsection may also expose a coarser human-readable breadcrumb with its source path. Both forms are generated UI metadata, not durable Markdown identity.

## Log
- 260806 2142 · [REVISE-CC] swept to the 260806 architecture; Files now names the real split `10-address.js` / `20-breadcrumb.js` and the sentence contract's home `haipipe-sentence/SKILL.md`, and the dead `QB8-where-we-are.md` path plus the nonexistent `Current decision` breadcrumb were corrected
260802 · 🔎 Brought to the current page contract after a fresh cold read. The Opening's blank line sat after the question, so the whole rationale rendered behind a click and the page opened as one bare sentence; the four sentences under it were also the named form-letter scaffold ("This page …", "The hard part is …", "The design succeeds when …"), so they were rewritten in this page's own order around the trade it actually makes, which is that a render address may focus a chat and may never key a record. Thirteen occurrences of `QAb3` still taught the page by an id two renames old, twelve worked examples cited `QB4e`, which is archived, and nine breadcrumbs showed the retired section name `Where we are` while this page's own new §1 figure already showed `States`. All of it now reads `QD8`, `QB8` and `States`
260802 · Moved out of the sentence family to `QD8` when `QB8`'s five faces folded. A generated address is not an attachment: nothing is written under the sentence and nothing enters the file at all, because addresses are made at render time and stored nowhere. Its readers are the chat drawer and the routing verb, both in this lane, so it sits beside `QD1`'s one session per page. The old ids `QB8d` and `QD8` still resolve through `board.md`'s Links table
260731 2015 · Heading focus BUILT: every `##` and `###` heading gains a hover-revealed page list (breadcrumb chip that copies address + source path, `⧉` for a subsection's text, `🤖` for page chat); `__boardHeadingChat` + a `kind` on the focus packet; recomputed by the existing rewire hook. All 5 remaining items ticked; the state line waits on JL
260731 · Items, States, and Files regrouped to the QB4d/QB8/QB4f subsection conventions (matrix retrofit)
260731 · Address chips moved to the END of their heading and became hover-reveal, on JL's "C11" read; shipped in board.js/board.css, haipipe-board 0.58.0
260730 · Reopened for section/subsection focus: every heading gains a generated breadcrumb plus Copy and Chat actions while the accepted Content sentence grammar remains unchanged
260729 · Fresh Chrome acceptance passed on pointer and touch: 106 C, 73 H, 978 C.P.S refs, deterministic across three rewires; exact focus path and apparatus Send packet verified.
260729 · Replaced page-global `Pn.Sn` with Content-aware `Cn.Hn` and `Cn.Pn.S1`; JL ruled that `H` terminates and never contains `P.S`.
260729 · Fresh browser acceptance passed after rebuilding the Send-handler repair: zero request on focus, exactly one on Send, exact focus packet, clean user bubble, and clear-focus behavior verified.
260729 · Refined the interaction: desktop action page list, inline Comment, clearable Chat focus, deferred model call, and touch overflow menu.
260729 · Fresh-context acceptance passed: 2,463 sentence controls verified, with deterministic rewiring, page-session reuse, complete focus packets, and no regressions.
260729 · Implemented sentence-specific chat: generated `Pn.Sn`, hover/focus controls, existing-Q-session reuse, and a focus packet containing the address, sentence, and direct apparatus.
