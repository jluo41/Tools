# a-executor

Read from disk on 260819.

**Agent files in page-workflows/agents/: 6** (`ls`, minus README.md and CHANGELOG.md):

```
haipipe-page-outline-agent    ① OUTLINE   producer
haipipe-page-draft-agent      ④ DRAFT     producer
haipipe-page-probe-agent      ② PROBE     producer
haipipe-page-evidence-agent   ③ EVIDENCE  producer
haipipe-page-revise-agent     ⑤ REVISE    producer · also serves ⑥ COMPILE
haipipe-page-check-agent      ⑦ CHECK     judge, not a producer
```

**Phases with a producer agent of their own: 5** — OUTLINE, PROBE, EVIDENCE, DRAFT, REVISE.

**Phases lacking one: 2**, each on purpose, per the controller's PRODUCER_AGENTS table in `haipipe-board/ref/page-lifecycle.workflow.js`:
- COMPILE has no agent file; the table maps it to `haipipe-page-revise-agent`, because the fold is haipipe-page-revise's (0.5.0).
- CHECK is not in PRODUCER_AGENTS at all; the controller dispatches `haipipe-page-check-agent` as the JUDGE (workflow.js line 207), so no producer judges its own version.

**The fallback**: a phase with no PRODUCER_AGENTS row dispatches `haipipe-page-creator-agent` (workflow.js line 343), which lives in the support roster, not in page-workflows/agents/. A roster gap therefore degrades silently instead of erroring.

**Support agents in skills/board/agents/: 4** — haipipe-board-reviewer-agent (the base ⑦'s judge still reads), haipipe-page-approver-agent, haipipe-page-auditor-agent, haipipe-page-creator-agent. README.md, CHANGELOG.md and the approve-rules/ folder are not agents and are excluded.
