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

## Interactive writer and reviewer

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

## Automatic one-Page RUN

```text
page-orchestrator-agent
        │
        ├── creator-agent · one DRAFT / PROBE / REVISE authority
        ├── mechanical builder · rebuild + source/render version
        └── reviewer-agent · fresh read-only CHECK + route
                    │
                    └── CLOSE | REVISE | PROBE | DRAFT | HOLD
                                      ↺ bounded
```

The Page contract owns the packet and receipt. The Board engine owns the
Workflow and deterministic receipt auditor. The orchestrator owns only routing
and storage under `_runs/page/`; it cannot write Page prose or convert a missing
human gate into approval. `RUN` is not `ADVANCE`, because routes can repeat,
branch, hold, or begin a new DRAFT round.

## Knowledge homes

- Operational workflow: `haipipe-board/SKILL.md`
- Source and rendering grammar: `haipipe-board/ref/board-form.md`
- Readability standard: `haipipe-board/ref/writing-rules.md`
- Page template: `haipipe-board/ref/page-template.md`
- Page RUN contract: `haipipe-board-page/ref/page-run-contract.md`
- Page RUN engine: `haipipe-board/ref/page-lifecycle.workflow.js`
- Page RUN audit: `haipipe-board/src/page_lifecycle.py`
- Phase-scoped Related Board Page context: `haipipe-board/src/page_context.py`
  and `haipipe-board/cli/pagecontext.py`
- Settled and unsettled design history: `../diagrams/01-boardform-260722/`
