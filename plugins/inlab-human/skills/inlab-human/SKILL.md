---
name: inlab-human
description: "In-lab human evaluation of a deployed prediction endpoint — the Claude Code chat is the reader UI. Tier-1 orchestrator: parses intent and dispatches to inlab-human-bundle (freeze cases+scores+narratives into review_bundle.json), inlab-human-review (blind→assisted clinician reading session → responses.jsonl), inlab-human-report (decision-influence metrics vs gold). Endpoint-agnostic: local Flask, Databricks, SageMaker — same wire contract. Trigger: inlab, in-lab eval, clinician eval, reader study, human evaluation, /inlab-human."
argument-hint: "[bundle|review|report|status] [args...]"
allowed-tools: Bash, Read, Write, Grep, Glob, Skill
metadata:
  version: "0.1.0"
  last_updated: "2026-07-10"
  summary: "Tier-1 orchestrator for in-lab clinician evaluation sessions."
---

Skill: inlab-human (in-lab human evaluation, tier-1)
=====================================================

One clinician + one Claude Code session + one frozen bundle = one reading
session. The skill family enforces what free-form chat would not: blinding
(raw data before model output), structured capture (every judgment → a
`responses.jsonl` row), and separate ratings for the score vs the explanation.

```
/inlab-human status                          -> what bundles/responses exist here
/inlab-human bundle <endpoint_path> [...]    -> /inlab-human-bundle  (freeze cases)
/inlab-human review <bundle.json>            -> /inlab-human-review  (run the session)
/inlab-human report <bundle.json>            -> /inlab-human-report  (metrics + figures)
```

Routing
-------

```
Step 1: parse $ARGUMENTS.
Step 2: verb -> dispatch:
  bundle  -> Skill inlab-human-bundle    (needs: endpoint path or live URL)
  review  -> Skill inlab-human-review    (needs: a frozen review_bundle.json)
  report  -> Skill inlab-human-report    (needs: bundle + responses.jsonl)
  status | no args -> scan cwd + study project for review_bundle*.json and
    responses*.jsonl; print a one-table dashboard (bundle id, n cases,
    n responses, readers) and suggest the next verb.
Step 3: relay the specialist's return contract verbatim.
```

Hard rules (enforced across the family)
----------------------------------------

1. **The score is never LLM-produced.** All scores come from the
   `endpoint-predict` tool (MCP server, or its CLI twin
   `mcp-servers/endpoint-predict/predict_cli.py` via Bash).
2. **Frozen bundle.** Reading sessions consume a static `review_bundle.json`;
   never call a live endpoint mid-session.
3. **gold is invisible** during a session. Only the report skill reads it.
4. **Study data lives with the study** (the project repo), never in this plugin.

Contracts: `../../ref/review-bundle-schema.md` · `../../ref/feedback-form.md`.

Return contract
---------------

```
status:    ok | blocked | failed
summary:   what was done / what the dashboard shows
artifacts: [paths]
next:      suggested next command
```
