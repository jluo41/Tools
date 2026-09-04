---
name: inlab-human-review
description: "Run the in-lab clinician reading session in the Claude Code chat: blind pass (raw case data only → clinician's risk estimate, decision, confidence), reveal (model score + explanation), assisted pass (re-estimate + rate score and explanation SEPARATELY), append structured rows to responses.jsonl. Consumes a frozen review_bundle.json; never calls a live endpoint; never shows gold. Called by /inlab-human orchestrator; also directly. Trigger: reading session, review bundle with clinician, blind assisted, /inlab-human-review."
argument-hint: "<review_bundle.json> [--reader-id RXX] [--resume]"
allowed-tools: Bash, Read, Write, Grep, Glob
metadata:
  version: "0.1.0"
  last_updated: "2026-07-10"
---

Skill: inlab-human-review
==========================

The chat IS the reader UI. This skill turns a session into a disciplined
instrument: fixed case order, blind-before-assisted, structured capture.
Response contract: `../../ref/feedback-form.md` (v0.1).

Session protocol
----------------

```
0. SETUP
   - Load the bundle. Confirm reader_id (pseudonymous, e.g. R01 — roster is
     kept OUTSIDE the repo). responses.jsonl sits next to the bundle:
     responses_<bundle_id>_<reader_id>.jsonl
   - --resume: skip cases already answered by this reader.
   - Tell the reader the ground rules: estimates are theirs alone in the blind
     pass; there are no right answers being graded live; free-text is welcome.

1. PER CASE (in bundle order — never reorder, never skip silently):
   BLIND
   - Render ONLY the presentation block, clinician-readable:
     demographics line · visit context · problem list table · medications table
     · measurements · questionnaires · visit history. NOTHING model-derived.
   - Ask (conversationally, one message): risk estimate 0-100 (or "declined"),
     decision [refer | monitor_closely | routine_care], confidence 1-5,
     one-line rationale.
   - APPEND the blind fields to the row IMMEDIATELY (before any reveal).
   REVEAL
   - Show model_output: risk score + band, shap_top (if any), narrative.
     If attribution_available=false, SAY SO — "the model provides no feature
     attributions; the narrative is descriptive."
   ASSISTED
   - Ask: revised estimate + decision + confidence; then the ratings —
     score_plausibility 1-5, explanation_quality 1-5, explanation_issues
     [spurious_feature|missing_key_factor|wrong_direction|overconfident_language|none],
     would_act_on 1-5, free-text case notes.
   - Complete the row (blind fields are IMMUTABLE once written) and append via
     Bash (>> responses.jsonl). One JSON line per case, schema_version 0.1.

2. WRAP-UP (after last case)
   - Session block: overall_trust, fit_in_workflow (+where in the day),
     top_concern, keep_using. Append as the "type":"session" row.
   - Quote-worthy free text: keep verbatim in the row, never paraphrase.

HARD RULES
- gold is NEVER printed, hinted at, or confirmed ("was I right?" -> "the
  report stage compares everyone's answers to outcomes; not during reading").
- Blind fields never edited after reveal. If the reader revises, it goes in
  case_notes, not the blind fields.
- Missing answer -> "declined", not a guess. Never invent or default a value.
- If the session aborts mid-case, the partial row keeps its blind fields;
  --resume re-presents that case from the REVEAL step.
```

Return contract
---------------

```
status:    ok | blocked | failed
summary:   n cases read / n total, reader_id, notable free-text themes
artifacts: [responses_<bundle_id>_<reader_id>.jsonl]
next:      /inlab-human report <bundle path>   (once enough readers/cases)
```
