Function: qa
=============

The discovery layer's question door.
One question in general language goes in; a path to a QA file comes out.

The verb does not know who is asking, or why, and must not try to find out.
It never reads a paper.
It never resolves an id.
A consumer is just one caller among three.

⚠️ `qa` is this layer's SIDE door, not its engine.
The discovery session's PRIMARY mode is autonomous Plan → Build → Execute → Report, with no question pending at all.
Most questions should already have an answer sitting in the bank before anyone asks.

QA-file anatomy, the canonical field names and the state values live in `probe/haipipe-probe/SKILL.md` PART 3a.
Read them there — they are not restated here.
This file is the VERB.


Usage
------

```
/haipipe-discovery qa "<question>" [<discovery-folder>]     answer it
/haipipe-discovery qa "<question>" --check-only        detect only. write nothing. run nothing.
```

**`<question>`** — general language.
No paper reference, no id, no stake.
If one arrives anyway: strip it, restate the question on its own terms, and answer the restatement.
Say you stripped it, in the return.
Never act on it. Never launder it. Never refuse over it.

**`<discovery-folder>`** — optional, e.g. `discoveries/L03_cycle/01_prior_art/`.
Absent → scan every discovery-folder under the project's `discoveries/`.
A discovery-folder is ANY directory holding work: a `discovery.yaml`, `sources.md`, `verdict.md` or `landscape.md`.
⛔ NEVER filter by name.
Folder names vary across projects — detect by STRUCTURE, never by a pattern.
A name filter goes silently blind.

**`--check-only`** — the consumer's MATCH step calls this.
It is a FREE pass by definition.
It must never fall through to ③ and spawn an unbudgeted run.

THREE CALLERS, one door.
The verb behaves identically for all three and cannot tell them apart: a human exploring, the orchestrator self-directed, or a consumer's commission relayed.
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

  ② DIGEST      no QA file, but sources.md / verdict.md already hold the answer
                → write the QA file from what is there. no code runs.             cheap

  ③ RUN IT      neither → run the lifecycle at the shallowest depth (below),
                then complete the QA file at Report.                              agent

  🚫 REFUSE     not this layer's question, or not this discovery-folder's
                → return the reason + the re-route. the CALLER re-routes.
```

⛔ ORDER IS LOAD-BEARING.
A `working` file's `## Answer` is EMPTY BY CONSTRUCTION.
Test it for "does it answer me?" and it always fails — so you dispatch a second run of work already underway.
That is the exact duplicate this mechanism exists to prevent.
Match a `working` file on its `# Q —` line, never its `## Answer`.

⛔ THE ANSWER TEST — a hit counts ONLY if the QA file LITERALLY ANSWERS THIS QUESTION.
Read the file. Topic similarity is not an answer.
"Profile the WellDoc cohorts" and "scan WellDoc for cycle columns" look like the same topic and share ZERO evidence.
A near-miss is NOT a hit — it falls through to ② or ③.
(This applies to an `answered` file. A `working` file is matched on its question, per the ordering above.)

At ②, write the QA file complete and in ONE write: `state: answered`.
Nothing to race, so nothing to start.

At 🚫, never answer a task-shaped question by inventing a discovery.
A REFUSE is a COMPLETE answer, never a failure.
It writes no QA file and produces no `working` state — there is nothing to clean up.


How deep (③) — the depth IS the entry point into Plan → Build → Execute → Report
---------------------------------------------------------------------------------

```
  depth 0  READ         the terminal files already hold it → enter at REPORT. nothing runs.
  depth 1  ENRICH       same topic, a delta                → the orchestrator's ENRICH mode
  depth 2  NEW FOLDER   a different topic, same group      → full lifecycle, sibling folder
  depth 3  NEW GROUP    a different purpose entirely       → new group + folder
```

**Depth 1** appends to an existing topic — a few sources, a verification flip.
Never rewrite a landed verdict.

**Depth 2 and 3** mint a new folder — NAME IT TO MATCH ITS SIBLINGS.
Read the existing discovery-folders and follow THEIR convention.
Do not impose a scheme.

**Scope test (1 vs 2)** — is the question ON THIS TOPIC, inside the same `discovery.yaml` scope?
Yes → enrich.
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
QA_FILE="<discovery-folder>/QA/<n>-<slug>.md"
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
  ACCRETES (add-only)   QA files · sources · discovery-folders
  FROZEN                landed terminal files · a QA file's BODY, once written
  MUTABLE               a QA file's `state:` line — the ONE mutable field
                        discovery.yaml — this layer's own
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

The checker lints this, and it exists because of a real incident.
A discovery commissioned in a consumer's own vocabulary came back with its `sources.md` and `verdict.md` structured around that consumer's hypotheses.
Evidence meant to serve every future reader was effectively single-use.
Contaminating the bank costs more than the discovery did.


Return
-------

```
qa_file:     <path>                       the answer, or the in-progress file
state:       answered | working | refused
path_taken:  1-scan | 2-digest | 3-run(depth N) | refuse
note:        one line
```

On `working`, the note reads "in progress since <started>".
On refuse, it carries the reason and the re-route.
If the incoming question carried vocabulary you stripped, say so.
