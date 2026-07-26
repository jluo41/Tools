# Handoff stays on the item
state: 🟡 PARTIAL
owner: JL
method: close the originating queue item with paths and verification instead of creating a sidecar

## Question
Where does the result of a completed queue item live?

A separate Handoff file, request file, or per-change report splits the request from the result and creates another queue that can drift. The completed item should carry the live artifact, preview, verification, and next consumer in its own `handoff:` record.

## Boundary
- ✅ Covered here
  The paper-side location of completed work and the rule against request or Handoff sidecars.
- ↪ Covered elsewhere
  Evidence remains in its bank-owned QA artifact under `QD1`; Display ownership is `QI1`.

## Content
### Existing Display
A request for `display04` goes directly into `S-Display-4`.
The worker updates the same Display unit and closes the item on that page.
The requesting Section keeps the stable `display_id`.

### New Display
A not-yet-allocated Display begins as one item on the Display stage page.
When accepted, the creator makes `S-Display-N`, moves the item verbatim into it, and removes it from the unallocated queue.
The new S page is the Display, not a request sidecar.

### Handoff contents
```
handoff:
  artifact: live output path
  preview: inspectable rendering
  verification: what was checked
  consumer: page or adapter that uses it next
```

## Items to Finish
- [x] 🚫 Reject `_DISPLAY_REQUEST.md`
      Existing Display work goes to its owning page and new work starts on the Display stage page.
- [x] 📎 Reject a separate Handoff file
      The originating item carries its own result and downstream pointer.
- [ ] 📐 Define the compact handoff syntax
      It must remain readable Markdown and support more than Display work.
- [ ] 🧹 Migrate future writers
      Stop skills from generating request sidecars or writing completed work only to chat.

## Where we are
The no-sidecar ruling is explicit.
Current paper skills still contain `_DISPLAY_REQUEST.md` routes and have not been migrated.

## Files
- `stages/4-display/stage.md`
  Still declares the retired inbox.
- `haipipe-paper-draft-display/SKILL.md`
  Still files Display request rows.
