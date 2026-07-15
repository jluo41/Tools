haipipe-task-llm-engine — Changelog
===================================

Skill-scoped changelog (never loaded at invocation; read on demand).
Versions match SKILL.md frontmatter `version:`.
Newest first.


## [1.2.0] — 2026-07-04

- fn/usage.md updated to the CREATE-from-ref/engine flow (was routing users to hand-copy the ProjC PoC, contradicting SKILL.md); LLMCallStore leaf = <case_id> per SKILL.md (was <transport>); example model ids claude-opus-4-8; __pycache__ .pyc pollution removed from ref/engine/.

## [1.1.0] — 2026-07-04

- add missing metadata block (version/last_updated/pointer) + this CHANGELOG (the only task skill lacking one — skill-set review B3).
- wired into the 9_agent domain: named as the agent domain's engine in haipipe-task-for-agent and the orchestrator type table (was an orphan nothing routed to).

## [1.0.0] — (undated)

- baseline: owns code/haiutils/llm_engine/ (Claude Agent SDK + Codex OAuth transports, API-key fallback); CHECK/CREATE/EVALUATE/UPDATE flow against ref/engine/.
