# ⑧ Its board: one S page per task-folder
state: 🔴 OPEN
owner: JL
method: one page per independently gated unit, state derived from disk, and a page that describes code rather than being it

## Opening
If a task-group opens a board, what are its pages? The group's own state is the sum of its children's states, so the answer that falls straight out is one page per task-folder: twelve folders, twelve pages, and the board index IS the status table that `02-tasks.txt` was supposed to be and is not.

That is the easy half. The hard half is that this board would be a third kind of board, and the two kinds that already exist do not tell us how to run it. A design board like this one EMPTIES: a ruling reaches ✅ and its Law graduates into the skill, so the page is scaffolding. A paper board never empties, because its pages ARE the manuscript: the Content on the page is the prose that gets generated into LaTeX. A task board is neither. Its page cannot be the artifact, because the artifact is a `.py` file, a config and a directory of results, and none of those are markdown.

So a task board's page DESCRIBES something it does not contain, and that is a failure mode neither existing board has. A design board cannot drift from its skill without a human noticing, because the skill is the only reader. A paper board cannot drift from the paper at all, because it is the source. A page that narrates a folder of code can be wrong about that folder from the moment the next commit lands, and nothing would say so.

**Covered elsewhere**: What the folder being described contains is `QA6`; what makes a child a task-folder at all is `QB1`; the two gates whose passing a `state:` would report are `QB3` and `QB5`; who calls the board and when is `QA4`. What a board IS belongs to `01-boardform-260722` and is not ruled here. The opposite object, a board whose pages are the artifact, is `QA7@paper`.

## Diagram
```
   THREE KINDS OF BOARD.   the third one is new, and it can be WRONG.

   ② a DESIGN board          ⑧ a PAPER board          ⑧ a TASK board
      diagrams/01-*             Paper-X/0-lifecycle/     tasks/{G}{NN}_*/
   ─────────────────────    ─────────────────────    ─────────────────────
   the page ARGUES a        the page IS the          the page DESCRIBES
   rule                     manuscript               a folder of code
        │                        │                        │
        ▼                        ▼                        ▼
   it EMPTIES:              it NEVER empties:        it never empties AND
   a ✅ ruling's Law        Content is generated     it can go STALE.
   graduates into the       into sections/*.tex      Nothing generates
   skill and the page       one way                  from it, and nothing
   becomes scaffolding                               checks it against
                                                     the code it narrates.
   drift is impossible:     drift is impossible:     ← THE NEW PROBLEM
   the skill is the only    the page is the source
   reader

```

```
   ── WHAT THE PAGES WOULD BE ──────────────────────────────────────

   tasks/B01_evaluation_clm/
     board.md                    Topic = what 01-overview.txt held
     S-Task-01-eval-holdout.md   ┐
     S-Task-02-eval-ood.md       ├─ ONE PAGE PER TASK-FOLDER
     S-Task-03-eval-ablation.md  ┘   the index IS 02-tasks.txt, derived
     QB1-<a ruling this group had to make>.md    Q pages allowed, rare

   the group's state = the sum of its children's. Nothing else to store.

   ── WHAT A PAGE HOLDS, when the artifact is not text ─────────────
      Question       what this folder answers, and why it exists
      Content        the approach: what 01-overview + 02-design held
      Items          the runs still owed, and the gates not yet passed
      Where we are   the runs table: 03-runs.txt, but derived
      Log            04-progress.txt, which was already a dated log

      four .txt files become one page with a state and a comment box.

```

```
   ── the open question this shape forces ──────────────────────────
      what does ✅ MEAN on a task page?
      a paper page: its ONE human gate passed.
      a task folder has TWO machine gates (CODE_REVIEW, RUN_AUDIT)
      and a human who presses the button between them.
      Three candidates, none ruled:
        (a) Report finished and RUN_AUDIT passed
        (b) a human read the result and accepted it
        (c) every run in Items to Finish is ticked
      (a) is derivable. (b) matches the board's own meaning of ✅.
      (c) is the only one that survives a folder gaining a new run.
```

## Content
### One page per task-folder, because the unit is already there
The board's rule is one page per independently gated unit. A task-folder is exactly that: it has
its own `workflow/plan.yaml`, its own code, its own runs, its own `CODE_REVIEW.md` and
`RUN_AUDIT.md`, and it succeeds or fails on its own. No smaller unit is gated and no larger one
is, since the group runs nothing itself.

So the mapping needs no invention, which is the strongest argument for it. Twelve folders, twelve
pages, and the index that the board already renders is the status table the docs asked someone to
maintain by hand.

### What Content means when the artifact is a `.py`
On a paper board the page holds the prose and `sections/*.tex` is generated from it, one way. That
cannot happen here: nobody wants markdown generating Python, and the `.py` is the source of truth
for what the task does.

What is left for Content is the thing that was already being written by hand and thrown into a
`.txt`: what this folder is for, what approach it takes, and why it is shaped that way. That is
real content, it is genuinely authored, and no tool derives it. The page is therefore a NARRATIVE
over an artifact rather than the artifact, and the honest way to say that is that `01-overview.txt`
and `02-design.txt` become the page's Content, while `03-runs.txt` and `04-progress.txt` become
`## Where we are` and `## Log`, which the board already has sections for.

### The drift this creates, and the only defence that would work
A page describing code can be wrong about that code, and the failure is silent. Three defences
are possible and only one of them is cheap:

```
 a human re-reads it        does not happen. The .txt files prove it.
 a machine diffs prose
   against code             not possible in any useful sense.
 the page carries DERIVED
   rows nobody types        cheap, and partial.
```
The third is the one worth doing. A run table is derivable from `results/`; a gate status is
derivable from `CODE_REVIEW.md` and `RUN_AUDIT.md`; a folder's last activity is derivable from
the filesystem. If every derivable row on the page is generated on rebuild, then the only prose
that can drift is the prose a human wrote on purpose, which is the part they are most likely to
notice being wrong.

That does not solve it, and this face should not claim it does. It shrinks the drifting surface
from the whole page to the two paragraphs somebody meant.

### The family name is unruled, and both answers are defensible
The board's filename rule is `S-<Family>-<unit>-<slug>.md`, and a task-group has no obvious
family.

```
 one family, "Task"      S-Task-01-eval-holdout.md
   simplest, and honest: within a group the children ARE all the
   same kind of thing, which is what makes them a group.

 family = task-TYPE      S-Eval-01-holdout.md · S-Fit-02-sweep.md
   groups the index by kind of work, which matters exactly when a
   group is heterogeneous, which is the case the docs already say
   should not use a shared narrative at all.
```
The first is probably right for that reason: a group that would benefit from the second is a
group that should have been two groups.

## Aims
- [ ] 📄 Rule one page per task-folder
      The mapping itself. Everything else on this page assumes it.
- [ ] 🏷 Rule the family name
      `S-Task-<NN>-<slug>.md` or family-by-type. The argument in Content favours the first; nothing is decided.
- [ ] ✅ Rule what SETTLED means on a task page
      Three candidates in the Diagram. A folder that gains a thirteenth run after being marked ✅ is the case that separates them, and it is the common case.
- [ ] 🔄 Rule which rows are DERIVED and regenerate on every build
      Runs, gate status, last activity. This is the only defence against drift that costs nothing, and it decides how much of the page a human is allowed to type.
- [ ] 📥 Rule what happens to the 5 existing diagram/ folders
      They hold the only authored group narrative that exists. They are the migration's input; nothing may be deleted before it is read.
- [ ] 🧪 Lay a board over one real group and read it cold
      A group with several children, a board built, and a fresh agent asked what state the group is in without being told. That is the whole proposition, tested once.

## States
Nothing exists. No task-group on disk carries a board, and the S-page shape above has not been
written even once, so every claim here is a proposal rather than a report.

What is settled is the surrounding shape rather than this page's own content: `QA4` has JL's
ruling that entering a group opens a board, and `QA6` has the measurement that says the surface
it would replace is written by 7% of groups. This face is the part between those two, and it is
the part with the most unruled decisions on it.

- 260726 CC · 🧩 Named the third kind of board
      Writing the page shape surfaced that a task board is neither of the two kinds that exist: it does not empty like a design board and it is not the artifact like a paper board, so it is the first board that can be silently wrong about the thing it describes. That is now the face's central problem rather than a footnote.

## Files
- `task-structure.md`
  The four `.txt` files this board would absorb, and what each was for.
- `haipipe-board/`
  The tool that would render it, including `stage.py`, which owns the S filename rule the family question above is about.
- `QA7@paper`
  The opposite object: a board whose pages ARE the artifact. Read for the contrast, not the recipe.

## Discussion
> CC 260726: the drift problem is the reason I would not simply copy the paper board's shape and change the nouns. On the paper side, "nothing leaves the board" is safe because the board is the source. Here the code is the source and the board is commentary, so the same sentence would mean the opposite thing: a page that never changes while the folder it describes changes weekly. If only one thing gets ruled from this face, it should be the derived-rows item, because it is the only mechanism that makes the page cheaper to keep true than to let rot.

## Log
260726 · Created with the board.
