# Fresh-agent acceptance: enter a group, run a folder
state: 🔴 OPEN
owner: JL
method: give a new agent only the shipped docs and one real group, and watch where it stops

## Opening
Can someone who was not here enter a task-group and run a task-folder without us? That is the only test of everything on this board, and it is deliberately last, because every other page is an opinion until this one passes.

The test has to run on the shipped surface and nothing else: `SKILL.md`, `ref/`, `fn/`, and a real task-group on disk. Not this board, which the runtime may never depend on, and not a conversation. If a fresh agent needs something that exists only in a design page or in somebody's memory, the package is incomplete and the specific missing thing is the finding.

What makes this worth its own face rather than a checkbox is that the interesting output is not pass or fail. It is WHERE the agent stops. A run that gets to Build and cannot name a config is telling us something different from one that cannot decide whether a directory is a task-folder, and each stopping point maps to a page on this board.

**Covered elsewhere**: Every page on this board is a candidate stopping point. The paper family's version of this test is `QE2@paper`.

## Diagram
```
   THE ACCEPTANCE RUN

   given     a FRESH agent, clean context
             a REAL task-group on disk
             the SHIPPED surface only:
                 SKILL.md · ref/ · fn/ · the specialist for the type
   forbidden this board · any conversation · any of us

   the run
     1  enter the group        what does it SEE?              → QA4
     2  pick a task-folder     by STRUCTURE, or by name?      → QB1
     3  plan                   is the IPO contract complete?  → QB2
     4  build                  does it write an Intent docstring? → QB3
     5  execute                does it press the button itself?   → QB4
     6  report                 does it compare, or describe?  → QB5
     7  asked a question       does it use the qa door?       → QA5

   ── the useful output is WHERE it stops, not whether ───────
      each stopping point names the page that failed to ship a rule:

        cannot tell a folder from a group   → QB1 did not graduate
        names four sisters inconsistently   → QC1 did not graduate
        commits a checkpoint                → QC2 did not graduate
        reads results/ to answer            → QD2 did not graduate
        writes a claim id into a digest     → QA5 did not graduate
        types /haipipe-board itself         → QA4 did not graduate

   ── the entry step is the new one ──────────────────────
      step 1 is currently untestable: entering a group prints text,
      so "what does it see" has an answer nobody is happy with.
      This face cannot pass before QA4 does.
```

## Content
### The shipped surface is the whole surface
The rule that makes the test meaningful: a fresh agent reads what a stranger would find, which is
the skill package. This board is a working record and the runtime may never depend on it, which is
`QA3`'s one-way rule stated as a test rather than as a principle.

### A stopping point is a graduation failure, and that is the report
Every place the agent stalls names a rule that was decided here and did not reach the manual. That
makes the acceptance run a diagnostic on this board rather than only on the package, and it is why
the mapping in the Diagram is worth keeping current as pages settle.

### It cannot run yet, and the reason is the ask
Step 1 asks what a fresh agent sees on entering a group. Today it sees a paragraph, which is the
thing `QA4` exists to change. So this face is blocked on `QA4` in a way the others are not: the
rest of the run could be exercised now, but the first step would be testing the behaviour we have
already decided to replace.

## Aims
- [ ] 🚪 Wait for `QA4`
      Step 1 tests what a human sees on entering a group. Running it before the entry ruling lands measures the thing we are removing.
- [ ] 🧪 Run the test once, on a real group
      A group with several children, a fresh agent, the shipped docs. One run produces the whole stopping-point map.
- [ ] 🗺 Keep the stopping-point map current
      Each entry names a page. As pages settle and graduate, the map is the check on whether the graduation actually worked.
- [ ] 🔁 Rule what a failure costs
      Whether a stopping point blocks the board's `close:` or is recorded as an open item on the page it names. The second is more honest and the first is what a close condition usually means.

## Discussion

### From the retired States section (merged 260831)
Not run. It cannot be run until `QA4` settles the entry, and nothing else on this board has
graduated yet, so a run today would stop at step 1 and report the one thing already known.
- 260726 CC · 🧭 Made the stopping point the output
      Modelled on the paper family's fresh-agent face, with one change: the map from stopping point to page turns a pass/fail test into a diagnostic on this board's own graduation.

## Files
- `SKILL.md`
  The shipped surface, and the first thing a fresh agent reads.
- `hierarchy.md`
  What `SKILL.md` Step 0 tells it to read before anything else.
- `QE2@paper`
  The same test in the paper family. Consulted for shape.

## Log
260726 · Created with the board.

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0