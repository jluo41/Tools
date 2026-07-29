---
name: haipipe-paper-revise
description: "REVISE phase worker (internal). Called by stage skills to rewrite draft prose to venue-quality after PROBE. Default REVISE changes prose directly and leaves %% {CC-*}: why-comments; an explicit author request for original-preserving or sentence-apparatus review instead enables candidate-diff mode, which leaves prose unchanged and writes word-level Note-lane diffs. Dispatches place, content, humanizer, and results workers; place runs first. Users invoke stage skills (pitch, narrative, section-edit...), not this skill directly."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  argument_hint: "[section-name-or-number] [paper-path]"
  version: "0.2.2"
  last_updated: "2026-07-27"
  summary: "REVISE phase worker (internal): default direct revision plus an author-selected candidate-diff mode for auditable, original-preserving wording review."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

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

## What REVISE means

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

## Revision modes

### Default direct mode

Apply the four workers to the source `.md`, leave `%% {CC-*}:` why-comments for non-trivial edits, then sync the accepted source to TeX. This is the normal autonomous REVISE path.

### Candidate-diff mode

Use this mode only after an explicit author request for reviewable alternatives. Read `haipipe-paper-revise-humanizer/ref/venue-sciwrite.md` before proposing any change.

1. Keep the source sentence, its citations, values, display lanes, and user comments byte-intact.
2. Put one complete proposed sentence in an adjacent `> Note:` lane. Mark removed text as `~~removed~~` and inserted or replacement text as `**inserted**`.
3. Append `· <verified model label> · YYYY-MM-DD`; never invent a model name or version.
4. Make only minimum, meaning-preserving changes. Do not add or remove a claim, qualifier, causal strength, number, citation, display reference, or defined term.
5. Place the Note after any existing adjacent `> Citation:`, `> Value:`, or `> Display:` lanes so the entire apparatus folds under the same sentence.
6. Do not sync candidate Notes to TeX, call the source revised, or mark REVISE complete. Promote only author-accepted candidates in a later direct REVISE or CHECK action.

## Universal rules

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

## Dispatch logic

Read the section outline and tex to determine which workers to run:

| Worker | Run when | Skip when |
|---|---|---|
| place | the artifact carries any placeholder | no placeholder in the artifact |
| content | always | never |
| humanizer | always | never (AI-authored prose reliably contains patterns) |
| results | section is Results or contains figure/table narration | non-results sections |

When no specific worker is named, run in order: place → content (incl. its weave step for ¶-flow) → humanizer → results (if applicable).
`place` runs FIRST and the order is binding: substituting after the prose workers would re-open sentences they had already finished, so the shipped text would never have been reviewed in its final form.

## Automation

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

## Phase status

Derive revise status from disk:

```
revise ✅    tex synced from revised outline, all rules applied
revise 🚀    revise in progress
revise ⬜    not yet started (PROBE must complete first)
```

## Relation to other phases

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

## Return contract

```
status:    ok | blocked
section:   <section-name>
workers:   place <status> │ content <status> │ humanizer <status> │ results <status>
next:      <suggested command>
```


## Who calls this skill

Stage skills call this as their REVISE phase:

| Stage skill | What this skill revises |
|---|---|
| pitch | cover letter prose (readability rules) |
| narrative | story beat prose (arc/flow coherence) |
| section-edit | section tex (full revise: content + humanizer + results) |

Note: whether a stage runs REVISE is declared by its own contract's `phases:` list, not by this table. Argument docs (seed, resource, claims) need no venue-quality POLISH — but they DO run REVISE when their contract lists it, because REVISE is also where a landed answer is woven back into the sentences that cite it and the `[Q-<Stage>-<n>]` bracket is discharged. `2a-venue` is the one stage that genuinely omits REVISE: it produces a contract, not prose.
Resource has ONE exception: a woolly fitness ruling ("probably fine") is a DEFECT, not an answer -- when an **A** does not say what it KILLS, resource does NOT skip REVISE and sharpens it instead.

## Sibling phase workers

| Phase | Worker | Called after |
|---|---|---|
| DRAFT | haipipe-paper-draft | -- |
| PROBE | haipipe-paper-probe | DRAFT |
| REVISE (this) | haipipe-paper-revise | PROBE |
| CHECK | haipipe-paper-check | REVISE |
