---
name: learn-databricks-feedback
description: "Utility verb. Captures a complaint/confusion/wish about the learn-databricks SKILL itself (lesson gaps, wrong instructions, outdated info, missing concepts), ROUTED at capture time to the right topic category. `feedback list` shows open items; `feedback move` re-routes a mis-filed item."
argument-hint: "[\"<text>\" | list | move <file> <category>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Feedback (capture skill feedback, route at capture, fix later)

Captures feedback about the learn-databricks SKILL (lessons are wrong, a concept
is missing, instructions don't work, a journey doc is confusing) and FILES IT in
the `feedback/` folder. Does NOT fix anything; fixing is a separate revision pass.
Distinguish from project issues: feedback is about the LEARNING MATERIAL, not
about Databricks itself.

## Capture: `/learn-databricks feedback "<text>"`

```
1. INFER the topic category from the text (see "Routing" below).
2. MERGE-OR-CREATE (inbox must NOT grow without bound):
   a. Read OPEN (and fixed) items already in feedback/.
   b. SAME-TOPIC test: same underlying concern, not just same category.
   c. SAME TOPIC -> UPDATE in place (append recurrence, bump count, reopen if fixed).
   d. NEW TOPIC -> CREATE feedback/<YYYY-MM-DD>_<short-slug>.md.
3. CONFIRM where it landed (MERGED or NEW).
```

### Routing (topic categories)

```
vm, stockout, confidential       -> lesson: azure-vm-stockout
init-script, libraries-api       -> lesson: init-scripts
runtime, ml-runtime              -> lesson: ml-runtime
pip, %pip, magic, interactive    -> lesson: pip-magic
dbutils, notebook.run, env-var   -> lesson: dbutils-notebook-run
job, task, orchestrator          -> lesson: job-tasks
env, environment, explicit       -> lesson: env-vars
pandas, version, compatibility   -> lesson: pandas-version
package, install, small-vm       -> lesson: package-install
partition, caseset, upload       -> lesson: caseset-partition
journey, session, deployment     -> journey doc
NO MATCH                         -> general (feedback/ root)
```

### One file per item (schema)

```
---
status: open | fixed
created: YYYY-MM-DD
updated: YYYY-MM-DD
occurrences: 1
context: <lesson-page or "general">
fixed_in: ""
regressed: ""
---
<the feedback, in the reporter's words>

## Recurrences
- YYYY-MM-DD: <the new phrasing, verbatim>

Fix: <added when resolved>
```

## List: `/learn-databricks feedback list`

```
Grep feedback/*.md for `status: open`, print newest-first.
```

## Move: `/learn-databricks feedback move <file> <category>`

```
Re-tag the context field.
```
