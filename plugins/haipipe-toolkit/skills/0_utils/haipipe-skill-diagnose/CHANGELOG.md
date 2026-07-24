haipipe-skill-diagnose — Changelog
===================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.

## [0.1.3] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.3.0; older entries below keep their original numbers).

## [1.3.0] — 2026-07-19 — the review ledger moves to `_console/`

### Changed (JL: "haipipe-skill-diagnose/SKILL.md:46 please also change this, and make SKILLS to save things to a _console folder?")

- **The review no longer ships inside the bucket it reviews.** Phase 3 REPORT wrote `SKILLSET_REVIEW.md` at the bucket root, so a process artifact went out to every consumer of the reviewed skills and drifted the moment either side changed. It is now written to `skills/_console/<YYMMDD>-<slug>.md` — date = day of BIRTH, never re-dated; one file per TOPIC, later sessions APPEND. The folder's contract is `skills/_console/README.md` (new).
- Everything that pointed at the old location follows it: the [J] thread MIRROR target (Phase 3), RESOLVE's reply sweep (Phase 5 — the console file is now explicitly non-optional in the grep, since it is where the owner actually types), the COMMIT gate and `git add` scope (Phase 6 — bucket path PLUS the one console file this review owns), the `artifacts:` return contract, `ref/thread-protocol.md`, and `ref/finding-taxonomy.md`.
- New MUST NOT: never write the review ledger beside its subject.

### Changed (JL: "only add it or assign the new tags until we really have the final version, not everytime, we have a new tag")

- **Versioning is per BODY OF WORK, not per pass.** Phase 4 had said "Every fixed skill gets a version bump + CHANGELOG entry in the same pass", which fragmented a single multi-round review across several tags — the 260719 DRAFT round had already produced 5.0.2 and 5.1.0 on one skill, and three 1.0.1s on its lanes, before the ruling landed; all were collapsed back into one. The rule is now: one tag, assigned at the END, marked `⚠️ IN PROGRESS` and appended to while the round is open. The matching MUST NOT flipped from "no bump" to "fragmenting one round across several tags".
- Closed reviews predating this (`0_connect/`, `task/`, `task/1_data/`, `task/3_end/SKILLSET_REVIEW.md`) stay where they are — CHANGELOG entries cite those paths. Only new reviews go to `_console/`.

## [1.2.1] — 2026-07-14 — probe-redesign residue sweep

Fixed
- **The exemplar taught a dead command surface.** `ref/thread-protocol.md`'s "Good (option comparison, drawn)" example — the block a session copies when authoring a review thread — was built on `/haipipe-probe file "tasks/R02_…"` (there is no `file` verb; the verbs are contract | anatomy | status | "<question>"), on a first-hop read of `probe-attach.md` (no such file anywhere in the tree), and on a "gather link? 还是 plan?" router that died with the probe-folder era. Re-cut against a live decision: MATCH first (`/haipipe-task qa "<Q>" --check-only` → T2 REUSE, 1 grep + 1 read, zero agent) vs skipping MATCH straight to a T4 commission (a new leaf + full P-B-E-R — the unbudgeted-spend smell). The diagram FORM — side-by-side option boxes with real values — is the point of the doc and is unchanged.

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
