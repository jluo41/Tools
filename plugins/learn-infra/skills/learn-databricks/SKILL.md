---
name: learn-databricks
description: "Databricks-specific lessons and knowledge base. 13 hard-won lessons from the REACH-ADHD deployment (VM stockout, init scripts, env vars, pandas compatibility, partition mismatches, MLflow signatures, Model Serving payload routing, CLI auth) plus the full deployment journey doc. Use when running pipelines on Databricks, debugging cluster/notebook issues, deploying to Model Serving, or onboarding. Verbs: lesson (capture/list/search gotchas), feedback (lesson doc gaps), digest (bulk harvest from session). Trigger: databricks, cluster issue, notebook, dbutils, pipeline on databricks, model serving, mlflow, /learn-databricks."
argument-hint: "[lesson | feedback | digest] [args]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "1.0.0"
  last_updated: "2026-06-26"
  summary: "Databricks lessons, journey docs, and feedback system."
---

Skill: learn-databricks
=======================

Databricks-specific knowledge base for the REACH team.

What It Contains
----------------

  lesson/     13 hard-won lessons from the REACH-ADHD Databricks deployment
              (VM stockout, init scripts, env vars, pandas compat, partitions,
               MLflow signatures, Model Serving payload routing, CLI auth)
  feedbacks/  Journey docs + inbox for lesson gaps and errors

Existing Lessons
----------------

  01  Azure VM stockout — use confidential compute (DC-series)
  02  Init scripts blocked — use Libraries API
  03  Use ML Runtime for ML packages
  04  %pip magic only works interactively
  05  dbutils.notebook.run() loses env vars
  06  Use separate job tasks, not orchestrator notebook
  07  Set all env vars explicitly per notebook
  08  pandas version compatibility (1.5.3 vs 2.x)
  09  Don't install many packages on small VMs
  10  CaseSet partition mismatch — upload from local
  11  Unity Catalog requires model signature
  12  "dataframe_records" is reserved — use payload passthrough
  13  Databricks CLI auth tokens expire (~1 hour)

Verbs
-----

  /learn-databricks lesson "<text>"     Capture a new lesson
  /learn-databricks lesson list         List all lessons
  /learn-databricks lesson search <kw>  Find relevant lessons before acting
  /learn-databricks feedback "<text>"   Report a lesson doc gap or error
  /learn-databricks digest              Bulk harvest feedback from a session

The Guardrail Contract
----------------------

BEFORE executing Databricks pipeline or infrastructure work, the agent MUST:
  1. Scan lesson/ for relevant lessons
  2. Flag any that apply to the user

Entry Points
------------

  Before acting ..... grep lesson/*.md for relevant gotchas
  After a surprise .. /learn-databricks lesson "<what happened>"
  Lesson is wrong ... /learn-databricks feedback "<what's wrong>"
