# inlab-human

**In-lab human evaluation of deployed prediction endpoints, with the Claude Code chat as the reader UI.**

A clinician sits with a Claude Code session and reads de-identified cases in a
**blind → assisted** protocol: first estimate risk from the raw chart data alone, then see
the model's risk score + SHAP attribution + an agent-written narrative and re-estimate.
Every judgment lands as a structured row in `responses.jsonl`; a report skill scores the
model *and* its influence on the clinician against gold outcomes.

Seeded 2026-07 by the REACH → clinic translation effort (first target:
`reach.adhd.xgb` on Databricks), but **endpoint-agnostic by construction** — any endpoint
that takes a JSON payload and returns a score is a *config*, not code.

## Why this exists

Before a research model goes anywhere near production (Epic, SIP review, live FHIR), the
agreed first step is an in-lab clinician pilot: does the score+explanation actually help a
clinician, or mislead them? No platform for this exists (confirmed by JHU Health IT); every
team hand-rolls it. This plugin is the reusable engine: no web app to build, host, or
secure — the chat session **is** the interface, and the skills enforce the protocol
(blinding, structured capture) that free-form chat would not.

## Architecture — skill → agent → tool

```
/inlab-human            Tier-1 session driver (dispatch + status)
    │
    ├── /inlab-human-bundle    for each sampled de-id case:
    │        endpoint-predict MCP tool  ──►  {score, shap}     (deterministic; LLM never
    │        narrator agent             ──►  clinical narrative      produces the number)
    │        freeze ALL of it ──► review_bundle.json
    │
    ├── /inlab-human-review    THE READER SESSION (chat = UI)
    │        case N: raw features only ──► clinician: blind risk + decision + confidence
    │        reveal score + SHAP + narrative ──► assisted re-estimate
    │        + rate the SCORE and the EXPLANATION **separately**
    │        append structured row ──► responses.jsonl
    │
    └── /inlab-human-report    responses + gold ──► metrics.json + figures
             (model accuracy on sample · blind→assisted influence · agreement · ratings)
```

Two design rules the skills enforce:

1. **The score is deterministic.** The XGBoost/endpoint score comes from the
   `endpoint-predict` MCP tool, pipeline-driven — the narrator agent only *consumes* it.
2. **Frozen bundle.** The reader session reads a static `review_bundle.json` — never a live
   cluster. Reproducible, offline, de-identified, immune to endpoint cold-start.

## Components

| Path | What |
|---|---|
| `skills/inlab-human/` | Tier-1 orchestrator — `/inlab-human` |
| `skills/inlab-human-bundle/` | sample cases → predict → narrate → freeze bundle |
| `skills/inlab-human-review/` | the blind→assisted reading session |
| `skills/inlab-human-report/` | metrics + pilot figures |
| `agents/inlab-narrator-agent.md` | narrative writer (consumes score+SHAP; never scores) |
| `mcp-servers/endpoint-predict/` | the endpoint URL as an MCP tool: `predict(payload) → {score, shap}` |
| `ref/review-bundle-schema.md` | frozen-bundle contract |
| `ref/feedback-form.md` | per-case + per-session response fields (`responses.jsonl` contract) |

## Wire-contract provenance

`endpoint-predict` embeds a self-contained copy of the payload/POST logic from
`haipipe-toolkit/skills/task/4_individual/haipipe-individual-inference/src/{client,build_payload}.py`
(Endpoint_Set `dataframe_records` contract — same wire format for local FastAPI, Databricks
Model Serving, SageMaker). Provenance is pinned in each file header; if the upstream
contract changes, re-sync the copy.

## What this plugin is NOT

- ❌ Not a recruitment platform (finding/paying clinicians) — that is a possible future
  product this engine seeds.
- ❌ Not production-schema validation (OMOP ↔ live-FHIR skew) — separate, later work with
  the deploying institution.
- ⚠️ Cases shown to clinicians must be **de-identified** before they enter a bundle; the
  plugin never de-identifies for you.

## Study data lives with the study

The plugin is the engine. Endpoint configs, frozen bundles, `responses.jsonl`, and analysis
outputs live in the study's project repo (e.g. `examples/Project-InLabHumanEval-Reach/`),
never inside the plugin.
