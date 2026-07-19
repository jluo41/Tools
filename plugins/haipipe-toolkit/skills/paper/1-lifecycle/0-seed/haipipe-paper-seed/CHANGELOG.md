haipipe-paper-seed — Changelog
==============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## 4.2.0 — 2026-07-18 — rules inline in the template; Q-consumer with linked+cited questions; +Landscape

A live co-design session with JL (2026-07-18) reshaped the seed. Net design (after one reversal — see below): `ref/seed-template.md` is the SINGLE source of truth and holds BOTH the skeleton (`<placeholders>`) AND the fill rules, the rules carried as `<!-- RULE: … -->` comments the author follows then DELETES (they never ship in 0-seed.md). No wiki doc; the skill never restates the rules, only phase behavior.

Template (`ref/seed-template.md`)
- Section `Probes` (answers inline) → `Q-consumer` (questions only): `## Q-Seed-<n>` blocks with `Description` / `Reason` / `Answer`.
- STAGE-PREFIXED question ids — `Q-Seed-<n>` (each stage owns its index — Q-Claim-<n>, Q-Pitch-<n>, …) so a cited id is unambiguous across stages.
- INLINE CITATION — a content sentence a question hangs on carries the id in a bracket, e.g. `[Q-Seed-1]` (forward link); `Reason` names every anchor it is cited from (back link). One question may be cited from several sentences/sections — that is the multi-section link.
- NEW section `Landscape` (between Motivations and Tentative Claim Shape): what others are already doing on this topic — the field map that frames the questions; sourced from the novelty/landscape feasibility probe.
- Fill rules moved INTO the template as `<!-- RULE -->` comments; top marker updated to "follow then delete the RULE comments".

SKILL.md
- Content structure no longer restates per-section rules — it points to the template's `<!-- RULE -->` comments as the single home and lists the 5 sections (Landscape added).
- `## Template`: inline template copy (had drifted, still said `Probes`) deleted; now points to `ref/seed-template.md` as the one source of BOTH skeleton and rules.
- Phase Orchestration wired to the citation lifecycle: DRAFT raises `## Q-Seed-<n>` + cites `[Q-Seed-<n>]` inline; PROBE lands the answer in `Answer` (evidence, stops there); REVISE weaves it into every citing sentence AND discharges the bracket (prose). "4 sections" → "5 sections" throughout; `Probes` section-name reconciled to `Q-consumer` everywhere it had gone stale (summary, done-criteria, Principle 5, weaving lines).
- Clarified the PROBE-vs-REVISE boundary (JL question): the loop closes at REVISE, not PROBE — born from content (DRAFT drops the bracket), dies into content (REVISE discharges it).

Reversal (recorded per decision-register discipline)
- An interim step this same session extracted the rules OUT to the skill's Artifact Spec and added `wiki/14-template-skill-split.md`. JL reversed it: "I don't want the wiki things … keep the rules in the template markdown file." The wiki doc was deleted and the rules returned to the template as `<!-- RULE -->` comments. Final state is above.

JL design comments (verbatim, resolved out of the template into this record):
> JL: So the question should be also I don't know used to spot your content in this draft. You know, we don't want to ask questions like it's detached from the drought to do gather lemming. So we want to make it consistent.
> JL: I don't want the wiki things … keep the rules in the template markdown file.


## 4.1.0 — 2026-07-14

- "PP card skeleton" / "card state" / `status: planned` -> question SECTION / SECTION STATE / `state: planned`. The DRAFT-vs-PROBE invariant is now stated as: `planned` + empty `target:` (DRAFT) vs `read` + a `target:` that RESOLVES to a QA file (PROBE).
- The PROBE worker's ownership line no longer says "card creation/format, index bookkeeping": it owns the probe file + its sections, MATCH, dispatch, and the `target:`/`reading:` backfill.

## [4.1.1] — 2026-07-14 — the required-reads were off by one `../`

Fixed
- **The first instruction in this skill pointed at nothing.** `Read first: ../../PHILOSOPHY.md, ../../wiki/04-lifecycle-map.md` — but this skill lives at `skills/paper/1-lifecycle/<N>-<stage>/<skill>/`, so `../../` is `1-lifecycle/`, which holds neither `PHILOSOPHY.md` nor `wiki/`. Both live one level further up, at `skills/paper/`. Every in-body citation (`../../wiki/08-stage-gate.md`, `../../wiki/02-comment-lifecycle.md`, `../../wiki/09-stage-illuminate.md`, `../../wiki/11-delivery-need.md`, `../../_venue/playbook-<venue>`) failed the same way, silently — an agent loading the philosophy and the stage-gate rules got file-not-found and proceeded without them. All repointed to `../../../`; every target verified to resolve on disk.

## [3.7.0] -- 2026-07-14
## 4.0.0 — 2026-07-14

- PROBE REDESIGN (Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14 — R1-R18). 1-probe-plans/ -> 1-probes/ (PPNN_<topic>.md, one file per TOPIC, one SECTION per question: serves/target/state/commission/reading + ONE `## Why` per file holding the stake). Binding is by PATH: a section's `target:` points at the answering `<leaf>/QA/<n>-<slug>.md` in the bank. DELETED: `## Verdict`, the `verdicted` and `dispatched` states, `_ASK/`/`_ANS/` stubs, `answers:`, and Agent(haipipe-probe-orchestrator-agent) (the GATEWAY — archived + de-registered). A claim's STATUS now lives ONLY in 0-lifecycle/1b-claims/1b-claims.md. Dispatch is now DIRECT: the section's `commission:` block, VERBATIM, to Agent(haipipe-task-orchestrator-agent) / Agent(haipipe-discovery-orchestrator-agent).
- ALSO fixes the vacuous checker locator: the done-criteria `find` was UNFILTERED and resolved to the APPLICATION checker first on this machine, silently asserting a paper against application invariants. Now filters on `-path '*haipipe-paper-probe/check-probe-cards.sh'` and FAILs loudly when nothing matches.

Changed (JL ruling 2026-07-14: the RESOURCE stage is inserted between seed and claims)
- Handoff: seed now promotes to `/haipipe-paper resource` (was claims). Resource hands to claims; seed -> resource -> claims -> [venue] -> pitch. Boundary stated: seed asks "is this paper WORTH doing and is the data even OBTAINABLE in principle?"; resource asks "what EXACTLY must exist, does it, and can it CARRY the claim?".
- Principle 5a: internal-data profiling forward-points to RESOURCE, not CLAIMS (it always was a prerequisite question, never a claim-status one). PROBE diagram + frontmatter summary + CHECK exit line follow.
- New principle 5c: the forward pointer has ONE emitted form -- `**[FORWARD -> RESOURCE] PPNN_<slug>**`, ASCII arrow. Resource's DRAFT consumes it with a glyph- and legacy-tolerant grep (`\[FORWARD (->|→) (RESOURCE|CLAIMS)\]`) because the 7 pointers already on disk say CLAIMS and one uses a unicode arrow. Legacy pointers are NOT rewritten.
- Unchanged: seed keeps its own probe policy (novelty + external-data-obtainable feasibility). Novelty probes do not move to resource.

## [3.6.1] -- 2026-07-10

Fixed (fresh-agent audit, C9 -- R1 alignment)
- Orientation-search weaving uses \cite{TOADD} slots (was "(Author Year)" placeholders).

## [3.6.0] -- 2026-07-09

Changed (JL ruling 2026-07-09 (LLMTrait-Section session postmortem): normalize the writing process)
- Phase VERBS on the stage (`seed <paper-dir> [draft|probe|revise|check]`); bare invocation = status, user's verb advances.
- Hard gates + binding comment rules inlined (STOP after DRAFT with [GATE] log; Skill() dispatch proof; [REVISE] workers line; never delete `> USER:` comments; surgical edits only).
- Draft diagram: `> JL:` example unified to `> USER:`.

## [3.5.0] — 2026-07-07

Changed (DRAFT-searches / PROBE-runs-real split + seed-vs-claims probe layering -- reference behavior: the Paper-CGMtoCyclePhase session; JL: "always run the real probes in the probe phase")
- DRAFT phase MAY WebSearch to orient: weave into prose + buffer feasibility probes as `status: planned` skeletons; never findings/refs into a PP card.
- PROBE phase scope narrowed to FEASIBILITY: novelty + external-data-obtainable ("can this paper exist at all?"). ALWAYS run the real orchestrator; inline search forbidden here.
- Internal-data profiling is claims-stage task work -> register a `[FORWARD -> CLAIMS] PPNN` pointer in _LOG, do not dispatch in seed.
- New principles 5a (feasibility-only) + 5b (DRAFT may search; PROBE must dispatch; the line is card state, checker-enforced).

## [3.3.0] — 2026-07-06

Changed
- Added Probes as a fourth section in the seed content structure. The seed now has: Seed Question, Motivations, Tentative Claim Shape, Probes. Probes carry the landscape/novelty check inline (PP01 takeaways visible in the document, not buried in _PROBE/ only).
- Heading style changed from `#`/`##` to `=====`/`-----` underlines for paper artifacts.
- One-sentence-per-line convention added as a formatting principle.
- Updated ref/seed-template.md to match.

## [3.2.1] — 2026-07-04

Fixed
- PROBE step route updated: the worker ALWAYS dispatches the orchestrator agent; the agent's SWEEP decides enrich / reuse-directly / create+gather.

## [3.2.0] — 2026-07-04

Changed
- Artifact spec + Location gain `_PROBE/PPNN_<slug>.md` (probe plans + backfilled takeaways; `_DISCOVERY_0-seed.md` retired) and `_CITATION_0-seed.md` (harvested candidates when the probe returns literature). PROBE step routes via Agent(haipipe-probe-orchestrator-agent).

## [3.1.0] — 2026-07-03

Changed (live seed run silently skipped PROBE+REVISE and drifted into CHECK)
- frontmatter summary listed phases as draft -> revise -> check; PROBE restored to the spine.
- PROBE no longer "optional": DEFAULT RUN for a new seed (landscape/related-work/novelty, mode light -- it answers the gate's "who cares?" / "is this new?"); skip only on re-entry/minor edits by explicit logged verdict. Direct dispatch of discovery/task agents or /haipipe-probe from the stage is forbidden.
- REVISE now explicitly weaves probe takeaways into Motivations.
- Phase visibility pointer added (Phase Transition Contract, wiki/08): announce every boundary, no silent skips, CHECK opens with the exit-criteria report + approval ask.

## [3.0.1] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER -> PROBE, POLISH -> REVISE; workers haipipe-paper-probe*, haipipe-paper-revise*).

## [3.0.0] — 2026-07-03

- seed becomes stage orchestrator that drives its own phases. Phase skills (draft/polish/check) are internal workers called by this skill, not user-facing. Simplified to 3 sections (question/motivations/claim-shape). Comment lifecycle wired in (wiki/02). All ref/ moved to wiki/.

## [2.1.0] — 2026-07-03

- simplified seed to 4 sections (question/motivations/claim-shape/promotion-gate); removed current-evidence-status, open-evidence-needs, kill-criteria (belong in claims, not seed); removed 'prospectus' terminology.

## [2.0.0] — 2026-06-29

- switched from .tex to .md + _LOG. Argument documents are markdown; only display compiles to PDF.

## [unversioned]

- v1.1.1: added mandatory compile-after-edit rule; venue awareness note

## [1.1.0] — 2026-06-22

- added illuminate+gate+compile protocol (../../wiki/08-stage-gate.md, ../../wiki/09-stage-illuminate.md, ../../wiki/13-tex-quality.md)

## [1.0.0] — 2026-06-22

- baseline.
