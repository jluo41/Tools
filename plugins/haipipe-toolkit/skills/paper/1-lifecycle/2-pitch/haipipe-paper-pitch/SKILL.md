---
name: haipipe-paper-pitch
description: "Create or update the paper folder's 0-lifecycle/2-pitch/2-pitch.md + _LOG_2-pitch.md: the venue-ALIGNED cover letter and one-minute story for this concrete manuscript. Absorbs the Editor's Chair Test, [primary] claim designation, and venue-specific RQ framing. Includes a Probes section for pitch-level investigation (venue fit, framing risk, competing papers). Archives semantic old versions in _LOG when the pitch shifts. Markdown only. Use for paper pitch, cover letter, one-minute story, hook/surprise/so-what, audience/venue fit, editor's chair, primary claim, RQ framing, story trajectory, pitch provenance."
argument-hint: "[paper-dir] [--reason <slug>] [--source <path-or-note>...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "4.1.0"
  last_updated: "2026-07-08"
  summary: "Pitch stage orchestrator. Defines WHAT (cover letter sections + probes) and drives phases (draft -> probe -> revise -> check) internally. User invokes pitch, not phases."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-paper-pitch
====================================

Stage orchestrator for the **pitch** stage (stage 2, venue-ALIGNED). The user invokes this skill; it drives the phases internally.

The pitch is the **cover letter**: the venue-ALIGNED document that tells THIS editor why THIS paper fits THEIR journal. It can be sent to an editor as-is.

The pitch is not a paper plan, outline, or claim matrix. It is the version a person can understand in one minute:

```
What is this paper about?
What vivid question or scene pulls the reader in?
What is surprising?
So what changes if it is true?
Who reads the target venue, and why does this matter to them?
Will the editor publish this? (Editor's Chair Test)
Which claim is primary for THIS venue?
How do the hypotheses become RQs for THIS audience?
Why should we believe it?
What is still fragile?
How did the story get here?
```

Read first: `../../PHILOSOPHY.md`, `../../wiki/04-lifecycle-map.md`.

## Artifact Spec

**Files produced:**
- `0-lifecycle/2-pitch/2-pitch.md` -- the cover letter (venue-ALIGNED)
- `0-lifecycle/2-pitch/_LOG_2-pitch.md` -- changelog with provenance
- `0-lifecycle/2-pitch/_PROBE/` -- probe plans for pitch-level investigation

**Content structure (2-pitch.md):**
- Title -- <=15 words, specific, evocative
- One-Minute Pitch -- 4-6 sentences for a newcomer
- Hook -- >=2 candidate methods, one recommended lead
- Finding-Surprise -- the non-obvious turn
- Implication-So What -- what changes and who can act
- Editor's Chair Test -- venue question from the 2-venue.md Venue Profile, one-sentence answer per primary claim
- Primary Claim + RQ Framing -- [primary] designation, H-to-RQ mapping for THIS venue
- Audience and Venue Fit -- who reads this journal, why they care
- Evidence-Why Believe -- source per claim
- Limitation-Still Fragile -- top 3 risks
- Next Evidence Move -- verb + artifact
- Probes -- pitch-level investigation needs (venue fit, framing risk, competing papers)

**Formatting:**
- Heading style: `=====` for the document title, `-----` for sections. No `#`/`##`/`###`.
- One sentence per line (semantic line breaks). No dense multi-sentence paragraphs.

**Done-criteria:**
- [ ] Editor's Chair Test passes (venue question answered)
- [ ] Readability rules pass (8 rules from ref/pitch-readability.md)
- [ ] [primary] claim designated for THIS venue
- [ ] RQ framing complete (H-to-RQ mapping with venue rationale)
- [ ] All labeled sections present (Title, Hook with >=2 candidates, Surprise, Implication, etc.)
- [ ] Probes section present with pitch-level investigation results
- [ ] Readable in one minute

Illustration:
- `images/stage2-pitch-gate-image2.png` -- Stage 2 as a pitch gate: either return to narrative/project work or proceed to Stage 3 evidence-backed narrative.

## Phase Orchestration

When the user invokes `/haipipe-paper pitch`, this skill drives the phases in order. The user does not call phase skills directly.

```
pitch invoked
  │
  ▼
DRAFT ──→ illuminate existing content, elicit taste,
          write/iterate the cover letter sections with > JL: / > CC: comments;
          read STATUS venue + the paper's 0-lifecycle/2-venue/2-venue.md
          (Venue Profile + Fit Assessment blocks) to shape
          Editor's Chair Test, [primary] designation, RQ framing, Audience
          (fallback: _venue/playbook-<venue> only if 2-venue.md is absent);
          read claims ledger for venue-neutral H1/H2/H3
          (internally calls /haipipe-paper-draft with this artifact spec)
  │
  ▼
PROBE ──→ citation audit for anchor papers cited in Evidence-Why Believe;
          verify 2-venue.md provenance (if its recorded _venue commit is behind
          HEAD, note "venue contract stale -- consider /haipipe-paper-venue refresh");
          confirm H-to-RQ mapping against claims ledger
          (internally calls /haipipe-paper-probe)
  │
  ▼
REVISE ─→ refine prose, apply 8 readability rules from ref/pitch-readability.md,
          de-AI voice, one idea per sentence, lead with the point
          (internally calls /haipipe-paper-revise)
  │
  ▼
CHECK ──→ present exit gate per ../../wiki/08-stage-gate.md:
          quality gate checklist (see below), template enforcement,
          Editor's Chair Test passes, readability rules pass
          user confirms → advance to narrative
          (internally calls /haipipe-paper-check)
```

Phase visibility per the Phase Transition Contract in `../../wiki/08-stage-gate.md`: announce every phase boundary (reply line + `[PHASE]` entry in `_LOG` + phase-line 🔥 moves); skip a phase only by an explicit logged verdict (`[PROBE] skipped -- <reason>`, phase line shows `--`); CHECK is never implicit -- it opens by presenting the exit-criteria report and the approval ask.

Comment lifecycle per `../../wiki/02-comment-lifecycle.md`: comments live in 2-pitch.md while active, move to _LOG on resolve, each phase starts clean.

### Quality gate checklist (CHECK phase)

- [ ] Title section present with working title?
- [ ] Hook section with >=2 candidate methods, all retained?
- [ ] Surprise section with a non-obvious turn stated?
- [ ] Implication section with "so what" and audience stated?
- [ ] Editor's Chair Test present with venue question and one-sentence answer?
- [ ] Primary Claim + RQ Framing present with [primary] designation and H-to-RQ mapping?
- [ ] Audience/Venue Fit section names who reads this journal and why they care?
- [ ] Why Believe section with evidence pointers (>=1 per claim)?
- [ ] Still Fragile section with the weakest point named?

## Location

```text
<paper>/0-lifecycle/2-pitch/2-pitch.md       cover letter (venue-ALIGNED)
<paper>/0-lifecycle/2-pitch/_LOG_2-pitch.md   changelog with provenance
<paper>/0-lifecycle/2-pitch/archive/          older semantic pitch snapshots (vNN_<reason>.md)
```

Markdown only (argument documents don't need compilation).

## Template

The canonical template is the source of truth for section order: `ref/pitch-template.md`

Reading order:

```text
1. Title                       ← <=15 words, specific, evocative
2. One-Minute Pitch            ← 4-6 sentences for a newcomer
3. Hook                        ← >=2 candidates, one recommended lead
4. Finding - Surprise          ← the non-obvious turn
5. Implication - So What       ← what changes and who can act
6. Editor's Chair Test         ← venue question from 2-venue.md Venue Profile; one-sentence answer per primary claim
7. Primary Claim + RQ Framing  ← [primary] designation + H→RQ mapping for THIS venue
8. Audience and Venue Fit      ← venue-ALIGNED: who reads this journal, why they care
9. Evidence - Why Believe      ← source per claim
10. Limitation - Still Fragile ← top 3 risks
11. Next Evidence Move         ← verb + artifact
```

**Template enforcement:** A pitch is NOT complete unless it contains, as labeled sections: Title, One-Minute Pitch, Hook (with >=2 candidates), Surprise, Implication, Editor's Chair Test, Primary Claim + RQ Framing, Audience/Venue Fit, Why Believe, Still Fragile. A pitch that is one flat paragraph missing these sections must be flagged and restructured before it can pass any gate.

The pitch is venue-ALIGNED: it reads STATUS `venue` and the paper's `0-lifecycle/2-venue/2-venue.md` (Venue Profile + Fit Assessment blocks) to shape the Editor's Chair Test, the [primary] claim designation, the RQ framing, and the Audience section. `2-venue.md` is the compiled venue contract; read it FIRST. Fall back to reading `_venue/playbook-<venue>` directly only when `2-venue.md` does not exist (venue stage not yet run, or a pack-less venue); if no pack exists either, proceed without venue inputs. Deep dives follow the `[source: ...]` tags recorded in `2-venue.md` into `_venue/playbook-<slug>/<journal>/...`. If the provenance commit in `2-venue.md` is older than the current `_venue` HEAD, note "venue contract stale -- consider /haipipe-paper-venue refresh" but still use `2-venue.md` (never silently re-read packs). A venue change means the pitch rewrites. (Claims stays unchanged because it is venue-free.)

### Pitch Log template (_LOG_2-pitch.md)

```markdown
# Pitch Log

## v01 -- Seed

Archived:
- none

Source:
- Author intuition / initial review / early project direction.

Pitch:
- See `2-pitch.md`.

Why this version:
- Initial public-facing story before the evidence base is stable.

Still fragile:
- No direct evidence may exist yet.

Next:
- Identify the first discovery, task, or probe that can strengthen or kill this story.
```

Version-to-version log entry shape:

```markdown
## v02 -> v03 -- <reason>

Archived:
- archive/v02_<reason>.md

Source:
- <author decision / discovery / task / probe / insight / review>

Change:
- Old: ...
- New: ...

Why:
- ...

Still fragile:
- ...

Next:
- ...
```

## Principles

1. **One minute or it failed.** `2-pitch.md` should be readable in one minute. Keep it short enough to fit on one screen.
2. **Pitch can start as intuition.** A seed pitch may cite author judgment, a research review, or a rough direction.
3. **Later shifts need sources.** Every semantic shift after the seed should cite a source: `discoveries/`, `tasks/`, stage `_PROBE/` cards, `insights/`, reviewer feedback, venue strategy, or an explicit author decision.
4. **Archive semantic versions only.** Archive when the story state changes (`seed -> discovery-shift`, `accuracy -> robustness`, `method-first -> application-first`), not for typo edits.
5. **Do not write the paper here.** Abstract, intro, section plan, and LaTeX belong downstream. This skill only maintains the story kernel.
5b. **Pitch is the cover letter.** The pitch IS the venue-ALIGNED cover letter. It can be sent to the editor as-is. It tells THIS editor why THIS paper fits THEIR journal. Venue pinning (STATUS `venue`) must happen before or during pitch. If no venue is pinned, run `/haipipe-paper venue` first.
5c. **Editor's Chair Test lives here.** Read the Venue Profile block of `0-lifecycle/2-venue/2-venue.md` (its one-sentence test) for the editor's chair question; fall back to `_venue/playbook-<venue>` only if `2-venue.md` is absent. Every primary claim must have a one-sentence answer. This test was migrated from claims (v3.0.0) because it is a venue question, not an evidence question.
5d. **[primary] claim designation lives here.** Read the claims ledger (venue-neutral H1, H2, H3) and designate ONE PRIMARY claim aligned to what THIS venue rewards. A result that is novel elsewhere but already established for this venue's readers is an enabler (Methods), not a primary claim. A venue change re-runs this designation.
5e. **RQ framing lives here.** Venue-neutral hypotheses (H1, H2, H3) live in claims. The pitch reframes them as venue-specific RQs: H1 -> RQ1 worded for what the editor rewards. Include an explicit H->RQ mapping with a "why this RQ for this venue" column.
6. **Each hook candidate is one move, not a stack of questions.** Each candidate hook should commit to ONE narrative move (not a stacked enumeration): a vivid concrete scene, a surprising or counterintuitive fact, a paradox tied to stakes, or one sharp question. Do not stack multiple rhetorical questions within a single candidate, which dilutes the punch and reads as undecided. The final artifact keeps all candidate hooks visible (>=2 candidates, one marked as recommended lead). A flat statement of background is not a hook. See `ref/pitch-readability.md`.
7. **Read it in one minute or rewrite it.** The pitch must be fast and easy to read; if a reader slows down to parse a sentence, rewrite that sentence. Follow the readability rules and per-section cues in `ref/pitch-readability.md`: short sentences, lead with the point, one idea per sentence, plain words, concrete numbers, no AI voice. Readability is part of the pitch done-gate.

## Relationship to other structure skills

`0-lifecycle/2-pitch/2-pitch.md` is one stage of the lifecycle spine:

```
0-seed.md        why this paper might exist (venue-FREE)
    ↓
1-claims.md      claim/evidence inventory (venue-FREE)
    ↓
2-pitch.md       cover letter + one-minute story (venue-ALIGNED, this skill)
    ↓
3-narrative.md   evidence-backed arc (venue-ALIGNED)
    ↓
4-display.tex    display contract (venue-HEAVY)
```

Upstream: claims (0-lifecycle/1-claims/) provides the venue-neutral hypotheses (H1, H2, H3) and evidence status. Pitch reframes them for the target venue.

Downstream: narrative expands the pitch into a full section-mirrored arc. If a downstream stage disagrees with the pitch, either update the pitch with a logged reason or revise the downstream stage. Do not let abstract, introduction, hero figure, and discussion carry different stories.

## Handoff

On CHECK confirm, update `STATUS.md` (`current_layer`, `maturity: pitch`) and advance:

```text
promote     -> /haipipe-paper narrative <paper-dir>
```

End the reply with the stage strip (run `../../../haipipe-paper/stage-strip.sh`).
