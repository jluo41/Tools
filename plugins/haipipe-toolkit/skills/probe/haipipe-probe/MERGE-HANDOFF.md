MERGE HANDOFF — two sessions → one (2026-07-19)
================================================

WHY THIS EXISTS.
Two live Claude sessions have both been editing the SHARED probe/paper skill files on the same
filesystem. Before continuing in ONE surviving session, read this so the two do not collide
(撞车). Companion: `HANDOFF.md` (the full design record) — this file is the merge protocol only.


1. CANONICAL STATE — the source of truth RIGHT NOW
--------------------------------------------------

The probe file was redesigned to be Q-EXECUTOR-oriented. These files are DONE and CANONICAL;
treat them as truth and reconcile everything else TO them:

- `SKILL.md`                       v9.5.0  — the constitution, new anatomy. THE authority.
- `ref/probe-template.md`                  — the new "version B" format (`## QX<n>` + four `###`).
- `CHANGELOG.md`                           — history through [9.5.0].
- `HANDOFF.md`                             — the 8-point design record + pending list.

⚠️ THE OLD PROBE FORMAT IS DEAD. These strings are RETIRED — if you see them in any probe/paper
   file, that file is STALE and must be swept, never restored:
     `- serves:`  ·  `- match:`  ·  `- a-consumer:`  ·  `## Why`  ·  `## Q-<Stage>-<n>` as a PROBE
     entry heading (it is still the STAGE-DOC Q-consumer heading — that one stays).
   The new vocabulary: `## QX<n>` entry · `### q-executor` · `### q-consumer` (bulleted, copies in
   each consumer's original question) · `### bank binding` (`**route**`/`**bank**`/`**target**`/
   `**state**`) · `### a-executor` (a COPY of the QA answer).


2. DONE — do NOT redo
---------------------

- Probe-file redesign + constitution sync (v9.5.0), template, CHANGELOG. (this session)
- DRAFT-authors-the-plan phase model + DRAFT self-review (constitution v9.2.0–9.4.0;
  `haipipe-paper-draft` v4.2.0; `haipipe-paper-seed`). (both sessions, already reconciled on disk)


3. PENDING — each does ONCE; the surviving session works this top-down
----------------------------------------------------------------------

a. `check-probe-cards.sh` — TWO copies, rewrite PASS 1 (the awk that parses probe files) to the new
   format: section = `## QX<n>` + `### ` subsections; parse `**field**:` under `### bank binding`;
   `--stage` gate greps the `### q-consumer` bullets for the `Q-<Stage>` id; DROP `no-why-section`;
   rename serves→q-consumer, match→bank, a-consumer→a-executor. QA-file checks (PASS 3) UNCHANGED.
     paper: `../../paper/2-phase/1-probe/haipipe-paper-probe/check-probe-cards.sh`
     app:   `../../application/2-phase/1-probe/haipipe-application-probe/check-probe-cards.sh`
b. `../../paper/2-phase/1-probe/haipipe-paper-probe/SKILL.md` — its own description + body still name
   the OLD fields (serves/match/a-consumer/## Why). Sweep to the new anatomy.
c. Paper stage skills — field-name sweep: `grep -rn "a-consumer\|serves:\|## Why\|- match:" ../../paper`.
d. APPLICATION family (whichever session owns it): mirror everything — app DRAFT worker, app PROBE
   worker, `application/haipipe-application/SKILL.md`, and any app-side probe template.
e. Existing real probe files — migrate to the new format. Known: `examples/Project-Personality-OpioidRx/
   papers/Paper-Personality2Opioid-MISQ2026/1-probes/PP01_seed-feasibility.md` (old format).


4. COLLISION RULES — how not to 撞车
------------------------------------

- FILES ARE SHARED ON DISK. Before editing ANY probe/paper skill file, RE-READ it first — the other
  session may have changed it since you last saw it. (The "modified since read" guard blocks silent
  stomps, but re-reading avoids the churn.)
- THE CONSTITUTION WINS. `SKILL.md` is the single source of truth. Where a worker, template, or stage
  skill disagrees, fix the WORKER to match the constitution — never edit the constitution to match a
  stale worker.
- NEVER reintroduce the retired strings from §1.
- NEVER run the old checker on a new-format probe file, or vice versa — do the constitution + both
  checkers as ONE consistent set before any real probe file is checked.
- COORDINATE VERSION BUMPS. Read the current `version:` in the frontmatter FIRST; bump from what is
  actually there (this session already took it to 9.5.0).


5. TO MERGE — JL's steps
------------------------

1. Pick ONE session to continue in (the "survivor").
2. In the survivor: read `HANDOFF.md` then this file.
3. STOP the other session (do not keep editing from it).
4. The survivor's first task = the PENDING list §3, top-down (start with the checker ×2, since it is
   the last thing blocking a real probe file from being validated).
