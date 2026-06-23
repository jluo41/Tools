---
status: open
created: 2026-06-23
context: probe + task reviewer agents / G2 integrity gate (discovered during JAMANO probe dispatch review)
fixed_in: ""
---

Both the probe reviewer and task reviewer agents declared Codex MCP tools (mcp__codex__codex, mcp__codex__codex-reply) for out-of-family independence in the Judge gates. But no Codex MCP server is configured in the project settings — those tools silently fail at runtime.

The Codex dependency was the architectural backbone of the builder!=judge principle: the retired probe-integrity-auditor-agent and claim-verifier-agent used Codex as an independent model to read source files and verify numbers. When they were merged into the unified probe-reviewer-agent, the Codex tools were carried over but never tested against the actual MCP config.

The probe agents CODE_REVIEW.md (written the same day as the agents) already flagged this:
> "The builder-is-not-judge principle relied on Codex as an out-of-family reviewer. Without Codex, the merged reviewer judges its own reading of evidence, weakening the independence guarantee."

PARTIALLY FIXED this session:
1. Reviewer agent v1.1.0 removes Codex tools and documents the replacement approach.
2. A deterministic G2 integrity checker script (g2_integrity_check.py) is being built to cross-reference evidence.md numbers against source CSVs — zero model involvement for number-tracing.
3. G1 (structural) and G3 (claim) use fresh-agent reasoning (separate agent, no memory of creation) for independence.

The independence guarantee is now:
- G2: deterministic code (strongest — no hallucination possible)
- G1/G3: fresh-context agent (good — no shared memory with creator, but same model family)

Remaining: the deterministic G2 script needs testing on all 4 probes. The fresh-agent G1/G3 approach needs one end-to-end test to confirm the dispatcher→reviewer handoff works.

Design question for later: should we support pluggable reviewer backends (Codex when available, Gemini, or code-only) so the independence tier can be upgraded when an MCP server is configured?
