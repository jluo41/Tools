---
name: haipipe-discover
description: "Router for Stage A (discover) literature/idea discovery. Dispatches to 1 of 4 buckets: search (arxiv/semantic-scholar/exa-search), read (alphaxiv/deepxiv/paper-analyzer), review (research-lit/comm-lit-review/academic-researcher), idea (idea-creator/novelty-check). Pipelines escalate to /idea-discovery. Patent work lives in D_patent/. Trigger: discover, find paper, lit review, 找idea, 查新, /haipipe-discover."
argument-hint: "[bucket] [specialist] [args...]"
allowed-tools: Bash, Read, Grep, Glob, Skill
metadata:
  version: "1.5.0"
  last_updated: "2026-06-20"
  summary: "Single entry for discover: capability router plus lightweight markdown discovery notes."
  changelog:
    - "1.0.0 (2026-05-31): baseline metadata added."
    - "1.1.0 (2026-06-01): added Review Output Contract (3_review) — full citations, numbered reference list, same-author/year disambiguation, plain-language finding, per-paper verification flag; router appends it to review-bucket dispatches."
    - "1.2.0 (2026-06-19): define discoveries/ as project-level external-evidence work, sibling to tasks/ and referenced by probes."
    - "1.3.0 (2026-06-19): split capability router from durable discovery artifact contract; add ref/discovery-yaml-schema.md."
    - "1.4.0 (2026-06-20): add discovery-group/discovery-folder hierarchy and one-interface lifecycle: open/search/read/review/verdict/post."
    - "1.5.0 (2026-06-20): make one markdown file the default durable artifact; folderized discovery becomes an opt-in heavy mode."
---

Skill: haipipe-discover (orchestrator)
======================================

Single entry for Stage A / the discover layer. Multi-step idea pipelines
still escalate to `/idea-discovery`.

This skill has two modes:

```
1. Durable project work
   Operate on lightweight discovery markdown files under
   examples/<PROJECT>/discoveries/.

2. Capability routing
   Dispatch to search/read/review/idea specialists for one-off discovery, or
   for work inside the current discovery markdown file.
```

In project workflows, discovery is **external evidence work**. It is not a
task execution stage. When a discovery needs to become durable project
evidence, write it under `discoveries/` and let probes or narratives reference
it the same way probes reference tasks:

```
Probe-open
  dispatches discoveries/   "what does the outside world already know?"
  dispatches tasks/         "what do our own runs show?"

Probe-post
  harvests both discovery evidence and task evidence before judging the claim.
```

Invocation:
```
/haipipe-discover                              -> dashboard
/haipipe-discover <discovery.md>               -> run full lifecycle
/haipipe-discover <discovery-group>            -> iterate/summarize children
/haipipe-discover status [path]                -> read-only status
/haipipe-discover open <role> <question>       -> scaffold discovery markdown
/haipipe-discover open-group <slug>            -> ensure discovery-group dir
/haipipe-discover search <discovery.md>        -> fill Sources section
/haipipe-discover read <discovery.md>          -> fill Notes section
/haipipe-discover review <discovery.md>        -> synthesize Notes/Verdict
/haipipe-discover verdict <discovery.md>       -> finalize Verdict section
/haipipe-discover post <discovery.md>          -> mark consumed if parent exists

/haipipe-discover <bucket>                     -> list specialists
/haipipe-discover <specialist> [args]          -> dispatch specialist
/haipipe-discover "<natural language>"         -> infer + dispatch
/haipipe-discover pipeline [topic]             -> escalate /idea-discovery
```

---

Hierarchy
---------

Discover mirrors task's clean grouping, but stays much lighter because it does
not execute code:

```
Task:     task-group      -> task-folder      -> run
Discover: discovery-group -> discovery.md     -> source row
```

Definitions:

```
discovery-group   A directory grouping related outside-evidence questions.
discovery.md      One durable outside-evidence question, stored as one file.
source row        One paper/webpage/report/dataset citation in the Sources
                  section.
```

Project shape:

```
examples/<PROJECT>/
├── discoveries/
│   ├── L01_initial-landscape/
│   │   ├── 01_landscape-review.md
│   │   └── 02_novelty-check.md
│   └── P01_rare-phenotype-lift/
│       ├── 01_prior-art.md
│       └── 02_benchmark-landscape.md
├── probes/
├── tasks/
├── paper/
└── applications/
```

Group letters are organizational hints, not the source of truth. The
frontmatter `role:` in the discovery markdown is authoritative.

Recommended group hints:

```
L  landscape / delivery-open discovery
P  probe-backed prior art or counterevidence
B  benchmark landscape
C  counterevidence
S  source reads
```

Folderized legacy packages such as `discoveries/D0619_noisy-labels-prior-art/`
or `discoveries/P01_group/01_question/` are readable for compatibility, but new
durable work should default to `discoveries/<GROUP>/<NN_slug>.md`.

---

Discovery Lifecycle
-------------------

Every discovery markdown answers one external-world question:

```
Open     create <NN_slug>.md with frontmatter and empty sections
Search   fill ## Sources with candidate sources + verification state
Read     fill ## Notes with extracted source facts
Review   synthesize notes into claim-relevant findings
Verdict  finalize ## Verdict (ok/inconclusive/blocked)
Post     update parent refs/status and _haipipe/project.log.jsonl
```

`post` does not judge the research claim. It only makes the discovery verdict
available to its parent narrative or probe.

File ownership:

```
Open      <NN_slug>.md frontmatter + headings
Search    ## Sources
Read      ## Notes
Review    ## Notes / ## Verdict draft
Verdict   frontmatter status/verdict + ## Verdict
Post      parent refs, project.status.yaml, project.log.jsonl
```

No local status/site files belong in a discovery-group by default. Timeline
events go to `_haipipe/project.log.jsonl`.

Folderized heavy mode is opt-in only. Use it when the discovery must keep PDFs,
HTML snapshots, many per-source notes, or other source artifacts:

```
discoveries/<GROUP>/<NN_slug>/
├── discovery.md
└── sources/
```

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


Project Discovery File
----------------------

Use this folder when discovery output is part of a narrative/probe stack:

```
examples/<PROJECT>/
├── discoveries/
│   ├── P01_robustness-claim/
│   │   └── 01_noisy-labels-prior-art.md
│   └── L01_initial-landscape/
```

Default markdown contract:

```md
---
kind: discovery
id: P01.01
group: P01_robustness-claim
role: prior_art_check
status: ok
parent: probes/P001_robustness_claim
verdict: inconclusive
created_at: "2026-06-20T15:05:00-04:00"
updated_at: "2026-06-20T15:05:00-04:00"
consumed_by: []
---

# Noisy-label prior art

## Question

## Sources

## Notes

## Verdict

## Caveats
```

Legacy folderized schema authority: `ref/discovery-yaml-schema.md`.

`discoveries/` should contain evidence and citations, not code/runs/metrics.
The single project event log remains `_haipipe/project.log.jsonl`; discovery
files do not keep their own orchestration logs.

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
2. First positional is an existing path:
     discovery markdown -> run requested stage or full lifecycle.
     discovery-group    -> iterate/summarize child discovery files.
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

Use this protocol whenever `/haipipe-discover` is used for durable project
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
  path is a discovery markdown file, or a heavy folder containing discovery.md
  -> run requested stage or full lifecycle

existing discovery-group:
  path is under discoveries/, contains discovery markdown files or heavy
  discovery markdown files or heavy discovery folders, and has no discovery.md
  at root -> summarize/iterate

open-group:
  create discoveries/<GROUP_slug>/ only. Do not add status.yaml/site.md by
  default.

open:
  create discoveries/<GROUP_slug>/<NN_slug>.md by default.
  Use folderized heavy mode only when explicitly requested with --folder or
  when source artifacts must be stored.

specialist:
  dispatch one-off or scoped specialist work
```

Step 2: Detect or choose discovery-group.

```
If parent is a narrative or story-level shadow -> prefer LNN_<slug>.
If parent is a probe or candidate probe -> prefer PNN_<slug>.
If the question is benchmark norms -> BNN_<slug>.
If the question is counterevidence -> CNN_<slug>.
If the question is a deep read of a specific source -> SNN_<slug>.
```

Pick the next free two-digit group id within that letter. Do not renumber
existing groups. Group letter is an organizational hint only; `role:` remains
authoritative.

Step 3: Detect or choose discovery file.

```
Inside the selected discovery-group, pick the next free two-digit file:
01_<slug>.md, 02_<slug>.md, ...
```

Each discovery file answers one external-world question. If the request
contains multiple questions, create multiple discovery markdown files rather
than putting all verdicts into one file.

Step 4: Run lifecycle stages.

```
open:
  write <NN_slug>.md with frontmatter and the required sections
  append discovery.opened or discovery.group_opened to _haipipe/project.log.jsonl

search:
  inspect local project evidence first unless the user asks for fresh web search
  fill ## Sources with citation/source rows and verification state
  update frontmatter status to searching or reading

read:
  extract source-specific findings into ## Notes
  keep source records in the markdown unless heavy artifacts are required

review:
  synthesize the notes into claim-relevant findings
  update ## Notes and draft ## Verdict

verdict:
  write ## Verdict using the Verdict Contract
  update frontmatter to ok/inconclusive/blocked
  append discovery.completed to _haipipe/project.log.jsonl

post:
  verify the parent path exists before marking consumed
  add the parent to consumed_by only after ## Verdict exists and parent exists
  if parent is missing, leave consumed_by unchanged and report blocked:
    missing_parent=<path>
  update _haipipe/project.status.yaml when present
  append discovery.consumed to _haipipe/project.log.jsonl
```

YAML timestamps MUST be quoted strings, e.g.
`"2026-06-20T15:05:00-04:00"`. JSONL files must contain one JSON object per
non-empty line and no blank lines.

Step 5: Return structured result.

```
status: ok | blocked | failed
discovery_group: <project-relative path>
discovery_file: <project-relative path>
files_written:
  - ...
next:
  - what should consume the Verdict section
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
  search | read | review | verdict | post <discovery.md>

Specialists:
  1_search   arxiv | semantic-scholar | exa-search
  2_read     alphaxiv | deepxiv | paper-analyzer
  3_review   research-lit | comm-lit-review | academic-researcher
  4_idea     idea-creator | novelty-check

Pipeline:  /idea-discovery   (research-lit -> idea-creator -> novelty-check)
```

Suggest the most likely next command based on context.

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
