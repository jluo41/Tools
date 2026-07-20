haipipe-paper-seed — Changelog
==============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## 4.8.0 — 2026-07-19 — the "typically raises" block contradicted principle 5a

### Fixed
Board 260719-04-SEED-2PHASE, P2-4. The **Questions this stage typically raises** block was written in
the pre-5a spirit and gave the OPPOSITE instruction to principle 5a two pages above it:

    "NOT here: profiling OUR OWN data ... do not raise it in seed"
        vs 5a: such a question IS raised, keeps its `## Q-Seed-<n>`, takes `Answer: deferred -> RESOURCE`
    "Two questions is the usual shape. A seed raising eight has not decided what it is about."
        vs 5a + the frontmatter: "RAISE freely ... as generous as the draft needs"

Same file, two contracts — an agent obeyed whichever it read. The block now states what it actually
bounds (DISPATCH, never RAISING) and drops the count cap: the DRAFT gate sets how many go out, not
this document.

Also (D5): principle 5's "the `1-probes/` probe files carry the question SECTIONS" -> ENTRIES.

### Added
`ref/seed-template.md` — the Q-consumer block gains a `Probe:` field (`→ 1-probes/PP<nn> · QX<n>`,
or `--` when the gate DEFERRED the question). The live seed docs already wrote this line; the
template never defined it (board P2-3).

## 4.7.0 — 2026-07-19 — the gate command carries `--stage seed`

### Fixed
The done-criteria checker snippet ran `sh "$CHK" <paper_root>` with no stage filter, so the
seed gate globbed the WHOLE paper and inherited every other stage's open work. Measured on
`Paper-Personality2Opioid-MISQ2026`: the seed gate reported 5 FAILs, and 4 of them were
section-edit's placeholders — work seed does not own and cannot fix. A gate that reds on other
people's work is a gate people learn to read past, and then it stops reporting what it does own.

Now `sh "$CHK" <paper_root> --stage seed`, with a note that the flag is PART of the command.
Brings seed in line with resource's gate (`ref/08-stage-gate.md`) and the check worker's own
report format, both of which already passed `--stage`. Requires haipipe-paper-probe >= 6.1.0.

## 4.6.0 — 2026-07-19 — questions this stage typically raises

From `_console/closed/260719-01-DRAFT-RAISE-QUESTIONS.md` (R1).

### Added (JL: "是不是我们给每个stage写上，我们这里要写什么东西，一般会问到什么类型的问题？")

- **`## Questions this stage typically raises`** — the kinds of question this stage is PRONE to, named so a drafter can hunt for them instead of only stumbling into them. Until now nothing anywhere said how to FIND a question worth raising: `probe`'s DRAFT rule 2 opened "For each open question", presupposing it already existed, and the DRAFT workers only had a trigger ("when the search reveals a gap"). The mechanical half was covered — placeholder sweeps find missing numbers and citations — but the JUDGMENT half, the questions a stage is structurally prone to, had no home.
- This stage OWNS its list; the DRAFT worker points here and never restates it. One home.
- Not invented: the four `PROBE:` lines that had been sitting in `haipipe-paper-draft`'s Stage-specific notes were exactly this content, filed under the wrong PHASE (they assigned question ELICITATION to PROBE, against `probe`'s PROBE rule 1). This is where they belong.

## 4.5.0 — 2026-07-19 — D12: principle 5a constrains DISPATCH, not RAISING

JL ruling on D12 ("Yes"), 2026-07-19. His words that produced it: "feel free to add more questions … the Q-consumer is as many as possible … if there's no one here, I think you should propose a new question."

The problem: principle 5a read "**Seed probes are FEASIBILITY only**" and told the agent, when DRAFT surfaced a non-feasibility need, to "DO NOT open a seed probe for it". Read literally that forbids RAISING — so an agent drafting a seed would suppress a real question rather than write it down, and the anchor loop (`[Q-Seed-<n>]` cited inline from the sentence it hangs on) would leave that sentence unanchored forever. But the cost the rule was actually protecting against is DISPATCH (agent-hours, GPU-weeks, external searches), not the sentence in the Q-consumer. Asking is cheap; the Q-consumer should be generous.

Changed
- Principle 5a retitled and rewritten as **RAISE freely; DISPATCH narrowly**. Raise ANY question the seed's prose hangs on, however far from feasibility it sits; when a sentence rests on something no existing question tests, PROPOSE A NEW ONE rather than leave it unanchored — no question shape is disqualified from being asked. The narrow part is what goes OUT: feasibility-shaped only (novelty, external-data-obtainability), both `discover` work. A raised question of any other shape KEEPS its `## Q-Seed-<n>` block, gets NO entry in `1-probes/`, records `Answer: deferred -> RESOURCE`, and carries the `[FORWARD -> RESOURCE]` pointer of principle 5c. **The DRAFT gate is where the split is decided** — the user rules per question.
  The "no entry in 1-probes/" clause matters mechanically: it keeps a deferred question from becoming a `planned` survivor that `check-probe-cards.sh` would fail at the CHECK gate.
- DRAFT phase block — was "raise the feasibility questions as ENTRIES in 1-probes/". Now: raise EVERY question the draft hangs on as a `## Q-Seed-<n>` block + inline `[Q-Seed-<n>]` citation; the gate then rules which are DISPATCHED (also get a `1-probes/` entry) and which are DEFERRED (block only, forward pointer). Planning (①ORGANIZE + ②MATCH) applies to the dispatched entries.
- PROBE phase block — "That is the seed's whole probe scope" → "the seed's whole DISPATCH scope; this phase runs exactly the entries the DRAFT gate approved, no more". A non-feasibility question is now described as legitimately RAISED and then deferred at the gate, not as something that should never have existed.
- Principle 5 — "Q-consumer is explicit" → "explicit, and generous": it makes EVERY question the draft hangs on visible, as many as the draft needs; `1-probes/` carries only the dispatched ones.
- Done-criterion — the Q-consumer criterion no longer says "carries the feasibility questions"; it requires every question the draft hangs on, each anchored, each marked DISPATCHED or DEFERRED by the gate.
- Handoff — "Seed KEEPS its own probe policy" → "its own DISPATCH policy"; "novelty probes" → "novelty questions".
- Frontmatter `summary:` rewritten to lead with RAISE freely / DISPATCH narrowly.
- `ref/seed-template.md` (the single source of truth for fill rules) — the Q-consumer RULE opens with "every question the draft raises" and gains two bullets, RAISE FREELY and DISPATCH NARROWLY, stating the gate split and the deferred form. The `Answer:` placeholder documents `deferred -> RESOURCE`.

Untouched (deliberately)
- Every `mode: light | full` reference, including PROBE's `(mode light)` — deferred to a separate review.
- Principle 5b (DRAFT may search; PROBE must bind) and 5c (the one emitted forward-pointer form) — both already constrain dispatch/binding rather than raising, and 5a now leans on 5c explicitly.

## 4.4.0 — 2026-07-19 — BREAKING: `_CITATION_0-seed.md` sidecar RETIRED; Formatting/`##` contradiction fixed

JL ruling, 2026-07-19 (Paper-Personality2Opioid seed redo): "we should delete it. do not use it." The 4.3.0 sync had deliberately left the `_CITATION_0-seed.md` harvest rule untouched; that is now reversed — seed keeps NO stage-local sidecars at all, matching the rule resource already had (`haipipe-paper-draft/SKILL.md` "NO SIDECARS"). Found the hard way: an agent drafting a seed read the artifact-spec bullet and regenerated the file, and it did so BEFORE any probe had run — the bullet's own "only when the probe returns literature" condition was unenforceable because nothing checked it.

- Artifact spec bullet (SKILL.md:36) — `_CITATION_0-seed.md` line REPLACED by an explicit NO SIDECARS prohibition naming the retired file, so the next reader sees a ban rather than an absence.
- Location block — the `_CITATION_0-seed.md` row dropped; the probe-file row now says where candidates actually live.
- PROBE phase description — "sources harvest into _CITATION_0-seed.md" → "sources harvest into the ENTRY's own `**sources**:` lane".
- NEW HOME for citation candidates: the probe ENTRY's `**sources**: harvest: OWED` lane in `1-probes/PPNN_<topic>.md` (already in `probe/haipipe-probe/ref/probe-template.md` under "Harvest lanes"). No new mechanism was invented; the sidecar was redundant with one the probe template already had.
- SATELLITE SWEEP, ROUND 1 (incomplete — see round 2) — `paper/2-phase/1-probe/haipipe-paper-probe/ref/per-stage-dispatch.md` carried the SAME rule in TWO more places (lines 34, 80); both rewritten.
- Formatting clause (SKILL.md) — fixed a self-contradiction a fresh-context reviewer caught: it said "No `#`/`##`/`###`" while `ref/seed-template.md` mandates `## Q-Seed-<n> · <title>` for Q-consumer blocks. Now carves out that one sanctioned exception and states the template wins.

### ROUND 2 — the same-day fresh-context validation caught round 1 short (recorded because the failure mode matters more than the fix)

A naive-reader validation agent, given only the revised skill and asked "what files would you create", found round 1 had missed the file that actually EXECUTES the phase. Three corrections, plus a retracted claim:

- ❌ RETRACTED: round 1 claimed "live references to `_CITATION_0-seed.md` are now zero outside CHANGELOG history." FALSE when written. The round-1 grep searched the literal filename `_CITATION_0-seed`, but `haipipe-paper-draft/SKILL.md` says `_CITATION_` generically — so the two lines that MANDATE the sidecar (:33, :125) survived, in the one file seed's DRAFT phase dispatches to. Worse, that file's only NO-SIDECARS line sat under `### resource`, so *expressio unius* actively told a reader that seed DOES get one. Lesson: sweep the CONCEPT, not the filename.
- WRONG DESTINATION, fixed: round 1 rehomed owed citations onto the probe ENTRY's `**sources**: harvest: OWED` lane. That lane is a checker FAIL (`check-probe-cards.sh` rule 7: "harvest: OWED -> FAIL on any lane line") and is written at PROBE harvest, never at DRAFT. The checker's PASS 2 header states the real rule and was authoritative all along: "`1-probes/` is the only consumer-side source of truth; `_LOG` is the only kept sidecar." Owed `\cite{TOADD}` now goes to `_LOG_0-seed.md`, in this skill, in per-stage-dispatch.md, and in the draft worker.
- Principle 7 restated "No `#`/`##`/`###`" WITHOUT the carve-out added to the Formatting clause, 160 lines below it — so an agent reading top-to-bottom would strip the `## Q-Seed-<n>` blocks the `[Q-Seed-<n>]` anchor loop depends on. Both statements now carry the exception.
- Cross-skill contradiction fixed in `haipipe-paper-draft`: it described 0-seed.md as THREE sections in three places, omitting Landscape and Q-consumer — the second of which is where every `[Q-Seed-<n>]` anchor lives. An agent following the worker's Step 3 would present a 3-section plan and fail this skill's own done-criterion 1.

## 4.3.0 — 2026-07-19 — sync to probe constitution v9.5.0 (Q-executor-entry probe-file format)

Synced the probe-file-anatomy references to the new v9.5.0 shape across the artifact-spec bullets, the Location block, the DRAFT/PROBE phase descriptions, principle 5b, and the done-criteria: a probe entry is now `## QX<n>` with `### q-executor` / `### q-consumer` / `### bank binding` (`route` / `bank` / `target` / `state`) / `### a-executor`. Field renames: `serves:`→a `### q-consumer` bullet (the `Q-Seed-<n>` id + original question), `match:` (`EXISTS`/`NONE→NEW`)→`bank: reuse | run | code | new`, the probe-file `a-consumer:`→`### a-executor`, "SECTION"→"ENTRY", and the per-file `## Why` DROPPED — the stake lives in each stage-doc Q-consumer. Unchanged (deliberately): the stage-doc `## Q-Seed-<n>` Q-consumer block and its `Answer:` (station ②) — only the probe-file entry moved; the `_CITATION_0-seed.md` harvest and `\cite{TOADD}`/`{VAL:?}` citation rules are untouched. No archaeology tags were present in this SKILL.md to strip.

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
- An interim step this same session extracted the rules OUT to the skill's Artifact Spec and added an interim template-skill-split doc. JL reversed it: "I don't want the wiki things … keep the rules in the template markdown file." That doc was deleted and the rules returned to the template as `<!-- RULE -->` comments. Final state is above.

JL design comments (verbatim, resolved out of the template into this record):
> JL: So the question should be also I don't know used to spot your content in this draft. You know, we don't want to ask questions like it's detached from the drought to do gather lemming. So we want to make it consistent.
> JL: I don't want the wiki things … keep the rules in the template markdown file.


## 4.1.0 — 2026-07-14

- "PP card skeleton" / "card state" / `status: planned` -> question SECTION / SECTION STATE / `state: planned`. The DRAFT-vs-PROBE invariant is now stated as: `planned` + empty `target:` (DRAFT) vs `read` + a `target:` that RESOLVES to a QA file (PROBE).
- The PROBE worker's ownership line no longer says "card creation/format, index bookkeeping": it owns the probe file + its sections, MATCH, dispatch, and the `target:`/`reading:` backfill.

## [4.1.1] — 2026-07-14 — the required-reads were off by one `../`

Fixed
- **The first instruction in this skill pointed at nothing.** `Read first: ../../PHILOSOPHY.md, ../../<shared-refs>/04-lifecycle-map.md` — but this skill lives at `skills/paper/1-lifecycle/<N>-<stage>/<skill>/`, so `../../` is `1-lifecycle/`, which holds neither `PHILOSOPHY.md` nor the shared-reference folder. Both live one level further up, at `skills/paper/`. Every in-body citation (stage-gate, comment-lifecycle, stage-illuminate, delivery-need, `../../_venue/playbook-<venue>`) failed the same way, silently — an agent loading the philosophy and the stage-gate rules got file-not-found and proceeded without them. All repointed to `../../../`; every target verified to resolve on disk.

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
- Phase visibility pointer added (Phase Transition Contract, 08-stage-gate.md): announce every boundary, no silent skips, CHECK opens with the exit-criteria report + approval ask.

## [3.0.1] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER -> PROBE, POLISH -> REVISE; workers haipipe-paper-probe*, haipipe-paper-revise*).

## [3.0.0] — 2026-07-03

- seed becomes stage orchestrator that drives its own phases. Phase skills (draft/polish/check) are internal workers called by this skill, not user-facing. Simplified to 3 sections (question/motivations/claim-shape). Comment lifecycle wired in. All ref/ docs re-homed.

## [2.1.0] — 2026-07-03

- simplified seed to 4 sections (question/motivations/claim-shape/promotion-gate); removed current-evidence-status, open-evidence-needs, kill-criteria (belong in claims, not seed); removed 'prospectus' terminology.

## [2.0.0] — 2026-06-29

- switched from .tex to .md + _LOG. Argument documents are markdown; only display compiles to PDF.

## [unversioned]

- v1.1.1: added mandatory compile-after-edit rule; venue awareness note

## [1.1.0] — 2026-06-22

- added illuminate+gate+compile protocol (08-stage-gate.md, 09-stage-illuminate.md, 13-tex-quality.md)

## [1.0.0] — 2026-06-22

- baseline.
