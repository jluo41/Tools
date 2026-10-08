# subjective-label — Feedback Inbox

Capture complaints, confusions, and wishes about the subjective-label SKILL
while using it, then fix them later in a skill-revision pass. This is feedback
about the TOOL, not the annotation methodology (that's lessons).

## How

```
capture   /haipipe-labeling feedback "<what bugged you>"
          -> infers the target sub-skill, merges or creates in feedback/.
digest    /haipipe-labeling digest
          -> bulk harvest from a session → lesson/ + feedback/.
list      /haipipe-labeling feedback list
          -> shows open items, newest first.
move      /haipipe-labeling feedback move <file> <skill>
          -> re-route a mis-filed item.
resolve   during a revision: set status: fixed + fixed_in + one-line Fix note.
```

Routing map, merge-or-create, and the file schema live in `../fn/feedback.md`.
Capture-only by design: filing a complaint never tries to fix it on the spot.
