② Reason ideas · `run-reason-t00`
=================================

The first step of a Job's work, in `t00_reason-ideas/`, by the designer agent. It turns the fence into a set of
ideas, each with the chain of reasoning that led to it, so a reader can see why each design exists before any
design is written. It writes ideas only; the Job's `run-open-designs-jNN` opens one design Task per idea after the
reviewer has checked the fence (that Run's first pass, `fence-check.md`).


What it reads
-------------

- the Job's face: `n`, N (how many designs the Job keeps; copied from the goal's line in `board.md`).
- `inputs/goal.md`: the aim, who it is for, the same N.
- `inputs/method.md`: the pinned version's ② choice (how far to spread, distinct in principle or variations of one,
  and how many ideas) and its ① parts.

**How many ideas.** ② makes N + 5 ideas unless the method version's ② names another count; this is the one place
the rule is stated (the method registry's README points here). Every idea becomes a design Task; t99 keeps N.
- the other files of `inputs/` the manifest lists, and nothing else.


What it writes
--------------

```text
runs/run-reason-t00/result/
├── chains.yaml     the topics and their reasoning chains
├── ideas.yaml      one row per idea, N + 5 (or the method's count)
└── topics.md       the readable report, written from chains.yaml
```

```yaml
# chains.yaml
topics:
- id: T1
  title: <what this line of reasoning is about>
  from: <a manifest file, its name or an id in it, with a locator; or: own knowledge>
  steps:
  - says: <what the source says>
    so: <what it means for the design>
  - says: <what a second source says>
    so: <what it adds>
    from: <its own source, overriding the topic's for this step>
  ideas: [I01, I02]
```

```yaml
# ideas.yaml
ideas:
- id: I01
  idea: <one sentence: what this design tries>
  topic: T1
  design: d01          # the design Task it becomes: t01_d01_<name>/
  name: <short-name>   # lowercase words joined by '-': the Task's slug, kept through every revise
```


Rules
-----

1. **Every topic names its `from`, and a step may name its own.** A file in the manifest (`handoff-W-03.md · row 2`,
   `W-03 row 2`, `rule r2.1`) or exactly `own knowledge`; a step's own `from` overrides its topic's for that step. A
   step that rests on no source says `own knowledge`; it is never given a borrowed one.
2. **N + 5, distinct.** As many ideas as the method asks (N + 5 unless its ② says otherwise), each trying something
   the others do not; two ideas that differ only in wording are one idea.
3. **Every idea has its topic, its design and its `name`.** `design` numbers the Tasks in idea order (`I04` → `d04`); `name`
   is born here and never changes.
4. **No design text.** An idea is what a design tries, not its words; ③ writes the words.
5. **Writes only `result/`.** The Task face's `state` and the design Tasks belong to the caller.

Check: `python3 scripts/check_unit.py --ladder-result <Job>/t00_reason-ideas/runs/run-reason-t00`.
