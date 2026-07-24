# Where a board lives
state: ✅ SETTLED
owner: JL
method: boards live under "<owning unit>/diagram/", apart from the skill itself; named number-topic-date

## Question
Where in the repo does a board's folder go, and how is it named?

- Why it is hard
  Boards serve all kinds of owners (a plugin, a task folder, a paper) — there is no single "all boards go here" place.
- What breaks if we leave it
  Boards will multiply and get assigned to RAs. Once locations and names drift, nothing can be found and no other document can point at a board reliably.
- What it affects downstream
  The relative paths in `## Links`, and the directory structure when boards are shared out later (`QE1`).

## Boundary
- ✅ This question owns
  **Where the folder goes and what it is named**: under whose name it hangs, how number and date are assigned.
- ❌ This question does not own
  What is **inside** the folder — that is `QA1`. Nor what the index page looks like — that is `QC2`.

## Diagram
```
skills/0_utils/
├── diagram/                    ← boards: working artifacts, change daily
│   └── 01-boardform-260722/
│         number  topic    date
└── haipipe-board/              ← the skill: the deliverable package
      SKILL.md  build.py  ref/

rule: <owning unit>/diagram/<NN>-<topic>-<YYMMDD>/
```

## Items to Finish
- [x] Decide where this board lives
- [x] Decide where the next board lives
- [x] Naming rule settled — the name alone identifies the board

## Where we are
JL has ruled: boards live under the **owning unit's `diagram/`**, apart from the skill itself. This board has already moved to
`Tools/plugins/haipipe-toolkit/skills/0_utils/diagram/01-boardform-260722/`.

```
skills/0_utils/
  diagram/                  ← boards live here (working artifacts, change daily)
    01-boardform-260722/
  haipipe-board/            ← the skill itself lives here (the deliverable package)
    SKILL.md  build.py  ref/
```

The rule solved something that had never been thought through: **a board is a working artifact, a skill is a deliverable package** — they do not belong in one folder.
This board used to sit inside `haipipe-board/diagram/`, which effectively shipped a daily-changing work log inside the skill.

The name stays `number-topic-date` (`01-boardform-260722`), number first, date last.

Two small non-blocking items, settled through use: whether the date is fixed at opening forever or refreshed on major changes; whether numbering restarts at 01 per `diagram/` or is repo-global.

## Files
- `ref/board-form.md`
  §1 folder — location and naming rules live there.
- `SKILL.md`
  The first line of the "🗂 Shape" section (owning unit = whom this board serves).

## Glossary
owning unit: the thing a board serves — a skill group, a task folder, a paper. The board lives in that thing's `diagram/`.

## Discussion
> JL: this board should be at `Tools/plugins/haipipe-toolkit/skills/0_utils/diagram`
>> CC0722: moved. `haipipe-board/` keeps only the skill itself (`build.py` + `ref/`). The rule is recorded in "Where we are" above.

## Log
260724 1242 · Translated to English (JL 260724: everything on the board in English)
260723 · Rewritten to the new structure: Question expanded into "one paragraph + bullets", added `## Boundary` and `## Files`; the retired `## Why here` merged into Question
260723 0919 · Renumbered Q7 → QC1; state → ✅ SETTLED, 3/3
260722 2249 · JL ruled: boards under the owning unit's diagram/, apart from the skill itself; this board moved on the spot
260722 2240 · Opened with a single hard requirement from JL: the name is "number-topic-date"
