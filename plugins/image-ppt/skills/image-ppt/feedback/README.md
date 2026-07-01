# image-ppt — Feedback Inbox

Capture complaints, confusions, and wishes about the image-ppt SKILLS or their SCRIPTS while
using them, then fix them later in a revision pass. This is feedback about the TOOL (a script is
clunky, compose mis-places text, a flag is missing), NOT about the vectorization craft (that's
`lesson/`).

## How

```
capture   /image-ppt feedback "<what bugged you>"
          -> infers the target sub-skill/script, merges or creates in feedback/.
digest    /image-ppt digest
          -> bulk harvest from a session -> lesson/ + feedback/.
list      /image-ppt feedback list
          -> shows open items, newest first.
move      /image-ppt feedback move <file> <target>
          -> re-route a mis-filed item.
resolve   during a revision: set status: fixed + fixed_in + a one-line Fix note.
```

Routing map, merge-or-create rules, and the file schema live in `../fn/feedback.md`.
Capture-only by design: filing a complaint never tries to fix it on the spot.
