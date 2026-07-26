# CHECK · Who may say a stage is done, and on what evidence?
state: 🟡 PARTIAL
owner: JL
method: one gate per stage; make the APPROVER visible where the state is read, not only where it is logged

## Question
A gate is the moment a stage becomes done, and the design spends the human's attention there and nowhere else, once per stage, on a finished thing rather than on a stream of approvals. Everything upstream is unattended because nothing upstream can spend. So CHECK carries the entire weight of the design's safety, and two things about it are less settled than they look: who is allowed to say yes, and what they are supposed to be reading when they do.

On who: an agent CAN say yes, and this is sanctioned rather than a loophole. `gate_mode: autopilot` puts a fresh-context reviewer subagent in the human's place; it returns approve or restart-from-a-named-phase, human-only items are marked DEFERRED into a queue rather than passed, and the Gate Ledger records the agent as the actor. `QA6` improved that on 260726 by retiring `STATUS.md` and moving the Ledger into each S page's own `## Log`, so the record of who passed a gate now sits on the page whose gate it was. What did not survive the move intact is where the MODE lives: two files claim it, and they name different places on the same page.

On evidence: every contract declares `done_criteria`, and across the eight there are 73 of them, of which 7 can be checked by a machine. The other 66 are judgments in prose. Every contract also declares `closed_when` and `exit_when`, the second being the stage's backward exit when the work fails. No page on this board has ever owned any of the three, so what a gate reads has been defined eight times and described zero.

## Boundary
- ✅ Covered here
  Who may pass a gate, what the gate reads, and where a stage goes when it fails.
- ↪ Covered elsewhere
  Why the earlier phases need no gate is `QB9`; the why-comments a gate reads are `QB10`; what a re-run does to a page that already passed is `QB5`; how a page's state is displayed is `QA9`.

## Diagram
```
   🚦 CHECK.   the human's attention, spent ONCE, on a finished thing.

      DRAFT ──▶ PROBE ──▶ REVISE ──▶  CHECK
      ╰────────  unattended  ───────╯   🧠 one yes

      ✅ safe upstream ONLY because probe_depth caps spending  → QB9
         remove that ceiling and all three need gates again.

   ── WHO MAY SAY YES: two sanctioned modes ─────────────────────────
      gate_mode:  copilot | autopilot                 default copilot

      ⚠️ AND IT HAS TWO DECLARED HOMES, WHICH DISAGREE
         ref/08-stage-gate.md:10       "the stage's S page FRONTMATTER"
         haipipe-paper-check:85        "gate_mode in the stage's
                                        S page ## LOG"
         …and :85 cites :10 as the owner while contradicting it.
         Both appeared when QA6 retired STATUS.md, which is where the
         field used to live. No live MISQ S page carries either.

      🧑 copilot     the human reads the exit-criteria report, adds
                     `> JL:` comments, and confirms / restarts / accepts

      🤖 autopilot   a FRESH-CONTEXT reviewer subagent reads the artifact
                     + the report, leaves `> REVIEWER:` comments, returns
                       approve                 ──▶ advance
                       restart-from-<PHASE>    ──▶ that phase re-runs,
                                                   READING the comments
                     · the LEDGER records the agent as actor
                     · HUMAN-ONLY items (bibtex 🔒) are never silently
                       passed: marked DEFERRED into a human queue
                     · the human may REOPEN any agent-approved gate,
                       which resets that stage's ledger row

      ⚠️ THE GAP IS NOT THE MODE. IT IS THE RECORD.
         QA6 260726 ✅  the Gate Ledger moved OUT of STATUS.md and
                        INTO each S page's `## Log`, one row on the
                        page whose gate it was. That is the right
                        home: history cannot be read off disk state.
         ⬜ not yet populated. No live MISQ S page carries a Ledger
            row; only `_archive/QA1-frontier.md` mentions one.
         ⬜ `state:` still shows ✅ and nothing else, so until the
            rows land, a gate a human read and a gate an agent
            approved look identical on the surface people read.

   ── ON WHAT EVIDENCE: what the gate actually reads ────────────────
                        done_criteria   machine-checkable
         0-seed               6              1
         1a-resource          9              1
         1b-claims            8              1
         2a-venue            10              0     ◄── none at all
         2b-pitch            13              1
         3-narrative          9              1
         4-display            9              1
         5-section-edit       9              1
         ─────────────────────────────────────
         TOTAL               73              7

      so 66 of 73 are JUDGMENTS IN PROSE. That is not a defect: most
      of them should be judgments. It does mean the gate is a reading
      task, and that no face has ever said so.

   ── AND WHERE IT GOES WHEN IT FAILS ───────────────────────────────
      exit_when:   every one of the eight declares a BACKWARD exit
        0-seed          not viable ──▶ drop the paper
        1b-claims       claim unsupported, no route
        3-narrative     arc weak ──▶ pitch / claims
        4-display       display cannot support claim
        5-section-edit  writing exposes missing evidence ──▶ claims
      ⚠️ CHECK is the only place a stage can take one, and no page on
         this board has ever mentioned the field.
```

## Content
### The mode is designed; the record has just moved and not arrived
Autopilot is not a hole somebody left open. It uses a fresh context so the approver is not the author, it refuses to pass human-only items, it records the actor, and it lets a human reopen anything it approved. Each of those is the right decision.

The record of who approved has just been given a much better home. `QA6` retired `STATUS.md` on 260726 and put the Gate Ledger into each S page's `## Log`, one row on the page whose gate it was, on the argument that history is the one thing that cannot be re-derived from disk. That is exactly right and it is not yet true: no live S page on the MISQ paper carries a Ledger row, so today the answer to "who passed this gate" is still nowhere a reader stands.

Meanwhile `gate_mode` came out of the same retirement with two homes. The gate protocol says it lives in the S page's frontmatter; the CHECK worker says it lives in the S page's `## Log` and cites the gate protocol as the owner while saying something different. Neither is populated anywhere, so nothing has broken, and the first paper to set the field will pick a side by accident.

### A gate is a reading task, and the contracts say so without saying so
Sixty-six prose criteria across eight stages is a real workload, and it is the workload the design is buying with everything upstream: three unattended phases exist so that this reading happens once, on something finished, with the REVISE why-comments beside it. That trade is the core of the design and it is stated on `QB10` from REVISE's side and nowhere from CHECK's.

The seven machine-checkable criteria are worth naming as the shape of the answer rather than the answer: `check-probe-cards.sh <paper_root> --stage <key> exits 0` appears in seven of the eight contracts, and `2a-venue` has none of any kind.

### The exit nobody has described
`exit_when` is how a stage says the work failed backwards: the arc does not hold, the claim cannot be supported, the writing exposed missing evidence. It is declared in all eight contracts, it can only be taken at CHECK, and it has never appeared on this board. A lifecycle with no described failure exit reads as though stages only ever succeed.

## Items to Finish
- [x] 🚦 One gate per stage, at CHECK
      Declared per stage as `gates:`, defaulting to `[check]`, honoured by all eight.
- [x] 🤖 The stand-in is designed rather than tolerated
      Fresh context, human-only items deferred not passed, actor recorded, reopenable.
- [x] 🏠 Give the Gate Ledger a home that survives
      `QA6` 260726: out of `STATUS.md`, into each S page's `## Log`, one row on the page whose gate it was. It was the only part of that file that is history and cannot be re-derived, and it was the last blocker to retiring the file.
- [ ] 🔧 Rule where `gate_mode` lives, and write it once
      `ref/08-stage-gate.md:10` says the S page's frontmatter. `haipipe-paper-check/SKILL.md:85` says the S page's `## Log`, and cites the first as the owner. Both were written when `STATUS.md` was retired; neither is populated on any live page.
- [ ] 🧨 Populate the Ledger on the pages that already have gates
      The new home is ruled and empty. Until a row lands, `state: ✅` is still the only signal, and it cannot say who passed.
- [ ] 📐 Own `done_criteria`, `closed_when` and `exit_when`
      Declared 8 times each, described nowhere. Say what a criterion is allowed to be, and which of the three the gate consults.
- [ ] 🔎 Decide what a surviving placeholder means at a gate
      A `\cite{TOADD}` that reaches CHECK is either a blocking defect or accepted debt. Today it is judged case by case.
- [ ] 📐 Describe the backward exit
      `exit_when` is the only way a stage says it failed. It fires at this gate and appears on no page.
- [ ] 🔎 Give `2a-venue` a machine-checkable criterion, or say why it has none
      It is the one stage with ten prose criteria and zero automated ones.

## Where we are
One gate per stage is implemented and honoured, and both approval modes work as documented. The safety argument holds: nothing before CHECK can spend, so nothing before CHECK needs a person.

The record moved to the right place on 260726 and has not arrived. `QA6` retired `STATUS.md` and put the Gate Ledger in each S page's `## Log`, which is the correct home and is currently empty on every live page. In the same move `gate_mode` acquired two declared locations that disagree with each other, and the three fields that define what a gate READS have never been described anywhere a reader of this board would find them.

## Files
- `1-lifecycle/ref/08-stage-gate.md`
  The gate protocol, both modes, and the no-silent-skips rule.
- `stages/*/stage.md`
  `gates:`, `done_criteria`, `closed_when`, `exit_when`.
- `0-lifecycle/0-seed/S-Seed-0-seed.md`
  The MISQ page carrying the agent-approved seed gate.

## Law
A stage closes at exactly one gate, at CHECK, and the human's attention is spent there and nowhere else. The phases before it run unattended only because none of them can spend; that is the whole safety argument, and raising `probe_depth` reopens all three.

CHECK is never implicit. Entering it means presenting the exit-criteria report and the approval ask. Feedback arriving early does not become a gate because somebody responded to it.

An agent may stand in for the human only in the declared `autopilot` mode, in a fresh context, and it may never pass a human-only item: those are marked DEFERRED and accumulate in a human queue. The ledger records the actor. A human may reopen any agent-approved gate, which resets that stage's ledger row.

## Log
260726 · Rewritten from `_archive/QB8-what-is-a-gate.md`, which asked what a gate is and treated the agent stand-in as an unprevented loophole. Reading `ref/08-stage-gate.md` corrected that: the stand-in is a documented mode with real safeguards. The live gap is narrower and worse, that the board's `state:` cannot show which mode passed a gate. The `done_criteria` / `closed_when` / `exit_when` block was added here because it had no owner on the board at all.
260726 · Aligned against `QA6`, which had moved well past this group. The Gate Ledger moved out of `STATUS.md` and into each S page's `## Log`, which is the right home and is empty on every live page; `gate_mode` came out of the same retirement with two declared locations that disagree.
