---
name: haipipe-paper-narrative
description: "Generate 0-lifecycle/3-narrative/3-narrative.md + _LOG_3-narrative.md, the design contract for /haipipe-paper: a venue-ALIGNED, section-mirrored, evidence-tracked story (Introduction, Methods, Results, Discussion), with every beat carrying a readiness tag and an interrogation comment. Includes a Probes section for narrative-level investigation (evidence gaps per beat, citation needs, arc verification). Markdown only. Use when transitioning from research/experiment phase to writing phase, or when the user says 'write narrative report', '生成 narrative', '/haipipe-paper-narrative'."
argument-hint: "[paper-dir-or-topic]"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "4.2.2"
  last_updated: "2026-07-19"
  summary: "Narrative stage orchestrator (stage 3, venue-ALIGNED): the section-mirrored, readiness-tagged design contract with an explicit Probes section, driving DRAFT -> PROBE -> REVISE -> CHECK internally (the user invokes narrative, not the phases). A [GAP] beat raises a question SECTION in 1-probes/PPNN_<topic>.md. History: ./CHANGELOG.md."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-paper-narrative
===================================

Stage orchestrator for the **narrative** stage (stage 3, venue-ALIGNED).
The user invokes this skill; it drives the phases internally.

It answers one question:

```text
How does the evidence compose into a section-mirrored, readiness-tagged story?
```

The narrative report is **not** a draft of the paper.
It is the **design contract** (stage 3, venue-ALIGNED) that the paper writes from.
Every claim, figure, and citation in the final PDF should trace back to a line in this file.
If something is not in the narrative, the downstream pipeline (`/haipipe-paper-display -> /haipipe-paper-section-edit`) will not invent it.

If the paper folder has `0-lifecycle/2b-pitch/2b-pitch.md`, read it before composing the narrative.
The pitch is the one-minute public-facing story for this concrete paper; this narrative expands it into evidence-backed claims, figures, and limitations.
If the evidence forces a different pitch, update `0-lifecycle/2b-pitch/2b-pitch.md` through `/haipipe-paper-lifecycle pitch` and log the shift instead of silently diverging.

Read first: `../../../PHILOSOPHY.md`, `../../ref/04-lifecycle-map.md`.

## Artifact Spec

**Files produced:**
- `0-lifecycle/3-narrative/3-narrative.md` -- the design contract (venue-ALIGNED)
- `0-lifecycle/3-narrative/_LOG_3-narrative.md` -- phase progress journal (per the Comment lifecycle section in `../../../haipipe-paper/SKILL.md`)
- `0-lifecycle/4-display/_DISPLAY_REQUEST.md` -- one DR row per beat that needs a display unit, filed on this stage's behalf (the display stage owns the file and advances its statuses)
- `1-probes/PPNN_<topic>.md` -- the probe FILES; a narrative need becomes a question ENTRY (flat cross-stage pool), its `### q-consumer` bullet naming the `Q-Narrative-<n>` it serves

`1-probes/` is the only consumer-side source of truth; `_LOG_3-narrative.md` is the only sidecar.
An owed citation is written `\cite{TOADD} [Q-Narrative-<n>]` and an owed number `{VAL:? <what>} [Q-Narrative-<n>]` -- the marker and the anchor bracket sit side by side, never fused -- where the bracket names the question that will produce it.
A placeholder with no bracket is a defect: it is a hole no question will ever fill.

**Content structure (3-narrative.md):**
- Readiness legend -- five tags: [READY], [PENDING], [INFER], [LIT], [GAP]
- Spine (throughline) -- one paragraph, the whole paper in one breath
- Section blocks (Intro, Methods, Results, Discussion) -- each with heading+subtitle, Flow arrow chain, grounded prose paragraph, Key points with tagged beats
- Per-beat comments -- \rev interrogation (internal) + \fb feedback (external)
- Probes -- narrative-level investigation needs: [GAP] beats that need evidence, [LIT] beats that need citations, arc verification questions
- Footer ledger -- reviewer-flagged gaps, arc summary, awaiting review

**Formatting:**
- Heading style: `=====` for the document title, `-----` for sections.
  No `#`/`##`/`###`.
- One sentence per line (semantic line breaks).
  No dense multi-sentence paragraphs.

**Done-criteria:**
- [ ] All beats have readiness tags (no untagged beats)
- [ ] No [GAP] beat without an entry in the Probes section and a question SECTION in 1-probes/
- [ ] Every beat needing a display carries a DR row in `0-lifecycle/4-display/_DISPLAY_REQUEST.md`
- [ ] Per-beat interrogation complete (subagent reviewed every beat)
- [ ] Spine throughline present
- [ ] Probes section present with all [GAP]/[LIT] needs surfaced
- [ ] Venue contract (2a-venue.md; pack fallback if absent) consulted for arc shaping
- [ ] _LOG entry records the current state

**DPRC applicability:**
- DRAFT: design contract with section blocks and tagged beats; each beat's display need filed as a DR row
- PROBE: link claims to beats, check readiness, citation needs per beat
- REVISE: sharpen arc and flow, refine beat prose
- CHECK: all beats [READY]?
  Interrogation complete?
  Every DR row ruled by the display stage?

## Phase Orchestration

When the user invokes `/haipipe-paper narrative`, this skill drives the phases in order.
The user does not call phase skills directly — but steers them with VERBS on this stage:

```
/haipipe-paper narrative <paper-dir>            -> open: status + frontier; advance ONLY on the user's verb
/haipipe-paper narrative <paper-dir> draft      -> run/redo DRAFT  -> STOP for user review
/haipipe-paper narrative <paper-dir> probe      -> run/redo PROBE  (agent-only)
/haipipe-paper narrative <paper-dir> revise     -> dispatch REVISE workers (agent-only, proof-carrying)
/haipipe-paper narrative <paper-dir> check      -> open the CHECK gate
```

**Hard gates (binding).**
After DRAFT: ⛔ STOP — present the draft for review and end the turn; the user's verb/"go" advances, logged as `[GATE] draft-review: approved` quoting the user.
Each phase runs via its `Skill()` dispatch — a phase executed inline did not happen; the `[REVISE]` _LOG entry carries its `workers:` proof line.
Never commit or conclude the stage before CHECK opens with its report.
The agent never self-advances past a gate.

**Comment rules (binding).**
The agent NEVER deletes, rewords, or relocates a `> USER:` comment; it replies `> CC:` underneath; only the user resolves a thread; resolved threads MOVE to `_LOG` verbatim.
Working files are edited surgically — no full-file rewrite of a file carrying `> USER:` comments.
Background: `../../../haipipe-paper/SKILL.md`, Comment lifecycle.

```
narrative invoked
  |
  v
DRAFT --> discover inputs (pitch, claims, experiment results, repo source),
          illuminate existing content, elicit taste,
          build claim-evidence map, write the section-mirrored story
          with readiness-tagged beats and spine throughline,
          run per-beat interrogation (subagent reviewed every beat),
          integrate interrogation comments,
          raise each beat's display need as a DR row in
          0-lifecycle/4-display/_DISPLAY_REQUEST.md (via /haipipe-paper-draft-display)
          (internally calls /haipipe-paper-draft with this artifact spec)
          Ends at ⛔ STOP: user reviews, iterates, approves ([GATE] logged).
  |
  v
PROBE --> identify citation needs per beat ([LIT] tags),
          check each beat's DR row against the display stage's ruling
          (accepted / declined-with-reason / done),
          raise [GAP]/[PENDING] beats as question SECTIONS (-> 1-probes/),
          thread external reviewer comments (\fb) onto beats
          (internally calls /haipipe-paper-probe)
  |
  v
REVISE -> refine prose clarity across all beats,
          sharpen arc and flow between sections,
          apply short-plain-sentence rule to all comments,
          ensure venue-contract (2a-venue.md) arc shaping is applied
          (internally calls /haipipe-paper-revise; [REVISE] _LOG entry carries workers: proof)
  |
  v
CHECK --> present exit gate per ../../ref/08-stage-gate.md
          user confirms -> advance to display
          (internally calls /haipipe-paper-check)
```

Phase visibility per the Phase Transition Contract in `../../ref/08-stage-gate.md`: announce every phase boundary (reply line + `[PHASE]` entry in `_LOG` + phase-line 🔥 moves); skip a phase only by an explicit logged verdict (`[PROBE] skipped -- <reason>`, phase line shows `--`); CHECK is never implicit -- it opens by presenting the exit-criteria report and the approval ask.

Comment lifecycle per `../../../haipipe-paper/SKILL.md` (Comment lifecycle section): comments live in 3-narrative.md while active, move to _LOG on resolve, each phase starts clean.

## Context: $ARGUMENTS

## When to Use

- Research / experiment phase is essentially done -- results are in, story is approximately settled
- Before invoking `/haipipe-paper` or `/haipipe-paper-display` (they consume this file)
- After `/auto-review-loop` finishes, as the handoff to writing
- When the project has accumulated `IDEA_REPORT.md`, `AUTO_REVIEW.md`, experiment logs, and figures but no single document tells the story

Do **not** use when:
- Experiments are still running (the narrative would be premature)
- You only have a vague topic -- use `/idea-discovery` or settle the claims stage first
- A current `0-lifecycle/3-narrative/3-narrative.md` already exists; edit it directly

## Inputs (in priority order)

The skill discovers whichever of these exist in the project tree:

0. **`0-lifecycle/2b-pitch/2b-pitch.md`** (paper folder, if present) -- current one-minute paper story.
   Use it as the reader-facing framing constraint, not as evidence.
1. **`0-lifecycle/1b-claims/1b-claims.md`** (best) -- the claim ledger.
   It is the ONLY home of a claim's status (`supported | refuted | inconclusive` + confidence + claim_type): a probe entry carries only its `### a-executor`.
   If present, use the ledger as the spine of the narrative; every supported claim becomes a section in the report.
2. **`IDEA_REPORT.md`** -- chosen idea, hypothesis, novelty justification (from `/idea-discovery`).
   Supplies the problem statement and intended contribution.
3. **`review-stage/AUTO_REVIEW.md`** (fall back to `./AUTO_REVIEW.md`) -- review history, weaknesses fixed, remaining limitations (from `/auto-review-loop`).
   Supplies the limitations section and reframings.
4. **Experiment results** -- JSON / CSV / TSV under `figures/`, `results/`, `outputs/`, `tasks/`.
   These are the raw evidence for every quantitative claim.
   Each number that ends up in the narrative must trace back to one of these files.
5. **`EXPERIMENT_LOG.md` / `probe-log.txt`** -- comparison-first experiment ledger.
   Useful for cross-probe deltas and baseline-vs-method tables.
6. **Repo source** -- for the method summary (what was actually built; not what was originally proposed).
   One short paragraph, not a code dump.

If multiple inputs disagree (e.g. `IDEA_REPORT` says "X improves Y by 5%" but `CLAIMS_FROM_RESULTS` says "no improvement on test-od"), **trust the latest / most data-grounded source** (CLAIMS_FROM_RESULTS > experiment files > AUTO_REVIEW > IDEA_REPORT) and surface the discrepancy as a note in the report.

## Content Structure

The narrative mirrors the paper's REAL sections, in reading order, and has five structural parts:

1. **Readiness legend (top).**
   Five color-coded tags, defined once, applied to every beat:
   - `[READY]` (green): evidence in hand (a confirmed probe or a run we trust).
   - `[PENDING]` (orange): data exists but a render/check/probe is still open.
   - `[INFER]` (purple): an inference, grounded in the evidence, reaching one reasoned step beyond, never measured (no probe will confirm it).
   - `[LIT]` (blue): rests on outside literature, citation audit pending.
   - `[GAP]` (red): no evidence yet, needs a probe.

   The tag is not decoration: `[PENDING]` and `[GAP]` beats ARE the open evidence needs, and they route to `/haipipe-probe`.
   The narrative is venue-ALIGNED -- it reads STATUS `venue` and consults the venue contract (2a-venue.md) to shape the arc.

2. **Spine (throughline).**
   One paragraph, an arrow chain, the whole paper in one breath: problem, the move this paper makes, the core finding, the so-what.
   Every beat below must serve this line.

3. **One block per paper section** (Introduction, Methods, Results, Discussion, in reading order), each with:
   - a heading plus a plain-language subtitle (for example "what is known, the gap, and the bet");
   - a **Flow:** line, the section's own arrow chain;
   - a **grounded prose paragraph**, draft-quality and in plain language.
     This paragraph is the literal opener the manuscript grows from.
   - a **Key points to cover** enumerate, where each beat is `[TAG] **Label:** one to three sentences`.

4. **Per-beat comments.**
   Every beat carries an interrogation comment of the form `verb + role` then one sharp sentence on why the beat is here or what breaks without it.
   Verbs: `keep / add / demoted / cut / added by author`.
   Roles: `stakes / validity / contribution / guardrail / safety / defense / mechanism / grounded opener / no-blame anchor / so-what` (extend as the venue needs).
   These are authored by the interrogation subagent, not self-authored (see Per-Beat Interrogation below).
   When an EXTERNAL named reviewer comments on the paper, their comment is threaded onto the same beat (see External Reviewer Comments below).
   All comment text uses short plain sentences (one idea each); compress rather than nest, split rather than join.

5. **Footer ledger.**
   Lines: **Reviewer-flagged gaps** (each known reviewer concern and which section beat now threads it, or marked Remaining and routed to a probe), **Arc** (one line: what each section lands on after demotions/parks/folds, and how the spine's peak claim is defended), **Awaiting review** (beats authored since the last interrogation pass that still need a verdict), and, when an external review has been threaded, an **External review (`<name>, <date>`)** line that points to the comments above and carries any comment with no home beat plus the source file path.

This form absorbs the old markdown buckets: the claim-evidence matrix becomes the readiness-tagged beats; the figure/table inventory becomes Methods/Results beats (a Table 1 beat, a STROBE-flow beat); limitations become Discussion beats; the pitch alignment stays a constraint read from `0-lifecycle/2b-pitch/2b-pitch.md` (venue-ALIGNED), not a printed section.

## Per-Beat Interrogation (subagent review)

After drafting the narrative, EACH beat/item in every section is interrogated by an independent subagent.
The drafting agent does NOT self-author inclusion justifications (self-authored "why it's here" comes out limp and circular).

Protocol:
  1. Dispatch ONE reviewer subagent that sees ALL beats so it can also judge flow, redundancy, and gaps.
  2. The reviewer returns, per item: verdict (keep | move-to-section | demote-to-Supplement | cut) + one sharp venue-aware comment.
  3. The drafting agent integrates the returned comments attached to each beat, visibly subordinate to the beat.

The reviewer subagent JUDGES; the drafting agent INTEGRATES.
Builder != judge.

## External Reviewer Comments (threaded per beat)

Internal interrogation comments are the INTERNAL pass (above).
External comments are for an EXTERNAL named reviewer: a co-author, advisor, or referee who comments on the paper.
When such a review arrives, thread each comment onto the beat it concerns (post + comments model), not into one summary footer paragraph.
This makes a review pass trackable at the point where the change must happen, and lets the narrative double as a progress tracker.

Each external comment carries:

- **name** -- the reviewer (e.g. `Ritu`).
- **status** -- `done` | `part` | `open`, judged against THIS narrative contract (not the manuscript prose): `done` = the comment's substance is in the narrative arc/beats; `part` = the arc handles it but a manuscript reflow or an open decision is still pending; `open` = not yet addressed.
- **feedback** -- their words, VERBATIM.
  Do not paraphrase, compress, or translate.
- **resolution** -- OUR words, in SHORT PLAIN sentences.
  One idea each.

Placement and ordering: a comment that maps to a beat threads onto that beat.
When a beat carries both, order is beat text, then internal comment, then external comment.
A comment with no single home beat stays in the footer ledger, on the `External review (<name>, <date>)` line, with the source file path.

Multiple reviewers: give EACH reviewer its own footer `External review (<name>, <date>)` line; on the beats, both reviewers' comments simply coexist (each carries its own name).
Keep the footer label exactly `External review (...)` so it is not confused with the internal `Reviewer-flagged gaps` line.

## Location

```text
<paper>/0-lifecycle/3-narrative/3-narrative.md          design contract
<paper>/0-lifecycle/3-narrative/_LOG_3-narrative.md      phase progress journal
<paper>/0-lifecycle/4-display/_DISPLAY_REQUEST.md       DR rows this stage files for the beats' display needs
<paper>/1-probes/PPNN_<topic>.md                    probe files; one SECTION per [GAP] beat's question
```

Markdown only (argument documents don't need compilation).

## Template

The canonical template is the source of truth for structure: `ref/narrative-template.md`.
It carries the readiness legend, the comment vocabulary (internal interrogation + external reviewer lines), the spine, the four section blocks with tagged beats, and the footer ledger.
Copy it to `<paper>/0-lifecycle/3-narrative/3-narrative.md` and replace the placeholders.

## Principles

1. **Claim-evidence is non-negotiable.**
   Every quantitative line in the narrative must have a traceable file path.
   Numbers without sources will fail `/haipipe-paper-claim-audit` later anyway, so catch them here.
2. **Every beat carries a readiness tag.**
   No beat is untagged.
   `[PENDING]` and `[GAP]` beats are the paper's live evidence worklist: surface them and route them to `/haipipe-probe`; never quietly upgrade a beat to `[READY]` without the evidence in hand.
3. **Do not invent claims the data doesn't support.**
   If `CLAIMS_FROM_RESULTS` says partial, do not round up to "yes" in the narrative.
4. **Honest limitations save the paper.**
   Round-2 reviewers (human or auto) punish overclaiming far harder than they punish modest claims.
5. **The narrative is editable.**
   Treat the first generation as a draft -- expect a human pass before downstream stages consume it.
6. **One narrative per paper**, not per probe.
   Multi-probe projects collapse into one story or split into separate papers; don't try to fit two stories into one narrative.
7. **Venue-ALIGNED arc.**
   The narrative is explicitly venue-aligned: read STATUS `venue` and the paper's `0-lifecycle/2a-venue/2a-venue.md` FIRST -- the Structural Blueprint blocks (section roles, beat allocation, paragraph budgets) plus Writing Principles -- for what the venue rewards in terms of narrative arc and argument structure.
   This contract shapes which beats are expanded (theory-forward for MISQ, clinical-impact-forward for JAMA) and which are condensed.
   Fall back to `venue/playbook-<venue>` directly only when `2a-venue.md` is absent (venue stage not yet run, or a pack-less venue); if no pack exists either, proceed without venue inputs.
   Deep dives follow the `[source: ...]` tags in `2a-venue.md` into `venue/playbook-<slug>/<journal>/...`.
   If `2a-venue.md`'s recorded pack commit is behind the current `venue` HEAD, note "venue contract stale -- consider /haipipe-paper-venue refresh" but still use `2a-venue.md` (never silently re-read packs).
8. **Comment text is short and plain.**
   All comment text (interrogation, external comments, footer ledger lines) uses short declarative sentences, one idea each.
   No run-on lines chained by semicolons, no stacked parentheticals; compress rather than nest, split rather than join.
   A long compound line is unreadable, and the comment thread exists to scan at a glance.
   Same readability discipline as the pitch.
   (Reviewer feedback quoted verbatim stays verbatim; only OUR resolution prose follows this rule.)
9. **External reviewer comments thread per beat.**
   When a named reviewer comments on the paper, attach each comment to the beat it concerns; do not collapse them into one footer paragraph.
   Internal = interrogation; external = named reviewer.
   A comment with no home beat stays in the footer.

## Questions this stage typically raises

DRAFT's Step 4b raises what the draft cannot answer. Narrative asks per BEAT — a beat that cannot be sourced is a beat that cannot be written.

```
⚓ beat anchor      This beat asserts something about the field. Which source carries it?
                    Every [LIT] tag is this question, not yet asked.
🕳️ gap beat        A [GAP] beat has no evidence at all. What would produce it, and is it
                    worth producing? Every [GAP] is a question or a cut — never a maybe.
🖼️ display need    Does this beat need the reader to SEE something? Then it owes a DR row
                    in 0-lifecycle/4-display/_DISPLAY_REQUEST.md, not a promise.
🧵 arc break       Does the throughline actually survive this beat order, or does the
                    argument need a fact we have not established to get from here to there?
```

## Handoff

On CHECK confirm, update `STATUS.md` (`current_layer`, `maturity: narrative`) and advance:

```text
promote     -> /haipipe-paper display <paper-dir>
```

End the reply with the stage strip (run `../../../haipipe-paper/stage-strip.sh`).
