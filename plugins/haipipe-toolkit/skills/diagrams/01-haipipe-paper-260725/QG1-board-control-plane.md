# The Board is the control plane
state: 🟡 PARTIAL
owner: JL
method: keep durable context on the page and treat every coding session as replaceable

## Question
Where should a person see, start, steer, and resume paper work?

Remote interaction should not depend on a terminal transcript or a long-lived Claude Code or Codex session. The Board should carry the lifecycle, work queue, comments, state, gate, preview, and completed handoffs so a new worker can resume from disk.

## Boundary
- ✅ Covered here
  The user-facing control plane and the role of an execution session.
- ↪ Covered elsewhere
  Which file owns state is `QF3`; the executable queue is `QG2`; the runner behind the Board is `QG4`.

## Content
### Durable and ephemeral
```
BOARD / S page          durable: context, Content, queue, comments, gate, state
Claude Code / Codex     ephemeral: works one bounded item and may disappear
worker sub-agent        ephemeral: receives a narrow task packet and returns evidence
```

### Interaction direction
Work starts from `Work this item` or `Work this queue` on an S page.
Progress, blockers, results, and handoffs return to that same page.
The CLI may remain as an internal recovery surface, but the user should not need to monitor it.

## Items to Finish
- [x] 🧭 Choose the Board as the remote control plane
      The durable working state lives on pages rather than in session memory.
- [ ] 🖱 Define the two Board actions
      `Work this item` and `Work this queue` need exact stop and refresh behavior.
- [ ] 🔍 Make progress visible
      Claimed owner, blocker, result, verification, and handoff must be visible on the page.
- [ ] 🧪 Resume from a new session
      A fresh session should continue a page without reading the previous transcript.

## Where we are
The architectural direction is accepted.
The Board currently renders the state but does not yet drive the page-first worker loop.

## Files
- `haipipe-board/`
  The durable interaction surface.
- `haipipe-paper-stage/`
  The execution engine behind an S page.
