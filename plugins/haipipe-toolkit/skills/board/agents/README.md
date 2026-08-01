board: Agent Roster
====================

The Board family owns one live agent:
`haipipe-board-reviewer-agent`, a read-only, zero-background reviewer.

The main session and `haipipe-board` skill are the writers. They identify the
attached Board or page, make the change, synchronize the markdown, and rebuild
the HTML. The reviewer starts afterward in a fresh context, judges the result,
and returns findings. Builder and judge never share the pen.

Dispatch
--------

```text
current session / haipipe-board
        │
        │ substantive Board revision is written and rebuilt
        ▼
Agent(haipipe-board-reviewer-agent)
        ├── run the mechanical checker
        ├── cold-read the changed pages in Board context
        ├── identify stale or contradictory claims
        └── return pass | revise | blocked
                    │
                    ▼
          the original writer fixes
```

There is no Board orchestrator: `haipipe-board` already routes Board actions.
There is no sync agent: synchronization needs the current conversation's
context and remains with its writer. A proposer agent may be added only after
the page-and-group proposal rules are settled and forward-tested.

Knowledge home
--------------

Agents are thin. Rules live in:

```text
Board operations and synchronization  → ../haipipe-board/SKILL.md
Board source and rendering grammar    → ../haipipe-board/ref/board-form.md
Cold-read rules and prompt            → ../haipipe-board/ref/writing-rules.md
Mechanical checks                     → ../haipipe-board/check.py
Design rulings                        → ../../diagrams/01-boardform-260722/
```

Registration
------------

Agent source definitions live in this folder. Claude's plugin convention only
discovers top-level `agents/*.md`, so
`../../../agents/haipipe-board-reviewer-agent.md` is a symlink to this source.
The workspace's `.claude/agents/` uses the same pattern for immediate local
dispatch. The `name:` frontmatter supplies the callable agent type after
discovery.
