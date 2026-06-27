---
status: open
created: 2026-06-27
updated: 2026-06-27
occurrences: 1
context: general
fixed_in: ""
regressed: ""
---

I want to use /subjective-label as the orchestrated skill instead of using the sub-skills (/sl-init, /sl-iterate, etc.) directly. The router should detect project state and dispatch automatically, not ask me to pick a sub-command.

Current behavior: /subjective-label shows a menu of sub-commands and waits for me to pick one. I then have to invoke /sl-init or /sl-iterate separately.

Desired behavior: /subjective-label reads .state.json (or detects no project yet), auto-dispatches to the right sub-skill, and stays in copilot mode as a single orchestrator. The sub-skills should be internal implementation, not user-facing entry points. Like how /haipipe-paper is one skill that routes through the lifecycle internally.

## Recurrences
