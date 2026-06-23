# fn: feedback

Two feedback scopes: **tool feedback** (about haipipe-application itself)
and **intervention feedback** (about a specific intervention's content).


## Tool feedback

Captures complaints about the skill — a verb is missing, a stage is
clunky, the draft output is poorly structured.

```
/haipipe-application feedback "<text>"
/haipipe-application feedback list
```

Writes to: `Tools/plugins/haipipe-toolkit/skills/application/haipipe-application/feedback/`

File format:
```yaml
---
status: open | fixed
created: YYYY-MM-DD
context: <what you were doing>
fixed_in: ""
---
<the feedback>

Fix: <added when resolved>
```


## Intervention feedback

Captures feedback about a specific intervention's design, artifacts,
versions, targeting, or performance — the work, not the tool.

```
/haipipe-application feedback "<text>" --intervention <name>
/haipipe-application feedback list --intervention <name>
```

Writes to: `<PROJECT_ROOT>/applications/<intervention>/feedback/`

Same file format as tool feedback, but scoped to the intervention.


## Routing logic

```
/haipipe-application feedback "<text>"
  → no --intervention flag → tool feedback (skill's feedback/)
  → --intervention given   → intervention feedback (project's applications/<name>/feedback/)

/haipipe-application feedback "<text>" --intervention 01_personalized_framing
  → resolves PROJECT_ROOT
  → writes to applications/01_personalized_framing/feedback/<DATE>_<slug>.md

/haipipe-application feedback list
  → no --intervention → list skill feedback/ open items
  → --intervention    → list intervention feedback/ open items
  → --all             → list both
```


## Workflow

```
Step 1: Parse args.
        First token = "feedback" → enter feedback handler.
        If remaining starts with "list" → list mode.
        Otherwise → capture mode.

Step 2: Determine scope.
        --intervention <name> → intervention scope.
        No flag → tool scope.

Step 3: Capture mode:
        a. Derive slug from feedback text (kebab-case, ≤ 6 words).
        b. Write file: <YYYY-MM-DD>_<slug>.md
        c. Set status: open, created: today, context: inferred from
           active intervention or "general".
        d. Confirm: "Feedback filed: <path>"

Step 4: List mode:
        a. Glob feedback/*.md in target directory.
        b. Filter status: open.
        c. Print one-line per item: date, slug, first line of body.
        d. Count: "N open items."
```


## Examples

```
/haipipe-application feedback "V02 targeting rule is too broad — female AND generic captures patients who should get authority framing instead"
  → tool scope (no --intervention)
  → writes: haipipe-application/feedback/2026-06-23_v02-targeting-too-broad.md

/haipipe-application feedback "V02 targeting rule is too broad" --intervention 01_personalized_framing
  → intervention scope
  → writes: applications/01_personalized_framing/feedback/2026-06-23_v02-targeting-too-broad.md

/haipipe-application feedback list --intervention 01_personalized_framing
  → lists open items in applications/01_personalized_framing/feedback/
```


## When to use which scope

```
"the draft skill should support multi-segment output"     → tool feedback
"the lifecycle orchestrator missed the venue check"        → tool feedback
"V02 emotional cue tone is too warm for generic-Rx"        → intervention feedback
"V01 targeting should include pre_total_auth_7d"           → intervention feedback
"the VERSION-MAP priority order needs rethinking"          → intervention feedback
```
