# ⑦ The task-group folder: what exists on disk
state: 🔴 OPEN
owner: JL
method: measure what is actually there before ruling what should be, and treat an unadopted mandatory rule as a broken rule

## Question
What is in one task-group's folder, and what tells a human what state that group is in? A group holds several runnable folders that share a context, and the specification gives it exactly one place to say what it is and how far along it is: a `diagram/` folder of static `.txt` files. That surface is documented as mandatory for a cohesive group. It exists on 5 of 67 groups.

An unadopted rule is worse than an absent one, because it makes the docs describe a repository that does not exist. A reader of `ref/task-structure.md` expects `01-overview.txt`, `02-tasks.txt`, `03-progress.txt` and `04-design.txt` in every cohesive group, and will find them in 7% of them. Anyone reasoning about the bank from the docs is reasoning about a different bank.

The reason for the non-adoption is not laziness and that is the useful part. A `.txt` file has no state, no checklist that counts itself, nowhere for a comment to land, and nothing opens it. Writing it is beside the work rather than on the path through it, so it is written once at scaffold and never again, and `03-progress.txt` is stale by the second run. What this face has to settle is what a group folder contains once the thing that reports its state is something the entry command actually opens.

## Boundary
- ✅ Covered here
  What a task-group holds, what the doc surface was supposed to be, what it actually is, and what crosses this folder's edges.
- ↪ Covered elsewhere
  What would replace `diagram/` is `QA7`. What makes a child directory a task-folder is `QB1`. What binds one run together inside a child is the `QC` group. The letter-and-index naming rules are `hierarchy.md`'s and are not re-ruled here. The paper's version of this question is `QA6@paper`, whose delete test has no counterpart here.

## Diagram
```
   A TASK-GROUP.   ● = specified AND common   ◐ = specified, RARE   ○ = absent

   tasks/{G}{NN}_{group_name}/
   │
   ● │  {NN}_{task_name}/     the task-folders. THE WORK.
   │ │    detected by STRUCTURE, never by name          → QB1
   │ │    107 of them across 67 groups
   │ │
   ◐ │  sbatch/               cross-task orchestration, env.sh + batchers
   │ │
   ◐ │  diagram/              THE DOC SURFACE, as specified
   │ │    01-overview.txt   what this group is
   │ │    02-tasks.txt      | Task | What it sweeps | Status |
   │ │    03-progress.txt   cross-task run table
   │ │    04-design.txt     shared script logic
   │ │    group.excalidraw  the bundle
   │ │
   ○ └  a board              DOES NOT EXIST ANYWHERE       → QA7

   ── what the docs say, against what is on disk ───────────────────
      "MANDATORY when group is cohesive"     ref/task-structure.md
       diagram/ present                       5 of 67 groups     7%
       workflow/ present in a child          21 of 107 folders  20%
       QA/ present in a child                 1 of 107 folders   1%

      The one number that is not a problem is the last one. A QA/ is
      written only when a direction was worth digesting, so 1 is low
      but not wrong. The first is a rule nobody follows.  → QD1

```

```
   ── why 02-tasks.txt in particular does not survive ──────────────
      it is a STATUS TABLE, hand-maintained, listing every sibling.
      Every fact in it is derivable from the siblings themselves, and
      every one of them goes stale the moment a run finishes.
      A hand-written status table beside a machine-readable truth is
      the same defect STATUS.md was on the paper side, and it was
      retired there on the same day this board opened.

   ── what a group must NEVER hold ─────────────────────────────────
      ✗ README.md            the doc surface is diagram/, and now ⑧
      ✗ a .py of its own     that would make it a task-FOLDER  → QB1
      ✗ any consumer word    a claim id, a paper name, "for the paper"
                             → QA5. This is a grep nobody runs.
```

## Content
### The group is a container, and its only real content is its children
Everything in a group that is not a child folder exists to say something ABOUT the children:
`sbatch/` coordinates runs across them, `diagram/` narrates them. So the group's own state is
entirely a function of its children's states, which is exactly why a hand-maintained
`02-tasks.txt` cannot hold: it stores something derivable, and stored derivable state is state
that will disagree with the truth.

That observation is what makes `QA7` possible rather than merely nice. If the group's state is
the sum of its children's, then a board over the group needs one page per child and nothing else.

### What the doc surface was for, and which parts of it are real work
Not all four `.txt` files are the same kind of thing, and the distinction survives whatever
replaces them.

```
 01-overview.txt   WHY this group exists, and what binds the siblings.
                   Genuinely authored. Nothing derives it. It must survive.
 04-design.txt     the shared approach when siblings share a .py.
                   Also genuinely authored, also must survive.
 ────────────────────────────────────────────────────────────────────
 02-tasks.txt      a status table over the siblings.       DERIVABLE.
 03-progress.txt   a run table over the siblings.          DERIVABLE.
```
The top two are content and the bottom two are a report. A board keeps the first two as prose a
human writes once and edits rarely, and stops storing the second two at all, because a page per
child already carries its own state and its own log.

### What crosses this folder's edge
```
 ① ──▶ ⑦   IN, through a lifecycle run or a scaffold. The group
           CONSUMES the contract and never stores a copy: no SKILL.md,
           no ref/, no template is ever copied into a group.

 ⑧ ──▶ ⑦   IN, once ⑧ exists. Today nothing.

 ⑦ ──▶ out THE QA DIGEST, and nothing else. results/ is not a
           consumer surface and never becomes one.        → QD1 QD2

 ⑦ ──▶ a consumer   NOTHING. A task never names a paper.  → QA5
```
Almost nothing in a group is authored at group level. The code, the configs, the runs and the
results all live one level down. What the group genuinely owns is the SHAPE: which children
exist, why they belong together, and how far each has got.

## Items to Finish
- [ ] 📏 Accept the measurement as the starting point
      5 of 67, 21 of 107, 1 of 107. These are counts from disk on 260726, not estimates, and the first one says a documented mandatory rule is not followed.
- [ ] ✂️ Rule which of the four .txt files survive
      `01-overview` and `04-design` are authored content. `02-tasks` and `03-progress` store derivable state. The proposal is that the first two survive as pages and the last two stop existing. Nothing is ruled.
- [ ] 🗂 Rule where the surviving prose lives
      Either a group-level page on `⑧`, or the group's `board.md` `## Topic`. The second is cheaper and puts the "why these belong together" text exactly where a reader arrives.
- [ ] 🧹 Rule what happens to the 5 groups that DO have a diagram/
      They are the only ones with real authored narrative, so they are the migration's input, not its casualty. Nothing may be deleted before it is read.
- [ ] 🔍 Make "no consumer vocabulary" checkable
      A grep over `tasks/` for claim ids, paper names and the word "paper" in a stake-bearing sense. The rule is stated in `SKILL.md` and enforced nowhere.

## Where we are
Nothing is ruled and the measurement is done. 67 task-groups hold 107 task-folders. The
documented group-level doc surface exists on 5 of them, the per-folder `workflow/` on 21 of 107,
and a `QA/` on 1 of 107.

The single actionable finding is that the group has no live state surface at all, and the one it
was given is not written because nothing opens it. That is the fact `QA7` and `QA4` are both
answers to.

- 260726 CC · 📏 Measured rather than assumed
      `ref/task-structure.md` and `ref/hierarchy.md` describe the group folder; the counts above come from `ls` over `examples/*/tasks/`. The two disagree, and the docs are the ones that are wrong.

## Files
- `task-structure.md`
  The group-folder contract, including the `diagram/` surface that 7% of groups have.
- `hierarchy.md`
  Level 2 in the conceptual model: what a group is and how it is named and indexed.
- `fn/task-group.md`
  The scaffold verb, which is where any change to what a new group contains has to land.

## Discussion
> CC 260726: the parallel to `QA6@paper` is close enough to be worth naming and it stops in one place. There, the ruling was the delete test: a prefix means working machinery and `rm -rf 0-* 1-* 2-*` must leave something submittable. A task-group has no deliverable, so it has no delete test and cannot borrow one. What it has instead is the derivable/authored split above, which does the same job of making a rule checkable rather than tasteful.

## Log
260726 · Created with the board.
