board: Agent Roster
====================

The Board family owns a producer base, an approver, a reviewer, an auditor,
and (under `../page-workflows/agents/`) one agent per lifecycle phase:

```text
haipipe-page-creator-agent      producer BASE + the two non-phase verbs
                                (create-page, revise-opening); dispatch fallback
haipipe-page-approver-agent     rule-bound machine ticks against approve-rules/
haipipe-board-reviewer-agent    fresh read-only board review; base of the judge
haipipe-page-auditor-agent      packet builder + receipt keeper, NOT a dispatcher
../page-workflows/agents/       ①-⑥ one producer per phase (outline, probe,
                                evidence, draft, revise+compile) and
                                ⑦ haipipe-page-check-agent, the judge
```

The main session and `haipipe-board` remain the interactive writers. They
identify the attached Board or Page, make known changes, synchronize Markdown,
and rebuild HTML. The reviewer starts afterward in a fresh context. Producer
and judge never share the pen.

Dispatch
--------

```text
interactive one-off                  automatic one-Page RUN
current session / haipipe-board      MAIN session invokes the Workflow;
        │                            auditor-agent validates the packet before,
        │ writes known change        stores + audits the receipt after
        ▼                                      │
reviewer-agent: board review                   ├── producer: one phase agent per
        │                                      │   phase (PRODUCER_AGENTS map;
        └── original writer fixes              │   creator-agent = fallback)
                                               ├── builder: snapshot version
                                               ├── judge: haipipe-page-check-agent
                                               └── _runs receipt + audit
                                                          ↺ bounded
```

The RUN lane is narrower than the Board door. It drives one already
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
Page RUN packet and receipt           → ../page-workflows/haipipe-page-workflow/ref/page-run-contract.md
Page RUN Workflow                     → ../haipipe-board/ref/page-lifecycle.workflow.js
Lifecycle receipt audit               → ../haipipe-board/cli/pageflow.py
Design rulings                        → ../../diagrams/BoardSkillBoard-260722/
```

Registration
------------

Agent source definitions live in this folder and in
`../page-workflows/agents/`. Claude's plugin convention only discovers
top-level `agents/*.md`, so each live agent has a symlink under
`../../../agents/` to its source. As of 260819 the symlinked roster is:

```text
haipipe-board-reviewer-agent    haipipe-page-approver-agent
haipipe-page-auditor-agent      haipipe-page-creator-agent
haipipe-page-outline-agent      haipipe-page-probe-agent
haipipe-page-evidence-agent     haipipe-page-draft-agent
haipipe-page-revise-agent       haipipe-page-check-agent
(+ the task family's haipipe-task-creator-agent, haipipe-task-reviewer-agent)
```

Verify with `ls -la <toolkit>/agents/`: every entry must be an unbroken
symlink into `skills/`. The workspace's `~/.claude/agents/` uses the same
pattern for immediate local dispatch. The `name:` frontmatter supplies the
callable agent type after discovery — and only after: a type not registered
when the session started is dispatched through the stand-in rule in
`../page-workflows/agents/README.md`.
