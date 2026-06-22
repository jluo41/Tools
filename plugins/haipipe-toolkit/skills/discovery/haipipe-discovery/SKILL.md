---
name: haipipe-discovery
description: "Router for Stage A (discovery) literature/idea discovery. Dispatches to 1 of 4 buckets: search (arxiv/semantic-scholar/exa-search), read (alphaxiv/deepxiv/paper-analyzer), review (research-lit/comm-lit-review/academic-researcher), idea (idea-creator/novelty-check). Pipelines escalate to /idea-discovery. Patent work lives in D_patent/. Trigger: discover, find paper, lit review, 找idea, 查新, /haipipe-discovery."
argument-hint: "[bucket] [specialist] [args...]"
allowed-tools: Bash, Read, Grep, Glob, Skill
metadata:
  version: "1.9.0"
  last_updated: "2026-06-22"
  summary: "Single entry for discovery: capability router plus per-topic discovery-folders (mirror task-folders)."
  changelog:
    - "1.0.0 (2026-05-31): baseline metadata added."
    - "1.1.0 (2026-06-01): added Review Output Contract (3_review) — full citations, numbered reference list, same-author/year disambiguation, plain-language finding, per-paper verification flag; router appends it to review-bucket dispatches."
    - "1.2.0 (2026-06-19): define discoveries/ as project-level external-evidence work, sibling to tasks/ and referenced by probes."
    - "1.3.0 (2026-06-19): split capability router from durable discovery artifact contract; add ref/discovery-yaml-schema.md."
    - "1.4.0 (2026-06-20): add discovery-group/discovery-folder hierarchy and one-interface lifecycle: open/search/read/review/verdict/post."
    - "1.5.0 (2026-06-20): make one markdown file the default durable artifact; folderized discovery becomes an opt-in heavy mode."
    - "1.6.0 (2026-06-21): add ref/lifecycle-map.md as the canonical verb table (SKILL/DESIGN point to it, not restate it); retire the narrative parent (parents are now delivery paper/application or probe); folder renamed discover -> discovery."
    - "1.7.0 (2026-06-21): revert v1.5 single-file default. A discovery is one research topic = its own FOLDER (discovery.yaml + sources/notes/verdict + status/site), mirroring a task-folder; lifecycle-map.md recast as open -> search -> read -> review/idea -> post filling the folder's IO files."
    - "1.8.0 (2026-06-21): rename skill haipipe-discover -> haipipe-discovery to match the haipipe-<noun> sibling convention; inner folder, refs, and command (/haipipe-discovery) updated."
    - "1.9.0 (2026-06-22): add the feedback utility verb + feedback/ inbox (mirrors probe). /haipipe-discovery feedback captures skill feedback (capture-only), feedback list reviews open items; fixing is a separate revision pass."
---

Skill: haipipe-discovery (orchestrator)
======================================

Single entry for Stage A / the discovery layer. Multi-step idea pipelines
still escalate to `/idea-discovery`.

This skill has two modes:

```
1. Durable project work
   Operate on per-topic discovery-folders under
   examples/<PROJECT>/discoveries/.

2. Capability routing
   Dispatch to search/read/review/idea specialists for one-off discovery, or
   for work inside the current discovery-folder.
```

In project workflows, discovery is **external evidence work**. It is not a
task execution stage. When a discovery needs to become durable project
evidence, write it under `discoveries/` and let probes or delivery lifecycles
(paper/application) reference it the same way probes reference tasks:

```
Probe-open
  dispatches discoveries/   "what does the outside world already know?"
  dispatches tasks/         "what do our own runs show?"

Probe-post
  harvests both discovery evidence and task evidence before judging the claim.
```

Invocation:
```
/haipipe-discovery                              -> dashboard
/haipipe-discovery <discovery>                  -> run full lifecycle on a folder
/haipipe-discovery <discovery-group>            -> iterate/summarize children
/haipipe-discovery status [path]                -> read-only status
/haipipe-discovery open <role> <question>       -> scaffold discovery-folder
/haipipe-discovery open-group <slug>            -> ensure discovery-group dir
/haipipe-discovery search <discovery>           -> write sources.md
/haipipe-discovery read <discovery>             -> write notes.md
/haipipe-discovery review <discovery>           -> write verdict.md (or idea)
/haipipe-discovery post <discovery>             -> link verdict to parent if it exists
/haipipe-discovery feedback "<text>"            -> capture skill feedback to feedback/ (fix later); `feedback list` shows open items

/haipipe-discovery <bucket>                     -> list specialists
/haipipe-discovery <specialist> [args]          -> dispatch specialist
/haipipe-discovery "<natural language>"         -> infer + dispatch
/haipipe-discovery pipeline [topic]             -> escalate /idea-discovery
```

---

Hierarchy
---------

Discovery mirrors task: a discovery is one research topic stored as its own
FOLDER, the way a task is one runnable unit stored as its own folder.

```
Task:      tasks/{G}{NN}_group/   ⊃  {NN}_taskname/   -> one runnable unit
Discovery: discoveries/<GROUP>/   ⊃  <NN>_<topic>/    -> one research topic
```

Definitions:

```
discovery-group    A directory grouping related research topics.
discovery-folder   One research topic = one folder (discovery.yaml + sources.md
                   / notes.md / verdict.md + status.yaml / site.md). Its IO files
                   mirror a task-folder's configs / results / runtime / notebooks.
source row         One paper/webpage/report/dataset citation inside sources.md.
```

Project shape:

```
examples/<PROJECT>/
├── discoveries/
│   ├── L01_initial-landscape/
│   │   ├── 01_landscape-review/
│   │   └── 02_novelty-check/
│   └── P01_rare-phenotype-lift/
│       ├── 01_prior-art/
│       └── 02_benchmark-landscape/
├── probes/
├── tasks/
├── paper/
└── applications/
```

Group letters are organizational hints, not the source of truth. The `role:`
in `discovery.yaml` is authoritative.

Recommended group hints:

```
L  landscape / delivery-open discovery
P  probe-backed prior art or counterevidence
B  benchmark landscape
C  counterevidence
S  source reads
```

A one-off capability call (just dispatch arxiv / alphaxiv / research-lit) does
NOT create a folder; the discovery-folder is only for durable, project-tracked
topics, the same split as a quick script vs a scaffolded task-folder.

---

Discovery Lifecycle
-------------------

A discovery is one research topic = one folder. The lifecycle fills the folder's
IO files, the way a task-folder's results are filled by its runs:

```
open  ->  search  ->  read  ->  review (or idea)  ->  post
```

```
discoveries/<GROUP>/<NN>_<topic>/
├── discovery.yaml   spec (open)         ↔ task configs/<run>.yaml
├── sources.md       search -> 1_search
├── notes.md         read   -> 2_read
├── verdict.md       review -> 3_review  (or idea -> 4_idea)
├── status.yaml      machine snapshot    ↔ task runtime.yaml
└── site.md          human panel         ↔ task notebooks/<run>.ipynb
```

The CANONICAL per-stage contract (skill, files_in, files_out, parent model)
lives in ONE place: `haipipe-discovery/ref/lifecycle-map.md`. Do not restate it
here or in DESIGN.md; edit the map. In short: `open` scaffolds the folder,
`search/read/review` fill the IO files, and `post` makes the verdict available
to the parent delivery lifecycle (paper/application) or probe without judging
the claim. Heavy source artifacts (PDFs, HTML snapshots) go in an optional
`sources/` subfolder.

---

Buckets
-------

```
1_search   fetch papers / web
  arxiv               preprint search + PDF download
  semantic-scholar    published venue + citations
  exa-search          broad web (blogs/news/docs)

2_read     consume one paper (input: arXiv ID/URL)
  alphaxiv            fast LLM summary
  deepxiv             progressive section reading
  paper-analyzer      deep structured note

3_review   topic landscape
  research-lit        default multi-source
  comm-lit-review     communications domain
  academic-researcher cross-discipline template

4_idea     ideate / validate (academic)
  idea-creator        brainstorm + rank
  novelty-check       method novelty (查新)
```

Bucket aliases: `1|search`, `2|read`, `3|review`, `4|idea|novelty`.


Project Discovery Folder
------------------------

Use a discovery-folder when output is part of a probe or delivery
(paper/application) stack:

```
examples/<PROJECT>/
├── discoveries/
│   ├── P01_robustness-claim/
│   │   └── 01_noisy-labels-prior-art/
│   │       ├── discovery.yaml
│   │       ├── sources.md
│   │       ├── notes.md
│   │       ├── verdict.md
│   │       ├── status.yaml
│   │       └── site.md
│   └── L01_initial-landscape/
```

`discovery.yaml` is the spec (question · parent · role · requested sources ·
expected_outputs · verdict block). Full field schema:
`ref/discovery-yaml-schema.md`.

A discovery-folder contains evidence and citations, not code/runs/metrics. The
project-wide event log remains `_haipipe/project.log.jsonl`; the folder's own
`status.yaml` / `site.md` are per-topic snapshots (like a task-folder's), not
event logs.

Parent contracts:

```
Delivery-triggered discovery
  parent.type = paper | application
  use: landscape_review, novelty_check, benchmark_landscape
  consumer: delivery lifecycle open need

Probe-triggered discovery
  parent.type = probe
  use: prior_art_check, counterevidence, source_read, benchmark_landscape
  consumer: Probe-post
```

---

Routing Logic
-------------

```
1. First positional is a lifecycle verb    -> durable discovery operation.
   The utility verb `feedback` captures skill feedback into feedback/ (fix later).
2. First positional is an existing path:
     discovery-folder -> run requested stage or full lifecycle.
     discovery-group  -> iterate/summarize child discovery-folders.
3. First positional is a specialist name  -> dispatch directly.
4. arXiv ID / arxiv URL in args            -> 2_read.
     "summarize|explain"   -> alphaxiv (default)
     "section|layered"     -> deepxiv
     "analyze|claims"      -> paper-analyzer
5. First positional is a bucket alias      -> use that bucket.
6. Keyword scan:
     "preprint|arxiv"           -> arxiv
     "IEEE|ACM|venue|citation"  -> semantic-scholar
     "web|blog|news|exa"        -> exa-search
     "review|survey|related work" + comms   -> comm-lit-review
     "review|survey|related work" (default) -> research-lit
     "brainstorm|find idea|找idea"           -> idea-creator
     "novelty|查新"                          -> novelty-check
     "patent|专利|prior art"                  -> hand off to D_patent/
     "pipeline|全流程|end-to-end"             -> escalate /idea-discovery
7. Bucket resolved, specialist unresolved -> use bucket default
   (arxiv | alphaxiv | research-lit | idea-creator).
8. Nothing resolves -> ask user to pick lifecycle vs specialist bucket.

Dispatch: Skill(<specialist>, args="<remaining_args>"). Do not auto-chain.
         For any 3_review dispatch, APPEND the Review Output Contract
         (below) to args so the result is citation-matchable.
```

---

Step-by-Step Protocol
---------------------

Use this protocol whenever `/haipipe-discovery` is used for durable project
work. Do not hand-place a completed discovery package without walking the
lifecycle stages.

Step 0: Resolve project root.

```
Project root = nearest ancestor containing tasks/, paper/, applications/, probes/,
or _haipipe/. If ambiguous, ask. In AUTO mode, return blocked.
```

Step 1: Resolve scope.

```
existing discovery:
  path is a discovery-folder (contains discovery.yaml)
  -> run requested stage or full lifecycle

existing discovery-group:
  path is under discoveries/, contains discovery-folders, and is not itself a
  discovery-folder (no discovery.yaml at its root) -> summarize/iterate

open-group:
  create discoveries/<GROUP_slug>/ only (a container dir).

open:
  scaffold discoveries/<GROUP_slug>/<NN_slug>/ with discovery.yaml + status.yaml
  + site.md. Heavy source artifacts go in an optional sources/ subfolder.

specialist:
  dispatch one-off or scoped specialist work
```

Step 2: Detect or choose discovery-group.

```
If parent is a delivery lifecycle (paper/application) -> prefer LNN_<slug>.
If parent is a probe or candidate probe -> prefer PNN_<slug>.
If the question is benchmark norms -> BNN_<slug>.
If the question is counterevidence -> CNN_<slug>.
If the question is a deep read of a specific source -> SNN_<slug>.
```

Pick the next free two-digit group id within that letter. Do not renumber
existing groups. Group letter is an organizational hint only; `role:` remains
authoritative.

Step 3: Detect or choose discovery-folder.

```
Inside the selected discovery-group, pick the next free two-digit folder:
01_<slug>/, 02_<slug>/, ...
```

Each discovery-folder answers one research topic. If the request contains
multiple topics, create multiple discovery-folders rather than cramming all
verdicts into one.

Step 4: Run lifecycle stages.

```
open:
  scaffold the discovery-folder: write discovery.yaml + status.yaml + site.md
  append discovery.opened to _haipipe/project.log.jsonl

search (1_search):
  inspect local project evidence first unless the user asks for fresh web search
  write sources.md (citation/source rows + verification state)
  set status.yaml to searching

read (2_read):
  extract per-source findings into notes.md

review (3_review) | idea (4_idea):
  synthesize notes into verdict.md (and the discovery.yaml verdict block)
  set status to ok / inconclusive / blocked
  append discovery.completed to _haipipe/project.log.jsonl

post:
  verify the parent path exists before marking consumed
  add the parent to discovery.yaml consumed_by only after verdict.md + parent exist
  if parent is missing, leave consumed_by unchanged and report blocked:
    missing_parent=<path>
  update _haipipe/project.status.yaml
  append discovery.consumed to _haipipe/project.log.jsonl
```

YAML timestamps MUST be quoted strings, e.g.
`"2026-06-20T15:05:00-04:00"`. JSONL files must contain one JSON object per
non-empty line and no blank lines.

Step 5: Return structured result.

```
status: ok | blocked | failed
discovery_group: <project-relative path>
discovery_folder: <project-relative path>
files_written:
  - ...
next:
  - what should consume verdict.md
```

---

Review Output Contract (3_review)
---------------------------------

Append this to the args of any review-bucket dispatch (research-lit /
comm-lit-review / academic-researcher). It exists because short author-year
tags alone (e.g. "Lu 2025") are **not matchable** by the reader. Every
review MUST satisfy all five rules.

```
1. FULL NAMES, never bare tags. Each paper gets a FULL citation on first
   mention AND a line in the final reference list:
     - Full title, verbatim (not shortened or paraphrased).
     - Full author list (name all; use "first three + et al." only when
       authors >= 6).
     - Venue: journal/conference with vol(issue):pages if published, else
       "arXiv preprint" / "working paper" with status.
     - Year + a LOCATOR: arXiv ID (arXiv:2405.07960), DOI, or URL.
   A short tag in running prose is OK ONLY if it maps to exactly one full
   reference-list entry.

2. NUMBERED REFERENCE LIST at the end ("References (full, verified)"):
   one self-contained, deduped line per paper. The reader must be able to
   match any in-text mention to exactly one numbered entry.

3. DISAMBIGUATE COLLISIONS. Two papers sharing author+year each get a
   distinguishing nickname in EVERY mention:
     Lu et al. 2025a (AgentA/B)  vs  Lu et al. 2025b (multi-turn behavior)
   Never leave two different papers both as "Lu 2025".

4. ONE-LINE PLAIN FINDING per paper (jargon-free) so a non-specialist can
   tell the papers apart at a glance.

5. VERIFICATION FLAG per paper: VERIFIED (id/DOI/venue confirmed via
   search) vs NEEDS-VERIFICATION. Never assert an unchecked citation; a
   gray-zone citation is flagged, not stated. Fabrication is the worst
   failure — fewer real entries beat invented ones.
```

Output skeleton the specialist should follow:

```
## <Topic> — Related Work
### <Theme / sub-question>   (repeat per group)
  - FULL citation (rule 1) + 1-line plain finding (rule 4) + flag (rule 5)
### References (full, verified)
  1. <self-contained full citation>   (rules 2 + 3, deduped & numbered)
```

For deeper rigor (systematic search + adversarial citation verification +
synthesis), escalate to the deep-research lit-review pipeline
(`Tools/plugin-workflows/academic-research-skills/deep-research`, mode
`lit-review`) — its source_verification_agent enforces rule 5 by re-checking
every id/DOI/venue and labelling FABRICATED / UNVERIFIABLE.

---

Dashboard (no-arg)
------------------

```
Durable:
  status [path]
  open <role> <question>
  open-group <slug>
  search | read | review | post <discovery>   (review -> verdict.md, or idea)
  feedback "<text>" | feedback list           (capture / review skill feedback)

Specialists:
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

Capture a complaint / confusion / wish about the discovery SKILL itself (clunky
step, confusing output, missing verb, wrong bucket dispatch) into this skill's
`feedback/` folder. Capture-only: filing never fixes on the spot; fixing is a
separate revision pass. Feedback is about the TOOL, not a discovery finding.

Capture: `/haipipe-discovery feedback "<text>"`
```
1. Write one file: feedback/<YYYY-MM-DD>_<short-slug>.md
   frontmatter: status: open | created | context (stage/bucket or "general") | fixed_in: ""
   body: the feedback in the reporter's words, then a trailing "Fix:" line.
2. Confirm captured. Do NOT attempt a fix now.
```

List: `/haipipe-discovery feedback list`
```
Grep feedback/*.md for `status: open` and print them (newest first) with context,
so a revision pass knows what to fix.
```

Resolve happens during a revision pass (not via this verb): set status: fixed +
fixed_in: <skill version> + a one-line Fix note; keep the file as history. Full
contract: `feedback/README.md`.

---

Escalation to Pipelines
------------------------

This skill is a SINGLE-STEP ROUTER. For multi-step orchestration, hand off:

```
/idea-discovery     full idea pipeline (research-toolkit Workflow 1)
/research-pipeline  end-to-end (idea -> experiments -> paper)
/patent-pipeline    patent track
```

Trigger phrases: "pipeline", "全流程", "end-to-end", "chain these", "all together".

---

Disambiguation
--------------

  - Bare arXiv ID, no verb       -> /alphaxiv
  - "find X": X=topic -> 1_search; X=idea -> 4_idea
  - Topic clear, bucket unclear  -> ask: search vs review?

---

Shared Resources / Cross-Domain
--------------------------------

```
0_venue/    venue filter data (utd24-is-venues.md) — read by
            research-lit / novelty-check / idea-creator on `— venues:`.
D_patent/   patent work. Skills: /prior-art-search,
            /patent-novelty-check, /patent-review, /jurisdiction-format,
            /specification-writing. Full flow: /patent-pipeline.
```

---

## Feedback

`/haipipe-discovery feedback "<text>"` captures a complaint / confusion / wish about THIS
skill into `feedback/` (one dated file per item, `status: open`) to fix in a
later revision pass. `/haipipe-discovery feedback list` shows the open items. This is
feedback about the tool, not the work it produces. Route a `feedback` first-token
here before other parsing. Full convention: `feedback/README.md`.
