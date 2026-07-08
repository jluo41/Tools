---
name: haipipe-paper-revise
description: "REVISE phase worker (internal). Called by stage skills to rewrite draft prose to venue-quality after PROBE. REVISE = the agent CHANGES the prose directly AND leaves %% {CC-*}: why-comments explaining each change; the human gives preferences in CHECK. Dispatches content, humanizer, and results workers (weaving merged into content 2026-07-07). Fully automatic (no human gate). Users invoke stage skills (pitch, narrative, section-edit...), not this skill directly."
argument-hint: "[section-name-or-number] [paper-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.3.0"
  last_updated: "2026-07-03"
  summary: "REVISE phase worker (internal). Called by stage skills to rewrite draft prose to venue-quality: change directly, leave why-comments. Dispatches content/humanizer/results workers (weaving merged into content)."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-paper-revise (internal phase worker)
====================================================

REVISE phase worker. Called by stage skills (pitch, narrative, section-edit) to rewrite draft prose to venue-quality after PROBE. The stage defines WHAT was drafted. This skill defines HOW to revise it.

**What the REVISE contract means.** The agent CHANGES the prose directly AND leaves `%% {CC-*}:` comments explaining WHY each non-trivial change was made. The human does not approve changes here; the human gives preferences in CHECK (via `> USER:` comments), and a REVISE restart responds to them.

**Not user-facing.** Users invoke stage skills:
```
/haipipe-paper pitch        → pitch skill calls this internally for REVISE phase
/haipipe-paper narrative    → narrative skill calls this internally for REVISE phase
/haipipe-paper section-edit §3  → section-edit skill calls this internally
```

## What REVISE means

REVISE = rewrite draft sentences to venue-quality prose, applying changes directly with why-comments. Four workers, each with a different lens:

```
haipipe-paper-revise-content              WHAT sentences say (accuracy, completeness, claims)
haipipe-paper-revise-humanizer            HOW sentences sound (de-AI audit, voice)
haipipe-paper-revise-results              results-specific (figure narration, effect reporting)
```

All four apply rules directly. No comment-first protocol, no human gate. The agent reads prose-quality.md + venue style profile, applies fixes, leaves `%% {CC-*}:` why-comments, and moves on. Human review of revised prose happens in CHECK.

## Universal rules

All revise workers read and enforce `../../REF/prose-quality.md`:

- One idea per sentence
- No em-dashes
- Compress, don't split
- No AI voice
- Use verified numbers
- <=6 sentences per paragraph
- Pn.Sn markers on every sentence

Venue-specific norms (word budget, tone, section arc) from `_venue/playbook-*/style-profile.md` override where they conflict.

**Venue guard** (same rule as DRAFT): when revising a venue-ALIGNED artifact, no `venue:` pinned in STATUS.md or no matching `_venue/playbook-*` pack -> STOP with `status: blocked` and point the user to `/haipipe-paper venue`. Pack present but per-section style file missing -> revise with the general style-profile and flag the gap in `_LOG` + the CHECK report. Never silently invent venue norms.

## Dispatch logic

Read the section outline and tex to determine which workers to run:

| Worker | Run when | Skip when |
|---|---|---|
| content | always | never |
| humanizer | always | never (AI-authored prose reliably contains patterns) |
| results | section is Results or contains figure/table narration | non-results sections |

When no specific worker is named, run in order: content (incl. its weave step for ¶-flow) → humanizer → results (if applicable).

## Automation

REVISE is fully automatic. The agent:

1. Reads the outline .md and current .tex
2. Applies prose-quality.md rules directly, leaving `%% {CC-*}:` why-comments on non-trivial changes
3. Syncs changes between .md outline and .tex
4. Moves on to CHECK

No stopping for comments. No waiting for approval. The CHECK phase is where the human reviews everything and states preferences.

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
                    ├── haipipe-paper-revise-content     (WHAT: accuracy, claims)
                    ├── haipipe-paper-revise-humanizer   (HOW: de-AI voice)
                    └── haipipe-paper-revise-results     (results-specific)
```

REVISE reads PROBE outputs (citations placed, values verified, displays linked) and rewrites draft sentences into final prose. CHECK then verifies the revised result.

## Return contract

```
status:    ok | blocked
section:   <section-name>
workers:   content <status> │ humanizer <status> │ results <status>
next:      <suggested command>
```


## Who calls this skill

Stage skills call this as their REVISE phase:

| Stage skill | What this skill revises |
|---|---|
| haipipe-paper-pitch | cover letter prose (readability rules) |
| haipipe-paper-narrative | story beat prose (arc/flow coherence) |
| haipipe-paper-section-edit | section tex (full revise: content + humanizer + results) |

Note: seed and claims produce argument docs that skip REVISE (markdown only, no venue-quality prose needed).

## Sibling phase workers

| Phase | Worker | Called after |
|---|---|---|
| DRAFT | haipipe-paper-draft | -- |
| PROBE | haipipe-paper-probe | DRAFT |
| REVISE (this) | haipipe-paper-revise | PROBE |
| CHECK | haipipe-paper-check | REVISE |
