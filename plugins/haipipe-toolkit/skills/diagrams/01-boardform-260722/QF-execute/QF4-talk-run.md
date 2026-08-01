# Driving the talk layer: the SDK chat version and the TUI chat version
state: 🔴 OPEN · the SDK chat version has three suites and real numbers; the TUI chat version has none
owner: JL
method: list the talk failures that shipped green through every existing instrument, then name the axes a run has to cover

## Opening
What has to be typed into a chat and answered before a talk change can be called done?
`QF3` added a browser that loads the built page and clicks it, and 260731 showed that a whole class of failure passes even that: the page rendered perfectly, every widget was built, a write landed, and the chat in front of JL was answering for the wrong page.

This face owns the fourth instrument.
It is not a better browser run: it is the same browser sending a real message to a real model and asking who received it, whether the answer came back, and whether the second turn still knows about the first.

## Content
### 1 · Five failures that shipped green through the checker AND the browser run
Every one of these was found by JL using the board, not by any instrument, and every one of them renders correctly.

The drawer stayed attached to the page you came FROM, because the split site navigates through a client-side router that swaps content without touching the hash, and the drawer only listened for `hashchange`.
The transcript vanished at the start of every second turn, because a shipped asset stamp made the tab reload and the reload landed the instant the first turn ended.
Every section the reader had opened re-collapsed for the same reason, and read as the page resetting itself.
A refused turn was rendered as a normal empty answer, because the server replied `HTTP 400` about a stale terminal hold and the drawer displayed `(no text reply, it may have only used tools)` with a `0.0s` timing.
And every turn silently reconnected its session, because the reuse fingerprint included the resumed session id, which necessarily changes after turn one; the only visible symptom was that a turn cost 11.34s instead of 1.17s.

The pattern is one sentence: **`QF3` asks what the page DID with the markup, and every one of these lives in what the CONVERSATION did afterwards.**

### 2 · What a talk run answers that nothing else can
```text
                                  check.py  reader  QF3 browser  talk run
does the markdown parse              ✅        ·         ·           ·
is the prose readable                 ·       ✅         ·           ·
did the CSS apply                     ✗        ✗        ✅           ·
did a click write a file              ✗        ✗        ✅           ·
which session got my message          ✗        ✗         ✗          ✅
did a model actually answer           ✗        ✗         ✗          ✅
does turn two remember turn one       ✗        ✗         ✗          ✅
did a refusal look like an answer     ✗        ✗         ✗          ✅
do both chat versions share a session ✗        ✗         ✗          ✅
```

### 3 · The five axes
**BINDING**
- The drawer is attached to the page the reader is looking at, at all three levels: board, group, page.
- It has to hold across a router navigation, a browser Back, a live refresh, and a full reload, because each of those rebuilds the page by a different path.

**TURN**
- A message reaches a model and an answer comes back, on every page KIND and not just on a Q page.
- A refusal has to be visibly a refusal; this axis exists because `HTTP 400` was rendered as a blank answer for days.

**CONTINUITY**
- Turn two keeps turn one's session, its context, and its transcript.
- The session is REUSED rather than reconnected, which is a timing assertion and not a correctness one, because a reconnecting session still answers correctly.

**HANDOVER**
- The SDK chat version and the TUI chat version share one session per page without fighting over it, which is `QD1`'s Law.
- A dead TUI chat must not leave a hold that refuses the SDK chat forever.

**INTERRUPTION**
- Navigating, reloading, or shipping new assets during a live turn must not lose the turn or the transcript.
- This is the axis that produced two of the five failures in §1.

### 4 · What exists today, and what it measured
Three suites, all Chrome over CDP against the live server, driving the real drawer rather than the endpoint.

```text
① navtest.mjs   27 checks   binding + interruption
                            index → group → page → page, Back, drawer closed,
                            and a real turn that survives navigating away
② rl.mjs         3 checks   interruption: a reload mid-conversation keeps
                            every open section, the drawer, and its page
③ allpages.mjs  61 + 5      binding on every built URL, then one real turn
                            on one page of each kind
```

Two older instruments already sit next to these and are not duplicated here.
`test_hold.py` measures the second-turn latency that exposed the reconnect bug, and `gate_live.py` freezes the live layer's responses so a refactor of `serve.py` can be proven not to change any of them.

### 5 · The trap this run has already fallen into
A talk run has one failure mode the browser run does not, and it cost most of a session on 260731.
The harness reads a state that a MODEL TURN has not reached yet, so a fixed sleep reports a failure that is only slowness.
Worse, the harness can be steered: a sibling session running `open <board url>` navigates any Chrome tab on the machine, and three separate red runs were traced to the tab having been moved out from under the test.

So the run pins its own tab and re-navigates if it drifts, it waits on conditions rather than clocks, and any assertion about a model's answer allows minutes rather than seconds.

## Items to Finish
### Making the run exist as a thing
- [ ] 🧰 Make it one command
      Three `.mjs` files in a scratchpad today, which means they protect only the rounds where someone remembers them; they should be files in the skill that take a board folder and exit non-zero.
- [ ] ⌨ Cover the TUI chat version
      Every assertion listed above drives the SDK chat version; the TUI chat version has none, and HANDOVER is exactly the axis where the two meet.
- [ ] 🎛 Settle which model and tier the run uses
      Cheap tiers make the run affordable and expensive tiers are what JL actually uses; 260731 showed a bug that only appeared at JL's settings.

### Making it run without being remembered
- [ ] 🚦 Wire it into the round
      `QA3`'s gate says reachable; `QF3` claims that word for rendering, and nothing yet claims it for talking.
- [ ] 🧪 Prove it catches a real regression
      Break the router listener on purpose and watch `navtest.mjs` go red, the same way `assets.py`'s `verify()` was proven.

## Where we are
The SDK chat version has three suites and real numbers; the TUI chat version has nothing, and none of it is a command anyone can run without being told.

- 260801 CC · 🔬 Opened from a session that fixed four talk failures and built the suites while doing it
  JL: "I think I want to add something in QF about testing out code for the SDK-Talk and CLI-Talk."
  JL named the two versions the same round: the SDK chat version (`QD2`) and the TUI chat version (`QD3`), which is the vocabulary this face uses throughout.
  Written from the runs rather than from a plan: every failure in §1 is one JL hit in the browser, and every suite in §4 was built to catch it afterwards.
  What justifies a fourth face rather than an item on `QF3` is that the instrument spends a model turn: `QF3` is free and fast and can run on every change, and this one costs money and minutes, so it cannot inherit the same trigger.

### Decision Now
These are the calls only JL can make; CC ticks nothing here.

- [ ] 🎛 Rule which tier the talk run uses
      → CC's proposal: cheap by default for BINDING and INTERRUPTION, which never read the answer's content, and JL's own tier for one TURN per kind.
      The reason is 260731: every suite that session ran used `haiku` and `low` while JL was on `Opus 4.8` and `high`, and that is why the runs stayed green through a bug JL could see.
- [ ] 🚦 Rule whether a red talk run BLOCKS a round or only reports
      → CC's proposal: reports only, matching `check.py`'s default, because a model turn can fail for reasons that are not the board's fault.

## Files
- `../../board/haipipe-board/assets/js/10-drawer/20-chat/`
  The SDK chat version, in six parts; BINDING and CONTINUITY live here.
- `../../board/haipipe-board/assets/js/10-drawer/30-terminal.js`
  The TUI chat version, which no assertion currently touches.
- `../../board/haipipe-board/assets/js/10-drawer/40-follow.js`
  `follow()`, the function whose missing listener was failure one in §1.
- `../../board/haipipe-board/live/chat.py`
  The session host, the hold, and the refusal that was rendered as an answer.
- `../../board/haipipe-board/test_hold.py`
  The second-turn latency probe that exposed the reconnecting session.
- `../../board/haipipe-board/gate_live.py`
  The response-identical gate for the live layer, which this run does not replace.
- `QF3-browser-run.md`
  The third instrument; this face is the fourth and shares its browser but not its trigger.
- `QD2-chat-sdk.md`
  The SDK chat version's own face.
- `QD3-chat-terminal.md`
  The TUI chat version's own face.

## Log
260801 · Opened on JL's ask for a QF face covering the SDK chat version and the TUI chat version, written from the five talk failures found in the browser on 260731 and the three suites built to catch them
