# board

`board/` is the first-class HAI-Pipe family for turning one topic into a
reviewable set of question pages or lifecycle stages.

## Entry points

- `haipipe-board/` is the callable skill and owns the Board format, actions,
  renderer, local service, write-back, checks, and the reply-ending session
  status strip. It is the family's one DOOR.
- `haipipe-board-index/` owns the board + group altitude: proposing a board's
  structure before any file exists, and the per-group lane blocks (`lanes.py`).
- `haipipe-board-page/` is a loadable SPEC: what a page is, its three kinds over
  one base, the seven sections, and where a machine may write into one.
- `haipipe-board-sentence/` is a loadable SPEC: the atomic unit, the `>` lanes,
  the evidence card, and the archive-never-delete record lifecycle.
- `haipipe-board-routing/` is a VERB: one input, find the owning page and
  section, append an anchored write; it proposes rather than creates, and it
  never ticks a box. (`haipipe-board-digest`, the transcript-scale fan-out, is
  named on the roster and not yet shipped.)
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
├── haipipe-board-index/
├── haipipe-board-page/
├── haipipe-board-sentence/
├── haipipe-board-routing/
└── haipipe-board/
    ├── SKILL.md
    ├── CHANGELOG.md
    ├── ref/
    ├── assets/
    ├── src/
    ├── vendor/
    ├── build.py
    ├── check.py
    ├── serve.py
    ├── stage.py
    ├── status.py
    ├── watch.py
    └── xcal.py
```

The design Board remains a working artifact at
`../diagrams/01-boardform-260722/`. It does not ship inside the skill.

Every Board-attached session makes its attachment public at the end of each
reply: Board, page-group queue, board/group/page focus, work mode, next action,
and deep link. `status.py` derives a concise three-line block from Board files
and never writes a shared status ledger.
