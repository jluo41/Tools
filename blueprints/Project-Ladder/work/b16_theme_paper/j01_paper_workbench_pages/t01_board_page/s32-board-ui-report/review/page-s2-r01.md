# Board page (Report and Work) · stage 2 · round 1 · 261105

A fresh reviewer, the live placeholder Board (Paper-Example), all 14 views; haipipe-ui Review, verbatim.

```text
page     http://127.0.0.1:5602/_board/workbench?layout=focus&path=Tools/blueprints/Project-Ladder/paper/Paper-Example&section=report|work (all 14 views)
answers  what: Paper-Example, Purpose "does <a policy> change <an outcome>…" · where: path DrFirst-SPACE › … › Paper-Example · here: partly; the section and view are lit, but the content is only closed bars · do: partly; no verb shows until a bar is opened
rules    1 ✅ · 2 ❌ no view-caption on any of the 14 views (board_views.py defines the captions, none render) · 3 ✅ · 4 ❌ closed bars carry no main sentence, state or tally; the 🙋 empty state is an instruction ("…runs/rNN_collect_<slug>/ (haipipe-interaction)") · 5 ❌ "waiting for JL" (Plan › Roadmaps); the Writing tabs have no state word
tasks    direction chosen: 2 clicks · RQ2 answered?: 2 · main estimate as printed: 1 · what waits on me: 3 (Work › Data + Paper Plan; no flag on the closed bars) · Figure 1 state: 2, the plan drawing is unreadable without Draw
walk     82 steps · 80 ✅ · 0 ❌ · 2 ⚠️ (a favicon 404 "no icon" on every fresh load; at phone width the Values table loses its column labels and the iframes clip Values and Citations)
bar      Opened, it matches the paper UI (side tabs, chips, tree, pills). Closed, every view is 3 to 10 identical bars with no picture or state.
rubrics  Glance 8 · Place 7 · Lean 6 · Words 6 · One job 7 · Same look 9 · Phone 8 · Salience 4 · Works 7 · Modern 6 · Plain 6 · Complete 8
score    mean 6.8/10 · not yet
fixes    1. Move section 1's main sentence under its closed bar, and put a state word on each bar's right ("A selected", "RQ2 open", "waiting for you").
         2. Remove the instruction text to Guide: the 🙋 empty state becomes "Nothing asked yet", the maps' "Not written yet: ask in the Studio chat…" becomes "No map yet", and Plan's 3–4-line monospace prompts go behind Copy prompt. Render the view-caption.
         3. Rename "waiting for JL" to "waiting for you". Give Displays "1 · Plan" an emoji. Give Plan its own emoji (not Direction's 🧭) and Runs to do its own (not the band's ⚙️). Rename Idea's "🚧 Open" to "📌 Open points". Remove "Runs to do" (it repeats the Task roadmap) and the "j11_writing_v1130_desk ·" sub-line that repeats 5 times.
complete Every field is one click away except Report Writing's per-Section state, which shows in Work only.
questions Should section 1 start open, since every view now reads as a page of headings? Should Theory move into each Direction's panel, since Idea lists the same three directions twice?
```

The walk, recorded after this round's fixes (261105), as a short video to pause and step: [block.html](../../../../walks/block.html)
(also under the Block's Report › Block UI › 🎬 The walk).
