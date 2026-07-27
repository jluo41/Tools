board agents — Changelog
========================

Agent-scoped history. Versions match the agent frontmatter.

## [1.0.0] — 2026-07-26 — haipipe-board-reviewer-agent

- Added the Board family's first agent.
- Made the role read-only: it runs the mechanical checker, cold-reads prose,
  checks for stale claims, and returns findings without editing the Board.
- Kept Board discovery, synchronization, repair, and rebuilding with the
  original session and `haipipe-board` skill.

