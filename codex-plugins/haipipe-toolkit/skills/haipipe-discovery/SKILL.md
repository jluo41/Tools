---
name: haipipe-discovery
description: "Router and durable lifecycle for the discovery (external-evidence) layer. A discovery is one research topic = one folder, a sibling of a task-folder, running the uniform Plan -> Build(opt) -> Execute -> Report lifecycle across 3 folder types: 搜 (source = search+read -> sources.md/notes.md), 析 (analyze = judge a claim -> verdict.md, or synthesize a field -> landscape.md), 创 (idea -> ideas.md). The 4 capability buckets (search/read/review/idea via arxiv/semantic-scholar/exa/alphaxiv/research-lit/idea-creator/novelty-check) are the Execute-stage workers. Trigger: discover, find paper, lit review, 找idea, 查新, source, verdict, landscape, /haipipe-discovery."
argument-hint: "[verb|type] [discovery] [args...]"
allowed-tools: Bash, Read, Grep, Glob, Skill
metadata:
  version: "2.0.0"
  last_updated: "2026-06-22"
  summary: "Two-axis discovery: uniform Plan/Build/Execute/Report lifecycle x 3 folder types (搜/析/创), mirroring task. Capability buckets are the Execute workers."
  changelog:
    - "1.0.0 (2026-05-31): baseline metadata added."
    - "1.6.0 (2026-06-21): ref/lifecycle-map.md canonical verb table; retire narrative parent; folder renamed discover -> discovery."
    - "1.7.0 (2026-06-21): a discovery is one research topic = its own FOLDER mirroring a task-folder."
    - "1.8.0 (2026-06-21): rename skill haipipe-discover -> haipipe-discovery."
    - "1.9.0 (2026-06-22): add feedback utility verb + feedback/ inbox."
    - "2.0.0 (2026-06-22): TWO-AXIS redesign mirroring task. Lifecycle is now the uniform Plan -> Build(opt) -> Execute -> Report (retires open/search/read/review/post). search/read/review/idea are no longer stage verbs; the folder TYPE is one of 3 Chinese-char types 搜/析/创 (搜=search+read source, 析=judge|synthesize, 创=idea). verdict block renamed to report (report-to-human). The 4 capability buckets become the Execute-stage workers. See ref/lifecycle-map.md + ref/discovery-yaml-schema.md."
---

Skill: haipipe-discovery (orchestrator)
======================================

Single entry for the discovery layer: what the outside world already knows (`搜` gather, `析` analyze) and the new angles drawn from it (`创` create). Multi-step idea pipelines still escalate to `/idea-discovery`.

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
/haipipe-discovery open <type> <question>       -> scaffold a typed discovery-folder (type = 搜 | 析 | 创)
/haipipe-discovery open-group <slug>            -> ensure discovery-group dir
/haipipe-discovery plan <discovery>             -> (re)write discovery.yaml
/haipipe-discovery build <discovery>            -> author the optional instrument (build/)
/haipipe-discovery execute <discovery>          -> do the work, write the terminal file
/haipipe-discovery report <discovery>           -> write report block + status.yaml + site.md
/haipipe-discovery feedback "<text>"            -> capture skill feedback (fix later); `feedback list` shows open items

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
Axis 1 — LIFECYCLE (uniform; every folder runs it)   Plan -> Build(opt) -> Execute -> Report   (English)
Axis 2 — TYPE      (what kind of folder this is)      搜 · 析 · 创                              (Chinese)
```

The type axis is named in Chinese single characters and the stage axis in English on purpose: different alphabets mean the two can never be confused. Task = (Plan/Build/Execute/Report) × (data/nn/fit/...). Discovery = (Plan/Build/Execute/Report) × (搜/析/创). Every type runs every stage; the type only changes what Execute produces.

The CANONICAL contract (per-stage IO, per-type terminal, the chain) lives in ONE place: `ref/lifecycle-map.md`. Field schema: `ref/discovery-yaml-schema.md`. Do not restate them here, edit those.

---

The Three Types (Axis 2, IPO: gather -> analyze -> create)
----------------------------------------------------------

```
字   type      IPO       Execute does                     terminal              consumer
--   -------   -------   ------------------------------   -------------------   ---------------------
搜   source    INPUT     search + read source material    sources.md+notes.md   析 / 创, reusable source base
析   analyze   PROCESS   judge a claim OR map a field     verdict.md / landscape.md   probe (verdict) / paper (landscape)
创   create    OUTPUT    generate candidate claims        ideas.md              probe-open / paper-seed
```

`析` is the only type whose terminal branches; `role:` decides verdict (判, a judgment -> probe) vs landscape (综, a map -> paper). `搜` merges the old search + read (always bound together; the digested source set is a reusable, accumulating base). `创` stays separate because it is divergent (invent new) while 搜/析 are convergent.

```
role -> type -> terminal
搜  source_gather, source_read                      -> sources.md (+ notes.md)
析  prior_art_check, counterevidence, novelty_check  -> verdict.md   (判 -> probe)
析  landscape_review, benchmark_landscape            -> landscape.md (综 -> paper)
创  idea_generation                                  -> ideas.md
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
│   ├── L01_initial-landscape/        (parent = paper; 析 综 + 创)
│   │   ├── 01_landscape-review/       (type: 析, role: landscape_review -> landscape.md)
│   │   └── 02_novelty-check/          (type: 析, role: novelty_check -> verdict.md)
│   └── P01_rare-phenotype-lift/       (parent = probe; 搜 + 析 判)
│       ├── 01_source-base/            (type: 搜 -> sources.md + notes.md)
│       └── 02_prior-art/              (type: 析, role: prior_art_check -> verdict.md)
├── probes/
├── tasks/
├── paper/
└── applications/
```

Group letters are organizational hints, not the source of truth. `type:` (and `role:`) in `discovery.yaml` are authoritative.

Recommended group hints:

```
L  landscape / delivery-open discovery     (mostly 析 综, 创)
P  probe-backed prior art or counterevidence (mostly 析 判, 搜)
B  benchmark landscape                       (析 综)
C  counterevidence                           (析 判)
S  source reads / shared source base         (搜)
```

---

Buckets (the Execute-stage workers)
-----------------------------------

The four capability buckets do NOT change. They are the WORKERS invoked inside a folder's Execute stage. Workers (4, capability) and types (3, purpose) are different axes: `搜` uses 1_search + 2_read, `析` uses 3_review, `创` uses 4_idea.

```
1_search   fetch papers / web        (used by 搜, and inline inside 析/创)
  arxiv               preprint search + PDF download
  semantic-scholar    published venue + citations
  exa-search          broad web (blogs/news/docs)

2_read     consume one paper          (used by 搜, and inline inside 析/创)
  alphaxiv            fast LLM summary
  deepxiv             progressive section reading
  paper-analyzer      deep structured note

3_review   analyze across sources     (used by 析: judge -> verdict, synthesize -> landscape)
  research-lit        default multi-source
  comm-lit-review     communications domain
  academic-researcher cross-discipline template

4_idea     ideate / validate          (创 uses idea-creator)
  idea-creator        brainstorm + rank          -> 创 worker
  novelty-check       method novelty (查新)        -> a 析-JUDGE worker that happens to live here (writes verdict.md, not ideas.md)
```

Bucket aliases: `1|search`, `2|read`, `3|review`, `4|idea|novelty`. Note bucket 4 is the one place a bucket is NOT 1:1 with a type: `idea-creator` serves `创`, `novelty-check` serves `析`.

---

Routing Logic
-------------

```
1. First positional is a lifecycle verb (open / open-group / plan / build / execute / report / status)
     -> durable discovery operation. The utility verb `feedback` captures skill feedback.
2. First positional is an existing path:
     discovery-folder -> run requested stage or full lifecycle.
     discovery-group  -> iterate/summarize child discovery-folders.
3. `open <type>` where type ∈ {搜, 析, 创} -> scaffold that typed folder.
4. First positional is a specialist name -> dispatch the bucket worker directly (one-off, NO folder).
5. arXiv ID / arxiv URL in args -> 2_read bucket worker.
     "summarize|explain" -> alphaxiv ; "section|layered" -> deepxiv ; "analyze|claims" -> paper-analyzer
6. First positional is a bucket alias -> use that bucket.
7. Keyword scan (to pick a bucket worker for a one-off, or to infer a folder type):
     "preprint|arxiv"           -> arxiv          (搜)
     "IEEE|ACM|venue|citation"  -> semantic-scholar (搜)
     "web|blog|news|exa"        -> exa-search     (搜)
     "review|survey|landscape|related work" -> research-lit (析 综)
     "prior art|does X exist|already done"   -> 析 判 (verdict)
     "novelty|查新"             -> novelty-check  (析 判)
     "brainstorm|find idea|找idea|propose"   -> idea-creator (创)
     "patent|专利"              -> hand off to D_patent/
     "pipeline|全流程|end-to-end" -> escalate /idea-discovery
8. Bucket resolved, specialist unresolved -> bucket default (arxiv | alphaxiv | research-lit | idea-creator).
9. Nothing resolves -> ask user to pick a lifecycle verb (durable) vs a bucket (one-off).

Dispatch: Skill(<specialist>, args="<remaining_args>"). Do not auto-chain.
         For any 3_review dispatch in service of a 析 folder, APPEND the Review Output
         Contract (below) so the result is citation-matchable.
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
  write discovery.yaml: type (搜/析/创) + role + question + sources + expected_outputs (terminal by type)
  write status.yaml (planned) + site.md
  append discovery.opened to _haipipe/project.log.jsonl

Build (OPTIONAL — skip for a quick lookup):
  author the instrument under build/ (query strategy / extraction schema / synthesis rubric)
  reference it from discovery.yaml; set status building

Execute (dispatch the bucket worker for the type):
  搜  -> 1_search + 2_read   : write sources.md + notes.md
  析  -> 3_review            : write verdict.md (判) or landscape.md (综), per role; sources.md/notes.md are work products
  创  -> 4_idea              : write ideas.md
  inspect local project evidence first unless the user asks for fresh web search
  set status executing

Report (report to a human):
  write the discovery.yaml report block (report.outcome/summary/confidence; supports/contradicts for 析-judge).
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
type: 搜 | 析 | 创
files_written: [...]
next: what should consume the terminal
```

---

Review Output Contract (析 — research-lit / comm-lit-review / academic-researcher)
---------------------------------------------------------------------------------

Append this to the args of any review-bucket dispatch in service of a `析` folder. Short author-year tags alone are NOT matchable by the reader. Every analysis MUST satisfy all five rules.

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
  open <type> <question>      (type = 搜 | 析 | 创)
  open-group <slug>
  plan | build | execute | report <discovery>
  feedback "<text>" | feedback list

Types:  搜 source (-> sources.md/notes.md)  ·  析 analyze (-> verdict.md / landscape.md)  ·  创 idea (-> ideas.md)

Bucket workers (Execute stage):
  1_search   arxiv | semantic-scholar | exa-search
  2_read     alphaxiv | deepxiv | paper-analyzer
  3_review   research-lit | comm-lit-review | academic-researcher
  4_idea     idea-creator | novelty-check

Pipeline:  /idea-discovery   (research-lit -> idea-creator -> novelty-check)
```

Suggest the most likely next command based on context.

---

Feedback (capture skill feedback, fix later)
--------------------------------------------

Capture a complaint / confusion / wish about the discovery SKILL itself into `feedback/`. Capture-only: filing never fixes on the spot; fixing is a separate revision pass. Feedback is about the TOOL, not a discovery finding.

Capture: `/haipipe-discovery feedback "<text>"`
```
1. Write feedback/<YYYY-MM-DD>_<short-slug>.md
   frontmatter: status: open | created | context (stage/type or "general") | fixed_in: ""
   body: the feedback in the reporter's words, then a trailing "Fix:" line.
2. Confirm captured. Do NOT attempt a fix now.
```

List: `/haipipe-discovery feedback list` -> grep feedback/*.md for `status: open`, print newest-first with context.

Resolve happens in a revision pass: set status: fixed + fixed_in: <version> + a one-line Fix note. Full contract: `feedback/README.md`.

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
"find X": X=sources        -> open 搜 ; X=idea -> open 创
"is X known / does X exist"-> open 析 (role: prior_art_check)
"map the field on X"       -> open 析 (role: landscape_review)
Topic clear, type unclear  -> ask: 搜 (gather) / 析 (judge or map) / 创 (ideas)?
```

---

Shared Resources / Cross-Domain
-------------------------------

```
0_venue/    venue filter data (utd24-is-venues.md) — read by research-lit / novelty-check / idea-creator.
D_patent/   patent work. Skills: /prior-art-search, /patent-novelty-check, /patent-review,
            /jurisdiction-format, /specification-writing. Full flow: /patent-pipeline.
```

Legacy: old discovery-folders that use `role:` + a `verdict:` block with no `type:` remain readable. Treat a missing `type:` as `析` and a `verdict.md` as its terminal; migrate lazily on next edit.

---

## Feedback

`/haipipe-discovery feedback "<text>"` captures a complaint / confusion / wish about THIS skill into `feedback/` (one dated file per item, `status: open`) to fix in a later revision pass. `/haipipe-discovery feedback list` shows the open items. Route a `feedback` first-token here before other parsing. Full convention: `feedback/README.md`.
