---
status: open
created: 2026-06-22
context: haipipe-paper-structure-pitch (/haipipe-paper pitch); artifact = Paper-Personality-Opioid-MedJournal/0-lifecycle/1-pitch/1-pitch.tex
fixed_in: ""
---
我觉得这个pitch 不好，你也加到feedback上去吧。不知道是哪个skill跟这个相关的。

就是说，你得有hook，有supersie 有implication，然后有什么证据支持，诸如此类的，你可以看看我们pitch相关的skill是怎么写的。这个pitch写的不行。

Diagnosis (after reading the skill):
- Related skill = haipipe-paper-structure-pitch (/haipipe-paper pitch).
- The skill ALREADY defines exactly the structure the reporter wants (SKILL.md lines 82-103 template): Hook / Surprise / So What (= implication) / Why Believe (= evidence support) / Still Fragile / Next Evidence Move.
- But the produced 1-pitch.tex only has \section*{One-Minute Story} + \section*{Current Fragility} -- it is freeform prose missing Hook / Surprise / So What / Why Believe entirely. The author did not apply the skill's own template.

Root cause = the skill has no QUALITY GATE. The template only fires in "Step 2: ensure files exist (create missing with templates)". Nothing forces an authored or revised pitch to actually contain hook + surprise + implication + supporting-evidence before it is considered done. So a pitch can be written as a blurb and pass.

Secondary skill issues found while reading it:
- Naming drift: Principles (line 47) and PITCH_LOG template (lines 116, 123) still say PAPER_PITCH.md, but the real file is 1-pitch.tex.
- Two different section-label lists inside the skill: the intro list (lines 20-28: "What is this paper about / Why care / What is surprising / So what / Why believe / Still fragile / How did it get here") vs the actual template (lines 83-102: One-Minute Pitch / Hook / Surprise / So What / Why Believe / Still Fragile / Next Evidence Move). Pick one canonical rubric.

Suggested fix direction (for the later revision pass, not now):
- Add a pitch DONE-rubric / gate: a pitch is not complete unless it contains, as labeled parts, Hook + Surprise + So-What(implication) + Why-Believe(evidence) (+ Still-Fragile). Make the skill check an existing/revised pitch against this rubric, not only when scaffolding a missing file.
- Unify the two rubrics and fix the PAPER_PITCH.md -> 1-pitch.tex naming.

Fix:
