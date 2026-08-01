board agents: Changelog
========================

Agent-scoped history. Versions match the agent frontmatter.

## [0.1.0] · 2026-07-31 · haipipe-board-creator-agent

- Added the family's second agent, and the producer half of the creator and
  reviewer pair the rest of this toolkit already uses.
- Scoped it to exactly ONE page per invocation, so the caller fans out N of
  them in parallel instead of `haipipe-board` writing pages one by one
  (JL 260731).
- Made the parallel safety structural rather than advisory: no Bash tool, so it
  cannot run `build.py`; `board.md` is off limits, so the one file every writer
  would collide on stays the caller's; and no sibling page may be read, so two
  agents cannot start duplicating each other's judgment.
- Gave it the `siblings` field in its assignment packet, which is what lets a
  page write an honest `## Boundary` without reading the board, and what stops
  two pages claiming the same decision.
- Left every shared write with the caller: registering in `board.md`, the lane
  block, one rebuild, one check, and dispatching the reviewer.

## [0.1.0] · 2026-07-26 · haipipe-board-reviewer-agent

- Added the Board family's first agent.
- Made the role read-only: it runs the mechanical checker, cold-reads prose,
  checks for stale claims, and returns findings without editing the Board.
- Kept Board discovery, synchronization, repair, and rebuilding with the
  original session and `haipipe-board` skill.

