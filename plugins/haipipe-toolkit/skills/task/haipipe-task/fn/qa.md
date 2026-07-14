Function: qa
=============

The task layer's QUESTION DOOR. One question in general language goes in; a path to a
readable answer file comes out.

  /haipipe-task qa "<question>" [<leaf>]

The verb does NOT know who is asking, or why, and it must not try to find out. It never
receives a paper reference, a claim id, or a stake, and if one arrives anyway it is
stripped and ignored — the question is answered on its own terms or REFUSED.

This verb REPLACES the deleted `asks` verb. `asks` read consumer-authored stubs and
resolved consumer ids; it was probe-AWARE and is dead. `qa` takes a question and returns
an answer: probe-UNAWARE by construction.

⚠️ `qa` is the task session's SIDE door, not its engine. The task session's PRIMARY mode
is autonomous Plan → Build → Execute → Report — no question pending, no ask, just the
project's own research. See "Two session modes" at the bottom.

Constitution: `probe/haipipe-probe/SKILL.md` (PART 3a — R19 the claim · R20 supersession ·
R21 the three readers). It holds the CANONICAL strings (the field names, the state values,
`QA_CLAIM_TTL_HOURS`, the timestamp format, the `set -C` idiom). Where this file and that
one disagree, that one wins. The discovery twin (`discovery/haipipe-discovery/fn/qa.md`)
must stay CHARACTER-IDENTICAL to this one on every one of those strings.


Usage
------

```
/haipipe-task qa "<question>"              answer it from anywhere in the bank
/haipipe-task qa "<question>" <leaf>       answer it inside ONE named task-folder
/haipipe-task qa "<question>" --check-only detect ①/② only, execute NOTHING

<question>   ONE question, GENERAL language, self-contained.
             ✅ "Do any WellDoc tables carry a menstrual/cycle column?"
             ❌ "Does C6 survive?"   ❌ "Scan for the cycle column so H2 lives."

<leaf>       a task-folder path (tasks/<group>/<NN>_<name>/). Optional.
             Absent → scan every leaf under the project's tasks/.

--check-only runs ① and ② DETECTION and STOPS: it reports which path the question
             WOULD take (① a QA file already answers it — or one is already `working`
             on it · ② results/ answer it but no digest exists · ③ real work is needed)
             and executes nothing, writes nothing at all — no results, no digest, and
             NO CLAIM. This is the door the probe's MATCH step calls — MATCH is defined
             as a FREE detection pass (T2: 1 grep + 1 read), so a qa call that fell
             through to ③ there would silently spawn an unbudgeted P-B-E-R run, plant a
             claim, and write into the bank during a step whose whole purpose was to cost
             nothing. The discovery twin spells this flag IDENTICALLY. It must stay that
             way: two dialects of one verb means the probe's MATCH has two dialects.
```

THREE CALLERS, one door — the verb behaves IDENTICALLY for all three, and cannot tell
them apart:

```
  🧑 a HUMAN, steering an exploration        "what about the female subset?"
  🤖 the ORCHESTRATOR, SELF-DIRECTED         answerability work, no question pending
  📄 a COMMISSION relayed by the orchestrator a consumer's question, handed over verbatim
                                             with no context attached
```

A consumer is just one caller. It gets no special path, no special field, no special
folder.


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
              in results/, zero code runs, the write is instant. There is nothing to race.
  ③ P-B-E-R   writes TWICE: the CLAIM (`state: working` + `started:` + an EMPTY
              `## Answer`) at the moment it decides to run, then the COMPLETION
              (`state: answered` + the `## Answer` body) at REPORT.
  🚫 REFUSE   writes NO QA file — and RELEASES any claim it made.

  ⇒ ONLY path ③ ever produces a `working` file, and only transiently.
```


The gate — ① ② ③, in order, shallowest first
---------------------------------------------

```
  ┌─ ① QA SCAN     grep <leaf>/QA/*.md   (or every leaf, if none was named)
  │                READ THE STATE LINE FIRST — BEFORE asking "does it answer me?".
  │                (A `working` file's ## Answer is EMPTY BY CONSTRUCTION: test it for
  │                 an answer and you get a guaranteed miss, and you re-run the job
  │                 someone is already running. Match a `working` file on its `# Q —`.)
  │                  state: answered   → return the QA file PATH                     ~0
  │                  state: working    → DO NOT RE-RUN. Return the path +
  │                                      "in progress since <started>"               ~0
  │                  state: working, EXPIRED past QA_CLAIM_TTL_HOURS
  │                                    → 🧟 ZOMBIE. RECLAIM it (below).
  │                  superseded-by: X  → FOLLOW the chain; return the LIVE answer     ~0
  │                  NO state line     → MALFORMED (state: is MANDATORY). REPAIR my
  │                                      own file: tag it `answered` if the Answer has
  │                                      a body, else RECLAIM it as a zombie.
  │
  ├─ ② DIGEST      results/ already answer it, but no readable digest exists?
  │                → write QA/<n>-<slug>.md FROM THE EXISTING ARTIFACTS            cheap
  │                  ONCE, COMPLETE, `state: answered`. NO code runs. No claim.
  │
  └─ ③ P-B-E-R     neither → ⚑ CLAIM FIRST (the noclobber idiom, below), then run the
        │          lifecycle at the SHALLOWEST depth that answers it (the depth ladder
        │          below), and COMPLETE the same file at REPORT.
        │
        └─ 🚫 REFUSE — out of scope for the TASK layer or for THIS leaf.
                 Say so plainly and stop. RELEASE any claim. The caller re-routes.

  --check-only     run ① and ② DETECTION, then STOP. Report which path the question
                   would take. Execute nothing. Write nothing — including NO CLAIM.
                   Never fall through to ③.
```

Step 1 — ① QA SCAN.

```
  leaf given:   grep -il "<key terms>" <leaf>/QA/*.md
  no leaf:      grep -rils "<key terms>" tasks/**/QA/*.md
```

⚠️ **READ THE STATE LINE FIRST — BEFORE you ask whether the file answers the question.** The
ORDER IS LOAD-BEARING, and getting it backwards re-opens the exact hole this mechanism closes.
A `working` file's `## Answer` is EMPTY BY CONSTRUCTION (that is what `working` MEANS — the
CLAIM idiom writes it empty on purpose). Apply the literally-answers test to it and it is a
guaranteed miss, you fall through to ③, you allocate a NEW `<n>`, `set -C` never fires because
the path differs — and you run THE SAME EXPENSIVE RUN A SECOND TIME, alongside the one already
in flight. That is the duplicate run, executed by following the rules.

```
  state: answered           → NOW apply the answer test (below). A hit returns the path.
                              Cost ~0. Run nothing, write nothing.

  state: working            → MATCH IT ON ITS `# Q —` LINE, NOT ON ITS ANSWER. Does that
    (started: within TTL)     restated question BE my question? If YES: ⏳ SOMEONE IS ALREADY
                              ON IT. Return the path + "in progress since <started>". DO NOT
                              RE-RUN. DO NOT CLAIM. DO NOT TOUCH THE FILE. An expensive
                              P-B-E-R run is SAVED. Cost ~0. If NO (a different question):
                              it is not a hit — fall through to ② or ③ as normal.

  state: working            → 🧟 ZOMBIE CLAIM. The run that made it is dead.
    (started: past TTL)       RECLAIM it (Step 3b).

  superseded-by: QA/<m>-…   → the answer CHANGED. FOLLOW the chain to the live file
                              (and keep following it — a chain may be longer than one hop).
                              Return the LIVE answer's path, never the superseded one.
                              THEN apply the answer test to the LIVE file.

  NO state line             → MALFORMED. `state:` is MANDATORY (checker: qa-no-state), and
                              this is MY OWN LAYER'S file — so REPAIR it, in place:
                                · `## Answer` has a body  → add `- state:   answered`
                                · `## Answer` is EMPTY    → it is an untagged claim of unknown
                                  age. Treat it as a ZOMBIE and RECLAIM it (Step 3b).
                              A consumer may NEVER do this. Only the owner.
```

THE ANSWER TEST (applies to an `answered` file — see the ordering above). A hit counts ONLY if
the QA file LITERALLY ANSWERS THIS QUESTION. Read the file — topic similarity is not an answer.
"Profile the WellDoc cohorts" and "scan WellDoc for cycle columns" look like the same topic and
share zero evidence. A near-miss is NOT a hit; it falls through to ② or ③.

Step 2 — ② DIGEST. No QA file, but `results/` (or an existing report) already contain the
answer.

```
  read:   results/<run>/metrics.json · results/<run>/*.md · workflow/report*.yaml
  write:  <leaf>/QA/<n>-<slug>.md         ← the ONLY file this path creates
          ONCE, COMPLETE, `state: answered`. No `started:` needed — nothing was claimed.
  run:    nothing. Zero code executes on this path.
```

This is the digest-only run. It is deliberately cheap: the evidence already exists and was
simply never written down in readable form. It never produces a `working` file — there is
nothing to claim when the write is instant.

Step 3 — ③ P-B-E-R. Neither ① nor ② holds. CLAIM the file, run the lifecycle at the
SHALLOWEST depth that honestly answers the question, and COMPLETE the file at REPORT.


Step 3a — ⚑ THE CLAIM (write it BEFORE the lifecycle runs)
-----------------------------------------------------------

The moment ③ is decided — BEFORE Plan, BEFORE any code — write the claim. It says to every
future reader: *someone is already on this; do not duplicate the work.*

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

At REPORT, COMPLETE the same file — the second and last write by its one owner:

```
  - state:   answered        (rewrite the state line; `started:` may stay or go)
  ## Answer  ← the body, now filled. See "The output" below.
```

If the run DIES or the question is REFUSED after a claim was made, RELEASE the claim:
delete the claim file (it has an empty `## Answer` — it is a ticket, not evidence). A
claim you cannot complete must not be left standing; if it is left standing anyway, the TTL
is the backstop, not the plan.


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
   day 1    QA/1-cycle.md   - state: answered      "no cycle column"
   day 40   a re-run lands NEW data. The truth CHANGED.
            the EXECUTOR writes  QA/2-cycle.md   - state: answered   "cycle column found
                                                                      in the 2026 export"
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

Supersede ONLY when the answer CHANGED. A new question, a deeper cut, or a different subset
is NOT a supersession — it is simply `QA/<n+1>-<slug>.md`, and the old file stays live.


The ENRICH depth ladder
------------------------

The depth IS the entry point into Plan → Build → Execute → Report:

```
  depth 0  📖 READ        existing results/ already hold the answer
                          → enter at REPORT: write QA/<n>-<slug>.md · nothing runs
                            (this is the ② DIGEST path, reached from ③ — so it writes
                             ONCE, COMPLETE, `state: answered`. No claim is needed.)

  depth 1  ⚙️  NEW RUN     an existing script answers it with a NEW config
                          → enter at EXECUTE:
                              + configs/<new>.yaml       new parameters / new subset
                              + runs/<new>/              a NEW run directory
                            SAME CODE. Never edit an old run, never overwrite old results.

  depth 2  🔧 NEW SCRIPT  the question fits this leaf's SCOPE, but no script computes it
                          → enter at BUILD:
                              + <new>.py
                              + workflow/plan-script-<new>.yaml
                            → Execute → Report

  depth 3  🌱 NEW LEAF    outside this leaf's scope — a different unit of work
                          → full P-B-E-R from PLAN, in a SIBLING leaf at the next free NN
```

Depths 1, 2 and 3 all run code, so all three CLAIM FIRST (Step 3a). Depth 0 runs nothing —
it is the digest, and it writes once, complete.

SCOPE TEST (the only hard call — depth 2 vs depth 3):

```
  Does the question fit THIS leaf's workflow/plan.yaml IPO —
  the SAME inputs, and the SAME process family?

    yes → depth 2 (new script inside this leaf)
    no  → depth 3 (new sibling leaf)
```

Worked example: a leaf that scans WellDoc table SCHEMAS for a column name is asked to
COUNT female patients with ≥14 days of CGM. Different inputs (BG entries + a Patient
join, not the schema listing) ⇒ depth 3, a sibling leaf — not a new script inside the
schema scanner.

Always pick the shallowest depth that answers the question honestly. Never inflate:
a depth-1 answer dressed up as a depth-3 rebuild is waste, and a depth-3 question forced
into depth 1 is a wrong answer.


What accretes, what is frozen, what is mutable
-----------------------------------------------

```
  ACCRETES (add-only)        QA files · configs/ · runs/ · scripts · leaves
  FROZEN   (never edit)      past results/ · a QA file's BODY (# Q / ## Answer /
                             ## Caveats / ## Not-done), once written
  MUTABLE  (one owner)       a QA file's `state:` LINE — and nothing else in the file.
                             Only this layer ever edits it. Two edits in a file's life:
                             working → answered, and answered → + superseded-by:
  LIVING   (one writer)      workflow/plan.yaml — the task layer's own; may evolve
```

A new question NEVER mutates an old answer. It ADDS `QA/<n+1>-<slug>.md`. If the new work
contradicts an old QA file, the new file SAYS SO in its own `## Caveats` — and if the old
answer is now WRONG rather than merely narrower, the old file's state line gains
`superseded-by:` (above). The old body stays exactly as written.


The output: QA/<n>-<slug>.md
-----------------------------

```
  path      tasks/<leaf>/QA/<n>-<slug>.md
  <n>       creation order within THIS leaf: 1, 2, 3, …
            THE NUMBERING IS THE INDEX. `ls QA/` IS the index. No INDEX file.
  <slug>    a short kebab-case slug of the question. SLUG ONLY.
  writer    THE TASK LAYER — the CLAIM at the ③ decision, the COMPLETION at Report.
            ONE WRITER. Nobody else writes this file, ever.
```

**ALLOCATING `<n>` — FAIL-CLOSED, IMMEDIATELY BEFORE THE WRITE.** Parallel orchestrators are the
DESIGNED dispatch mode (a probe batches independent questions, backgrounded), and two of them can
be T3 ENRICH on the SAME leaf at once. If both `ls QA/` early, both see 2 files, both compute
n=3, and both write — and if they also picked the SAME SLUG the second Write silently CLOBBERS an
answer that was never supposed to be editable. Allocating late + `set -C` is what turns that
clobber into a DETECTED loss.

The residual case — same `<n>`, DIFFERENT slug (`QA/3-foo.md` + `QA/3-bar.md`) — is **NON-FATAL
BY RULING** and is NOT a reviewer REVISE: `ls QA/` still indexes both files, and ① SCAN finds
both. The reviewer's FILENAME check carries this exemption EXPLICITLY. Never "fix" it by
renaming a QA file — the body is frozen, and a rename orphans a live claim.

```
  n = (highest existing <n> under <leaf>/QA/) + 1     ← computed at WRITE time, not earlier
  if <n>-<slug>.md already exists → DO NOT overwrite. Re-scan, take the next free n.
```

On path ③ the WRITE that matters for allocation is the CLAIM: `<n>` is allocated
immediately before the `set -C` create, and the noclobber guard is what makes "already
exists" a DETECTED loss rather than a silent clobber. The completion at REPORT rewrites the
file this run already owns — it never re-allocates `<n>`.

⛔ NEVER put an EXTERNAL ID in the filename — not a claim id, not a footnote number, not a
ticket. If a token arrives that this layer cannot itself explain, it does not belong in a
filename here. The slug comes from the QUESTION, and from nothing else.

Anatomy — the state line, then exactly three sections, in this order:

```markdown
# Q — <the question, restated by the executor in its own words, self-contained, general>
- state:   answered
- started: 2026-07-14T09:12
- by:      <run id | agent | human>

## Answer
<plain words. The finding, stated so a reader who has never opened this leaf can use it.>
<every load-bearing number carries an anchor: [→ results/<run>/metrics.json]>

## Caveats
<what this does NOT establish. Scope limits. Known confounds. Anything a reader could
 over-read from the Answer.>

## Not-done
<what was asked but not resolved, and WHY. Empty is allowed — say "nothing outstanding".>
```

Rules for the body:

- Self-contained. The `# Q` line must make sense to someone who has read nothing else.
- GENERAL language only. The answer belongs to the bank, not to whoever asked for it.
- Every number that carries weight gets an `[→ results/…]` anchor. A number with no anchor
  is an assertion, not evidence.
- `## Not-done` is not an apology — it is the honest boundary of the run. A negative result
  is a COMPLETE answer, never a failure.
- No markdown tables. Bullets and prose.
- ⛔ NEVER leave `## Answer` empty on a file that says `state: answered`. That is a LYING
  RECEIPT, and the checker FAILs it: `qa-answered-empty`. An empty `## Answer` is legal in
  exactly one situation — the file is `state: working`.

🚫 NO CONSUMER VOCABULARY (this is a hard lint, and it is checked):

```
  forbidden in a QA file:   C1, C2, … (claim ids) · H1, H2, … (hypothesis ids)
                            "claims-stage" · "the paper" (meaning some specific paper)
                            "supports the claim" · "this rescues …" · a paper's name
  why:                      the task layer never saw a paper. It cannot honestly write
                            one of these words — if one appears, the wall was crossed and
                            the evidence is coming back consumer-SHAPED.
  precedent:                a task result file on disk today says "to answer two
                            claims-stage questions: C6 … C7 …". That file is the bug this
                            rule exists to prevent. Do not write another one.
```


The abuse guard — three reasons, no fourth
-------------------------------------------

A QA file needs ONE of these reasons to exist:

```
  🎯 commissioned    a question arrived (from any of the three callers) and this file
                     answers it
  ♻️ digest-only     results/ already answered it; the digest was simply missing (gate ②)
  ✍️ executor's own  a task session judged a finding worth digesting — including proactive
                     ANSWERABILITY WORK: writing the digest before anyone asks
```

⛔ There is no fourth reason. A `QA/` folder that mirrors every result file is NOISE, not
an index. Do not digest a run just because it finished.


How a QA file READS — for anyone, at any time
----------------------------------------------

The state line is not bookkeeping. It is what lets three different readers, days or weeks
apart, avoid three different mistakes:

```
   ① SCAN — a 2nd qa call        `state: working` → DO NOT RE-RUN. Return the path +
      (this layer, days later)    "in progress since <started>". An expensive P-B-E-R run
                                  is SAVED. This is the duplicate-work fix.

   ② A CONSUMER'S MATCH           `state: working` → the question is LIVE. It sets its OWN
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
   no QA file                              → NOT ANSWERED
   QA file · state: working                → IN PROGRESS (since <started>)
                                             — unless started: is older than
                                               QA_CLAIM_TTL_HOURS, in which case the claim
                                               is STALE and RECLAIMABLE
   QA file · state: answered               → ANSWERED
   QA file · state: answered · superseded-by: X
                                           → ANSWERED, but STALE — the LIVE answer is X
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


REFUSE — and mean it
---------------------

REFUSE when the question is not the task layer's to answer:

```
  literature / prior art / "has anyone published …"   → /haipipe-discovery qa "<question>"
  needs data this project does not hold                → say so; name what is missing
  the named <leaf> is the wrong leaf                   → name the right one, if one exists
  answering honestly would require crossing a scope
    guard the question itself set                      → STOP and report the conflict
```

A REFUSE writes NO QA file — and if a claim was already made before the refusal became
clear, it RELEASES it (delete the claim file; its `## Answer` is empty, so nothing of value
is lost). Never leave a `working` file behind a refusal: it tells every future reader that
work is underway when nothing is.

A REFUSE is a complete, honest return. Never half-answer a question that is out of scope,
and never quietly widen the scope to make an answer possible.


Return
-------

```
status:    ok | refused | blocked | failed
gate:      1 (qa scan) | 2 (digest) | 3 (p-b-e-r)
depth:     0 | 1 | 2 | 3        (gate 3 only; the caller does not need it, but the human does)
qa_file:   tasks/<leaf>/QA/<n>-<slug>.md      ← THE ANSWER. A path, always.
qa_state:  working | answered                 ← the state line of the file at qa_file.
           `working` means: SOMEONE IS ALREADY ON IT (in progress since <started>).
           The caller does NOT re-dispatch, and does NOT touch the file.
artifacts: [any configs / runs / scripts / results created]
next:      suggested follow-up, or none
```

The qa_file PATH is the whole return. Whoever asked reads that file and interprets it on
their own side, in their own vocabulary, on their own schedule. This layer does not
follow up, does not notify, does not open the caller's files, and does not care what the
answer turned out to mean.


Two session modes (why this verb is a side door)
-------------------------------------------------

```
  ⚙️ THE TASK SESSION — the primary mode
     Just runs P-B-E-R for its own sake: train, sweep, profile, scan.
     No question pending. No ask. This IS the project's research.
     The bank grows AUTONOMOUSLY, and it grows here.

     It may ALSO do ANSWERABILITY WORK — task-native, no question pending:
       · write QA/ digests for findings worth digesting     (reason ✍️ above)
       · build/refactor code so FUTURE questions are cheap to answer
     It does not know WHICH questions will come. It makes the bank EASIER TO ASK.

  📄 A CONSUMER SESSION — somewhere else, weeks apart
     Asks. When it does, it arrives HERE, through this door, with one general
     question and nothing else.
```

Consequence: in a healthy project MOST questions are already answered before anyone asks
them. Gate ① and gate ② should be the common outcomes. A gate-③ P-B-E-R run is the
EXCEPTION — and if every question is landing on ③, either the scan was lazy or the bank
is starving.
