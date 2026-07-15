# haipipe-task — Behavioral Preferences (portable)

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

- **Reply under every `> JL:` comment with `>> CC HH:MM:`, and tag it [SOLVED] / [PENDING].** When JL leaves a `> JL:` comment in a doc, resolve it IN PLACE: write the answer on a `>> CC <hour>:<minute>:` line directly beneath the comment, NEVER delete the `> JL:` line, and tag the outcome [SOLVED] (done) or [PENDING] (needs JL's call). An un-tagged `> JL:` line therefore always means genuinely still-open — so a later session never re-litigates a solved point or assumes an open one is closed. (JL, 2026-07-14, haipipe-task SKILL.md review: "以后每一次...我的问题解决了之后，你都要在我的这个上面回复...mark 一下，说这个是 solved".)

- **In doc BODY prose, one sentence per line.** Author skill-doc / manuscript body text with each sentence on its own line (frontmatter, code blocks, and `> JL:`/`>> CC:` comment lines are exempt). Keeps diffs sentence-level and edits surgical. (JL, 2026-07-14, haipipe-task SKILL.md: "在正文中，我们做到每一句话是一行".)

- **A SKILL.md ROUTES; `fn/` and `ref/` hold the contracts — do not re-derive.** Keep the always-loaded SKILL.md to: what-am-I + hierarchy, the verb/route table, the routing protocol, and pointers. Any full contract (gate mechanics, schemas, per-file manifests, keyword tables) lives in a `fn/`/`ref/` file, CITED not restated — restating it inline is how a skill doc bloats and drifts. Test each block: "does the ROUTER need this to dispatch, or is it detail a fn/ owns?" (JL, 2026-07-14/15, the haipipe-task 503→381-line conciseness pass.)

- **Skill `description:` budget ≤ ~55 words.** The frontmatter `description:` is ALWAYS-LOADED trigger text — paid on every session across every skill — so keep it to ONE purpose sentence + the `Trigger:` keyword list, and nothing else (no mechanics, no examples, no rationale; those go in the body/CHANGELOG). Never drop trigger keywords when trimming. Applies fleet-wide, not just one skill. (JL, 2026-07-14, set for haipipe-task then extended to all specialists.)

- **Verify a "done"/pre-written claim against disk before trusting it; report the REAL numbers.** When a log entry, hand-off, or pre-written SOLVED note asserts work is complete ("reflowed all 9", "176 files"), check the actual state before building on it and correct the record with the true counts. A plausible-but-wrong "SOLVED" is worse than an honest open item. On any rename/reflow SWEEP: protect frontmatter/code blocks explicitly (a token-identity check does NOT catch structural breakage), review the diff per-site, and confirm no information was lost. (JL, 2026-07-14: "all 9"→actually 4, "176"→actually 35; the feedback.md frontmatter-mangle catch.)

- **Resolved `> JL:` threads MOVE to the topic's `_LOG.txt` once the body edit lands.** Answer inline with `>> CC HH:MM:`, apply the edit, then migrate the whole thread (JL line verbatim + CC reply) out of the body into `diagram/<topic>/_LOG.txt`, keeping the doc body clean; PENDING threads stay inline until decided. (JL, 2026-07-14: "把我的 comments 都移到这个 log 里面去".)
