---
name: learn-azure
description: "Azure + Databricks infrastructure knowledge base. Wiki of core concepts (subscription, IAM, quota, workspace, cluster, Unity Catalog, volumes, notebooks, model serving, user management, cost control), hard-won lessons (gotchas to check BEFORE acting), and an overview diagram. Use when setting up Azure resources, inviting users, debugging infrastructure, or onboarding team members. Verbs: lesson (capture/list/search gotchas), feedback (wiki gaps), digest (bulk harvest from session). Trigger: azure, databricks setup, invite user, quota, cluster, IAM, infrastructure, /learn-azure."
argument-hint: "[lesson | feedback | digest] [args]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "1.0.0"
  last_updated: "2026-06-26"
  summary: "Azure + Databricks wiki, lessons, and feedback system."
---

Skill: learn-azure
==================

Azure + Databricks infrastructure knowledge base for the REACH team.

What It Contains
----------------

  wiki/     14 concept pages (subscription, IAM, quota, workspace, cluster,
            Unity Catalog, volumes, notebooks, model serving, user management,
            invite runbook, cost control)
  lesson/   Hard-won gotchas — things that surprised us and should be checked
            BEFORE acting on Azure/Databricks infrastructure
  diagram/  ASCII overview diagram of the full stack
  feedback/ Inbox for wiki/diagram gaps and errors

Verbs
-----

  /learn-azure lesson "<text>"     Capture a new lesson
  /learn-azure lesson list         List all lessons
  /learn-azure lesson search <kw>  Find relevant lessons before acting
  /learn-azure feedback "<text>"   Report a wiki gap or error
  /learn-azure digest              Bulk harvest feedback from a session

The Guardrail Contract
----------------------

BEFORE executing Azure/Databricks infrastructure work, the agent MUST:
  1. Scan lesson/ for relevant lessons
  2. Flag any that apply to the user
  3. Scan wiki/ for relevant concept pages if the user is unfamiliar

Entry Points
------------

  Concept lookup .... read wiki/<topic>.md
  Before acting ..... grep lesson/*.md for relevant gotchas
  After a surprise .. /learn-azure lesson "<what happened>"
  Wiki is wrong ..... /learn-azure feedback "<what's wrong>"
