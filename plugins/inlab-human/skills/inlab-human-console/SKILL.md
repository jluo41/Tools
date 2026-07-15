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

Tooling — DO NOT go exploring
-----------------------------

Two interchangeable paths. **Never** grep for stores, read `.mcp.json`, or
hand-roll python: the CLI twin resolves its own config (flags → `INLAB_*` env →
the repo's `.mcp.json`), so **no env vars are needed**.

A. MCP tools if present: `mcp__endpoint-predict__{list_patients,get_patient,
   list_models,prepare_payload,predict_for_patient}`.
   If only `ping`/`predict`/`predict_packaged_example` are exposed, the MCP
   process is STALE (started before v0.2) — say so, tell the user a session
   restart picks up the console tools, and use path B meanwhile. Do not
   investigate further.

B. CLI twin (always works, copy-paste):

```bash
CLI=Tools/plugins/inlab-human/mcp-servers/endpoint-predict/predict_cli.py   # from repo root
python3 $CLI list-patients
python3 $CLI list-models
python3 $CLI get-patient          --patient-id <ID> [--tables Dx Med] [--max-rows 20]
python3 $CLI prepare-payload      --patient-id <ID> --model <MODEL>
python3 $CLI predict-for-patient  --patient-id <ID> --model <MODEL> [--obs-dt 2023-06-01]
# <ID> / <MODEL> come from list-patients / list-models above — the cohort is the
# study's, not this plugin's, so nothing study-specific is hard-coded here.
```

| Step | Tool / subcommand | Notes |
|---|---|---|
| who is available | `list_patients` | id + demographics + table counts |
| the patient's data | `get_patient` | ALL source tables; `tables`/`max_rows` for huge charts (MIMIC) |
| what models exist | `list_models` | name, version, required tables, URL, **live?** |
| run it | `predict_for_patient` | prepares payload (incl. trigger record) → POSTs → score + gaps |
| payload only (inspect) | `prepare_payload` | show what would be sent, without calling |

Endpoint not live? Start it (background) and wait for `/ping` — model load takes
~20-40s, so warm it up BEFORE the user picks a model:

```bash
.venv/bin/python examples/Project-InLabHumanEval-Reach/tasks/A01_serve_endpoint_local/serve_endpoint.py \
    --endpoint-path _WorkSpace/6-EndpointStore/<pkg> --port <5050 adhd|5051 pd2d|5052 mimic>
```

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
