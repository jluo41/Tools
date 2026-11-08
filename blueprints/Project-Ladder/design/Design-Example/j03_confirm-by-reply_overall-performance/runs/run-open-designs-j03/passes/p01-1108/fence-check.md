Fence check · t00 reason ideas of j03
=====================================

by: reviewer agent (context R), a reviewer context that generated nothing in this Job (t00's by is the designer agent, maker context A)
read: t00_reason-ideas/runs/run-reason-t00/result/chains.yaml against inputs/manifest.yaml (inputs i2, frozen 261108, method M02 m1)
checker: `python3 scripts/check_unit.py --ladder-result <Job>/t00_reason-ideas/runs/run-reason-t00` printed `PASS: ladder Result shape, fence and independence` (exit 0). The checker matches only a from's first word, so each locator below was read against the file by hand.
fence: goal.md 11a94b37ea87 · method.md 827409845f5e · past-designs.md 63ecf227d9fa · rules.md e19bcaf0ebfe. All four match the manifest's sha256. The links to ../../inputs/i2/past-designs.md and ../../inputs/i2/rules.md resolve.

Each topic and step
-------------------

- T1 topic (Keep what worked in the stronger past design): from `past-designs.md · P2`: inside. past-designs.md is a fence file (the Examples part), and P2 is its section "P2 · j01 d01 yes-first (arm B)".
- T1 step 1 (P2 put the reply word first and came back +1.1 pp against the control in e01): from its topic's `past-designs.md · P2`: inside. P2's text opens with "Reply YES" after the sender, and its result line reads +1.1 pp [+0.1; +2.1] against the control. The number comes from the fence file, not from the Exp's own folder.
- T1 step 2 (every message opens with who it is from): from its own `rules.md · r1.2`, which overrides the topic's: inside. r1.2 says this.
- T2 topic (Fix the weaker past design's second ask): from `past-designs.md · P1`: inside. P1 is the file's section "P1 · the control (arm A)".
- T2 step 1 (P1, the control, asked for two things, reply YES or call to change it): from its topic's `past-designs.md · P1`: inside. P1's text reads "Reply YES to confirm or call us to change it."
- T2 step 2 (one clear ask, reply YES to confirm): from its own `goal.md · rules for this goal`, which overrides the topic's: inside. It is goal.md's first rule.

No step rests on own knowledge.

Failing steps
-------------

none

Outside the fence check
-----------------------

M02 m1's ② makes "one idea per strong past design, adapted to the goal". T2 builds on P1, which the file shows as the control, the weaker of the two. Whether a fix of the weaker design meets ② is a method question, not a fence question, so it does not change this verdict. Next owner: the designer side (t00), or the method's next version if ② should allow it.

pass
