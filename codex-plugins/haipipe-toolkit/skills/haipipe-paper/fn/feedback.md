---
name: haipipe-paper-feedback
description: "Utility verb. Captures a complaint/confusion/wish about the paper SKILL itself into feedback/ (fix later); not paper content. `feedback list` shows open items."
argument-hint: "[\"<text>\" | list]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Feedback (capture skill feedback, fix later)

Captures feedback about the paper SKILL (confusing dashboard, clunky stage,
missing verb, bad routing, hard-to-read output) into this skill's `feedback/`
folder. Does NOT fix anything; fixing is a separate revision pass. Distinguish
from paper content: feedback is about the TOOL, not the manuscript.

## Capture: `/haipipe-paper feedback "<text>"`

```
1. Read the active paper + frontier from .paper-console.yaml if present (for context).
2. Write one file: feedback/<YYYY-MM-DD>_<short-slug>.md
   frontmatter: status: open | created | context (paper/stage or "general") | fixed_in: ""
   body: the feedback in the reporter's words, then a trailing "Fix:" line.
3. Confirm captured. Do NOT attempt a fix now.
```

## List: `/haipipe-paper feedback list`

```
Grep feedback/*.md for `status: open` and print them (newest first), with their
context, so a revision pass knows what to fix.
```

## Resolve (during a revision pass, not via this verb)

```
Set status: fixed + fixed_in: <skill version> + a one-line Fix note.
Keep the file as history; never delete it.
```

## Where it lives

`feedback/` is in THIS skill's folder. Each skill keeps its own; there is no
cross-skill shared feedback. It travels with the skill in the submodule, so the
inbox sits right next to the code that needs fixing.
