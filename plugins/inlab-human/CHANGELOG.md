# Changelog — inlab-human

## 0.1.0 — 2026-07-10
- Plugin scaffold: plugin.json, README (architecture: skill → narrator agent → endpoint-predict MCP tool; chat = reader UI).
- `ref/review-bundle-schema.md` v0.1 — frozen-bundle contract (presentation / model_output / gold separation + build invariants; attributions optional via `attribution_available` for endpoints that return no SHAP).
- `ref/feedback-form.md` v0.1 — blind→assisted response contract (`responses.jsonl`), score vs explanation rated separately.
- `mcp-servers/endpoint-predict/` — dependency-free MCP server (ping, predict, predict_packaged_example) + `predict_cli.py` twin for Bash use; stdio rebinding kept out of the import path so the module doubles as a library.
- Skills: `/inlab-human` (tier-1), `/inlab-human-bundle` (+ deterministic `scripts/build_bundle.py`, examples-mode v0.1), `/inlab-human-review`, `/inlab-human-report`; `agents/inlab-narrator-agent.md`.
- Smoke-tested end-to-end against `reach.adhd.xgb_v0003` served locally (Flask, Databricks wire contract): 6-case demo bundle frozen with live scores (0.256–0.864) + narrator narratives; validation OK.
