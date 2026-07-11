# Changelog — inlab-human

## 0.1.0 — 2026-07-10
- Plugin scaffold: plugin.json, README (architecture: skill → narrator agent → endpoint-predict MCP tool; chat = reader UI).
- `ref/review-bundle-schema.md` v0.1 — frozen-bundle contract (presentation / model_output / gold separation + build invariants; attributions optional via `attribution_available` for endpoints that return no SHAP).
- `ref/feedback-form.md` v0.1 — blind→assisted response contract (`responses.jsonl`), score vs explanation rated separately.
- `mcp-servers/endpoint-predict/` — dependency-free MCP server (ping, predict, predict_packaged_example) + `predict_cli.py` twin for Bash use; stdio rebinding kept out of the import path so the module doubles as a library.
- Skills: `/inlab-human` (tier-1), `/inlab-human-bundle` (+ deterministic `scripts/build_bundle.py`, examples-mode v0.1), `/inlab-human-review`, `/inlab-human-report`; `agents/inlab-narrator-agent.md`.
- Smoke-tested end-to-end against `reach.adhd.xgb_v0003` served locally (Flask, Databricks wire contract): 6-case demo bundle frozen with live scores (0.256–0.864) + narrator narratives; validation OK.

## 0.2.0 — 2026-07-10
- CONSOLE mode (new default): patient-first on-demand inference, per user direction — get a patient → all their data → list models → "run this model on this patient" → tool prepares payload → endpoint → results + analysis.
- endpoint-predict v0.2 tools: `list_patients`, `get_patient`, `list_models` (live-status via registry ping), `prepare_payload`, `predict_for_patient` (one-shot: build payload incl. trigger dataframe_records → POST → score + gaps report). Model resolution prefers registered-URL + highest version. `obs_dt` override = "predict as of date X".
- New env config: INLAB_PATIENT_STORE, INLAB_ENDPOINT_STORE, INLAB_REGISTRY (endpoint-URL registry JSON).
- `/inlab-human-console` skill; tier-1 `/inlab-human` re-routed (console default; bundle/review/report = study mode).
- Patient-store contract: extractor scrubs outcome fields (Label/Split/ground_truth*) from all tables — caught a real gold leak in PD2D's Cohort table — and stores per-endpoint trigger records.
- Verified live: reach-200020×PD2D → 0.1977 MODERATE; reach-100060×ADHD → 0.795 HIGH; cross-model (ADHD patient × PD2D model) runs with explicit missing-tables gaps.

## 0.2.1 — 2026-07-10
Fixes found by monitoring a real console session that spent ~80s on discovery instead of inference:
- `predict_cli.py`: console verbs added (`list-patients`, `get-patient`, `list-models`, `prepare-payload`, `predict-for-patient`) — the fallback path previously exposed only the 3 network verbs, so a session without live MCP tools had nothing to fall back to.
- `predict_cli.py`: config auto-resolution (flags → `INLAB_*` env → the repo's `.mcp.json`). **No env vars required** — the previous flow forced the agent to grep server.py and .mcp.json to find the stores.
- `inlab-human-console` SKILL.md: explicit copy-paste commands + "DO NOT go exploring"; stale-MCP detection (only ping/predict/predict_packaged_example exposed ⇒ server started pre-v0.2 ⇒ tell the user to restart the session, use the CLI meanwhile); warm the endpoint up front (model load ~20-40s).
