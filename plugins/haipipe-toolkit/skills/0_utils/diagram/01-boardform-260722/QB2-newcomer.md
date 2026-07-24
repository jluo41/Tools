# Fresh-agent acceptance test
state: ✅ SETTLED
owner: CC
method: start an agent with no memory of this conversation and hand it only SKILL.md

## Question
How do we prove this skill is **usable** — and not usable only by the person who wrote it?

- Why it is hard
  The author's head holds a pile of things that never made it into SKILL.md; self-testing in the same conversation can never reveal what is missing.
- What breaks if we leave it
  The repo's `CLAUDE.md` hard-codes the rule: any skill change must be validated by a fresh agent before it counts as done. Unvalidated equals unfinished.
- What it affects downstream
  It is the only acceptance gate that can be **re-run** — every structural change (like the 260723 redesign) voids the previous acceptance and forces a re-run.

## Boundary
- ✅ This question owns
  **How acceptance is run**: what the fresh agent is given, what it must do, what counts as passing, how often to re-run.
- ❌ This question does not own
  **What SKILL.md says** — that is `QB1`. This question only judges whether it suffices.

## Diagram
```
┌ me, in this conversation ┐  a head full of things not in SKILL.md
└──────────────────────────┘  → self-testing reveals nothing     ✗

┌ fresh agent ┐  given only SKILL.md + one real topic
└──────┬──────┘
       ▼
   it opens a board on its own
       │
   compare: did its steps match the design?
       ├─ match     → pass
       └─ mismatch  → fix SKILL.md, run again  ⟲
```

## Items to Finish
- [x] Start an agent with no memory of this conversation; give it only SKILL.md + ref/ and one real topic
      Topic: "set the usage rules for the lab's new GPU cluster". Explicitly forbidden from looking at any existing board.
- [x] It opens a board on its own
      5 Qs (QA1 access / QA2 scheduling / QB1 storage / QB2 forbidden / QC1 admin),
      self-grouped into QA/QB/QC, `build.py` succeeded first try, board.html structure verified (not just its own claim).
- [x] Compare its steps against the design
      Matched: read SKILL.md+ref → draft spine/close/Q list → stopped at the "Q list needs a nod" gate →
      wrote board.md → wrote each question → build. Never touched the forbidden zone (never peeked at an existing board).
- [x] Feed the findings back into SKILL.md
      Verdict YES: SKILL.md + ref/ suffice for a newcomer to open a valid board. The single spot that could truly block someone
      — `build.py` lives in the skill dir, not the board folder, and how to invoke it was unclear — fixed into SKILL.md (invoke with its path, do not cd in).
      Everything else was "which convention" minutiae (slug format, default state, owner assignment), also written into the open section.

## Where we are
Ran once (260723, GPU-cluster topic), verdict YES; the single real gap is fixed into SKILL.md. Re-run whenever the structure changes materially.

## Files
- `SKILL.md` · `ref/`
  The complete material handed to the fresh agent — nothing else may be given.
- `ref/writing-rules.md`
  The zero-background cold-read prompt and convergence criterion live here.

## Glossary
fresh agent: a separately started Claude that cannot see this conversation and sees only the files you hand it.

## Discussion

## Log
260724 1242 · Translated to English (JL 260724: everything on the board in English); Where-we-are updated — the old "never ran" line predated the 260723 run
260723 · Rewritten to the new structure: Question expanded into "one paragraph + bullets", added `## Boundary` and `## Files`; the retired `## Why here` merged into Question
260723 1720 · Fresh-agent acceptance ran (GPU-cluster topic): success first try, workflow matched, verdict YES;
              the single real gap (how to invoke build.py) fixed into SKILL.md → ✅ SETTLED
260723 0919 · Renumbered Q5 → QB2
260723 0915 · The readability acceptance moved to QA5; this question keeps only "can a board be opened from SKILL.md alone"
260722 2255 · Opened, per the repo CLAUDE.md rule "a changed skill must be validated by a fresh agent"
