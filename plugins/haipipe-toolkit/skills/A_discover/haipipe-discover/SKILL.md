---
name: haipipe-discover
description: "Router for Stage A (discover) literature/idea discovery. Dispatches to 1 of 4 buckets: search (arxiv/semantic-scholar/exa-search), read (alphaxiv/deepxiv/paper-analyzer), review (research-lit/comm-lit-review/academic-researcher), idea (idea-creator/novelty-check). Pipelines escalate to /idea-discovery. Patent work lives in D_patent/. Trigger: discover, find paper, lit review, 找idea, 查新, /haipipe-discover."
argument-hint: [bucket] [specialist] [args...]
allowed-tools: Bash, Read, Grep, Glob, Skill
---

Skill: haipipe-discover (orchestrator)
======================================

Single-step router for Stage 6. Multi-step pipelines escalate to `/idea-discovery`.

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
```

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
