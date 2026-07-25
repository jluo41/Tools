# LLM topic icons
state: 🔴 OPEN
owner: CC
method: serve.py gains an endpoint letting an LLM pick emoji into the md; build.py stays dumb

## Question
The emoji at the head of a group title (`**🎨 …**`) is hand-written today. Could an LLM assign them automatically, so nobody has to think one up per line?

The hard part is that `build.py` is a pure static generator with no network and no LLM, so automating there means keyword guessing, and group titles are free sentences with no stable vocabulary; real automation can only live in `serve.py`, the layer that has an LLM. Leave it and every group title demands a human-chosen emoji, people get lazy, everything ends up the default 🔹, and the icon mechanism might as well not exist. The open forks are trigger, model, overwrite policy, and scope, all JL's to call: I must not pick for him and get overturned (`QD1`'s permission rule went through exactly that rework).

## Boundary
- ✅ Covered here
  **Automatic icon assignment**: how it triggers, which model, fill-blanks-only vs. overwrite, one question vs. the whole board.
- ↪ Covered elsewhere
  The hand-written half (`**🎨 …**` → 🎨, default 🔹 when absent), settled with `QA4`, spec in `ref/board-form.md §5`.

## Diagram
```
click 🎨 on the page      serve.py (already has OAuth + SDK)     write back to md → rebuild → reload
"assign icons"       →    reads this question, finds group    →   **the four undecided ones**
                          titles without an emoji                       ↓
                          haiku picks in one shot (a small job)   **🗂️ the four undecided ones**
                          fills blanks only; hand-written ones untouched
```

## Where we are
**Only the hand-written half exists (settled by QA4); automatic assignment is design-only so far.**

- Hand-written works today
  `**🎨 layout landed**` → 🎨; nothing written → default 🔹. `GT_ICON` extracts the first emoji; build.py renders the marker. Settled by QA4, graduated into `ref/board-form.md §8`.
- Automatic is still just a design
  serve.py already has an LLM (OAuth + SDK); one more endpoint lets it pick emoji and write them into the md. build.py takes no part: it has no brain; automation belongs to the LLM layer.

**The undecided forks (JL's to call):**

- 🔀 How it triggers
  A button (one click, instant, cheap, controllable, reversible) vs. auto-on-save (spends money on every save and edits your md while you type). I lean button.
- 🤖 Model + overwrite policy
  Picking emoji is a small job → haiku suffices; fill only group titles **without** an emoji, never overwrite what an author wrote.
- 📄 Scope
  Only the current question, or the whole board in one pass.

## Items to Finish
- [ ] Trigger settled
      Button vs. auto-on-save: pick one, write it into `## Law`.
- [ ] Model + overwrite policy settled
      Which model; fill blanks only, never overwrite hand-written.
- [ ] Scope settled
      Current question / whole board.
- [ ] Built and verified
      serve.py endpoint + page button; assigned emoji are visible, editable, revertible.

## Files
- `serve.py`
  The auto-assign endpoint goes here (it already has OAuth + SDK).
- `build.py`
  `GT_ICON` extracts the first emoji, `.gt .gi` renders the marker; the hand-written half already lives here.

## Discussion
> JL: could group-title icons be assigned in realtime by an LLM?
>> CC0723: yes, serve.py already has an LLM. But "realtime" forks: button-triggered (recommended: cheap, controllable) vs. auto-on-save (expensive, edits your md while you type). build.py stays dumb; clever work goes to the LLM layer.

## Log
260724 1242 · Translated to English (JL 260724: everything on the board in English)
260723 · Rewritten to the new structure: Question expanded into "one paragraph + bullets", added `## Boundary` and `## Files`; the retired `## Why here` merged into Question
260723 · Opened: "LLM auto-assigns group-title icons" recorded as a Q; the hand-written half settled with QA4, the trigger / model / scope of automation pending JL
