# board

`board/` is the first-class HAI-Pipe family for turning one topic into a
reviewable set of question pages or lifecycle stages.

## Entry points

- `haipipe-board/` is the callable skill and owns the Board format, actions,
  renderer, local service, write-back, checks, and the reply-ending session
  status strip. It is the family's one DOOR.
- `haipipe-board-page/` is a loadable SPEC: what a page is, its six kinds over
  one base, its sections in their fixed order, and where a machine may write.
- `haipipe-board-page-for-venue/` is the loadable VARIANT of that base for
  `QBv<n>` venue pages, one per place a paper is submitted to. Its pages live on
  the paper board, and the board family maintains the contract, which is why it
  ships here.
- `haipipe-board-page-for-skill/` is the loadable VARIANT of that base for the
  two skill and agent page kinds, `Skill-<n>` and `Agent-<n>`. A skill page mirrors a unit
  that ships elsewhere and decides nothing, so its Opening introduces the unit
  instead of asking a question.
- `haipipe-board-sentence/` is a loadable SPEC: the atomic unit, the `>` lanes,
  the evidence card, and the archive-never-delete record lifecycle.
- `haipipe-board-routing/` is the WRITE VERB, at both altitudes. Board and group:
  propose a board's structure before any file exists, materialize it after
  approval, and keep the per-group lane blocks current (`src/lanes.py`). Page:
  one input, find the owning page and section, append an anchored write. It
  proposes rather than creates, and it closes only the boxes you have already
  answered. (`haipipe-board-digest`, the transcript-scale fan-out, is named on
  the roster and not yet shipped.)
- `haipipe-board-index/` was retired on 260802 and merged into
  `haipipe-board-routing`: three of its five verbs were the door's own `open`,
  `regroup.py` and `check.py` written a second time, and its one unique script
  moved with it.
- `agents/haipipe-board-creator-agent.md` writes exactly ONE page in a fresh
  context, from an assignment packet rather than from the board, so N of them
  run at once instead of one context writing every page in turn. It holds no
  shared state: no `board.md`, no rebuild, no sibling page.
- `agents/haipipe-board-reviewer-agent.md` is the read-only, fresh-context
  reviewer. It checks structure, readability, and stale claims; it never repairs
  the Board it judges.

## Layout

```text
board/
├── README.md
├── DESIGN.md
├── CHANGELOG.md
├── agents/
│   ├── README.md
│   ├── CHANGELOG.md
│   ├── haipipe-board-creator-agent.md
│   └── haipipe-board-reviewer-agent.md
├── haipipe-board-page/
├── haipipe-board-page-for-skill/
├── haipipe-board-page-for-venue/
├── haipipe-board-sentence/
├── haipipe-board-routing/
│   └── src/lanes.py
└── haipipe-board/
    ├── SKILL.md
    ├── CHANGELOG.md
    ├── status.py        ← the ONLY script at the top level
    ├── cli/             ← every other runnable script lives here
    ├── src/
    ├── live/
    ├── ref/
    ├── assets/
    ├── checks/
    ├── tests/
    └── vendor/
```

The design Board remains a working artifact at
`../diagrams/01-boardform-260722/`. It does not ship inside the skill.

Every Board-attached session makes its attachment public at the end of each
reply: Board, page-group queue, board/group/page focus, work mode, next action,
and deep link. `status.py` derives a concise three-line block from Board files
and never writes a shared status ledger.
