# One file, two skills: what does each own?
state: 🟡 PARTIAL
owner: JL
method: keep one shared file; state the ownership line rather than leaving it to habit

## Question
When a lifecycle page is written by one skill and rendered by another, which one owns it?

The answer that was chosen is deliberately blunt: there is ONE file. The stage's artifact and the board's page are the same markdown, not two representations kept in step. That decision removed an entire class of bug before it existed, and it created a smaller, sharper problem in its place, which is that two skills now write to one file and nothing states who may touch which part.

## Boundary
- ✅ Covered here
  The ownership line inside a shared page, and what each skill may write.
- ↪ Covered elsewhere
  What the artifact contains is `QC1`; the Content boundary is `QBa1`; what the file is called is `QC2`; who creates it is `QF4`.

## Content
### Why one file rather than two
The alternative was an adapter: the paper skill writes its own format, the board reads and renders it. It was tried and rejected, because an adapter means a rendering that can silently disagree with its source, and a comment layer that cannot write back to anything a human edits. One file removes both.

### The ownership line as it actually stands
```
 /haipipe-paper   the page's SUBSTANCE
                  Question · Boundary · Content · Items to Finish · Where we are
                  written by DRAFT and REVISE, ruled at CHECK

 /haipipe-board   the page's FURNITURE and the machine-managed block
                  the section grammar, the state vocabulary,
                  the Stage Contract between its sentinel comments

 the human        anything, at any time; the file is plain markdown and that
                  is the reason it was chosen
```

### The part that is real and unwritten
The Stage Contract block is generated and will be overwritten. Everything else is authored and must never be. That rule exists in the code and in a comment inside the block; it is not in the paper skill's contracts at all, which is exactly where an agent writing a stage would look for it.

## Items to Finish
- [x] 📄 One file, not two
      The stage artifact and the board page are the same markdown; no adapter exists.
- [ ] 📐 Write the ownership line into the paper skill
      A stage worker reads `stage.md`, not the board's source. If the rule that the managed block is regenerated lives only in the board's code, a worker will eventually hand-edit it.
- [ ] 🧠 Rule what happens when the board's grammar changes
      The section shape rule changed on 2026-07-25 and nine pages were re-levelled by hand. Decide whether a grammar change is a migration the board runs, or a duty the paper skill inherits.

## Where we are
The one-file decision is implemented and has held. The ownership line is understood by whoever is working and written down nowhere a stage worker reads.

## Files
- `stages/*/stage.md`
  Where the ownership line should be stated.
- `haipipe-board/src/stage_contract.py`
  The only writer of the managed block.
