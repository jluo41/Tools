discovery — External Evidence Layer (DESIGN)
=============================================

Status: v2.6.0 (2026-07-03) - TWO-AXIS model mirroring task. Uniform lifecycle
        Plan -> Build(opt) -> Execute -> Report, crossed with 3 folder types
        Search / Review / Idea. 3 buckets, exactly one per type, each headed
        by a type specialist (haipipe-discovery-search/-review/-idea).
        Self-contained folders: no parent field, no upward references. Folder
        contract = discovery.yaml + evidence files only. Group letters S/L/P.
        Skill is haipipe-discovery; discovery = one topic per FOLDER.
Owner:  jluo41
Scope:  external-evidence discovery work and its durable artifact contract inside
        project folders.


Why this layer exists
=====================

`discovery` answers what the outside world already knows. It is not a task
execution stage and it judges nobody's claims.

```
discovery   outside-world evidence   sources, notes, verdicts, maps, ideas   ⚙️ EXECUTOR
task        inside-world execution   code, runs, metrics, reports            ⚙️ EXECUTOR
probe       a PAPER-LEVEL document   papers/<P>/1-probes/PPNN_<topic>.md —   📄 CONSUMER
                                     one question per SECTION, holding the
                                     stake it never lets out; binds to an
                                     answer BY PATH
paper/app   delivery (story)         owns the message, judges its own claims in 1-claims.md
```

The two EXECUTORS are the same shape and follow the same rules (task = discovery).
Both are **probe-UNAWARE**: they run their own lifecycle for their own reasons, and
they answer plain questions through their own `qa` verb. Nothing under `discoveries/`
ever learns that a probe, a paper, or a claim exists.


Two Parts
=========

```
1. Skill interface layer
   /haipipe-discovery is the single entry. It runs the durable discovery lifecycle
   (Plan/Build/Execute/Report) and routes to search/review/idea bucket workers.

2. Durable artifact layer
   discoveries/<group>/<NN>_<topic>/ stores external evidence — for the project, not
   for any one consumer of it. The optional QA/ folder is its readable face.

3. The question door
   /haipipe-discovery qa "<question>" (fn/qa.md) — one question in general language,
   one QA file out. Three callers, none of them special: a consumer's probe dispatch
   (via the orchestrator agent, whose clean context is the wall), a human exploring a
   direction, or the orchestrator itself doing answerability work with nothing pending.
```

Each type has a TYPE SPECIALIST skill at the head of its bucket
(haipipe-discovery-search / -review / -idea, v2.5.0), mirroring the sibling
layers (haipipe-data-source etc.): it owns that type's Execute procedure and
output contracts and dispatches the capability workers beside it.
`discoveries/` is the persistent package they fill. (The v2.0.0 decision NOT
to create a per-type family was made when workers != types; it dissolved when
buckets became 1:1 with types.)


The Two-Axis Model (mirrors task)
=================================

Discovery has the SAME two axes as task: a uniform lifecycle crossed with a
folder type.

```
Axis 1 — LIFECYCLE (uniform; every folder runs it)   Plan -> Build(opt) -> Execute -> Report   (process verbs)
Axis 2 — TYPE      (what kind of folder this is)      Search · Review · Idea                    (folder kinds)

Task = (Plan/Build/Execute/Report) × (data/nn/fit/...)
Discovery = (Plan/Build/Execute/Report) × (Search/Review/Idea)
```

The two axes use non-overlapping vocabularies on purpose: the stages are
process verbs every folder runs, the types name the kind of folder, and no
word appears in both lists, so they can never be confused (the historical
mistake was using search/read/review/idea as BOTH the stages and the types).

One simplification versus task: a task-folder holds MANY runs; a discovery-folder
holds ONE execution per topic — one Plan, one Execute, one Report.

The canonical per-stage / per-type contract lives in ONE place:
`haipipe-discovery/ref/lifecycle-map.md`. Field schema:
`haipipe-discovery/ref/discovery-yaml-schema.md`. Do not restate them here.


Hierarchy
=========

A discovery is one research topic stored as its own folder, the way a task is
one runnable unit stored as its own folder.

```
Task:      tasks/{G}{NN}_group/   ⊃   {NN}_taskname/   -> one runnable unit
Discovery: discoveries/<GROUP>/   ⊃   <NN>_<topic>/    -> one research topic
```

```
discovery-group    A directory grouping related research topics.
discovery-folder   One research topic = one folder: discovery.yaml (Plan + Report)
                   + sources.md / notes.md (work products) + the terminal
                   (verdict.md | landscape.md | ideas.md). Nothing else.
source row         One paper/webpage/report/dataset citation inside sources.md.
```

Group letters (S source base / L landscape / P proof-prior-art) are
organizational hints only. `type:` and `role:` in discovery.yaml are
authoritative.


The Three Types (Axis 2, IPO: Search -> Review -> Idea)
========================================================

```
type     IPO       Execute does                      terminal
------   -------   -------------------------------   -------------------------------------------
Search   INPUT     search + read source material     sources.md + notes.md (reusable source base)
Review   PROCESS   judge a claim OR map a field      verdict.md / landscape.md
Idea     OUTPUT    generate ideas OR check novelty   ideas.md / verdict.md
```

Merge decisions:
- Search = search + read merged. They are always bound together (you read what
  you searched), and the digested source set is a reusable, accumulating base —
  the reason task gives `data` its own type instead of folding it into `fit`.
- Review = judge + synthesize merged. Identical mechanics (read many -> combine
  -> conclude); the only difference is output shape. `role:` picks verdict (a
  judgment) vs landscape (a map). One type, two flavors.
- Idea = generate + novelty-check merged (v2.4.0). They are the two halves of
  the ideation loop (invent, then evaluate what was invented); `role:` picks
  ideas.md vs verdict.md. Idea stays separate from Review because ideation is
  divergent while Search/Review are convergent.

```
role -> type -> terminal
Search  source_gather, source_read               -> sources.md (+ notes.md)
Review  prior_art_check, counterevidence         -> verdict.md   (judge)
Review  landscape_review, benchmark_landscape    -> landscape.md (synthesize)
Idea    idea_generation                          -> ideas.md
Idea    novelty_check                            -> verdict.md   (is this idea new?)
```


Skill Structure
===============

```
discovery/
├── haipipe-discovery/          router + durable artifact contract
│   ├── SKILL.md
│   ├── CHANGELOG.md            skill-scoped history (not loaded; read on demand)
│   ├── PREFERENCES.md          portable behavioral preferences
│   ├── fn/                     utility-verb contracts (feedback.md, digest.md)
│   ├── feedback/               orchestrator fallback feedback inbox
│   └── ref/
│       ├── lifecycle-map.md          canonical 2-axis lifecycle + type table
│       └── discovery-yaml-schema.md
├── agents/                    orchestrator / creator / reviewer agent triad
├── 1_search/                  Search bucket
│   ├── haipipe-discovery-search/   TYPE SPECIALIST (owns the Search Execute)
│   ├── arxiv/ semantic-scholar/ exa-search/
│   ├── alphaxiv/ deepxiv/ paper-analyzer/
├── 2_review/                  Review bucket
│   ├── haipipe-discovery-review/   TYPE SPECIALIST (owns the Review Execute + Output Contract)
│   ├── research-lit/ comm-lit-review/ academic-researcher/
└── 3_idea/                    Idea bucket
    ├── haipipe-discovery-idea/     TYPE SPECIALIST (owns the Idea Execute)
    ├── idea-creator/ novelty-check/
```

Buckets and types are exactly 1:1, each headed by its type specialist: Execute
dispatches haipipe-discovery-<type>, which picks among the capability workers
beside it. No exceptions: since v2.4.0 novelty_check is an Idea role — the
evaluation half of the ideation loop.


Project Folder Contract
=======================

```
examples/<PROJECT>/
├── _haipipe/
│   ├── project.log.jsonl      single append-only orchestration log
│   ├── project.status.yaml
│   └── project.site.md
├── discoveries/
│   ├── L01_personality-prescribing-landscape/  (landscape / context work)
│   │   ├── 01_empathy-agreeableness-outcomes/   (Review, landscape_review -> landscape.md)
│   │   └── 02_trait-signal-novelty/             (Idea, novelty_check -> verdict.md)
│   └── P01_trait-opioid-prior-art/             (claim evidence)
│       ├── 01_trait-rx-source-base/             (Search -> sources.md + notes.md)
│       └── 02_agreeableness-rx-prior-art/       (Review, prior_art_check -> verdict.md)
├── tasks/
├── paper/
└── applications/
```

The single orchestration log remains `_haipipe/project.log.jsonl`. A
discovery-folder keeps NO bookkeeping files of its own: lifecycle progress is
`discovery.yaml status:`, the human summary is `report.summary`.


Discovery Lifecycle (Axis 1)
============================

```
Plan       -> Build (opt)        -> Execute                  -> Report
discovery.yaml  build/ instrument    sources/notes + terminal    report block + status/site
```

`Plan` scaffolds the folder and declares the type; `Build` (optional) authors a
reusable instrument; `Execute` runs the bucket worker for the type and writes the
terminal file; `Report` reports to a human and returns the terminal to the caller.
The canonical per-stage IO lives in `ref/lifecycle-map.md`.

The chain — types compose like task types (`data -> fit -> eval`):

```
Search folder ─sources/notes→ Review folder ─landscape.md→ Idea folder
 (reusable source base)        (verdict/landscape)          (ideas)
```

A light effort skips the standalone `Search`: a `Review` folder's Execute
searches + reads inline. Build a standalone `Search` when the source base is
reused across several analyses.


Self-Contained By Design
========================

A discovery-folder knows nothing outside itself: no `parent` field, no
consumer tracking, no reference to any upper layer. It answers its question,
writes its terminal, and stops (JL principle: task and discovery run freely;
organizing happens one level up). Whoever needs the terminal records the link
in their OWN files and appends `discovery.consumed` to the project log; that
bookkeeping never enters the discovery-folder.

`discovery` writes external evidence; it does not judge project claims — the
claim-level judgment lives with whoever consumes the terminal.


Boundary Rules
==============

- `discoveries/` stores citations, source notes, verdicts, maps, ideas — and the OPTIONAL
  `QA/<n>-<slug>.md` readable digests (`fn/qa.md`).
- `discoveries/` does not store code, notebooks, runs, or metrics.
- `discoveries/` NEVER stores a trace of who asked: no `_ASK/`, no `_ANS/`, no `answers:`
  field, no PP id, no claim id. The bank is probe-unaware (R2). A caller's question arrives
  in general language, is answered on its own terms, and the answer is a FILE they point at.
- `tasks/` stores execution artifacts and metrics — and its own `QA/` digests, identically.
- A paper's evidence questions live in ITS OWN `1-probes/PPNN_<topic>.md` probe file, with
  the stake in a `## Why` that never leaves it; its claim statuses live in ITS OWN
  `1-claims.md`. Neither is ever written, read, or resolved from this layer.
- `paper/` and `applications/` own the delivery story and bind to our answers by PATH.
- `_haipipe/project.log.jsonl` is the only orchestration event log.
- `sources.md` is the default home for source records; a `sources/` subfolder is
  optional and only for heavy artifacts (PDFs, HTML snapshots).


Decision Log
============

2026-06-19  Adopted: discoveries/ as durable external-evidence packages.
2026-06-20  Adopted: discovery-group/discovery-folder hierarchy.
2026-06-21  Retired: the narrative layer. Parents are now a delivery lifecycle
            (paper/application) for L* and a probe for evidence exploration.
2026-06-21  A discovery is one research topic = its own FOLDER mirroring a
            task-folder. Skill renamed haipipe-discover -> haipipe-discovery.
2026-06-22  Added: feedback utility verb + feedback/ inbox.
2026-06-22  TWO-AXIS redesign (v2.0.0). The lifecycle is now the uniform task
            lifecycle Plan -> Build(opt) -> Execute -> Report, retiring the
            open/search/read/review/post verb-lifecycle. search/read/review/idea
            are no longer stage verbs; the folder TYPE is one of 3 Chinese-char
            types 搜/析/创. 搜 = search+read merged (reusable source base); 析 =
            judge+synthesize merged (role picks verdict.md vs landscape.md); 创 =
            idea. verdict block renamed to report (report-to-human). The 4
            capability buckets become the Execute-stage workers; per-type
            specialists are NOT created (workers != types). New terminal files
            landscape.md + ideas.md alongside verdict.md. Old folders (role +
            verdict, no type) remain readable; migrate lazily.
2026-06-24  Type axis renamed to English (v2.1.0): 搜 -> Search, 析 -> Review,
            创 -> Idea. Both axes are now English; orthogonality comes from
            non-overlapping word lists (process verbs vs folder kinds), not
            different scripts. All existing discovery folders migrated. Chinese
            TRIGGER phrases (查新/找idea) kept.
2026-07-03  Buckets 4 -> 3, one per type (v2.3.0). 2_read merged into 1_search
            (read is half of the Search type; only ever used together);
            3_review -> 2_review; 4_idea -> 3_idea. novelty-check stays in
            3_idea by choice (pairs with ideation) while serving Review-judge —
            the one documented bucket/type exception. English-only pass purged
            residual 搜/析/创 from DESIGN.md, agents/, and the live docs (history
            entries keep their original wording). Dropped dangling references:
            0_venue/, D_patent/, /idea-discovery, /research-pipeline,
            /patent-pipeline, and the agents' fn/plan-build-execute-report
            reads; deleted the stray haipipe-discovery self-symlink.
2026-07-14  PROBE-UNAWARE, AND THE QA VERB (v3.0.0). Spec of record:
            Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ (v3, approved JL
            2026-07-14, R1-R18); constitution: probe/haipipe-probe/SKILL.md 8.0.0.
            (1) DELETED the probe handoff bridge whole — `_ASK/` stub folders, the
            `answers: [PPNN]` return field, and every PP id under discoveries/.
            v2.7/2.8/2.8.1 built a two-footed bridge into this layer; R2 rules the
            bank probe-UNAWARE, so both feet come out. (2) ADDED the `qa` verb
            (fn/qa.md): one question in GENERAL language, gate ① QA SCAN → ② DIGEST
            → ③ lifecycle at the shallowest depth (READ | ENRICH | NEW FOLDER | NEW
            GROUP) → 🚫 REFUSE (task-shaped re-routes to /haipipe-task qa). It
            returns discoveries/<leaf>/QA/<n>-<slug>.md. (3) ADDED the optional QA/
            folder to the leaf contract — numbered = the index, slug only,
            write-once, three legal reasons to exist (commissioned · digest-only ·
            executor's own). THE EXECUTOR HOLDS THE PEN (CC-8): a consumer may CAUSE
            a QA file; this layer AUTHORS it — a consumer session writing a bank file
            with the stake in context is exactly how tasks/A03_.../result.md ended up
            carrying "C6"/"C7". (4) The probe GATEWAY agent is RETIRED; the
            discovery-orchestrator is now the DIRECT dispatch target, and its clean
            context IS the wall. (5) Task and discovery are BOTH EXECUTORS — same
            shape, same rules (JL-10). (6) A Review-type verdict.md is THIS layer's
            own terminal and SURVIVES; it is not the retired probe "Verdict" (R7).

2026-07-03  JL simplification pass (v2.4.0). (1) novelty_check re-typed
            Review -> Idea: it is the evaluation half of the ideation loop, so
            Idea branches by role (idea_generation -> ideas.md, novelty_check ->
            verdict.md) and buckets = types exactly 1:1 (the v2.3.0 exception
            dissolved). (2) parent:/consumed_by: fields REMOVED — task and
            discovery are probe-UNAWARE (JL principle: they run freely; the
            probe level organizes). References point one way, downward: probe
            records its discovery/task links in its own files; a discovery
            never tracks who commissioned or consumed it. (3) Folder contract
            slimmed to discovery.yaml + evidence files: status.yaml + site.md
            dropped (redundant with discovery.yaml status: and report.summary);
            report: block appended at Report, absent before. Schema doc
            rewritten lean per JL's "keep it as concise as possible".
2026-07-03  Group letters 5 -> 3 (v2.6.0, JL). S source base / L landscape
            (absorbs B) / P proof-prior-art (absorbs C). S/R/I rejected: the
            letter tags the GROUP's purpose while type: tags each folder, and
            groups mix types. Letters kept (task mirror, ls clustering,
            compact ids); existing B/C folders stay named as-is. Same day:
            SKILL.md dedup rewrite (v2.6.0, ~50% smaller) and the toolkit-wide
            changelog convention (per-skill CHANGELOG.md, frontmatter carries
            version + pointer only).
2026-07-03  Type specialist skills (v2.5.0, JL). Created haipipe-discovery-search
            / -review / -idea, one at the head of each bucket, mirroring the
            sibling layers (haipipe-data-source etc.). Each owns its type's
            Execute procedure and output contracts and dispatches the workers
            beside it; the orchestrator's Execute dispatches the type skill.
            Review Output Contract moved into haipipe-discovery-review.
            Reverses the v2.0.0 "no per-type skill family" decision, whose
            rationale (workers != types) dissolved when buckets became 1:1
            with the types.
