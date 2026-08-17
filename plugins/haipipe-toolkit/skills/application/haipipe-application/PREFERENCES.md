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

- **Application owns no evidence Probe; route missing knowledge to a real Insight Page.** Brief and Intervention read settled Task/Insight Pages through PageX. When a premise is missing, keep the application stake on the owning Page, rewrite a consumer-neutral question, and route it through `/haipipe-task insight`. The Insight Page, not Application, runs the real Probe against Task/Discovery sources and settles D→I→K→W. An inline scan is never a substitute for a settled Insight Page. This supersedes the legacy application-local `1-probes/` behavior on 2026-08-17.

- **Missing-Insight release is a user-visible routing decision.** Before commissioning new Task/Discovery work, show the neutral question, required DIKW target, existing PageX matches, destination Task Board, and which Application Aim it blocks. The Task/Insight Page then applies its own Probe release gate. Application never presents or dispatches probe cards of its own.

- **Share the Page substrate, not the delivery vocabulary.** Paper and Application both consume Insight Pages through PageX and both use the shared Page phases. Paper keeps Opening→Narrative→Section; Application keeps Brief→Intervention→Artifact. A change to PageX, Page phases, or the Insight handoff triggers a cross-family review. A change to Paper argument structure does not automatically port into Application intervention structure.

- **No prose without understanding: explain what each sentence DOES before writing it.** The agent must not produce prose (manuscript sentences, story-line drafts, paragraph rewrites) unless it can explain what each sentence does for the reader and why it says THIS and not something else. Production without understanding (知其然不知其所以然) is the root cause of bad writing: the output reshuffles bullet points into plausible-sounding text without grasping the argument. If unable to explain the sentence's job, say so rather than draft. One sentence at a time, grounded in what it DOES, not what it CONTAINS. (JL, 2026-06-26, MISQ-Introduction session: "What is the root cause, in philosophy")

- **Prefer the simplest grouping that captures the point; do not over-split into clever multi-cell taxonomies.** When organizing conditions, claims, options, or findings, reach for the coarsest grouping that still explains the data before inventing finer distinctions. A 2x2 or multi-cell framing that separates items the user sees as ONE group is usually over-engineering; collapse to the simpler grouping unless the finer split clearly earns its keep. JL, 2026-06-26 (MISQ-Introduction): proposed a "two roads to null" 2x2 separating headache and cancer (and flagged recaptioning a figure to split them); JL replied "I think cancer should be together with headache?" and the simpler grouping (both = no opioid discretion) was correct. (kin to the anti-over-split spirit of compress-not-split / one-idea-per-sentence.)
