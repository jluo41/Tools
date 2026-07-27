# ③ The HUMAN channel: /haipipe-board, called and never typed
state: 🔴 OPEN
owner: JL
method: one door in, /haipipe-task dispatches and /haipipe-board renders, and the tool stays generic

## Question
When a human enters a task-group, what do they SEE, and who puts it in front of them? Today they see a paragraph of text. Entering a paper now opens a live board in a browser. That is the same human on the same day getting a control plane for the manuscript and a printed summary for the work that produced it, and the asymmetry has no defence.

The gap is not cosmetic, because the two surfaces are not equivalent renderings of the same thing. A board carries `state:` per unit, a checklist that counts itself, a comment that lands on a sentence and is written back to disk, and a log. Printed text carries none of those, so anything a human notices while reading it has nowhere to go except a follow-up message. Work observed and not recorded is work done twice, and a group of a dozen task-folders is exactly the scale at which that starts to hurt.

JL ruled the shape on 260726: `/haipipe-task` is the single door, and `/haipipe-board` is CALLED rather than typed, exactly as `/haipipe-paper enter` now calls it. What is not yet ruled is the harder half. `/haipipe-paper` has an `enter` verb to hang this on and `/haipipe-task` has none: a bare path today means "run the full lifecycle on this", which is the most expensive thing the skill can do. So the door has to be named before it can be opened.

## Boundary
- ✅ Covered here
  What `/haipipe-board` is to this skill, when this skill calls it, what the call replaces, and what stays this skill's own.
- ↪ Covered elsewhere
  What a board IS, its face grammar, its live layer and its write-back are `④`'s, at `01-boardform-260722`, and this face may not rule any of them. What the board would be laid over is `QA7`. Who owns which REGION of a shared page is already ruled at `QA8@paper` and is inherited here, not re-argued. The same ruling on the paper side is `QA4@paper`.

## Diagram
```
   THE DOOR.   ruled 260726: ① is the single entry.

   TODAY                                  RULED
   ─────────────────────────────          ─────────────────────────────
   /haipipe-task <group>                  /haipipe-task <group>
        │                                      │
        ▼                                      ├─ ① resolve the group
   run the FULL LIFECYCLE                      ├─ ③ build.py  ⑧ → board.html
   on every child folder                       ├─ ③ serve.py  push the URL
        │                                      └─ ① print ONE line + the URL
        ▼                                             │
   the most expensive thing                            ▼
   the skill can do, from                     the human is LOOKING at ⑧
   the cheapest thing a
   human can type

   ⚠️ the bare path is ALREADY TAKEN, and by the worst possible verb.
      /haipipe-paper had an `enter` verb to hang this on. We have none.
      Naming the door is the open half of this ruling. → Items

```

```
   ── WHEN ① calls ③.  three moments, not one ──────────────────────

    1  ENTER            resolve the group → build → serve → URL
                        the human sees ⑧ before any work starts

    2  AFTER EVERY WRITE TO ⑧          ← the one a naive reading misses
                        a phase ends, a gate passes, a run finishes:
                        each rebuilds, or the human is reading a page
                        that describes a folder that has moved on

    3  BEFORE ① ACTS                   ← the reverse direction
                        a human comment or a > lane arrived through
                        serve.py, so ⑧'s markdown changed underneath us.
                        Re-read. Never cache.

      Point 2 is what makes this a design ruling rather than a
      convenience. "Entering opens a board" alone gives you a board
      that is correct for exactly as long as nobody works.

```

```
   ── why this does not make ③ ours ────────────────────────────────
      CALLING IS NOT OWNING.
        ③ owns the format, the build, the filename rule, the html,
          the write-back. ① renders nothing and never will.
        ① owns the ENTRY, and dispatches.

      /haipipe-board stays a real door for every board NOT laid over
      a task-group, including this one. It must not become task-aware.

   ── the risk this moves onto the critical path ───────────────────
      the URL reaches the human over the VS Code IPC socket, :5599.
      When that push fails the board does not appear, and after this
      ruling that is EVERY entry rather than an occasional one.
      The entry MUST print the URL and say the push failed. A silent
      success is indistinguishable from a dead port forward.
```

## Content
### The door has to be named, and every candidate costs something
```
 A  add `enter`        /haipipe-task enter <group>
      mirrors /haipipe-paper exactly. Costs a new verb on a skill
      whose Step 2 cascade already has eight branches.

 B  overload the path  /haipipe-task <group>       → opens the board
                       /haipipe-task run <group>   → the old behaviour
      cheapest to type and the biggest behaviour change: a path that
      today runs 12 folders would stop doing so. Anything scripted
      against it breaks silently, and it breaks by doing LESS, which
      is the failure mode nobody notices.

 C  a separate verb    /haipipe-task board <group>
      safest and weakest. It is another thing to know, so the human
      who most needs the board is the one least likely to type it.
```
`B` is what the ask literally describes and `A` is what the paper side did. The deciding
question is whether a bare group path running twelve lifecycles is a behaviour anyone relies on,
or an accident nobody has ever intentionally invoked. That is measurable and has not been
measured.

### What the board makes redundant
The entry today prints a summary, and `scan-status` prints a bigger one across a whole project.
Both are renderings of state that the board renders better, with one thing a terminal cannot
have: somewhere for a reaction to land.

What a terminal is genuinely good at survives, and it is short: the URL, one line naming the
frontier, and the next command. That is the same split the paper console settled on, and the
reason to keep it is not symmetry but failure: when the push fails, that line is all the human
gets, and it has to be enough to work from.

### Inherited, not re-argued
Two skills writing one markdown file without colliding is a solved problem, and it was solved on
the paper board at `QA8@paper`: `③` owns the filename, the face shell, the managed block and
every keystroke a human contributes through the live layer, while `①` owns Question, Boundary,
Content, Items to Finish and Where we are.

Nothing about that seam is task-specific, so this board inherits it whole. A page here that
restates it will drift from `QA8@paper` and then two boards will disagree about the same file.

## Items to Finish
- [ ] 🚪 Name the door
      Rule A, B or C above. Everything else on this page is blocked on it, because none of the three can be implemented halfway.
- [ ] 📏 Measure whether the bare path is load-bearing
      Option B is only cheap if nothing relies on a bare group path running every child. Grep the runs, the sbatch scripts and the shell history for it, and count. Until that number exists, B is a guess.
- [ ] 🔁 Rule all three sync points, not just the first
      Entry, after every write to `⑧`, and re-read before acting. A ruling that covers only entry ships a board that is correct until the first phase completes.
- [ ] 🔌 Make the transport failure loud
      Print the URL and say the push failed. Silent success and a dead port forward look identical from the terminal, and one session was already lost that way on 260725.
- [ ] ✂️ Decide what the terminal keeps
      The URL, one frontier line, the next command. Whether `scan-status` survives at project scope, where there is no single board to open, is a real question and not obviously yes.
- [ ] 🧪 Enter one real group and get a board
      The acceptance test for this face: a group on disk, one command, a board in the browser, no second command typed.

## Where we are
Nothing is built. `/haipipe-task` contains no reference to `/haipipe-board`, `board.html` or port
5599, so the two skills have never been connected in either direction.

The paper side is the working precedent rather than a plan: `haipipe-paper-enter` 0.5.0 already
resolves a paper, calls the board, pushes the URL and prints only what a terminal is good at. The
shape is proven; what is unproven here is where to hang it, because this skill has no `enter`.

- 260726 JL · 🚪 Ruled the shape
      `/haipipe-task` is the single door and `/haipipe-board` is a sub-skill it calls, not a command a human types for a group. The naming of the door was left open.

## Files
- `SKILL.md`
  Step 2's scope cascade, where a new verb would land, and the current meaning of a bare group path (branch 4).
- `paper-enter/`
  `haipipe-paper-enter` 0.5.0, the working precedent: resolve, call the board, push the URL, print one line.
- `haipipe-board/`
  The tool. Consulted, never modified from here.

## Law
`/haipipe-board` is CALLED by this skill and never typed by a human for a task-group. Calling is
not owning: the tool keeps the format, the build, the filename rule, the html and the write-back,
and this skill renders nothing.

`/haipipe-board` must stay generic. A task-specific behaviour belongs behind a declared seam in
the board's own dialect mechanism, never in the tool's core.

## Discussion
> JL 260726: I want to make the haipipe-task the same as haipipe-paper, that when we enter a task group folder, we will enter a board, so it will call /haipipe-board within the /haipipe-task.
> CC: recorded as the ruling. The half I could not settle from the ask is which command is the door, because this skill has no `enter` verb and its bare path already means the most expensive operation it offers. Three options are in Content with what each costs.

> CC 260726: worth stating that the second sync point is the one that decides whether this is worth doing. A board built only at entry is accurate until the first phase finishes writing, which on a twelve-folder group is a few minutes. If only entry is ruled, the honest description of what we shipped is a screenshot.

## Log
260726 · Created with the board, carrying JL's ruling on the entry shape.
