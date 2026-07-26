# ③④ Two adapters, and one forked checker

state: 🟡 PARTIAL
owner: JL
method: measure the fork, separate the differences that are real from the ones that are drift, then rule who owns it

## Question
Two consumer families each carry their own probe skill; what is legitimately different between them, and what has merely drifted apart?
The two skills are thin and honest, and the two checkers inside them are 1096 lines against 679 with a 600 line diff.
Some of that gap is a paper having a manuscript and an application not having one, and some of it is nobody having decided.

The fork is where the layer's enforcement actually lives, which is what makes it worth a page.
A rule agreed on this board and written into the shared model binds nothing until it reaches a checker, and there are two checkers, held in step by a comment asking the reader to keep them in step.
So the question is not whether forking was wrong, it is who owns the reconciliation now that the two have moved.

## Boundary
- ✅ Covered here
  What each adapter is, what each declares as its own delta, the measured size of the fork, and which differences are defensible.
- ↪ Covered elsewhere
  What the checker fails on, and the failures it currently reports on real data, is `QC2`.
  The shared model both adapters defer to is `QA2`; the vocabulary propagation rule is `QD1`.

## Diagram
```
   ③ paper/2-phase/1-probe/haipipe-paper-probe/          v0.6.1
       SKILL.md                219    ref/per-stage-dispatch.md
       check-probe-cards.sh   1096    feedback/
   ④ application/2-phase/1-probe/haipipe-application-probe/  v0.3.2
       SKILL.md                174    ref/per-stage-dispatch.md
       check-probe-cards.sh    679    ref/harvest-acceptance.md

   both open with the SAME disclaimer, near-verbatim:
     "⭐ THE MODEL IS NOT THIS FILE'S — it is owned by
      ../../../../probe/haipipe-probe/SKILL.md"

   ── the declared deltas ──────────────────────────────────────────
   ③ paper_root · the paper's own registries (T1) · the RESOURCE
     stage intake and write-back (paper only) · HARVEST inline with
     value / citation / display lanes · _LOG_<stage>.md as the one
     kept sidecar
   ④ intervention_root · the DIKW ladder rungs raise the questions
     (no resource stage) · harvest folds into ### a-executor, no
     sidecar docs and no lanes

   ── the fork, measured 260726 ────────────────────────────────────
             ③ 1096 lines          ④ 679 lines        600 diff lines
             34 FAIL codes         31 FAIL codes      SKILL.md says 11
   PASS 1    every probe file      same
   PASS 2    sidecar ledgers       REMOVED 260718     ← a real difference
   PASS 3    the QA files          same
   PASS 4    manuscript place-     absent             ← a real difference
             holder ownership
   RESOURCE  paper-only pass       absent             ← a real difference
   the 3 ③ has and ④ does not:
     concern-with-route · concern-not-discussed   ← plausibly paper-only
     deferred-undeclared                          ← NOT paper-shaped: the
       model states the deferral rule generally, so an application
       deferral with no depth-and-cost line passes today

   the mechanism holding them together, in ③'s own header:
     "Keep the two in step; the paper copy is the source."
```

## Content
### 1 · The skills are thin, and that part works
#### Both adapters disclaim the model in the same sentence, then list only their deltas
(219 and 174 lines, most of which is how-to rather than rules)
Neither file restates the anatomy, the ladder, the laws or the states, and both say explicitly that the shared model wins on conflict.
That is the arrangement working: a rule changed in `①` does not need either of these files edited, because neither one copied it.
The deltas each declares are genuinely family-shaped, not preference: a paper has a resource stage and a manuscript, an application has DIKW rungs and no manuscript.

### 2 · The checkers are not thin, and that is where it breaks
#### The enforcement forked and the model did not
(`③` holds 1096 lines of rules that `①` does not know about)
Every FAIL condition the shared model documents lives in both copies, and both copies have grown conditions the model never mentions.
So the layer has two answers to "what does the contract enforce", and the shared file that claims to be the vocabulary source is not one of them.
`QC2` measured it exactly: 34 codes in `③`, 31 in `④`, and 11 in the model.

#### Three of the four differences are defensible on their face
(a manuscript pass cannot apply to a family with no manuscript)
PASS 4 scans stage docs for `\cite{TOADD}` and `{VAL:? …}` placeholders and requires each to name the question that will settle it, which is meaningless for an application.
PASS 2 was removed from `④` on 260718 by a no-sidecar ruling, so its absence is a decision rather than a lag.
The RESOURCE pass is tied to a stage only the paper family has.

#### Exactly three codes exist in `③` and not in `④`, and one of them is a hole
(`concern-with-route`, `concern-not-discussed`, and `deferred-undeclared`)
The two `concern` codes guard a terminal state recording a construct-validity threat, a design limitation, or any question no task or discovery can settle.
It never fails the gate, it is reported every run, and under `--final` it must be shown discussed in the prose; whether that is paper-shaped is a ruling, since an application has design limitations too.
`deferred-undeclared` is not a ruling.
The model states the deferral rule for the whole layer, `③` enforces it, and `④` does not, so an application entry can sit `deferred` with no depth-and-cost line and pass a gate that would red the same entry in a paper.
That is one fork out of compliance with the constitution, and it was 5 of the 12 failures the paper fork found on real data.

### 3 · What holding them in step actually costs
The paper copy declares itself the source and the application copy repeats the request in its own header.
Reconciliation therefore happens when somebody remembers, reads 1775 lines across two files, and decides per hunk whether a difference is a family delta or a missed port.
No diff runs, no test compares them, and the shared `test/` fixture drives one of the two without saying which, which is `QA2`'s open item and this page's problem too.

## Items to Finish
- [x] 📏 Both adapters are inventoried, with the deltas each declares
      Line counts, versions, ref files and the declared family differences, measured 260726.
- [x] 🍴 The fork is measured rather than described
      1096 against 679, 600 diff lines, four structural differences named.
- [ ] 🧠 JL rules one file with family flags, or two files with a named owner
      Today it is two files, an informal owner, and a request in a comment.
      This closes with a ruling either way, because both are workable and the current state is neither.
- [ ] 🔍 A difference between the two forks is detected rather than noticed
      Nothing compares them, so a rule ported to one and not the other looks exactly like a family delta.
      This closes when a diff runs, even a crude one that lists condition names present in one copy and not the other.
- [ ] 🧠 JL rules whether `concern` is paper-only
      An application can carry a doubt the bank cannot close just as a paper can, so its absence from `④` reads as a missed port rather than a delta.
      This closes when the state is either ported or ruled paper-shaped for a stated reason.
- [ ] 🕳 `deferred-undeclared` is ported to `④`
      Not a ruling: the model states the deferral rule for the layer and only one fork enforces it, so `④` is simply out of compliance.
      This closes when an application deferral with no depth-and-cost line fails the way a paper's does.
- [ ] 📋 The conditions each fork enforces are listed where the model can see them
      `①` documents eleven and the forks enforce more, so the constitution under-reports its own contract.
      This overlaps `QC2` and closes with it.

## Where we are
The two skills are in good shape and the two checkers are not.

The skills are thin, disclaim the model, and list only family deltas, which is exactly what an adapter should be.
The checkers hold every line of enforcement the layer has, in two copies, 600 diff lines apart, reconciled by a sentence asking the reader to reconcile them.
Counting the emitted codes rather than eyeballing the diff narrowed the question usefully: exactly three codes exist in `③` and not in `④`.
Two are the `concern` pair, which may be a genuine family delta and is written up as a ruling.
The third, `deferred-undeclared`, is not a delta at all: the model states that rule for the whole layer, so `④` is out of compliance with the constitution and the fix needs no ruling.

## Files
- `haipipe-probe/`
  The shared model both adapters defer to, and the folder where a ported condition should be documented.
- `SKILL.md`
  The eleven FAIL conditions the model claims, against which both forks over-deliver.
