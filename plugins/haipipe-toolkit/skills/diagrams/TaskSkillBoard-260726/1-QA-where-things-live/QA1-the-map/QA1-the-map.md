# Seven folders, one door in, one door out
state: 🔴 OPEN
owner: JL
method: name every folder, allow one entry and one exit, and treat the consumers as a wall rather than a room

## Opening
Where does a new rule, file, or page belong, and what may reach this layer from outside it? Seven folders exist, and the two that matter most are a task-group on disk and the board that should be laid over it. Put something in the wrong one and it either binds nothing, because no runtime reads it, or it becomes wrong for every other project.

The word "task" names several different things at once, and they sit in two different repositories. There is a reusable skill package that ships. There is a design board arguing about that package. There are 67 task-groups holding 107 runnable folders across real projects. And there is the control plane those folders should be worked from, which today does not exist. Each holds a different kind of truth and each has a different lifetime, but all four are called "the task work" in conversation, so nothing stops a file from landing in the wrong one.

The asymmetry with `/haipipe-paper` is the thing to get right, because the two look like mirror images and are not. A paper is a CONSUMER: it owns neither channel out of itself, and its design is mostly a boundary it must not cross. This layer is an EXECUTOR: it may run anything, and its discipline runs the other way. It must never learn who asked. So the wall the paper board draws from outside is the same wall drawn here from inside, and `⑤` is not a door we go out through; it is the door a question comes in through, and it is one verb wide.

**Covered elsewhere**: What is inside the skill set is `QA2`; what is on this board is `QA3`; the human channel is `QA4`; the wall as a mechanism is `QA5`; what a task-group holds is `QA6` and what its board would hold is `QA7`. The probe layer's own model is `01-probe-qa-260726`, which we consult and never rule.

## Diagram
```
   THE SHAPE.   we are the BANK.  one door in, one door out.

        A CONSUMER                                      THE HUMAN
    paper · application                             eyes, clicks, a yes
        asks, never reaches in                              ▲
              │                                             │
              ▼                                             │
        ⑤ the `qa` verb            ①            ③ /haipipe-board
        THE ONLY DOOR IN     /haipipe-task        the ONLY way a human
        one question in,     THE SUBSTANCE        touches the work
        one PATH out         runs ⑦ and ⑧               │
              │                     │                      │
              └─────────────────────┴──────────────────────┘
                                    ▼
                       ⑦ the task-group · ⑧ its board

```

```
   ── the seven folders ────────────────────────────────────────────
   ┌──────────────┬──────────────────────────┬─────────────────────────────┐
   │ reusable     │ ① skills/task/           │ ② diagrams/01-haipipe-      │
   │ THE TASK     │   44 skills · 9 domains  │     task-260726/  19 faces  │
   │  SKILL       │   7,134 lines            │     WHAT IS ARGUED ← here   │
   ├──────────────┼──────────────────────────┼─────────────────────────────┤
   │ reusable     │ ③ board/                 │ ④ diagrams/BoardSkillBoard- │
   │ THE HUMAN    │   haipipe-board/         │     260722/                 │
   │  CHANNEL     │   v0.30.0                │     READ-ONLY from here     │
   ├──────────────┼──────────────────────────┼─────────────────────────────┤
   │ reusable     │ ⑤ probe/haipipe-probe/   │ ⑥ diagrams/01-probe-qa-     │
   │ THE WALL     │   the CONSUMER's skill,  │     260726/  20 faces       │
   │              │   not ours. We never     │     READ-ONLY from here.    │
   │              │   call it.               │     It owns the QA contract │
   ├──────────────┼──────────────────────────┼─────────────────────────────┤
   │ ONE GROUP    │ ⑦ tasks/{G}{NN}_{name}/  │ ⑧ its BOARD                 │
   │              │   67 groups · 107 folders│     DOES NOT EXIST YET      │
   │              │   WHAT IS RUN            │     ← this board's ask      │
   └──────────────┴──────────────────────────┴─────────────────────────────┘

   ⑧ is the only cell on this grid that is empty, and that is the whole
   reason this board was opened.

```

```
   ── the crossings, and nothing else ──────────────────────────────

   ⒜  ② ──graduates──▶ ①
        a ruling reaches ✅ and its Law is COPIED into SKILL.md or ref/.
        Nothing graduates into ③ or ⑤: we do not own them.

   ⒝  ① ＋ ③ ──together──▶ ⑦ AND ⑧
        two skills on ONE markdown file, never the same REGION.
        The seam is ruled on QA8@paper and is NOT re-ruled here.

   ⒞  a CONSUMER ──asks in──▶ ⑤ ──▶ the `qa` verb
        a STRING with the stake already stripped, arriving in general
        language. We answer with a PATH. We never learn who asked,
        and we never call ⑤ ourselves.

   ⒟  ✗ FORBIDDEN
        ① ──▶ a consumer   naming a paper, a claim id, an application
        ① ──▶ ②            a runtime skill needing an open Q page
        a consumer ──▶ results/   reading past the digest  → QD2
        delete this board and every skill still runs.
```

## Content
### Seven folders, and why the eighth cell is empty
```
① task skill     settled, reusable procedure     skills/task/
② its board      the rulings that produced it    diagrams/TaskSkillBoard-260726/
③ board tool     THE HUMAN CHANNEL               skills/board/haipipe-board/
④ its board      the rulings that produced IT    diagrams/BoardSkillBoard-260722/
⑤ probe layer    THE WALL, from the far side     skills/probe/haipipe-probe/
⑥ retired 260804 the QA-file contract shipped    skills/probe/haipipe-probe/
⑦ a task-group   67 of them, 107 folders         examples/*/tasks/{G}{NN}_*/
⑧ its board      DOES NOT EXIST                  ← the ask
```
Seven exist and the eighth is the question. Every other THING on this grid has a board that
argues its rules; a task-group has a `diagram/` folder of static `.txt` files, specified as
mandatory for cohesive groups, present on 5 of 67. `QA6` measures that and `QA7` proposes what
replaces it.

### We are the bank, so the wall is drawn from the other side
`⑤` appears on this grid and we do not own it, do not call it, and do not rule it. That is
deliberate and it is the single most important line here. The probe layer belongs to the
CONSUMER: a paper or an application uses it to reach a question across to us. From where we
stand, the entire mechanism reduces to one verb, `qa`, which takes a question in general language
and returns a path.

What this buys is worth stating plainly. Because we never learn who asked, an answer written for
one question is worth the same to the next one. A task that shaped its output around a claim id
would produce evidence with a single customer. `QA5` is the page that holds this and `QA8@probe`
is where the same rule is written from the consumer's side.

### What this board may rule, and what it may only consult
We rule `①`, `②`, `⑦` and `⑧`. We consult `③`, `④`, `⑤` and `⑥` and write nothing into them.

The distinction matters most for `③`. This board is about to rule that `/haipipe-task` CALLS
`/haipipe-board` (`QA4`), which is a ruling about OUR skill's behaviour, not about the tool. The
tool's format, its filename rule, its build and its write-back are `④`'s, and a page here that
starts specifying what a board IS has crossed into a folder we do not own.

## Aims
- [ ] 🗺 Settle the seven-folder map itself
      That these are the folders, that `⑤` is consulted and never called, and that `⑧` is the empty cell this board exists to fill.
- [ ] 🚪 Rule the one door in and the one door out
      In: the `qa` verb, one question, one path. Out: the QA digest and nothing else. Both are stated in `SKILL.md` today and neither is checkable.
- [ ] 🧱 State the forbidden crossings so a machine could check them
      "No consumer vocabulary anywhere under `tasks/`" is the strongest of them and it is a grep. Nothing runs that grep.
- [ ] 🔗 Point at the two boards we consult without restating them
      `QA8@paper` owns the shared-page seam; `QC1@probe` owns the QA state line. A copy here would drift within the week.

## Files
- `SKILL.md`
  The router, and the current statement of the one door in and the one door out.
- `DESIGN.md`
  The layering: executors versus consumers, and which family owns which folder.
- `hierarchy.md`
  Project, task-group, task-folder, run. The conceptual model `SKILL.md` tells you to read first.

## Discussion
> CC 260726: the grid is deliberately the same shape as `QA1@paper` so the two can be read side by side, but one row means the opposite thing. There, `⑤` is a door the paper goes OUT through and the paper skill owns neither channel. Here, `⑤` is a door a consumer comes IN through, and we own neither of the two shared skills either. The symmetry is real; the direction is inverted, and a reader who carries the paper board's reading across will get the probe row exactly backwards.


### From the retired States section (merged 260831)
The map is drawn and nothing is ruled. Seven folders exist on disk with the counts above, and the
eighth cell is genuinely empty: no task-group anywhere carries a board.
- 260726 CC · 🗺 Board opened, map drawn
      Written from `SKILL.md`, `DESIGN.md` and `ref/hierarchy.md`, with the folder counts measured on disk rather than taken from the docs. The docs and the disk disagree in one place worth noting here: `ref/task-structure.md` calls a group-level `diagram/` mandatory for cohesive groups, and 5 of 67 groups have one.

## Log
260816 · The board took the two shape rules the Board family had landed. The group folders now carry their place in `## Pages` as a leading number, `1-` through `5-QE-shipping-the-skill`, so the folder listing and the board read in one order. Then every page took a folder of its own, `1-QA-where-things-live/QA1-the-map/QA1-the-map.md`, the shape ruled on 260815, which is what gives a page's drawing, deck or export somewhere to live. Both moves were made by `cli/refold.py` and its sibling in the Board engine, and the check came back with nothing new: same 19 pages, no new error, no new warning. Alongside it every dead link was repaired: the paper design board had been renamed and folded, and the probe design board retired on 260804, so its ids now point at `haipipe-probe`, which carries those rulings.
260726 · Created with the board.

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0