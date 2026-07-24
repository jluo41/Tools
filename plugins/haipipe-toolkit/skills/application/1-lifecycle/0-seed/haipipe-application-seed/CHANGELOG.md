haipipe-application-seed — Changelog
====================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [0.6.1] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 6.1.0; older entries below keep their original numbers).

## 6.1.0 — 2026-07-19 — converge on paper's seed contract (JL ruling D3)

### Changed
Board 260719-04-SEED-2PHASE, D3 — JL: "我们统一一下：Description / Reason / Answer 都是这个。
填写规则住哪 ： template 内联 <!-- RULE -->(template 是唯一家) ，(c) 也是paper的方法".

- (a) `ref/seed-template.md` Q-consumer fields `Ask:` / `Why:` -> `Description:` / `Reason:` /
      `Answer:`. The block had NO `Answer:` line at all while the Done gate tested its state, so a
      seed generated from the template could never pass its own gate (board P2-2).
- (b) The fill rules move INTO the template as inline `<!-- RULE -->` comments — the template is the
      single home. (Was: rules in SKILL, template left blank.)
- (c) The PROBE line now names the call — `Skill("haipipe-application-probe", args="from-buffer
      <root>")`. It previously said only "one worker call" while the prose named
      `Agent(haipipe-probe-q-executor-agent)`, which is the worker's INTERNAL step, not the stage's.
- The DRAFT/PROBE split is stated correctly: DRAFT authors the plan (①ORGANIZE + ②MATCH), PROBE runs
      it forward (③④⑤) and does NOT re-raise or re-match. The block previously assigned the
      five-step loop's raising to PROBE, contradicting probe/haipipe-probe/SKILL.md.
- (D5) `state: planned` sections -> ENTRIES.

### Added
`Probe:` field in the template's Q-consumer block (board P2-3), matching paper's.

## 4.4.0 — 2026-07-19 — questions this stage typically raises

From `_console/closed/260719-01-DRAFT-RAISE-QUESTIONS.md` (R1).

### Added (JL: "是不是我们给每个stage写上，我们这里要写什么东西，一般会问到什么类型的问题？")

- **`## Questions this stage typically raises`** — the kinds of question this stage is PRONE to, named so a drafter can hunt for them instead of only stumbling into them. Until now nothing anywhere said how to FIND a question worth raising: `probe`'s DRAFT rule 2 opened "For each open question", presupposing it already existed, and the DRAFT workers only had a trigger ("when the search reveals a gap"). The mechanical half was covered — placeholder sweeps find missing numbers and citations — but the JUDGMENT half, the questions a stage is structurally prone to, had no home.
- This stage OWNS its list; the DRAFT worker points here and never restates it. One home.
- Not invented: the four `PROBE:` lines that had been sitting in `haipipe-paper-draft`'s Stage-specific notes were exactly this content, filed under the wrong PHASE (they assigned question ELICITATION to PROBE, against `probe`'s PROBE rule 1). This is where they belong.

## [4.3.0] — 2026-07-18

- Kill criteria section removed from the seed doc (unhelpful at seed stage; six content sections -> five). Q-consumer question blocks renamed `## Q<n>` -> `## Q-Seed-<n>` (id carries the origin stage) and reshaped to a fixed 3-field, human-readable form: `Ask` / `Why` (carries the content-section link + failure consequence) / `Answer` (`__TO_BE_FILLED__` == OPEN, else ANSWERED — the only state the seed doc tracks). Rule prose moved out of the template into SKILL (template = skeleton, SKILL = rules). Template + SKILL (frontmatter, skeleton, Done gate, formatting) updated.

## [4.2.0] — 2026-07-17

- Q-consumer migration: the stage doc's `Probes` tail section is renamed + reshaped to `Q-consumer` (`## Q` question blocks, matching the constitution's `q-executor:`/`a-consumer:` fields); the stage RAISES questions, the PP-id/route/state organize into 1-probes/ at APPROVE. Template + SKILL (artifact list, REVISE line, Done gate) updated.

## [4.1.0] — 2026-07-17

- Template D3: probe roster placeholder + label `status` -> `state` (canonical field name).

## [1.0.0] — 2026-06-22

- initial version modeled on paper-seed.

## [2.0.0] — 2026-06-29

- added _LOG_0-seed.md changelog; output folder 0-seed/ (was flat file); borrowed .md + _LOG pattern from paper-seed v2.0.0.

## [3.0.0] — 2026-07-06

- stage folder contract; venue-FREE marker (channel = hunch, not pin); DPRC phases; scaffolding delegated to enter get-or-create (paper-alignment refactor, SOP archived in haipipe-application/CHANGELOG.md §5.0.0).

## [3.1.0] — 2026-07-06

- 765696f port: visible Probes section in the seed doc + ascii artifact formatting.

## [3.2.0] — 2026-07-07

- Port of paper seed 3.5.0 (paper-alignment round 2, SOP §4 row 7, R3+R4): DRAFT may WebSearch to orient (fuel -> prose + buffered `status: planned` skeletons); PROBE scope narrowed to FEASIBILITY only (novelty + external-data obtainability) and must ALWAYS dispatch the real worker (Skill haipipe-application-probe, from-buffer) -- inline search forbidden in PROBE; internal-data profiling (the intervention's own cohort/engagement data) registers as a `[FORWARD -> CLAIMS] PPNN_<slug>` pointer line in _LOG_0-seed.md (a pointer, not a card; consumed at claims DRAFT); new "Probe scope and FORWARD handoff" section; done-criteria gain the check-probe-cards.sh find-pattern verification.
