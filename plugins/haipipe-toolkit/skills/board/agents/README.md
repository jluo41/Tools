board: Agent Roster
====================

The Board family owns a producer, a reviewer, and a Page orchestrator:

```text
haipipe-board-creator-agent             one target Page; DRAFT/PROBE/REVISE
haipipe-board-reviewer-agent            fresh read-only CHECK
haipipe-page-orchestrator-agent   bounded router + durable audit receipt
```

The main session and `haipipe-board` remain the interactive writers. They
identify the attached Board or Page, make known changes, synchronize Markdown,
and rebuild HTML. The reviewer starts afterward in a fresh context. Producer
and judge never share the pen.

Dispatch
--------

```text
interactive one-off                  automatic one-Page RUN
current session / haipipe-board      page-orchestrator-agent
        │                                      │
        │ writes known change                  ├── creator: produce one phase
        ▼                                      ├── builder: snapshot version
reviewer-agent: CHECK                         ├── reviewer: CHECK and route
        │                                      └── _runs receipt + audit
        └── original writer fixes                         ↺ bounded
```

The Page orchestrator is narrower than the Board door. It runs one already
identified persistent Page and never proposes Board structure, registers a
Page, synchronizes a transcript, or edits `board.md`. Those actions still need
the current conversation's context and remain with `haipipe-board`.

Knowledge home
--------------

Agents are thin. Rules live in:

```text
Board operations and synchronization  → ../haipipe-board/SKILL.md
Board source and rendering grammar    → ../haipipe-board/ref/board-form.md
Cold-read rules and prompt            → ../haipipe-board/ref/writing-rules.md
Mechanical checks                     → ../haipipe-board/cli/check.py
Page RUN packet and receipt           → ../haipipe-page/ref/page-run-contract.md
Page RUN Workflow                     → ../haipipe-board/ref/page-lifecycle.workflow.js
Lifecycle receipt audit               → ../haipipe-board/cli/pageflow.py
Design rulings                        → ../../diagrams/01-boardform-260722/
```

Registration
------------

Agent source definitions live in this folder. Claude's plugin convention only
discovers top-level `agents/*.md`, so each live agent has a symlink under
`../../../agents/` to its source here. The workspace's `~/.claude/agents/` uses
the same pattern for immediate local dispatch. The `name:` frontmatter supplies
the callable agent type after discovery.
