Function: qa — the discovery layer's question door
==================================================

**One question in, one QA file out.** `qa` takes a question in GENERAL language
and returns a path to `discoveries/<leaf>/QA/<n>-<slug>.md`. It never learns WHO
asks or WHY. It is probe-UNAWARE, and that is the whole point.

Constitution: `probe/haipipe-probe/SKILL.md` (v8.2.0 — R2 / R9 / R10 / R11 / R15 /
R17 / R18 + R19 the claim · R20 supersession · R21 the three readers + the two LAWS).
It holds the CANONICAL strings (the field names, the state values, `QA_CLAIM_TTL_HOURS`,
the timestamp format, the `set -C` idiom). Where this file and that one disagree, that
one wins.

The task twin is `task/haipipe-task/fn/qa.md`. Task and discovery are BOTH
executors — same shape, same rules (JL-10). Only what Execute *does* differs. Every
FIELD NAME, state value, TTL constant and flag spelling in this file is
CHARACTER-IDENTICAL to the task twin's. They drifted before. Do not let them.

💀 The old probe-aware `asks` verb is DELETED. It read `_ASK/PPNN_*.md` stubs and
resolved PP ids; it knew the probe existed. `qa` knows nothing about probes,
papers, claims, or stakes — and it is reachable by anyone.


Usage
------

```
/haipipe-discovery qa "<question>"                answer it from ANY discovery leaf
/haipipe-discovery qa "<question>" <leaf>         answer it from THIS leaf
/haipipe-discovery qa "<question>" --check-only   detect ①/② only, execute NOTHING

  <question>  ONE question, GENERAL language. NO PP id. NO paper reference. NO stake.
              ("Does published work already establish X?" — not "does X rescue C6?")
  <leaf>      a discovery-folder: discoveries/<GROUP>/<NN>_<topic>/
              omitted -> scan every leaf, then decide where the answer belongs.
```

`--check-only` runs ① and ② DETECTION and STOPS: it reports which path the question
would take (① a QA file already answers it — or one is already `working` on it · ② the
leaf's artifacts answer it but no digest exists · ③ real work is needed) and writes
nothing at all — no terminal, no digest, and NO CLAIM. (This is how a probe's MATCH step
probes the bank without spending. MATCH is defined as a FREE detection pass, so a qa call
that fell through to ③ there would spawn an unbudgeted lifecycle run, plant a claim, and
write into the bank during a step whose whole purpose was to cost nothing.) The task twin
spells this flag IDENTICALLY. It must stay that way: two dialects of one verb means the
probe's MATCH has two dialects.

⚠️ A question arriving with a PP id, a claim id (C\d / H\d), a hypothesis, or the
words "the paper" / "claims-stage" in it is a LAW-2 violation on the way in. Do not
launder it: STRIP the consumer vocabulary, restate the question in general language,
and answer THAT. If stripping it leaves nothing answerable, REFUSE and say so.


THREE CALLERS, one door
------------------------

```
📄 the PROBE's DISPATCH     via Agent(haipipe-discovery-orchestrator-agent).
                            The agent's clean context IS the wall: it receives one
                            commission block, verbatim, and nothing else.
🧑 a HUMAN, directly        the everyday "go explore this direction" verb (R18).
                            "what does the literature say about Y?" -> QA/3-….md
🤖 the ORCHESTRATOR itself  self-directed answerability work (R17): it picks a
                            worthwhile direction and explores it, no question pending.
```

All three write the SAME artifact through the SAME gate. None of them is special.

⚠️ `qa` is the discovery session's SIDE door. The PRIMARY mode (R17) is autonomous
Plan → Build(opt) → Execute → Report on the layer's own research topics — no
question, no ask, nobody asking. The bank grows by itself; `qa` is how a question
finds what the bank already knows.


A QA file is a TICKET that becomes a RECEIPT
---------------------------------------------

A QA file carries exactly ONE MUTABLE FIELD — the **state line**. Everything below the
state line is written once and never touched again.

```markdown
# Q — <the question, restated by the executor in its own words>
- state:   working | answered | superseded-by: QA/<m>-<slug>.md
- started: 2026-07-14T09:12          ← MANDATORY when state: working
- by:      <run id | agent | human>  ← optional provenance

## Answer     EMPTY while state: working. Filled at REPORT.
## Caveats
## Not-done
```

THE THREE FIELDS, canonical spelling (lowercase, colon, no underscores, in this order):

```
  state:      MANDATORY, always. The ONLY mutable field in the file.
              Exactly three values — working · answered · superseded-by: QA/<m>-<slug>.md
              There is NO `pending`, NO `in-progress`, NO `claimed`, NO `done`.
  started:    MANDATORY when `state: working`. Optional/absent otherwise.
              Format YYYY-MM-DDTHH:MM — minute precision, local time, no seconds, no
              timezone suffix. Produced by: date +%Y-%m-%dT%H:%M
  by:         OPTIONAL provenance (run id | agent | human).
```

`superseded-by:` is APPENDED to the state line of an `answered` file; it does NOT replace
`answered`. The composed form on disk is:

```
  - state:   answered · superseded-by: QA/2-cycle.md
```

Grep/parse form (the checker and both qa verbs use exactly this):

```bash
sed -n 's/^- state:[[:space:]]*//p'   <file> | head -1
sed -n 's/^- started:[[:space:]]*//p' <file> | head -1
```

**⚠️ THE LOAD-BEARING INVARIANT IS *ONE WRITER*, NOT *WRITE-ONCE*.**

```
   ✅ ONE WRITER — the EXECUTOR, and nobody else, EVER
   ═══════════════════════════════════════════════════════════════════════════
   the EXECUTOR writes the file TWICE, in its OWN folder:
     ① at the ③ DECISION  → the CLAIM      (state: working + started:)
     ② at REPORT          → the COMPLETION (state: answered + the ## Answer body)
   Two writes by the SAME OWNER is fine. Nothing is shared. Nothing is planted.

   ⛔ A CONSUMER (probe / paper / application) MUST NEVER create, claim, edit, complete,
      or supersede a QA file. Not the state line. Not the body. Not "just this once".
      A consumer-planted `working` file is the retired `_ASK/` stub wearing a `QA/`
      costume, and it is FORBIDDEN.
```

"Write-once was never the real rule. ONE WRITER was."

THE GATE-PATH WRITE CONTRACT — which path writes what, and when:

```
  ① QA SCAN   writes NOTHING. Returns the path. On `working`: return the path +
              "in progress since <started>", and DO NOT RE-RUN.
  ② DIGEST    writes ONCE, COMPLETE, `state: answered`. No claim — the facts are already
              in the leaf's artifacts, zero searching happens, the write is instant.
              There is nothing to race.
  ③ LIFECYCLE writes TWICE: the CLAIM (`state: working` + `started:` + an EMPTY
              `## Answer`) at the moment it decides to run, then the COMPLETION
              (`state: answered` + the `## Answer` body) at REPORT.
  🚫 REFUSE   writes NO QA file — and RELEASES any claim it made.

  ⇒ ONLY path ③ ever produces a `working` file, and only transiently.
```


The gate — ① → ② → ③, cheapest first
-------------------------------------

```
   ┌─ ① QA SCAN     grep the readable corpus:
   │                  <leaf>/QA/*.md          (leaf given)
   │                  discoveries/**/QA/*.md  (no leaf given)
   │                READ THE STATE LINE FIRST — BEFORE asking "does it answer me?".
   │                (A `working` file's ## Answer is EMPTY BY CONSTRUCTION: test it for
   │                 an answer and you get a guaranteed miss, and you re-run the job
   │                 someone is already running. Match a `working` file on its `# Q —`.)
   │                  state: answered   -> apply R14 (match on the ANSWER, never the
   │                                       topic). A hit RETURNS the QA file PATH       ~0
   │                  state: working    -> DO NOT RE-RUN. Return the path +
   │                                       "in progress since <started>"               ~0
   │                  state: working, EXPIRED past QA_CLAIM_TTL_HOURS
   │                                    -> 🧟 ZOMBIE. RECLAIM it (below).
   │                  superseded-by: X  -> FOLLOW the chain; return the LIVE answer     ~0
   │                  NO state line     -> MALFORMED (state: is MANDATORY). REPAIR my
   │                                       own file: tag it `answered` if the Answer has
   │                                       a body, else RECLAIM it as a zombie.
   │
   ├─ ② DIGEST      the leaf's OWN artifacts already answer it, but no readable
   │                digest exists:
   │                  sources.md · notes.md · verdict.md · landscape.md · ideas.md
   │                -> WRITE discoveries/<leaf>/QA/<n>-<slug>.md from those artifacts
   │                   ONCE, COMPLETE, `state: answered`. No claim.                  cheap
   │                   NO searching. NO new sources. NO new judgment.
   │                   Read what is on disk, write the digest, stop.
   │
   └─ ③ LIFECYCLE   neither -> ⚑ CLAIM FIRST (the noclobber idiom, below), then run the
         │          discovery lifecycle at the SHALLOWEST depth that answers the question
         │          (the depth ladder below), and COMPLETE the same file at Report.
         │
         └─ 🚫 REFUSE — the question is not discovery-shaped, or not this leaf's.
                  Return the reason + the re-route. RELEASE any claim. The CALLER
                  re-routes; never answer a task-shaped question by inventing a discovery.
```


Step 1 — ① QA SCAN, and the state line
---------------------------------------

⚠️ **READ THE STATE LINE FIRST — BEFORE you ask whether the file answers the question.** The
ORDER IS LOAD-BEARING, and getting it backwards re-opens the exact hole this mechanism closes.
A `working` file's `## Answer` is EMPTY BY CONSTRUCTION (that is what `working` MEANS — the
CLAIM idiom writes it empty on purpose). Apply the literally-answers test (R14) to it and it is
a guaranteed miss, you fall through to ③, you allocate a NEW `<n>`, `set -C` never fires because
the path differs — and you run THE SAME EXPENSIVE LIFECYCLE A SECOND TIME, alongside the one
already in flight. That is the duplicate run, executed by following the rules.

```
  state: answered           -> NOW apply R14 (match on the ANSWER, never the topic; READ the
                               file). A hit returns the path. Cost ~0. Search nothing,
                               write nothing.

  state: working            -> MATCH IT ON ITS `# Q —` LINE, NOT ON ITS ANSWER. Does that
    (started: within TTL)      restated question BE my question? If YES: ⏳ SOMEONE IS ALREADY
                               ON IT. Return the path + "in progress since <started>". DO NOT
                               RE-RUN. DO NOT CLAIM. DO NOT TOUCH THE FILE. An expensive
                               lifecycle run is SAVED. Cost ~0. If NO (a different question):
                               it is not a hit — fall through to ② or ③ as normal.

  state: working            -> 🧟 ZOMBIE CLAIM. The run that made it is dead.
    (started: past TTL)        RECLAIM it (Step 3b).

  superseded-by: QA/<m>-…   -> the answer CHANGED. FOLLOW the chain to the live file
                               (and keep following — a chain may be longer than one hop).
                               Return the LIVE answer's path, never the superseded one.
                               THEN apply R14 to the LIVE file.

  NO state line             -> MALFORMED. `state:` is MANDATORY (checker: qa-no-state), and
                               this is MY OWN LAYER'S file — so REPAIR it, in place:
                                 · `## Answer` has a body  -> add `- state:   answered`
                                 · `## Answer` is EMPTY    -> it is an untagged claim of
                                   unknown age. Treat it as a ZOMBIE and RECLAIM it (Step 3b).
                               A consumer may NEVER do this. Only the owner.
```


Step 3a — ⚑ THE CLAIM (write it BEFORE the lifecycle runs)
-----------------------------------------------------------

The moment ③ is decided — BEFORE Plan, BEFORE any search — write the claim. It says to
every future reader: *someone is already on this; do not duplicate the work.*

Allocate `<n>` first (the fail-closed rule below), then create the file with `set -C`
(noclobber). The `set -C` IS the race guard, and it is the WHOLE race guard:

```bash
QA_CLAIM_TTL_HOURS=24                          # the claim TTL — the named constant
QA_FILE="<leaf>/QA/<n>-<slug>.md"
mkdir -p "$(dirname "$QA_FILE")"

if ( set -C; cat > "$QA_FILE" ) 2>/dev/null <<EOF
# Q — <the question, restated by the executor in its own words>
- state:   working
- started: $(date +%Y-%m-%dT%H:%M)
- by:      <run id | agent | human>

## Answer

## Caveats

## Not-done
EOF
then
  : # CLAIM WON  -> proceed with gate ③; complete this file at REPORT.
else
  : # CLAIM LOST -> the file already exists. Re-run gate ① QA SCAN and DEFER. Run nothing.
fi
```

WHAT THE LOSER DOES — and it must NOT loop:

```
  The loser does not retry, does not pick another <n>, and does not run the lifecycle.
  It goes back to ① QA SCAN ONCE, reads the winner's state line, and RETURNS:

    winner is `working`   → return the winner's path + "in progress since <started>".
                            status: ok · gate: 1 · Cost ~0. Done.
    winner is `answered`  → return the winner's path. Done.

  One re-scan. One return. A loser that loops back into ③ is the duplicate run this whole
  mechanism exists to prevent.
```

`set -C` shrinks the race window from THE WHOLE RUN to microseconds. A residual
same-instant / DIFFERENT-slug collision is still possible (`QA/3-foo.md` and `QA/3-bar.md`
for one question) and is NON-FATAL — ① SCAN finds both files. **DO NOT over-engineer past
this: no lock dirs, no lease servers, no ledgers, no flock.** They are all retired
machinery in a new hat.

At Report, COMPLETE the same file — the second and last write by its one owner:

```
  - state:   answered        (rewrite the state line; `started:` may stay or go)
  ## Answer  ← the body, now filled. See "The QA file" below.
```

If the run DIES or the question is REFUSED after a claim was made, RELEASE the claim:
delete the claim file (it has an empty `## Answer` — it is a ticket, not evidence). A
claim you cannot complete must not be left standing; if it is left standing anyway, the
TTL is the backstop, not the plan.


Step 3b — 🧟 RECLAIM (the zombie path)
---------------------------------------

A crashed run leaves `state: working` forever, and every future reader defers to a run that
is dead. THE CLAIM MUST EXPIRE. This is the staleness test the RECLAIM path and the checker
SHARE — same constant, same arithmetic:

```bash
QA_CLAIM_TTL_HOURS=24                          # the claim TTL — the named constant

started=$(sed -n 's/^- started:[[:space:]]*//p' "$QA_FILE" | head -1)
[ -n "$started" ] || echo "FAIL qa-working-no-started"
age_h=$(( ( $(date +%s) - $(date -d "$started" +%s) ) / 3600 ))
[ "$age_h" -ge "$QA_CLAIM_TTL_HOURS" ] && echo "STALE — reclaimable (checker: qa-working-expired)"
```

```
  QA_CLAIM_TTL_HOURS = 24     the NAMED CONSTANT. Tune it HERE and in the constitution.
                              NEVER hard-code the literal 24 anywhere else — reference
                              the name. The checker and the OTHER executor twin read the
                              same name and the same value.
```

To RECLAIM a stale `working` file (this is an in-place rewrite of a file THIS LAYER owns —
not a mutation of a frozen body; the body is still empty):

```
  1. Rewrite the state line with a FRESH started: (and your own by:).
       - state:   working
       - started: <now, via date +%Y-%m-%dT%H:%M>
  2. Record the abandoned attempt in `## Not-done`:
       - Abandoned attempt: claimed <old started>, never completed (claim expired past
         QA_CLAIM_TTL_HOURS). Re-claimed <new started>.
  3. Proceed with gate ③ and complete the file at REPORT as normal — including
     carrying that `## Not-done` line into the completed file. It is honest history.
```

⛔ A `working` file with NO `started:` is an INVALID claim — it can never expire, so it is a
zombie by construction. Do not defer to it. Treat it as STALE and RECLAIM it (adding the
`started:` the original writer omitted). The checker FAILs it: `qa-working-no-started`.


SUPERSESSION — when a later run CHANGES the answer
---------------------------------------------------

A QA file's BODY is never edited. The state line is the ONE mutable field, and only its own
owner — this layer — ever edits it.

```
   day 1    QA/1-cycle.md   - state: answered      "no prior art for X"
   day 40   a re-run finds a 2026 paper. The truth CHANGED.
            the EXECUTOR writes  QA/2-cycle.md   - state: answered   "prior art exists —
                                                                      Zhang et al. 2026"
            and APPENDS to       QA/1-cycle.md   - state:   answered · superseded-by: QA/2-cycle.md
                                                                       ▲ the ONLY edit ever
                                                                         permitted to a
                                                                         frozen file
```

```
  MUTABLE   the `state:` line — and ONLY that line, and ONLY by the file's OWN OWNER.
            Two edits are legal in a file's whole life:
              working → answered            (the completion, at REPORT)
              answered → + superseded-by:   (the pointer, when a later run changes the truth)
  FROZEN    `# Q —` · `## Answer` · `## Caveats` · `## Not-done` — forever, once written.
  ⛔ A CONSUMER writes NEITHER. A consumer that finds a stale target does not "fix" the QA
     file — it re-points its OWN section's target: at the live one.
```

Supersede ONLY when the answer CHANGED. A new question, a deeper cut, or a different source
base is NOT a supersession — it is simply `QA/<n+1>-<slug>.md`, and the old file stays live.


The depth ladder (③) — the executor picks, the caller never learns which
------------------------------------------------------------------------

Task's ladder is read / new run / new script / new leaf. Discovery's is the same
shape, but a discovery-folder holds ONE execution per topic, so the rungs differ:

```
   a NEW question arrives at the discovery bank
   ──────────────────────────────────────────────────────────────────────────
   depth 0  📖 READ         an existing leaf's terminal already holds the answer
                            -> enter at Report: write QA/<n>-<slug>.md · nothing runs
                            (this IS path ②, reached from ③'s side — so it writes ONCE,
                             COMPLETE, `state: answered`. No claim is needed.)

   depth 1  ♻️ ENRICH       the question is ON-TOPIC for an existing leaf's
                            discovery.yaml `question:`, but the evidence is thin
                            -> the orchestrator's ENRICH mode: verification flips +
                               appended S## sources into the SAME sources.md,
                               coverage declaration updated
                            -> then write QA/<n+1>-<slug>.md
                            never re-opens the lifecycle, never rewrites the terminal

   depth 2  🌱 NEW FOLDER   the question is OFF-TOPIC for every existing leaf, but
                            fits an existing purpose group (S / L / P)
                            -> full Plan → Build(opt) → Execute → Report in a NEW
                               <NN>_<topic>/ inside that group (next free NN)
                            -> QA file at Report

   depth 3  🌳 NEW GROUP    no existing group carries the purpose
                            -> open the group (S source base / L landscape /
                               P proof-prior-art), then depth 2 inside it
   ──────────────────────────────────────────────────────────────────────────
   🚫 REFUSE                wrong executor / wrong shape -> the caller re-routes

   Depths 1, 2 and 3 all do real work, so all three CLAIM FIRST (Step 3a). Depth 0 runs
   nothing — it is the digest, and it writes once, complete.

   scope test (depth 1 vs 2): does the question fit THIS leaf's discovery.yaml
   `question:` — same topic, same source base?   yes -> ENRICH.   no -> new folder.
   (Off-topic deltas forced into an existing leaf are already REJECTED by the
    orchestrator's ENRICH guard. That guard is this test, enforced.)

   ACCRETES (add-only):  QA files · appended S## sources · folders · groups
   FROZEN (never edit):  a QA file's BODY · a reported terminal file
   MUTABLE (one owner):  a QA file's `state:` LINE — and nothing else in the file.
                         Only this layer ever edits it. Two edits in a file's life:
                         working → answered, and answered → + superseded-by:
   LIVING (one writer):  discovery.yaml — the layer's own, may evolve normally
```

Pick the TYPE for a depth-2/3 folder from the question's shape (the standard
routing — `haipipe-discovery/SKILL.md` "Routing"):

```
   "what exists / what has been published?"      -> Search  (find + read)
   "does this claim already exist / hold up?"    -> Review, role prior_art_check
                                                   | counterevidence  -> verdict.md
   "map the field / what are the baselines?"     -> Review, role landscape_review
                                                   | benchmark_landscape -> landscape.md
   "what new angles are there / is this new?"    -> Idea, role idea_generation
                                                   | novelty_check
```

⚠️ A Review-type discovery's `verdict.md` is the layer's OWN terminal file. It is
NOT the retired probe "Verdict" (which is dead, R7). It survives, unchanged, and a
QA file may anchor straight into it: `[→ verdict.md#Evidence]`.


REFUSE — when this is not our question
---------------------------------------

```
🚫 task-shaped     needs code, a run, a config, a metric on OUR OWN data
                   ("what is the val MAE of the 4-layer model on the id split?")
                   -> re-route: /haipipe-task qa "<question>"
🚫 consumer-shaped it is a claim judgment, not an evidence question
                   ("is C6 supported?") -> not ours, and not answerable here.
                   Claim status lives in the consumer's own 1-claims.md.
🚫 wrong leaf      discovery-shaped, but this leaf's discovery.yaml `question:` is
                   a different topic and no depth-1 ENRICH is honest
                   -> name the right leaf (or "no leaf — needs a new folder") and
                      let the caller re-dispatch.
```

A REFUSE writes NO QA file — and if a claim was already made before the refusal became
clear, it RELEASES it (delete the claim file; its `## Answer` is empty, so nothing of value
is lost). Never leave a `working` file behind a refusal: it tells every future reader that
work is underway when nothing is.

A REFUSE is a legitimate, cheap outcome. Return the reason + the re-route target.
Never scaffold a discovery folder to avoid saying no.


The QA file — path, anatomy, rules
-----------------------------------

```
   PATH   discoveries/<GROUP>/<NN>_<topic>/QA/<n>-<slug>.md

   <n>    creation order inside THIS leaf. THE NUMBERING IS THE INDEX —
          `ls QA/` IS the index. No INDEX file until a leaf's QA count earns one.
   <slug> a slug and NOTHING ELSE. A PP id in a bank filename is R2 broken.
   WRITER the EXECUTOR (this layer) — the CLAIM at the ③ decision, the COMPLETION at
          Report. ONE WRITER. Nobody else writes this file, ever.
   A later question ADDS QA/<n+1>-<slug>.md. A QA file's BODY is never edited.
```

**ALLOCATING `<n>` — FAIL-CLOSED, IMMEDIATELY BEFORE THE WRITE.** Parallel orchestrators are the
DESIGNED dispatch mode (a probe batches independent questions, backgrounded), and two of them can
land on the SAME leaf at once. If both `ls QA/` early, both see 2 files, both compute n=3, and
both write — and if they also picked the SAME SLUG the second Write silently CLOBBERS an answer
that was never supposed to be editable. Allocating late + `set -C` is what turns that clobber
into a DETECTED loss.

The residual case — same `<n>`, DIFFERENT slug (`QA/3-foo.md` + `QA/3-bar.md`) — is **NON-FATAL
BY RULING** and is NOT a reviewer REVISE: `ls QA/` still indexes both files, and ① SCAN finds
both. The reviewer's FILENAME check ("no gap, no reuse") carries this exemption EXPLICITLY.
Never "fix" it by renaming a QA file — the body is frozen, and a rename orphans a live claim.

```
  n = (highest existing <n> under <leaf>/QA/) + 1     ← computed at WRITE time, not earlier
  if <n>-<slug>.md already exists → DO NOT overwrite. Re-scan, take the next free n.
```

On path ③ the WRITE that matters for allocation is the CLAIM: `<n>` is allocated
immediately before the `set -C` create, and the noclobber guard is what makes "already
exists" a DETECTED loss rather than a silent clobber. The completion at Report rewrites the
file this run already owns — it never re-allocates `<n>`.
(The task twin states these rules identically — the two banks must not drift.)

```markdown
# Q — <the question, restated by the executor in its own words, self-contained, general>
- state:   answered
- started: 2026-07-14T09:12
- by:      <run id | agent | human>

## Answer
<plain words — a reader who has never opened this folder must be able to act on it>
<every load-bearing statement carries an anchor into an artifact:>
  [→ sources.md#S02]  [→ verdict.md#Evidence]  [→ landscape.md#Gaps]  [→ notes.md]

## Caveats
- <what this does NOT establish — coverage gaps, unverified sources, scope limits>

## Not-done
- <what was asked but not resolved, and why>
```

The state line, then exactly those three sections. No markdown tables (house rule — this
is a discovery document). The `# Q` line must stand alone: a QA file that only makes sense
next to the question that caused it has failed.

⛔ NEVER leave `## Answer` empty on a file that says `state: answered`. That is a LYING
RECEIPT, and the checker FAILs it: `qa-answered-empty`. An empty `## Answer` is legal in
exactly one situation — the file is `state: working`.

**LAW 2 (bank surface).** A QA file carries NO consumer vocabulary: no `C\d`, no
`H\d`, no "claims-stage", no "the paper" meaning *someone's* paper. The precedent it
exists to prevent is on disk (`tasks/A03_welldoc_cycle_check/result.md`, "C6: … → NO").
Write the answer the way the NEXT reader — who has a different stake, or none —
needs it.

**R10 — the three reasons a QA file may exist** (there is no fourth):

```
   commissioned    🎯 a dispatch named it (the probe's DISPATCH, via the orchestrator)
   digest-only     ♻️ gate ② — the artifacts already answered; no code, no search
   executor's own  ✍️ this layer judged a finding worth digesting, incl. proactive
                      ANSWERABILITY WORK (R17): digests written so that future
                      questions are cheap, with no question pending
   ⛔ ABUSE GUARD  a QA/ that mirrors every source is noise, not an index.
```


How a QA file READS — for anyone, at any time
----------------------------------------------

The state line is not bookkeeping. It is what lets three different readers, days or weeks
apart, avoid three different mistakes:

```
   ① SCAN — a 2nd qa call        `state: working` -> DO NOT RE-RUN. Return the path +
      (this layer, days later)    "in progress since <started>". An expensive lifecycle
                                  run is SAVED. This is the duplicate-work fix.

   ② A CONSUMER'S MATCH           `state: working` -> the question is LIVE. It sets its OWN
      (a probe, a week later)     question section to `state: commissioned` and points its
                                  `target:` at that QA file. NO SECOND DISPATCH.
                                  ⛔ It does NOT touch the QA file. The pen never crosses
                                     the wall — this layer's file, this layer's pen.

   ③ A HUMAN                      `ls QA/` + the state line now reads as BOTH: what this
                                  leaf has ESTABLISHED, and what it is ESTABLISHING RIGHT
                                  NOW.
```

STATUS DERIVATION — read the STATE LINE, not mere existence:

```
   no QA file                              -> NOT ANSWERED
   QA file · state: working                -> IN PROGRESS (since <started>)
                                              — unless started: is older than
                                                QA_CLAIM_TTL_HOURS, in which case the claim
                                                is STALE and RECLAIMABLE
   QA file · state: answered               -> ANSWERED
   QA file · state: answered · superseded-by: X
                                           -> ANSWERED, but STALE — the LIVE answer is X
```

THE CHECKER'S TEETH (`check-probe-cards.sh` implements them; stated as LAW in the
constitution's PART 6). Five conditions, each a HARD FAIL:

```
   read-target-working       a consumer's question section at `state: read` whose target:
                             resolves to a QA file that is `state: working`
                             ⇒ it claims it read an UNFINISHED answer.
   read-target-superseded    a consumer's question section at `state: read` whose target:
                             resolves to a QA file carrying `superseded-by:`
                             ⇒ its reading is built on a STALE answer.
   qa-working-no-started     a `working` QA file with no `started:`  ⇒ an UNEXPIRABLE claim.
   qa-working-expired        a `working` QA file older than QA_CLAIM_TTL_HOURS ⇒ a ZOMBIE.
   qa-answered-empty         `state: answered` with an EMPTY `## Answer` ⇒ a LYING RECEIPT.
```

The last three are OURS: this layer writes the files that trip them. A claim with no
`started:`, a claim left standing past the TTL, and a receipt with nothing on it are all
defects of THIS verb, and they are now machine-detectable — which is the whole point.


Step-by-step
-------------

```
Step 0  Resolve the project root (nearest ancestor with tasks/ | discoveries/ |
        papers/ | applications/ | _haipipe/). Ambiguous -> ask.
        STRIP any consumer vocabulary from the question (see Usage). Restate it
        general. That restatement IS the question from here on.

Step 1  ① QA SCAN.  grep -ril "<key terms>" discoveries/**/QA/*.md  (or <leaf>/QA/).
        For every candidate: READ IT. A hit counts ONLY if the file literally
        answers THIS question (R14). Then READ ITS STATE LINE:
          answered        -> return the path. Done, ~0 cost.
          working (fresh) -> return the path + "in progress since <started>". DO NOT
                             RE-RUN, DO NOT CLAIM, DO NOT TOUCH THE FILE. Done, ~0 cost.
          working (stale) -> RECLAIM it (Step 3b), then continue into ③.
          superseded-by:  -> follow the chain, return the LIVE answer's path.

Step 2  ② DIGEST.  For the leaf(s) whose topic covers the question, read
        discovery.yaml + the terminal + sources.md/notes.md. Do they already
        answer it?
          yes -> write QA/<n>-<slug>.md from those artifacts — ONCE, COMPLETE,
                 `state: answered` — and return the path. Run NO searches. Add NO
                 sources. Make NO new judgment: a digest that reaches a conclusion the
                 terminal did not reach is not a digest, it is an unreviewed Execute.
                 No claim is written on this path — the write is instant.
          no  -> Step 3.

Step 3  ③ LIFECYCLE.  ⚑ CLAIM FIRST (Step 3a: allocate <n>, `set -C` create with
        `state: working` + `started:`). Lost the race? -> back to Step 1 ONCE and DEFER.
        Then choose the shallowest depth (ladder above) and run it:
          depth 1 -> ENRICH the leaf (orchestrator ENRICH mode; reviewer quick-pass
                     is mandatory — any ledger write gets a second pair of eyes)
          depth 2/3 -> scaffold the folder (+ group), then Plan → Build(opt) →
                     Execute → Report through the normal agents. The QUESTION is
                     the contract: it seeds discovery.yaml `question:` directly.
        Report COMPLETES the claimed QA file (`state: answered` + the `## Answer` body).
        Same reviewer gates as any other discovery — `qa` adds a door, it does not add
        an exemption.

Step 4  Return: { qa_file, qa_state, leaf, depth, type, terminal, status }.
        Notify nobody. Update nobody's files. Whoever asked harvests the path on
        their own schedule — that is what makes the bank reusable.
```

Return
-------

```
status:    ok | refused | blocked | failed
gate:      1 (qa scan) | 2 (digest) | 3 (lifecycle)
depth:     0 | 1 | 2 | 3        (gate 3 only; informational — the caller does not act on it)
qa_file:   discoveries/<leaf>/QA/<n>-<slug>.md   ← THE ANSWER. A path, always.
qa_state:  working | answered                    ← the state line of the file at qa_file.
           `working` means: SOMEONE IS ALREADY ON IT (in progress since <started>).
           The caller does NOT re-dispatch, and does NOT touch the file.
terminal:  sources.md / verdict.md / landscape.md / ideas.md   (when one was produced)
artifacts: [any folders / groups / appended sources created]
next:      suggested follow-up, or none
```


Boundary
---------

- `qa` writes ONLY inside the discovery leaf it works in: `discovery.yaml`,
  `sources.md` / `notes.md` / the terminal, `QA/<n>-<slug>.md`. Nothing else.
- It NEVER opens a paper folder, an application folder, a `1-probes/` file, or a
  `1-claims.md`. It NEVER writes upward. It NEVER learns who asked.
  (**LAW 1**, from the other side: a consumer session may not do bank work inline —
  and this layer may not do consumer work at all.)
- It NEVER edits another leaf's files, a reported terminal, or a QA file's BODY. The
  `state:` line of a QA file in THIS layer is the one exception, and only this layer
  edits it.
- `--check-only` writes nothing at all — no terminal, no digest, and NO CLAIM.
- A discovery still records nothing about who commissioned or consumed it. There is
  no `answers:` field, no `_ASK/`, no `_ANS/`, no PP id — anywhere under
  `discoveries/`. All of that is DELETED (R2).
