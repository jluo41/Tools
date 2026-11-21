haipipe-chat · Changelog
========================

## [0.1.0] — 2026-11-21

New skill. A Block holds `cNN_<slug>/` chat sessions beside its `jNN` Jobs and `sNN` Studio topics, one
folder per kept session, numbered in time order (JL 261121: "we have sNN, jNN in blocks, so I think we can
have the cNN, which means the chat"; "we might have a skill named haipipe-chat"). `scripts/new_chat.py`
(`new`, `list`, `check`) is the one writer; the face carries the pass front matter (session, provider,
date, goal, paths, cards), so the Session view (`servers/workbench/ref/three-views.md`) reads it as an
episode. Tests: `tests/test_new_chat.py`.
