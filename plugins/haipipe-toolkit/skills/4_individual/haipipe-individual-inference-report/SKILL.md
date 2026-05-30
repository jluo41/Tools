---
name: haipipe-individual-inference-report
description: "Per-individual prediction-interpretation report. Loads one individual's data + recent CGM, hits the deployed prediction endpoint, then asks Claude (via claude_agent_sdk) to compose a dual-layer Report — structured JSON + natural-language text — for a specified audience persona (patient / clinician / etc.). Builds on haipipe-individual-inference (which provides the load+predict). The persona library (system prompt, schema, safety rules, tone) is pluggable: name a shipped persona or pass an absolute path to your own. Use to test how a deployed endpoint's prediction reads to a real audience, or to generate reports for downstream LLM-judge / doctor evaluation. Trigger: individual report, prediction interpretation, generate patient message, /haipipe-individual-inference-report."
argument-hint: "--individual <id> --persona <name_or_path> [--endpoint-url URL] [--model X]"
allowed-tools: Bash, Read
---

Skill: haipipe-individual-inference-report
========================================

Per-individual prediction → interpretation → audience-tailored report.

```
  📥 individual data        🌐 endpoint prediction       🤖 LLM compose
  (parquet)              (haipipe-end-deploy-local)   (claude_agent_sdk)
       │                          │                          │
       └─ ctx ───┬───── forecast ─┴───── system_prompt ───────┘
                │                       (persona)
                ▼
           📨 Report{json, nl}
              + telemetry
```

Sibling progression in `5_individual/`:

| Skill | Adds | Output |
|-------|------|--------|
| `haipipe-individual` | (data load only) | ctx dict |
| `haipipe-individual-inference` | + payload + POST | forecast JSON |
| `haipipe-individual-inference-report` | + persona + LLM | Report{json, nl} |

---

Layout
-------

```
src/
  compose_report.py     SDK call (cribbed from physician judge), XML extract, parse
  report_schema.py      pydantic Report model
  persona_loader.py     resolve --persona name | path → system_prompt + meta

personas/                   ← shipped reference personas (1-2)
  patient-friendly/
    persona.yaml          metadata: audience, tone, model, safety_rules
    system.md             system prompt
    schema.md             <report> XML schema description

scripts/
  make_report_cli.py    end-to-end CLI: individual + persona → report

tests/
  (smoke against Subject-18, when written)
```

---

Quickstart
-----------

1. Start the local prediction endpoint (sibling skill):

```
ENDPOINT_PATH=_WorkSpace/6-EndpointStore/endpoint_cgm_patchtst_ohio_v0001 \
PORT=8765 \
    python Tools/plugins/haipipe-toolkit/skills/3_end/haipipe-end-deploy-local/scripts/serve_local.py
```

2. Generate a report:

```
python Tools/plugins/haipipe-toolkit/skills/5_individual/haipipe-individual-inference-report/scripts/make_report_cli.py \
    --individual Subject-18 \
    --persona patient-friendly
```

Output: `_WorkSpace/7-AgentWorkspace/reports/<individual_id>/<persona>/<ts>/`
```
report.json     structured payload (matches Report pydantic)
report.txt      patient-facing NL (3-6 sentences)
response.xml    raw <report> block from the LLM
meta.json       telemetry: model, cost, duration, session_id, ...
```

---

Persona system
---------------

A persona is a **folder** with three files:

```
<persona-dir>/
├── persona.yaml      audience, tone, model, language, safety_rules
├── system.md         system prompt
└── schema.md         <report> XML schema description
```

`--persona` accepts:

| Form | Resolves to |
|------|-------------|
| `patient-friendly` | `personas/patient-friendly/` (shipped) |
| `/abs/path/to/cardiologist/` | that exact folder |

This lets external persona libraries (Samsung-internal, IRB-approved
templates, etc.) live **outside** haipipe-toolkit and still be invoked
without forking the skill.

Required fields in `persona.yaml`:
- `audience`  (e.g. patient, clinician, parent)
- `tone`
Optional: `model`, `language`, `safety_rules`, anything else the persona
author wants to track (logged into report `meta.json`).

---

LLM call mechanics
-------------------

Uses `claude_agent_sdk` (subprocess to local `claude` CLI). Auth flows
through `~/.claude` OAuth — same login the user did in this Claude Code
session. **Cost is reported (`cost_usd_equiv` in telemetry) but not
billed when subscription auth is active.**

The script `unset`s `ANTHROPIC_AUTH_TOKEN` and `ANTHROPIC_BASE_URL`
before the SDK call to avoid the project's CRS proxy diverting the
request away from OAuth (see repo memory `reference_crs_proxy_gotcha`).

---

Output schema (XML the model emits)
------------------------------------

```xml
<report>
  <basics>{individual_id, dataset, gender, year_of_birth, disease_type}</basics>
  <current>{last_obs_dt, last_bg_mg_dl, recent_window_n, recent_min/max/mean}</current>
  <forecast_summary>{horizon_minutes, n_windows, pred_min/max/mean}</forecast_summary>
  <interpretation>
    <verdict>rising|stable|falling|mixed</verdict>
    <why>...</why>
    <actions><action>...</action></actions>
    <confidence>high|medium|low</confidence>
    <safety_flag>none|hypo_risk|hyper_risk|hypo_and_hyper_risk</safety_flag>
  </interpretation>
  <nl>... patient-facing prose ...</nl>
</report>
```

---

Failure modes
--------------

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `no <report>...</report> block in SDK output` | Model wrote prose around the XML | Tighten persona system prompt; check `response.xml` |
| `requests.exceptions.ConnectionError ... 8765` | Endpoint server not running | Start `serve_local.py` (see step 1) |
| `pydantic.ValidationError` on Report | Model violated enum (verdict/confidence/safety_flag) | Inspect `response.xml`; persona should constrain enum strictly |
| SDK reports `is_error` | Auth or model id wrong | Confirm `~/.claude` logged in; `claude --version`; check `model` in persona.yaml |

---

Reuses
------

- `haipipe-individual-inference` for `load_patient_ctx`, `build_payload`, `client.call_predict`
- `haipipe-end-deploy-local` for the prediction endpoint
- `claude_agent_sdk` for the LLM call (subprocess of `claude` CLI)
- Pattern reference: `Physician-SPACE/.../tasks/A3_cross_family_judge/run_sdk_judge.py`
