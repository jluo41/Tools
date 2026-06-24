# haipipe-paper — Behavioral Preferences (portable)

Global "how to work" preferences for this skill, kept HERE under git so they
survive a machine change. The `~/.claude` auto-memory is machine-local and does
NOT sync across computers; this file does (it travels with the Tools submodule).
ALWAYS read and honor these in a paper session.

These are global BEHAVIORAL preferences (how the agent should act), NOT skill
defects — defects go to the `feedback/` inboxes. Entries are added by
`/haipipe-paper digest` / `feedback` when a global pref is flagged, or by hand,
using merge-or-create (one entry per topic; update, don't duplicate).

## Preferences

- **Communicate via ASCII diagrams, not walls of prose.** Show plans, options,
  and "my thinking" as emoji-rich ASCII (boxes + arrows); keep prose to a one-line
  ask. Preview confusing figures/displays as a `/diagram-ascii` sketch rather than
  a dense paragraph. (also mirrored in auto-memory: feedback_communicate_via_diagram_ascii)

- **Route data/artifact work through the haipipe-task lifecycle agents, not a
  generic subagent.** When paper/probe work needs a data artifact built (parse
  aggregated logs into a table, run a regression, materialize a display), dispatch
  it via `haipipe-task-orchestrator-agent` (Plan -> Build -> Execute -> Report with
  creator/reviewer gates and a reproducible task-folder), NOT a generic
  `general-purpose` subagent that edits the artifact directly. Reserve a plain
  subagent for non-task work (broad reads, recon, doc edits). Route is probe -> task.
  (also mirrored in auto-memory: feedback_data_work_via_haipipe_task_agents)

- **Keep manuscript paragraphs to 4-5 sentences.** Not too many, not too few: 4-5
  sentences (or sentence-points) per paragraph is the target, with ~6 the hard
  ceiling (compress, do not split). Applies to minimap sentence-points and to
  write/edit prose. (refines auto-memory: feedback_compress_not_split)
