# Lifecycle of an inline comment
state: 🟡 PARTIAL
owner: JL
method: pin down the states a comment passes through from written to gone, and who pushes each step
session: b597ef84-d77a-4941-bafa-f1c216030f44
## Question
From the moment an inline comment is written to the moment it disappears from the board, which states does it pass through?
And who pushes each step?

`QA6` built the feature, but "comments pile up forever", "broken quotes that nobody repairs", and "can a board close with open comments": the feature itself answers none of these.
With open comments sitting in `## Comments`, nobody can say whether the board counts as closable, so the close condition is hollow.
It rewrites the closing rule (`close:`), and decides who owns the repair after an anchor is flagged.

## Boundary
- ✅ Covered here
  A comment's **lifecycle**: which states exist, who pushes them, who repairs broken anchors, what open comments mean for closing.
- ↪ Covered elsewhere
  How commenting is **built** (selection, storage syntax, disk write, highlighting): that is `QA6`.

## Diagram
```
  ① draft      in the browser, not yet on disk (localStorage)
       │  Save (written into md automatically)
       ▼
  ② open       in the md's ## Comments, `- [ ]`; header and index carry 💬 N
       │  mark solved (click on the page, or edit the md)   ┌── reopen ──┐
       ▼                                                    │            │
  ③ solved     `- [x]`, entry dims, highlight turns grey ───┘            │
       │                                                                 │
       │  ? keep forever, or move somewhere                              │
       ▼                                                                 │
  ④ archived   ← whether this state even exists is undecided             │
                                                                         │
  ⚠ lost       the original was edited, the quote no longer matches —────┘
               ② and ③ can both fall in; today it is only flagged, repair unbuilt
```

How a comment travels from "HTML in the browser" to "md on disk" to being read by an agent (the write→store→read round-trip):

```
  ① browser board.html         ② serve.py (the machine the files are on)   ③ agent
  ┌ select a line ┐  POST      ┌ writes into QX.md's ## Comments ┐   ┌ reads ## Comments ┐
  │ write comment │ /_board/…  │ one line: - [ ] WHO “quote” ·time│   │ this session: I   │
  │ hit Save      │ ─────────► │                                  │   │  read when told   │
  │               │ ◄───────── │ then build.py → board.html       │   │ drawer/terminal AI:│
  └────┬──────────┘ {ok,wrote} └──────────┬───────────────────────┘   │  primed at start   │
       │                                  │ reload to see highlight    └────────┬──────────┘
       │  ✗ server down →                 │                                     │
       │    falls back to localStorage    └── the md is the single truth; both readers read it ──┘
       │    → never hit disk, agents cannot see it
       └──────────────────────────────────────────────────────────────────────┘

  In one line: a comment "exists" only after ①→② (written into md); agents (③) read only
  the md, never the browser. If an agent cannot see it, it is stuck at ① — not on disk.
```

## Items to Finish
- [x] Every state written down
      draft → open → solved (↔ reopen) → archived, plus ⚠ lost.
      Exactly the ## Diagram above, per state: what it looks like in md, on the page, and who pushes it. ①②③ implemented; ④ archived and lost-repair still empty.
- [ ] Solved comments get a destination
      Stay in `## Comments` forever, move into `## Log` after enough pile up, or get deleted.
      Today they pile up forever.
- [ ] Broken anchors become repairable (one-click re-anchor = the confirmed goal, JL 260723 1518)
      At minimum, jump to that md line; the real bar: when a quote no longer matches, the page offers "the closest sentence in the body" and one click moves the anchor there.
      Not a nice-to-have; this IS the acceptance bar for this step.
- [ ] Closing rules spelled out, two nested levels (JL 260723 1519)
      There are two "closes", nested: · closing one question: a single QX.md's `state:` marked ✅/done.
      Today only Done-when ticks are checked, comments are not. · closing the board: every question in the folder closed.
      Today there is no independent board state; you check question by question.
      Open comments should block BOTH levels: a question carrying `- [ ]` must not be marked ✅, a board holding any `- [ ]` must not count as closed.
      Today neither level checks comments.

## Where we are
Only ①②③ exist, and they emerged while building over these two days; nobody designed this first. ④ archived and the ⚠ lost repair are both still empty.

- The segment that runs today
      select → write → Save auto-writes the md → open on the page → mark solved flips it to solved.
- Who reads a comment, and when (JL asked 260723, the step the lifecycle diagram had missed)
      After the disk write there are two readers, both reading the same place, the md's `## Comments`: ① this CC session: you say "read QA7" and I Read the file, scooping the new comments right then (a snapshot on demand, no automatic sensing); ② the AI attached to this question in the drawer/terminal: primed at start: open comments are injected into its system prompt, no need to brief it.
      So "the agent cannot see it" happens only while a comment is still browser-side in localStorage, not yet on disk.
- They pile up forever
      Solved comments have no exit; `## Comments` only grows.
      This board is two days old and QA6 already holds 3.
- Why anchors kept "getting lost", three layers (JL asked 260723)
      ① Scan range too narrow: highlighting used to skip `## Diagram`, so selecting words inside the figure got wrongly flagged. → Fixed; figures are scanned too. ② Quotes crossing inline tags: a sentence containing `code`/**bold** cannot match tagged HTML as plain text. → Fixed:
         when exact match fails, fall back to "strip tags + normalize whitespace" containment; if present, it does not count as lost.
      ③ The real bulk: many `## Comments` entries quote **things said in chat** (not sentences from the body), so there is nothing on the page to anchor to.
         These are not "lost"; they were **never anchored**.
- "anchor lost" was the wrong thing to shout, renamed
      No history is kept → "you really edited that sentence" and "this sentence was never in the body" cannot be told apart.
      So no more red "⚠ anchor lost"; now a neutral grey "· unanchored" (hover text: the quote is not in the body, maybe chat, maybe a real edit).
      Result: red alarms 45 → 0, replaced by 26 neutral "unanchored".
- Nobody guards open comments (both closing levels leak)
      Closing a question checks only its Done-when ticks; closing a board checks only per-question states; neither level mentions comments.
      A Q can carry 3 open comments and still be marked ✅; a board can hold `- [ ]` and still pass as closed.

## Files
- `serve.py`
  `resolve` (ticking `[x]`) is currently the only state-transition entry point.
- `build.py`
  Open counts, default expansion, and the lost/unanchored verdict all live in the rendering pass.

## Glossary
draft: a comment still in the browser, not yet written into `.md`.
Invisible from any other machine. anchor: how a comment finds its place, by quoting the original sentence.
Edit the sentence, break the anchor.

## Discussion
> JL: after I write a comment, what is its lifecycle? Open a dedicated question. QA6 is mostly done, can it be closed?

## Comments
- [x] JL “closing the board” · 260723 1519
      do you mean board or question?
      >> CC0723: both, and they nest. Rewrote the Done-when line and the Now line in two-level form:
      · closing a question = a single QX.md's `state:` → ✅; · closing a board = every question closed.
      Open comments should block both levels; today neither level looks at comments, so a question carrying 3 `- [ ]` can be marked ✅
      and a board holding `- [ ]` can pass as closed. That is the answer to "which one closes": both levels must guard.
- [x] JL “‘the closest sentence in the body’ with one-click re-anchoring.” · 260723 1518
      yes, this is exactly what I want.
      >> CC0723: noted, promoted from "nice-to-have" to the formal acceptance bar. The Done-when line "broken anchors become repairable" now reads:
      when a quote no longer matches, the page offers the closest sentence in the body and one click moves the anchor; that is the bar for done.
      (Implementation not started; the requirement is pinned first.)
- [x] JL “stay in ## Comments forever, move into ## Log after enough pile up, or get deleted. Today they pile up forever” · 260723 1518
      solved comments could be collapsed.
      >> CC0723: done. Solved comments (`[x]`) fold their body into a one-line `▸ reply`; the surface keeps only the header
      (who · quote · time · solved); click reply to expand. Open ones stay expanded.
      This is v1 of "a destination for solved comments": not deleted, not moved, just tucked in. The move-to-## Log idea is parked.
- [x] JL “when a quote no longer matches the page flags ⚠ anchor lost, but repairing means editing the md yourself.” · 260723 1517
      why anchor is so easier to be lost?
      >> CC0723: your sentences never actually got lost; detection had two bugs, both fixed:
      ① scan range too narrow: highlighting covered Question/Now/Done/Why but skipped `## Diagram`.
      Your “Save (written into md automatically)” lives inside the figure → wrongly flagged. Figures are scanned now; it highlights.
      ② more fundamental: quotes were matched as plain text against **tagged HTML** by exact substring.
      A selected sentence often contains inline markup (`code`→`<code>`, **bold**→`<b>`); once the quote crosses such a tag,
      `e in html` fails: the words are visibly on the page yet reported lost. Your 1517 comment quoted the backticked `⚠ anchor lost` itself, a direct hit.
      Fix: when exact match fails, fall back to "strip tags + normalize whitespace" containment; present = not lost (just not highlighted).
      Result: QA7 went from "⚠ 1 anchor lost" to 0.
      ⚠️ Genuine loss still exists: when you **really edit the original sentence**, the quote truly mismatches; that is the case worth repairing (see the 1518 one-click re-anchor).
- [x] JL “Save (written into md automatically)” · 260723 1511
      the question now is: how do I let the agent read my comments?
      >> CC0723: exactly like this: I am reading this one right now; it is already in this question's ## Comments.
      The chain: Save → serve.py writes into the md's ## Comments → the agent reads that section. Two prerequisites, both required:
      ① the server is running at save time (the disk-write step; otherwise the comment is stuck in browser localStorage);
      ② the agent actually reads the file, nothing is sensed automatically: you say "read it", or the drawer AI is primed at start.
      So "cannot read it" only happens when ① is unmet (not yet on disk). This chain is precisely the "who reads" step the lifecycle diagram had missed.
- [x] JL “① draft, in the browser, not yet on disk (localStorage)” · 260723 1200
      that grant I gave is on my local machine, but this thing is on the server, that can't work, right?
      >> CC0723: you are right, the whole path is dead. Switched to server-side writes: the browser sends one POST,
      serve.py edits the md on this machine and regenerates the html. Verified.

## Log
260724 1242 · Translated to English (JL 260724: everything on the board in English)
260723 · Rewritten to the new structure: Question expanded into "one paragraph + bullets", added `## Boundary` and `## Files`; the retired `## Why here` merged into Question
260723 1735 · Closed two open comments: ① JL 1519 "board or question" → Done-when and Now rewritten in two-level form (close a question = QX state → ✅; close a board = every question closed; open comments should block both levels, today neither checks); ② JL 1518 "one-click re-anchor is exactly what I want" → promoted from nice-to-have to the formal acceptance bar (closest sentence offered, one click moves the anchor)
260723 1520 · Answered JL's "why do anchors keep getting lost": three layers; the scan-range and cross-tag bugs fixed;
              "anchor lost" was a false alarm for most (quotes from chat, never in the body) → renamed to neutral "unanchored", red alarms 45→0
260723 1530 · JL asked "why don't comments stick to the text anymore" + "solved ones should collapse" → two build.py changes: ① highlighting now uses mark_span, spanning <code>/<b> (the naive substring match failed at any tag): QA7 surface highlights 4→6, cross-tag quotes stick again; ② solved comments fold into ▸ reply, header-only on the surface. Closed the 1518 one
260723 1525 · JL asked "does the Q explain the html→disk→agent chain" → only the state machine existed plus scattered "who reads" notes; added the write→store→read round-trip figure to ## Diagram: browser Save → serve.py writes the md's ## Comments → agents read only the md. Spelled out: agent can't see it = stuck before the disk write (still in localStorage)
260723 1520 · JL asked "why are anchors so easy to lose" → found two detection bugs (originals were never lost): ① highlighting skipped ## Diagram; ② quotes crossing inline tags (<code>/<b>) failed exact substring match. Both fixed: figures scanned + fallback to plain-text containment. QA7 went ⚠1 → 0. Closed the 1517 one
260723 1515 · JL asked "how do agents read my comments" → read his 1511 comment on the spot and closed it: after the disk write agents read ## Comments;
              two readers (this session / the drawer AI), prerequisites ① server running at save ② the agent actually reads. Added the "who reads" step to Now
260723 1710 · Ticked during the board-wide review: the state machine is written down (this question's Diagram) → 🟡 PARTIAL; the archived exit + anchor repair still empty
260723 1150 · JL raised "a comment's lifecycle", question opened; "how to repair a broken anchor" moved over from QA6
