---
# CONTRACT — machine-readable. No `name:` field: this is DATA the router reads,
# not a registered skill.
key: claims
order: "1b"
title: Claims
one_line: "Which claims are supported, refuted, or inconclusive?"
board_family: Work
board_unit: "C"
board_slug: claims          # family + unit + slug resolve the S-face filename;
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
needs_paper: true
on_rerun: diff-and-ask   # QB2c, ruled 260727. Protected on a re-run: any `> <ACTOR>:`
                         # lane, `state:`, `## States`, a settled State row, a GATE row in
                         # `## Log`. Everything else: compute the change, SHOW it, ask.
                         # Never silently overwrite. Full rule: ../CONTRACT.md.
venue_free: true          # does not change when retargeting to another journal

artifact: 0-lifecycle/S02-work/S-Work-C-claims.md
artifact_fallback: 0-lifecycle/S02-work/1b-claims.md
                          # papers that predate the 2026-07-25 S-face restructure carry
                          # the stage file under its old name. Use this ONLY when the
                          # resolved S face is absent, and say which one you used.
probes: 0-lifecycle/S03-literature/probes/L<n>-<topic>/ | 0-lifecycle/S04-value/probes/V<n>-<topic>/
checker: paper/haipipe-paper/probe/check-probe-cards.sh --stage claims
                          # run by CHECK before judging; path relative to the skills root
craft:                    # data files DRAFT loads after the type contract (ex workers/)
  - ../../S03-literature/citation-craft.md
  - ../../S04-value/values-craft.md
template: template.md

exit_when: "claim unsupported/too strong, no route"   # the stage's own failure exit

commissions:              # claims RUNS THE EXPERIMENT — it hands units OUT to the bank,
                          # through the probe layer's five-step loop. See the craft body.
  - haipipe-task-orchestrator-agent        # fit + eval; settles an INTERNAL experimental claim
  - haipipe-discovery-orchestrator-agent   # external cohorts/context/citations; never settles a claim alone

sections:                 # logical order; Q-consumer adapts to Board Aims
  - Hypotheses            # venue-NEUTRAL; the H1 -> RQ1 reframing happens in PITCH, not here
  - Claims                # one C<n>: statement + status + `Evidence: [Q-Claim-<n> …]`
  - Q-consumer            # one Board Aim record per question: Done when / Description / Reason / Probe / Answer

status:                   # THIS STAGE IS THE ONLY HOME OF A CLAIM'S STATUS — per-claim,
                          # private to this paper, NEVER in a probe file. No `## Verdict` section.
  vocabulary: [supported, refuted, inconclusive]
  confidence: "per-claim, written beside the status"
  claim_type: [associational, causal, in-sample, generalizing]
  blocked: "BLOCKED-ON-RESOURCE — cites the resource row it waits on (`-> N<n>` in S-Work-0-resources.md)"
  written_at: "INTERPRET, when a nested QA-probe's `#### A-executor` lands and the evidence page's consumers row records it"

formatting:
  title_rule: "====="
  section_rule: "-----"
  headings: "direct `###` divisions under Board Content; Q-consumer records are Aim records
             under `## Aims`, never Content headings"
  line_breaks: "one sentence per line (semantic line breaks); no dense paragraphs"

q_id_pattern: "- P<n> · Q-Claim-<n> · <title> — the title NAMES the angle, e.g. `· main coefficient (fit)`"
q_anchor: "[Q-Claim-<n>] listed on the `Evidence:` line of EVERY claim it bears on, and set beside every owed value it will fill"
closed_when: "REVISE feeds each landed Answer into the status of every claim it settles"

done_criteria:
  - "both Content divisions plus the Q-consumer records carry real content; every <!-- RULE --> comment deleted"
  - "every claim carries a status and an `Evidence:` line naming the Q-Claim-<n>s that settle it"
  - "every GAP/inconclusive claim has a plan and a question ENTRY — or is BLOCKED-ON-RESOURCE citing its `-> N<n>` row"
  - "every settled claim passes BOTH stages: the cited file exists with the number in it, AND a nested entry whose `target:` QA file resolves on disk carries the answer in its `#### A-executor`"
  - "no aspirational anchor cited as evidence — a `planned` entry settles nothing"
  - "no bare {VAL:?} or \\cite{TOADD} — the marker and its [Q-Claim-<n>] bracket sit side by side"
  - "the S page's ## Log records phase history and the gate row"
  - "check-probe-cards.sh <paper_root> --stage claims exits 0"

upstream: [resource]
downstream: [venue]       # claims is venue-free; venue is pinned AFTER it, then pitch
handoff: "on CHECK confirm, append the gate row to this stage's S page ## Log -> venue (-> pitch directly if the venue is already pinned)"
---

Claims — the craft
==================

Claims settles the paper's argument. Two things make it unlike every other stage.

**It is the ONLY home of a claim's status.** A probe entry carries the evidence itself (its
`### A-executor`); the A-consumer HERE says what that evidence MEANS for this paper. Two papers
reading the same bank fact may judge their own claims differently — the fact is shared, the
judgment is not, and the judgment is ours to write.

**It runs the experiment.** Training this paper's model and evaluating it is claims' work; resource
only checked the ingredients exist.

```text
RESOURCE  does the DATA / a reusable model / producing-CODE exist?   (the ingredients)
CLAIMS    train THIS paper's model (fit) + evaluate it (eval)        (the experiment -> the verdict)
```

The GPU-weeks SPEND gate therefore lives here, not in resource. A claim whose ingredients are not
ready is `BLOCKED-ON-RESOURCE` and gets NO build probe here — do not re-ask resource's question
under a claims id.

Decompose the experiment; never bundle fit+eval
-----------------------------------------------

One probe per task type. A bundled fit+eval makes a null uninterpretable; split, and each outcome
reads cleanly:

```text
fit stalls   a training problem — the claim is UNTESTED, not refuted, and no rebuild is forced
eval nulls   the effect is ABSENT — which is a real finding
```

The same discipline governs the Q-consumer. A claim is settled by SEVERAL small questions from
different angles — fit, eval, robustness, placebo, IV, external — never one. Name the angle in the
question title. "Is the effect real?" is not a question a task can answer; it is a claim wearing a
question mark.

M:N, both directions: a question may settle several claims, and a claim needs several questions.
Cite each question on the `Evidence:` line of every claim it bears on (forward), and name the
`C<n>`(s) in its own `Reason` (back). If one question needs another's answer first, say so there.

`supported` is a two-stage test
-------------------------------

```text
1  the cited file EXISTS and the number APPEARS in it
2  a probe entry whose `target:` QA file RESOLVES on disk, whose `### A-executor` carries the
   answer, and whose Q-consumer A-consumer here says that number CARRIES the claim
```

Stage 1 alone is a number nobody has judged; stage 2 alone is an assertion. AGGREGATION happens at
REVISE and the required angles must CONVERGE — one favorable question is not a supported claim, and
any angle still weak or GAP holds the whole claim below `supported`.

`claim_type` is the author's own overclaim check: never say "causes" from associational evidence,
and keep in-sample-only evidence at low confidence when the claim generalizes. No other stage in
the lifecycle runs this check.

Owed values name the question that will fill them
-------------------------------------------------

```text
{VAL:? <what>} [Q-Claim-<n>]      an owed number
\cite{TOADD} [Q-Claim-<n>]        an owed citation
```

Marker and anchor bracket sit SIDE BY SIDE, never fused. The bracket names the question that will
produce the value; the value lands in that question's `Answer`, sourced from the QA file its entry's
`target:` names. A placeholder with NO bracket is a defect — a hole no question will ever fill.

The four lenses
---------------

Claims asks whether the evidence actually carries the hypothesis.

```text
⚖️ sufficiency         Does this evidence support H<n>, or only fail to contradict it?
                       Name the effect, the N, and the test — not "results look good".
🔀 rival explanation   What else would produce this same result, and what would
                       distinguish the two? A claim with no named rival is untested.
📏 robustness          Does it survive the obvious alternative specification / sample /
                       cutoff? Name which one, and what would count as surviving.
🧱 ingredient          Is a prerequisite still missing? Then the claim is
                       BLOCKED-ON-RESOURCE — do not re-ask resource's question here.
```

Rival explanation is the lens reviewers reach for first, and the one a draft is most likely to skip.

Not from claims
---------------

Claims RECEIVES evidence, never PRODUCES it inline: it raises questions and the probe layer binds
them. Task settles an internal experimental claim; discovery supplies external cohorts, context,
and citations, and never settles one alone.
Hypotheses stay venue-NEUTRAL — the same H1 becomes RQ1 for a different venue, and that reframing
is PITCH's, not this stage's.
