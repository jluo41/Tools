# Driving the board in a real browser
state: 🟡 PARTIAL · the run exists and passes 36/36; it is not yet one command and nothing dispatches it
owner: JL
method: list the failures that shipped green, group them into what a browser can answer, and make the run repeatable

## Opening
What must a real browser click, drag, and observe before a board change can be called usable?

Source checks cannot tell whether CSS hid a control, JavaScript built the wrong widget, or a write failed in the page.
Those failures can leave every Markdown and structural check green while the product in front of the reader is broken.
The browser run closes that gap by exercising the same page and gestures a person uses.
It succeeds when navigation, controls, writes, refreshes, and in-progress work survive together.

## Content
### 1 · Six failures that shipped with a green checker
Every one of these was found by JL rather than by the pipeline, and every one of them was invisible to `check.py` by construction.

The index rendered as a wall of inline underlined links, because its rows were reimplemented with invented class names and not one CSS rule matched.
The left page list was absent from the tree entirely, because the template never had the slot.
Six group-intro ASCII figures were missing, so the ASCII was not failing to render as monospace, it was not being emitted at all.
Every write from a tree page failed SILENTLY, because the path a write posts resolved to a folder with no `board.md` in it.
A shipped CSS fix did not reach the page, because the linked stylesheet had no cache-busting.
And a stray disclosure triangle survived two fixes, because the rule meant to suppress it had the same specificity as a generic rule further down the file.

The pattern is one sentence: **a checker reads the SOURCE, and every one of these lives in what the BROWSER did with it.**

### 2 · What a browser run answers that nothing else can
**The instrument gap**: what only a real browser can witness.
```text
                          check.py   fresh reader   browser run
does the markdown parse       ✅          ·             ·
is the prose readable         ·          ✅             ·
did the CSS apply             ✗           ✗            ✅
did the JS build its widgets  ✗           ✗            ✅
does a click write a file     ✗           ✗            ✅
does a drag move anything     ✗           ✗            ✅
did an edit reach the page    ✗           ✗            ✅
```

### 3 · The run, as it stands today
**The run today**: each numbered assertion and where it stands.
```text
①  index renders its ruled components   rows · groups · intros · ASCII figures
                                        Board Map · Matrix · Activity · page list
②  the ASCII is really monospace        computed font-family and white-space
③  every link the index offers resolves 62 targets, HEAD each one
④  a page renders in focus format       no coloured bar, focus width, breadcrumb
⑤  every widget the JS builds           drawer · fabs · dock · page list · drag handle
⑥  the page list drags and the text yields   238 to 440, content 369 to 470
⑦  a real write reaches the .md         row lands in place, page does not jump
⑧  the loop closes                      .md edited, page updates itself in ~3s,
                                        open sections, scroll AND a half-typed
                                        chat draft all survive
⑨  isolation                            page C changes, page B untouched
```
Chrome over CDP, driving a real page rather than fetching it: `Input.dispatchMouseEvent` for genuine presses and drags, `getComputedStyle` for what the CSS actually did, and a real `.md` write to close the loop.
Nine groups, 36 assertions, all passing on 260801.


Two of these deserve their names.
Group ② exists because "the figure is present" and "the figure is monospace" are different claims and only the second is what a reader gets.
Group ⑧ ends by checking a half-typed chat draft, because the point of the live update is not that the content changes, it is that it changes without costing the reader anything they had in flight.

### 4 · The trap this run has already fallen into twice
A browser run fails for two reasons, and they look identical: the thing under test is broken, or the harness is.
On 260731 every assertion went red at once and the cause was `serve.py` having died; `document.body.className` was `neterror`.
Earlier the same day a live-update test reported a failure that was a race in the TEST: the poll took its first baseline AFTER the rebuild, so it never saw a change.

So the run's first assertion is deliberately `page actually loaded`, and any group that goes wholly red is treated as a harness fault until proven otherwise.

## Aims
### Making the run repeatable
- [ ] 🧰 Make it one command
      It is a script pasted into a shell today. It should be a file in the skill that takes a board folder and exits non-zero on a red assertion.
- [ ] 🔌 Decide how it gets a browser
      It needs Chrome plus CDP plus `websocket-client`, and two sibling harnesses have since answered that for the skill.
      `cli/sentencerun.py` marks the import optional and exits 2 with a loud SKIP when no browser answers the CDP port; `checks/run.py --full` boots its own headless Chrome on a free port.
      What is left for this run is to adopt one of the two rather than invent a third.

### Making it run without being remembered
- [ ] 🚦 Wire it into the round
      `QA3`'s gate is written as written-back, rebuilt, checked, reachable, stated. This run is what "reachable" should mean, and nothing dispatches it.
- [ ] 🧪 Prove it catches a real regression
      The `verify()` gate in `assets.py` was proven by breaking a filename on purpose and watching it fail. This run deserves the same proof, on one of the six failures in §1.

## States
The run exists and passes 36 of 36 on 260801, on the boardform board.
It is not yet a file and nothing dispatches it, so today it protects only the rounds where someone remembers to type it.
Its dependency half is no longer open: `cli/sentencerun.py` (260801) and `checks/run.py` (260802) both shipped a browser-dependency policy this run can adopt as it stands.

- 260801 JL · 🔬 Opened on JL's ask to run the browser and evaluate
  JL: "could you run the browser to do the evaluation? I think in the QF series, we might have the page to explain what things we might need to check."
  The evaluation ran first and the page was written from its evidence rather than from a plan: nine groups, 36 assertions, all green.
  What justifies a third face rather than an item on `QF1` is that the instrument is different in kind: `QF1`'s two instruments both read text, one mechanically and one as a person, and every failure in §1 lived in what a browser did with that text afterwards.

## Files
- `../../board/haipipe-board/cli/check.py`
  The first instrument, and the one that was green through all six failures in §1.
- `9-QF-execute/QF1-acceptance/QF1-acceptance.md`
  The two text instruments and their shared trigger; this face is the third and shares that trigger.
- `1-QA-constitution/QA3-the-round/QA3-the-round.md`
  The gate whose "reachable" condition this run is the only honest test of.
- `7-QC-engine/QC3-roundtrip/QC3-roundtrip.md`
  The loop that group ⑧ closes: markdown to html and back. It carried the id `QC9` before the 260801 renumbering.

## Log
- 260806 2201 · [REVISE-CC] swept to the 260806 architecture; the dead `QC9-roundtrip.md` pointer repointed at its live file `7-QC-engine/QC3-roundtrip/QC3-roundtrip.md` (renumbered 260801), and the "the skill declares no browser dependency" claim corrected in Aims and States against `cli/sentencerun.py` (exit 2 + loud SKIP) and `checks/run.py --full` (its own headless Chrome on a free CDP port)
260801 · Opened after a 36-assertion browser run passed, and written from that run's evidence; the six failures it exists to catch all shipped green through check.py on 260731
