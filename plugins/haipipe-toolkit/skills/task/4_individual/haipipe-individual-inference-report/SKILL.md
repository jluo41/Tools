---
name: haipipe-individual-inference-report
description: >-
  Per-individual prediction-interpretation report: loads one individual's data
  and recent CGM, hits the deployed endpoint, then asks Claude to compose a
  dual-layer report — structured JSON plus natural language — for an audience
  persona. Trigger: individual report, prediction interpretation, generate
  patient message, /haipipe-individual-inference-report.
argument-hint: "--individual <id> --persona <name_or_path> [--endpoint-url URL] [--model X]"
allowed-tools: Bash, Read
metadata:
  version: "0.1.1"
  last_updated: "2026-09-20"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
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

Sibling progression in `task/4_individual/`:

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
  compose_report.py     SDK call, XML extract, parse
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
  test_label_contract.py  offline trend and report-label parsing checks
```

---

Quickstart
-----------

Use an already deployed endpoint when one is available.
For a new local server, follow `haipipe-end-deploy-local`: copy its reference
`serve_local.py` into the canonical serving Task's `scripts/` before launch.
Choose the platform of the packaged Src2InputFn/Input2SrcFn pair.

```sh
python Tools/plugins/haipipe-toolkit/skills/task/4_individual/haipipe-individual-inference-report/scripts/make_report_cli.py \
    --workspace-root /path/to/project \
    --individual UserGroup-OhioT1DM/Subject-559 \
    --platform sagemaker \
    --endpoint-model endpoint_cgm_patchtst_ohio/v0001 \
    --endpoint-url http://127.0.0.1:8765/invocations --persona patient-friendly
```

Output: `_WorkSpace/7-AgentWorkspace/reports/<individual_id>/<persona>/<ts>/`
```text
forecast.json   selected endpoint response
report.json     structured Report payload
report.txt      reader text
response.xml    raw LLM report response
meta.json       telemetry and forecast/report hash binding
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

This lets external persona libraries (Samsung-internal, IRB-approved templates, etc.) live **outside** haipipe-toolkit and still be invoked without forking the skill.

Required fields in `persona.yaml`:
- `audience`  (e.g. patient, clinician, parent)
- `tone`
Optional: `model`, `language`, `safety_rules`, anything else the persona author wants to track (logged into report `meta.json`).

---

LLM call mechanics
-------------------

Uses `claude_agent_sdk` (subprocess to local `claude` CLI).
Auth flows through `~/.claude` OAuth — same login the user did in this Claude Code session.
**Cost is reported (`cost_usd_equiv` in telemetry) but not billed when subscription auth is active.**

The script `unset`s `ANTHROPIC_AUTH_TOKEN` and `ANTHROPIC_BASE_URL` before the SDK call to avoid the project's CRS proxy diverting the request away from OAuth (see repo memory `reference_crs_proxy_gotcha`).

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
    <why>Evidence-based interpretation; state when a cause is unknown</why>
    <actions><action>...</action></actions>
    <confidence>unavailable</confidence>
    <safety_flag>none|hypo_risk|hyper_risk|hypo_and_hyper_risk</safety_flag>
  </interpretation>
  <nl>... patient-facing prose ...</nl>
</report>
```

Trend is a fixed mathematical description of the supplied series: a constant
series is `stable`; increases with no decreases are `rising`; decreases with
no increases are `falling`; and a series with both directions is `mixed`. It
does not establish clinical significance. The report interface has no forecast
calibration input, so `confidence` is `unavailable`; it must not infer
confidence from trajectory range or smoothness. Neither label establishes a
cause.

---

Failure modes
--------------

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `no <report>...</report> block in SDK output` | Model wrote prose around the XML | Tighten persona system prompt; check `response.xml` |
| `requests.exceptions.ConnectionError ... 8765` | Endpoint server not running | Start `serve_local.py` (see step 1) |
| `pydantic.ValidationError` on Report | Model violated enum (verdict/confidence/safety_flag) | Inspect `response.xml`; persona should constrain enum strictly |
| report rejected for trend/confidence | Model did not use the supplied fixed trend label or claimed confidence without calibration evidence | Inspect `response.xml` and the forecast evidence; do not override the trend rule |
| SDK reports `is_error` | Auth or model id wrong | Confirm `~/.claude` logged in; `claude --version`; check `model` in persona.yaml |

---

Reuses
------

- `haipipe-individual-inference` for `load_patient_ctx`, `build_payload`, `client.call_predict`
- `haipipe-end-deploy-local` for the prediction endpoint
- `claude_agent_sdk` for the LLM call (subprocess of `claude` CLI)
- Pattern reference: `Physician-SPACE/.../tasks/A3_cross_family_judge/run_sdk_judge.py`

`make_report_cli.py` accepts `--workspace-root` and `--platform`; select the deployed
wire pair even for a local wrapper. `meta.json` binds forecast.json and report.json
hashes and selected model/window indices. `forecast.json` is required for independent
forecast fact-checking; it follows the same project data policy as the report.
Patient actions are limited to explanation, care-team contact and a supplied existing
clinician plan. Do not derive new treatment, exercise, food or hydration instructions
from the forecast. The report and safety-review persona apply the same boundary.

Use `--endpoint-model` for the deployed model id. In the report CLI, `--model` selects the report-writing LLM and is a different setting.
