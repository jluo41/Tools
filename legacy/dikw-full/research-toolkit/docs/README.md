# docs/

Companion docs for research-toolkit. For the toolkit's ideology and workflow
maps, see the top-level `PRINCIPLES.md` and `WORKFLOW.md`. This folder holds
operational guides inherited from ARIS and kept because they describe infra
(reviewers, MCP servers, session files) we use unchanged.

===========================================================================
Review setup
===========================================================================

- `CODEX_CLAUDE_REVIEW_GUIDE.md` / `_CN.md` -- install Codex MCP and enable the
  Codex-reviewed variants of research-review, auto-review-loop, etc. Required
  for every skill that offers a `reviewer: codex` mode.
- `CODEX_GEMINI_REVIEW_GUIDE.md` / `_CN.md` -- same, with Gemini as the external
  reviewer.

Both paths layer onto `skills/00_meta/skills-codex/` (base runtime mirror) via
`skills/00_meta/skills-codex-claude-review/` or
`skills/00_meta/skills-codex-gemini-review/`.

===========================================================================
LLM routing
===========================================================================

- `LLM_API_MIX_MATCH_GUIDE.md` -- when to use Claude vs GPT vs open-weight
  models for different skill roles.
- `MiniMax-GLM-Configuration.md` -- specific configuration for MiniMax and GLM
  endpoints.
- `MINIMAX_MCP_GUIDE.md` -- setting up the MiniMax MCP server used by
  `auto-review-loop-minimax`.
- `MODELSCOPE_GUIDE.md` -- ModelScope endpoint setup.

===========================================================================
Project conventions
===========================================================================

- `PROJECT_FILES_GUIDE.md` / `_CN.md` -- canonical paper project layout
  (`notes/`, `figures/`, `output/`) and what lives in each directory.
  Used by `paper-bootstrap`, `manuscript-optimizer`, and anything that
  touches the `notes/` discipline.
- `NARRATIVE_REPORT_EXAMPLE.md` -- example of a narrative report that feeds
  into `paper-plan` and downstream writing.
- `SESSION_RECOVERY_GUIDE.md` / `_CN.md` -- recover from interrupted sessions;
  where state lives and how to resume.
- `WATCHDOG_GUIDE.md` / `_CN.md` -- operating `tools/watchdog.py` for
  long-running experiment supervision.

===========================================================================
Not here
===========================================================================

IDE / platform adapters (Cursor, Trae, AntiGravity, OpenClaw, Alibaba Coding
Plan) were removed because this toolkit runs only in Claude Code. If you need
any of them, consult the upstream ARIS repo directly.
