haipipe-probe — Changelog
=========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [6.1.0] — 2026-07-05

Added (JL: "We might still need a haipipe-probe, but we don't need a standalone probes folder")
- DIRECT ASK front door restored: `/haipipe-probe "<question|claim>" [light|full]` runs ad-hoc evidence work outside any stage — gateway dispatch (bg), evidence lands in discoveries/tasks, anchored takeaways return in chat (user = consumer, reply = receipt). No folder, no card, no console state. Later paper use = PPNN card with refs to the already-landed artifacts (pure REUSE).

## [6.0.0] — 2026-07-05

Changed (FOLDERLESS REFACTOR — see ../CHANGELOG.md 5.0.0 for the layer rollup)
- SKILL.md rewritten thin: layer contract + PPNN card anatomy; Probe Console, probes/ folders, probe.yaml/evidence.md/verdict.md retired; fn/ + ref/ marked LEGACY.

## [5.2.0] — 2026-07-05

- SKILL.md slimmed 481 → 286 lines (JL: "这个怎么这么长，是不是有很多重复的地方"): feedback/digest rules were stated 4 times (Commands, Skill Procedures, Routing 1b/1c, Feedback section) and are now one-liners pointing at fn/feedback.md + fn/digest.md, the single source of truth; Gather detail (Call/Link/Extract/DONE, fan-out, naming) deferred to fn/gather.md; Boundaries merged into the header; full/light chains stated once; Copilot policy and stage-strip prose compressed. No rule was deleted, only duplicates; every cut has its canonical body in fn/ or ref/.
- Formatting: one sentence per line, no manual line wrapping (JL: "一句话一行 不要break lines").

## [5.1.0] — 2026-07-05

- Legacy verbs removed entirely (owner decision, JL: "我们就用一个gather得了，把legacy去掉好了。"): the legacy-alias table is deleted from SKILL.md and ref/lifecycle-map.md; design/bridge/dispatch/harvest/post/resume/review/file/return no longer route; scattered-work filing goes through `gather` (link path applies ref/probe-attach.md); probe-attach front door and the dashboard nag line reworded from `/haipipe-probe file` to gather. Old probe.yaml DATA stays compatible (status: returned etc. still accepted by the stage strip).
- Skill-set review round (SKILLSET_REVIEW.md): fn/judge.md rewritten off the 3 retired reviewer agents onto haipipe-probe-reviewer-agent G1/G2/G3 with deterministic fn/g2_integrity_check.py for G2 and the caveats-checklist pointer (A1); allowed-tools Task → Agent in SKILL.md, fn/judge.md, fn/gather.md (A8); letter convention P.<LETTER><MMDD> added to fn/plan.md (id: field + write paths), fn/gather.md, ref/probe-attach.md scaffold, SKILL.md layout (A7); lifecycle-map Judge external calls updated off Codex (A4); dashboard shallow-check `return` → `deposit` and schema "called by Return" → Deposit (A6); fn/deposit.md target path corrected to source.deposit_target (C3); false "auto-invoked by haipipe-data/haipipe-discovery" claims removed from ref/probe-attach.md, lower layers are probe-UNAWARE by design (D1); argument-hint extended with utility verbs (B2).

## [5.0.1] — 2026-07-03

- paper phase renamed GATHER->PROBE; paper-side worker names updated (haipipe-paper-probe-{citation,values,display}).

## [5.0.0] — 2026-07-02

- added mode: full|light. Light probes stop at Read (no Judge, no Deposit, no insight cards). Escalation from light to full supported. Section-edit gather workers (citation, values, display) route evidence needs through light probes. Added Connection to Section-Edit section. Unwrapped hard-wrapped lines.

## [4.3.0] — 2026-06-23

- feedback-driven revision pass (14 items). (1) Plan: kind: field (atomic|comparison); comparison arms must be atom: links. (2) Gather: link+extract lightweight variant; fan-out model (1 probe : N discoveries : N tasks); naming rule (topic not verb); done-predicate strengthened (actual items, not evidence_plan); participant roster at Gather->Read boundary. (3) Read: elevated to stop-and-internalize gate (most participatory step); verdict-language ban in evidence.md. (4) Deposit: output readability template. (5) stage-strip.sh: fixed Gather false-positive (evidence_plan was Plan artifact, not Gather). (6) Dashboard: no-args view trimmed to compact glance. (7) Orchestrator agent: Write/Edit removed from tools (structural anti-monolith enforcement); dispatch prompts use coordinator language. (8) probe-yaml-schema: kind field, deposited status, deposit block heading.

## [4.2.0] — 2026-06-22

- completed the Return->Deposit rename (artifact deposit.md, fn/deposit.md, probe.yaml deposit:/status: deposited/deposited_at/deposit_target; stage-strip predicate + accepts deposited|returned|closed). LEAN-ATOM MODE: a leaf probe declaring parent: logs Read/Judge/Deposit as yaml blocks (result:/verdict:/deposit:) and the strip reads them (yaml is disk). Deposit step now ALWAYS proposes the /haipipe-insight review handoff in next: (loop no longer implicit).

## [4.1.0] — 2026-06-22

- source-type letter in the probe ref. P.D<MMDD> discovery-sourced, P.T<MMDD> task-sourced (other source.type derives the letter from the primary evidence_plan kind). Folder becomes probes/<LETTER><MMDD>_<slug>/. Resolver accepts lettered + legacy letterless refs; existing letterless probes migrate lazily. See ref/probe-yaml-schema.md.

## [4.0.1] — 2026-06-22

- rename lifecycle step Return -> Deposit (settle the judged verdict into durable memory); legacy command alias return kept; Read reframed as a present-and-internalize stop; Gather-done = participating tasks/discoveries have run, closed by a participant manifest.

## [4.0.0] — 2026-06-22

- reframe probe around Probe Console and the concise lifecycle Plan/Gather/Read/Judge/Deposit; flat probe folders; group folders removed.

## [3.3.0] — 2026-06-21

- delivery-need inputs from paper/application and verdict backfill.

## [3.1.0] — 2026-06-19

- sandwich lifecycle around discoveries/tasks.
