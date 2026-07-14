insight — Changelog
===================

## [TOMBSTONE MAINTENANCE] — 2026-07-14

The layer stays retired; only the tombstone's FORWARD POINTERS were corrected. `README.md`'s
"Where the functions went" section had been written against machinery that has itself since been
retired (`Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/` v3, JL 2026-07-14): the PPNN card's `## Verdict`, the `_ASK/` stub
chain, and the gateway agent's SWEEP. All three are dead.

- **K** no longer "→ the PPNN card's `## Verdict`". It SPLITS: the general, reusable FACT →
  the executor's `<leaf>/QA/<n>-<slug>.md`; the paper-specific JUDGMENT → that paper's own
  `1-claims.md`. (A K card tried to be both at once — which is why it was never written.)
- **W** no longer "→ PPNN card → `_ASK/` stub chain". It is a SECTION in the paper's own
  `1-probes/PPNN_<topic>.md`, whose `commission:` reaches the executor's `qa` verb.
- **Cross-consumer reuse** is no longer "the gateway's SWEEP item 1b" (there is no gateway). It is
  a plain `grep {tasks,discoveries}/**/QA/*.md` — the bank's readable corpus, general by
  construction.
- No skill, agent or archived file changed. Nothing was resurrected.


## [RETIRED] — 2026-07-12

**The insight layer is fully retired (JL ruling).** All skills, agents, refs and scripts moved to `_archive/` and de-registered (7 `/haipipe-insight*` skill symlinks + 9 `card-*` / `index-integrity-auditor` agent symlinks removed). This folder is now a tombstone: README + this CHANGELOG + `_archive/`.

Why: zero K cards and zero W cards had ever been written, in any project; zero `insights/INDEX.md` files existed. The DIKW ladder was a design promise, never a practice — so retiring it cost nothing at runtime.

Where the functions went, and what replaced the one real loss (cross-consumer reuse of a settled judgment): see `README.md` in this folder, and `probe/haipipe-probe/CHANGELOG.md` [7.9.0].

Everything below this line is the history of the layer while it was live.

---

insight — Changelog
======================

Layer-scoped changelog for the insight (KNOWLEDGE / archive) layer. Newest
first. Rollup lives in the plugin-level `CHANGELOG.md`.

## [3.2.0] — 2026-07-05

### Fixed (skill-set review, JL; ledger = SKILLSET_REVIEW.md)

- **Narrative layer purged family-wide** (JL: "现在已经没有narrative了，insight只会被probe call。直接都删掉。"): ~40 references deleted across orchestrator, review skill (its narrative scope block replaced by a discovery scope), ref/ (namespace `narrative:` removed from schema + review-contract; `by_narrative` view removed from index-templates), play/, DESIGN, and the two K agent files. Caller model everywhere: probe (Deposit step) or the user directly.
- **Recut stragglers closed**: `ref/invocation-modes.md` rewritten (was still ≥2-D I gate + judged-K gate; now dataset-based I rule, K = claim + basis + confidence + claim_type, `--id` pre-assignment honored); K writer gains `claim_type` end-to-end (2.0.0); explore FULLY REWRITTEN to the recut model (2.0.0, JL: "重新写吧"); schema K validation now checks claim_type and its W example gained the required `## Risk posture` + current `plan new` verb; dikw-boundaries K01 example + play/04 example cards made schema-valid; old-D examples in review-contract + card-granularity re-labeled (metric contrasts are I, not D); body budgets unified on the schema's.
- **K source rule settled to option B** (JL: "我也倾向B。"): K `sources` may cite the I card(s) generalized OR a namespaced external origin (probe:/lit:/discover:) when no I exists; schema + index-integrity-auditor aligned.
- **Contract-drift fixes**: index-integrity-auditor's invented status enum replaced by the schema enum (`deposited` was probe vocabulary; `contested`/`acted_on` were being false-flagged) and its source-legality row widened to the schema's; wisdom creator now forwards the apply-assigned `--id` (the one creator missing it: parallel W fan-out collided); review sidecars' home `insights/_reviews/` stated in all 5 reviewers + README + review skill; Codex fallback line added to the 4 card reviewers (JL: "okay。没有的话就fallback"); "G-ask" renamed to application-ask (JL: "改成现在的吧"); `.insight-console.yaml` fictional routing signal removed (JL: "删掉吧"); views/ reworded to the dual-mode contract (co-pilot with a human; --auto when a subagent calls; JL).
- **Dead paths zeroed**: 4 writers' `../../ref/` and review's bare `ref/` (24 pointers) now resolve; orchestrator play/scripts depths fixed; okf-compat example command rooted.
- **export_okf.py**: external-ref carve-out now applied to `ref_by` (spurious "dangling ref_by" warnings gone); `--out` rmtree guarded (refuses non-`okf`, non-empty targets).
- **Ledgers trued up**: all 7 skill changelogs actually newest-first; knowledge/review versions bumped past bodies that had outrun them; DESIGN header at v3.1.0 with real read-first pointers.
- D1 follow-up resolved (JL: "delete it."): ask-session removed as a review scope family-wide (orchestrator + review skill + review-contract); application keeps only READ-side citations (`app:ask:` refs stay legal) and the outbound question redirect; "ask report phase" trigger phrases and "can chain this" caller claims scrubbed from creators + writers.
- E5 resolved option A (JL: "我记得我说了选A"): the checklist stays with the reviewed material; orchestrator boundary reworded to "permanent artifacts only under insights/".

## [3.1.0] — 2026-06-22

### Added / fixed (post-apply hardening, JL audit)
- **Causal axis (new K field).** K cards now carry `claim_type: associational |
  causal`, ORTHOGONAL to `confidence`. `causal` requires a valid identification
  (RCT / strong valid IV / RDD / DiD+parallel-trends) named in `## Generalization
  basis`; weak-IV stays associational; high confidence never licenses causal.
  Enforced by `card-reviewer-knowledge-agent` and documented in `ref/dikw-boundaries.md`.
- **Parallel-safe apply (id pre-assignment).** `apply` now pre-assigns every card
  id before fan-out and passes `--id` to each writer; the four layer writers honor
  `--id` (auto-NN only for serial writes). Closes the latent collision where
  concurrent creators all picked `D01`.
- **K->K synthesis edge formalized.** A cross-population synthesis K may `sources`
  its sibling per-population K cards (not a layer-skip); `index-integrity-auditor`
  accepts it and now checks `confidence`+`claim_type` presence INSTEAD of the dead
  "K needs a confirmed probe" gate.
- **`_reviews/` folder documented.** `insights/_reviews/` is now the canonical home
  for `<LAYER>_CARD_REVIEW.md` + `INDEX_AUDIT.md` (review provenance, not cards).
- **Coverage gaps made explicit** in the project INDEX (one-slice KB is now stated).

## [3.0.0] — 2026-06-22

### Changed (breaking — DIKW model recut, JL)
- **The cut is now in-sample DESCRIPTION (D/I) vs out-of-sample GENERALIZATION (K).**
  D describes ONE named dataset's profile; I is a pattern INSIDE that same dataset.
  Both require a `dataset:` field and carry NO p-value / CI / significance.
- **K is the generalization layer.** The inferential quantities (p-value, CI,
  confidence) live ONLY at K. A single regression output now SPLITS: estimate /
  direction / shape → I; significance / confidence → K.
- **Removed the I→K controlled-comparison-probe gate.** K has no admission gate.
  It needs a generalization basis (a significance test, robustness across
  subgroups, or a vetted external claim) and an explicit confidence — not a probe.
- **Low-confidence and negative K are recorded, not withheld.** `confidence` is the
  load-bearing K field, always present. A negative ("does not generalize", ns) K is
  valid knowledge. Documentation = recording every K regardless of confidence (not a
  new layer).
- **W reads K confidence to set risk posture** (bold for high-confidence K,
  conservative/hedged for low) and records that provenance.

### Files touched
- `ref/dikw-boundaries.md` (full rewrite), `ref/insight-md-schema.md`,
  `ref/card-granularity.md`, `ref/okf-compat.md`, `DESIGN.md`, `agents/README.md`,
  `haipipe-insight/SKILL.md`, all four layer writers
  (`haipipe-insight-{data,information,knowledge,wisdom}/SKILL.md`),
  `haipipe-insight-review/SKILL.md`, all four card reviewers + the two card
  creators (`agents/{reviewers,creators}/card-*-{data,information,knowledge,wisdom}-agent.md`),
  `play/01_plain_mental_model.md`, `play/04_cards_after_apply.md`.

### Validated
- Fresh-context subagent (not told the model) independently applied the new cut to
  a real probe (P.0605 + 4 atoms): coefficients → I, significance + ns → K (ns as
  negative low-confidence K), datasets named on D/I, K filed with no probe gate.
  The model is discoverable from the docs alone.
- Post-validation fixes: removed the stale CONFIRMED-probe gate from
  `card-creator-knowledge-agent`; made the orchestrator's `ref/` paths consistent
  (`../ref/`) + symlink-resolution note; fixed the dangling `haipipe-insight-apply`
  dispatch; pinned the `dataset:` naming convention; added granularity guidance for
  null-I (optional) and per-population vs cross-population K.

## [2.6.0] — 2026-06-21

### Added
- **Beginner play folder.** Added `play/` as a new-reader walkthrough for the
  review/apply workflow, including a plain mental model, toy walkthrough,
  example `INSIGHT_REVIEW.yaml`, example cards after apply, and card update
  rules.

## [2.5.0] — 2026-06-20

### Added
- **Card lifecycle policy.** Added `ref/card-lifecycle.md` to define how cards
  evolve after creation: stable IDs, `merge` for new evidence, `update` for
  maintenance, `supersede` for refuted/wrong-scope cards, and a body
  `## Change log` for meaningful changes.
- **Card granularity policy.** Added `ref/card-granularity.md` to control card
  size and count: one card = one reusable knowledge unit; use `merge` for
  reinforcing evidence, `split` for broad candidates, and `skip` for raw/noisy
  material.
- **Generated views contract.** Added `insights/views/{by_topic,by_source,
  by_narrative,by_status}.md` as the preferred navigation layer instead of
  adding topic subfolders under D/I/K/W.
- **Review/apply user vocabulary.** `/haipipe-insight review <folder>` now
  means "show me what is worth keeping as insight cards"; `/haipipe-insight
  apply <INSIGHT_REVIEW.yaml>` writes the accepted cards. Internally these map to
  the review/apply contract.
- **Review contract.** Added `ref/review-contract.md` to make insight
  construction explicit: task/probe/discover produce material;
  narrative/application/human review decides what becomes permanent KB;
  insight files curated D/I/K/W cards, then reviews, indexes, and audits.
- **Review skill.** Added `haipipe-insight-review/SKILL.md` for
  `/haipipe-insight review ...`, `/haipipe-insight apply ...`, and `--auto` workflows.
- **Namespaced external refs.** Insight cards can now cite external source refs
  such as `task:T.A01.02`, `probe:P.0619_film_ood`, `discover:Dsc.03`,
  `narrative:N01.C2`, `app:ask:03`, and `lit:smith2024`.

### Changed
- `/haipipe-insight` is now review-first. Direct D/I/K/W writer calls remain
  valid low-level APIs, but are no longer the recommended construction path.
- DIKW boundaries and invocation-mode docs now distinguish source production
  from archival filing. `insights/` is the curated permanent archive, not a
  session log, task log, probe log, or narrative workspace.
- OKF export now treats namespaced external refs as external sources instead of
  dangling internal graph links.


## [2.4.0] — 2026-06-19

### Added
- **OKF compatibility layer.** Added `ref/okf-compat.md` to define how the
  project-level `insights/` archive can be exposed as an Open Knowledge
  Format-style Markdown bundle without weakening the DIKW source schema.
- **Derived exporter.** Added `scripts/export_okf.py`, a read-only source-card
  scanner that writes `insights/okf/{index.md,graph.json,D/I/K/W copies}` with
  normalized `type/title/description` metadata and resolved graph links.
- **Orchestrator route.** `/haipipe-insight export-okf [project-path]` now has
  documented routing semantics and risk boundaries.

### Changed
- Insight cards now SHOULD include OKF-facing `type`, `title`, and
  `description` fields. The existing DIKW fields remain authoritative.
- New W cards should use `type: Insight Wisdom` plus `rec_type:` for the
  recommendation subtype. Legacy W cards using `type:` as the recommendation
  enum remain supported by the exporter.


## [2.3.4] — 2026-05-31

### Added
- **W is now wired into the probe-cycle** (the K's twin). A converged
  `haipipe-probe-loop` Step 3 now files the 🟨 K, then OPTIONALLY (◇) chains
  `card-creator-wisdom-agent --scope <new-K>` to file the per-probe 🟧 W (the
  probe's concrete next-step), scoped to the just-filed K. Skips when the probe
  implies no concrete next-step (no fabrication). The W machinery
  (`haipipe-insight-wisdom` + `card-creator-wisdom-agent` + `invocation-modes`
  W row) was already correct — only the probe-loop wiring was missing.
- The probe-cycle deliverable is now **🟨 K + 🟧 W** end-to-end; the
  narrative-cycle gets both the claim and the recommended next whip-crack.

### Changed
- Distinction made explicit: **per-probe W** (single-K next-step, filed in the
  loop) vs **strategic W** (across many K, stays cross-cycle via the report
  phase / `haipipe-insight-explore`).
- Docs threaded: `06-probe-cycle.txt` step ⑥ + gates table, `00-index.txt`,
  `07-end-to-end-claim-gap.txt`, `ARCHITECTURE.md`, `DESIGN.md` Q2 (which still
  described the pre-K-fix `card-creator-data-agent` dispatch — corrected to
  knowledge→wisdom).

### Verified
- **Dogfood-verified** on the stub (`/tmp/haipipe-dogfood/`): confirmed probe →
  K01 → **W01** ("param-matched FiLM re-test"). 13/13 `card-reviewer-wisdom`
  gates + 5/5 `index-integrity` gates green on an independent re-run (reciprocal
  K01↔W01 back-link, INDEX consistency, schema sections/enums, legacy type/cost enums,
  actionable `/haipipe-probe` command, boundary = action-not-restated-belief).


## [2.3.2] — 2026-05-31

### Fixed
- **K now sources the confirmed probe's `claim`**, not `≥1 I card`. The
  `haipipe-insight-knowledge` skill + `card-creator-knowledge-agent` +
  `ref/invocation-modes.md` (K row) now take a `probe_ref` (status==confirmed);
  the probe's `claim` becomes the K, `caveats` → counter-evidence, supporting
  I cards cited in the body. This matches `ref/insight-md-schema.md` (which
  already said K sources = confirmed probe) and unblocks a single probe-cycle
  from reaching K (the I-chain needs ≥2 D, which one cycle can't produce).
- `probe-loop` convergence dispatches `card-creator-knowledge-agent` (the K),
  closing the probe-cycle with its actual deliverable.
- `dikw-boundaries.md`: K boundary + worked example now source the probe.
- **Dogfood-verified** on a stub (confirmed probe → K01; all gates passed).


## [2.3.0] — 2026-05-31

### Added
- **Agent skeleton (the layer had none before).** `agents/` now mirrors
  task / probe, applied THOUGHTFULLY:
  - `creators/` — one thin BUILDER per DIKW layer
    (`card-creator-{data,information,knowledge,wisdom}-agent`). Each calls its
    `haipipe-insight-<layer>` skill headless (full spec → SILENT) to file one
    card, then verifies + returns. `_TEMPLATE.md` to add the next layer.
  - `reviewers/` — **per-type** (a deliberate departure from C/D's
    type-agnostic reviewers, because each DIKW card has a different boundary):
    `card-reviewer-{data,information,knowledge,wisdom}-agent`, each checking
    accuracy (Codex re-reads the cited evidence) + boundary/style — PLUS one
    cross-layer `index-integrity-auditor-agent` (the graph cannot be per-type).
- **`ref/dikw-boundaries.md`** — the canonical boundary of each layer (IS /
  IS NOT / the line to the next layer), the two promotion gates (I→K needs a
  probe; D/I describe vs K/W prescribe), and a complete cross-referenced worked
  example (D01→I01→K01→W01). Creators follow it; per-type reviewers enforce it.
- **`ref/invocation-modes.md`** — the dual-mode contract for the DIKW filer
  skills + the per-layer "spec complete" table + the structured-return schema.
- **DESIGN.md** — agentification + dual-mode + per-type-reviewer design, the
  loop-closure finding, and the asymmetry note (E vs C vs D).
- **Top-level `agents/` registry** — 9 flat symlinks added (registry 13 → 22).

### Changed
- **The 4 DIKW filer skills declare dual-mode** (`haipipe-insight-{data,
  information,knowledge,wisdom}`): interactive (ASK the missing source) OR
  headless (full spec → silent), chosen by input completeness; agent + missing
  source → `status: blocked`, never hang.
- **`haipipe-probe-loop` wired to close L0** (the change lives in probe): on
  convergence, Step 3 dispatches `card-creator-data-agent` to file the D card —
  closing the probe cycle (`probe → task → insight`, L0) the loop previously left open.

### Notes / remaining
- Higher-layer I/K/W auto-synthesis (as D cards accumulate) is NOT per-probe —
  deferred to the report phase / `haipipe-insight-explore`.
- Known model↔skill tension: `haipipe-insight-data` sources a D card from a
  *confirmed probe* (not a task); the loop wiring matches the skill as-built.
  A "D-from-task" reconciliation is a future pass.
