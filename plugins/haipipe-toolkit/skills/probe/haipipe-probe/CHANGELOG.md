haipipe-probe — Changelog
=========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [3.1.0] — 2026-06-19

- sandwich lifecycle around discoveries/tasks.

## [3.3.0] — 2026-06-21

- delivery-need inputs from paper/application and verdict backfill.

## [4.0.0] — 2026-06-22

- reframe probe around Probe Console and the concise lifecycle Plan/Gather/Read/Judge/Deposit; flat probe folders; group folders removed.

## [4.0.1] — 2026-06-22

- rename lifecycle step Return -> Deposit (settle the judged verdict into durable memory); legacy command alias return kept; Read reframed as a present-and-internalize stop; Gather-done = participating tasks/discoveries have run, closed by a participant manifest.

## [4.1.0] — 2026-06-22

- source-type letter in the probe ref. P.D<MMDD> discovery-sourced, P.T<MMDD> task-sourced (other source.type derives the letter from the primary evidence_plan kind). Folder becomes probes/<LETTER><MMDD>_<slug>/. Resolver accepts lettered + legacy letterless refs; existing letterless probes migrate lazily. See ref/probe-yaml-schema.md.

## [4.2.0] — 2026-06-22

- completed the Return->Deposit rename (artifact deposit.md, fn/deposit.md, probe.yaml deposit:/status: deposited/deposited_at/deposit_target; stage-strip predicate + accepts deposited|returned|closed). LEAN-ATOM MODE: a leaf probe declaring parent: logs Read/Judge/Deposit as yaml blocks (result:/verdict:/deposit:) and the strip reads them (yaml is disk). Deposit step now ALWAYS proposes the /haipipe-insight review handoff in next: (loop no longer implicit).

## [4.3.0] — 2026-06-23

- feedback-driven revision pass (14 items). (1) Plan: kind: field (atomic|comparison); comparison arms must be atom: links. (2) Gather: link+extract lightweight variant; fan-out model (1 probe : N discoveries : N tasks); naming rule (topic not verb); done-predicate strengthened (actual items, not evidence_plan); participant roster at Gather->Read boundary. (3) Read: elevated to stop-and-internalize gate (most participatory step); verdict-language ban in evidence.md. (4) Deposit: output readability template. (5) stage-strip.sh: fixed Gather false-positive (evidence_plan was Plan artifact, not Gather). (6) Dashboard: no-args view trimmed to compact glance. (7) Orchestrator agent: Write/Edit removed from tools (structural anti-monolith enforcement); dispatch prompts use coordinator language. (8) probe-yaml-schema: kind field, deposited status, deposit block heading.

## [5.0.0] — 2026-07-02

- added mode: full|light. Light probes stop at Read (no Judge, no Deposit, no insight cards). Escalation from light to full supported. Section-edit gather workers (citation, values, display) route evidence needs through light probes. Added Connection to Section-Edit section. Unwrapped hard-wrapped lines.

## [5.0.1] — 2026-07-03

- paper phase renamed GATHER->PROBE; paper-side worker names updated (haipipe-paper-probe-{citation,values,display}).
