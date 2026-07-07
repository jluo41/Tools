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

- **Communicate via ASCII diagrams, not walls of prose.** Show plans, options,
  and "my thinking" as emoji-rich ASCII (boxes + arrows); keep prose to a one-line
  ask. (also mirrored in auto-memory: feedback_communicate_via_diagram_ascii)

- **Always run the REAL probe in the PROBE phase — never substitute an inline scan.** In any stage's PROBE phase, the evidence work MUST go through the ledgered worker path: materialize the stage's `_PROBE/PPNN_*.md` cards + the `1-probe-plans/README.md` index, then dispatch `Agent(haipipe-probe-orchestrator-agent)` per card (BOOKKEEP → DISPATCH → TRANSLATE → VERIFY). A light web scan woven into the stage prose is a DRAFT-phase scoping aid, not a probe; findings that never landed project-side (empty `refs:`) leave the PROBE phase INCOMPLETE and the `_PROBE/` folder empty. Do not promote a stage past PROBE on an inline scan. JL, 2026-07-07 (paper-side origin, Paper-CGMtoCyclePhase seed: "you need to always run the real probes in the probe phase"); family-generic — applies verbatim to every application stage. (also in auto-memory: feedback_always_run_real_probes)

- **Alignment watch: paper drift triggers an application port review.** Any commit touching `paper/2-phase/` or `paper/1-lifecycle/{0-seed,1-claims}` triggers an application port review BEFORE the next application work round. Cheap by design: grep the `git log` of the paper tree at enter time; no automation. Rationale: paper drifted the SAME DAY as the round-1 port (2026-07-06 → 07-07); this line exists to stop chasing. JL, 2026-07-07 (SOP paper-alignment round 2, R6).

- **No prose without understanding: explain what each sentence DOES before writing it.** The agent must not produce prose (manuscript sentences, story-line drafts, paragraph rewrites) unless it can explain what each sentence does for the reader and why it says THIS and not something else. Production without understanding (知其然不知其所以然) is the root cause of bad writing: the output reshuffles bullet points into plausible-sounding text without grasping the argument. If unable to explain the sentence's job, say so rather than draft. One sentence at a time, grounded in what it DOES, not what it CONTAINS. (JL, 2026-06-26, MISQ-Introduction session: "What is the root cause, in philosophy")

- **Prefer the simplest grouping that captures the point; do not over-split into clever multi-cell taxonomies.** When organizing conditions, claims, options, or findings, reach for the coarsest grouping that still explains the data before inventing finer distinctions. A 2x2 or multi-cell framing that separates items the user sees as ONE group is usually over-engineering; collapse to the simpler grouping unless the finer split clearly earns its keep. JL, 2026-06-26 (MISQ-Introduction): proposed a "two roads to null" 2x2 separating headache and cancer (and flagged recaptioning a figure to split them); JL replied "I think cancer should be together with headache?" and the simpler grouping (both = no opioid discretion) was correct. (kin to the anti-over-split spirit of compress-not-split / one-idea-per-sentence.)
