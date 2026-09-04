---
name: inlab-human
description: "In-lab human interaction with deployed prediction endpoints — the Claude Code chat is the UI. Tier-1 orchestrator with two modes: CONSOLE (default; patient-first on-demand inference: pick patient → see chart → list models → predict via the endpoint-predict tool → analyze) and STUDY (formal reader protocol: bundle → blind/assisted review → decision-influence report). Endpoint-agnostic: local Flask, Databricks, SageMaker — same wire contract. Trigger: inlab, console, get patient, run prediction, clinician eval, reader study, /inlab-human."
argument-hint: "[console|patient|models|predict | bundle|review|report | status] [args...]"
allowed-tools: Bash, Read, Write, Grep, Glob, Skill
metadata:
  version: "0.2.0"
  last_updated: "2026-07-10"
---

Skill: inlab-human (in-lab human evaluation, tier-1)
=====================================================

Two modes, one plugin:

```
CONSOLE (default)  clinician DRIVES: patient → chart → models → on-demand
                   prediction → analysis.        -> /inlab-human-console
STUDY              clinician is MEASURED: frozen bundle → blind→assisted
                   reading → influence metrics.  -> bundle / review / report
```

```
/inlab-human                                 -> console (orient: patients + models)
/inlab-human <patient_id> [model]            -> console (jump straight in)
/inlab-human console | patient | models | predict ...   -> console verbs
/inlab-human status                          -> dashboard: patients, models(live?),
                                                bundles, responses
/inlab-human bundle <endpoint_path> [...]    -> /inlab-human-bundle  (study: freeze cases)
/inlab-human review <bundle.json>            -> /inlab-human-review  (study: run session)
/inlab-human report <bundle.json>            -> /inlab-human-report  (study: metrics)
```

Routing
-------

```
Step 1: parse $ARGUMENTS.
Step 2: verb -> dispatch:
  (nothing) | console | patient | models | predict | a patient id
          -> Skill inlab-human-console   (DEFAULT — on-demand inference)
  bundle  -> Skill inlab-human-bundle    (needs: endpoint path or live URL)
  review  -> Skill inlab-human-review    (needs: a frozen review_bundle.json)
  report  -> Skill inlab-human-report    (needs: bundle + responses.jsonl)
  status  -> dashboard: list_patients + list_models (via endpoint-predict
             tools or CLI twin) + scan for review_bundle*.json /
             responses*.jsonl; suggest the next verb.
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
