---
name: haipipe-discovery
description: "Router and durable lifecycle for the discovery (external-evidence) layer. A discovery is one research topic = one folder, a sibling of a task-folder, running the uniform Plan -> Build(opt) -> Execute -> Report lifecycle across 3 folder types: Search (source = search+read -> sources.md/notes.md), Review (analyze = judge a claim -> verdict.md, or synthesize a field -> landscape.md), Idea (idea -> ideas.md). The 4 capability buckets (search/read/review/idea via arxiv/semantic-scholar/exa/alphaxiv/research-lit/idea-creator/novelty-check) are the Execute-stage workers. Trigger: discover, find paper, lit review, 找idea, 查新, source, verdict, landscape, /haipipe-discovery."
argument-hint: "[verb|type] [discovery] [args...]"
allowed-tools: Bash, Read, Grep, Glob, Skill
metadata:
  version: "2.2.0"
  last_updated: "2026-06-24"
  summary: "Two-axis discovery: uniform Plan/Build/Execute/Report lifecycle x 3 folder types (Search/Review/Idea), mirroring task. Capability buckets are the Execute workers."
  changelog:
    - "1.0.0 (2026-05-31): baseline metadata added."
    - "1.6.0 (2026-06-21): ref/lifecycle-map.md canonical verb table; retire narrative parent; folder renamed discover -> discovery."
    - "1.7.0 (2026-06-21): a discovery is one research topic = its own FOLDER mirroring a task-folder."
    - "1.8.0 (2026-06-21): rename skill haipipe-discover -> haipipe-discovery."
    - "1.9.0 (2026-06-22): add feedback utility verb + feedback/ inbox."
    - "2.0.0 (2026-06-22): TWO-AXIS redesign mirroring task. Lifecycle is now the uniform Plan -> Build(opt) -> Execute -> Report (retires open/search/read/review/post). search/read/review/idea are no longer stage verbs; the folder TYPE is one of 3 types (Search=search+read source, Review=judge|synthesize, Idea=idea). verdict block renamed to report (report-to-human). The 4 capability buckets become the Execute-stage workers. See ref/lifecycle-map.md + ref/discovery-yaml-schema.md."
    - "2.1.0 (2026-06-24): renamed the three type values from the glyphs 搜/析/创 to the English words Search/Review/Idea (type axis is no longer CJK; the names now mirror their Execute bucket). Updated SKILL.md + ref/lifecycle-map.md + ref/discovery-yaml-schema.md and migrated all existing discovery folders. Chinese trigger phrases (查新/找idea/全流程/专利) are unchanged."
    - "2.2.0 (2026-06-24): capture-time feedback ROUTING (mirrors haipipe-paper). `feedback \"<text>\"` infers the bucket unit (1_search/2_read/3_review/4_idea/agents) and files into THAT unit's feedback/; cross-cutting -> orchestrator fallback. Added fn/feedback.md (full contract: cross-cutting guard -> keyword -> context -> fallback; merge-or-create; list aggregates across all inboxes; move re-routes). Recast feedback/README.md as the fallback inbox. Migrated the type-field-chinese-glyph item (cross-cutting, stays) and sources-per-section item (-> 1_search/feedback/)."
---

Skill: haipipe-discovery (orchestrator)
======================================

Single entry for the discovery layer: what the outside world already knows (`Search` gather, `Review` analyze) and the new angles drawn from it (`Idea` create). Multi-step idea pipelines still escalate to `/idea-discovery`.

Two modes:

```
1. Durable project work
   Operate on per-topic discovery-folders under examples/<PROJECT>/discoveries/,
   running the Plan -> Build(opt) -> Execute -> Report lifecycle on each.

2. Capability routing
   Dispatch to search/read/review/idea bucket workers for one-off discovery, or
   for work inside the current discovery-folder's Execute stage.
```

Discovery is **external evidence work**. It is not a task execution stage. When a discovery becomes durable project evidence, write it under `discoveries/` and let probes or delivery lifecycles (paper/application) reference it the same way probes reference tasks.

Invocation:
```
/haipipe-discovery                              -> dashboard
/haipipe-discovery <discovery>                  -> run full lifecycle on a folder
/haipipe-discovery <discovery-group>            -> iterate/summarize children
/haipipe-discovery status [path]                -> read-only status
/haipipe-discovery open <type> <question>       -> scaffold a typed discovery-folder (type = Search | Review | Idea)
/haipipe-discovery open-group <slug>            -> ensure discovery-group dir
/haipipe-discovery plan <discovery>             -> (re)write discovery.yaml
/haipipe-discovery build <discovery>            -> author the optional instrument (build/)
/haipipe-discovery execute <discovery>          -> do the work, write the terminal file
/haipipe-discovery report <discovery>           -> write report block + status.yaml + site.md
/haipipe-discovery feedback "<text>"            -> capture skill feedback, ROUTED at capture to the bucket unit (else fallback); `feedback list [unit]` / `feedback move <file> <unit>`
/haipipe-discovery digest ["<session-name|id>"] [--dry-run]  -> digest a session (a named/id'd PAST session, or current): harvest feedback, dedup, confirm-gate, route to bucket-unit inboxes

/haipipe-discovery <bucket>                     -> list bucket workers
/haipipe-discovery <specialist> [args]          -> dispatch a bucket worker (one-off, NO folder)
/haipipe-discovery "<natural language>"         -> infer + dispatch
/haipipe-discovery pipeline [topic]             -> escalate /idea-discovery
```

---

Two Axes (the model)
--------------------

Discovery has the SAME two axes as task: a uniform lifecycle crossed with a folder type.

```
Axis 1 — LIFECYCLE (uniform; every folder runs it)   Plan -> Build(opt) -> Execute -> Report   (process verbs)
Axis 2 — TYPE      (what kind of folder this is)      Search · Review · Idea                    (folder kinds)
```

The two axes use non-overlapping vocabularies on purpose: the stages are process verbs every folder runs, the types name the kind of folder, and no word appears in both lists, so they can never be confused. The type names match their primary Execute bucket (Search -> 1_search + 2_read, Review -> 3_review, Idea -> 4_idea). Task = (Plan/Build/Execute/Report) × (data/nn/fit/...). Discovery = (Plan/Build/Execute/Report) × (Search/Review/Idea). Every type runs every stage; the type only changes what Execute produces.

The CANONICAL contract (per-stage IO, per-type terminal, the chain) lives in ONE place: `ref/lifecycle-map.md`. Field schema: `ref/discovery-yaml-schema.md`. Do not restate them here, edit those.

---

The Three Types (Axis 2, IPO: gather -> analyze -> create)
----------------------------------------------------------

```
type     IPO       Execute does                     terminal                    consumer
------   -------   ------------------------------   -------------------------   ---------------------
Search   INPUT     search + read source material    sources.md + notes.md       Review / Idea, reusable source base
Review   PROCESS   judge a claim OR map a field     verdict.md / landscape.md   probe (verdict) / paper (landscape)
Idea     OUTPUT    generate candidate claims        ideas.md                    probe-open / paper-seed
```

`Review` is the only type whose terminal branches; `role:` decides verdict (judge, a judgment -> probe) vs landscape (synthesize, a map -> paper). `Search` merges the old search + read (always bound together; the digested source set is a reusable, accumulating base). `Idea` stays separate because it is divergent (invent new) while Search/Review are convergent.

```
role -> type -> terminal
Search  source_gather, source_read                      -> sources.md (+ notes.md)
Review  prior_art_check, counterevidence, novelty_check  -> verdict.md   (judge -> probe)
Review  landscape_review, benchmark_landscape            -> landscape.md (synthesize -> paper)
Idea  idea_generation                                  -> ideas.md
```

A one-off capability call (just dispatch arxiv / alphaxiv / research-lit) does NOT create a folder; the discovery-folder is only for durable, project-tracked topics, the same split as a quick script vs a scaffolded task-folder.

---

Hierarchy
---------

```
task:       tasks/{G}{NN}_group/   ⊃  {NN}_taskname/   -> one runnable unit
discovery:  discoveries/<GROUP>/   ⊃  <NN>_<topic>/    -> one research topic
```

Project shape:

```
examples/<PROJECT>/
├── discoveries/
│   ├── L01_initial-landscape/        (parent = paper; Review synthesize + Idea)
│   │   ├── 01_landscape-review/       (type: Review, role: landscape_review -> landscape.md)
│   │   └── 02_novelty-check/          (type: Review, role: novelty_check -> verdict.md)
│   └── P01_rare-phenotype-lift/       (parent = probe; Search + Review judge)
│       ├── 01_source-base/            (type: Search -> sources.md + notes.md)
│       └── 02_prior-art/              (type: Review, role: prior_art_check -> verdict.md)
├── probes/
├── tasks/
├── paper/
└── applications/
```

Group letters are organizational hints, not the source of truth. `type:` (and `role:`) in `discovery.yaml` are authoritative.

Recommended group hints:

```
L  landscape / delivery-open discovery     (mostly Review synthesize, Idea)
P  probe-backed prior art or counterevidence (mostly Review judge, Search)
B  benchmark landscape                       (Review synthesize)
C  counterevidence                           (Review judge)
S  source reads / shared source base         (Search)
```

---

Buckets (the Execute-stage workers)
-----------------------------------

The four capability buckets do NOT change. They are the WORKERS invoked inside a folder's Execute stage. Workers (4, capability) and types (3, purpose) are different axes: `Search` uses 1_search + 2_read, `Review` uses 3_review, `Idea` uses 4_idea.

```
1_search   fetch papers / web        (used by Search, and inline inside Review/Idea)
  arxiv               preprint search + PDF download
  semantic-scholar    published venue + citations
  exa-search          broad web (blogs/news/docs)

2_read     consume one paper          (used by Search, and inline inside Review/Idea)
  alphaxiv            fast LLM summary
  deepxiv             progressive section reading
  paper-analyzer      deep structured note

3_review   analyze across sources     (used by Review: judge -> verdict, synthesize -> landscape)
  research-lit        default multi-source
  comm-lit-review     communications domain
  academic-researcher cross-discipline template

4_idea     ideate / validate          (Idea uses idea-creator)
  idea-creator        brainstorm + rank          -> Idea worker
  novelty-check       method novelty (查新)        -> a Review-JUDGE worker that happens to live here (writes verdict.md, not ideas.md)
```

Bucket aliases: `1|search`, `2|read`, `3|review`, `4|idea|novelty`. Note bucket 4 is the one place a bucket is NOT 1:1 with a type: `idea-creator` serves `Idea`, `novelty-check` serves `Review`.

---

Routing Logic
-------------

```
1. First positional is a lifecycle verb (open / open-group / plan / build / execute / report / status)
     -> durable discovery operation. The utility verbs `feedback` (capture | list | move)
        and `digest` are routed to fn/feedback.md / fn/digest.md BEFORE other parsing;
        first positional "feedback" -> target=feedback; first positional "digest" ->
        target=digest. Neither scaffolds a folder.
2. First positional is an existing path:
     discovery-folder -> run requested stage or full lifecycle.
     discovery-group  -> iterate/summarize child discovery-folders.
3. `open <type>` where type ∈ {Search, Review, Idea} -> scaffold that typed folder.
4. First positional is a specialist name -> dispatch the bucket worker directly (one-off, NO folder).
5. arXiv ID / arxiv URL in args -> 2_read bucket worker.
     "summarize|explain" -> alphaxiv ; "section|layered" -> deepxiv ; "analyze|claims" -> paper-analyzer
6. First positional is a bucket alias -> use that bucket.
7. Keyword scan (to pick a bucket worker for a one-off, or to infer a folder type):
     "preprint|arxiv"           -> arxiv          (Search)
     "IEEE|ACM|venue|citation"  -> semantic-scholar (Search)
     "web|blog|news|exa"        -> exa-search     (Search)
     "review|survey|landscape|related work" -> research-lit (Review synthesize)
     "prior art|does X exist|already done"   -> Review judge (verdict)
     "novelty|查新"             -> novelty-check  (Review judge)
     "brainstorm|find idea|找idea|propose"   -> idea-creator (Idea)
     "patent|专利"              -> hand off to D_patent/
     "pipeline|全流程|end-to-end" -> escalate /idea-discovery
8. Bucket resolved, specialist unresolved -> bucket default (arxiv | alphaxiv | research-lit | idea-creator).
9. Nothing resolves -> ask user to pick a lifecycle verb (durable) vs a bucket (one-off).

Dispatch: Skill(<specialist>, args="<remaining_args>"). Do not auto-chain.
         For any 3_review dispatch in service of a Review folder, APPEND the Review Output
         Contract (below) so the result is citation-matchable.

Utility-verb dispatch (handled inline, never scaffolds a folder):
  If target = feedback:
    Read fn/feedback.md and run it inline. Three sub-modes:
      - capture "<text>": infer the target unit (cross-cutting guard first, else
        keyword in text, else active type/stage from .discovery-console.yaml,
        else orchestrator fallback), write one dated file into THAT unit's
        feedback/ folder (create it + README if missing), then confirm where it
        landed + how it matched.
      - `feedback list [unit]`: aggregate open items across ALL feedback/ inboxes
        under the discovery layer root, grouped by unit.
      - `feedback move <file> <unit>`: re-route a mis-filed item.
    Capture is MERGE-OR-CREATE: a same-topic complaint updates the existing inbox
    file (append a dated recurrence, preserve prior wording verbatim, reopen if it
    was fixed) instead of spawning a duplicate, so inboxes stay self-limiting. This
    orchestrator handles feedback directly; no fix on the spot.
  Else if target = digest:
    Read fn/digest.md and run it inline. RESOLVE the target session first: no
    arg = the CURRENT session; "<session-name|id>" = a PAST session — locate its
    transcript .jsonl in this repo's ~/.claude/projects dir (id directly, or grep
    the store for the /rename'd name) and extract its human turns as the
    transcript to scan. Then scan for tool/skill feedback, distill discrete items,
    dedup (within-batch + against inboxes via the same-topic test), PRESENT for a
    mandatory confirm gate, then route each approved item through the feedback
    capture (merge-or-create). Honor --dry-run (present only, file nothing). Flag
    global behavioral prefs for /remember rather than filing them. Never
    auto-files. Best run from a fresh session for clean context.
```

---

Step-by-Step Protocol (durable project work)
--------------------------------------------

Walk the lifecycle stages; do not hand-place a completed discovery package.

Step 0: Resolve project root = nearest ancestor with tasks/, paper/, applications/, probes/, or _haipipe/. If ambiguous, ask (AUTO -> blocked).

Step 1: Resolve scope.
```
existing discovery-folder (has discovery.yaml) -> run requested stage or full lifecycle
existing discovery-group   (under discoveries/, holds folders, no discovery.yaml at root) -> summarize/iterate
open-group <slug>          -> create discoveries/<GROUP_slug>/ container only
open <type> <question>     -> scaffold discoveries/<GROUP_slug>/<NN_slug>/ as a typed folder
specialist                 -> one-off bucket worker (NO folder)
```

Step 2: Choose discovery-group (letter hint by parent: paper/application -> L; probe -> P; benchmark -> B; counterevidence -> C; shared source base -> S). Pick the next free two-digit id within that letter; do not renumber.

Step 3: Choose discovery-folder: next free `NN_<slug>/` in the group. One topic per folder.

Step 4: Run lifecycle stages (Axis 1). Each stage owns its files.
```
Plan:
  write discovery.yaml: type (Search/Review/Idea) + role + question + sources + expected_outputs (terminal by type)
  write status.yaml (planned) + site.md
  append discovery.opened to _haipipe/project.log.jsonl

Build (OPTIONAL — skip for a quick lookup):
  author the instrument under build/ (query strategy / extraction schema / synthesis rubric)
  reference it from discovery.yaml; set status building

Execute (dispatch the bucket worker for the type):
  Search  -> 1_search + 2_read   : write sources.md + notes.md
  Review  -> 3_review            : write verdict.md (judge) or landscape.md (synthesize), per role; sources.md/notes.md are work products
  Idea  -> 4_idea              : write ideas.md
  inspect local project evidence first unless the user asks for fresh web search
  set status executing

Report (report to a human):
  write the discovery.yaml report block (report.outcome/summary/confidence; supports/contradicts for Review-judge).
  report.outcome is the per-type result; do NOT confuse it with the top-level lifecycle status.
  finalize status.yaml (ok / inconclusive / blocked) + site.md
  append discovery.completed to _haipipe/project.log.jsonl

Post-handoff (part of Report when a parent exists):
  verify the parent path exists; add it to discovery.yaml consumed_by only after the terminal + parent exist
  if parent missing, leave consumed_by unchanged and report blocked: missing_parent=<path>
  update _haipipe/project.status.yaml; append discovery.consumed to _haipipe/project.log.jsonl
```

YAML timestamps MUST be quoted strings (e.g. `"2026-06-22T15:05:00-04:00"`). JSONL: one JSON object per non-empty line, no blank lines.

Step 5: Return structured result.
```
status: ok | blocked | failed
discovery_group: <project-relative path>
discovery_folder: <project-relative path>
type: Search | Review | Idea
files_written: [...]
next: what should consume the terminal
```

---

Review Output Contract (Review — research-lit / comm-lit-review / academic-researcher)
---------------------------------------------------------------------------------

Append this to the args of any review-bucket dispatch in service of a `Review` folder. Short author-year tags alone are NOT matchable by the reader. Every analysis MUST satisfy all five rules.

```
1. FULL NAMES, never bare tags. Each paper gets a FULL citation on first mention AND a line in
   the reference list: full title (verbatim), full author list (first three + et al. only when
   >= 6 authors), venue with vol(issue):pages or "arXiv preprint"/status, year + a LOCATOR
   (arXiv ID / DOI / URL). A short tag in prose is OK only if it maps to exactly one full entry.
2. NUMBERED REFERENCE LIST at the end ("References (full, verified)"): one self-contained,
   deduped line per paper; any in-text mention matches exactly one numbered entry.
3. DISAMBIGUATE COLLISIONS. Same author+year papers each get a distinguishing nickname in EVERY
   mention (Lu et al. 2025a vs Lu et al. 2025b). Never leave two papers both as "Lu 2025".
4. ONE-LINE PLAIN FINDING per paper (jargon-free).
5. VERIFICATION FLAG per paper: VERIFIED (id/DOI/venue confirmed via search) vs NEEDS-VERIFICATION.
   Never assert an unchecked citation; fabrication is the worst failure.
```

For deeper rigor (systematic search + adversarial citation verification), escalate to the deep-research lit-review pipeline (`Tools/plugin-workflows/academic-research-skills/deep-research`, mode `lit-review`).

---

Dashboard (no-arg)
------------------

```
Durable lifecycle (Plan -> Build(opt) -> Execute -> Report):
  status [path]
  open <type> <question>      (type = Search | Review | Idea)
  open-group <slug>
  plan | build | execute | report <discovery>
  feedback "<text>" | feedback list [unit] | feedback move <file> <unit>   (routed at capture)
  digest ["<session-name|id>"] [--dry-run]   (harvest a session's feedback — past named/id'd or current — dedup, confirm-gate, route to inboxes)

Types:  Search (-> sources.md/notes.md)  ·  Review (-> verdict.md / landscape.md)  ·  Idea (-> ideas.md)

Bucket workers (Execute stage):
  1_search   arxiv | semantic-scholar | exa-search
  2_read     alphaxiv | deepxiv | paper-analyzer
  3_review   research-lit | comm-lit-review | academic-researcher
  4_idea     idea-creator | novelty-check

Pipeline:  /idea-discovery   (research-lit -> idea-creator -> novelty-check)
```

Suggest the most likely next command based on context.

---

Feedback (capture skill feedback, route at capture, fix later)
--------------------------------------------------------------

Capture a complaint / confusion / wish about the discovery SKILL itself, ROUTED at capture time to the specific bucket unit it concerns (else the orchestrator fallback). Capture-only: filing never fixes on the spot; fixing is a separate revision pass. Feedback is about the TOOL, not a discovery finding (sources / verdict / landscape / ideas). The folder a file lives in IS the record of which unit it concerns; there is no `skill:` field. Full contract (routing, inbox paths, merge-or-create, schema): `fn/feedback.md`.

The routable UNIT is the BUCKET FOLDER, plus the shared `agents/` folder:
```
1_search   search, find paper, arxiv, semantic scholar, exa, sources.md  -> 1_search/feedback/
2_read     read, summarize paper, alphaxiv, deepxiv, analyze, notes       -> 2_read/feedback/
3_review   review, lit review, landscape, verdict, synthesize, novelty    -> 3_review/feedback/
4_idea     idea, idea-creator, generate ideas, ideas.md                   -> 4_idea/feedback/
agents     creator/orchestrator/reviewer agent, dispatch                  -> agents/feedback/
--------------------------------------------------------------------------------------------
cross-cutting (the Plan/Build/Execute/Report lifecycle, the Search/Review/Idea
type field, the discovery.yaml schema, the stage strip; true across all types)
                                                          -> orchestrator fallback (this folder)
```

Three sub-modes:
```
capture   /haipipe-discovery feedback "<text>"
          -> resolve order: (0) CROSS-CUTTING GUARD first, a SEMANTIC test: is the
             rule true across ALL types/stages, or does it name a cross-cutting
             concern? -> fallback, overriding any keyword. (1) keyword -> unit
             (most specific wins). (2) active type/stage context. (3) fallback.
             MERGE into a same-topic file or CREATE a new dated file in THAT unit's
             feedback/ (created LAZILY); confirm merged-vs-new + the one-line move.
list      /haipipe-discovery feedback list [unit]
          -> AGGREGATE across ALL feedback/ inboxes under the discovery layer root
             (`find skills/discovery -type d -name feedback`, grep `status: open`),
             newest-first, grouped by unit; [unit] restricts to one inbox.
move      /haipipe-discovery feedback move <file> <unit>
          -> re-route a mis-filed item to the right unit's inbox (pure file move).
digest    /haipipe-discovery digest ["<session-name|id>"] [--dry-run]
          -> the bulk harvester: digest a session (a named/id'd PAST session run
             from fresh context, or the current one with no arg), scanning the
             transcript for feedback you gave conversationally, distilling +
             deduping items, and (after a MANDATORY confirm gate) routing each
             through the same capture. Files only skill-feedback; global behavioral
             prefs are flagged for `/remember`, not filed. Honors --dry-run. Full
             contract: `fn/digest.md`.
```

Resolve happens in a revision pass: set status: fixed + fixed_in: <version> + a one-line Fix note (keep the file as history). Full contract: `fn/feedback.md`, `fn/digest.md`; fallback inbox conventions: `feedback/README.md`.

---

Escalation to Pipelines
-----------------------

Single-step router. For multi-step orchestration, hand off:
```
/idea-discovery     full idea pipeline (research-toolkit Workflow 1)
/research-pipeline  end-to-end (idea -> experiments -> paper)
/patent-pipeline    patent track
```
Trigger phrases: "pipeline", "全流程", "end-to-end", "chain these", "all together".

---

Disambiguation
--------------

```
Bare arXiv ID, no verb     -> /alphaxiv (one-off 2_read)
"find X": X=sources        -> open Search ; X=idea -> open Idea
"is X known / does X exist"-> open Review (role: prior_art_check)
"map the field on X"       -> open Review (role: landscape_review)
Topic clear, type unclear  -> ask: Search (gather) / Review (judge or map) / Idea (ideas)?
```

---

Shared Resources / Cross-Domain
-------------------------------

```
0_venue/    venue filter data (utd24-is-venues.md) — read by research-lit / novelty-check / idea-creator.
D_patent/   patent work. Skills: /prior-art-search, /patent-novelty-check, /patent-review,
            /jurisdiction-format, /specification-writing. Full flow: /patent-pipeline.
```

Legacy: (a) before v2.1.0 the three type values were the glyphs 搜/析/创 — read them as `Search`/`Review`/`Idea` respectively (migrate on next edit). (b) older discovery-folders that use `role:` + a `verdict:` block with no `type:` remain readable: treat a missing `type:` as `Review` and a `verdict.md` as its terminal.

---

## Feedback

A `feedback` first-token is a utility verb: route it to `fn/feedback.md` BEFORE any other parsing (it is not a lifecycle verb and never scaffolds a discovery-folder). It captures a complaint / confusion / wish about THIS skill, ROUTED at capture time to the bucket unit it concerns (else the orchestrator fallback), to fix in a later revision pass, never on the spot. Three sub-modes:

```
feedback "<text>"            -> capture: infer the unit (cross-cutting guard -> keyword
                                -> active context -> fallback), merge-or-create a dated
                                file in THAT unit's feedback/, confirm where it landed.
feedback list [unit]         -> aggregate open items across ALL feedback/ inboxes under
                                skills/discovery (grouped by unit); [unit] restricts.
feedback move <file> <unit>  -> re-route a mis-filed item to the right unit's inbox.
digest ["<session-name|id>"] [--dry-run]
                             -> harvest a session (named/id'd PAST or current): scan
                                the transcript, distill + dedup feedback, confirm-gate,
                                route each through capture.
```

The routable unit is the BUCKET FOLDER (1_search / 2_read / 3_review / 4_idea) or the shared `agents/`; cross-cutting items (lifecycle, the Search/Review/Idea type field, discovery.yaml schema, stage strip) fall back to the orchestrator's own `feedback/`. The folder a file lives in IS the record of which unit it concerns. Full contract: `fn/feedback.md`; fallback inbox: `feedback/README.md`.

`/haipipe-discovery digest ["<session-name|id>"] [--dry-run]` is the bulk harvester: it digests a session — a named/id'd PAST session run from fresh context, or the current one if given no argument — scanning the transcript for feedback you gave conversationally, distilling + deduping the discrete items, and (after a MANDATORY confirm gate) routing each through the same capture. It files only skill-feedback; global behavioral preferences are flagged for `/remember`, not filed. Route a `digest` first-token to it before other parsing (it never scaffolds a discovery-folder). Full conventions: `fn/feedback.md` (cross-cutting guard -> keyword -> context -> fallback map, inbox paths, merge-or-create, schema) and `fn/digest.md` (session resolution + harvest); fallback inbox: `feedback/README.md`.

## Behavioral Preferences (portable)

ALWAYS read and honor `PREFERENCES.md` in this skill's own folder: git-tracked
global behavioral preferences (e.g. communicate via ASCII diagrams) that survive a
machine change, unlike the machine-local `~/.claude` auto-memory. Global behavioral
prefs are kept in sync across all orchestrators by `/haipipe-paper digest`'s
global-pref fan-out (merge-or-create; one entry per topic).
