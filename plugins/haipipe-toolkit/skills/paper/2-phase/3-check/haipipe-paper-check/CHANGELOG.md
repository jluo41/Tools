haipipe-paper-check — Changelog
===============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [0.3.0] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 3.0.0; older entries below keep their original numbers).

## 3.0.0 — 2026-07-19

Changed (JL 2026-07-19, paper/2-phase refactor — the sidecar model is retired: `1-probes/` is the only consumer-side source of truth, `_LOG_<stage>.md` the only sidecar)

- **What CHECK walks is RE-ROOTED**: the stage doc (or section `.md`) + the paper's `1-probes/` entries. Every `_CITATION_` / `_VALUES_` / `_DISPLAY_` reference is gone from SKILL.md — they were load-bearing in NINE places (frontmatter summary, step 2.5 comment-seeding targets, the one-shot `./checks.sh` invocation, the Citation table, the Values table, the report-format SEEDED example, Citation verification, Values verification, Display review, and the seed row of the per-stage gate table). A checker that scores a document nobody writes reports a metric it cannot compute.
- **📚 PROBE checks restructured** around the DRAFT contract "every hole is FILLED or OWNED". New leading table (**The entries**): `check-probe-cards.sh --stage <key>` exit 0 · every `\cite{TOADD}` / `{VAL:?` carries a `[Q-<Stage>-<n>]` id (a bare placeholder = a hole nobody owns) · every id resolves to a Q-consumer block AND a bound `## QX<n>` entry · the entry's `### a-executor` is non-empty. Citation/Values/Display tables re-rooted onto the `### a-executor` bodies: 🔍 sources are greppped there, and a placed value must satisfy `grep -F '<value>' <the source path the a-executor names>` (the fabrication guard, mirrored from the probe worker's ⑤).
- **Display track** now reads `0-lifecycle/4-display/_DISPLAY_REQUEST.md` for DR rows short of `done` — 📨 pending, flagged for CHECK, never a pre-placed `\ref` for a unit that does not exist.
- **Human Actions** re-rooted: Citation verification, Values verification, and Display review now open the `1-probes/PP*.md` entries the report names. Step 7 of citation verification states where a verified key LANDS: the `\cite{TOADD} [Q-<Stage>-<n>]` hole that owns it.
- **Vocabulary**: `section` → ENTRY, `serves:` → `### q-consumer`, `card` → entry throughout (`--stage` scoping, the resource gate rulings block, the resource row of Who-calls-this-skill). `## Locating the card checker` → `## Locating the probe checker`; the script's `check-probe-cards.sh` filename is unchanged and still load-bearing.
- **PROBE restart** guidance: new-candidate requests become `## QX<n>` ENTRIES (was "question SECTIONS").

Fixed

- **`checks.sh` no longer asserts a dead marker is the convention.** The TODO-marker block's rationale claimed `% TODO[values]` / `% TODO[cite]` are "planted in comments by DRAFT and MUST block the gate until PROBE fills them" — that convention is retired (1.8.1 already marked the flags legacy, but the comment still taught them as live). The TODO/FIXME grep itself STAYS at the ❌ tier on its own merit: unfinished work parked in a `%` comment is exactly work hidden from the compiled PDF. The two LIVE markers (`\cite{TOADD}`, `{VAL:?}`) are enforced elsewhere, not here.
- **`checks.sh` `--md` header** re-rooted: "a markdown working doc (`_CITATION_`/`_VALUES_`/outline)" → a stage doc, a section `.md`, or a `1-probes/PP*.md` entry file.

## 2.1.0 — 2026-07-14

- "planned/dispatched cards" -> `planned` sections + unresolvable `target:`s; `status: planned card` -> `state: planned` section. (`check-probe-cards.sh` KEEPS its filename; only its internals changed.)
- PROBE restart: new-candidate requests from `> USER:` comments become question SECTIONS in `1-probes/`, dispatched by the PROBE phase (was "probe plans -> gateway").

## [1.9.0] -- 2026-07-14
## 2.0.0 — 2026-07-14

- PROBE REDESIGN (Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14 — R1-R18). 1-probe-plans/ -> 1-probes/ (PPNN_<topic>.md, one file per TOPIC, one SECTION per question: serves/target/state/commission/reading + ONE `## Why` per file holding the stake). Binding is by PATH: a section's `target:` points at the answering `<leaf>/QA/<n>-<slug>.md` in the bank. DELETED: `## Verdict`, the `verdicted` and `dispatched` states, `_ASK/`/`_ANS/` stubs, `answers:`, and Agent(haipipe-probe-orchestrator-agent) (the GATEWAY — archived + de-registered). A claim's STATUS now lives ONLY in 0-lifecycle/1b-claims/1b-claims.md. Dispatch is now DIRECT: the section's `commission:` block, VERBATIM, to Agent(haipipe-task-orchestrator-agent) / Agent(haipipe-discovery-orchestrator-agent).
- The seed done-criterion re-stated for probe SECTIONS: every section's `reading:` written and every `target:` resolving on disk.

Added (BLOCKER 10 repair -- the worker that RUNS Gate 2 did not know the resource stage existed)

- **`resource` row in the per-stage gate table** (Applicability Beyond Section-Edit). Before this, a live resource CHECK had NO gate criteria to apply -- the stage shipped a load-bearing sentence that the executing worker had never heard of. The META column now carries it VERBATIM: "Does every hypothesis have a resource that is HAVE+FIT, or a COMMISSIONED build with an owner and a DATE, or a SCOPE CUT the human said out loud?" The PROBE column carries the stage-scoped card pass (`sh "$CHK" <paper_root> --stage resource` exits 0).
- **Resource gate rulings block**, below the table: `commissioned` + owner + future eta -> PASS; no owner -> FAIL (an unowned build is a wish); eta PASSED with no receipt -> FAIL (C6); a BUILD card with no `cross-project:` -> FAIL (C4); a fitness ruling that does not say what it KILLS -> FAIL; **a demand with NO resource is NOT a failure -- it is a SCOPE CUT, said out loud and logged.** Card-status rulings are checker-enforced (RUN it, never eyeball); fitness + scope cut are `> CHECK:` judgment items.
- **`haipipe-paper-resource` row in Who calls this skill.**

Changed

- **Stage Exit Invariant AMENDED: two directions for every stage EXCEPT `resource`, which has THREE** (JL ruling C7, 2026-07-14; spec in `08-stage-gate.md`, which already carried the amendment while the EXECUTING worker did not -- so `reseed` and `park` were UNREACHABLE in practice). ✅ proceed -> claims · 🔥 reseed -> [LOOPBACK -> SEED] · 🅿️ park -> `maturity: resource-blocked`. Rationale: a stage whose PURPOSE is discovering the paper CANNOT BE WRITTEN must be able to SAY SO -- without these it could only `promote -> claims`, mechanically handing a DEAD PAPER FORWARD. The Report Format decision menu gains the two resource-only checkboxes. Does NOT generalize.
- **seed row's exit fixed**: seed now advances to **resource**, not claims.

Fixed

- **Card-checker locator is now UNAMBIGUOUS** (new section: Locating the card checker). TWO files named `check-probe-cards.sh` exist on disk -- the paper family's and the application family's -- so the old hard-coded `../../1-probe/haipipe-paper-probe/check-probe-cards.sh` (fragile: installed skills flatten the tree) and any bare `find -name check-probe-cards.sh | head -1` could resolve to the WRONG FAMILY and silently check a paper against application invariants. Now: `find ... -path "*haipipe-paper-probe*" -name check-probe-cards.sh | head -1`, plus a LOUD failure when nothing matches (`[ -n "$CHK" ] || { echo "FAIL: paper checker not found"; exit 1; }`) -- a gate that cannot run its checker has not checked anything.

## [1.8.1] -- 2026-07-10

Fixed (fresh-agent audit, C5)
- PROBE-restart guidance: placement is md-first; new-candidate requests become probe plans -> gateway (was "search for new candidates").
- checks.sh header: TODO[] flags marked legacy (DRAFT plants {VAL:?}/\cite{TOADD} in the .md).

## [1.8.0] -- 2026-07-09

Changed (JL ruling 2026-07-09 (LLMTrait-Section session postmortem): normalize the writing process)
- checks.sh: new `--log <file>` check -- the newest [REVISE] entry in a _LOG must carry its `workers:` proof line (missing = FAIL; REVISE present without a [GATE] draft-review on record = WARN). Enforces the proof-carrying REVISE dispatch contract.

Fixed
- checks.sh: `mapfile` replaced with portable while-read loops (macOS /bin/bash 3.2 has no mapfile -- dir-mode tex scan and .bib discovery silently broke, making broken-cite checks unreliable on Macs); empty --log array guarded for set -u under bash 3.2.

## [1.7.0] — 2026-07-07

Changed (skillset-diagnose FIX round; threads T1/T10 + findings D2-D9)
- Gate wiring (T1, JL: "同意你的意见"): step 1 Run now ALSO runs the probe checker `check-probe-cards.sh <paper_root>` — a FAIL line (planned/dispatched card, unresolved ref, `harvest: OWED` lane, bibtex/table in a working doc) means the gate cannot go green. Closes the seed-stage incident class (probe ✅ shown over an unrun probe; three sibling docs had promised this wiring, code was absent).
- em-dash upgraded ⚠️→❌ in checks.sh (T10, JL: "统一提议。") — absolute house rule, same tier as TODO; AI-voice/Pn.Sn stay ⚠️ (false-positive room). SKILL row note added.
- Decision enumeration: intro line 25 (D2) and the flow diagram (D3) reconciled to the full 5 outcomes (proceed/restart/new round/accept/park).
- checks.sh hardening: bibtex-leak grep matches ANY entry type via `@word{key,` shape (D4; was 7 hardcoded types); XXX dropped from TODO tier — collides with double-blind placeholders (D5); `\cite` present + no .bib found is now a loud ⚠️ with a --depth hint, not a silent skip, and the split-bib-below-depth false-positive caveat is documented (D6); AI-voice grep runs on comment-stripped text like em-dash (D8); `--depth`/`--md` argument parsing guarded against flag-swallowing (D9).

Changed (skill-quality pass: contract was sound but prose was ~412 lines with each rule stated 4-6×, guaranteeing drift on the next edit)
- De-duplicated: "CHECK is the ONLY human phase" collapsed from ~6 statements to 2 (intro + one anti-pattern); bibtex rule collapsed from ~6 to 2 (one bolded rule + one anti-pattern, anti-patterns 387/388 merged); the per-track "human action during CHECK" blocks that duplicated the standalone section removed from the Sub-Checker tables and folded into a single **Human Actions During CHECK** home; the "three parts" list folded into the intro so the flow is shown once as diagram + one step list.
- Frontmatter: dropped the nonstandard `predecessors:` key (proof-checker relation already documented in-body); version → 1.6.0, last_updated → 2026-07-07; outcome enumeration reconciled to the full 5 (proceed/restart/new round/accept/park) everywhere.
- ~412 → ~285 lines, zero contract/behavior change.

Added
- `checks.sh` — self-contained deterministic MECHANICAL sub-checks: em-dash, AI-voice tells, TODO/FIXME/XXX, bibtex-in-markdown, broken `\cite` (not in any .bib), broken `\ref` (no matching `\label`), orphan `\label` (defined, never `\ref`-ed → ⚠️), and Pn.Sn sequence (gaps/dupes per ¶ → ⚠️). Emits ✅/⚠️/❌ lines for direct paste into the report; comments stripped so `%% ---- Pn.Sn ----` markers don't false-flag as em-dashes; exit 1 on any ❌. Flags: `--md <file>` (bibtex-leak scan of a working doc, repeatable), `--depth N` (widen tex/bib scan for deep layouts / split bibs), `--compile` (opt-in, wraps `./1-compile.sh` and greps its log for LaTeX errors). `_external/` and `_archive/` trees excluded so reference bibs don't mask real broken cites.
- AI-voice list tuned to high-signal tells only (delve/utilize/tapestry/seamless/showcase/intricate/nuanced/realm/underscore/leverage); noisy academic connectives (Furthermore/Moreover/Additionally) dropped — on a live paper they produced 8 false hits and buried the 1 real one.
- The stale `check_refs.py` reference (the script lived only under `_archive/`) is retired — the META `\label/\ref`/compile and PROBE `\cite`/bibtex rows now point at `./checks.sh`, which is shipped in-folder and validated against a real paper (`Paper-FairGlucose-icml2026`: caught 3 real broken cites, 5 broken refs, 4 TODOs).

## [1.5.2] — 2026-07-05

Changed (JL: 为啥不叫comments — one mechanic, one name)
- "pin" vocabulary dropped throughout: the feature is plain `> CHECK:` comments (comment family: > USER: / > CC: / > REVIEWER: / %% {CC-worker}: / > CHECK:). Report line renamed PINS SEEDED -> CHECK COMMENTS SEEDED. Mechanics unchanged.

## [1.5.1] — 2026-07-05

Fixed (audit of 1.5.0: pin contract landed in the front half, back half still spoke pre-pin language — the sections a fresh session reads as the operational contract)
- On-restart reads pins + replies (unanswered pin = surfaced back, never silently skipped); done criteria gain pin-seeded + pin-replied gates; anti-patterns gain clean-file handover + pin-ignoring; Human Actions entry point = walk the pins (not self-service flag hunting); pin targets include _DISPLAY_; report Summary carries a PINS SEEDED line (count + files).

## [1.5.0] — 2026-07-05

Added (test-123333333: JL entered 0-seed.md for the CHECK pass and found a clean file — flags lived only in the chat report; JL: "check的时候我需要进去仔细看，然后你加comments 之类的，这些你有做吗")
- SEED THE PINS (step 2.5, mode-independent): every flagged/🔍/⚠️ report item is planted as ONE `> CHECK:` comment at its exact spot in the working doc (issue + judgment needed, concrete values). Chat report = map, in-file pins = what the human walks; clean-file handover is DEFECTIVE. Human replies `> USER:` per pin; restart reads pins + replies; resolved pins archive to _LOG per the comment lifecycle. Autopilot reviewer reads the pins too.

## [1.4.1] — 2026-07-04

Fixed
- Seed row PROBE check updated: `_DISCOVERY_ takeaways linked` -> `_PROBE/ plan takeaways backfilled + _CITATION_ candidates eyeballable` (naming unification).

## [1.4.0] — 2026-07-03

- Gate Modes section added (JL: copilot 人给 comments / autopilot 派 subagent 给 comments，必须有 approval 动作): mode spec owned by 08-stage-gate.md; autopilot dispatches ONE fresh-context reviewer subagent that leaves > REVIEWER: comments + returns proceed|restart|accept; HUMAN-ONLY items (Scholar bibtex verification) are marked DEFERRED into a human queue, never silently passed; humans can reopen agent-approved gates.
- Stage Exit Invariant added under What Each Decision Does (JL: only check can jump out the current stage): restart re-opens a phase WITHIN the same stage; proceed/accept is the only cross-stage move; cross-stage loopback is a lifecycle re-entry, not a CHECK outcome.

## [1.3.0] — 2026-07-03

- renamed haipipe-paper-checker -> haipipe-paper-check. Phase workers are named by the phase verb (draft/probe/revise/check); agent nouns are reserved for sub-tools (proof-checker stays).

## [1.2.0] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER->PROBE, POLISH->REVISE); sibling worker names updated; seed check row aligned with the 3-section seed.

## [1.1.0] — 2026-07-03

- reframed as internal worker. Users invoke stage skills (seed, claims, pitch...), not this skill directly. Stage skills call this during their CHECK phase.

## [1.0.0] — 2026-07-02

- created as the general auto-gate. The former checker was actually a proof-checker (mathematical proofs only); renamed to haipipe-paper-proof-checker and kept as one sub-checker.
