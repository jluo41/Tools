# haipipe-paper-revise · v0.2.2
state: ✅ SETTLED · account written; the acceptance test is open in Items
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Question
How can revision make a paper more accurate, logically connected, and scientifically readable without quietly changing the evidence, claim scope, or the author's original sentence?

This page brings the three revision layers into one contract: evidence bindings, paragraph argument, and sentence-level scientific prose.
It also distinguishes the normal direct REVISE from the author's original-preserving candidate review.

## Diagram
<!-- haipipe:skill:tree:start 150deccb409110e5 paper/2-phase/2-revise/haipipe-paper-revise -->

```
haipipe-paper-revise/
  feedback/
    2026-07-09_revise-skipped-humanize-and-outline-first.md    34 ln  "the revise phase didn't really work." (JL, 2026-07-09)
    README.md                            4 ln  haipipe-paper-revise -- Feedback Inbox
  CHANGELOG.md                          67 ln  haipipe-paper-revise — Changelog
  SKILL.md                             182 ln  Skill: haipipe-paper-revise (internal phase worker)
```

<!-- haipipe:skill:tree:end -->

```
PROBE-landed answers + venue contract + source Markdown
                         │
                         ▼
  1. EVIDENCE       value · display · citation bindings; never fabricate
  2. PARAGRAPH      claim → evidence → warrant → implication; no logic jump
  3. SENTENCE       venue register + SciWrite clarity + human academic voice
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
direct REVISE                      candidate-diff REVIEW
edit .md → why-comments → tex      retain source → adjacent > Note only
CHECK reviews the result            no tex sync; not a completed REVISE
```

## Content
<!-- haipipe:skill:body:start 150deccb409110e5 paper/2-phase/2-revise/haipipe-paper-revise -->

**haipipe-paper-revise** · `0.2.2` · last shipped 2026-07-27

- folder   `paper/2-phase/2-revise/haipipe-paper-revise/`
- tools    Bash, Read, Write, Edit, Grep, Glob, Skill
- summary  REVISE phase worker (internal): default direct revision plus an author-selected candidate-diff mode for auditable, original-preserving wording review.

### SKILL.md



Skill: haipipe-paper-revise (internal phase worker)
====================================================

REVISE phase worker.
Called by stage skills (pitch, narrative, section-edit) to rewrite draft prose to venue-quality after PROBE.
The stage defines WHAT was drafted.
This skill defines HOW to revise it.

**What the REVISE contract means.** By default, the agent CHANGES the prose directly and leaves `%% {CC-*}:` comments explaining WHY each non-trivial change was made.
The human does not approve changes here; the human gives preferences in CHECK (via `> USER:` comments), and a REVISE restart responds to them.

**Author-selected exception.** When the author explicitly asks to retain the original sentence, show deletions/additions, use the Board's sentence apparatus, or review candidates before applying, run **candidate-diff mode**. This mode leaves every original sentence unchanged and writes a `> Note:` candidate beneath it. It is a review artifact, not a completed direct REVISE.

**Proof-carrying (binding).** A stage hub reaches REVISE ONLY through `Skill(haipipe-paper-revise)` — hand-editing the prose inline is a protocol violation ("the REVISE phase did not happen").
Every run writes a `[REVISE]` entry in the owning S page's `## Log` with a
workers line: `workers: place ✓ content ✓ humanizer ✓ results --` (✓ ran · --
skipped-with-reason). `checks.sh --stage-page` fails a `[REVISE]` entry without it.
Order of operations: revise the working `.md` FIRST, then sync to tex — never tex-first (the .md is the document the human reads and comments in).

**Not user-facing.** Users invoke stage skills:
```
/haipipe-paper pitch        → pitch skill calls this internally for REVISE phase
/haipipe-paper narrative    → narrative skill calls this internally for REVISE phase
/haipipe-paper section-edit §3  → section-edit skill calls this internally
```


- 1 · What REVISE means
      REVISE = put the landed answers into the prose, then rewrite those sentences to venue-quality, applying changes directly with why-comments.
      Four workers, each with a different lens:
      ```
      haipipe-paper-revise-place                SUBSTITUTE landed answers into placeholders (runs FIRST)
      haipipe-paper-revise-content              WHAT sentences say (accuracy, completeness, claims)
      haipipe-paper-revise-humanizer            HOW sentences sound (de-AI audit, voice)
      haipipe-paper-revise-results              results-specific (figure narration, effect reporting)
      ```
      All four apply rules directly.
      No comment-first protocol, no human gate.
      The agent reads prose-quality.md + venue style profile, applies fixes, leaves `%% {CC-*}:` why-comments, and moves on.
      Human review of revised prose happens in CHECK.

- 2 · Revision modes

- 2.1 · Default direct mode
      Apply the four workers to the source `.md`, leave `%% {CC-*}:` why-comments for non-trivial edits, then sync the accepted source to TeX. This is the normal autonomous REVISE path.

- 2.2 · Candidate-diff mode
      Use this mode only after an explicit author request for reviewable alternatives. Read `haipipe-paper-revise-humanizer/ref/venue-sciwrite.md` before proposing any change.
      1. Keep the source sentence, its citations, values, display lanes, and user comments byte-intact.
      2. Put one complete proposed sentence in an adjacent `> Note:` lane. Mark removed text as `~~removed~~` and inserted or replacement text as `**inserted**`.
      3. Append `· <verified model label> · YYYY-MM-DD`; never invent a model name or version.
      4. Make only minimum, meaning-preserving changes. Do not add or remove a claim, qualifier, causal strength, number, citation, display reference, or defined term.
      5. Place the Note after any existing adjacent `> Citation:`, `> Value:`, or `> Display:` lanes so the entire apparatus folds under the same sentence.
      6. Do not sync candidate Notes to TeX, call the source revised, or mark REVISE complete. Promote only author-accepted candidates in a later direct REVISE or CHECK action.

- 3 · Universal rules
      All revise workers read and enforce `../../REF/prose-quality.md`. Installed skills flatten the tree (symlinks under `~/.claude/skills/`), so that relative path is NOT reliable — locate it layout-agnostically:
      `PQ=$(find -L ~/.claude/skills ./.claude/skills "${CLAUDE_PLUGIN_ROOT:-/nonexistent}" -maxdepth 4 -path '*2-phase/REF/prose-quality.md' 2>/dev/null | head -1)` (absent → apply the rules below, note the gap in the S page's `## Log`).
      The rules:
      - One idea per sentence
      - No em-dashes
      - Compress, don't split
      - No AI voice
      - Use verified numbers
      - <=6 sentences per paragraph
      - Pn.Sn markers on every sentence
      Venue-specific norms come from
      `0-lifecycle/2-venue/S-Venue-0-venue.md` and override where they conflict.
      Read a venue pack directly only as fallback when that S page is absent, or as a
      deep dive via its `[source: ...]` tags.
      **Venue guard** (same rule as DRAFT): when revising a venue-ALIGNED artifact, no `venue:` pinned in S-Venue-0-venue.md -> STOP with `status: blocked` and point the user to `/haipipe-paper venue`.
      Venue pinned -> read `S-Venue-0-venue.md` FIRST; fall back to the pinned pack
      only when it is absent. If a per-section style file is missing, flag the gap in
      the S page's `## Items to Finish` and `## Log`, and in CHECK.
      Never silently invent venue norms.

- 4 · Dispatch logic
      Read the section outline and tex to determine which workers to run:
      | Worker | Run when | Skip when |
      |---|---|---|
      | place | the artifact carries any placeholder | no placeholder in the artifact |
      | content | always | never |
      | humanizer | always | never (AI-authored prose reliably contains patterns) |
      | results | section is Results or contains figure/table narration | non-results sections |
      When no specific worker is named, run in order: place → content (incl. its weave step for ¶-flow) → humanizer → results (if applicable).
      `place` runs FIRST and the order is binding: substituting after the prose workers would re-open sentences they had already finished, so the shipped text would never have been reviewed in its final form.

- 5 · Automation
      REVISE is fully automatic.
      The agent:
      1. Reads the working .md and current .tex
      2. Uses default direct mode or the author-selected candidate-diff mode above
      3. In direct mode, applies prose-quality.md rules to the .MD, leaves `%% {CC-*}:` why-comments on non-trivial changes, and syncs the revised .md → .tex (Pn.Sn markers; tex prose never edited directly)
      4. In candidate-diff mode, writes only `> Note:` lanes in the .MD and rebuilds the Board; it does not change or sync the manuscript prose
      5. Writes the owning S page's `[REVISE]` Log entry only for a completed direct run; candidate-diff mode records an `[REVIEW]` entry if the project uses logs
      6. Hands back to the stage hub, which opens CHECK after direct REVISE — never commit or conclude before the CHECK gate opens
      No stopping for comments mid-pass.
      No waiting for approval.
      The CHECK phase is where the human reviews everything and states preferences.

- 6 · Phase status
      Derive revise status from disk:
      ```
      revise ✅    tex synced from revised outline, all rules applied
      revise 🚀    revise in progress
      revise ⬜    not yet started (PROBE must complete first)
      ```

- 7 · Relation to other phases
      ```
      DRAFT → PROBE → REVISE (this) → CHECK
                          │
                          ├── haipipe-paper-revise-place       (SUBSTITUTE landed answers, FIRST)
                          ├── haipipe-paper-revise-content     (WHAT: accuracy, claims)
                          ├── haipipe-paper-revise-humanizer   (HOW: de-AI voice)
                          └── haipipe-paper-revise-results     (results-specific)
      ```
      REVISE reads what PROBE landed in each entry's `### a-executor`, PLACES it into the prose (discharging the placeholder's bracket), and rewrites those sentences into final prose.
      CHECK then verifies the revised result.

- 8 · Return contract
      ```
      status:    ok | blocked
      section:   <section-name>
      workers:   place <status> │ content <status> │ humanizer <status> │ results <status>
      next:      <suggested command>
      ```

- 9 · Who calls this skill
      Stage skills call this as their REVISE phase:
      | Stage skill | What this skill revises |
      |---|---|
      | pitch | cover letter prose (readability rules) |
      | narrative | story beat prose (arc/flow coherence) |
      | section-edit | section tex (full revise: content + humanizer + results) |
      Note: whether a stage runs REVISE is declared by its own contract's `phases:` list, not by this table. Argument docs (seed, resource, claims) need no venue-quality POLISH — but they DO run REVISE when their contract lists it, because REVISE is also where a landed answer is woven back into the sentences that cite it and the `[Q-<Stage>-<n>]` bracket is discharged. `2a-venue` is the one stage that genuinely omits REVISE: it produces a contract, not prose.
      Resource has ONE exception: a woolly fitness ruling ("probably fine") is a DEFECT, not an answer -- when an **A** does not say what it KILLS, resource does NOT skip REVISE and sharpens it instead.

- 10 · Sibling phase workers
      | Phase | Worker | Called after |
      |---|---|---|
      | DRAFT | haipipe-paper-draft | -- |
      | PROBE | haipipe-paper-probe | DRAFT |
      | REVISE (this) | haipipe-paper-revise | PROBE |
      | CHECK | haipipe-paper-check | REVISE |
### The other files

2 files besides `SKILL.md` and `CHANGELOG.md`, each with the purpose it states about itself. They are described here, not reproduced: the folder is the copy.

```
feedback/2026-07-09_revise-skipped-humanize-and-outline-first.md    34 ln  "the revise phase didn't really work." (JL, 2026-07-09)
feedback/README.md                   4 ln  haipipe-paper-revise -- Feedback Inbox
```

<!-- haipipe:skill:body:end -->

## Items to Finish
- [x] 🧬 Separate the three revision layers
      Evidence revision binds only landed values, displays, and citations.
      Paragraph revision makes the warrant and sequence explicit.  Sentence
      revision applies venue norms, SciWrite clarity, and a human academic
      voice.  None may invent a fact to make prose smoother.
- [x] 🛡️ Establish the invariants against over-editing
      Preserve claim scope, causal strength, technical terms, evidence-tied
      hedging, numbers, citations, and display references.  Anti-AI revision is
      not merely deleting adjectives; it removes defensive repetition and
      empty detail while making the actual inferential link readable.
- [x] ✏️ Establish the two modes
      Default direct mode runs `place → content → humanizer → results?`, edits
      source Markdown, leaves why-comments for non-trivial edits, and only then
      synchronizes accepted prose to TeX.  Candidate-diff mode is allowed only
      when the author asks to retain and inspect the original.
- [x] 📝 Establish the candidate sentence apparatus
      ```markdown
      Agreeableness reflects an individual's tendency toward cooperation.
      > Note: Agreeableness reflects ~~an individual's~~ **a** tendency toward cooperation. · <verified model label> · YYYY-MM-DD
      ```
      `~~removed~~` renders as deletion and `**inserted**` renders as bold
      addition.  The Note follows any Citation, Value, or Display lane, leaves
      the original byte-intact, and never synchronizes to TeX by itself.
- [ ] 🧪 Run a matched direct/candidate review
      Use the same venue-aligned section to verify that direct mode records
      provenance and syncs only accepted prose, while candidate mode produces
      legible diffs without altering claims or the manuscript.

## Where we are
The revision page now makes a substantive distinction that generic "humanize" tools miss: prose quality comes after evidence integrity and paragraph logic, not instead of them.
The remaining acceptance test compares both modes on the same source section and verifies that candidate notes never leak into TeX.

## Log
260727 · Audited against `board.md`'s decision-only rule, which says `state:` is about the DECISION and that implementation does not gate this board. Every open item here is implementation or a test, not an undecided question, so the page was reporting itself as open because code was missing. Flipped with no ruling made.
260727 1455 · Created the REVISE skill page from `paper/2-phase/2-revise/haipipe-paper-revise/`.
It incorporates the venue-grounded SciWrite and anti-AI-prose work as a three-layer revision model, not a generic word-substitution pass.

<!-- haipipe:skill:log:start 150deccb409110e5 paper/2-phase/2-revise/haipipe-paper-revise -->

Converted from the skill's own `CHANGELOG.md`: 11 releases.

260726 · `0.2.1` · provenance lives on the S page
      - `[REVISE]` worker proof now lives in the owning S page's `## Log`.
      - `checks.sh --stage-page` replaces the retired `_LOG` input.
      - Venue guidance reads `S-Venue-0-venue.md`.
      - Preserved the invocation hint under `metadata.argument_hint`, which conforms to
        the current Skill frontmatter schema.
260726 · `0.2.0` · the venue guard reads the venue page
      Aligned with the paper-folder layout ruled 2026-07-26 on the design board (`skills/diagrams/01-haipipe-paper-260725`, face QA6): `0-sections/` to `sections/`, `0-displays/` to `displays/` (one folder per unit, the only home of an asset, no top-level `figures/`), `1-compile.sh` to `2-src/compile.sh`, and `STATUS.md` retired. The venue guard, which blocks REVISE on a venue-ALIGNED artifact when no venue is pinned, was grepping `STATUS.md`. It reads `S-Venue-0-venue.md` frontmatter.
260724 · `0.1.6`
      Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.6.0; older entries below keep their original numbers).
260719 · `1.6.0` · a fourth worker, `place`, and it runs FIRST
      From the `paper/2-phase` review (`../../../_console/260719-02-PHASE-BOUNDARY-REFACTOR.md`), ruling D7.
      ### Changed (JL: "Follow your recommendation.")
      `haipipe-paper-revise-place` joins the roster and runs before every prose worker. The dispatch order becomes `place → content → humanizer → results`, and the order is BINDING, not stylistic: substituting a landed key or number after the prose workers have run drops it into sentences they had already closed, so the text that actually ships was never reviewed in its final form. Running the de-AI pass over `{VAL:? held-out accuracy}` and swapping in `0.87` afterwards reviews a sentence that does not exist.
      - `workers:` proof line widened to `place ✓ content ✓ humanizer ✓ results --`. `checks.sh --log` FAILs a `[REVISE]` entry without it, so the line and the roster must stay in step.
      - Dispatch table, phase diagram, return contract, `description:` and `summary:` all updated together; the roster was previously described as "Four workers" over a list of three.
      - The phase's own definition was rewritten: REVISE reads what PROBE landed in each entry's `### a-executor`, PLACES it, then rewrites. It previously stated "REVISE reads PROBE outputs (citations placed…)" as a PRECONDITION — self-referential once placement became REVISE's own first step.
260710 · `1.5.1`
      Changed
      - Wording: the .md stays markup-free APART FROM citation commands (real-citation convention, JL 2026-07-10); REVISE resolves `\cite{TOADD}` slots whose keys have landed in .bib.
260709 · `1.5.0`
      Changed (JL ruling 2026-07-09 (LLMTrait-Section session postmortem): normalize the writing process; closes feedback/2026-07-09_revise-skipped-humanize-and-outline-first.md)
      - Proof-carrying contract (binding): stage hubs reach REVISE ONLY via Skill(haipipe-paper-revise) -- inline hand-editing = "the REVISE phase did not happen"; every run writes a [REVISE] _LOG entry with `workers: content/humanizer/results` line; checks.sh --log FAILs without it.
      - Order of operations pinned: revise the working .md FIRST, then sync to tex -- never tex-first (the .md is what the human reads/comments).
      - Automation steps now end with "hand back to the stage hub, which OPENS CHECK -- never commit or conclude before the CHECK gate opens".
260708 · `1.4.0`
      Changed (venue lockfile wiring)
      - Venue norms + venue guard repointed: primary read = the paper's `0-lifecycle/2a-venue/2a-venue.md` (Writing Principles + Structural Blueprint block); direct `_venue/playbook-*` reads demoted to fallback (2a-venue.md absent) or deep dives via its `[source: ...]` tags; STOP/warning semantics unchanged.
260707 · `1.3.0`
      Changed (T7, JL: "maybe just go into Content")
      - Worker roster 4 → 3: weaving retired and merged into content (its weave step + ref/weaving.md). Default order now content (incl. weave) → humanizer → results. Kills the router↔weaving mutual-dispatch contradiction (C11) structurally. Also C13: the REF/prose-quality.md pointer corrected to ../../REF/ (was resolving into the router's own folder).
260703 · `1.2.0`
      - phase spine renamed DGPC -> DPRC (GATHER->PROBE, POLISH->REVISE). Phase verb is REVISE: the agent changes prose directly and leaves why-comments; the human gives preferences in CHECK.
260703 · `1.1.0`
      - reframed as internal worker. Users invoke stage skills (pitch, narrative, section-edit...), not this skill directly. Stage skills call this during their POLISH phase.
260703 · `1.0.0`
      - new hub skill for the POLISH phase. Dispatches to polish-content, -humanizer, -weaving, -results based on section needs.

<!-- haipipe:skill:log:end -->
