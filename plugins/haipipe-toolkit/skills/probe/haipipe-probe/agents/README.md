probe - Agent Roster
======================

probe owns **3 reviewer agents**, all firing in the **Judge** step. They exist
for one reason: independent review (builder != judge). The probe's planner never
grades its own claim.

```
agents/reviewers/
├── probe-structural-reviewer-agent   Judge gate 1: is the comparison apples-to-apples?
├── probe-integrity-auditor-agent     Judge gate 2: is the setup honest? (Codex, paths-only)
└── claim-verifier-agent              Judge gate 3: does evidence support the claim? (Codex)
```

Order, run by `fn/judge.md`: structural → integrity → claim.
`integrity = fail` blocks `claim`. Integrity and claim are Codex-backed and
out-of-family: the executor passes only file paths; Codex reads and rules.

```
deliverables:
  structural → verdict.md (structural section) + probe.yaml.verdict.structural
  integrity  → INTEGRITY_AUDIT.md + probe.yaml.verdict.integrity
  claim      → CLAIMS_FROM_RESULTS.md + probe.yaml.verdict (status/confidence/scope)
```

Retired in v4 (no firing path in the Plan→Gather→Read→Judge→Return lifecycle):
`probe-idea-creator` / `probe-idea-reviewer` (Plan is interactive - its Gate
absorbs falsifiable/not-duplicate/worth-it) and `probe-explorer` (the `explore`
command was dropped; the dashboard's UNLINKED EVIDENCE surfaces gaps).

Knowledge home
--------------

Agents are THIN pointers - the judgment logic lives in its canonical home, not
duplicated here:

```
judge steps + gates       → ../fn/judge.md
confound walk             → ../ref/probe-caveats-checklist.txt
probe.yaml verdict schema → ../ref/probe-yaml-schema.md
```

Registration
------------

Real files live here; the plugin top-level `agents/` holds flat symlinks so each
is callable as a `subagent_type`. The nested folder is for humans; the top-level
symlinks are for the harness. (Symlinks point at `../skills/probe/...`.)
