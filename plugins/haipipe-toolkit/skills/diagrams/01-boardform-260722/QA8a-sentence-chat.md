# A sentence attachment, and whether any agent sees it

state: 🟡 PARTIAL
owner: JL
method: read what prime_context and CHAT_RULES actually hand the agent, then rule what they should

## Question
When someone attaches something to a sentence on the page, a `> Check:` lane or a comment, does the agent that will act on that sentence see it?
Measured rather than assumed, the answer is yes if it reads the file, since a lane is an ordinary line in the markdown.
Everything turns on that "if": the agent is handed a count and a pointer, never the text, a plain session in the workspace gets nothing at all, and neither is told when something arrives mid-session.

The page has become a place where things get attached: a comment pinned to a selection, a typed `>` lane folded under a sentence, and now an excalidraw dropped into a Diagram.
Every one of those writes into the page's markdown, which is the whole point of the design, and an agent working on that page opens the same markdown, so the obvious assumption is that whatever you attach, whoever works on it is looking at it.
There are two kinds of agent, not one, and the drawer is the better-served of them (JL 260726): a plain Claude Code session working in the workspace gets no orientation at all.
That assumption is close to true and not exactly true, and the gap is the kind that stays invisible: the agent is handed a count and an instruction to read the file, so it usually does read, and it usually does see, and nothing tells you which time it did not.
Worse, nothing in what the agent is told explains that a `>` line under a sentence is an attachment addressed to it, so an agent that reads the file perfectly can still treat a lane as ordinary quoted text.
Leave it unruled and the attachment layer is a message people believe they are sending, with no rule about whether it arrives.

## Boundary
- ✅ Covered here
  What any agent that could act on a page is actually handed, and what it should be handed: the count, the file, the apparatus, or nothing.
  Both channels: the in-page drawer and terminal, which get `prime_context`, and a plain Claude Code session opened on the workspace, which gets nothing.
  Whether a session already running is told that something new arrived.
- ↪ Covered elsewhere
  How a lane is attached to a sentence and what the lanes are: that is `QA8`.
  How a comment is written and what its states are: that is `QA6`.
  One session per question, the drawer, and the terminal: `QD1`, `QD2`, `QD3`.
  What a marker MEANS in a paper (a citation, a value, a display): that is the paper board's `QC` group.

## Diagram

```
  WHO COULD ACT ON A PAGE, AND WHAT EACH IS HANDED
  ──────────────────────────────────────────────────────────────────────────
  ① the in-page drawer / terminal            (serve.py prime_context)
     ✓ board title and folder
     ✓ page id and title
     ✓ the page's path, relative to cwd (= the repo root)
     ✓ first 280 chars of ## Question
     ✓ N unresolved comments · N unticked items, counted separately
     ✓ what a `>` lane is and that it is addressed to this turn   (CHAT_RULES)
     ✗ the comments themselves
     ✗ the sentence lanes themselves
     → "Read that file for the full picture."

  ② a plain Claude Code session on the workspace
     ✗ everything above. No orientation, no count, no instruction.
     It sees an attachment only when a human says "read QA8a", or when it opens
     the file for some unrelated reason and happens to look.

  SO THE PATH IS:      attach ──► md ──► agent READS md ──► sees it
                                          ▲
                                   ① instructed, not guaranteed
                                   ② not even instructed
                                   neither is repeated when something
                                   arrives mid-session
```

http://127.0.0.1:5599/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/fig/board.excalidraw&frame=QA8a

## Content
### §1 What is actually handed over
#### P1. The orientation is a pointer, not the content
(what `prime_context` builds, read from the code on 260726)
`prime_context` assembles the board title and folder, the page id and title, the page's path relative to the repo root, the first 280 characters of `## Question`, and one line naming a count.
Then it says: "Read that file for the full picture."
The file's body is never inlined, which is a reasonable design and cheap, and it means every attachment reaches the agent only through an act of reading that the agent chooses to perform.
The drawer and the terminal share this function, so they share the gap.

#### P1b. The other channel gets nothing at all
(a plain Claude Code session in the workspace, which is the one most used)
`prime_context` runs for the drawer and the terminal. A Claude Code session started in the repo the ordinary way never touches it.
It has no board orientation, no counts, no instruction to read the page, and nothing in `CLAUDE.md` tells it that a `>` line under a sentence is addressed to it.
The mechanism to change that exists and is used for something else: `~/.claude/settings.json` already defines a `SessionStart` hook, which plays a sound.
This is the channel doing most of the work, so it is odd that it is the one told least, and it is the reason this page is about any agent rather than about the drawer.

#### P2. The count is mislabelled
(a small bug, and it points at the bigger question)
The line reads "It has N unresolved comment(s) in its `## Comments`", but N counts every `- [ ]` in the file.
On a normal page most unchecked boxes are Items to Finish, so the agent is routinely told there are eleven unresolved comments on a page that has none.
Either the count should be scoped to the Comments section, or the sentence should say what it is really counting, which is open work.

#### P3. The rules never mention the apparatus
(`CHAT_RULES` describes a page that no longer exists)
The rules block lists the page's sections as `## Question / ## Diagram / ## Done when / ## Now / ## Why here / ## Lesson / ## Glossary / ## Discussion / ## Comments / ## Log`.
Two of those names were renamed long ago to `## Items to Finish` and `## Where we are`, and `## Why here` was retired outright.
It explains the `- [ ] WHO 「quote」` comment row and how to reply to one, and it says nothing at all about `>` lanes under a sentence.
So an agent can read the file, see `> Check: this number is stale`, and have no reason to treat it as a request rather than as prose someone quoted.

### §2 What the markdown actually gains
#### P4. Every write on the page is one line an author could have typed
(measured 260726 by firing all four endpoints at a throwaway page and diffing the file)
This is the property the whole design rests on, and it is checkable rather than promised.
Attaching a `Check` lane to a sentence adds exactly one line, directly under that sentence, bound to it by adjacency and by nothing else:

```
  ## Content
  ### 1 · Body
  The coefficient is 0.42 in the pooled model.
+ > Check: 0.42 is from the robust-SE run, not the clustered one
  This second sentence has nothing attached to it.
```

Commenting on the same sentence writes somewhere else entirely, appending a block to `## Comments` and creating that section when the page has none:

```
+ ## Comments
+ - [ ] JL “The coefficient is 0.42 in the pooled model.” · 260726 1400
+       is this the clustered spec?
```

Marking it solved is a one-character edit in place, `- [ ]` to `- [x]`, and attaching an excalidraw inserts `## Diagram` before `## Content`, which is where the fixed on-stage order puts it.
Four different writes, four different destinations, and every one of them is ordinary markdown: no marker, no id, no sidecar file, nothing that only the button knows how to produce.
`build.py` never writes to the `.md` at all, which the same test confirmed by rebuilding and diffing: the file was byte-identical.

#### P5. So the answer to "will the chat see it" is structural
(the agent reads a file, not a feed)
Because a lane is just a line in the file, an agent that reads the page after the write sees it, with no protocol between them and nothing to keep in sync.
That is the strength of the design and also exactly why the gap in §1 is easy to miss: the content is genuinely there, and only the notification is missing.
A lane attached while a drawer is open changes the file on disk and changes nothing about what that session has already been told.

### §3 What the ruling has to decide
#### P6. Push or pull
(inlining costs tokens on every turn; pulling costs a read that might not happen)
Handing the agent the open comments and the sentence lanes at start makes the attachment layer a real channel, at the price of paying for that text on every session open.
Leaving it as a pointer keeps the cost at zero and keeps the guarantee at zero too.
A middle option exists and is probably the answer: name what is attached without quoting it, so the agent is told there are three lanes and two open comments and where to look, which is enough to make reading non-optional.

#### P6b. Whether the plain session should be oriented at all
(a hook would work; whether it should is a different question)
A `SessionStart` hook could print the same orientation the drawer gets, or a line naming the pages that carry unresolved attachments.
Against that: a hook fires on every session in the repo, most of which have nothing to do with a board, and a board-shaped preamble on unrelated work is noise that trains people to skip preambles.
The alternatives are a sentence in `CLAUDE.md`, a line in the `/haipipe-board` skill so it only applies once the skill is invoked, or ruling that a plain session is the human's job to brief.

#### P7. Mid-session arrival
(the drawer stays open while you keep attaching things)
Orientation is built once, when the session starts.
Attach a lane afterwards and the running agent is not told; the text is on disk, so a re-read finds it, but nothing prompts that re-read.
The live-refresh already watches the file's timestamp for the page's benefit, so the signal exists and is simply not routed to the agent.

## Items to Finish
- [ ] 🧠 JL rules what the chat is handed at start
      Push the attached text, name it without quoting it, or leave the pointer as it is.
      This is the ruling; the rest of the list follows from it.
- [x] 🔢 The count says what it counts
      Today N was every `- [ ]` in the file and the sentence called them comments.
      Fixed 260726: `prime_context` counts the `## Comments` boxes and the rest separately and names each, so a page with one comment and one open item now reports one of each instead of "2 unresolved comments".
      The cost of the old line was measured rather than assumed: a cold agent noticed the discrepancy, could not resolve it, and invented an explanation for it, which is worse than saying nothing.
- [x] 📖 CHAT_RULES describes the page as it is now
      It listed `## Done when`, `## Now` and `## Why here`, two renamed and one retired, and never mentioned `>` lanes at all.
      Fixed 260726: the section list matches the current form with the old names named as accepted aliases, and a short block explains that a lane is bound to the sentence above it by adjacency, is typed by its first word, and is addressed to whoever works on that sentence.
      This does not decide what the agent is HANDED, which is the ruling below; it only stops the rules describing a page that no longer exists.
- [ ] 🧭 The plain workspace session is either oriented or ruled out of scope
      `prime_context` serves the drawer and the terminal only; an ordinary Claude Code session in this repo gets nothing, and it is the channel doing most of the work.
      The options are a `SessionStart` hook, a line in `CLAUDE.md`, a line in the `/haipipe-board` skill so it applies only once invoked, or a ruling that briefing a plain session is the human's job.
      This closes either way: something orients it, or the page says plainly that nothing does and why.
- [ ] 🔔 A running session learns that something arrived
      The drawer polls the file's timestamp already for the page; nothing tells the agent.
      Closes when a mid-session attachment reaches an open session, or a ruling says it should not.
- [x] 🧪 A cold agent is asked what it sees
      Run 260726 on a throwaway page carrying two lanes, one open comment, one open item, and a second sentence with nothing attached as a control.
      Both before and after the two fixes above, the agent found everything: it read the file, named the `Check` and `JL` lanes, scoped them to the correct sentence, and noticed that the control sentence was bare.
      So the current pointer IS sufficient for a fresh session that is asked directly, which is the honest answer to the question this page opened with, and it narrows what is left to the mid-session case below.

## Where we are
Nothing is ruled, and three of the five items are now closed by measurement rather than by argument.
The agent still gets a pointer, a count and an instruction and never the attached text, which is `P6`'s open ruling. What changed is that the count is now correct, the rules describe the page that exists, and "usually reads, usually sees" has been replaced by a result: asked directly, a cold session found every attachment, both before and after the fixes.
What remains unmeasured is the mid-session case, where nothing tells an open drawer that something arrived, and the plain workspace session, which is not told anything at any point.

- 260726 JL · 🧭 It was never only the drawer
  JL: "This is not limited to the draw chat, also any claude code session for the workspace dir."
  Correct, and the second channel is the worse-served one: `prime_context` runs for the drawer and the terminal, and a plain Claude Code session started in this repo gets no orientation, no counts and no instruction to read the page.
  Checked rather than assumed: `CLAUDE.md` says nothing about board attachments, and the `SessionStart` hook that exists in `~/.claude/settings.json` plays a sound.
  This session is an instance of it. Every attachment JL made today arrived because JL typed it in chat; a `> JL:` lane written on the page would have reached me only if I were told to read that page.
  The page is now about any agent that could act on a sentence, its title and Boundary say so, and the ruling below has two channels to answer for rather than one.

- 260726 CC · 🧪 The measurement, and what the agent actually said
  A throwaway page carried `> Check:` and `> JL:` under one sentence, an open comment quoting that sentence, an open item, and a bare second sentence as a control. One scoped turn, the same question both times: what is attached to this page, and what does any of it want from you.
  Before the fixes it found everything and then stumbled on the count, verbatim: "(The orientation note mentioned "2 unresolved comments," but the file itself carries one `- [ ]` comment plus the inline Check/JL note — two distinct pieces of feedback, both pointing at the same sentence.)"
  That guess is wrong. The second box was the open ITEM, not the inline note. A number that does not match the file does not merely mislead, it makes the agent construct a reason for the mismatch and proceed on it.
  After the fixes it bucketed them correctly, verbatim: "Two lanes, both stuck to one sentence ... One comment, pinned to the same sentence ... One unticked item", and it used the grammar the rules now teach: "Both are bound by adjacency to that sentence, and on this turn they're addressed to me/you."
  It also identified the control unprompted: "The next sentence (line 14) explicitly has nothing attached — that's the control in this visibility test."
  Cost fell from $0.22 to $0.055 across the two runs. Some of that is prompt caching on a repeated question, so the fix cannot claim all of it; the part that is certainly real is that the second run spent no effort reconciling a number against the file.

- 260726 JL · ❓ Opened from QA8, after the ➕ excalidraw landed
  JL asked whether a thing attached on the page is seen by the chat as well.
  The answer turned out to be "yes, if it reads, and nothing tells it that lanes exist", which is enough of a gap to be its own question.
  `QA6` had claimed for three days that open comments were injected into the drawer's system prompt; they are not, and that line is now corrected there.

## Files
- `serve.py`
  `prime_context` builds the orientation; `CHAT_RULES` is the rules block above it. Both are what this question rules on.
- `haipipe-board/assets/board.js`
  The live-refresh poller already watches the file's timestamp, which is the signal P5 would reuse.

## Glossary
orientation: the text `prime_context` prepends to a chat or terminal session so it knows which board and page it is attached to.
apparatus: the typed `>` lanes folded under a sentence (`QA8`), as distinct from a comment pinned to a selection (`QA6`).
push / pull: whether the agent is handed the attached text at start, or must read the file to find it.

## Discussion
> JL: I want to have another new one from QA8, is the QA8-comments, after adding the QA8-comment, will the chat see that content as well?
>> CC0726: opened as QA8a: a sub-question of QA8, sorted right after it, and named for the sentence because that is what it is about. The short answer is in §1: it sees the file, so it sees the lane once it reads, but it is handed a count rather than the text and is never told that lanes exist.

## Log
260726 · opening lead widened to three lines (JL: the openings are too short; say the question, how it is answered, and what turns on it)
260726 · widened from the drawer to any agent (JL: "not limited to the draw chat, also any claude code session for the workspace dir"): second channel added to the Diagram, `P1b` and `P6b` written, one new item; the plain session gets no orientation at all, which is worse than the case this page opened on
260726 · worked (JL: "please work on QA8a"): 🔢 and 📖 fixed in `serve.py`, 🧪 measured with one scoped turn before and after; the ruling `P6` and the mid-session signal `P7` deliberately untouched, since both are JL's and implementing either would settle the ruling by hand
260726 · renamed QA11 -> QA8a and retitled for the sentence (JL: "if it is sentence related, call it QA8a"); `§2` added with the four write destinations measured from a throwaway page rather than described
260726 · opened from JL's question on QA8; `prime_context` and `CHAT_RULES` read and recorded, three concrete gaps written down (mislabelled count, retired section names in the rules, no mid-session signal), nothing ruled
