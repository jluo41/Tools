---
mindmap: 1
title: Labeling at Scale
built: design proposal
---

# Labeling at Scale <!-- root -->

- Work Folder <!-- folders -->
  - Block: bNN_labeling_at_scale <!-- block -->
  - Job: One Items snapshot × one signed Guideline release × one executor configuration. Batches and retries are Runs. <!-- job -->
  - Task roles: Qualification · Execution · Quality <!-- tasks -->
  - Run: one bounded operation with recorded input versions <!-- runs -->
  - Delivery: Audited labels with coverage, exclusions and per-item provenance <!-- output -->
- Work UI <!-- ui -->
  - Job topics: Guideline release <!-- jobtopics -->
  - Main: input binding and Task results <!-- main -->
  - Task: evidence, Runs and owned actions <!-- taskpage -->
  - Studio: human choices and acceptance <!-- human -->
- Handoff <!-- handoff -->
  - Reads: Released Items, signed Guideline and executor configuration <!-- input -->
  - Immutable release and explicit downstream references <!-- versions -->
- Definition <!-- define -->
  - Page: legacy live baseline <!-- live -->
  - Effect: synthetic interactive proposal <!-- effect -->
  - Trace: plan, prompts, changes and checks <!-- trace -->
