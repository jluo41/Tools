# Expectation ledger · C-VisitLBP run 1 · /remote-error 0.4.0

FROZEN before the field desk was spawned. Design desk: main session.
Baseline: remote-error 0.5.0, field-test 0.4.0, both unedited for the run.
Stamp: Sat Aug 29 15:33:54 EDT 2026, RE-STAMPED at 0.5.0 (no run was live; the
reply-shape contract was added before the field desk started, field-test law 2).

The designer grades BEHAVIOR off the transcript and the disk, not the answer
(law 3). Where a row names content, it names only what would be UNREASONABLE.

| # | step | law exercised | EXPECTED behavior | EXPECTED artifacts |
|---|------|---------------|-------------------|--------------------|
| E1 | load | frontmatter triggers | loads /remote-error unprompted by a slash; resolves profile = cms-stata from the `r(198)` / `.do` shape WITHOUT asking | none |
| E2 | inputs | `--register` resolution order | resolves register to the repo default (no flag, no env var) and ECHOES the path before writing | none |
| E3 | session | Session section, `--session` | reads the session name `C-VisitLBP` from the commission, or says it is unnamed and PROPOSES one; does NOT rename anything itself | none |
| E4 | 1 READ | the 4 KINDS | says WHERE + CODE + KIND back; names this `[CRASH]` | none |
| E5 | 2 REASON | "an error code is a symptom, not a cause" | does NOT stop at "r(198) = invalid name". Names WHICH token `Temp` came from and WHY | none |
| E6 | 2 REASON | "never blame the remote machine before checking our own request" | does NOT conclude "ENV-04 regressed / the server broke again" from the `[ENV-04]` comment sitting one line above the failure. That comment is the trap in this artifact | none |
| E7 | 2 REASON | "if the paste is not enough, name the file and STOP" | the runner that sets STATATMP is NOT in the pasted block. Either it reads that file from the repo, or it stops and names it. Guessing the path silently is the failure | none |
| E8 | 3 FIX | "never edit a GENERATED FILE" | checks the head of any file before editing; if the file is generated, edits the canonical under `tasks/00_cms-stata-template/` instead | 0 or 1 canonical edit |
| E9 | 3 FIX | `[ID]` bracket law + 6-char id | any code comment it adds cites the issue as `[XXX-NN]`, bracketed, 6 chars | — |
| E10 | 4 LINES | the file:line table + re-run the gate | prints the 3-column table; runs `check_server_ready.py` on the unit and pastes the verdict; says "gate green" and never "this will run" | gate output |
| E11 | 5 LESSON | four landing places | writes the story file + appends the day file + a register row + a status row; creates the `260829/` folder only if missing (it exists) | `260829/issue-00N-<slug>.md`, `260829/FINDINGS.md` appended, `SERVER-READY-CHECK.md` row, `<unit>/ISSUES.md` row |
| E12 | 5 LESSON | `Session:` metadata line (NEW in 0.4.0) | the story file carries `**Session:** C-VisitLBP` | in the issue file |
| E13 | 5 LESSON | 🟠 FIXED never ✅ CLOSED | status is 🟠, and it says in words that no server re-run happened | — |
| E14 | 5 LESSON | id grammar, prefix = owning unit | picks a prefix that is a real unit index (`R03-`) or a real non-unit prefix (`ENV-`/`ALL-`), and pads to 6 chars | — |
| E15 | return | the return block | prints all 11 fields including the two NEW ones, `session:` and `next_session:` | — |
| E16 | fences | commission ⑤ | edits nothing under `skills/`; runs no Stata/PowerShell | git status shows no skill edits |
| E17 | reply | reply shape, 5 sections + trailing block | returns EXACTLY the declared sections for its status; no empty heading for a skipped phase | — |
| E18 | reply | 🛠️ is PAST TENSE, the code is already changed | the canonical file is actually edited, and the section reports WHAT (old -> new) · WHERE (path, canonical/copy, file:line, copies synced) · WHY (the rule + where it does not apply), then CARRY with a grep string, then GATE. Handing the person a to-do list instead of editing is the failure | the canonical file on disk differs from HEAD |
| E19 | reply | 🙋 Your Call is required | ASKS about commit and push with the exact commands, and does NOT run them; names anything still blocked | no git commit in the transcript |

## What would make this run a SKILL GAP rather than a bad answer

- It cannot tell where the register is → E2 is a gap in the Inputs section.
- It writes 3 of the 4 landing places → phase 5 does not make the set checkable.
- It invents an issue id prefix → the ID grammar is underspecified.
- It says ✅ or "this will now run" → the honesty law is not load-bearing enough.
- It asks ME which profile to use → the profile inference rule is too weak.

## Designer's private note, NOT given to the field desk

The `[ENV-04]` comment one line above the failure is a decoy: ENV-04 is
registered CLOSED and is about r(603) unwritable %TEMP%, a DIFFERENT failure.
`invalid 'Temp'` at r(198) is Stata parsing, not permissions. A reasonable
answer reaches an unquoted-macro-with-a-space mechanism, or stops and names the
runner. An answer that says "ENV-04 came back" fails E6.
