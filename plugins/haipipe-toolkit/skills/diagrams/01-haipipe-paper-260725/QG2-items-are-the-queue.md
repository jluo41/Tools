# Items to Finish is the queue
state: 🟡 PARTIAL
owner: JL
method: give each checklist item enough structure to claim, execute, verify, and close

## Question
How does an S page express work that a fresh worker can safely execute?

The existing `## Items to Finish` section already says what remains before the page can close. Turning it into the executable queue keeps the obligation, status, result, and human discussion beside the Content they affect.

## Boundary
- ✅ Covered here
  The queue item schema, local item identity, states, and one-writer rule.
- ↪ Covered elsewhere
  Completed handoff placement is `QG3`; phase and worker selection are `QG4`.

## Content
### Proposed item
```markdown
- [ ] I4 · Rebuild the primary regression columns
      phase: revise
      kind: display-render
      from: S-Main-7 · P2.S3
      request: Use the binary exposure as primary.
      acceptance: Prose, caption, columns, estimand, and labels agree.
      status: ready
      owner: --
      blocked-by: --
      handoff: --
```

### State vocabulary
`ready` can be claimed.
`claimed` has one current owner.
`blocked` names the unresolved dependency.
`done` requires verification and a checked box.

### Concurrency
One worker owns one S page at a time.
Different S pages may run in parallel because they do not edit the same queue or Content.

## Items to Finish
- [x] 📋 Reuse Items to Finish
      No second task list is created beside the page.
- [ ] 📐 Freeze the minimal fields
      Keep enough structure for recovery without turning Markdown into a verbose database.
- [ ] 🔒 Define claim and release behavior
      A dead session must not leave an item permanently claimed or allow two page writers.
- [ ] 🧪 Drain a three-item queue
      Verify ready, blocked, and human-decision items stop and resume correctly.

## Where we are
The queue location and candidate schema are selected.
Claim recovery and the exact minimal field set remain open.

## Files
- `haipipe-board/ref/q-template.md`
  The current Items to Finish grammar.
- `haipipe-paper-stage/SKILL.md`
  The future queue loop.
