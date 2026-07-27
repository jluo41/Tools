---
# CONTRACT — machine-readable. No `name:` field: this is DATA the router reads,
# not a registered skill.
key: seed
order: "0"
title: Seed
one_line: "Why might this paper exist?"
board_family: Seed
board_unit: "0"
board_slug: seed          # family + unit + slug resolve the S-face filename;
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
venue_free: true          # does not change when retargeting to another journal

artifact: 0-lifecycle/0-seed/S-Seed-0-seed.md
artifact_fallback: 0-lifecycle/0-seed/0-seed.md
                          # papers that predate the 2026-07-25 S-face restructure carry
                          # the stage file under its old name. Use this ONLY when the
                          # resolved S face is absent, and say which one you used.
probes: 1-probes/PPNN_<topic>/
template: template.md

exit_when: "not viable -> drop the paper"   # the stage's own failure exit

sections:                 # logical order; Q-consumer adapts to Board Items to Finish
  - Seed Question
  - Motivations
  - Landscape
  - Tentative Claim Shape
  - Q-consumer

formatting:
  title_rule: "====="
  section_rule: "-----"
  headings: "direct `###` divisions under Board `## Content`; Q-consumer records are checklist
             items under `## Items to Finish`, never Content headings"
  line_breaks: "one sentence per line (semantic line breaks); no dense paragraphs"

q_id_pattern: "- [ ] 🔎 Q-Seed-<n> · <title>"
q_anchor: "[Q-Seed-<n>] cited inline in every sentence the question hangs on"
closed_when: "REVISE weaves the Answer back in and discharges the [Q-Seed-<n>] bracket"

dispatch_scope:           # what may LEAVE this stage — see the craft body, principle 5a
  - occupied-ground       # is the angle new? closest prior art on each half of the pairing
  - obtainability         # does the external data EXIST and can we get it? (in principle only)
defer_to: resource        # anything else: keep the Q block, `Answer: deferred -> RESOURCE`,
                          # emit `**[FORWARD -> RESOURCE] PPNN_<slug>**` in this S page's ## Log

done_criteria:
  - "all four Content divisions plus the Q-consumer records carry real content; every <!-- RULE --> comment deleted"
  - "every question the draft hangs on is a Q-consumer checklist record, anchored to a draft assertion"
  - "each Q marked DISPATCHED (an entry in 1-probes/) or DEFERRED (no entry, forward pointer)"
  - "no bare \\cite{TOADD} — the citation command and its [Q-Seed-<n>] bracket sit side by side"
  - "the S page's ## Log records phase history and the gate row"
  - "check-probe-cards.sh <paper_root> --stage seed exits 0"

upstream: []
downstream: [resource]
handoff: "on CHECK confirm, append the gate row to this stage's S page ## Log and hand to resource.
          The row is HISTORY (who confirmed, when, what was deferred), which is the one thing about a
          paper that cannot be derived from disk. It goes on the page whose gate it was, so a reader
          is already standing where they want it.
          There is no frontier to advance and none to protect: the frontier is DERIVED from each
          page's own `state:`, so a LOOPBACK — running seed again on a paper whose frontier is
          further along — simply records its gate and changes nothing else. That is what retiring
          a derived frontier makes possible. See ../../../ref/08-stage-gate.md."
---

Seed — the craft
================

A seed may be INTUITION. It does not require evidence yet. It keeps a paper-shaped possibility
alive while the evidence is still forming. It is not a pitch, not a claim ledger, not an outline.

The boundary with the stage after it:

```text
SEED      is this paper WORTH doing, and is the data even OBTAINABLE in principle?
RESOURCE  what EXACTLY must exist, does it, and can it CARRY the claim?
```

RAISE freely; DISPATCH narrowly
-------------------------------

This is the seed's one load-bearing idea, and the thing most often got wrong.

Asking is cheap, so the Q-consumer is as generous as the draft needs. Raise ANY question the
prose actually hangs on, however far from feasibility it sits. When a sentence rests on something
no existing question tests, PROPOSE A NEW ONE rather than leave it unanchored. Nothing about a
question's shape disqualifies it from being ASKED here.

The narrow part is DISPATCH. What goes OUT at seed stays feasibility-shaped:

```text
👣 occupied ground   Has anyone already taken this angle? Name the closest prior art on
                     each half of the pairing, or name the ground as unoccupied.
📦 obtainability     Does the external data this paper needs EXIST, and can we get it?
                     In principle only — size and coverage are RESOURCE's.
```

A raised question of any other shape — profiling OUR OWN data (cohort size, field coverage, label
availability in our AIData), or any other prerequisite — KEEPS its `## Q-Seed-<n>` block, gets NO
entry in `1-probes/`, records `Answer: deferred -> RESOURCE`, and carries a forward pointer. It
fires when resource opens.

**The split costs nothing to get wrong now.** At `probe_depth: 0` a dispatched question can only
HARVEST an answer the bank already holds — free — so DRAFT no longer needs a human to bound spend,
and this stage opens no gate before CHECK. Anything the bank cannot close for free comes back
`deferred`, and the human decides at CHECK (or when raising `--depth` for a batch) which deferred
questions are worth paying for. Raising stays free; only PAYING is gated.

There is NO CAP on how many questions a seed raises. The count that matters is how many it
DISPATCHES, and the gate sets that — not this document.

DRAFT may search; PROBE must bind
---------------------------------

Inline WebSearch is legitimate DRAFT fuel — orientation that becomes prose plus `planned`
q-executor entries. It is NEVER evidence.

PROBE must ALWAYS run the real worker. An inline result binds to nothing.
DRAFT raises the Q-consumer question; PROBE alone opens the entry, MATCHes it,
dispatches within the ceiling, and harvests `### a-executor`.

Profiling OUR OWN data belongs in RESOURCE. Such a question may well have been RAISED here — it
was deferred at the gate, and it is not dispatched from this stage.

The forward pointer has ONE emitted form
----------------------------------------

Seed emits, in its S page's `## Log`, ASCII arrow, destination RESOURCE:

```text
**[FORWARD -> RESOURCE] PPNN_<slug>**
<the need, and why it is not a seed question>
```

Resource's DRAFT consumes it with a grep that is glyph- and legacy-tolerant —
`grep -E "\[FORWARD (->|→) (RESOURCE|CLAIMS)\]"` — because 7 pointers written before the resource
stage existed say `CLAIMS`, and one of them uses a unicode arrow. Emit the ASCII/RESOURCE form for
anything new; never rewrite a legacy pointer to match, the consume-grep already takes it.

Not from the seed
-----------------

Do not create `sections/`, displays, or compile obligations here — those start later.
Do not reference a target venue: venue selection happens after claims
(`seed -> resource -> claims -> [venue] -> pitch`).
Evidence inventory, routing, and gap analysis belong to claims, not here.
