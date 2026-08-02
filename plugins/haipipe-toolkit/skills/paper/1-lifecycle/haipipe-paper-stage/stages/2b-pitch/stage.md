---
# CONTRACT — machine-readable. No `name:` field: this is DATA the router reads,
# not a registered skill.
key: pitch
order: "2b"
title: Pitch
one_line: "Why would THIS venue's editor send this paper out for review?"
board_family: Venue
board_unit: "1"
board_slug: pitch          # family + unit + slug resolve the S-face filename;
                          # haipipe-board/stage.py owns that resolution (QB4@paper)

phases: [draft, probe, revise, check]
gates: [check]             # THE HUMAN GATES THIS STAGE OPENS, declared like `phases:`.
                           # Default is ONE, at CHECK. DRAFT/PROBE/REVISE run unattended.
                           # This is safe only because PROBE cannot spend: see probe_depth.
probe_depth: 0             # THE CEILING on what PROBE may dispatch, on the bank's own ladder
                           # (task/haipipe-task/fn/qa.md:102-107), which maps 1:1 onto the
                           # consumer's `bank:` verdict:
                           #   0 READ        reuse  results already answer it   free, nothing runs
                           #   1 NEW RUN     run    old script, new config      costs
                           #   2 NEW SCRIPT  code   must write new code         costs
                           #   3 NEW FOLDER  new    open a new task-folder      costs most
                           # Rule: dispatch when depth(bank) <= probe_depth, else DEFER.
                           # At 0 the stage can only HARVEST, so a run of it is free and needs
                           # no gate. Raise it per invocation with `probe --depth N`.
runs: once
needs_paper: true
on_rerun: diff-and-ask   # QB2c, ruled 260727. Protected on a re-run: any `> <ACTOR>:`
                         # lane, `state:`, `## States`, a settled State row, a GATE row in
                         # `## Log`. Everything else: compute the change, SHOW it, ask.
                         # Never silently overwrite. Full rule: ../CONTRACT.md.
venue_aligned: true       # REWRITES when the venue changes (claims does not — it is venue-free)

artifact: 0-lifecycle/2-venue/S-Venue-1-pitch.md
artifact_fallback: 0-lifecycle/2-venue/2b-pitch.md
                          # papers that predate the 2026-07-25 S-face restructure carry
                          # the stage file under its old name. Use this ONLY when the
                          # resolved S face is absent, and say which one you used.
archive: 0-lifecycle/2-venue/archive/vNN_<reason>.md
probes: 1-probes/PPNN_<topic>/
template: template.md
support: [readability.md]   # the 9 global language rules, section lead cues, hook method menu,
                            # worked rewrites, reviewer checklist — LARGER than the template

exit_when: "abstract/intro sells another story"   # the stage's own failure exit

venue_contract:           # read FIRST, before a word is drafted — see the craft body
  read: 0-lifecycle/2-venue/S-Venue-0-venue.md
  blocks: [Venue Profile, Fit Assessment]
  shapes: [Editor's Chair Test, "[primary] designation", RQ framing, Audience and Venue Fit]
  fallback: "venue/playbook-<venue> ONLY if S-Venue-0-venue.md is absent; with neither, proceed without
             venue inputs and say so"
  stale: "provenance commit older than venue HEAD -> note 'venue contract stale — consider
          /haipipe-paper-stage venue refresh', still use S-Venue-0-venue.md; never silently re-read packs"
  rewrite_when: "venue changes"

sections:                 # logical order; Q-consumer adapts to Board Aims
  - Title
  - One-Minute Pitch
  - Hook
  - Finding — Surprise
  - Implication — So What
  - Editor's Chair Test
  - Primary Claim + RQ Framing
  - Audience and Venue Fit
  - Evidence — Why Believe
  - Limitation — Still Fragile
  - Next Evidence Move
  - Q-consumer

formatting:
  title_rule: "====="
  section_rule: "-----"
  headings: "direct `###` divisions under Board Content; Q-consumer records are Aim records
             under `## Aims`, never Content headings"
  line_breaks: "one sentence per line (semantic line breaks); no dense paragraphs"
  records: "Primary Claim + RQ Framing uses record lines, never a pipe table"
  length: "readable in one minute; fits on one screen"

q_id_pattern: "- P<n> · Q-Pitch-<n> · <title>"
q_anchor: "[Q-Pitch-<n>] cited inline wherever a point rests on the open check (usually Evidence)"
closed_when: "PROBE writes the finding + [source: PP<nn>] into Answer; REVISE weaves it back in
              and discharges the [Q-Pitch-<n>] bracket"

done_criteria:
  - "all twelve sections present as LABELED sections; every <!-- RULE --> comment deleted"
  - "a flat paragraph missing the labeled sections is restructured before any gate can pass"
  - "Hook carries >=2 candidates, each committing to ONE narrative move, one marked
     (recommended lead), none hidden or collapsed"
  - "Editor's Chair Test quotes the venue question from S-Venue-0-venue.md and answers it in one
     sentence per primary claim"
  - "exactly ONE [primary] claim designated for THIS venue, supporting claims named"
  - "H→RQ mapping complete as record lines, each carrying its own 'why this RQ for this venue'"
  - "Surprise states the unexpected result in sentence 1; Implication names who can act within
     the first two sentences; Audience names the reader and their need before the venue format"
  - "every Why-Believe sentence ties to a table/display/model/check/source; planned marked planned"
  - "Still Fragile lists at most three weaknesses; Next Evidence Move starts with a verb and names
     the artifact it updates"
  - "readability.md passes — global language rules, per-section lead cues, reviewer checklist;
     reads aloud without stumbling"
  - "Q-consumer present (`- P<n> · Q-Pitch-<n>` in Aims), each record anchored to a draft assertion"
  - "the S page's ## Log records the current state; a SEMANTIC shift cites its source and archives the
     prior version to archive/vNN_<reason>.md"
  - "the paper-family probe-card checker, scoped `--stage pitch`, exits 0"

upstream: [claims, venue]
downstream: [narrative]
handoff: "on CHECK confirm, append the gate row to this stage's S page ## Log -> narrative"
---

Pitch — the craft
=================

The pitch is the COVER LETTER: the venue-ALIGNED document that tells THIS editor why THIS paper
fits THEIR journal. It can be sent as-is. It is not a paper plan, an outline, or a claim matrix —
it is the version a person understands in one minute.

The boundary with the stages around it:

```text
CLAIMS     is the claim TRUE?          venue-free, settled BEFORE the pitch is written
PITCH      does the story LAND HERE?   venue-aligned, rewritten when the venue changes
NARRATIVE  how does the arc RUN?       the section-mirrored expansion of this pitch
```

The venue contract is read FIRST
--------------------------------

Before a word is drafted, read `0-lifecycle/2-venue/S-Venue-0-venue.md` — its **Venue Profile** and
**Fit Assessment** blocks. Nothing substitutes for them. They shape four sections: the Editor's
Chair Test question, the `[primary]` designation, the RQ framing, and Audience and Venue Fit.

A venue change means the pitch REWRITES. Claims does not move — it is venue-free.

Each hook candidate commits to ONE move
---------------------------------------

This is the pitch's load-bearing taste, and the thing most often got wrong.

A hook opens a curiosity gap by committing to ONE narrative move, not by hedging across several:

```text
🌀 paradox / tension   expectation against reality        "We reward X; yet X does the opposite."
🎬 vivid scene         a concrete moment with specifics   "Two patients, same pain, two outcomes."
💥 surprising fact     the counterintuitive result first  "The most praised X is the worst Y."
🔥 stakes              what is at risk, up front          "<harm> continues, yet <gap> is unexplained."
🕳️ gap                 an obvious-in-hindsight blind spot "<data> exists, yet no one asked <question>."
❓ one sharp question  a single gap, <=20 words           "Can X, vividly described, predict Y?"
🔭 reframe             the familiar from a new angle      "X is usually done one way; what if…"
```

A STACK of rhetorical questions is THE failure mode. It dilutes the punch and reads as undecided —
the author could not choose, so the reader is asked to. A flat statement of background is not a
hook at all. Length is 2-4 short sentences: one lone sentence is abrupt, past four it starts
eating the One-Minute Pitch.

Keep EVERY candidate visible, permanently — at least two, one marked `(recommended lead)`, none
hidden. The author picks the lead at write time, and the surviving alternates are how a later
venue change gets re-pitched cheaply. For medical and empirical venues the ranking runs
paradox+stakes > surprising fact > vivid scene; gap and single-question are weak alone; analogy
and metaphor are risky in clinical writing.

Per-method risks and the worked before/after rewrite live in `readability.md`.

[primary] is a VENUE judgment
-----------------------------

Claims holds the venue-neutral H1/H2/H3 and their status. The pitch designates exactly ONE
`[primary]` claim FOR THIS VENUE and names the rest as supporting.

The test is not which claim is strongest. It is which claim THIS venue's readers are not already
sure of. A result that is novel elsewhere but established for this audience is an enabler — it
belongs in Methods, not on the marquee.

RQ framing is the same move at sentence level: H1 → RQ1, worded for what this editor rewards, each
mapping carrying its own "why this RQ for this venue". A venue change re-runs both.

One minute or it failed
-----------------------

If a reader slows to parse a sentence, the pitch failed. Read each section aloud; a stumble is a
rewrite. One idea per sentence, lead with the point, plain words over jargon this venue's readers
will not parse, concrete numbers over qualifiers, active verbs, no AI voice. Compress rather than
split — drop hedging and adjectives before chopping sentences into fragments.

Frame findings as a trade-off or a mechanism, never as blame. Not "nice doctors over-prescribe",
but "being agreeable can mean yielding to patient pressure, while clinical firmness can protect".

The One-Minute Pitch is written for a NEWCOMER: ~4-6 short sentences opening with a plain "We
study whether/how X relates to Y", then the puzzle, the method in plain words, the surprising
finding, why it matters. A lone compressed thesis sentence is too terse for the reader it is for.

Readability is part of the done-gate, not a polish pass. `readability.md` holds the rules.

Intuition is allowed; a SHIFT needs a source
--------------------------------------------

A seed pitch may rest on author judgment, a research review, or a rough direction. Every SEMANTIC
shift after that must cite one: a landed QA file in `discoveries/` or `tasks/`, a `read` entry in
`1-probes/`, reviewer feedback, venue strategy, or an explicit author decision.

Archive on story-state change (`seed -> discovery-shift`, `accuracy -> robustness`,
`method-first -> application-first`), never for typo edits.

What this stage asks
--------------------

The pitch asks whether this story LANDS AT THIS VENUE:

```text
🎯 venue fit        Has this venue published work of this SHAPE recently, and what did it look
                    like? An Editor's Chair answer needs a precedent, not a hope.
🏁 competing paper  Is someone else telling this story right now — a preprint, a conference
                    version, a group known to be on it?
⚓ anchor source    The hook and the surprise each lean on a claim about the field. Which source
                    anchors it? A pitch anchored to nothing is a guess.
⚠️ framing risk     Which framing would an editor read as overclaiming, and what evidence would
                    we need to keep it?
```

NOT here: whether the claim is TRUE. That was settled in claims, venue-free, before the pitch was
written.

Not from the pitch
------------------

Do not write the paper here — abstract, introduction, section plan, and LaTeX belong downstream.
Do not let a downstream stage carry a different story: if narrative, the hero figure, or the
discussion disagrees with the pitch, either update the pitch with a logged reason or revise the
downstream stage. Two stories in one manuscript is this stage's failure exit.
