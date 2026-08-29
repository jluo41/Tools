# Commission · C-VisitLBP · run 1

Start stamp (design desk, `date`): Sat Aug 29 15:33:54 EDT 2026

## ① LOAD

Load and follow `/remote-error`. It is a skill available to you by that name.

Nobody will tell you what this round is called. If the skill needs that, use its
own rule for it.

## ② THE REAL TARGET

A run on the CMS secure server failed on 27 Aug 2026. Nobody has processed it.
The log it left behind is a real file in this repo:

```
_WorkSpace/0-CMS-Store/Report-From-CMS-Server/v0827_Code0827/
    D01-reg_visitami_leftdigit/_WorkSpace.log
```

This is the error, verbatim, from the end of that file:

```
. // [ENV-04] tempfile writes into %TEMP%, which is unwritable on the CMS server and fails r(603), so this line only works because runs/run_reg_visitami_leftdigit.ps1 points STATATMP at the results folder first.
. tempfile base

. save `base'
invalid 'Temp'
r(198);

end of do-file
r(198);

end of do-file
r(198);
```

Repo root: `/Users/jluo41/Desktop/Physician-SPACE`. Work only inside it.

## ③ STEPS, in order

1. Run the skill's phase 1 on this error.
2. Run phase 2. Read the actual code before you write it.
3. Run phase 3 if and only if phase 2 earns it.
4. Run phase 4.
5. Run phase 5.
6. End with the skill's return block.

## ④ GATES

Copilot mode. If the skill tells you to stop and ask, STOP and say what you need.
Do not push past a stop to look productive. Stopping is a valid outcome here.

## ⑤ SCOPE FENCES, with reasons

- Do NOT edit anything under `Tools/plugins/haipipe-toolkit/skills/`. The skill
  you are using is frozen for the duration of this run; an edit to it would make
  every finding ambiguous between "the skill was wrong" and "the skill changed".
- Do NOT run Stata, PowerShell, or any pipeline. This machine has neither Stata
  nor the CMS data, by design.
- Do NOT mark anything CLOSED or ✅ verified. No run can happen from here.
- Everything else in the repo you may read, and may write if the skill says to.

## ⑥ THE DELIVERABLE THAT MATTERS MOST

Keep a numbered FRICTION LOG: every place the skill was unclear, wrong,
self-contradictory, or missing a rule you needed. That log matters more than the
work. Write it to:

```
Tools/plugins/haipipe-toolkit/skills/0_utils/_field-test/260829-remote-error/friction-log.md
```

Four values only: UNCLEAR · WRONG · SELF-CONTRADICTORY · MISSING. Each entry
needs the file and the sentence (or the absence) that caused it. "It felt
awkward" is not an entry.

## ⑦ STOP

Report after step 6. No self-directed continuation, no second issue, no cleanup
pass on things you noticed along the way. List them in the friction log instead.

## ⑧ THE CLOCK

Every stamp comes from the `date` command, never estimated. Put the start stamp
in the friction log's header and the end stamp in a Close block at its foot.

## ⑨ ONE MORE FENCE

Do not read anything under `_field-test/_design/`. It holds the prediction of how
this run will go, and an executor who reads the prediction performs it instead of
working. Everything you need is in this file and in the repo.
