probe — Agent Roster
======================

probe has **three agent families**: creators, reviewers, and advancers.

The Design stage has TWO modes, which drives the creator family:

```
Mode A (interactive, default round 1):  human writes probe.yaml — NO agents in Design
Mode B (auto, round ≥2 or --auto):     idea-creator generates → idea-reviewer checks
```

The first probe in a research direction needs human judgment (framing the question).
Follow-up probes (fill a coverage gap, confirm single-seed, test the opposite direction)
can be automated — the explore agent already does 80% of the design work; the creator
just formalizes its proposal into a valid probe.yaml.


creators/ (1 — Design Mode B only)
------------------------------------

| Agent | Fires in | Input | Output | Does NOT do (→ who) |
|-------|----------|-------|--------|---------------------|
| `probe-idea-creator-agent` | Mode B only | explore proposals, existing probes, insights K/W, project goal | probe.yaml with hypothesis + arms + spec | review the idea (→ idea-reviewer); bridge (→ bridge skill); judge (→ reviewers) |


reviewers/ (4 — gate probes at two stages)
---------------------------------------------

| Agent | Gate | Stage | Reviewer | Sole deliverable | Does NOT do (→ who) |
|-------|------|-------|----------|------------------|---------------------|
| `probe-idea-reviewer-agent`        | idea QA     | Design (Mode B) | self (5 criteria) | pass/revise/fail | create ideas (→ idea-creator); structural/integrity/claim (→ other reviewers) |
| `probe-structural-reviewer-agent`  | structural  | Harvest + Judge | self (checklist)   | `review.md` | per-run (→ task auditor); fraud (→ integrity); claim (→ verifier) |
| `probe-integrity-auditor-agent`    | integrity   | Judge           | **Codex** (out-of-family) | `INTEGRITY_AUDIT.md` | structural; claim |
| `claim-verifier-agent`             | claim       | Judge           | **Codex** (out-of-family) | `CLAIMS_FROM_RESULTS.md` | author the claim (→ result skill); structural; integrity |

Idea-reviewer fires in Design Mode B. The other 3 fire in Judge stage,
order: structural → integrity → claim. `integrity = fail` blocks `claim`.
Integrity & claim are Codex-backed — the probe's builder never judges its own
work (the executor passes only file paths; Codex reads and rules).


advancers/ (1 — probe's unique third family)
------------------------------------------------

| Agent | Step | Sole deliverable | Does NOT do (→ who) |
|-------|------|------------------|---------------------|
| `probe-explorer-agent` | coverage + propose next | ranked next-probe list + coverage map | write probe.yaml (→ design skill / idea-creator); judge claims (→ reviewers) |


Three families, one axis each
-------------------------------

```
creator   agents CREATE probe ideas          idea-creator (Design Mode B only)
reviewer  agents JUDGE                       idea-reviewer · structural · integrity · claim
advancer  agents PROPOSE direction           explore
```


Stage 5 (Insight) borrows insight agents
---------------------------------------------

The Insight stage uses 9 agents from insight (not owned by probe):

```
insight/agents/
├── creators/   card-creator-{data,information,knowledge,wisdom}-agent    (4)
├── reviewers/  card-reviewer-{data,information,knowledge,wisdom}-agent   (4)
└──             index-integrity-auditor-agent                             (1)
```

Total in a full lifecycle run: 6 own + 9 borrowed = 15 agents.


Knowledge home
--------------

Agents are THIN pointers — the judgment logic stays in its canonical home and
is NOT duplicated here:
- per-probe checklist + caveats + Codex prompts → `../haipipe-probe-review/SKILL.md`
- confound walk → `../ref/probe-caveats-checklist.txt`
- probe.yaml schema → `../ref/probe-yaml-schema.md`
- coverage/propose logic → `../haipipe-probe-explore/SKILL.md`
- idea quality criteria → `probe-idea-reviewer-agent.md` (self-contained — 5 criteria)


Registration & invocation
--------------------------

Real files live here; the plugin top-level `agents/` holds flat symlinks so
each is callable as a `subagent_type` (used by `probe-lifecycle.workflow.js`
and by `application` when a session needs an independent verdict). Like
task, the nested folders are for humans; the top-level symlinks are for
the harness.
