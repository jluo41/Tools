# Fresh-agent acceptance test
state: ✅ SETTLED
owner: CC
method: start an agent with no memory of this conversation and hand it only SKILL.md

## Opening
How do we prove that a fresh agent can use the board skill from its written instructions alone?

The author can fill documentation gaps from memory and therefore cannot perform this test.
A clean agent reveals every step, convention, or gate that the skill forgot to state.
Material revisions invalidate the previous result because the workflow it proved has changed.
Acceptance means the agent opens a valid board, respects every gate, and leaves no guessed rule unfixed.

**Covered elsewhere**: **What SKILL.md says**: that is `QC1`. This question only judges whether it suffices.


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

No canvas frame is linked here. `board.excalidraw` holds no frame named `QF2`, and JL ruled on 260802 that a page shows no link rather than one that 404s; the link returns when someone draws the frame.

## Aims
- [x] Start an agent with no memory of this conversation; give it only SKILL.md + ref/ and one real topic
      Topic: "set the usage rules for the lab's new GPU cluster".
      Explicitly forbidden from looking at any existing board.
- [x] It opens a board on its own
      5 Qs (QB1 access / QA2 scheduling / QC1 storage / QF2 forbidden / QC1 admin), self-grouped into QA/QB/QC, `build.py` succeeded first try, board.html structure verified (not just its own claim).
- [x] Compare its steps against the design
      Matched: read SKILL.md+ref → draft spine/close/Q list → stopped at the "Q list needs a nod" gate → wrote board.md → wrote each question → build.
      Never touched the forbidden zone (never peeked at an existing board).
- [x] Feed the findings back into SKILL.md
      Verdict YES: SKILL.md + ref/ suffice for a newcomer to open a valid board.
      The single spot that could truly block someone (`build.py` lives in the skill dir, not the board folder, and how to invoke it was unclear) was fixed into SKILL.md (invoke with its path, do not cd in).
      Everything else was "which convention" minutiae (slug format, default state, owner assignment), also written into the open section.
- [x] 🔁 Re-run after the Q/S merge (260725)
      The 260723 verdict was earned against SKILL.md 0.3.0, before Q/S pages, Opening, the structure ops and the live layer existed, so by this question's own rule it had expired.
      A fresh agent was given only SKILL.md + `ref/` (existing boards explicitly out of bounds) and asked to open a board on lab data-retention rules with 4 Q pages in 2 groups **plus one S stage**.
      Verdict **YES**: it built on the first run, 5 pages discovered, the index counted `0/4 questions settled · 0/1 stages gated`, the S page's Stage Record was lifted into Opening, and it stopped at the right gate (it quoted the "Q list needs a nod" sentence and the question it would have asked).
      Four documentation gaps it had to guess through were all fixed the same day, see Where we are.

## States
**Run twice, both YES: 260723 on the Q-only skill, 260725 on the shared Q/S skill. The four gaps the second run had to guess through are closed.**

- 260725 CC · 🔁 Second run passed, and paid for itself in gaps
  The agent produced a valid board and a correct build, so the verdict is YES, but everything it had to invent was about **S pages**, because the skill described them only for the reading side: ① how an S page is listed in `## Pages` (it invented a `### S · …` group, which happened to be right); ② what `state:` an S carries, since `close` said "human-gated / explicitly parked" while the template offered only four pill values; ③ the `open` procedure asked for "有哪几个 Q" and told you to name files `Q<letter><n>`, never mentioning S at all; ④ the Q-consumer `**Probe:**` line pointed at `1-probes/PPNN_topic/…`, which does not exist on a standalone board.
  All four were written into `SKILL.md` / `ref/board-form.md` / `ref/page-template.md` in the same pass (0.16.0).
  It also flagged that `build.py` runs on plain `python3` while `serve.py` needs the venv, now stated in the build section.
- 260725 CC · ✅ The fixes were verified by a second fresh reader, not by us
  A third agent, given only the docs and forbidden to read any board or any source file, was asked the five things the second agent had to guess and told that "NOT DOCUMENTED" was an acceptable answer.
  It answered all five correctly and quoted the sentence behind each one: **ALL DOCUMENTED**.
  This is the cheap half of the acceptance (a read, not a build) and it is what turns "we wrote something" into "the documents now say it".
- Known and deliberate
  `SKILL.md` and `ref/board-form.md` remain largely Chinese while board content is English-only; the reader noted an English-only operator would stall on the operative sections.
  This is JL's 260724 split (board md/html and artifacts are English; internal skill specs may stay bilingual), so it is recorded here rather than "fixed".
- Re-run rule
  Still stands: every material structural change voids the previous verdict.
  The 260725 run is the current one.

## Files
- `SKILL.md` · `ref/`
  The complete material handed to the fresh agent; nothing else may be given.
- `ref/writing-rules.md`
  The zero-background cold-read prompt and convergence criterion live here.

## Law
- The acceptance is "open a board", not "read a board"
  The agent gets SKILL.md + `ref/` and one real topic, is forbidden from opening any existing board, and must reach a successful build on its own.
  Since the Q/S merge the topic must force **both kinds**: a Q-only run cannot detect a gap in the S instructions, which is exactly what happened between 260723 and 260725.
- Every gap the run exposes is fixed before the verdict is recorded
  A YES with unfixed gaps is how a skill rots: the run proved a capable agent can guess past them, not that the documents said it.
  Fix them in the same pass, then log which run is the current one.

## Glossary
fresh agent: a separately started Claude that cannot see this conversation and sees only the files you hand it.

## Discussion

## Log
260726 · opening lead widened to three lines (JL: the openings are too short; say the question, how it is answered, and what turns on it)
260725 1225 · Fixes verified by a third fresh reader (docs only, "NOT DOCUMENTED" allowed): all five previously-guessed points answered with quotes → ALL DOCUMENTED
260725 1210 · Re-ran the acceptance against the shared Q/S skill (JL's go on the QB pass): fresh agent, 4 Q + 1 S on a lab data-retention topic, built first try, gate respected → verdict YES. Its four S-side documentation gaps (Pages listing · S state values · S absent from the open procedure · the probe pointer) were closed in SKILL.md and ref/ in the same pass; the deliberate Chinese-spec exception recorded; ## Law written
260724 1242 · Translated to English (JL 260724: everything on the board in English); Where-we-are updated: the old "never ran" line predated the 260723 run
260723 · Rewritten to the new structure: Question expanded into "one paragraph + bullets", added `## Boundary` and `## Files`; the retired `## Why here` merged into Question
260723 1720 · Fresh-agent acceptance ran (GPU-cluster topic): success first try, workflow matched, verdict YES;
              the single real gap (how to invoke build.py) fixed into SKILL.md → ✅ SETTLED
260723 0919 · Renumbered Q5 → QF2
260723 0915 · The readability acceptance moved to QA5; this question keeps only "can a board be opened from SKILL.md alone"
260722 2255 · Opened, per the repo CLAUDE.md rule "a changed skill must be validated by a fresh agent"
