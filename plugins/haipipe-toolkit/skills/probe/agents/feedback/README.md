# probe agents — Feedback Inbox

Feedback about the probe AGENTS (the orchestrator / creator / reviewer triad in
`../`), captured by `/haipipe-probe feedback "<text>"` when the text names agent
behavior (capture-time routing), or moved here via
`/haipipe-probe feedback move <file> agents`.

This inbox holds complaints about how the agents BEHAVE, not about the lifecycle
procedures or the console. Typical items: orchestrator collapses to monolithic
execution, expected-vs-actual dispatch mismatch, creator/reviewer loop skipped,
nested-agent dispatch hangs, the orchestrator's tool set is too powerful, a
reviewer's verdict enum is wrong, an agent's independence guarantee is broken.
Everything else (the fn-procedures plan/gather/read/judge/deposit, the console/
dashboard, stage strip, probe id/naming/granularity, the return tail, venue test,
compile-tex, and anything true across the whole lifecycle) lives in the
orchestrator fallback inbox `../../haipipe-probe/feedback/`.

One file per item: `<YYYY-MM-DD>_<slug>.md` (`status: open|fixed`). Fix in a
later revision pass; keep files as history (never delete). The folder a file
lives in IS the record of which unit it concerns; there is no `skill:`
frontmatter field. Shared convention: the orchestrator inbox
`probe/haipipe-probe/feedback/README.md`.
