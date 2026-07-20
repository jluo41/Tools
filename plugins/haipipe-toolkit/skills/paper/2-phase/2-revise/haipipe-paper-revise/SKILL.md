---
name: haipipe-paper-revise
description: "REVISE phase worker (internal). Called by stage skills to rewrite draft prose to venue-quality after PROBE. REVISE = the agent CHANGES the prose directly AND leaves %% {CC-*}: why-comments explaining each change; the human gives preferences in CHECK. Dispatches place, content, humanizer, and results workers; place runs first and substitutes landed answers into their placeholders. Fully automatic (no human gate). Users invoke stage skills (pitch, narrative, section-edit...), not this skill directly."
argument-hint: "[section-name-or-number] [paper-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.6.0"
  last_updated: "2026-07-19"
  summary: "REVISE phase worker (internal): rewrite draft prose to venue-quality -- change directly, leave why-comments, then sync .md -> tex. Proof-carrying: stage hubs MUST reach REVISE through this skill (never hand-edit inline) and the [REVISE] _LOG entry MUST carry a `workers:` line. Dispatches place/content/humanizer/results workers (place first). History: ./CHANGELOG.md."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-paper-revise (internal phase worker)
====================================================

REVISE phase worker.
Called by stage skills (pitch, narrative, section-edit) to rewrite draft prose to venue-quality after PROBE.
The stage defines WHAT was drafted.
This skill defines HOW to revise it.

**What the REVISE contract means.** The agent CHANGES the prose directly AND leaves `%% {CC-*}:` comments explaining WHY each non-trivial change was made.
The human does not approve changes here; the human gives preferences in CHECK (via `> USER:` comments), and a REVISE restart responds to them.

**Proof-carrying (binding).** A stage hub reaches REVISE ONLY through `Skill(haipipe-paper-revise)` — hand-editing the prose inline is a protocol violation ("the REVISE phase did not happen").
Every run writes a `[REVISE]` entry in the stage's `_LOG` with a workers line: `workers: place ✓ content ✓ humanizer ✓ results --` (✓ ran · -- skipped-with-reason).
`checks.sh --log` FAILs a `[REVISE]` entry without it.
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

## Universal rules

All revise workers read and enforce `../../REF/prose-quality.md`. Installed skills flatten the tree (symlinks under `~/.claude/skills/`), so that relative path is NOT reliable — locate it layout-agnostically:
`PQ=$(find ~/.claude/skills "$CLAUDE_PLUGIN_ROOT" -path '*2-phase/REF/prose-quality.md' 2>/dev/null | head -1)` (absent → apply the rules below, note the gap in _LOG).
The rules:

- One idea per sentence
- No em-dashes
- Compress, don't split
- No AI voice
- Use verified numbers
- <=6 sentences per paragraph
- Pn.Sn markers on every sentence

Venue-specific norms (word budget, tone, section arc) come from the paper's `0-lifecycle/2a-venue/2a-venue.md` (Writing Principles + the relevant Structural Blueprint block) and override where they conflict.
Read `venue/playbook-*/style-profile.md` directly only as fallback when 2a-venue.md is absent, or as a deep dive via its `[source: ...]` tags.

**Venue guard** (same rule as DRAFT): when revising a venue-ALIGNED artifact, no `venue:` pinned in STATUS.md -> STOP with `status: blocked` and point the user to `/haipipe-paper venue`.
Venue pinned -> read the paper's `0-lifecycle/2a-venue/2a-venue.md` FIRST; fall back to the pinned `venue/playbook-*` pack only when it is absent (no matching pack either -> STOP the same way).
Fallback pack present but per-section style file missing -> revise with the general style-profile and flag the gap in `_LOG` + the CHECK report.
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
2. Applies prose-quality.md rules directly TO THE .MD, leaving `%% {CC-*}:` why-comments on non-trivial changes (in the tex after sync; the .md stays markup-free apart from citation commands)
3. Syncs the revised .md → .tex (Pn.Sn markers; tex prose never edited directly)
4. Writes the `[REVISE]` _LOG entry with the `workers:` line
5. Hands back to the stage hub, which OPENS CHECK — never commit or conclude before the CHECK gate opens

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
| haipipe-paper-pitch | cover letter prose (readability rules) |
| haipipe-paper-narrative | story beat prose (arc/flow coherence) |
| haipipe-paper-section-edit | section tex (full revise: content + humanizer + results) |

Note: seed, resource and claims produce argument docs that skip REVISE (markdown only, no venue-quality prose needed).
Resource has ONE exception: a woolly fitness ruling ("probably fine") is a DEFECT, not an answer -- when an **A** does not say what it KILLS, resource does NOT skip REVISE and sharpens it instead.

## Sibling phase workers

| Phase | Worker | Called after |
|---|---|---|
| DRAFT | haipipe-paper-draft | -- |
| PROBE | haipipe-paper-probe | DRAFT |
| REVISE (this) | haipipe-paper-revise | PROBE |
| CHECK | haipipe-paper-check | REVISE |
