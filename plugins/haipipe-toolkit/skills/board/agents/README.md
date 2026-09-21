board: Agent Roster
====================

The Board family owns a producer base, an approver, a reviewer, an auditor,
and (under `../../page/page-workflows/agents/`) agents for the current controller dispatches:

```text
haipipe-page-creator-agent      producer BASE + two standalone verbs
                                (create-page, revise-opening); dispatch fallback
haipipe-page-approver-agent     rule-bound machine ticks against approve-rules/
haipipe-board-reviewer-agent    fresh read-only board review; base of the judge
haipipe-page-auditor-agent      packet builder + receipt keeper, NOT a dispatcher
../../page/page-workflows/agents/
                               00 context, 01 outline, 02 evidence,
                               03 content, and 04 check (the judge)
```

The main session and `haipipe-board` remain the interactive writers. They
identify the attached Board or Page, make known changes, synchronize Markdown,
and rebuild HTML. The reviewer starts afterward in a fresh context. Producer
and judge never share the pen.

Dispatch
--------

```text
interactive one-off                  automatic one-Page workflow pass
current session / haipipe-board      MAIN session invokes the Workflow;
        │                            auditor-agent validates the packet before,
        │ writes known change        stores + audits the receipt after
        ▼                                      │
reviewer-agent: board review                   ├── producer: one dispatch
        │                                      │   agent (PRODUCER_AGENTS map;
        └── original writer fixes              │   creator-agent = fallback)
                                               ├── builder: snapshot version
                                               ├── judge: haipipe-page-check-agent
                                               └── _runs receipt + audit
                                                          ↺ bounded
```

The workflow-pass lane is narrower than the Board door. The `RUN` verb drives one already
identified persistent Page and never proposes Board structure, registers a
Page, synchronizes a transcript, or edits `board.md`. Those actions still need
the current conversation's context and remain with `haipipe-board`.

The Workflow is a list of Runs, defined by its owner's Run Specs. Controller
coordinates (CONTEXT, OUTLINE, EVIDENCE, CONTENT, CHECK), snapshots, and dispatch
receipts do not independently add Runs. The Board's `_runs/page/` receipts
record a Workflow Runtime/pass; Page-owned `rp-struct-*`, `rp-sec-*`, `rp-para-*`,
and `rp-scratch-*` identities follow the canonical
[Page Run families](../../page/haipipe-page/ref/page-run-families.md).

Knowledge home
--------------

Agents are thin. Rules live in:

```text
Board operations and synchronization  → ../haipipe-board/SKILL.md
Board source and rendering grammar    → ../haipipe-board/ref/board-form.md
Cold-read rules and prompt            → ../haipipe-board/ref/writing-rules.md
Mechanical checks                     → ../haipipe-board/cli/check.py
Page workflow-pass packet + receipt  → ../../page/page-workflows/haipipe-page-workflow/ref/page-run-contract.md
Board-hosted pass adapter            → ../haipipe-board/ref/page-lifecycle.workflow.js
Lifecycle receipt audit               → ../haipipe-board/cli/pageflow.py
Design rulings                        → ../../diagrams/BoardSkillBoard-260722/
```

Registration
------------

Agent source definitions live in this folder and in
`../../page/page-workflows/agents/`. Claude's plugin convention only discovers
top-level `agents/*.md`, so each live agent has a symlink under
`../../../agents/` to its source. As of 260819 the symlinked roster is:

```text
haipipe-board-reviewer-agent    haipipe-page-approver-agent
haipipe-page-auditor-agent      haipipe-page-creator-agent
haipipe-page-context-agent      haipipe-page-outline-agent
haipipe-page-evidence-agent     haipipe-page-content-agent
haipipe-page-check-agent
(+ the task family's haipipe-task-creator-agent, haipipe-task-reviewer-agent)
```

Verify with `ls -la <toolkit>/agents/`: every entry must be an unbroken
symlink into `skills/`. The workspace's `~/.claude/agents/` uses the same
pattern for immediate local dispatch. The `name:` frontmatter supplies the
callable agent type after discovery — and only after: a type not registered
when the session started is dispatched through the stand-in rule in
`../../page/page-workflows/agents/README.md`.
