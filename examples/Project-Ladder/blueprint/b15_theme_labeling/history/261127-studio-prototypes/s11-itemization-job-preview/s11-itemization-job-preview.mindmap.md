---
mindmap: 1
title: Itemization
built: design proposal
---

# Itemization <!-- root -->

- Work Folder <!-- folders -->
  - Block: bNN_itemization <!-- block -->
  - Job: One source snapshot × one accepted item recipe; recipe trials are Runs of the same Job. <!-- job -->
  - Task roles: Source · Build · Check <!-- tasks -->
  - Run: one bounded operation with recorded input versions <!-- runs -->
  - Delivery: Items package with stable IDs, context and source references <!-- output -->
- Work UI <!-- ui -->
  - Job topics: Source collection <!-- jobtopics -->
  - Main: input binding and Task results <!-- main -->
  - Task: evidence, Runs and owned actions <!-- taskpage -->
  - Studio: human choices and acceptance <!-- human -->
- Handoff <!-- handoff -->
  - Reads: Source snapshot and an accepted item recipe <!-- input -->
  - Immutable release and explicit downstream references <!-- versions -->
- Definition <!-- define -->
  - Page: legacy live baseline <!-- live -->
  - Effect: synthetic interactive proposal <!-- effect -->
  - Trace: plan, prompts, changes and checks <!-- trace -->
