---
name: inlab-human-console
description: "The clinician-driven inference console — the default inlab-human mode. Patient-first flow in the Claude Code chat: pick a patient from the patient store, see their full chart, list the available prediction models (live Endpoint_Set endpoints), run 'this model on this patient' — the endpoint-predict tool prepares the payload, POSTs to the endpoint, returns the score — then analyze/explain the result. On-demand, interactive; no bundles, no blinding. Trigger: console, get patient, list models, run prediction for patient, /inlab-human-console."
argument-hint: "[patient_id] [model]"
allowed-tools: Bash, Read, Grep, Glob, Agent
metadata:
  version: "0.1.0"
  last_updated: "2026-07-10"
  summary: "Patient -> chart -> models -> on-demand prediction -> analysis."
---

Skill: inlab-human-console
===========================

The on-demand mode from the clinical-translation meeting: *"the doctor wants a
prediction for this patient."* The human drives; the tools answer.

```
👤 patient ──► 📋 full chart ──► 🧠 list models ──► ▶️ predict ──► 📊 analyze
                                                      │
                              endpoint-predict tool: prepare payload → POST → score
```

Tooling
-------

Use the `endpoint-predict` MCP tools when registered
(`mcp__endpoint-predict__*`); otherwise the CLI twin via Bash
(`mcp-servers/endpoint-predict/predict_cli.py`) or a python one-liner
importing `server.py`'s tool functions with the `INLAB_*` env vars set
(INLAB_PATIENT_STORE, INLAB_ENDPOINT_STORE, INLAB_REGISTRY).

| Step | Tool | Notes |
|---|---|---|
| who is available | `list_patients` | id + demographics + table counts |
| the patient's data | `get_patient` | ALL source tables; use `tables`/`max_rows` for huge charts (MIMIC) |
| what models exist | `list_models` | name, version, required tables, URL, **live?** |
| run it | `predict_for_patient` | prepares payload → POSTs → score + gaps + trigger info |
| payload only (inspect) | `prepare_payload` | show the clinician what would be sent |

Session flow
------------

```
1. ORIENT   No args? Show list_patients + list_models side by side.
            Dead endpoints: offer to start one (study project's
            A01 serve_endpoint.py) and re-check.

2. PATIENT  On selection, render the chart clinician-readable (tables:
            demographics · problem list · meds · vitals/labs ·
            questionnaires · visits). Big charts: summarize counts, offer
            table-by-table drill-down. NEVER show gold/outcome fields —
            the store is scrubbed, but say so if asked.

3. PREDICT  On "run <model>": predict_for_patient. Present:
            - the score + risk band, verbatim, prominently
            - the trigger (as-of date; offer obs_dt override = "predict as
              of an earlier visit")
            - the GAPS report honestly (missing/empty tables — especially
              cross-model runs, e.g. an ADHD-store patient on the PD2D
              model missing Pheno tables: say the model ran on partial data)

4. ANALYZE  On request: dispatch inlab-narrator-agent for a clinical
            narrative (it never sees outcomes, never re-derives the score);
            compare across models/patients; show what changed between two
            obs_dt runs. Deeper stats -> suggest a task in the study repo.

RULES
- Scores verbatim from the endpoint; the LLM never produces/edits a number.
- No care advice; this is an in-lab exploration tool on de-identified data.
- Every prediction shown = every gap shown. No silent partial-data runs.
```

Return contract
---------------

```
status:    ok | blocked | failed
summary:   patient(s) examined, predictions run (model -> score), gaps noted
artifacts: [payload/result files if the user asked to save them]
next:      another model/patient, obs_dt what-if, or /inlab-human review (study mode)
```
