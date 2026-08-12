---
# CONTRACT — machine-readable. No `name:` field: this is DATA the router reads,
# not a registered skill.
key: narrative
order: "3"
title: Narrative
one_line: "How does the evidence compose into a section-mirrored, readiness-tagged story?"
board_family: Work        # JL ruling 2026-07-25: the narrative is the third half of the
board_unit: "N"            # venue contract (what the outlet requires, what the paper promises,
                           # the story that promise implies), not the zeroth Main section.
board_slug: narrative      # family + unit + slug resolve the S-face filename;
                           # haipipe-board/stage.py owns that resolution (QB4@paper)

dashboard: none
#            no aggregate this stage's own pages cannot each answer for themselves.
#            Declared rather than left blank: a missing key reads as an
#            oversight, and this is a decision.
#            A dashboard is not a page TYPE: `for-dashboard` failed the
#            admission test's fourth question on 260806, because the four
#            pages wearing `-Dash` are three different things (two control
#            pages, one rehearsal, one measurement) and no single closing
#            rule covers them. What IS shared is the measured BLOCK, a span
#            any page may carry, and its rule is freshness rather than
#            completion: `check.py` reports a block older than its page's
#            newest Log date.

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
needs_paper: false        # argument-hint `[paper-dir-or-topic]` — a bare topic is accepted
on_rerun: diff-and-ask   # QB2c, ruled 260727. Protected on a re-run: any `> <ACTOR>:`
                         # lane, `state:`, `## States`, a settled State row, a GATE row in
                         # `## Log`. Everything else: compute the change, SHOW it, ask.
                         # Never silently overwrite. Full rule: ../CONTRACT.md.
venue_aligned: true       # REWRITTEN when the paper is retargeted to another journal

artifact: 0-lifecycle/S02-work/S-Work-N-narrative.md
artifact_fallback: 0-lifecycle/S01-opening/3-narrative.md
                          # papers that predate the 2026-07-25 S-face restructure carry
                          # the stage file under its old name. Use this ONLY when the
                          # resolved S face is absent, and say which one you used.
probes: 0-lifecycle/S03-literature/probes/L<n>-<topic>/ | 0-lifecycle/S04-value/probes/V<n>-<topic>/
displays: 0-lifecycle/S03-literature/display/L<n>-<topic>/ | 0-lifecycle/S04-value/display/V<n>-<topic>/  # Narrative assigns claim role and selects candidates before S05 opens a unit
display_request: 0-lifecycle/S05-display/_DISPLAY_REQUEST.md   # one DR row per SELECTED candidate,
                          # filed on this stage's behalf; the DISPLAY stage owns the formal unit
                          # and advances its acceptance statuses
checker: paper/haipipe-paper/probe/check-probe-cards.sh --stage narrative
                          # run by CHECK before judging; path relative to the skills root
craft:                    # data files DRAFT loads after the type contract (ex workers/)
  - ../../S03-literature/citation-craft.md
  - ../../S04-value/values-craft.md
  - ../../S05-display/display/draft-craft.md
template: template.md

exit_when: "arc weak -> pitch / claims"   # the stage's own failure exit

venue_contract:           # read BEFORE composing — see the craft body
  read_first: 0-lifecycle/S01-opening/S-Open-Venue.md   # Structural Blueprint beats + Writing Principles
  fallback: venue/playbook-<venue>               # only if S-Venue-0-venue.md absent; no pack -> proceed without
  stale: "recorded pack commit behind venue HEAD -> note 'consider /haipipe-paper venue refresh',
          but still use S-Venue-0-venue.md; never silently re-read packs"

sections:                 # in order. The MIDDLE IS NOT FIXED (JL 260802, ruling A): one `## ` per
                          # section THIS paper writes, taken from read_first's Structural Blueprint
                          # and adapted. Each carries `venue-section:` and `Adaptation:`.
                          # template.md's Introduction/Methods/Results/Discussion are a FALLBACK,
                          # used only when no blueprint exists. `units_from` makes each one an
                          # S-Main page, so this list IS the manuscript's page list.
  - Readiness Legend
  - Spine (throughline)
  - "<venue sections>"    # variable count, from S-Venue-0-venue.md's Structural Blueprint
  - Probes
  - Footer Ledger

readiness_tags: [READY, PENDING, INFER, LIT, GAP]   # exactly one per beat; meanings in the craft body

read_order:               # optional DRAFT craft order; dependencies live on the Board page
  - 0-lifecycle/S01-opening/S-Open-Pitch.md      # the framing constraint, NOT evidence
  - 0-lifecycle/S02-work/S-Work-C-claims.md    # the spine; the ONLY home of a claim's status
  - experiment results under figures/ · results/ · outputs/ · tasks/
  - review history and recorded limitations
  - repo source                           # one paragraph on what was BUILT, not what was proposed
on_conflict: "trust the most data-grounded source (claims ledger > experiment files > review
              history > idea report) and surface the discrepancy as a note"

formatting:
  title_rule: "====="
  section_rule: "-----"
  headings: "direct `###` divisions under Board Content; Q-consumer records are Aim records
             under `## Aims`, never Content headings"
  line_breaks: "one sentence per line (semantic line breaks); no dense paragraphs"
  comments: "short plain sentences, one idea each; compress rather than nest, split rather than join"

q_id_pattern: "- P<n> · Q-Narrative-<n> · <title>"
q_anchor: "[Q-Narrative-<n>] cited inline on every beat the question hangs on; written
           `\\cite{TOADD} [Q-Narrative-<n>]` / `{VAL:? <what>} [Q-Narrative-<n>]` —
           marker and bracket side by side, never fused"
closed_when: "REVISE weaves the Answer into the beat and discharges the [Q-Narrative-<n>] bracket"

done_criteria:
  - "every beat carries exactly one readiness tag; no untagged beat"
  - "no [GAP] or [PENDING] beat without a Q-consumer Aim record and a nested question entry under S03 or S04"
  - "no placeholder without its bracket — a \\cite{TOADD} or {VAL:?} carrying no [Q-Narrative-<n>]
     is a hole no question will ever fill"
  - "every beat needing a display names a selected candidate card; only then does it carry a DR row in 0-lifecycle/S05-display/_DISPLAY_REQUEST.md"
  - "per-beat interrogation complete — an independent subagent ruled on every beat"
  - "Spine present, and every beat below it serves it"
  - "venue contract consulted for arc shaping (S-Venue-0-venue.md; pack fallback if absent)"
  - "the S page's ## Log records phase history and the gate row"
  - "check-probe-cards.sh <paper_root> --stage narrative exits 0"

upstream: [pitch]
downstream: [display]
handoff: "on CHECK confirm, append the gate row to this stage's S page ## Log -> display"
---

Narrative — the craft
=====================

The narrative is NOT a draft of the paper. It is the design CONTRACT the paper writes from.
Every claim, figure, and citation in the final PDF should trace back to a line in this file, and
what is not in this file the downstream stages will not invent.

The boundary with the stages on either side:

```text
PITCH      the one-minute public-facing story — read here as a CONSTRAINT, not as evidence
NARRATIVE  how the evidence COMPOSES into a section-mirrored, readiness-tagged story
DISPLAY    what the reader must SEE; SECTION-EDIT writes the actual manuscript prose
```

If the evidence forces a different pitch, update `S-Venue-1-pitch.md` through the pitch stage and log the
shift. Never let the narrative silently diverge from the pitch it was built against.

The five readiness tags
-----------------------

Every beat carries exactly one. The tag is not decoration — it is the beat's evidence status and
its routing instruction.

```text
🟢 [READY]    evidence in hand: a confirmed probe, or a run we trust.
🟠 [PENDING]  the data EXISTS; a render, check, or probe is still open. It is on its way to READY.
🟣 [INFER]    a reasoned step BEYOND the evidence, grounded in it, never measured.
🔵 [LIT]      rests on outside literature; the citation audit is still owed.
🔴 [GAP]      no evidence at all. It becomes a question, or it gets cut — never a maybe.
```

`[INFER]` is the one that is not self-explanatory, because it is the only tag NO probe will ever
close. That is both what it licenses and what it costs. It LICENSES asserting the thing — a
mechanism, an implication, a so-what — with no measurement behind it, on one condition: the beat is
phrased as the most plausible reading, never as established. It COSTS the beat any route to
`[READY]`: an `[INFER]` beat is finished the day it is written, is never dispatched to the probe
layer, and is never quietly promoted. The distinction that decides the tag is whether a run COULD
settle it. Something we could measure but have not is `[GAP]` or `[PENDING]`. Something no run
could ever settle is `[INFER]`. Labelling the first as the second is exactly how a paper overclaims.

`[PENDING]` and `[GAP]` beats ARE the paper's live evidence worklist, and `[LIT]` is its citation
worklist. Never upgrade a beat to `[READY]` without the evidence actually in hand.

An arc COMPOSES; it never GATHERS
---------------------------------

This is the narrative's one load-bearing discipline, and the thing most often got wrong.

The arc arranges evidence that already EXISTS or is already OWED. It does not produce evidence.
When a beat exposes a hole — a number nobody has run, a source nobody has read, a check nobody has
done — the arc does not stop and fill it inline. It ROUTES BACK and keeps composing:

```text
missing number / unrun check   ->  [GAP] beat + Q-consumer block + ENTRY in 1-probes/
missing citation               ->  [LIT] beat + Q-consumer block + ENTRY in 1-probes/
the claim itself is unsettled  ->  back to CLAIMS — a beat may not outrank its ledger row
the data may not exist at all  ->  back to RESOURCE
the arc itself does not hold   ->  back to PITCH (exit_when: arc weak)
```

Gathering inline is the failure this rule exists to prevent. An agent that answers its own `[GAP]`
with a quick search has produced an unbound answer, a beat that LOOKS `[READY]`, and nothing anyone
can audit. Inline search is legitimate DRAFT orientation and nothing more; it is never evidence.

Beat discipline
---------------

The Spine sits above everything: one paragraph, an arrow chain — problem → the move this paper
makes → the core finding → the so-what. Every beat below must serve that line.

Each section block is a heading plus a plain-language subtitle, a **Flow:** arrow chain of its own,
a grounded draft-quality prose paragraph (the literal opener the manuscript grows from), and then
Key points to cover. A beat is `[TAG] **Label:** one to three sentences` — that is the whole shape.

**Builder is not judge.** The drafting agent does not author its own inclusion justifications —
self-authored "why it's here" comes out limp and circular. ONE reviewer subagent sees ALL beats at
once, so it can judge flow, redundancy, and gaps rather than each beat in isolation. It returns per
beat a verdict (keep | move-to-section | demote-to-Supplement | cut) plus one sharp venue-aware
sentence, and the drafting agent INTEGRATES those comments visibly subordinate to their beats.

**External reviewer comments thread per beat.** A named outside reviewer (co-author, advisor,
referee) has each comment attached to the BEAT it concerns, never collapsed into one footer
paragraph — that is what makes a review pass trackable at the point where the change must happen.
Each carries: name; status (`done | part | open`, judged against THIS contract, not against the
manuscript prose); their feedback VERBATIM, never paraphrased, compressed, or translated; and our
resolution in our own short plain sentences. On a beat that has both, the order is beat text,
internal comment, external comment. A comment with no single home beat stays in the footer ledger
with its source path.

Venue-ALIGNED
-------------

Read the pinned venue contract FIRST, before composing anything. Its Structural Blueprint (section
roles, beat allocation, paragraph budgets) and its Writing Principles decide which beats EXPAND and
which CONDENSE: theory-forward for MISQ, clinical-impact-forward for JAMA. Same evidence, different
arc. Retarget the paper and this stage is REWRITTEN, not patched.

Questions this stage typically raises
-------------------------------------

Narrative asks per BEAT — a beat that cannot be sourced is a beat that cannot be written.

```text
⚓ beat anchor    This beat asserts something about the field. Which source carries it?
                  Every [LIT] tag is this question, not yet asked.
🕳️ gap beat      A [GAP] beat has no evidence at all. What would produce it, and is it worth
                  producing? Every [GAP] is a question or a cut — never a maybe.
🖼️ display need  Does this beat need the reader to SEE something? Select a same-numbered
                  candidate card first, name its claim and role, then file its DR row in
                  0-lifecycle/S05-display/_DISPLAY_REQUEST.md.
🧵 arc break     Does the throughline survive this beat order, or does the argument need a fact
                  we have not established to get from here to there?
```

Not from the narrative
----------------------

No manuscript prose, no `sections/`, no compile obligations — those are section-edit's.
Do not invent claims the data does not support: if the ledger says partial, the beat says partial.
Honest limitations save the paper; reviewers punish overclaiming far harder than modest claims.
ONE narrative per paper, never one per experiment — two stories are two papers, not one narrative.
Treat the first generation as a draft; a human pass comes before display consumes it.
