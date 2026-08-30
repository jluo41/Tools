---
name: remote-error
description: "The RETURN leg of work on a machine this session cannot reach: a person pastes an error a remote run produced, and this skill names the failure kind, gives the mechanism, edits the CANONICAL file, reports every line it touched, and lands the lesson in a register the person names, so the same failure cannot reach that machine twice. Engine-neutral method; the concrete commands come from a PROFILE in ref/ (ships with cms-stata for the CMS secure server). Sits beside field-test, which runs the same failure-to-rule loop against a planned run instead of a real one. Use when an error, a screenshot, a log tail or a red console comes back from a server, a VDI, an SSH box, a CI run, or a live site. One session per remote step, named by the person, and the name is recorded in the issue file so the chat and the fix stay tied. Trigger: remote error, server error, it failed on the server, remote run failed, name this session, r(198), r(111), r(601), 403 from the site, read this log, why did it crash, paste the error, new lesson, issue register, /remote-error."
argument-hint: "<paste the error text or screenshot>  [--profile <name>]  [--register <dir where the report is written>]  [--unit <task folder>]  [--session <name of this debugging round>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.9.0"
  last_updated: "2026-08-29"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: remote-error (the return leg)
====================================

A run happens somewhere this session cannot reach: a secure server, a VDI, an SSH
box, a CI runner, a live website. The code is here; the machine is not. So the
only thing that crosses back is TEXT that a person pastes, and the only honest
workflow is to reason from that text plus the code in this repo.

This is a METHOD, not an engine specialist. It lives in `0_utils` beside
`field-test`, which runs the same failure-to-rule loop against a PLANNED
run; this one runs it against a REAL failure. The engine-specific commands live
in a profile, never in this file.

```
  YOU CANNOT                          YOU CAN
  run the code                        read the code
  reach the machine                   read the log the person pasted
  open the data                       read the column list a check step printed
  prove the fix works                 prove the fix passes the static gate, and say so
```

**The one sentence that governs this whole skill:** never say a fix works. Say
what changed, say the static gate is green, and say it has not been re-run on
the machine.


Inputs
------

Five, and only the first is required.

```
ERROR      required   the pasted text, log tail, or screenshot.
                      Everything else can be inferred from it or defaulted.

--profile  optional   which environment this failure came from. Picks the
                      ref/profile-<name>.md that carries the concrete commands.
                      Inferred from the error's own shape: an r(nnn) code or a
                      .do path means cms-stata. Ask only if nothing in ERROR
                      names an environment.

--register optional   WHERE THE REPORT IS WRITTEN. The person owns this path.
                      Resolution order:
                        1. --register <dir>            given on the call
                        2. $HAIPIPE_ISSUE_REGISTER     an env var
                        3. the profile's default
                      Echo the resolved path in phase 5 before writing, so the
                      person sees where it went without opening a file.

--unit     optional   the task folder or module the failure belongs to.
                      Inferred from the run name or log path in ERROR.
                      Ask only if the guess would write to the wrong status file.

--session  optional   the NAME of this debugging round, as the person titled
                      their session. Read it from the transcript if it is
                      already named; otherwise propose one from the grammar in
                      the next section and let the person type `/rename`.
                      It is RECORDED in the issue file, never used to pick a path.
```

`${REGISTER}` below means the path resolved here. Nothing about it is hardcoded
past this section. A register that does not exist yet is CREATED, not refused: a
new project keeps its own, and this skill is not tied to one study. If the
resolved register has no index file yet, say so before writing, so nobody
silently seeds a register the person did not name.


Session
-------

**One session = one remote step.** Name it before the first paste, end it when
that step is done, open a new one for the next step. The name is the only thing
that ties a chat to the files it wrote, so it goes into the issue file; a reader
six weeks later can then find the conversation the fix came from.

```
NAME GRAMMAR, first match wins

  <STAGE>-<COHORT>    C-LBP   D-CABG   B-AMI
                      a remote RUN under debug: stage letter + what it runs on

  <UNIT>-<ISSUE-ID>   C01-R01-13
                      one issue that outlived its run and now owns a round

  SKILL-<SLUG>        SKILL-REMOTE-ERROR
                      building or repairing the tooling, running nothing
```

```
CUT A NEW SESSION                          STAY IN THIS ONE
the step changed   C-LBP done, D-LBP next  a new error at the same step
the topic changed  running -> tool-building  a second fix to the same file
the fix landed and a relaunch is next      the person is still pasting logs
```

`/rename` is the PERSON's command and this skill never runs it: a session that
renames itself mid-round breaks the tie to the files already written under the
old name. At the end of phase 5, print the name the NEXT session should carry
and stop there.


Profiles
--------

The five phases are the same everywhere. The commands are not. Read the profile
FIRST, then run the phases.

```
ref/profile-cms-stata.md   Stata + Windows PowerShell 5.1 on the CMS secure
                           server. The flagship, fully written: r-code table,
                           canonical/sync commands, the 19-rule static gate, the
                           ID grammar, the four landing places.

<no profile matches>       run the phases on the generic laws below and say
                           plainly that no profile covered this environment.
                           Then offer to write one; a second failure from the
                           same machine is what justifies it, not the first.
```


The five phases
---------------

Run them in order. Do not skip 4; the person asked for it by name.

```
 1  READ     name the failure KIND and the exact step it died at
 2  REASON   one paragraph: the MECHANISM, not a guess
 3  FIX      edit the CANONICAL file, then propagate to the copies
 4  LINES    report file:line for every line touched, then re-run the static gate
 5  LESSON   land it so the gate catches it next time
```


1 READ
------

Find three things in what the person pasted, and say all three back:

```
WHERE   the unit, the run name, and the step that was executing
CODE    the error code or message, verbatim
KIND    one of four. This vocabulary is generic and does not change per profile:

  [CRASH]   it stops, or never starts.               Cheapest kind.
  [NUMBER]  it runs clean and the printed number is wrong.  Worst kind.
  [LIES]    it runs, and the report it hands back is false.
  [SERVER]  the machine cannot do this, and never will.
```

A step that "ran" but moved zero rows is a `[LIES]`, not a `[CRASH]`, and a
register counts the two differently. The profile names which artifact shows that.


2 REASON
--------

One paragraph. Name the mechanism. Read the actual lines before writing it.

Rules that keep this phase honest, in every environment:

```
- Quote the line of code that does it, with its file:line. No paraphrase.
- If two causes fit, say both, and say which check would tell them apart.
- Never blame the remote machine before checking our own request. RateMDs was
  logged in this repo as Cloudflare-blocked for months; it was our own header,
  a Firefox TLS profile sending a Chrome User-Agent. Same discipline here.
- An error code is a symptom, not a cause. "variable not found" is not a cause;
  WHICH variable, and WHY it is absent, is.
- If the paste is not enough, say exactly which file or which line of the log
  would settle it, and stop. A guessed cause becomes a wrong lesson forever.
```

The profile carries the code-by-code table for its engine.


3 FIX
-----

**Never edit a file whose head says GENERATED FILE.** A generated file names its
canonical source in its own first lines. Edit the canonical, then propagate with
the profile's sync command, then confirm zero drift. Editing the copy costs the
fix: the next sync overwrites it, and the drift checker fails until it does.
Verify the head of the file before the first keystroke.

Generic laws the fix must not break:

```
match the file's own style   comment density, naming, line shape. A fix that
                             reads as foreign is a fix nobody maintains.
cite the issue as [ID]       at the line that causes it. The brackets are what
                             makes a later sweep safe: in this repo bare S33 is
                             also the ICD-10 code for lumbar sprain, and a sweep
                             on the bare form would have corrupted 49 codes.
one comment line = one       a sentence wrapped across two comment lines breaks
  sentence                   this repo's checker. A long line is fine.
no constant that can go      a version, a path, a host: one source of truth,
  stale in two places        never a copy in a runner script.
```

The profile adds its environment's own hard limits: character set, shell version,
what is absent at runtime.


4 LINES
-------

Report, always, in this shape. The person reads this instead of a diff.

```
FILE                                          LINES   WHAT + WHY
<canonical path>                              :46-47  [ID] one sentence
  (canonical, synced to N copies)             :52-65  [ID] one sentence
<other file>                                  :389    one sentence
```

Then re-run the profile's static gate for the affected unit and paste its verdict
line. Green is necessary and NOT sufficient: a gate scores what someone thought
to write down. Say "gate green" and never "this will run".


5 LESSON
--------

One failure lands in several places, and fewer than all of them means it comes
back. `${REGISTER}` is the path resolved in Inputs, never a literal typed here;
print it once before the first write.

```
THE STORY     ${REGISTER}/<YYMMDD>/issue-00N-<slug>.md
              Shape: ref/issue-file-template.md
              Its `Session:` line carries the session NAME, verbatim. An issue
              with no session name cannot be traced back to its reasoning.

THE DAY       ${REGISTER}/<YYMMDD>/FINDINGS.md
              Append a section. Create file and folder if the day is new.

THE REGISTER  ${REGISTER}/<the profile's index file>
+ THE STATUS  <unit>/ISSUES.md, which stays with the CODE and NOT in
  ROW         ${REGISTER}, so a reader of the folder sees it
              One line each, same ID, same status emoji.

THE GATE      the profile's static checker, plus the lessons file that checker
  if a static cites. Then put the rule id in the register's `gate` column.
  rule can     An issue no static rule can catch keeps gate `--`. A register
  catch it     counts those on purpose; do not invent a rule to fill the column.
```

**ID grammar** (ruled by JL 260822 for this repo, and a good default anywhere):

```
Exactly 6 characters, always. Pad the counter: C02-01, never C02-1.
Column tables in these files are hand-aligned; a variable-width id ruins them.
The prefix is the OWNING unit's own index, verbatim, never an abbreviation
invented for the register: read the id, open that folder, the issue is in there.
Two prefixes are not units, because two kinds of problem have no folder to open:
the environment itself, and the shape that repeats in every unit.
A renumber keeps a `was` column, since old ids are cited from code comments.
```

**Status emoji, and the one that matters most:**

```
🔴 OPEN      it will still bite you today
🟠 FIXED     repaired in the repo, NEVER re-run on the machine  <- default after 3
🟡 PARTIAL   some units repaired, others still live
✅ CLOSED    repaired AND verified by a clean run
⚪ KNOWN     permanent limit, history, or pure precaution
```

A fix this skill makes is 🟠, not ✅. Only a clean run on the real machine moves
it to ✅, and this session cannot produce one. Writing ✅ from here is the
`[LIES]` kind of failure, committed by us.

The reply shape
---------------

The five phases are the WORK. This is how the work comes back in chat. Follows
`/claude-response-format`: the answer on line 1, then sections of bullets, and a
fenced block only where one is earned.

**Line 1** is the verdict in one sentence: the KIND, the step it died at, and
whose fault it is (ours or the machine's).

```
## 🔍 What Failed                   phase 1 · WHERE · CODE · KIND
## 🧠 Why                           phase 2 · the mechanism, quoting file:line
## 🛠️ What I Changed, Where, And Why phase 3 + 4 · past tense, already done
## 📄 The Report I Wrote             phase 5 · the issue file, then the rest
## 🙋 Your Call                      commit and push? · anything still blocked
```

Five sections, and nothing after them. There is no machine-readable summary
block: every fact one would carry is already in the sections above it, and
repeating them under a second, unreadable heading is noise the person has to
scroll past. The reply ends on 🙋 Your Call, which is a question to them.

**THE SKILL CHANGES THE CODE. It does not hand the person a to-do list.**
Phase 3 edits the canonical file. So this section is written in the PAST tense
and reports work that is already done, in three parts, in this order:

One GROUP per file changed. Every group is two bold labels, each followed by one
fenced block, then the WHY as plain sentences. **WHERE comes first.**

```
**WHERE**   one fenced block. The directory on its own line, then the file with
            its LINES as `:NN-NN`, then whether it is CANONICAL or a COPY, then
            how many copies the sync fed. First, because a change is unreadable
            until you know where it is, and with two files changed a reader who
            met the code first cannot tell which block belonged to which.

**WHAT**    one fenced block, in the language of the file. Inside it, `// was`
            above the old lines and `// now` above the new ones. The smallest
            quotable unit, never a diff of the whole file. Both halves in ONE
            block, so the eye compares them without a heading in between.

WHY         plain sentences under the two blocks, no label and no fence: the
            rule this generalizes to, and where the rule does NOT apply, so a
            later sweep does not over-apply it. The [ID] cited at the changed
            line is what makes that sweep safe.
```

The shape on screen, verbatim, one file:

    **WHERE**

    ```
    tasks/00_cms-stata-template/C00_data_pipeline_template/scripts/0-libs/
      lib-state-end.do   :47-56   CANONICAL  -> synced to 3 C-stage jobs
    ```

    **WHAT**

    ```stata
    // was
        state_write_table
        state_write_report "`focus_vars'"

    // now
        capture state_write_table
        if _rc != 0 {
            display as error "  WARNING: state_write_table failed, rc=" _rc
        }
    ```

    - A receipt writer must never be able to kill the run it is describing.
    - Not applied to the step body itself, where a failure IS the result.

Two files changed means two WHERE/WHAT pairs, which keeps a path attached to its
own code. Ruled by JL on 260829, twice: the ORDER is his from the first ruling
and never moved, and the RENDERING is the second, the two bold labels with
`// was` and `// now` in one block. 0.7.0 wrongly read the second as replacing
the first and flipped the order; 0.8.0 puts it back.

Then exactly two bullets, in this order, and nothing else:

```
CARRY  what the person copies to the machine, and ONE string to grep in the
       copied file to prove the fix travelled. This is the only step left to
       them, because their copy on the machine is a different file that nobody
       has touched.

       THE WHAT BLOCK IS THE REPO FILE, BYTE FOR BYTE. Never offer a "simpler
       version to type by hand", a "minimum edit", or a shortened variant that
       the repo does not hold. The person copies from the repo; the moment the
       reply and the file disagree, every later screenshot is of a third thing
       that exists nowhere, and each round of that costs them a full run.
       If a shorter or a diagnostic form is the right one, WRITE THAT FORM INTO
       THE CANONICAL and sync it, then quote it. Ruled by JL on 260829, after
       six hand-edits diverged from the repo: "you didn't change this!!! I will
       follow this to update the server, you get it?"
GATE   the verdict line, last: <UNIT> n/<total>. Never "this will run".
```

If the fix could NOT be made from here, this section does not exist. Say so in
🙋 Your Call, whose outcome sentence carries `need-more-log` or
`no-repo-change`. A section
titled "what I changed" that changed nothing is the `[LIES]` kind, committed by us.

**📄 The Report I Wrote shows the report, not only its path.** A path is not a
report; the person must be able to decide whether to open it.

```
- the ISSUE FILE first: its 6-char id, its slug, its full path, and one line
  per heading it filled (Symptom · Cause · Fix · Scope · Not affected)
- then the other landing places, one bullet each, with what was appended
- then the gate row: the checker rule id if one was grown, or `--` with the
  reason no static rule can catch it
```

**🙋 Your Call is required, never optional.** It opens by naming the run's
OUTCOME, then asks two questions it never answers itself.

```
THE OUTCOME, one of four, written as a SENTENCE and never as a `key: value`:

  fixed              a canonical file was edited and the static gate is green.
                     The machine has not re-run it, so this is 🟠 and not ✅.
  need-more-log      the paste was not enough. ONE named file or log line would
                     settle it, and this run stopped rather than guess.
  environment-limit  the machine cannot do this and never will. No repo change
                     can help.
  no-repo-change     the cause is real but lives outside the code: a stale data
                     build, a rerun owed, a value only the machine holds.

THEN, both, every time:

  COMMIT AND PUSH? Ask in ONE plain sentence naming what would be committed and
  which repo or submodule it lands in. Do NOT print the commands: the person is
  deciding, not typing, and a wall of git text is the assistant's work showing.
  On a yes, THIS SESSION runs them and reports the commit line.
  ANYTHING STILL BLOCKED? Name what this session could not settle: a file it
  could not read, a rerun it cannot perform, a value only the machine has.
```

The four words are the same four the register and any later reader use, so
saying "this is `need-more-log`, and here is the file that would close it" is
exact without being a field block.

**A skipped phase leaves NO section.** On `need-more-log` there is no
🛠️ and no 📄; the shape is 🔍 · 🧠 How Far I Got · 🙋 What I Need. An empty
heading reads as work that happened.


Refs
----

```
ref/profile-cms-stata.md    the CMS secure server: commands, codes, gate, register
ref/issue-file-template.md  the issue-00N story shape
../field-test/       the same loop against a PLANNED run
```
