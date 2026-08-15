# figure-to-svg plugin — Feedback Inbox

Capture complaints, confusions, and wishes about the figure-to-svg plugin SKILLS or their SCRIPTS while
using them, then fix them later in a revision pass. This is feedback about the TOOL (a script is
clunky, compose mis-places text, a flag is missing), NOT about the vectorization craft (that's
`lesson/`).

## How

```
capture   /figure-to-svg feedback "<what bugged you>"
          -> infers the target sub-skill/script, merges or creates in feedback/.
digest    /figure-to-svg digest
          -> bulk harvest from a session -> lesson/ + feedback/.
list      /figure-to-svg feedback list
          -> shows open items, newest first.
move      /figure-to-svg feedback move <file> <target>
          -> re-route a mis-filed item.
resolve   during a revision: set status: fixed + fixed_in + a one-line Fix note.
```

Routing map, merge-or-create rules, and the file schema live in `../fn/feedback.md`.
Capture-only by design: filing a complaint never tries to fix it on the spot.
