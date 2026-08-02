# The order, and whether a step may be skipped

state: 🟡 PARTIAL
owner: JL
method: fix the order first, then say which phase owns the steps and which steps a correct run legitimately never reaches

## Opening
Five steps run in one order; what does the order buy, and which of them may a correct run skip?
② before ③ is the whole ruling, because it makes an existing answer free and a new one the only thing that costs.
Three of the five are skippable and one of them is skipped on most questions, which is the ladder working rather than a shortcut.

The order carries the ruling, not the list.
Any arrangement that dispatched before matching would work correctly and waste an agent on every question the bank has already answered, which in a healthy project is most of them.
The phase assignment was also wrong once and got fixed: steps ① and ② used to run at DRAFT so that one human gate could review draft and probe plan together, and when stages moved to `gates: [check]` that reason evaporated and the steps went back to PROBE.

**Covered elsewhere**: Each step has its own page: `QB2` through `QB6`, in order. What a paper's stage does with all of this is `QB9@paper`.

## Diagram
```
   DRAFT                      PROBE
   ─────                      ─────
   raises Q-consumers   ──▶   ① ORGANIZE   QB2
   (stake attached)           ② MATCH      QB3
   and stops                  ─── human APPROVE gate ───
                              ③ DISPATCH   QB4
                              ④ POINT      QB5
                              ⑤ INTERPRET  QB6

   ② BEFORE ③ is the ruling: reuse first, spend last.

   ── which steps a CORRECT run may never reach ────────────────────
   T0 JOIN          ① only, then stop     another entry already asks it
   T1 LOCAL         ①②, then ⑤            answered-local: no dispatch
   T2 REUSE         ①②, then ④⑤           the answer already exists
   deferred         ①②, then STOP         above the ceiling, declared
   T3/T4            all five

   so ③ is the EXCEPTION, not the spine. a run where every entry
   reaches ③ is the smell the collector agent is told to report.
```

## Content
### 1 · The phase boundary, and the one sentence that names a violation
DRAFT writes the stage's prose and the Q-consumer questions it cannot answer, and stops there.
It authors no entry, chooses no route, judges no bank, and never opens `1-probes/`.
A DRAFT that writes a `### q-executor` is doing PROBE's job, which is the cleanest violation statement the layer has and is checked by nothing.

### 2 · The gate sits between planning and spending, not between raising and planning
The human APPROVE gate is after ② and before ③, which is the only place it can be: everything before it is free and everything after it costs.
That is also why the ①② move back to PROBE was safe rather than a regression.
The gate reviews a plan that is complete, with every entry's route, bank verdict and target already decided, so approving is a decision about spend rather than about wording.

## Aims
- [x] 🔢 Five steps, fixed order, ② before ③
- [x] 🏗 All five belong to PROBE; DRAFT raises questions and stops
- [x] 🚪 A human APPROVE gate sits between planning and spending
- [x] ⏭ Which steps a correct run may skip is stated rather than inferred
      T0 stops at ①, T1 and T2 never reach ③, and a declared deferral stops after ②.
- [ ] 🔧 `SKILL.md` stops instructing DRAFT to do what it forbids DRAFT to do
      Line 81 says DRAFT "authors no probe entry, chooses no route, judges no bank, and never opens `1-probes/`", and line 83 names writing a `### q-executor` as PROBE's job.
      Line 249, inside the file's own DRAFT phase checklist, then instructs DRAFT to author the entry, write the `### q-executor`, judge `bank` and set `target`.
      Found by the `QD2` fresh-agent run on its first read, 260726, and verified at the source; it broke the tie by consulting the paper worker, which a reader without that instinct would not do.
- [ ] 🧪 A DRAFT that writes a q-executor is detected
      The rule is stated and nothing checks it, so the old behaviour would pass unnoticed.
      A grep for `### q-executor` in a stage doc's own commit range would close it crudely.

## States
Ruled and running. The order is the part that matters and it is stated as such.

The phase boundary is stated twice in the same file and the two statements disagree: the warning box at line 81 forbids what the DRAFT checklist at line 249 instructs.
A cold reader hit it on first pass and resolved it by going outside the constitution to the paper worker, which is not a resolution the file offers.
It is also unenforced: a DRAFT worker that planned probes would produce a valid-looking file, and the only reason it does not happen is that the workers were rewritten.
What the split into per-step pages added on 260726 is the skip map, which had been implicit in the ladder and never written as a property of the loop.

## Files
- `SKILL.md`
  The loop, the phase map, and the DRAFT/PROBE split.
