---
name: inlab-human-bundle
description: "Freeze a review_bundle.json for an in-lab reading session: sample de-identified cases, score each via the endpoint-predict tool (live endpoint, deterministic), add narrator-agent explanations, validate schema invariants, freeze. v0.1 source mode: the Endpoint_Set package's own examples/. Called by /inlab-human orchestrator; also directly. Trigger: build bundle, freeze bundle, review bundle, /inlab-human-bundle."
argument-hint: "<endpoint_path> [--endpoint-url URL] [--bundle-id ID] [--out PATH]"
allowed-tools: Bash, Read, Write, Grep, Glob, Agent
metadata:
  version: "0.1.0"
  last_updated: "2026-07-10"
  summary: "Builder: cases -> endpoint scores -> narratives -> frozen review_bundle.json."
---

Skill: inlab-human-bundle
==========================

Produces the single artifact a reading session consumes. Deterministic parts
(sampling, scoring, de-id shaping, validation) run in `scripts/build_bundle.py`;
the ONLY LLM-produced field is `model_output.narrative`, merged afterwards.

Procedure
---------

```
1. Locate the endpoint.
   - live URL given -> use it.  else: is a local server up? (predict_cli.py ping)
   - if not, offer to start one (the study project's serve_endpoint task, or
     /haipipe-end-deploy-local) and wait for /ping healthy.

2. Deterministic build (Bash):
     python3 scripts/build_bundle.py \
        --endpoint-path <Endpoint_Set dir> --endpoint-url <URL> \
        --bundle-id <id> --out <study>/bundles/review_bundle_<id>.json \
        --task-description "<what the model predicts, clinician-facing>" \
        --horizon "<prediction horizon>"
   The script POSTs every case through the SAME code path as the
   endpoint-predict MCP tool, writes the bundle + a .build_log.json
   (case_id ↔ raw score audit trail), and validates the schema invariants.
   A validation error is a HARD STOP — fix, rebuild; never hand-edit a bundle.

3. Narratives — dispatch the narrator agent (agents/inlab-narrator-agent.md),
   one call per case or batched. Input per case: presentation + model_output
   (score, band, shap_top if any). The agent NEVER sees gold. Write
   {case_id: {narrative, agent}} to narratives.json, then:
     python3 scripts/build_bundle.py --merge-narratives narratives.json --out <bundle>
   No SHAP from the endpoint? The narrative may DESCRIBE the case alongside the
   score but must not claim feature attributions the model didn't provide.

4. Freeze: report bundle path, n cases, strata table, validation status.
   A frozen bundle is immutable — changes mean a new --bundle-id.
```

Output contract: `../../ref/review-bundle-schema.md` (v0.1).

Return contract
---------------

```
status:    ok | blocked | failed
summary:   bundle id, n cases, strata counts, narrative coverage
artifacts: [review_bundle_<id>.json, .build_log.json]
next:      /inlab-human review <bundle path>
```
