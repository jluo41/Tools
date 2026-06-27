# haipipe-insight — Behavioral Preferences (portable)

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

- **No prose without understanding: explain what each sentence DOES before writing it.** The agent must not produce prose (manuscript sentences, story-line drafts, paragraph rewrites) unless it can explain what each sentence does for the reader and why it says THIS and not something else. Production without understanding (知其然不知其所以然) is the root cause of bad writing: the output reshuffles bullet points into plausible-sounding text without grasping the argument. If unable to explain the sentence's job, say so rather than draft. One sentence at a time, grounded in what it DOES, not what it CONTAINS. (JL, 2026-06-26, MISQ-Introduction session: "What is the root cause, in philosophy")

- **Prefer the simplest grouping that captures the point; do not over-split into clever multi-cell taxonomies.** When organizing conditions, claims, options, or findings, reach for the coarsest grouping that still explains the data before inventing finer distinctions. A 2x2 or multi-cell framing that separates items the user sees as ONE group is usually over-engineering; collapse to the simpler grouping unless the finer split clearly earns its keep. JL, 2026-06-26 (MISQ-Introduction): proposed a "two roads to null" 2x2 separating headache and cancer (and flagged recaptioning a figure to split them); JL replied "I think cancer should be together with headache?" and the simpler grouping (both = no opioid discretion) was correct. (kin to the anti-over-split spirit of compress-not-split / one-idea-per-sentence.)
