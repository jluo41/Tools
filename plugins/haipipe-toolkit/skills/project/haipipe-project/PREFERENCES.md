# haipipe-project — Behavioral Preferences (portable)

Global "how to work" preferences for this skill, kept HERE under git so they
survive a machine change. The `~/.claude` auto-memory is machine-local and does
NOT sync across computers; this file does (it travels with the Tools submodule).
ALWAYS read and honor these.

These are global BEHAVIORAL preferences (how the agent should act), NOT skill
defects (those go to the `feedback/` inbox). Kept in sync across all orchestrators
by `/haipipe-paper digest`'s global-pref fan-out (merge-or-create; one entry per
topic -- update, don't duplicate).

## Preferences

- **Communicate via ASCII diagrams, not walls of prose.** Show plans, options,
  and "my thinking" as emoji-rich ASCII (boxes + arrows); keep prose to a one-line
  ask. (also mirrored in auto-memory: feedback_communicate_via_diagram_ascii)
