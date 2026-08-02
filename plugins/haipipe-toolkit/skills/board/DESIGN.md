# Board design

## Ownership

```text
board/                         first-class product family
board/haipipe-board/           callable skill and runtime
board/agents/                  clean-context roles shared by the family
diagrams/01-boardform-260722/  design record and unsettled rulings
```

The skill contains only executable instructions, stable specifications, code,
and assets. The design Board stays outside it because a working record changes
daily while a skill is a deliverable package.

## Writer and reviewer

```text
current session / Board skill
        │
        │ writes and rebuilds
        ▼
   Board on disk
        │
        │ fresh context, read-only
        ▼
haipipe-board-reviewer-agent
        │
        └── pass | revise | blocked
```

The writer owns fixes. The reviewer owns judgment and cannot edit the files it
reviews. Session attachment and automatic write-back remain responsibilities of
the main Board skill because they require the current conversation's context.
That attachment is visible, not merely internal: every reply ends with a
read-only strip derived from `board.md` and the focused page. Live mode and next
action stay in the transcript; durable decisions, comments, and logs stay in
the Board files.

## Knowledge homes

- Operational workflow: `haipipe-board/SKILL.md`
- Source and rendering grammar: `haipipe-board/ref/board-form.md`
- Readability standard: `haipipe-board/ref/writing-rules.md`
- Page template: `haipipe-board/ref/page-template.md`
- Settled and unsettled design history: `../diagrams/01-boardform-260722/`
