# Discovery Inquiry Workflow Table

This is the canonical Discovery Workflow Definition for `folder-kind:
discovery`. A live Workflow is a list of owner-native Run Instances and their
dependency/route graph. This definition lists the available Run Specs and
controller policy; the Discovery owner declares source-analysis Specs here,
while the shared Page owner declares any Page Specs. A live Runtime contains
only the selected Runs. The controller labels below are internal Steps, not
separate workflow units. The Page owner remains independent; the two owners
meet through explicit Results and receipts.

```text
DISCOVERY CONTROLLER      SCOPE -> PREPARE? -> ACQUIRE <-> SYNTHESIZE -> CLOSE
DISCOVERY RUN SPECS       paper-analysis | source-analysis, one Subject each
PAGE RUN SPECS            shared Page-owned interaction, when commissioned
WORKFLOW RUNTIME          selected Discovery Runs + any selected Page Runs
PAGE CONTROLLER STEPS     00 CONTEXT -> 01 OUTLINE -> 02 EVIDENCE -> 03 CONTENT -> 04 CHECK
DISCOVERY RUN COUNT       R_discovery = N_admitted Subjects
```

There is no separate `haipipe-discovery-workflow` skill directory to load.
This owner contract publishes the Discovery Run Specs and controller routing
policy. The Page Workflow remains a separate shared authority and publishes
its own Page Run Specs when its interaction is commissioned.

The on-disk `1_search`, `2_review`, and `3_synthesize` directories are numbered
skill-family groups, following `haipipe-task`. Search resolves candidates,
Review inspects one source/Result, and Synthesize combines accepted Results.
Semantic ideation is a separate sibling skill, not a Discovery family. These
groups organize capability routers and workers; they are not Runs or controller
Steps. The `workflow-phases/` directory name is a retained compatibility
address; it does not grant a phase independent execution or commissioning
authority.

The optional external source adapters are part of the FIND family: Gemini
expands aliases and neighboring subproblems; OpenAlex contributes structured
metadata and citation-graph coverage. Both return read-only candidate harvests
to the same resolver and do not change the Run cardinality law.
For clinical or biomedical scopes, the same FIND family records medRxiv as a
relevant preprint channel and PubMed/Crossref as index and identity fallbacks;
they are coverage channels, not additional Run types.

The external capability registry also permits narrow reference procedures:
academic-paper-search for provider routing, K-Dense extraction/appraisal and
literature-source-tracing for per-Subject review, research-genealogy and
Result-to-Claim for synthesis, and citation-fidelity/reference-verify for
per-Result verification. Citation-audit is reserved for the cross-Result/Page
CHECK. Each returns a normalized packet to the local family router; none is a
Discovery controller Step, Run commissioner, Result writer, or Bib owner.

## BJTR Alignment Crosswalk

The earlier Discovery descriptions used 0/1/2/3 or 1/2/3/4 labels for a mix of
Page records and capability families. This table is the repair: only the first
column is the durable work address. The complete retrofit, legacy mapping, and
worked route are in `../../../haipipe-discovery/ref/bjtr-alignment.md`.

| Object | Physical location or label | Owner | Cardinality / relation | Correct interpretation |
|---|---|---|---|---|
| Bank | discoveries/ | Discovery bank | many Blocks | Root collection; it is not a Block level |
| Block | bNN_<block>/ | D1 + Board contract | contains Jobs | Board/program; group related inquiry campaigns here |
| Job | jNN_<job>/ | D1 | contains Task Pages | Self-contained inquiry or campaign group |
| Task Page | tNN_<task>/ | D1 + shared Page workflow | contains many Runs | One article-shaped question and one discovery_type; has Page and Task Faces |
| Run | runs/rNN_*.sh | Discovery d1.acquire Step + haipipe-run | one admitted canonical Subject | One paper/source analysis ticket; full address is bNN.jNN.tNN.rNN |
| Result | results/rNN_*/ | Run contract | exact same-stem pair with one Run | Readout projection; not a fifth hierarchy level |
| Discovery controller Step | SCOPE, PREPARE, ACQUIRE, SYNTHESIZE, CLOSE | Discovery owner contract | temporal route over one Task | Internal routing only; never a Run or b/j/t/r segment |
| Page controller Step | 00 CONTEXT through 04 CHECK | haipipe-page-workflow | Page control sequence | Page authoring/check routing; never itself a Run |
| Search family | 1_search | FIND and identity workers | many calls per acquisition | Capability family, chiefly Discovery ACQUIRE; never Job j01 |
| Review family | 2_review | per-Subject review workers | one packet per admitted source | Capability family, chiefly Discovery ACQUIRE; never Job j02 |
| Synthesize family | 3_synthesize | cross-Result synthesis router | one Page synthesis over many Results | Capability family, chiefly Discovery SYNTHESIZE/CONTENT; never Run r03 |

The hierarchy answers “where,” controller Steps answer “when to route,” the
Page controller answers “how the Page is authored,” and the Page type answers
“what article is promised.” A Search query, API call, worker turn, reviewer
pass, or Bib build remains receipt detail inside its owning Run or controller
Step; none receives a new BJTR address.

## Controller-Step Routing Table

| Step ID | Owner | Controller Step | Label | Purpose | Input / policy | Exact skill chain | Actor | L3 Task/Page content modified | L4 Run Spec(s) selected | Output | Exit gate | Next route | Human gate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| d1.scope | Discovery | D1 controller Step | SCOPE | Freeze BJTR identity, question, discovery_type, source boundary, and admission rule. | Parent Block/Job; request; source policy; preserved records. | haipipe-discovery -> haipipe-discovery-inquiry -> haipipe-discovery/ref/discovery-yaml-schema.md | Discovery creator | discovery.yaml intent and Task identity only. Opening the Folder may scaffold the same-stem Page, but SCOPE does not author Page Content. | none | Scoped Discovery Folder and Page-workflow input. | Path, manifest, type, question, boundary, and admission rule agree. | d1.prepare, d1.acquire, or HOLD; Page 00 CONTEXT may now resolve the Discovery owner. | Resolve a material scope ambiguity only when policy cannot. |
| d1.prepare | Discovery | D1 controller Step | PREPARE | Author reusable search, extraction, or synthesis support only when needed. | Frozen scope and instrument declaration. | haipipe-discovery -> haipipe-discovery-inquiry | Discovery creator | Optional used scripts/; no empty lane and no Page mutation. | none | Declared instrument or explicit omission. | Declared path exists and is reusable, or instrument.needed: false. | d1.acquire or HOLD. | none |
| d1.acquire | Discovery | D1 controller Step | ACQUIRE | Resolve Triggers, admit canonical Subjects, and produce one truthful analysis Result per Subject. | Scope/admission rule; Trigger provenance; Paper Run contract; optional instrument. | haipipe-discovery -> haipipe-discovery-inquiry -> haipipe-run -> haipipe-discovery-search -> FIND (arxiv / medRxiv when clinical / semantic-scholar / Crossref+PubMed resolver / exa-search / openalex / gemini-search) -> optional provider routing (academic-paper-search / ARIS research-lit / AER novelty pass) -> READ (alphaxiv / deepxiv / paper-analyzer) -> optional review packet (K-Dense extraction / literature-source-tracing / citation-fidelity / reference-verify) -> haipipe-discovery-review | Discovery creator; source workers are read-only helpers | Task progress and receipt links only; root Page claims remain unchanged. | Discovery paper-analysis or source-analysis x N_admitted; exactly one Subject per Run. | Reused or new same-stem Run/Result pairs plus Trigger dispositions and review packets. | Every admitted Subject has one valid pair; zero-Subject and unchanged duplicate Triggers open no Run; failures remain truthful. | d1.acquire, d1.synthesize, or HOLD. | Verify each complete Result citation in its own runtime before epistemic closure. |
| d1.synthesize | Discovery | D1 owner | SYNTHESIZE | Combine completed Review packets and Results into the promised article. This controller Step routes work; Page Workflow owns every Page mutation. | Accepted Results; review packets; type promise; manifest; current Page receipts. | haipipe-discovery -> haipipe-discovery-inquiry -> haipipe-discovery-synthesize -> optional synthesis craft (research-genealogy / Result-to-Claim) -> haipipe-page -> haipipe-page-workflow -> current Page controller Step -> declared craft worker -> shared CHECK | Discovery orchestrator plus current Page-Step producer/checker | Controller records only Task-side progress and optional typed record. Page 00–04 owns Context, generated Outline, Content, and Check artifacts; D1's direct Result/cite lineage makes typed local EVIDENCE/LAND skippable. | No Run in this controller Step by itself; the shared Page Workflow may select `rp00_mermaid-structure` then selected `rpNN_pNN[-pNN]` Specs, while CONTENT consumes their Results after the Page release barrier. | A CHECKed root Page, optional typed Task record, derived Bib, and exact Result/cite lineage. | The Page release barrier is open, Page Workflow reaches 04 CHECK, every factual claim resolves to completed Discovery Results, and missing evidence routes back to ACQUIRE. | d1.acquire, d1.close, or HOLD. | Shared Page gates apply inside Page Workflow; the Discovery owner adds no duplicate Page ruling. |
| d1.close | Discovery | D1 controller Step | CLOSE | Reconcile the Task Face against the already-CHECKed Page and publish the domain outcome/receipt. | Page CHECK receipt; manifest; Run inventory; derived Bib; verification receipts; checker output. | haipipe-discovery -> haipipe-discovery-inquiry -> haipipe-discovery/scripts/paper_runs.py check | Discovery creator after fresh Page checker | discovery.yaml report/status, final Task receipt, and handoff pointers; Page remains read-only here. | none | ok, inconclusive, blocked, or named backward route. | Checker passes; material Discovery Runs resolved; Page CHECK closed; Page/Task states agree; aggregated complete Result Bibs are verified. | CLOSE, d1.acquire, d1.synthesize, or HOLD. | none beyond unresolved Result-Bib verification; Page acceptance belongs to Page CHECK. |

Terminal classification is exact:

- `ok`: the article promise is met, every load-bearing Aim is met, material
  Discovery Runs are resolved, and every promoted Result citation is verified.
- `inconclusive`: all admitted evidence completed and was verified, but it
  cannot establish the substantive answer.
- `blocked`: an operational dependency, unresolved material Run, Page gate, or
  citation-verification debt remains.

## Cross-layer handoffs

These are handoffs between authorities, not Runs or Discovery hierarchy
levels.

| Handoff | Input | Receiving owner | Writes | Return route |
|---|---|---|---|---|
| d1.synthesize → haipipe-ideation | accepted Discovery Result/Card/Bib pointers plus Task Run/Result pointers | sibling haipipe-ideation | evidence bundle, Direction Cards, Idea Cards, pressure-test receipts | missing external evidence → d1.acquire; selected direction → haipipe-paper P0 |

Discovery does not contain an Idea Page type or compatibility route. Semantic
direction work begins only through the sibling `haipipe-ideation` handoff.

## Page Workflow-Step Crosswalk

This table is a specialization/adoption view, not a fork of the canonical Page
table at `haipipe-page-workflow/ref/workflow-table.md`.

| Page controller Step | Discovery use | Page-owned writes | Page Runs selected | Cross-workflow handoff |
|---|---|---|---|---|
| 00 CONTEXT / PREPARE | Resolve D1 Folder owner, manifest, type promise, Results, requirements, and policies into fresh context. | outline/<stem>-context.md only. | none | A stale/missing manifest routes to d1.scope or d1.prepare. |
| 01A OUTLINE / SHAPE | Shape the four-role article and declare exact Discovery Result/cite support for each checkable claim. | Plan, division intents, Aim promises, and direct Result/cite bindings; the Page's Mermaid structure and global paragraph order are reviewed in the Page-owned `rp00_mermaid-structure` interaction when selected. | no D1 Run; Page may allocate `rp00_mermaid-structure` only through the shared Page workflow | A changed evidence population routes to D1 ACQUIRE. |
| 01B OUTLINE / SURVEY | Decide whether existing Discovery Results suffice or D1 must acquire more. The D1 root Page does not create a redundant local Evidence Item graph. | Direct Result/cite routes and new Discovery requests. | none | new Discovery hands off to d1.acquire; completed Results return to SHAPE. |
| 02A EVIDENCE / LAND | Skipped in the D1 root Folder because its admitted Paper/Source Results are already the authoritative evidence objects. | none | none | A consumer Page that needs a typed Evidence Item owns its separate local Page Run in the consumer Folder. |
| 02B EVIDENCE / EMBED | Skipped without a local make-item. D1 SYNTHESIZE rebuilds the derived aggregate Bib through the Outline citation authority; SHAPE records direct Result/cite lineage. | none beyond the derived Bib projection owned by Outline. | none | CONTENT consumes the approved directly supported Shape. |
| 03 CONTENT / WRITE | Realize the discovery_type article from the approved Result-backed synthesis plan. | Root Page Content/Aims, delivery, build, and promotion trace. | consumes the accepted `rp00`/`rpNN` Page-owned interaction; no new writing Run per adopted paragraph and no Discovery writing Run. | Missing evidence routes to OUTLINE and D1 ACQUIRE; wording changes return to the owning Page Run. |
| 04 CHECK / CHECK | Judge one exact built Page version. | Check receipt/findings only. | none | A closed Page returns its receipt to d1.close; findings route to the owning Page controller Step or Run. |

## Runs Overview

This definition is not bound to a live Discovery Workflow Runtime, so it
contains no actual Run rows. A live Runtime inserts one row per selected
owner-native `rNN` or Page-owned `rpNN` Run; it never expands symbolic
cardinality into fictional Runs.

| Run | Owning controller step / Run owner | Kind | Target | Depends On | Status | Result |
|---|---|---|---|---|---|---|

## Available Run Spec Catalog

These entries are available specs, not instantiated Runs. A concrete Workflow
selects only the commissioned entries; the Workflow Runtime then lists their
actual owner-native Run instances.

| Run family | Operation | Owner / commission point | Cardinality | Target | Result | Counts toward R_discovery |
|---|---|---|---:|---|---|---|
| Discovery | paper-analysis | d1.acquire | 0..N | one canonical paper | same-stem Card + facts + runtime + one-entry Bib | yes |
| Discovery | source-analysis | d1.acquire | 0..N | one canonical non-paper source | same-stem Card + facts + runtime + one-entry Bib | yes |
| Page | evidence-item | not commissioned inside a Discovery root Folder | 0 | n/a; a consumer Page owns its own item | n/a | no |
| Page | interactive-writing | shared Page owner; selected by the Discovery Runtime when commissioned | `rp00` plus selected `rpNN` | whole-Page structure, then one selected paragraph group; Page owns feedback, Versions, Steps, and acceptance | Page Run Result/accepted preview consumed by CONTENT | no |

```text
Trigger --resolve--> canonical Subject --allocate--> Discovery rNN ticket
                                              \----> same-stem Result

R_discovery = N_admitted canonical Subjects
R_source    = R_discovery
R_page      = separate Page-owned `rpNN` lane; never counted in R_discovery
```

- Search queries, redirects, API/CLI calls, worker turns, synthesis passes,
  checker calls, Page workflow passes, Page-owned `rpNN` interactions, typed
  records, and derived Bib assembly are not Discovery Runs.
- An unchanged duplicate Subject reuses its existing Run/Result. A materially
  changed analysis allocates a new Discovery Run with `supersedes:`.
- Discovery `runs/`/`results/` are the Folder's only local Run inventory. A
  consumer Page may use these as Supporting Results, but owns its own local
  Page-family Run outside the Discovery Folder.

## Human Actions

This definition is not bound to a live Discovery Workflow Runtime, so it
contains no current unresolved human decisions. A live rendering inserts only
gates whose state is open.

| Gate | Controller step / decision owner | Trigger | Decision | State | Record |
|---|---|---|---|---|---|

## Human Gate Catalogue

| Gate | Controller step / decision owner | Trigger | Decision | State when instantiated | Record |
|---|---|---|---|---|---|
| Scope ambiguity | d1.scope | policy cannot freeze the evidence population | choose and freeze the boundary | open -> signed | manifest/context decision receipt |
| Shape approval | d1.synthesize | changed Page plan would commission new evidence work | approve or return the Shape | open -> signed / returned | Page plan approved: receipt |
| Admission branch | d1.scope or d1.synthesize | policy cannot decide acquire/reuse/exclude | select the disposition | open -> signed | durable decision receipt |
| Result-Bib verification | d1.acquire | complete Result would support ok or inconclusive | verify or return the citation | open -> signed / returned | runtime bib.verification person receipt |
| Built-Page acceptance | d1.synthesize | Page 04 CHECK requires acceptance | accept or return the built Page | open -> signed / returned | Page accepted: receipt |

`page_ruling: none` means the Discovery controller adds no second domain
approval. It does not erase
the Page workflow's own person-reserved acts.

## Adoption Gate

- The Discovery owner contract publishes the Discovery Run Specs and
  controller routing; SCOPE/PREPARE/ACQUIRE/SYNTHESIZE/CLOSE are internal
  Steps, not Workflow units. No standalone wrapper skill duplicates it.
- The shared Page workflow remains the sole owner of Page mutations. D1's root
  Page uses direct Result/cite lineage, skips typed local EVIDENCE/LAND, and
  records that CONTENT commissions no Discovery writing Run so the D1 local
  inventory remains paper/source only. Any `rpNN` interaction belongs to the
  shared Page workflow and is not counted in `R_discovery`.
- The Discovery owner commissions paper/source Runs from the ACQUIRE Step,
  one per admitted canonical Subject.
- The SYNTHESIZE Step routes the Page handoff but never writes through a Page
  controller Step's authority.
- Page CHECK closes the Page; D1 CLOSE then reconciles and closes the Folder's
  Task Face.

## Skill Coverage

`?` means the shared skill was not independently field-tested in this
Discovery revision. Paths are literal relative to
`Tools/plugins/haipipe-toolkit/`; paths, versions, and line counts were
refreshed on disk on 2026-09-13. Some shared Page/Task rows may include a
working-tree snapshot while their owning session is still changing them;
that does not count as a release or a field-test. Statuses marked valid come
from `quick_validate.py`, and row use is derived from the
Controller-Step Routing Table.

| Skill | Path | Role | Used by controller Step / Run Spec | Status | Version | SKILL.md lines | Quality / completeness | Field-test | Gap / next action |
|---|---|---|---|---|---:|---:|---|---|---|
| haipipe-discovery | skills/discovery/haipipe-discovery/SKILL.md | Search/Review/Synthesize door | d1.scope, d1.prepare, d1.acquire, d1.synthesize, d1.close | ✅ structurally valid | 0.15.2 | 469 | ?; static quality not assessed | fresh-context 2026-09-20 PASS for workflow routing and Run boundary | External retrieval not invoked; current source-map, review, and synthesis confidence contracts are linked |
| haipipe-discovery-inquiry | skills/discovery/workflow-phases/haipipe-discovery-inquiry/SKILL.md | Discovery Run Workflow Definition / Folder contract | d1.scope, d1.prepare, d1.acquire, d1.synthesize, d1.close | ✅ structurally valid | 0.6.3 | 214 | ?; static quality not assessed | terminology update inspected after cold route validation | Page Workflow Steps do not create Discovery Runs; direct Result/cite handoff retained |
| haipipe-folder | skills/board/haipipe-folder/SKILL.md | neutral Folder contract | d1.scope, d1.close | ? unknown | 0.5.1 | 301 | ?; not assessed in this revision | ? | re-audit on shared-contract change |
| haipipe-page | skills/page/haipipe-page/SKILL.md | Page door | d1.synthesize | ? unknown | 0.88.0 | 831 | ?; not assessed in this revision | ? | current Page contract inspected; fresh cross-family validation remains |
| haipipe-page-workflow | skills/page/page-workflows/haipipe-page-workflow/SKILL.md | Page Workflow controller | d1.synthesize | ? unknown | 0.45.0 | 453 | ?; not assessed in this revision | ? | current Page Run/release-barrier contract inspected; fresh cross-family validation remains |
| haipipe-page-context | skills/page/page-workflows/haipipe-page-context/SKILL.md | Page Workflow Step contract | d1.synthesize | ? unknown | 0.1.3 | 205 | ?; not assessed in this revision | ? | re-audit on shared-contract change |
| haipipe-page-outline | skills/page/page-workflows/haipipe-page-outline/SKILL.md | Page Workflow Step contract | d1.synthesize | ? unknown | 0.42.0 | 731 | ?; not assessed in this revision | ? | current Page-global paragraph and Outline contract inspected |
| haipipe-page-evidence | skills/page/page-workflows/haipipe-page-evidence/SKILL.md | skipped typed-local Page Workflow Step contract | d1.synthesize | ? unknown | 0.22.1 | 342 | ?; not assessed in this revision | ? | D1 root skips typed local LAND but keeps direct Result/cite lineage |
| haipipe-page-content | skills/page/page-workflows/haipipe-page-content/SKILL.md | Page Workflow Step contract | d1.synthesize | ? unknown | 0.14.0 | 237 | ?; not assessed in this revision | ? | current Page release barrier inspected |
| haipipe-page-check | skills/page/page-workflows/haipipe-page-check/SKILL.md | Page Workflow Step contract | d1.synthesize | ? unknown | 0.8.1 | 346 | ?; not assessed in this revision | ? | re-audit on shared-contract change |
| haipipe-plugin-outline | skills/page/page-plugins/haipipe-plugin-outline/SKILL.md | Outline/Evidence artifact contract | d1.synthesize | ? unknown | 0.65.0 | 566 | ?; not assessed in this revision | ? | current nested Evidence/Outline contract inspected; stale internal `rp01` prose references remain in the Page owner |
| haipipe-run | skills/run/haipipe-run/SKILL.md | Level-4 contract | d1.acquire | ? unknown | 0.19.0 | 541 | ?; not assessed in this revision | ? | current native Run/Page-facing projection inspected |
| haipipe-plugin-runs | skills/page/page-plugins/haipipe-plugin-runs/SKILL.md | read-only presenter | d1.acquire, d1.close | ? unknown | 0.23.0 | 333 | ?; not assessed in this revision | ? | current two-lane presenter inspected |
| haipipe-discovery-search | skills/discovery/1_search/haipipe-discovery-search/SKILL.md | acquisition/identity router | d1.acquire | ✅ structurally valid | 0.7.1 | 137 | ?; static quality not assessed | fresh-context 2026-09-20 route PASS; external search unverified | External provider routing stays below canonical identity and Run allocation |
| arxiv | skills/discovery/1_search/arxiv/SKILL.md | preprint FIND worker | d1.acquire | ✅ structurally valid | 0.1.1 | 203 | ?; static quality not assessed | ? | field-test when worker changes |
| semantic-scholar | skills/discovery/1_search/semantic-scholar/SKILL.md | venue FIND worker | d1.acquire | ✅ structurally valid | 0.1.1 | 210 | ?; static quality not assessed | ? | field-test when worker changes |
| exa-search | skills/discovery/1_search/exa-search/SKILL.md | web FIND worker | d1.acquire | ✅ structurally valid | 0.1.1 | 177 | ?; static quality not assessed | ? | field-test when worker changes |
| openalex | skills/discovery/1_search/openalex/SKILL.md | optional structured metadata/citation FIND worker | d1.acquire | ✅ structurally valid | 0.1.0 | 86 | ?; static quality not assessed | fresh-context 2026-09-07 PASS (/root/discovery_external_refresh_fieldtest); fresh-context 2026-09-07 PASS (/root/discovery_final_fieldtest); helper --help green; fresh-context 2026-09-07 PASS (/root/discovery_external_inventory_final) | Live API/query not exercised; run a bounded fixture/API smoke when credentials/network are available |
| gemini-search | skills/discovery/1_search/gemini-search/SKILL.md | optional alias/subproblem FIND worker | d1.acquire | ✅ structurally valid | 0.1.0 | 66 | ?; static quality not assessed | fresh-context 2026-09-07 PASS (/root/discovery_external_refresh_fieldtest); fresh-context 2026-09-07 PASS (/root/discovery_final_fieldtest); unavailable-source behavior inspected | MCP/CLI unavailable in test; run a live optional-source smoke when configured |
| alphaxiv | skills/discovery/1_search/alphaxiv/SKILL.md | quick READ worker | d1.acquire | ✅ structurally valid | 0.1.1 | 176 | ?; static quality not assessed | ? | field-test when worker changes |
| deepxiv | skills/discovery/1_search/deepxiv/SKILL.md | progressive READ worker | d1.acquire | ✅ structurally valid | 0.1.1 | 223 | ?; static quality not assessed | ? | field-test when worker changes |
| paper-analyzer | skills/discovery/1_search/paper-analyzer/SKILL.md | deep READ worker | d1.acquire | ✅ structurally valid | 0.1.0 | 52 | ?; static quality not assessed | ? | field-test when worker changes |
| haipipe-discovery-review | skills/discovery/2_review/haipipe-discovery-review/SKILL.md | per-Subject review router | d1.acquire | ✅ structurally valid | 0.7.1 | 84 | ?; static quality not assessed | fresh-context 2026-09-20 extraction contract PASS | Unresolved source/locator remains pending; confidence means packet fidelity, not study quality |
| research-lit | skills/discovery/2_review/research-lit/SKILL.md | multi-source craft worker called by Synthesize | d1.synthesize | ✅ structurally valid | 0.2.2 | 432 | ?; static quality not assessed | fresh-context 2026-09-07 PASS (/root/discovery_final_fieldtest); fresh-context 2026-09-07 PASS (/root/discovery_external_inventory_final) | no route divergence observed; optional live-source execution remains to be exercised |
| comm-lit-review | skills/discovery/2_review/comm-lit-review/SKILL.md | communications craft worker called by Synthesize | d1.synthesize | ✅ structurally valid | 0.1.0 | 312 | ?; static quality not assessed | ? | field-test when worker changes |
| academic-researcher | skills/discovery/2_review/academic-researcher/SKILL.md | cross-discipline craft worker called by Synthesize | d1.synthesize | ✅ structurally valid | 0.1.0 | 265 | ?; static quality not assessed | ? | field-test when worker changes |
| haipipe-discovery-synthesize | skills/discovery/3_synthesize/haipipe-discovery-synthesize/SKILL.md | cross-Result synthesis router | d1.synthesize | ✅ structurally valid | 0.3.1 | 170 | ?; static quality not assessed | fresh-context 2026-09-20 conflict scenario PASS | Preserve conflicting Results; no local D1 or Page Run |
| haipipe-ideation | skills/ideation/haipipe-ideation/SKILL.md | sibling semantic direction/idea handoff | d1.synthesize → Paper P0 | ✅ structurally valid | 0.2.0 | 351 | ?; static quality not assessed | fresh-context validation required after Discovery route change | Task/Discovery pointer bundle and human selection remain required; no local Discovery Run |
