---
name: learn-azure-feedback
description: "Utility verb. Captures a complaint/confusion/wish about the learn-azure SKILL itself (wiki gaps, wrong instructions, outdated info, missing concepts), ROUTED at capture time to the right topic category. `feedback list` shows open items; `feedback move` re-routes a mis-filed item."
argument-hint: "[\"<text>\" | list | move <file> <category>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Feedback (capture skill feedback, route at capture, fix later)

Captures feedback about the learn-azure SKILL (wiki pages are wrong, a concept
is missing, instructions don't work, a diagram is confusing) and FILES IT in the
`feedback/` folder. Does NOT fix anything; fixing is a separate revision pass.
Distinguish from project issues: feedback is about the LEARNING MATERIAL, not
about Azure/Databricks itself.

## Capture: `/learn-azure feedback "<text>"`

```
1. INFER the topic category from the text (see "Routing" below).
2. MERGE-OR-CREATE (inbox must NOT grow without bound):
   a. Read OPEN (and fixed) items already in feedback/.
   b. SAME-TOPIC test: is the new item the same underlying concern as an
      existing file -- not merely the same category?
   c. SAME TOPIC -> UPDATE that file in place:
        - append a dated line under "## Recurrences" in the reporter's NEW
          words. NEVER edit prior text.
        - bump frontmatter: updated: <today>; occurrences: +1.
        - if status was `fixed`, REOPEN: status: open + regressed: <today>.
   d. NEW TOPIC -> CREATE one file: feedback/<YYYY-MM-DD>_<short-slug>.md.
3. CONFIRM where it landed (MERGED or NEW).
```

### Routing (topic categories)

```
subscription, billing          -> wiki concept: subscription
resource-group                 -> wiki concept: resource-group
iam, role, contributor, owner  -> wiki concept: iam
azure-ad, entra, tenant, guest -> wiki concept: azure-ad
quota, vcpu                    -> wiki concept: quota
workspace                      -> wiki concept: workspace
cluster, serverless, runtime   -> wiki concept: cluster
unity-catalog, catalog, schema -> wiki concept: unity-catalog
volume, dbfs, file storage     -> wiki concept: volumes
notebook, dbutils, %pip        -> wiki concept: notebook
model-serving, endpoint, mlflow -> wiki concept: model-serving
user, invite, entitlement      -> wiki concept: user-management
cost, budget, spot, dbu        -> wiki concept: cost-control
diagram, overview              -> diagram
NO MATCH                       -> general (feedback/ root)
```

### One file per item (schema)

```
---
status: open | fixed
created: YYYY-MM-DD
updated: YYYY-MM-DD
occurrences: 1
context: <wiki-page or "general">
fixed_in: ""
regressed: ""
---
<the feedback, in the reporter's words>

## Recurrences
- YYYY-MM-DD: <the new phrasing, verbatim>

Fix: <added when resolved>
```

## List: `/learn-azure feedback list`

```
Grep feedback/*.md for `status: open`, print newest-first.
```

## Move: `/learn-azure feedback move <file> <category>`

```
Re-tag the context field. This is a metadata edit, not a file move (all items
live in one feedback/ folder).
```
