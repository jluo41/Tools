haipipe-chat · Changelog
========================

## [0.3.0] — 2026-11-21

As short as possible, updated once per answer (JL 261121: "you should not update the chat everytime, it should
be at the end of the answer"; "I even want to make it as concise as possible"). A QA is three lines at most:
`- **qNN** HH:MM · question`, `→ answer`, `⇢ files`; `## Summary` and `## Changed` are gone (`paths:` keeps the
files). `scripts/chat_hook.py` is a Claude Code Stop hook: it refreshes a chat saved with `--from` (registry
`~/.claude/haipipe-chat/kept.json`) and exits at once for any other session.

## [0.2.0] — 2026-11-21

A chat is kept as QAs, not a transcript (JL 261121: "one QA is one basic element ... we don't need to take so
many details ... but need to track questions, and the outputs"). One QA is one turn: the question verbatim (with
anything sent while the turn ran), the answer (the reply's line 1), the outputs (the turn's Edit and Write files).
`scripts/qa.py` reads them from a Claude Code session file; `new_chat.py new --from`, and `refresh` for a session
that went on. `--transcript` and `transcript.md` are gone; `## Ask` gave way to `## QA`.

## [0.1.0] — 2026-11-21

New skill. A Block holds `cNN_<slug>/` chat sessions beside its `jNN` Jobs and `sNN` Studio topics, one
folder per kept session, numbered in time order (JL 261121: "we have sNN, jNN in blocks, so I think we can
have the cNN, which means the chat"; "we might have a skill named haipipe-chat"). `scripts/new_chat.py`
(`new`, `list`, `check`) is the one writer; the face carries the pass front matter (session, provider,
date, goal, paths, cards), so the Session view (`servers/workbench/ref/three-views.md`) reads it as an
episode. Tests: `tests/test_new_chat.py`.
