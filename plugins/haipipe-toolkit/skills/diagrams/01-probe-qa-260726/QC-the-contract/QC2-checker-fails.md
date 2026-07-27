# What the checker actually fails on

state: 🟡 PARTIAL
owner: CC
method: enumerate the FAIL conditions from the SCRIPT rather than from the manual, so the gap between agreed, documented and enforced is visible

## Question
Which rules on this board are held by a machine rather than by agreement, and does the manual know?
Thirty-four named FAIL conditions in the paper checker and thirty-one in the application one, against the eleven `SKILL.md` documents.
What turns on it is knowing the size of the honour system, and the answer changed once the list was read off the script instead of off the manual.

The undercount is the finding, not a detail.
A reader of the constitution believes eleven things are enforced, so twenty-three enforced rules are invisible to anyone who has not opened 1096 lines of shell.
That cuts both ways: work fails a gate for a reason the manual never mentions, and a rule everyone assumed was honour-system has been mechanical all along.
The checker is the mechanical backstop at CHECK; the DRAFT self-review reads what the checker cannot, and the two are complementary rather than alternatives.

## Boundary
- ✅ Covered here
  The FAIL list, what each condition protects, and what is deliberately not checked.
- ↪ Covered elsewhere
  The QA contract itself is `QC1`; the entry states are `QC3`; the laws are `QA6` and `QA8`; the fork this script lives in is `QA4`.

## Diagram
```
   what SKILL.md documents          11
   what the paper script emits      34      ← counted 260726
   what the application emits       31

   ── the eleven the manual names ──────────────────────────────────
   the QA contract      qa-no-state · qa-working-no-started
                        qa-working-expired · qa-answered-empty
   the read state       read-target-working · read-target-superseded
   consistency          commissioned-target-answered
   the build lane       commissioned-no-owner · -no-eta
                        -no-blocks · -no-cross-project

   ── the twenty-three it does not ─────────────────────────────────
   the entry's shape    no-q-executor · no-state-field · empty-target
                        markdown-table · stale-old-format · dead-vocab
   the target           unresolved-target · workspace-target
                        read-target-no-state · commissioned-target-no-state
                        commissioned-target-superseded
   the harvest          answered-not-read · read-with-empty-a-executor
                        harvest-owed
   the states           state-planned · state-failed · probe-not-run
                        deferred-undeclared
   LAW 2               stake-disclosed · LAW2-q-executor-leak
   the bank            pp-id-in-bank-filename
   paper-only          sidecar-present · concern-with-route
                        concern-not-discussed

   ── one of them contradicts the manual outright ──────────────────
   SKILL.md L173  an undeclared deferral "FAILs as probe-not-run"
   the script     emits deferred-undeclared
   and the application fork does not emit it AT ALL

   ── and that same code FALSE-FAILS correct work ──────────────────
   MISQ, from the PROJECT root   12 FAIL
   MISQ, from the PAPER   root    7 FAIL      ← same data
   the 5 that vanish are all deferred-undeclared, on entries that
   DO carry their `**deferred**: depth-<n> · …` line. found by the
   QD2 fresh-agent run, 260726; reproduced at the source.

   NOT checked: LAW 1 · the strip's completeness · whether a station ②
   answer still matches ① · whether a hit really answers the question
```

## Items to Finish
- [x] 🧪 The FAIL conditions are counted from the script, not the manual
      34 in the paper fork, 31 in the application fork, against 11 in `SKILL.md`, counted 260726.
- [x] 🔬 A test suite with fixtures for five QX states
      `run-checker-tests.sh` over `test/fixture/`, carrying planned, harvested, answered-not-read, concern and lying-receipt cases.
- [ ] 📖 The unchecked rules are listed where a reader will see them
      The gap between agreed and enforced is currently only visible by comparing this page to the others.
      This closes when the skill itself names what the checker does not cover.
- [x] 🏃 The checker has been run on a real consumer
      Run 260726 against the MISQ paper: **exit 1**, and the failure count depends on where you stand.
      From the project root, 12 FAIL. From the paper root, 7 FAIL. Same paper, same checker, same data.
- [ ] 🐛 The cwd-dependent `deferred-undeclared` is fixed
      The deferral test greps `"$f"`, which `awk -v FN="$name"` set to the paper_root-relative path, while every other test in that loop uses fields awk already extracted.
      It resolves only when the process cwd is the paper root; from anywhere else every `deferred` entry fails whatever it contains.
      The fix is one word: grep `"$probe"`, the loop variable, which is already absolute.
- [ ] 🧯 The 7 real failures are fixed or triaged
      5 `answered-not-read` and 2 `commissioned-target-answered`, all of them one mistake seen from two entry states: the target says `answered` and the entry never re-read it.
      The other 5 this face reported on 260726 were the checker false-failing correct work, and are struck.
- [ ] 📋 The documented FAIL list matches the script
      `SKILL.md` names 11 and the paper script emits 34, so the constitution under-reports its own contract by 23 conditions.
      This is a correction rather than a ruling: the list can be regenerated from the script and pasted in.
- [ ] 🔧 The one outright contradiction is fixed
      `SKILL.md` line 173 says an undeclared deferral fails as `probe-not-run`; the script emits `deferred-undeclared`, and that was 5 of the 12 real failures.
      A reader chasing the documented code finds nothing.
- [ ] 🍴 `deferred-undeclared` is ported to the application fork, or ruled paper-only
      The model states the deferral rule generally and only one fork enforces it, so an application deferral with no depth-and-cost line passes today.
      Same shape as `QA4`'s `concern` question, and it closes with the same ruling.

## Where we are
The checker exists, is tested against fixtures, enforces three times what the manual says it does, and fails correct work depending on the caller's working directory.

It has not been run green against a real consumer, and the honour-system half of the board is not written down anywhere a reader would find it.
The 260726 count also moved this face's own subject: the interesting gap is no longer only between agreed and enforced, it is between enforced and DOCUMENTED, and that second gap is 23 conditions wide and fixable without any ruling.

- 260726 CC · 🏃 Run against the MISQ paper, the only real consumer
  `check-probe-cards.sh` over `papers/Paper-Personality2Opioid-MISQ2026`: exit 1, 12 FAIL, 13 PASS.
  The failures cluster into three kinds and none is a false alarm: 5 entries declare `deferred` without the depth-and-cost line that makes a deferral a decision rather than a skip, 5 sit `answered` with an empty `### a-executor` so the answer landed and nobody harvested it, and 2 are `commissioned` against a target that is already answered.
  Two of those condition names, `deferred-undeclared` and `answered-not-read`, do not appear in the eleven this face lists from `SKILL.md`, so the script enforces more than the contract documents.
  **Five of those twelve were later shown to be false**, see below.

- 260726 CC · 🔢 The real count, read off the script instead of the manual
  Extracting every emitted code: 34 in the paper fork, 31 in the application fork, 11 in `SKILL.md`.
  This face had been repeating the manual's number, which is how the undercount survived a page written specifically to enumerate the FAIL conditions.
  It also surfaced a direct contradiction at `SKILL.md` line 173, which names `probe-not-run` for a failure the script emits as `deferred-undeclared`, and that code was 5 of the 12 real failures.

- 260726 CC · 🐛 Five of the twelve were the checker, not the data
  The `QD2` fresh-agent run reported that the deferral test must be run with cwd set to the paper root or it false-fails.
  Reproduced: 12 FAIL from the project root, 7 from the paper root, and the five that vanish are exactly the `deferred-undeclared` ones this face had published as real.
  The entries carry their `**deferred**: depth-3 · …` lines; the checker could not see them.
  This face asserted "none is a checker bug", which was wrong, and it was wrong because the run was done from one directory and never repeated from another.

## Files
- `test/`
  `run-checker-tests.sh` and the five-state fixture tree.
- `SKILL.md`
  The FAIL list.
