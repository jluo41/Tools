# Handoff stays on the item
state: ✅ SETTLED
owner: JL
method: close the originating queue item with paths and verification instead of creating a sidecar

## Question
Where does the result of a completed queue item live?

A separate Handoff file, request file, or per-change report splits the request from the result and creates another queue that can drift. The completed item should carry the live artifact, preview, verification, and next consumer in its own `handoff:` record.

## Boundary
- ✅ Covered here
  The paper-side location of completed work and the rule against request or Handoff sidecars.
- ↪ Covered elsewhere
  Evidence remains in its bank-owned QA artifact under `QBb1`; Display ownership is `QD1`.

  ↪ On the boardform board: whether a page can be written from the browser at all is `QE4` on the boardform board, and whether the page stopped delivering what it promised is `QA9` there. What is asked here is where a paper stage's completed work is recorded.
## Diagram
```
 THE RESULT LIVES ON THE ITEM THAT ASKED FOR IT

  ✗ SIDECARS                        ✅ ON THE ITEM
   request.md ─┐                     - [x] I4 · Rebuild the columns
   HANDOFF.md ─┼─ a SECOND queue           request:   …
   report.md  ─┘  that can drift           handoff:
   the ask and the answer                    artifact:     live output path
   in different files, and                   preview:      inspectable render
   nothing keeps them married                verification: what was checked
                                             consumer:     who uses it next

 TWO PATHS, ONE RULE

  EXISTING display                  NEW display
   the request goes straight         starts as ONE item on the Display
   into S-Display-4                  stage page (unallocated)
   worker updates that unit                 │  accepted
   closes the item there                    ▼
   the Section keeps the             creator makes S-Display-N and moves
   stable display_id                 the item VERBATIM into it
                                     the new S page IS the display,
                                     not a request sidecar

 WHAT STILL LIVES ELSEWHERE, correctly
   evidence stays in its BANK-owned QA artifact (QBb1).
   the handoff POINTS at it; it never copies it.
```

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
