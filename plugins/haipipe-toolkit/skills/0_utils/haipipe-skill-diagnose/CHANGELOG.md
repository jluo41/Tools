haipipe-skill-diagnose — Changelog
===================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [1.2.0] — 2026-07-05

### Changed (JL: "你的comments，如果可以用diagram-ascii，就用这个来explain")

- Thread 例子 default form is now a DIAGRAM: drawable decisions (option A vs B, flow, before/after) get a compact emoji-rich ASCII block inside the thread (each line `> `-prefixed); prose one-liners only when a diagram cannot carry the point. Other fields stay one line each. Applied live to the probe review's B1/C1/D2 threads (both copies).


## [1.1.0] — 2026-07-05

### Changed (JL: "我觉得这个comment 必须要先生成好")

- [J] threads now open at REPORT time (Phase 3), delivered together with SKILLSET_REVIEW.md, so the user answers judgment questions in the same pass as the report eyeball instead of waiting for FIX. Each finding records its thread's path:line; the chat announcement links report + every open thread. Opening a thread is a question, not a fix; the 改前必报 gate is unchanged. First applied live on the probe-bucket review (threads B1/C1/D2).
- Threads are additionally MIRRORED in full under their findings in SKILLSET_REVIEW.md (JL: "我在哪里加入我的comments呀" - he reads the report, not the target files); either copy's > JL: slot counts, first reply wins, RESOLVE removes both copies together.


## [1.0.0] — 2026-07-05

### Added (JL: "你觉得我们的evaluation可以不可以成为一个新的skill 比如 haipipe-skill-diagnose" / "可以放到 .../skills/0_utils" / "很好，你现在建立吧")

- Initial skill, codifying the workflow proven on the discovery-set review (v2.6.0 round) and the task-set review (95+ findings, 44 skills, Tools 84d14bd): 6 phases SCOPE → DIAGNOSE → REPORT (eyeball gate) → FIX → RESOLVE → COMMIT (zero-thread gate).
- ref/finding-taxonomy.md: 4 root-cause classes (搬家没改地址 / 路由层失真 / 内部矛盾 / 层间耦合), severity 🔴🟡🟢, [M]/[J], finding line format, arbitration evidence order.
- ref/thread-protocol.md: the `> {CC->JL}:` judgment-point comment format with MANDATORY worked example per thread (JL 2026-07-05: "inline 的你的每个comments 都很难understand，try to provide more information and examples"), before/after quotes, plain-language no-shorthand rule, lifecycle (reply → execute → archive verbatim to CHANGELOG → remove thread), SUPERSEDED-banner rule for owner-overruled LESSONs, diagram-ascii escalation on confusion, clickable bare path:line eyeball lists.
