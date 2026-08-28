---
name: haipipe-discovery
description: >-
  External-evidence layer: literature search, claim review, and idea
  generation, one topic per discovery-folder running Plan → Build → Execute →
  Report. The `qa` verb answers one plain-language question and returns that
  folder's QA digest. Use to find papers, run a lit review, check prior art,
  or generate ideas. Trigger: discover, find paper, lit review, 找idea, 查新,
  source, verdict, landscape, qa, /haipipe-discovery.
argument-hint: "[verb|type] [discovery] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.3.5"
  last_updated: "2026-08-27"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-discovery (orchestrator)
======================================

Single entry for the discovery layer: what the outside world already knows (`Search` gather, `Review` analyze) and the new angles drawn from it (`Idea` create). Discovery is **external evidence work**, not a task execution stage. Durable evidence lives under `discoveries/`; whoever needs it references it from their own side — this layer never references upward.

Discovery is one of the **two EXECUTORS** (task is the other). Same shape, same rules: it runs a lifecycle for its OWN sake, it is **PROBE-UNAWARE**, and it answers plain questions through its own `qa` verb. See "Two session modes" below.

Verbs
-----

```
/haipipe-discovery                              -> dashboard: render this verb list + the Model line, suggest the likely next command
/haipipe-discovery <discovery>                  -> run full lifecycle on a folder
/haipipe-discovery <discovery-group>            -> iterate/summarize children
/haipipe-discovery status [path]                -> read-only status
/haipipe-discovery open <type> <question>       -> scaffold a typed discovery-folder (type = Search | Review | Idea)
/haipipe-discovery open-group <slug>            -> ensure discovery-group dir
/haipipe-discovery plan <discovery>             -> (re)write discovery.yaml
/haipipe-discovery build <discovery>            -> author the optional instrument (build/)
/haipipe-discovery execute <discovery>          -> do the work, write the terminal file
/haipipe-discovery report <discovery>           -> append the report block + log event
/haipipe-discovery qa "<question>" [<discovery-folder>]     -> THE QUESTION DOOR: answer ONE general-language
                                                   question -> <discovery-folder>/QA/<n>-<slug>.md  (see fn/qa.md)
/haipipe-discovery feedback "<text>" | list [unit] | move <file> <unit>   -> skill-feedback inbox (see Feedback)
/haipipe-discovery digest ["<session-name|id>"] [--dry-run]               -> harvest a session's feedback (see Feedback)

/haipipe-discovery <specialist> [args]          -> one-off worker dispatch (NO folder)
/haipipe-discovery "<natural language>"         -> infer + dispatch (Routing)
```

The `qa` verb — the question door (R11)
---------------------------------------

Full contract: `fn/qa.md`. In one screen:

```
/haipipe-discovery qa "<question>" [<discovery-folder>] [--check-only]

  input: ONE question, GENERAL language. NO PP id, NO paper ref, NO stake, NO claim id.
         The verb never learns WHO asks or WHY. It answers questions. That is all.

   ① QA SCAN    grep <discovery-folder>/QA/*.md (or all discovery-folders). MATCH ON THE ANSWER, never the
                topic: READ the file. Then READ ITS STATE LINE:                  ~0
                  state: answered  -> return the QA file PATH
                  state: working   -> SOMEONE IS ALREADY ON IT. Return the path +
                                      "in progress since <started>". DO NOT RE-RUN.
                  working, EXPIRED past QA_WORKING_TTL_HOURS -> 🧟 zombie: RESTART it
                  working, executor KNOWN dead before Report (its run ended
                    without completing the file) -> reclaim NOW, no TTL wait:
                    fresh `started:`/`by:` on the SAME file, or supersede it.
                    NEVER delete a ticket — deletion erases the claim history
                  superseded-by: X -> follow the chain, return the LIVE answer
   ② DIGEST     sources.md / notes.md / verdict.md / landscape.md / ideas.md already
                answer it, but no readable digest exists -> write QA/<n>-<slug>.md
                ONCE, COMPLETE, `state: answered`, from EXISTING artifacts.     cheap
                No searching, no new judgment. No claim — nothing to race.
   ③ LIFECYCLE  neither -> ⚑ CLAIM FIRST (write the QA file with `state: working` +
                `started:` under `set -C`), then Plan → Build(opt) → Execute → Report
                at the SHALLOWEST depth that answers it, and COMPLETE the same file at
                Report (`state: answered` + the `## Answer` body):
                  depth 0 READ · depth 1 ENRICH (on-topic, same discovery-folder) ·
                  depth 2 NEW FOLDER (in the group) · depth 3 NEW GROUP
   🚫 REFUSE    not discovery-shaped -> the CALLER re-routes. RELEASE any claim.
                task-shaped (code / runs / metrics on our own data) -> /haipipe-task qa

  THREE CALLERS: a probe's DISPATCH (via the orchestrator agent) · a HUMAN directly ·
                 the ORCHESTRATOR itself (self-directed). None of them is special.
```

The commission lives in the CONSUMER's own probe file; this layer only ever sees a plain
question, and nothing under `discoveries/` carries a trace of who asked.

Two session modes (R17) — the primary mode is NOT question-driven
------------------------------------------------------------------

```
   ⚙️ THIS LAYER (executor)                  📄 the CONSUMER (paper / application)
   ══════════════════════════               ═══════════════════════════
   just runs Plan → Build → Execute →       raises its questions, matches them
   Report on its own research topics        against this bank, commissions the gaps
   — no question needed, no ask             (its probe files hold the stake; we
        │                                    never see them)
        ▼                                        │
   the bank grows AUTONOMOUSLY  ◀───────────────┘  most questions should already
   discovery.yaml · sources.md · terminals         be ANSWERED before anyone asks
        │
        └─ ANSWERABILITY WORK (native, probe-unaware):
           · write QA/ digests for notable findings
           · build reusable source bases so future questions are CHEAP
           it does not know WHICH questions will come. It makes the bank
           EASIER TO ASK. That is discovery-native work.
```

The Model
---------

Two axes, same as task: LIFECYCLE `Plan -> Build(opt) -> Execute -> Report` (uniform, process verbs) × TYPE `Search · Review · Idea` (folder kinds; each type maps 1:1 to its bucket). The type only changes what Execute produces:

```
Search   INPUT     search + read source material      -> sources.md + notes.md (reusable source base)
Review   PROCESS   judge a claim OR map a field       -> verdict.md (judge) / landscape.md (synthesize), role: picks
Idea     OUTPUT    generate ideas OR check novelty    -> ideas.md (idea_generation) / verdict.md (novelty_check)
```

The CANONICAL contract lives in ONE place — per-stage IO and the chain: `ref/lifecycle-map.md`; fields, roles, terminal templates: `ref/discovery-yaml-schema.md`. Do not restate them here. A one-off capability call does NOT create a folder; the discovery-folder is only for durable, project-tracked topics — the same split as a quick script vs a scaffolded task-folder.

Hierarchy
---------

```
discoveries/<GROUP>/<NN>_<topic>/   -> one research topic per folder, e.g.:

├── L01_personality-prescribing-landscape/  (landscape / context work)
│   ├── 01_empathy-agreeableness-outcomes/   (Review, landscape_review -> landscape.md)
│   └── 02_trait-signal-novelty/             (Idea, novelty_check -> verdict.md)
└── P01_trait-opioid-prior-art/             (claim evidence)
    ├── 01_trait-rx-source-base/             (Search -> sources.md + notes.md)
    └── 02_agreeableness-rx-prior-art/       (Review, prior_art_check -> verdict.md)
```

The discovery-folder, in full — the `QA/` folder is OPTIONAL and every discovery-folder may carry one (R9):

```
discoveries/P01_trait-opioid-prior-art/02_agreeableness-rx-prior-art/
├── discovery.yaml     Q — the spec           (Plan writes · Report appends report:)
├── build/             the optional instrument
├── sources.md         A — raw evidence       ┐
├── notes.md           A — what was read      │ the layer's own terminals; a
├── verdict.md         A — the TERMINAL       ┘ Review verdict.md is OURS and SURVIVES
└── QA/                A — READABLE digests   🆕 optional, not every discovery-folder has one
    ├── 1-trait-rx-prior-art.md
    └── 2-dose-response-coverage.md
```

A QA FILE IS A TICKET THAT BECOMES A RECEIPT. It carries exactly ONE mutable field —
the state line — and everything below it is written once and never touched again:

```markdown
# Q — <the question, restated by the executor in its own words>
- state:   working | answered | superseded-by: QA/<m>-<slug>.md
- started: 2026-07-14T09:12          ← MANDATORY when state: working
- by:      <run id | agent | human>  ← optional provenance

## Answer     EMPTY while state: working. Filled at REPORT.
## Caveats
## Not-done
```

```
NAMING IS THE INDEX.  QA/<n>-<slug>.md, n = creation order. `ls QA/` IS the index —
numbered, ordered, greppable. It now reads as a menu of BOTH: what this discovery-folder has
established, AND what it is establishing right now. No INDEX file until a discovery-folder's QA
count earns one.

SLUG ONLY. No PP id, no claim id, no paper ref in a bank filename — ever.

⚠️ THE LOAD-BEARING INVARIANT IS *ONE WRITER*, NOT *WRITE-ONCE*.
   This layer writes the file TWICE — the CLAIM at the qa gate's ③ decision
   (state: working + started:), the COMPLETION at Report (state: answered + the
   ## Answer body). Two writes by the SAME OWNER is fine.
   ⛔ A CONSUMER (probe / paper / application) must NEVER create, claim, edit,
      complete, or supersede a QA file. A consumer-planted `working` file is the
      retired _ASK/ stub wearing a QA/ costume, and it is FORBIDDEN.

WRITER: this layer. Only gate ③ ever produces a `working` file, and only transiently
        (gate ① writes nothing; gate ② writes once, complete). Anatomy + the three
        legal reasons a QA file may exist (commissioned · digest-only · executor's
        own): fn/qa.md.

THE CLAIM MUST EXPIRE. `started:` is MANDATORY on a `working` file — a claim that
   cannot expire is a zombie by construction. TTL = the named constant
   QA_WORKING_TTL_HOURS = 24. Past it the claim is STALE and the next qa call may
   RESTART it (fresh started:, abandoned attempt recorded in ## Not-done).
RACE GUARD. Create the claim under `set -C` (noclobber). The loser re-scans and
   DEFERS. No lock dirs, no lease servers, no ledgers.
SUPERSESSION. A later run whose answer CHANGES writes QA/<n+1>-<slug>.md and APPENDS
   `superseded-by:` to the OLD file's state line — by this layer, never by a consumer.
   A QA file's BODY is never edited. The state line is the ONE mutable field.

STATUS reads the STATE LINE, not mere existence:
   no QA file                 -> not answered
   state: working             -> IN PROGRESS (since <started>)
   state: answered            -> answered
   superseded-by: X           -> answered, but STALE — the live answer is X

⛔ ABUSE GUARD: a QA/ that mirrors every source is noise, not an index.
⛔ LAW 2 (bank surface): a QA file carries NO consumer vocabulary — no C\d, no H\d,
   no "claims-stage", no "the paper" meaning someone's paper. Write it for the NEXT
   reader, who has a different stake, or none.
⛔ THE CHECKER HARD-FAILS three defects THIS layer can write:
   qa-working-no-started (unexpirable `working` file) · qa-working-expired (zombie past
   QA_WORKING_TTL_HOURS) · qa-answered-empty (`state: answered` with an EMPTY
   ## Answer — a lying receipt).
```


Group letters are purpose hints, not the source of truth (`type:`/`role:` in discovery.yaml are authoritative). Three purposes, one routing question each:

```
S  source base        just building a pile of sources?           (mostly Search)
L  landscape          understanding a field / context?           (mostly Review synthesize, Idea)
P  proof / prior art  testing a specific claim against outside?  (mostly Review judge, Search)
```

Buckets (Execute-stage workers)
-------------------------------

Three buckets, 1:1 with the types, each HEADED by a type-specialist skill that owns that type's Execute procedure and output contracts (the Review Output Contract lives in haipipe-discovery-review) and picks among the workers beside it:

```
1_search   /haipipe-discovery-search   fetch AND read -> sources.md + notes.md
  arxiv (preprints) · semantic-scholar (venues+citations) · exa-search (broad web)
  alphaxiv (fast read) · deepxiv (section read) · paper-analyzer (deep note)

2_review   /haipipe-discovery-review   judge -> verdict.md, synthesize -> landscape.md
  research-lit (default) · comm-lit-review (comms domain) · academic-researcher (cross-discipline)

3_idea     /haipipe-discovery-idea     generate -> ideas.md, novelty_check -> verdict.md
  idea-creator (brainstorm + rank) · novelty-check (查新)
```

Bucket aliases: `1|search`, `2|review`, `3|idea|novelty`. (Reading is part of searching — no separate `read` alias.)

Routing
-------

```
0. First positional is `qa` -> route to fn/qa.md BEFORE any other parsing. Everything after
     it is ONE general-language question (+ an optional discovery-folder path, + --check-only). Never
     re-interpret a qa question as a routing keyword.
1. First positional is a lifecycle verb (open / open-group / plan / build / execute / report / status)
     -> durable operation on the folder. `feedback` and `digest` route to fn/feedback.md /
        fn/digest.md BEFORE any other parsing; neither scaffolds a folder.
2. First positional is an existing path: discovery-folder -> run requested stage or full
     lifecycle; discovery-group -> iterate/summarize children.
3. `open <type>` where type ∈ {Search, Review, Idea} -> scaffold that typed folder.
4. First positional is a specialist name -> dispatch that worker (one-off, NO folder).
5. arXiv ID / URL in args -> a 1_search read worker:
     "summarize|explain" -> alphaxiv ; "section|layered" -> deepxiv ; "analyze|claims" -> paper-analyzer
     bare ID, no verb -> alphaxiv
6. First positional is a bucket alias -> use that bucket.
7. Keyword scan (pick a worker for a one-off, or infer a folder type):
     "preprint|arxiv"                          -> arxiv            (Search)
     "IEEE|ACM|venue|citation"                 -> semantic-scholar (Search)
     "web|blog|news|exa"                       -> exa-search       (Search)
     "review|survey|landscape|map the field|related work" -> research-lit (Review synthesize)
     "prior art|is X known|does X exist|already done"     -> Review judge (verdict)
     "novelty|is this idea new|查新"            -> novelty-check    (Idea, role novelty_check)
     "brainstorm|find idea|找idea|propose"      -> idea-creator     (Idea)
8. Bucket resolved, specialist unresolved -> bucket default
     (1_search: arxiv to find, alphaxiv to read one paper | 2_review: research-lit | 3_idea: idea-creator).
9. Nothing resolves -> ask: Search (gather) / Review (judge or map) / Idea (generate or check)?
```

Dispatch: `Skill(<specialist>, args="...")`; do not auto-chain. Type-level work goes to the type specialists — they pick workers and carry the output contracts.

Protocol (durable project work)
-------------------------------

Walk the lifecycle stages; never hand-place a completed discovery package.

```
Step 0  Resolve project root = nearest ancestor with tasks/, paper/, applications/, or _haipipe/.
        If ambiguous, ask (AUTO -> blocked).
Step 1  Resolve scope: folder (has discovery.yaml) -> run stage(s); group -> iterate;
        open-group -> create container; open <type> <question> -> scaffold; specialist -> one-off.
Step 2  Group: purpose letter (S/L/P) + next free two-digit id (no renumbering).
Step 3  Folder: next free NN_<slug>/ in the group. One topic per folder; slug names the TOPIC.
Step 4  Run the stages (each owns its files):
        Plan     write discovery.yaml (type + role + question + sources + expected_outputs).
                 The QUESTION is the whole contract — whether it came from this layer's own
                 research agenda, from a human, or verbatim from a caller's dispatch. It
                 arrives in GENERAL language and it is answered on its own terms; there is
                 no stub to read and nothing upward to look at.
                 NO parent field — self-contained; append discovery.opened to _haipipe/project.log.jsonl
        Build    (optional) author the instrument under build/; set status building
        Execute  dispatch the TYPE SKILL — Search -> haipipe-discovery-search,
                 Review -> haipipe-discovery-review, Idea -> haipipe-discovery-idea;
                 inspect local project evidence first unless fresh web search was asked; set status executing
        Report   APPEND the report: block (absent until now; outcome != lifecycle status);
                 set top-level status (ok / inconclusive / blocked);
                 THE QA FILE — QA/<n>-<slug>.md, for exactly one of the three legal
                 reasons (commissioned · digest-only · executor's own):
                   · came in via gate ③  -> the CLAIM already exists on disk
                     (state: working + started:, empty ## Answer, written at the ③
                     decision BEFORE Plan ran). COMPLETE it here: rewrite the state line
                     to `state: answered` and fill the `## Answer` body. That is the
                     SECOND and LAST write, by the same owner.
                   · came in via gate ②  -> CREATE it here, ONCE, COMPLETE,
                     `state: answered`. No claim was needed — the write is instant.
                 THE EXECUTOR HOLDS THE PEN: whoever asked may have CAUSED this file, but
                 this layer AUTHORS it — both writes — in general language, with no
                 consumer vocabulary in it (fn/qa.md · LAW 2). A CONSUMER never writes
                 a QA file, and never touches its state line;
                 append discovery.completed to the project log
        Handoff  return the terminal path (+ the QA file path, if one was written) to the
                 caller; the CALLER records the link on its own side and appends
                 discovery.consumed — the discovery records nothing upward. No `answers:`
                 field, no ask mailbox, no id of any kind: whoever asked harvests the path
                 on their own schedule.
Step 5  Return: {status, discovery_group, discovery_folder, type, files_written, qa_file, next}.
```

Feedback
--------

`feedback` / `digest` are utility verbs about THIS skill (not about discovery findings); capture-only — fixing is a later revision pass. Full contract: `fn/feedback.md` + `fn/digest.md`; fallback inbox: `feedback/README.md`.

```
capture  feedback "<text>"   -> route to the unit's feedback/ inbox: cross-cutting guard first
                                (lifecycle/type-field/schema-wide -> THIS folder's feedback/),
                                else keyword -> unit, else active context, else fallback.
                                Units: 1_search · 2_review · 3_idea · agents. MERGE-OR-CREATE:
                                same-topic items update the existing file (dated recurrence,
                                verbatim history, reopen if fixed), never duplicate.
list     feedback list [unit] -> aggregate open items across ALL inboxes, grouped by unit.
move     feedback move <file> <unit> -> re-route a mis-filed item (pure file move).
digest   digest [session] [--dry-run] -> scan a session transcript (past by name/id, else current)
                                for conversational feedback; distill, dedup, MANDATORY confirm
                                gate, then route each item through capture. Global behavioral
                                prefs go to /remember, not inboxes.
```

Behavioral Preferences (portable)
---------------------------------

ALWAYS read and honor `PREFERENCES.md` in this skill's folder: git-tracked global behavioral preferences that survive a machine change, kept in sync across orchestrators by `/haipipe-paper digest`'s global-pref fan-out.
