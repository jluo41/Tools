# haipipe-application — Behavioral Preferences (portable)

Global "how to work" preferences for this skill, kept HERE under git so they
survive a machine change. The `~/.claude` auto-memory is machine-local and does
NOT sync across computers; this file does (it travels with the Tools submodule).
ALWAYS read and honor these.

These are global BEHAVIORAL preferences (how the agent should act), NOT skill
defects (those go to the `feedback/` inbox). Kept in sync across all orchestrators
by `/haipipe-paper digest`'s global-pref fan-out (merge-or-create; one entry per
topic -- update, don't duplicate).

## Preferences

- **DEFAULT REPLY MODE = /diagram-ascii (JL 2026-07-09: "please set this as the default mode for the skills").** Every skill reply renders its substance as emoji-rich ASCII diagrams per the diagram-ascii skill conventions: dense emoji (every box/row/status), boxes + arrows, `── [N/TOTAL] Title ──` headers when a reply carries 3+ diagrams, compact status strips. Prose shrinks to one-line asks and connective sentences — if it can be a diagram, it IS one. Applies to plans, options, findings, state reports, release menus, and "my thinking". (also in auto-memory: feedback_diagram_ascii_default_mode)

- **Design never Probes; the Application-local Insight Page does.** Brief, Design, and Artifact Pages consume accepted Page evidence through PageX. When a design premise is missing, keep the application stake on the blocked Page, rewrite it as one Insight question, and open or refresh that Page under `1-insights/`. The Insight Page may run Probe against Task/Discovery sources under Task-backed source/run/staleness rules, settles D→I→K, adds application-contextual W, and publishes a Design Handoff. An inline scan inside a Design Page is never a substitute.

- **Missing-Insight release is a user-visible routing decision.** Before commissioning new Task/Discovery work, show the question, required DIKW target, existing PageX matches, destination local Insight Page, and which Brief or Design Aim it blocks. The local Insight Page then applies the Task-backed Probe release gate; the blocked Design Page never dispatches Probe cards itself.

- **Share the Page substrate, not the delivery vocabulary.** Paper and Application both consume Pages through PageX and both use the shared Page phases. Paper keeps Opening→Narrative→Section; Application keeps Brief→Insights→Design→Artifacts. A change to PageX, Page phases, or the Insight handoff triggers a cross-family review. A change to Paper argument structure does not automatically port into Application message structure.

- **No prose without understanding: explain what each sentence DOES before writing it.** The agent must not produce prose (manuscript sentences, story-line drafts, paragraph rewrites) unless it can explain what each sentence does for the reader and why it says THIS and not something else. Production without understanding (知其然不知其所以然) is the root cause of bad writing: the output reshuffles bullet points into plausible-sounding text without grasping the argument. If unable to explain the sentence's job, say so rather than draft. One sentence at a time, grounded in what it DOES, not what it CONTAINS. (JL, 2026-06-26, MISQ-Introduction session: "What is the root cause, in philosophy")

- **Prefer the simplest grouping that captures the point; do not over-split into clever multi-cell taxonomies.** When organizing conditions, claims, options, or findings, reach for the coarsest grouping that still explains the data before inventing finer distinctions. A 2x2 or multi-cell framing that separates items the user sees as ONE group is usually over-engineering; collapse to the simpler grouping unless the finer split clearly earns its keep. JL, 2026-06-26 (MISQ-Introduction): proposed a "two roads to null" 2x2 separating headache and cancer (and flagged recaptioning a figure to split them); JL replied "I think cancer should be together with headache?" and the simpler grouping (both = no opioid discretion) was correct. (kin to the anti-over-split spirit of compress-not-split / one-idea-per-sentence.)
