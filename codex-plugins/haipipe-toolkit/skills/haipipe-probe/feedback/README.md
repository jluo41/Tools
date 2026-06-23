# haipipe-probe - Feedback Inbox

Capture complaints, confusions, and wishes about THIS skill (its output is hard
to read, a step is clunky, a verb is missing) while using it, then fix them later
in a skill-revision pass. This is feedback about the TOOL, not a probe verdict.

Each skill keeps its OWN feedback/ folder. There is no cross-skill shared feedback.

## How

```
capture   /haipipe-probe feedback "<what bugged you>"
          -> writes one file here: <YYYY-MM-DD>_<slug>.md (status: open)
review    /haipipe-probe feedback list
          -> lists the open items so a revision pass knows what to fix
resolve   during a revision: set status: fixed + fixed_in + a one-line Fix note
          (keep the file as history; do not delete)
```

## One file per item

```
---
status: open | fixed
created: YYYY-MM-DD
context: <probe/step that triggered it, or general>
fixed_in: ""          # skill version when resolved
---
<the feedback, in the reporter's words>

Fix: <added when resolved>
```

Capture-only by design: filing a complaint never tries to fix it on the spot.
Fixing is a separate, deliberate pass over the open items.
