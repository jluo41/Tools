# Writing it so people understand
state: 🟡 PARTIAL
owner: CC
method: one set of writing rules + a zero-background reviewer subagent run over every revision

## Question
How should a Q's body be written so that someone who knows nothing about the matter understands it in one pass? And how do we make sure it **stays** that way, rather than depending on my mood on a good day?

The writer knows too many things that never made it onto the page, so your own text always reads fine to you. Readability cannot be self-tested; only an outsider can test it. JL's exact words: **"if it is not easy to read, writing that much is rubbish."** The board's entire value is being read by others; unreadable equals unwritten. This ranks ahead of structure and layout. It is the only rule that can be **re-run as acceptance**: every revision should be able to pass through it, instead of "written once, done forever".

## Boundary
- ✅ Covered here
  **How the words inside each section are written**: no invented terms, stale sentences must be purged, how zero-background cold reading verifies it, and how these rules land in `ref/writing-rules.md`.
- ↪ Covered elsewhere
  **Which sections exist** (structure): that is `QA2`; nor how sections are **arranged on the page**: that is `QA4`. This question owns only the prose itself.

## Diagram
```
    every QX-xxx.md
          │
          ▼
  ┌─ zero-background reviewer subagent ──────┐
  │  assumes: never saw the meeting notes,    │
  │        never read the code,               │
  │        does not know JL / CC / our colleagues│
  │  answers exactly three things:            │
  │    ① which sentence is unreadable — quoted│
  │    ② which word is never explained — list │
  │    ③ what background is missing           │
  └──────────────────┬───────────────────────┘
                     ▼
              issue list → edit md → run again  ⟲
                     │
              no new issues → the question counts as "readable"

  ✗ me re-reading in the same conversation — I know too much unwritten context to catch anything
```

## Items to Finish
- [x] Write down the rules for "what counts as plain language"
      `ref/writing-rules.md` (3.9KB): no invented terms, stale sentences must be purged, cold-read with a fresh agent after every revision; SKILL.md has a section pointing at it.
- [x] Per-file report: which sentence is unreadable, which word unexplained, what background is missing
      The cold read has run twice; the report follows exactly that format (unreadable sentences / unexplained words / missing premises / per-question grade).
- [ ] A standing zero-background reviewer subagent, not summoned by hand each time
      Today it is a manually dispatched fresh agent. Rules and prompt are written down, but not packaged as "one command runs it".
- [ ] Every major board change triggers a run automatically
      Relies on someone remembering. Not wired into build.py / serve.py.
- [ ] Convergence criterion written down
      `ref/writing-rules.md` has a first version (run until no new "unreadable" findings), but it is not quantified or finalized.

## Where we are
Ran it once by hand, it worked, but nothing has been institutionalized.

That first round's feedback was ugly: "like explaining a recipe's format without ever saying what the dish is"; ~35 terms used without explanation; of 7 questions, 1 barely clear, 5 vague, 1 incomprehensible.
After the edits things genuinely improved: `## Topic` (what this board is about) and `## Pipeline` (how the questions are ordered) were added, and terms moved into per-question `## Glossary`.

One more concrete lesson: **I have invented terms myself.** A coined translation for `battery`, plus "outward anchoring", "act one", "three-set gate", terms that appear 0 times in any source document. These hurt most: the reader assumes jargon, goes looking, finds nothing.

**The second round (this very board, 9 questions) just finished, and it does not look good: 2 clear (QA5 / QC1), 6 half-understood, 1 incomprehensible (QA4).**
Its three sharpest findings:
① The word "board" is ambiguous in self-referential context: sometimes the tool, sometimes this specific board; the reader guesses throughout.
② QA2's diagram says "top/bottom" while QA4's body said "side by side", the same fact contradicted in two places; and one section went by three different names.
③ `build.py`, `skill`, `/html-ppt`, "focus mode" appear across four or five files and are defined nowhere.

The two **self-contradictions from that report are fixed**: QA4's "side by side" now reads as the actual stacked layout; the section names are unified, no more three aliases in prose.
The big remainder is untouched: `build.py`, `skill`, `/html-ppt`, "focus mode" still have no single definition anywhere.

What is missing now: the rules and the prompt are in `ref/writing-rules.md`, and the cold read has run twice;
what lacks is **automation**: no standing agent, not wired into the build, still depends on someone remembering.

## Files
- `ref/writing-rules.md`
  This question's deliverable: the hard writing rules + the zero-background review prompt and convergence criterion.
- `SKILL.md`
  The "✍️ Writing" section: the three deadliest rules are excerpted there.

## Glossary
zero-background reader: someone who pretends to have never touched this project. Played by a fresh agent, because it genuinely does not know; I know too much unwritten context in this conversation to test anything myself.
subagent: a separately started Claude that sees only the files you hand it, not this conversation.

## Discussion
> JL: I want a new Q about how to write a Q's body so people can actually understand it. We can have a subagent review every md so someone with limited knowledge can still follow.

## Log
260724 1242 · Translated to English (JL 260724: everything on the board in English)
260723 · Rewritten to the new structure: Question expanded into "one paragraph + bullets", added `## Boundary` and `## Files`; the retired `## Why here` merged into Question
260723 1710 · Ticked during the board-wide review: writing-rules.md written, cold read run twice → 🟡 PARTIAL; the "automation" half remains
260723 0945 · Fixed the two self-contradictions from round two: QA4's side-by-side/stacked, and the three names for one section
260723 0925 · Second review (9 questions): 2 clear (QA5 / QC1), 6 half-understood, 1 incomprehensible (QA4)
260723 0915 · JL: "if it is not easy to read, writing that much is rubbish", formally opened as a question
260722 1900 · Added ## Topic and ## Pipeline per feedback; terms moved into per-question ## Glossary
260722 1830 · First zero-background review (7 questions then): 1 clear / 5 vague / 1 incomprehensible, ~35 unexplained terms
