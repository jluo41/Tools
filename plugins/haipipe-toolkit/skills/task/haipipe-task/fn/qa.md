Function: qa
=============

The task layer's question door.
One question in general language goes in; a path to a QA file comes out.

The verb does not know who is asking, or why, and must not try to find out.
It never reads a paper.
It never resolves an id.
A consumer is just one caller among three.

⚠️ `qa` is this layer's SIDE door, not its engine.
The task session's PRIMARY mode is autonomous Plan → Build → Execute → Report, with no question pending at all.
Most questions should already have an answer sitting in the bank before anyone asks.

QA-file anatomy — the field names, the state values, the TTL constant and the race guard — is DEFINED HERE, in the sections below.
This layer WRITES these files, so this layer is canonical for their shape.

NAMING: `QA/<n>-<slug>.md`, where `n` is CREATION ORDER — `ls QA/` IS the index.
A plain descriptive slug, never an identifier handed in by whoever asked.

WHERE: `$OUTPUT_ROOT/QA/` — the job in self-serving mode, the consumer's
store in consumer-serving mode, the same resolution `results/` uses and defined
in `ref/hierarchy.md` § job. A QA digest is an ANSWER, and an answer
belongs to the data it was computed on, not to the code that computed it.

⚠️ This is the gate's sharpest edge. Scan the WRONG bank and gate ① misses a
`working` file, so two callers run the same work, or misses an `answered` one,
so settled work is redone. When a store is in play, `--check-only`, the claim
write and the Report completion must ALL address `$OUTPUT_ROOT/QA/`. Two
cohorts sharing one job have two separate banks and must never see
each other's.

The discovery twin states every one of these rules IDENTICALLY — same field names, same state
values, same TTL constant. They must not drift.
This file is the VERB.


Usage
------

```
/haipipe-task qa "<question>" [<job>]     answer it
/haipipe-task qa "<question>" --check-only        detect only. write nothing. run nothing.
```

**`<question>`** — general language.
No paper reference, no id, no stake.
If one arrives anyway: strip it, restate the question on its own terms, and answer the restatement.
Say you stripped it, in the return.
Never act on it.
Never launder it.
Never refuse over it.

**`<job>`** — optional, e.g. `tasks/B01_evaluation_pretrain/B4_fit_scaling_law/`.
Absent → scan every job under the project's `tasks/`.
A job is ANY directory holding work: a `*.py`, `workflow/`, `results/`, `configs/` or `runs/`.
⛔ NEVER filter by name.
`{NN}_<name>` is the majority convention, but 31% of real jobs do not match it (`B4_fit_scaling_law`, `C3-Visual-ForecastScaling`).
A name filter goes silently blind to a third of the bank.

**`--check-only`** — the consumer's MATCH step calls this.
It is a FREE pass by definition.
It must never fall through to ③ and spawn an unbudgeted run.

THREE CALLERS, one door.
The verb behaves identically for all three and cannot tell them apart: a human exploring, the orchestrator self-directed, or a consumer's question relayed.
No caller gets a special path or a special field.


The gate — ① ② ③, shallowest first
------------------------------------

```
  ① QA SCAN     grep the QA/ files. already answered?

                READ THE STATE LINE FIRST — before asking whether it answers you.
                  answered           → return the path.                          ~0
                  working            → SOMEONE IS ALREADY ON IT. return the path
                                       + "in progress since <started>". run NOTHING.
                  working, EXPIRED   → the run died. RESTART it (below).
                  superseded-by: X   → follow the chain. return the LIVE answer.

  ② DIGEST      no QA file, but results/ already hold the answer
                → write the QA file from what is there. no code runs.             cheap

  ③ RUN IT      neither → run the lifecycle at the shallowest depth (below),
                then complete the QA file at Report.                              agent

  🚫 REFUSE     not this layer's question, or not this job's
                → return the reason + the re-route. the CALLER re-routes.
```

⛔ ORDER IS LOAD-BEARING.
A `working` file's `## Answer` is EMPTY BY CONSTRUCTION.
Test it for "does it answer me?" and it always fails — so you dispatch a second run of work already underway.
That is the exact duplicate this mechanism exists to prevent.
Match a `working` file on its `# Q —` line, never its `## Answer`.

⛔ THE ANSWER TEST — a hit counts ONLY if the QA file LITERALLY ANSWERS THIS QUESTION.
Read the file.
Topic similarity is not an answer.
"Profile the WellDoc cohorts" and "scan WellDoc for cycle columns" look like the same topic and share ZERO evidence.
A near-miss is NOT a hit — it falls through to ② or ③.
(This applies to an `answered` file.
A `working` file is matched on its question, per the ordering above.)

At ②, write the QA file complete and in ONE write: `state: answered`.
Nothing to race, so nothing to start.

At 🚫, never answer a discovery-shaped question by inventing a task.
A REFUSE is a COMPLETE answer, never a failure.
It writes no QA file and produces no `working` state — there is nothing to clean up.


How deep (③) — the depth IS the entry point into Plan → Build → Execute → Report
---------------------------------------------------------------------------------

```
  depth 0  READ         results/ already hold it       → enter at REPORT. nothing runs.
  depth 1  NEW RUN      existing script, new config    → enter at EXECUTE
                          + configs/<new>.yaml  + <task>/runs/  (nested job: <task>/config/<new>.yaml + <task>/runs/<new>.sh)
  depth 2  NEW SCRIPT   in scope, nothing computes it  → enter at BUILD
                          + <new>.py  + workflow/plan-script-<new>.yaml
  depth 3  NEW FOLDER   outside this folder's scope    → full lifecycle, sibling folder
```

**Depth 1** reuses the code and only adds a config and a run.
Never edit an old run.

**Depth 3** mints a new job — NAME IT TO MATCH ITS SIBLINGS.
Read the existing jobs in the group and follow THEIR convention: `01_foo` where they number, `B7_foo` where they letter.
Do not impose a scheme.

**Scope test (2 vs 3)** — does the question fit THIS job's `workflow/plan.yaml` IPO, same inputs and same process family?
Yes → new script.
No → new folder.

The caller never learns which depth you used.
It hands over a question and gets back a path.
The depth is this layer's private business.


Starting the QA file (③ only)
------------------------------

Write it BEFORE the run, with `state: working`.
That is what tells the next caller someone is already on it.

```bash
QA_WORKING_TTL_HOURS=24
QA_FILE="$OUTPUT_ROOT/QA/<n>-<slug>.md"    # job, or the declared store
mkdir -p "$(dirname "$QA_FILE")"

if ( set -C; cat > "$QA_FILE" ) 2>/dev/null <<EOF
# Q — <the question, restated in your own words>
- state:   working
- started: $(date +%Y-%m-%dT%H:%M)
- by:      <run id | agent | human>

## Answer

## Caveats

## Not-done
EOF
then
  : # WON  → run ③. complete this file at Report.
else
  : # LOST → it already exists. go back to ① ONCE, read the winner's state line,
    #        return its path. run nothing. do not loop.
fi
```

`set -C` IS the whole race guard.
No lock dir, no lease server, no ledger.
A same-instant collision on different slugs is possible and harmless — ① finds both.


When a run dies
----------------

```bash
started=$(sed -n 's/^- started:[[:space:]]*//p' "$QA_FILE" | head -1)
[ -n "$started" ] || echo "invalid: a working file with no started: can NEVER expire"
age_h=$(( ( $(date +%s) - $(date -d "$started" +%s) ) / 3600 ))
[ "$age_h" -ge "$QA_WORKING_TTL_HOURS" ] && echo "expired → RESTART"
```

RESTART = overwrite the state line with a fresh `started:`, record the abandoned attempt in `## Not-done`, then run ③.

`started:` is MANDATORY on a `working` file.
Without it the file can never expire, and it blocks every future caller forever.
The checker fails it.


What is frozen, what moves
---------------------------

```
  ACCRETES (add-only)   QA files · configs/ · runs/ · scripts · jobs
  FROZEN                past results/ · a QA file's BODY, once written
  MUTABLE               a QA file's `state:` line — the ONE mutable field
                        plan.yaml — this layer's own
```

You write a QA file exactly twice: `working` at ③, then `answered` at Report.
A third time only, to append `superseded-by:` when a later run changes the answer.

ONE WRITER — this layer, every time.
A consumer never creates, starts, completes, or edits a QA file.
A consumer-planted `working` file is the retired `_ASK/` stub in a new costume, and it is forbidden.

⛔ A consumer that finds a stale or unfinished target does NOT "fix" the QA file.
It re-points its own section, or it commissions fresh work.
Only the owner ever appends `superseded-by:` — the pen never crosses.

⛔ NEVER leave `## Answer` empty on a file that says `state: answered`.
That is a LYING RECEIPT, and the checker fails it.
`## Answer` is empty only while `state: working`, by construction.


When a QA file may exist
-------------------------

Exactly three reasons, and there is no fourth.

```
  commissioned    a caller asked a question. you answered it.
  digest-only     the facts were already in results/, but nobody had written them readably.
  your own        you judged a finding worth digesting, with no question pending.
```

⛔ A `QA/` folder that mirrors every result file is NOISE, not an index.
If none of the three reasons applies, do not write the file.


A QA file carries NO consumer vocabulary
-----------------------------------------

No claim ids (C6, H2).
No "claims-stage".
No "the paper".
No probe ids.

You have never seen a paper, so you cannot honestly write one down.
State each finding as a fact on its own terms — readable by anyone, with no reference to who asked or why.

The checker lints this, and it exists because of a real file still on disk.
`tasks/A03_welldoc_cycle_check/result.md` opens with *"to answer two claims-stage questions: C6 … C7 …"*.
A consumer session did the work inline, with the stake in its context.
The evidence came back paper-shaped and effectively single-use.


Return
-------

```
qa_file:     <path>                       the answer, or the in-progress file
bank:        <the $OUTPUT_ROOT this call addressed>
state:       answered | working | refused
path_taken:  1-scan | 2-digest | 3-run(depth N) | refuse
note:        one line
```

`bank:` is not decoration. A caller that supplied `RESULT_STORE` compares it
against the returned path and FAILS the card when the answer landed elsewhere
(`haipipe-probe` §③ R19). Without the field the caller can still compare
prefixes, but it cannot tell "I addressed the store and wrote there" apart from
"I never saw the store and wrote task-local" — and those need different fixes.

On `working`, the note reads "in progress since <started>".
On refuse, it carries the reason and the re-route.
If the incoming question carried vocabulary you stripped, say so.
