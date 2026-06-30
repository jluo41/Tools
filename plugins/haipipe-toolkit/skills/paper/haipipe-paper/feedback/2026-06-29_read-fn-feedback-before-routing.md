---
status: fixed
created: 2026-06-29
updated: 2026-06-29
occurrences: 1
context: §3 theory session, feedback routing
fixed_in: "v2.1.0 (added MANDATORY callout in routing logic to read fn/feedback.md first)"
regressed: ""
---

When /haipipe-paper feedback is invoked, the agent must read fn/feedback.md FIRST and follow the capture-time routing protocol. The agent defaulted to creating an auto-memory file instead of routing through the skill feedback inbox system. The fn/feedback.md file defines the keyword→skill map, cross-cutting guard, merge-or-create protocol, and inbox paths. These must be followed, not bypassed.
