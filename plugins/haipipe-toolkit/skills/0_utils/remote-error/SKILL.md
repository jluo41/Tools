---
name: remote-error
description: >-
  Diagnose a pasted error or log from a remote machine, explain the mechanism,
  fix the local canonical source when requested, and preserve an evidenced
  report. Use for remote/server/CI failures. Select environment-specific rules
  only from a confirmed profile; otherwise use the generic method. Internal
  debugging Steps and conversation labels do not create Workflow Runs.
argument-hint: "<paste the error text or screenshot>  [--profile <name>]  [--register <dir where the report is written>]  [--unit <task folder>]  [--session <name of this debugging round>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.10.1"
  last_updated: "2026-09-20"
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
  prove the fix works                 report checks actually run, or that none were available
```

**The one sentence that governs this whole skill:** never say a fix works. Say
what changed, report the actual local check result (or no available gate),
and say whether it has been re-run on the remote machine.


Inputs
------

Five, and only the first is required.

```
ERROR      required   the pasted text, log tail, or screenshot.
                      Everything else can be inferred from it or defaulted.

--profile  optional   which environment this failure came from. Picks the
                      ref/profile-<name>.md that carries the concrete commands.
                      Select from the user's environment, project configuration,
                      or another explicit source. Stata codes and .do/.ps1 paths
                      suggest an engine, but do not establish CMS. Use generic
                      mode if no profile is confirmed; ask only when the missing
                      environment changes the diagnosis or intended write.

--register optional   WHERE THE REPORT IS WRITTEN. The person owns this path.
                      Resolution order:
                        1. --register <dir>            given on the call
                        2. $HAIPIPE_ISSUE_REGISTER     an env var
                        3. the profile's default
                      Echo the resolved path in Step 5 before writing, so the
                      person sees where it went without opening a file.
                      If no profile matches and no register path was given,
                      ask where to write before creating any report.

--unit     optional   the task folder or module the failure belongs to.
                      Inferred from the run name or log path in ERROR.
                      Ask only if the guess would write to the wrong status file.

--session  optional   the NAME of this debugging round, as the person titled
                      their session. Reuse an existing name; otherwise use a
                      descriptive local report label for the bounded diagnosis.
                      It is RECORDED in the issue file, never used to pick a path
                      and never requires renaming or creating a chat.
```

`${REGISTER}` below means the path resolved here. Nothing about it is hardcoded
past this section. A register that does not exist yet is CREATED, not refused: a
new project keeps its own, and this skill is not tied to one study. If the
resolved register has no index file yet, say so before writing, so nobody
silently seeds a register the person did not name.


Session
-------

A debugging Session labels one bounded diagnosis, fix, and report. It does
not require a separate chat for every error or follow-up. Reuse the person's
existing name, or describe the affected unit and issue in the report. Never
rename a conversation or demand `/rename` to proceed.

The Session label is not a Workflow Run ID. Record the actual remote Run ID
separately when known; otherwise use `N/A`. READ, REASON, FIX, LINES, and
LESSON are internal Steps, not separate Runs. Preserve the report's label
when another log or a second fix belongs to the same diagnosis.


Profiles
--------

The five Steps are the same everywhere. The commands are not. Read a matching
profile FIRST, then follow the Steps. A generic pass has no engine-specific
commands, paths, status file, or static gate unless the user supplies them.

```
ref/profile-cms-stata.md   Stata + Windows PowerShell 5.1 on the CMS secure
                           server. The flagship, fully written: r-code table,
                           canonical/sync commands, the 19-rule static gate, the
                           ID grammar, the four landing places.

<no profile matches>       follow the generic Steps below and say plainly that
                           no profile covered this environment. Do not borrow
                           a profile's paths or status semantics. Ask for a
                           register path before writing; offer to add a profile
                           if repeated failures justify one.
```


The five Steps
--------------

Use the Steps needed for the request. After an edit, include LINES so the
person can locate the change. If evidence is insufficient, report the precise
missing evidence before attempting a fix.

```
 1  READ     name the failure KIND and the exact step it died at
 2  REASON   one paragraph: the MECHANISM, not a guess
 3  FIX      edit the CANONICAL file, then propagate to the copies
 4  LINES    report file:line for every line touched; run a profile gate only if one exists
 5  LESSON   preserve the report; add a rule only when a real checker can enforce it
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
  [SERVER]  the evidence identifies a current environment restriction.
```

A step that "ran" but moved zero rows is a `[LIES]`, not a `[CRASH]`, and a
register counts the two differently. The profile names which artifact shows that.


2 REASON
--------

One paragraph. Name the mechanism. Read the actual lines before writing it.

Rules that keep this Step honest, in every environment:

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
the project's documented generator/sync command, then check drift if a checker
is available. If regeneration is unavailable, report it as pending. Editing the copy costs the
fix: the next sync overwrites it, and the drift checker fails until it does.
Verify the head of the file before the first keystroke.

Generic laws the fix must not break:

```
match the file's own style   comment density, naming, line shape. A fix that
                             reads as foreign is a fix nobody maintains.
issue references             follow the selected project's issue convention;
                             do not fabricate an ID when none exists.
comment shape                follow the file and its actual checker; a CMS
                             comment rule is not a rule for other projects.
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

Then run the selected profile's static gate for the affected unit, if that
profile defines one, and paste its verdict line. Without a profile gate, say
that no static gate was available. A passing gate covers only its assertions.
Say "gate green" only when the actual verdict is green; never infer a remote
execution result from it.


5 LESSON
--------

Profiles define the durable landing places for their environment. The
CMS-Stata paths are defined only in `profile-cms-stata.md`.
With no matching profile, write only to a path the user has explicitly
provided or confirmed; do not invent a daily findings file, register index,
unit status file, or gate.

```
THE REPORT    <profile-defined path, or the user-confirmed path>
              Shape: ref/issue-file-template.md
              The generic shape records the debugging Session and a Remote Run
              ID when known. A profile defines its issue id and path grammar.

THE DAY       <profile-defined daily findings path, if the profile uses one>

THE REGISTER  <profile-defined index path, if the profile uses one>
THE STATUS    <profile-defined unit status path, if the profile uses one>

THE GATE      <profile-defined static checker, if one exists>
```

Never create a profile-specific artifact just because the generic method lists
it. If the user supplied a register directory but the profile does not define
the remaining landing places, ask before creating additional files.

The selected profile owns issue IDs and status words. A generic report may
use `unassigned` and describe the observed change and remaining verification.
A local edit does not prove a successful remote rerun. CMS-specific ID and
status rules are in `ref/profile-cms-stata.md`.

The reply shape
---------------

The five Steps are the WORK. This skill's required report sections are a
scoped exception to `/response-format`'s general chat layout; keep this order
when `/remote-error` is active. A separate operation inside one Step does not
create a Run.

**Line 1** is the verdict in one sentence: the KIND, the remote step it died at, and
the cause established by the evidence, or what remains uncertain.

```
## 🔍 What Failed                   Step 1 · WHERE · CODE · KIND
## 🧠 Why                           Step 2 · the mechanism, quoting file:line
## 🛠️ What I Changed, Where, And Why Step 3 + 4 · past tense, already done
## 📄 The Report I Wrote             Step 5 · the issue file, then the rest
## 🙋 Next Action                    only a real unresolved decision or missing evidence
```

Use only the sections with actual content, in the order above. Next Action is
optional: omit it when nothing remains for the user to decide. Do not repeat
all facts in another summary block.

**THE SKILL CHANGES THE CODE. It does not hand the person a to-do list.**
Step 3 edits the canonical file. So this section is written in the PAST tense
and reports work that is already done, in three parts, in this order:

One GROUP per file changed. Every group is two bold labels, each followed by one
fenced block, then the WHY as plain sentences. **WHERE comes first.**

```
**WHERE**   one fenced block. The directory on its own line, then the file with
            its LINES as `:NN-NN`, then whether it is CANONICAL or a COPY, then
            how many copies the sync fed. First, because a change is unreadable
            until you know where it is, and with two files changed a reader who
            met the code first cannot tell which block belonged to which.

**WHAT**    one fenced block, in the language of the file. Mark old and new
            lines with valid comments: `# was` / `# now` for Python or shell,
            `// was` / `// now` where supported. For a format without comments,
            use a `diff` fence with removed/added lines. The smallest
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
       copied file to prove the fix travelled. Use this only when a manual transfer is actually needed;
       otherwise state the verified deployment/sync mechanism. A remote rerun
       may still be needed after the fix reaches that machine.

       THE WHAT BLOCK IS THE REPO FILE, BYTE FOR BYTE. Never offer a "simpler
       version to type by hand", a "minimum edit", or a shortened variant that
       the repo does not hold. The person copies from the repo; the moment the
       reply and the file disagree, every later screenshot is of a third thing
       that exists nowhere, and each round of that costs them a full run.
       If a shorter or a diagnostic form is the right one, WRITE THAT FORM INTO
       THE CANONICAL and sync it, then quote it. Ruled by JL on 260829, after
       six hand-edits diverged from the repo: "you didn't change this!!! I will
       follow this to update the server, you get it?"
GATE   the check actually run and its verdict, or "No local gate available".
       Use the profile's verdict format only when that profile defines it.
       Never "this will run".
```

If the fix could NOT be made from here, this section does not exist. Say so in
🙋 Next Action, whose outcome sentence carries `need-more-log` or
`no-repo-change`. A section
titled "what I changed" that changed nothing is the `[LIES]` kind, committed by us.

**📄 The Report I Wrote shows the report, not only its path.** A path is not a
report; the person must be able to decide whether to open it.

```
- the ISSUE FILE first: its assigned id (or `unassigned`), its full path, and one line
  per heading it filled (Symptom · Cause · Fix · Scope · Not affected)
- then any other landing places actually written, with what was appended
- then the gate row: the checker rule id if one was grown, or `--` with the
  reason a checker rule was not added or a checker was unavailable
```

Name the diagnosis OUTCOME in the report. Add **🙋 Next Action** only for an
actual unresolved decision or missing evidence. An outcome is not a new Run.

```
THE OUTCOME, one of four, written as a SENTENCE and never as a `key: value`:

  fixed              a canonical file was edited. State checks actually run
                     and their verdicts, or no available local gate. This says
                     nothing about a remote rerun unless evidence was supplied.
  need-more-log      the paste was not enough. ONE named file or log line would
                     settle it, and this run stopped rather than guess.
  environment-limit  evidence identifies a current environment restriction;
                     state the condition and what would need to change.
  no-repo-change     the cause is real but lives outside the code: a stale data
                     build, a rerun owed, a value only the machine holds.

WHEN A DECISION OR EVIDENCE IS STILL NEEDED:

  COMMIT AND PUSH? Only when concrete changes exist and this decision is
  relevant and still open. Name the changes and destination. Reuse an existing
  explicit authorization for that scope; do not ask again. On need-more-log or
  no-repo-change, do not invent a commit question.
  ANYTHING STILL BLOCKED? Name what this session could not settle: a file it
  could not read, a rerun it cannot perform, a value only the machine has.
```

The four words are the same four the register and any later reader use, so
saying "this is `need-more-log`, and here is the file that would close it" is
exact without being a field block.

**A skipped Step leaves NO section.** On `need-more-log` there is no
🛠️ and no 📄; the shape is 🔍 · 🧠 How Far I Got · 🙋 What I Need. An empty
heading reads as work that happened.


Refs
----

```
ref/profile-cms-stata.md    the CMS secure server: commands, codes, gate, register
ref/issue-file-template.md  the generic remote-error report shape
../field-test/       the same loop against a PLANNED run
```
