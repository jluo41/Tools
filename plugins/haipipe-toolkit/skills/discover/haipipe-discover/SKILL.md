---
name: haipipe-discover
description: "Router for Stage A (discover) literature/idea discovery. Dispatches to 1 of 4 buckets: search (arxiv/semantic-scholar/exa-search), read (alphaxiv/deepxiv/paper-analyzer), review (research-lit/comm-lit-review/academic-researcher), idea (idea-creator/novelty-check). Pipelines escalate to /idea-discovery. Patent work lives in D_patent/. Trigger: discover, find paper, lit review, 找idea, 查新, /haipipe-discover."
argument-hint: "[bucket] [specialist] [args...]"
allowed-tools: Bash, Read, Grep, Glob, Skill
metadata:
  version: "1.3.0"
  last_updated: "2026-06-19"
  summary: "Router for Stage A (discover) literature/idea discovery; durable project artifacts live under discoveries/."
  changelog:
    - "1.0.0 (2026-05-31): baseline metadata added."
    - "1.1.0 (2026-06-01): added Review Output Contract (3_review) — full citations, numbered reference list, same-author/year disambiguation, plain-language finding, per-paper verification flag; router appends it to review-bucket dispatches."
    - "1.2.0 (2026-06-19): define discoveries/ as project-level external-evidence work, sibling to tasks/ and referenced by probes."
    - "1.3.0 (2026-06-19): split capability router from durable discovery artifact contract; add ref/discovery-yaml-schema.md."
---

Skill: haipipe-discover (orchestrator)
======================================

Single-step router for Stage A / the discover layer. Multi-step pipelines
escalate to `/idea-discovery`.

In project workflows, discovery is **external evidence work**. It is not a
task execution stage. When a discovery needs to become durable project
evidence, write it under `discoveries/` and let probes reference it the same
way they reference tasks:

```
Probe-open
  dispatches discoveries/   "what does the outside world already know?"
  dispatches tasks/         "what do our own runs show?"

Probe-post
  harvests both discovery evidence and task evidence before judging the claim.
```

Invocation:
```
/haipipe-discover                       -> dashboard
/haipipe-discover <bucket>              -> list specialists
/haipipe-discover <specialist> [args]   -> dispatch
/haipipe-discover "<natural language>"  -> infer + dispatch
/haipipe-discover pipeline [topic]      -> escalate /idea-discovery
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


Project Discovery Folder
------------------------

Use this folder when discovery output is part of a narrative/probe stack:

```
examples/<PROJECT>/
├── discoveries/
│   ├── D0619_noisy-labels-prior-art/
│   │   ├── discovery.yaml     external-evidence contract + status
│   │   ├── status.yaml        current snapshot
│   │   ├── site.md            human-readable summary
│   │   ├── sources.md         citations, URLs, verification flags
│   │   ├── notes.md           synthesis / extracted findings
│   │   └── verdict.md         concise answer for the parent probe
│   └── 2026-archive/
```

Schema authority: `ref/discovery-yaml-schema.md`.

`discoveries/` should contain evidence and citations, not code/runs/metrics.
The single project event log remains `_haipipe/project.log.jsonl`; discovery
folders do not keep their own orchestration logs.

---

Routing Logic
-------------

```
1. First positional is a specialist name  -> dispatch directly.
2. arXiv ID / arxiv URL in args            -> 2_read.
     "summarize|explain"   -> alphaxiv (default)
     "section|layered"     -> deepxiv
     "analyze|claims"      -> paper-analyzer
3. First positional is a bucket alias      -> use that bucket.
4. Keyword scan:
     "preprint|arxiv"           -> arxiv
     "IEEE|ACM|venue|citation"  -> semantic-scholar
     "web|blog|news|exa"        -> exa-search
     "review|survey|related work" + comms   -> comm-lit-review
     "review|survey|related work" (default) -> research-lit
     "brainstorm|find idea|找idea"           -> idea-creator
     "novelty|查新"                          -> novelty-check
     "patent|专利|prior art"                  -> hand off to D_patent/
     "pipeline|全流程|end-to-end"             -> escalate /idea-discovery
5. Bucket resolved, specialist unresolved -> use bucket default
   (arxiv | alphaxiv | research-lit | idea-creator).
6. Nothing resolves -> ask user to pick 1 of 4 buckets.

Dispatch: Skill(<specialist>, args="<remaining_args>"). Do not auto-chain.
         For any 3_review dispatch, APPEND the Review Output Contract
         (below) to args so the result is citation-matchable.
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
