# External Discovery Skill Map

This map records the related external research-skill repositories that were
pulled and inspected on 2026-09-07, which capabilities enter HAI Pipe, and
which remain reference-only. The HAI adapters are the compatibility boundary
for Page, Task, Run, Result, and Bib contracts; an external checkout is not an
implicit permission to run its independent orchestration or write layout.

## Promoted into the active Discovery family

| External capability | HAI location | Use in Discovery | Adaptation |
|---|---|---|---|
| gemini-search | discovery/1_search/gemini-search | Optional broad candidate scout | Read-only harvest; dispatcher verifies identity and allocates Runs. |
| openalex | discovery/1_search/openalex | Optional structured journal/index and citation-graph source | Pinned helper; metadata never becomes Bib authority by itself. |
| research-lit | discovery/2_review/research-lit | Supporting review and synthesis craft worker | Source options now include Gemini/OpenAlex; `3_synthesize` and the Page route own durable writes. |
| haipipe-discovery-synthesize | discovery/3_synthesize/haipipe-discovery-synthesize | Cross-Result article synthesis | HAI router; combines accepted Result/Card/Bib pointers and never creates a local Run. |

The existing HAI adapters for arxiv, semantic-scholar, deepxiv, exa-search,
alphaxiv, and paper-analyzer remain the active workers; they were compared
against the ARIS catalog but did not need a duplicate copy in this update.

The Science Superpowers prior-work lens is incorporated into
`discovery/2_review/research-lit` as an optional evidence-backed grounding
frame (methods, confounds, effect sizes, and relationship to prior work). Its
human-gated question/framing workflow remains outside D1.

## Pulled related repositories

These submodules are initialized at their fetched default-branch tips. The
commit is recorded so a later refresh can be compared rather than silently
overwriting the provenance.

| Repository | Tip (2026-09-07) | Relevant skills inspected | Decision |
|---|---|---|---|
| academic-research-skills | 6b7ee6d | deep-research, academic-paper-reviewer, academic-pipeline | Reference-only: 13-agent/report pipeline and its output files are not D1 Folder artifacts. |
| aris | 0472e53 | research-lit, gemini-search, openalex | Promoted adapters and synchronized local Discovery workers above; ARIS Idea workers are not installed in Discovery. |
| auto-empirical-research-skills | d31f17f | academic-paper-search, literature-review, literature-survey-generator, SLR/PRISMA, OpenAlex, hypothesis-generation | Reference-only: broad catalog and duplicated providers; use HAI research-lit/search contracts. |
| aer-skills | 85eae99 | aer-literature, aer-topic-selection | Reference-only: economics/top-venue gate; its citation-integrity and antecedents ideas inform novelty/review but its venue scope is narrower. |
| auto-research-skills | 1c277ad | catalog/site | Reference-only: no executable Discovery skill body in the checked-out tip. |
| literature-source-tracing | 4bf84a2 | literature-source-tracing | Reference-only: requires a DOCX plus reference-PDF tree and writes Word/highlighted-PDF outputs; a future citation-trace adapter can return inline evidence rows. |
| research-agent-skills | 4af0f96 | replication-archive and agent utilities | Reference-only: replication/build work belongs to Task or Paper, not source acquisition. |
| research-co-pilot | f824e6c | literature-review, research-brainstorm, peer-review | Reference-only: standalone research/<project> memory and phase network conflict with D1 authority. |
| paper-rag-skill | b1097d3 | paperrag | Optional infrastructure reference: a PDF vector index may feed local context, but it never creates a Discovery Run/Result/Bib. |
| research-genealogy | e075888 | research-genealogy | Reference-only view: citation lineage is a landscape projection, not one canonical paper/source Run. |
| science-superpowers | 9e348a4 | surveying-prior-work, framing-research-questions, feasibility, verification | Prior-work lens adapted into research-lit; the remaining human-gated analysis workflow stays outside D1. |
| superpower-socialscience-skills | 4c8ec80 | domain analysis experts, internet/bibliometric analysis | Reference-only craft workers; invoke after evidence admission when a domain method is explicitly requested. |
| paperjury | 53c75e8 | paper review/edit/auto hardening | Reference-only: manuscript review/editing is Paper work, not Discovery evidence acquisition. |

## Kept as upstream reference, not copied into the core route

| External skill | Why it stays reference-only | HAI replacement or next route |
|---|---|---|
| idea-discovery | ARIS end-to-end orchestrator owns a different phase/checkpoint and output model | Not part of Discovery; use the separate haipipe-ideation skill when semantic direction work is requested. |
| research-review | External adversarial critic, not topic literature synthesis; its standalone files/traces conflict with HAI receipts | Optional human/external review after Page content, outside D1 Run counting |
| research-wiki | Persistent ARIS knowledge-base layout is project-optional and not a HAI Folder Face | Use only when a project explicitly has research-wiki; never make it a required lane |
| research-refine, experiment-plan, ablation-planner, formula-derivation | Method/paper development belongs after Discovery | haipipe-paper or haipipe-task |
| prior-art-search | Patent/FTO workflow is a distinct legal-research scope | Add only when patent prior art is explicitly requested |

## Maintenance rule

Fetch the selected external submodules before comparing upstream changes. Copy
only a skill whose inputs, outputs, and authority can be stated in HAI terms;
otherwise keep the upstream path in this map and add a narrow adapter later.
Never overwrite a HAI contract with a whole external orchestrator. A refreshed
submodule tip is evidence of availability, not a release of the local skill.
