# board

`board/` is the first-class HAI-Pipe family for turning one topic into a
reviewable set of question pages or lifecycle stages.

## Entry points

- `haipipe-board/` is the callable skill and owns the Board format, actions,
  renderer, local service, write-back, checks, and the reply-ending session
  status strip.
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
│   └── haipipe-board-reviewer-agent.md
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
