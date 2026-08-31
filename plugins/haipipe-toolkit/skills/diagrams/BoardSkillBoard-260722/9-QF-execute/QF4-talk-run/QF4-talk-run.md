# Driving the talk layer: the SDK chat version and the TUI chat version
state: 🟡 PARTIAL · both chat versions have suites in `checks/` · open: 2 tiers unwired, no dispatcher
owner: JL
method: list the talk failures that shipped green through every existing instrument, then name the axes a run has to cover

## Opening
What must a real conversation prove before changes to the SDK chat or TUI chat can be called safe?

A page can render perfectly while sending a message to the wrong scope, losing the next turn, or hiding a refusal as an answer.
Only a live message can test the session and handover behavior that appears after the interface works.
The run must cover binding, turn completion, continuity, interruption, and movement between the two chat forms.
It succeeds when the right session receives the message and remains truthful through the next action.

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
**The instrument gap**: what only a live chat turn can witness.
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
- The SDK chat version and the TUI chat version share one current session and one live window per scope without fighting over it, which is `QD1`'s Law.
- A dead TUI chat must not leave a hold that refuses the SDK chat forever.

**INTERRUPTION**
- Navigating, reloading, or shipping new assets during a live turn must not lose the turn or the transcript.
- This is the axis that produced two of the five failures in §1.

### 4 · What exists today, and where it lives
**The two tiers**: the smoke pass and the full pass, side by side.
```text
smoke   python3 checks/run.py         seconds, read-only, the LIVE server:
                                      the tree serves, watch.py is rebuilding,
                                      the tree's _assets match the source,
                                      claude and node are present, and
                                      GET /_board/health proves the server's OWN
                                      interpreter imports claude_agent_sdk
full    python3 checks/run.py --full  minutes, real turns, on a THROWAWAY
                                      fixture board with its own server and its
                                      own Chrome: pty_e2e.py ①-⑦ (a real CLI turn
                                      through the PTY), one scoped SDK chat turn,
                                      and termnav.mjs (12 browser checks)
```
The three scratchpad suites of 260801 never landed under their own names; their coverage was rebuilt inside the board skill's `checks/` folder, and `checks/run.py` is the one command, in two tiers.


Five more suites sit next to those and are still typed one node file at a time, all Chrome over CDP against a real server, driving the real drawer rather than the endpoint.

```text
① binding.mjs     B1-B8    BINDING as an ORDER of operations, which is where
                           every instance of that bug has lived
② guichat.mjs     T1-T17   the SDK chat driven as a reader uses it: rendered
                           markdown, a reload mid-turn, 🗂 Sessions, context cost
③ tuichat.mjs     U1-U5    the TUI chat's own half; it runs `echo` and never
                           spends a model turn, so it costs nothing
④ switchback.mjs  S1-S3    HANDOVER: GUI → TUI → GUI while a turn is RUNNING,
                  C1-C2    a session switch, and closing the tab and coming back
⑤ scopechat.mjs   B1-B4    the chat at three scopes: page, group, whole board
```

`checks/ring_e2e.py` belongs to the same set and proves the turn outlives the socket that started it, which is CONTINUITY measured from the server side rather than the browser.

Two older instruments are not duplicated here.
`tests/test_hold.py` measures the second-turn latency that exposed the reconnect bug, and `cli/gate_live.py` freezes the live layer's responses so a refactor of `serve.py` can be proven not to change any of them.

### 5 · The trap this run has already fallen into
A talk run has one failure mode the browser run does not, and it cost most of a session on 260731.
The harness reads a state that a MODEL TURN has not reached yet, so a fixed sleep reports a failure that is only slowness.
Worse, the harness can be steered: a sibling session running `open <board url>` navigates any Chrome tab on the machine, and three separate red runs were traced to the tab having been moved out from under the test.

So the run pins its own tab and re-navigates if it drifts, it waits on conditions rather than clocks, and any assertion about a model's answer allows minutes rather than seconds.

## Aims
### Decision Now
These are the calls only JL can make; CC ticks nothing here.

- [ ] 🎛 Rule which tier the talk run uses
      → CC's proposal: cheap by default for BINDING and INTERRUPTION, which never read the answer's content, and JL's own tier for one TURN per kind.
      The reason is 260731: every suite that session ran used `haiku` and `low` while JL was on `Opus 4.8` and `high`, and that is why the runs stayed green through a bug JL could see.
- [ ] 🚦 Rule whether a red talk run BLOCKS a round or only reports
      → CC's proposal: reports only, matching `check.py`'s default, because a model turn can fail for reasons that are not the board's fault.


### Making the run exist as a thing
- [ ] 🧰 Make it one command
      `checks/run.py` is that command for the smoke tier and for the three checks inside `--full`, and it exits non-zero; the five browser suites in §4 are still typed one node file at a time, and nothing takes a board folder as an argument.
- [x] ⌨ Cover the TUI chat version
      Closed by `checks/tuichat.mjs` (U1-U5, its own half), `checks/pty_e2e.py` (a real CLI turn through the PTY), `checks/termnav.mjs` (the terminal follows the tree router, parked not held), and `checks/switchback.mjs` for HANDOVER, the axis where the two versions meet.
- [ ] 🎛 Settle which model and tier the run uses
      Cheap tiers make the run affordable and expensive tiers are what JL actually uses; 260731 showed a bug that only appeared at JL's settings.
      Unsettled in code too: the `--full` tier's SDK turn asks for `scope: scoped` and names no model, so it spends whatever the server's default is.

### Making it run without being remembered
- [ ] 🚦 Wire it into the round
      `QA3`'s gate says reachable; `QF3` claims that word for rendering, and nothing yet claims it for talking.
- [ ] 🧪 Prove it catches a real regression
      Break the router listener on purpose and watch `navtest.mjs` go red, the same way `assets.py`'s `verify()` was proven.

## Discussion

### From the retired States section (merged 260831)
Both chat versions now have suites checked into `checks/`, and `checks/run.py` gives two tiers of it a command that exits non-zero.
The five browser suites are still typed one file at a time, and no round dispatches any of it, so it still protects only the rounds where someone remembers.
- 260801 CC · 🔬 Opened from a session that fixed four talk failures and built the suites while doing it
  JL: "I think I want to add something in QF about testing out code for the SDK-Talk and CLI-Talk."
  JL named the two versions the same round: the SDK chat version (`QD2`) and the TUI chat version (`QD3`), which is the vocabulary this face uses throughout.
  Written from the runs rather than from a plan: every failure in §1 is one JL hit in the browser, and every suite in §4 was built to catch it afterwards.
  What justifies a fourth face rather than an item on `QF3` is that the instrument spends a model turn: `QF3` is free and fast and can run on every change, and this one costs money and minutes, so it cannot inherit the same trigger.

## Files
- `../../board/haipipe-board/assets/js/10-drawer/20-chat/`
  The SDK chat version, in six parts; BINDING and CONTINUITY live here.
- `../../board/haipipe-board/assets/js/10-drawer/30-terminal.js`
  The TUI chat version, which no assertion currently touches.
- `../../board/haipipe-board/assets/js/10-drawer/40-follow.js`
  `follow()`, the function whose missing listener was failure one in §1.
- `../../board/haipipe-board/live/chat.py`
  The session host, the hold, and the refusal that was rendered as an answer.
- `../../board/haipipe-board/checks/run.py`
  The standing checklist's entry point, smoke tier and `--full` tier; the rest of `checks/` is the suites in §4.
- `../../board/haipipe-board/tests/test_hold.py`
  The second-turn latency probe that exposed the reconnecting session.
- `../../board/haipipe-board/cli/gate_live.py`
  The response-identical gate for the live layer, which this run does not replace.
- `9-QF-execute/QF3-browser-run/QF3-browser-run.md`
  The third instrument; this face is the fourth and shares its browser but not its trigger.
- `4-QPf-page-folder/QPf4b-chat-sdk/QPf4b-chat-sdk.md`
  The SDK chat version's own face.
- `4-QPf-page-folder/QPf4c-chat-terminal/QPf4c-chat-terminal.md`
  The TUI chat version's own face.

## Log
- 260806 2201 · [REVISE-CC] swept to the 260806 architecture; `### 4` repointed from the three scratchpad `.mjs` suites to the checked-in `checks/` folder (`run.py`'s two tiers plus binding/guichat/tuichat/switchback/scopechat), the TUI-coverage Aim ticked on that evidence, `test_hold.py` corrected to `tests/test_hold.py`, and HANDOVER restated in `QD1`'s current per-scope Law
260801 · Opened on JL's ask for a QF face covering the SDK chat version and the TUI chat version, written from the five talk failures found in the browser on 260731 and the three suites built to catch them

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0