# Fresh-agent acceptance test
state: 🟡 PARTIAL · both runs said YES and both are voided; the page contract left SKILL.md and nobody has re-run since
owner: CC
method: start an agent with no memory of this conversation and hand it only the shipped material: haipipe-board's SKILL.md and ref/, plus haipipe-board-page

## Opening
How do we prove that a fresh agent can use the board skill from its written instructions alone?

The author can fill documentation gaps from memory and therefore cannot perform this test.
A clean agent reveals every step, convention, or gate that the skill forgot to state.
Material revisions invalidate the previous result because the workflow it proved has changed.
Acceptance means the agent opens a valid board, respects every gate, and leaves no guessed rule unfixed.

**Covered elsewhere**: **What SKILL.md must say**, and where it draws the cut to `ref/`: that is `QC1a`. This question only judges whether it suffices.


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

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/board.excalidraw&frame=QF2

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
- [ ] 🔁 Re-run after the page contract left SKILL.md (260806)
      The 260725 verdict was earned against `haipipe-board` 0.16.0, when one skill held the whole grammar.
      Today that door is 0.124.0 and the page contract is a separate skill, `haipipe-board-page` 0.21.0, carrying Page = Type x Phase with ten Page Types under `board/page-types/`, four Page Phases under `board/page-phases/`, and the verbs CREATE, WORK ON and RUN.
      That is a material structural change, so by this page's own re-run rule the verdict is void and no run is current.
      The handover grew with it: SKILL.md now tells a creator to load `haipipe-board-page` rather than restating the page grammar, so the next run hands over SKILL.md, `ref/` AND that skill, and nothing else.
      The topic must still force a Q page and an S page, since the two kinds are the reason the 260725 run found anything.

## States
**Run twice, both YES: 260723 on the Q-only skill, 260725 on the shared Q/S skill. Neither verdict is current, because the page contract left SKILL.md after both of them.**

- 260806 CC · ⌛ The verdict expired, and this page is the only thing that says so
  On the day of the second run the whole grammar lived in one skill at 0.16.0; that door is now 0.124.0, and the page contract has moved out of it entirely.
  `haipipe-board-page` 0.21.0 owns Page = Type x Phase, with ten Page Types under `board/page-types/` and four Page Phases under `board/page-phases/`, plus the verbs CREATE, WORK ON and RUN.
  That is the largest material change either run has seen, so the re-run rule voids the 260725 verdict and the state drops to 🟡 until a third run.
  It also changes what "the complete material" means: an agent handed only SKILL.md and `ref/` would stall at the line telling it to load `haipipe-board-page`, so the next handover includes that skill.
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
  No run is current: the 260725 one was voided when the page contract became its own skill.

## Files
- `SKILL.md` · `ref/`
  The board door's own material, and the part of the handover that has not changed since 260723.
- `../haipipe-board-page/SKILL.md`
  The rest of the handover since 260806: the page contract SKILL.md points a creator at instead of restating.
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
260806 2203 · [REVISE-CC] swept to the 260806 architecture; the 260725 verdict is expired, not current: the page contract left SKILL.md and is now `haipipe-board-page` 0.21.0 (ten Page Types, four Page Phases, CREATE/WORK ON/RUN) against a 0.16.0 door, so state went ✅ to 🟡 with a re-run Aim opened and the handover widened to include that skill. Also: `QC1` repointed to `QC1a` (QC1 is the skill-family page; QC1a is "What SKILL.md must say" and already points back here), and the "no frame named QF2" note replaced with the real canvas link because `board.excalidraw` now carries a `QF2` frame holding this page's title and diagram
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
