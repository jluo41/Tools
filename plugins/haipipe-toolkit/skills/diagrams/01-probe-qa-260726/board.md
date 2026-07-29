# /haipipe-probe: pinning down the wall between a question and its answer

spine: A probe carries one question a consumer cannot answer out to a bank that must never learn it was asked, and carries the answer back. Pin down what crosses that wall, what may not, what each side owes the other, and what a machine can check, so the layer can be run against real project data by someone who was not here.
close: Every Q reaches ✅ or ⏸️, with the decision on its own page, and `SKILL.md` says what those pages say. A fresh agent reads only `SKILL.md` and runs one probe end to end without breaking either LAW, and `check-probe-cards.sh` passes on a real consumer.

## Topic
`/haipipe-probe` is the layer between a consumer that has a question and an executor that can answer it.
A paper or an application may not run code and may not read the literature; the task and discovery layers do both and know nothing about papers.
The probe is the only thing that touches both sides, and it is COMMUNICATION rather than judgment: it carries a question out and an answer back, and decides nothing about what either means.

What makes the design hard is that the wall is not a boundary of politeness, it is the thing that makes answers reusable.
The consumer's question carries a STAKE, "does WellDoc have a cycle column, because my claim C6 dies if it does".
Let that stake cross and the executor shapes its answer around the hypothesis, and the answer is worth nothing to the next consumer who asks the same thing for a different reason.
So the probe rewrites the question with the stake stripped out, and that rewrite is its core act.

Cast: JL decides. CC is Claude Code, doing the work.
This board covers the LAYER. What a paper may ask and what it may spend is the paper board's `QB9@paper`, and the two must not drift.

Words this board leans on. A CONSUMER is a paper or an application. The BANK is the task and discovery layers, which are probe-UNAWARE: nothing under `tasks/` or `discoveries/` names a probe. A Q-CONSUMER is the question as the consumer asks it, stake attached, living in a stage doc. A Q-EXECUTOR is the same question in general language with the stake removed, and it is the only thing that crosses. A QA FILE is the answer the executor wrote for its own reasons. PROBE is the phase that runs all five steps.

## Pipeline
```
QA · the FOLDERS, one page each
   QA1 the map ── six that ship, three shapes that hold, and what has NO page here
        │
        │  what SHIPS                        where the DATA is
        ├─ QA2 ① haipipe-probe/    the       ├─ QA6 ⑦ the consumer   the STAKE
        │      shared model, defines all     │      lives here. LAW 1
        ├─ QA3 ② agents/    one agent,       ├─ QA7 ⑧ the wall   one q-executor
        │      its clean context IS          │      = one file = one path
        │      the wall                      └─ QA8 ⑨ the bank   stated as an
        ├─ QA4 ③④ the two adapters                  ABSENCE, so it is checkable
        │      where ALL enforcing code is,
        │      forked 1096 vs 679
        └─ QA5 ⑤⑥ the two records
               this board, and the .txt spec that outranks it

QB · the VERBS, one page each
   QB1 the ORDER ── ② before ③, and which steps a correct run skips
        │
        ├─ QB2 ① ORGANIZE   what must the strip refuse to carry?
        ├─ QB3 ② MATCH      what counts as a hit, and what may it spend?
        ├─ QB4 ③ DISPATCH   what crosses the wall?
        ├─ QB5 ④ POINT      what makes a target honest?
        └─ QB6 ⑤ INTERPRET  where does the answer come to rest?

   QB7 what is NOT a probe ── the test that sends a question elsewhere

QC · the CONTRACT, the part a machine holds
   QC1 the QA state line ──► QC2 what the checker FAILS on ──► QC3 derived state

QD · shipping the layer
   QD1 one vocabulary source ──► QD2 a fresh agent runs one probe
```
Four groups, and QA and QB were both rebuilt on 260726 by the same move: one page per
THING, rather than a few pages each straddling several. QA is a folder tour, which turns
every rule into what is in here and what may not be. QB is a verb tour, which gave ③ and
④ their first pages: ④ POINT alone owns five of the checker's codes and 7 of the 12
failures found on real data, and had been a line inside a combined loop page.
QC is separate from QA and QB because it is the enforceable half, and a law nothing
checks is a preference. QD is whether any of it survives leaving this room.

## Pages
### QA · The folders, one page each
Six folders ship this layer and three file shapes hold it, and every rule the board
makes is a rule about what one of them may and may not contain. QA1 counts them; the
seven pages after it take one each, in the order QA1 numbers them. Stating a rule as
a property of a folder is what makes it checkable by looking.
QA1-the-map.md
QA2-shared-model.md
QA3-the-agent.md
QA4-two-adapters.md
QA5-two-records.md
QA6-consumer-side.md
QA7-the-wall.md
QA8-the-bank.md
### QB · The verbs, one page each
Five steps in a fixed order, and the order is the ruling: ② before ③ makes an existing
answer free and a new one the only thing that costs. QB1 holds the order and the skip
map; QB2 through QB6 take one step each, in sequence; QB7 holds the test that decides
whether a question belongs in this loop at all.
QB1-the-order.md
QB2-organize.md
QB3-match.md
QB4-dispatch.md
QB5-point.md
QB6-interpret.md
QB7-not-a-probe.md
### QC · The contract
The part a machine can hold us to. One mutable field on the answer, eleven FAIL
conditions, and a state read off disk rather than believed.
QC1-qa-state-line.md
QC2-checker-fails.md
QC3-derived-state.md
### QD · Shipping the layer
Whether someone who was not here can run it. Last, because it tests everything above.
QD1-one-vocabulary-source.md
QD2-fresh-agent.md

## Links
SKILL.md            ../../probe/haipipe-probe/SKILL.md
CHANGELOG.md        ../../probe/haipipe-probe/CHANGELOG.md
ref/probe-template.md ../../probe/haipipe-probe/ref/probe-template.md
haipipe-probe/      ../../probe/haipipe-probe/
agents/             ../../probe/agents/
test/               ../../probe/haipipe-probe/test/
haipipe-task/       ../../task/haipipe-task/
haipipe-discovery/  ../../discovery/haipipe-discovery/
paper-board/        ../01-haipipe-paper-260725/
boardform-board/    ../01-boardform-260722/
QA1@paper           ../01-haipipe-paper-260725/QA-where-things-live/QA1-eight-folders.md
QA5@paper           ../01-haipipe-paper-260725/QA-where-things-live/QA5-the-probe-layer.md
QB9@paper           ../01-haipipe-paper-260725/QB-a-stage-a-page-and-a-flow/QB3b-probe.md
QC1@paper           ../01-haipipe-paper-260725/QC-the-sentence-with-evidence-card/QC1-sentence-citation.md
