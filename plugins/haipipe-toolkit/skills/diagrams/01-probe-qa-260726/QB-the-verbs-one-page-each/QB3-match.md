# ② MATCH · what counts as a hit, and what may it spend?

state: 🟡 PARTIAL
owner: JL
method: five rungs cheapest first, a hit that requires reading the answer, and a read-only eye on the bank

## Opening
Before anything is dispatched, how hard should the layer look for an answer that already exists, and what counts as finding one?
Five rungs, cheapest first, where only the top two summon an agent and a hit counts only if the file LITERALLY answers the question.
The reading rule is the load-bearing half: without it, reuse becomes a way to mark anything answered by finding a file on roughly the right subject.

This step is also where LAW 1's one permission lives.
Rooting a question against the bank means reading the bank, so a read-only grep of `{tasks,discoveries}/**/QA/*.md` is legal and required, while writing anything there is not.
The law bans the pen and the run, not the eye, and this step is the reason the distinction had to be drawn at all.

**Covered elsewhere**: LAW 1 itself is `QA6`; what a paper is allowed to spend, its `probe_depth` ceiling, is `QB9@paper`. The ceiling gate that consumes this step's verdict is `QB4`; what makes the target honest is `QB5`.

## Diagram
```
   ── the COST ladder, in SKILL.md ─────────────────────────────────
   T0 JOIN    another q-executor already asks this   → a bullet    ~0
   T1 LOCAL   my own registries answer it            → answered-local
   T2 REUSE   an existing QA file answers it         → point   1 grep + 1 read
   T3 ENRICH  the folder exists, never asked this    → ③        agent
   T4 FRESH   no task-folder at all                  → ③        agent

   ── the DEPTH ladder, in the paper adapter's ceiling gate ────────
   bank: reuse  = depth 0    results already answer it     free
   bank: run    = depth 1    old script, new config        costs
   bank: code   = depth 2    must write new code first     costs
   bank: new    = depth 3    open a new task-folder        costs most

   ⚠️ TWO LADDERS, FIVE RUNGS AGAINST FOUR DEPTHS, NO STATED MAP.
      reuse=T2 and new=T4 are clear. T0 and T1 have no depth at all.
      T3 ENRICH covers BOTH `run` and `code`, which are depth 1 and 2.
      the ceiling compares depth(bank) <= probe_depth, so the DEPTH
      ladder is the one that binds and the COST ladder is the one
      that is documented.

   MATCH ON THE ANSWER, NEVER ON THE TOPIC — read the file.
```

## Content
### 1 · A hit requires opening the file
The rule that stops the ladder being gamed is that the QA file must literally answer the question.
Topic similarity is not evidence, so `ls` and a filename are never enough.
Without it, T2 becomes a confident wrong answer instead of a bill, which is worse than paying for T4.

### 2 · Two ladders, and only one of them is enforced
#### The documented ladder and the binding ladder are not the same ladder
(five rungs in `SKILL.md`, four depths in the adapter's gate)
The cost ladder T0 to T4 is what the constitution teaches and what a reader learns.
The ceiling gate that actually decides whether an entry is dispatched or deferred compares `depth(bank)` against `probe_depth`, over the four `bank` values.
Nothing states the mapping between them, and it is not one-to-one: T0 and T1 have no depth, and T3 ENRICH spans both `run` and `code`, which sit at different depths and therefore pass different ceilings.

#### The measured distribution was counted on the binding ladder, not the taught one
(reuse 4, run 1, code 7, new 3, across 15 entries with a verdict)
So the finding that "T2 did not dominate" is really that `reuse` did not dominate, and `code` did, at 46 percent.
That is still the contradiction it looked like, because `reuse` is T2 by both ladders.
But the two rungs the constitution names as the cheap majority, T0 and T1, are not counted at all by this measurement, and T0 was separately measured to be firing on 6 of 17 entries.

## Aims
- [x] 🪜 Five rungs, cheapest first, agent only at T3 and T4
- [x] 📖 A hit requires reading the file, not matching the topic
- [x] 👁 The read-only grep is named as legal and required, so LAW 1 does not forbid this step
- [x] 📊 The distribution has been measured on a real project
      MISQ paper, 260726, 15 entries carrying a bank verdict: reuse 4 (26%), run 1 (6%), code 7 (46%), new 3 (20%).
- [ ] 🪜 The two ladders are reconciled, or the map between them is stated
      `SKILL.md` teaches five rungs and the ceiling gate binds on four depths, with no stated correspondence and no home for T0 or T1.
      This closes when one page carries both and says which rung is which depth.
- [ ] 🧠 JL rules what it means that reuse did not dominate
      `SKILL.md` says most entries should land on T2 and on the only real consumer most land on `code`.
      Either the expectation is wrong, or this paper asked an unusually code-heavy set of questions, or the bank is not filling on its own the way the ladder assumes.
- [ ] 🧠 JL rules what happens when the ladder and the ceiling disagree
      An entry can be a legitimate T4 while the run's `probe_depth` forbids it; today that lands as `deferred`.
      This closes when the interaction is stated on one page rather than inferred from two.

## States
Ruled, followed, and measured once.

The rungs are stated with their costs and the anti-gaming rule is explicit, which is the part that matters most.
Splitting this step onto its own page surfaced something the combined loop page had hidden: there are two ladders, the documented one has five rungs and the enforced one has four depths, and nothing maps them onto each other.

- 260726 CC · 📊 Reuse did not dominate, on the only data there is
  Counted across the MISQ paper's 15 entries with a bank verdict: `code` 7, `reuse` 4, `new` 3, `run` 1.
  `SKILL.md` states that most entries should land on T2 REUSE because a healthy bank fills on its own; here reuse is 26 percent and code is 46 percent.
  One paper is not a sample, and it is the only real consumer that exists, so the expectation should not be restated as fact until a second one is counted.

## Files
- `SKILL.md`
  The cost ladder and the match-on-the-answer rule.
- `haipipe-paper-probe/`
  The ceiling gate, where the depth ladder lives and where the comparison is actually made.
