---
# CONTRACT: machine-readable. No `name:` field: this is DATA the router reads,
# not a registered skill.
key: round
order: "6"
title: Round
one_line: "Where does this dated batch's feedback, decision, applied change, and response go?"
board_family: Round
board_unit: "the round number n (0, 1, 2, …), allocated next-unused, never reused"

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
# The phase list above runs once PER ROUND, not once for the paper. Phase mapping:
#   DRAFT   intake + triage: land the received material verbatim, atomize it into the
#           coverage ledger, record accepted decisions; routes work, never executes it
#   PROBE   evidence for ledger items the paper cannot answer from disk (a reviewer-demanded
#           robustness check, a prior-art claim); MATCH before DISPATCH, ceiling below
#   REVISE  apply: route each accepted item to its owning stage/page, record what changed and
#           which item it closes; draft the response/rebuttal when the round answers external
#           reviewers (craft: ../rebuttal-craft.md)
#   CHECK   close: every item applied or explicitly parked with a reason, close receipt

gates: [check]             # ONE human gate, at close. DRAFT/PROBE/REVISE run unattended.
                           # Safe only because PROBE cannot spend: see probe_depth.
probe_depth: 0             # THE CEILING on what PROBE may dispatch, on the bank's own ladder
                           # (task/haipipe-task/fn/qa.md), mapping 1:1 onto the consumer's
                           # `bank:` verdict:
                           #   0 READ        reuse  results already answer it   free, nothing runs
                           #   1 NEW RUN     run    old script, new config      costs
                           #   2 NEW SCRIPT  code   must write new code         costs
                           #   3 NEW FOLDER  new    open a new task-folder      costs most
                           # Rule: dispatch when depth(bank) <= probe_depth, else DEFER.
                           # A reviewer-demanded experiment is usually depth 1+; raising the
                           # ceiling is the human's call, per invocation: `probe --depth N`.
runs: per-unit
unit: round                # one unit = ONE dated batch of iterative work: a coauthor pass,
                           # an editor letter, an external review cycle, an internal sweep
units_from: 0-lifecycle/S10-round/
             # The unit list is the S-Round pages already on disk; a NEW round allocates the
             # next unused number and today's vYYMMDD slug. No stored pointer, no latest.md:
             # the active round is DERIVED (non-green state + date/unit order).

# ⚠️ ARGUMENT ORDER (the round is not positional 1):
#      /haipipe-paper round <n|new> [draft|probe|revise|check] [paper-path]
#    The stage key is always positional 1 under the door; the unit slides to 2.
argument_hint: "<round-n | new> [draft|probe|revise|check] [paper-path]"

needs_paper: true
on_rerun: diff-and-ask   # QB2c. Protected on a re-run: any `> <ACTOR>:` lane, `state:`,
                         # `## States`, a settled State row, a GATE row in `## Log`.
                         # Everything else: compute the change, SHOW it, ask.
                         # Full rule: ../../haipipe-paper/stages/CONTRACT.md.
venue_free: true          # a round is a dated HISTORICAL record of one exchange; a retarget
                          # to another journal opens a NEW round, it never rewrites old ones

artifact: 0-lifecycle/S10-round/S-Round-{board_unit}-{board_slug}.md
                          # PER ROUND. board_slug is the unit's date tag, vYYMMDD, allocated
                          # at creation; the FILENAME is resolved by haipipe-board/stage.py
                          # from family, unit and slug (QB4@paper), never spelled here.
                          # Received material (a reviewer letter, a coauthor memo) is copied
                          # or linked BESIDE the page in S10-round/, only when supplied.
probes: 0-lifecycle/S03-literature/probes/L<n>-<topic>/ | 0-lifecycle/S04-value/probes/V<n>-<topic>/
displays: 0-lifecycle/S03-literature/display/L<n>-<topic>/ | 0-lifecycle/S04-value/display/V<n>-<topic>/  # audit candidate dispositions and selected units by claim
checker: paper/haipipe-paper/probe/check-probe-cards.sh --stage round
                          # run by CHECK before judging; path relative to the skills root
craft:                    # data files the DRAFT/REVISE phases load after the type contract
  - ../rebuttal-craft.md  # the reviewer-response craft: coverage/provenance/commitment
                          # gates, issue atomization, strategy, drafting pattern

template: template.md     # the round page skeleton (this folder); rounds are venue-free,
                          # so there is no per-venue template resolution

read_order:               # optional DRAFT orientation; dependencies live on the Board page
  received:      the letter/feedback material beside this page in 0-lifecycle/S10-round/
  claims:        0-lifecycle/S02-work/S-Work-C-claims.md
  board:         0-lifecycle/board.md and the affected S pages' `state:` lines

exit_when: "an item needs NEW evidence beyond the ceiling -> the owning stage + its PROBE
            (record the deferral on the ledger row); an item with no target cannot close"

sections:                 # logical parts; Q-consumer adapts to Board Aims
  - Source and intake     # what arrived, from whom, verbatim or linked; the round's purpose
  - Coverage ledger       # one row per atomic item: id, quote anchor, decision, target, state
  - Decisions             # accepted rulings, with who ruled and when
  - Applied changes       # what changed where, item id it closes; unresolved stays visible
  - Response              # the reply/rebuttal artifact, when the round answers external readers
  - Close receipt         # affected page gates, build pointer, forward pointers
  - Q-consumer            # mandatory Aim records under Aims

formatting:
  headings: "direct `###` divisions under Board Content per the sections above; Aim records
             under `## Aims` per Q-consumer"
  ledger: "record lines, one item per line block, never markdown tables; every item names
           its target page or its parked reason"
  received_material: "verbatim, never paraphrased at intake; interpretation happens on the
                      ledger, quotes anchor back to the letter"
  template_residue: "grep -c '<tpl' on the page must print 0"

q_id_pattern: "- P<n> · Q-Round<unit>-<n> · <title>"
                                            # THE STAGE TOKEN IS THIS UNIT (this stage
                                            # `runs: per-unit`), so ids never collide across
                                            # rounds: Q-Round0-1, Q-Round1-3. Derive the unit
                                            # from the S page filename S-Round-<unit>-<slug>.md.
q_anchor: "[Q-Round<unit>-<n>] beside the ledger row or response sentence that needs the
           evidence; the entry's Reason names the reviewer point or decision that raised it"
closed_when: "PROBE writes the Answer + the target: QA-file path; CHECK's human verifies;
              the ledger row it serves flips to answered and the response sentence cites the
              evidence, never a promise"

done_criteria:
  - "every intake item appears on the coverage ledger exactly once; nothing silently disappears"
  - "every ledger item is applied (with its change recorded under Applied changes), answered,
     or explicitly parked with a reason and an owner"
  - "every applied item names the owning S page it changed; reopened pages carry their own
     re-gate obligation (this round records, it does not gate for them)"
  - "when the round answers external reviewers: the Response division holds the drafted reply
     and it passes the three rebuttal gates (coverage, provenance, commitment;
     ../rebuttal-craft.md)"
  - "the close receipt names the resulting build/candidate when one was produced"
  - "check-probe-cards.sh <paper_root> --stage round exits 0"

upstream: [section-edit]  # craft orientation, not a dependency graph: a round may reopen ANY
downstream: []            # family; the authoritative dependency is the page's own requires:.
                          # Nothing is downstream: a closed round feeds the NEXT round.
handoff: "on CHECK confirm (close), append the gate row + close receipt to THIS round's S page
          ## Log; reopened S pages keep their own gates; the next batch opens a new round page"
---

Round: the craft
================

Rounds are paper working memory expressed in the same Board grammar as every other lifecycle
unit. One round equals one page:

```text
0-lifecycle/S10-round/
├── S-Round-0-v260726.md
├── reviewer-letter-v260726.md   # optional received material beside its page
└── ...
```

There is no `latest.md`, `todo.md`, `decisions.md`, `discussion.md`, or `applied.md`. Those
would duplicate the S face and drift. The active round is DERIVED: non-green state plus
date/unit order; never read or create a stored pointer.

A response or rebuttal is an artifact INSIDE a round, not a top-level concern: it lives in
the page's Response division, beside the feedback it answers and the changes it promises.

Triage routes (DRAFT fills the ledger; REVISE routes the work)
--------------------------------------------------------------

Every ledger item names ONE target. Triage does not execute the work.

```text
claim unsupported / too strong      0-lifecycle/S02-work/S-Work-C-claims.md, then that
                                    stage's PROBE
display missing / stale             a DR row in the Display stage's request inbox
                                    (0-lifecycle/S05-display/)
paragraph placement unclear         the owning 0-lifecycle/S06-main/ section page
appendix issue                      the owning 0-lifecycle/S07-appendix/ page
wording / flow / style              the owning S page, then its declared REVISE/CHECK sequence
citation / value evidence           the owning Q-consumer, then that stage's PROBE route
reviewer response text              this page's Response division (craft: ../rebuttal-craft.md)
build / package for resubmission    the door's build verbs (fn/compile.md · fn/diffpdf.md ·
                                    fn/project.md)
```

Evidence always enters through a stage's PROBE phase; a round never runs bank work inline. A
reviewer-demanded experiment is a question ENTRY first: MATCH against the bank often closes
it (the run already exists), and only what MATCH cannot close is a spend decision, made by a
human raising the ceiling.

Nothing disappears
-------------------

The ledger is the round's honesty device. Every intake item ends in exactly one of:
applied (with its change recorded), answered (with its evidence), or parked (with a reason
and an owner). A concern that will NOT trigger a change is still a ledger row, closed with
its one-line reason. This is what makes the close receipt trustworthy and what a follow-up
round builds on.

Close is a human gate
----------------------

CHECK presents the close summary: ledger counts by state, pages reopened and their current
gates, the response (when one exists), the build pointer. Only after explicit approval does
the first state token become `✅` and the gate receipt land in `## Log`. Never close a round
with an unresolved item that is not explicitly parked.

Comment rules (binding)
------------------------

Never delete or reword a `> USER:` (or any `> <ACTOR>:`) lane; reply `> CC:` underneath;
only the user resolves a thread; a resolved thread MOVES verbatim into this S page's
`## Log`. Received letters are quoted, never edited. Surgical edits only; a full-page
rewrite of a page carrying comment lanes is forbidden.
