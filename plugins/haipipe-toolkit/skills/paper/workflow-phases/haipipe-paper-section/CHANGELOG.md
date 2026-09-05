## 0.8.2 · 260904

- Split stale upstream ownership precisely: Narrative returns to the journey;
  Venue returns to its QBv bank Page Type before Section resumes CONTEXT.
- Align the generic fallback template with typed Evidence Items and the
  Supporting Run → Local Input → Local Page Run → Result graph; remove its
  final active PageX/probe allowlist.

## 0.8.1 · 260904

- Enter every Section through the five-phase Page lifecycle beginning at
  CONTEXT and use the canonical dependency order.
- Replace active PageX/probe/bibex/value/display plugin language with typed
  Evidence Items, Supporting Runs, one Local Input, one Local Run, and one
  accepted local Result in the shared Outline plugin.
- Return stale Narrative or Venue authority to its paper-journey owner, then
  resume the Section at CONTEXT/PREPARE.
- Declare `page_ruling: none` for the unit Page; paper-level G6 remains the
  separate assembly/readiness human gate after all Sections close.

## 0.8.0 · 260902

- A Section's page-owned prose rules now live as authored `W<n>` records in
  `outline/<stem>-requirement.md`, after its generated venue `V<n>` block. The
  product Page carries no `### Writing Style`; one Requirement lens exposes
  both rule families for DRAFT, REVISE, and CHECK.

## 0.7.0 · 260901
- Section Pages use semantic IDs (`S-<desk>-Main-<section-name>` and `S-<desk>-Appendix-<section-name>`), with the Board Map governing order. Retained `S<D><NN>` / `SA<NN>` only for historical archive compatibility.

## 0.6.2 · 260831
- Runtime home tree letters per group: Ba-Main · Bb-Appendix · Bc-Round; later desk continues at Bd (JL 260831).

## 0.6.1 · 260831
- Runtime home tree shows the three desk groups (-Main/-Appendix/-Round, JL 260831).

## 0.6.0 — 2026-08-31

- **Renamed and moved** (JL 260831: "replace page-types to be workflow-phases"):
  `paper/page-types/haipipe-page-for-section/` is now `paper/workflow-phases/haipipe-paper-section/`.
  The skill is one paper JOURNEY PHASE and still owns its `page-type:` key;
  a new `## 🧭 Journey phase` block places the phase and its gates, and the
  description carries the P-number. Contract body unchanged.

## 0.5.5 — 2026-08-31

- **Appendix pages are `SA<NN>`, Section-Appendix** (JL 260831): the group
  token is `S<D> | SA`; `A<D>` retired, grandfathered where it still stands.

## 0.5.4 — 2026-08-31

- The outline mode is stated in the BODY (§🧱), not only in the frontmatter:
  a field desk found the Skill tool strips YAML frontmatter, so `mode:
  resolved` was invisible through the door (friction F4, SM01 field test).
  Also states: one `## C<n>` per Content division of the page (a flat section
  is `C1`), one bullet per sentence slot.

## 0.5.3 — 2026-08-31

- **A Section plan is a list of sentence slots** (JL 260831, approving SM00
  plan v3: "I love this outline style"): `S<n> · <what it does>` heads, groups
  by move, `C<n>:` tags on findings, a `Cut:` bullet, one-line Notes, no
  drafted prose in the plan; specimen quoted in `haipipe-plugin-outline` §✂️.

## 0.5.2 — 2026-08-31

- **`cli/resolve-structure.py` matches a division across desk numbering**:
  `KIND2TOK` is MISQ-numbered (`sec-3-methods`) and the JAMA IM desk numbers
  the same unit `Sec-2-Methods`, so every JAMA Section read MISSING. After the
  exact table hit, a UNIQUE `sec-<x>-<kind>` suffix hit is the same unit; two
  hits stay a gap. `("qbv6-jama-im", "conclusions")` is ABSENT BY DESIGN (JAMA
  IM folds Conclusions into Discussion; NA01 §5.6 allocates the page). The
  seven MedJournal Section pages are stamped (six EXACT, one ABSENT BY DESIGN);
  their `section-kind:` key was normalised to the law's `section_kind:`.

## 0.5.1 — 2026-08-30

- **`outline.source` is a real on-disk glob** (`paper/venue/bank/1-QBv-desks/
  QBv*/QBv*.md`), because `src/plan_shape.py` resolves it on disk and the 0.5.0
  prose sentence, like 0.2.0's and 0.4.0's, "resolved to nothing" on every
  Section (16 of 36 plan-checker failures on MISQ).
- **Two header keys, not one**: `structure-source:` is the bound QBv FILE (a
  path the checker can resolve) and `structure-division:` is the row inside it
  (`§8 Sec-4-Results`, `§7 Sec-3-Methods · shared with 1 sibling Page(s)`, or
  the fallback reason). `cli/resolve-structure.py --write` stamps both; run on
  MISQ it stamped 14 pages (SM00 fenced by a live session) and the plan checker
  went 36 → 2 failures, both on the fenced page.

## 0.5.0 — 2026-08-30

Found by running the contract against a real board (JL 260830: "it barely
doesn't work"). Every defect had one shape: the contract named a thing that
does not exist, and nothing checked.

- **The structure source was addressed by a name that exists nowhere.** 0.2.0
  and 0.3.0 pointed at "the QBv Venue Page's Unit Guidance division"; a
  `grep -rn "Unit Guidance"` over all 17 QBv pages returns ZERO hits. The real
  division id is `Sec-<n>-<Kind>`. Every Section therefore resolved to nothing
  and took the generic fallback, which is EXACTLY the failure 0.2.0 was written
  to fix (`section-page-template: 1` held zero files). The name changed; the
  bug did not. The contract now addresses the division with a GREP, not a
  remembered name, and requires the whole `QBv<n> §<n> Sec-<n>-<Kind>` address
  in `structure-source` so a re-read can prove it.
- **The division NUMBER is not stable and may not be used alone**: MISQ's
  abstract is §4, Nature Communications' is §3, PNAS §3 is Sec-0-Significance.
- **`section_kind` does not equal a `Sec-` token, and the mismatch has FOUR
  remedies, not one.** New table: EXACT resolves; SHARED (methods → one
  division serving two Pages, appendix → one serving six) resolves and SPLITS
  the budget on the Narrative row; ABSENT BY DESIGN takes the fallback and
  records a deviation on the Narrative; only MISSING raises a gap on the QBv
  page. The ABSENT BY DESIGN row is the one 0.4.0 lacked, and its absence told
  an agent to make the venue bank invent a division the desk does not have
  (MISQ publishes no related-work unit; a paper may still keep one because a
  person ruled it).
- **Eight of seventeen desks carry zero `Sec-` divisions**, so `mode: resolved`
  is aspirational there. The contract now names them instead of letting a page
  read as venue-resolved when it is not.
- **The skill spelled its own key two ways**: body `section_kind`, required
  block and `ref/generic-template.md` `section-kind`. Live pages use the
  underscore. One spelling now, and the kind list gains
  `literature-review` and `conclusion`, both in real use and both unlisted.
- **`cli/section-stats.py` restored.** Nine live Section Pages carry a
  `# --- form:begin (generated) ---` block naming it as their regenerator, and
  the file had been deleted with the stage-runtime purge (64de124b), so those
  blocks were frozen and unregenerable; `check.py` already reported six as
  stale. Recovered from `64de124b^` and verified: it reproduces SM08's own
  logged measurement (13 sentences, ~367 words) exactly. "This variant owns no
  scripts" is retired.
- `ref/generic-template.md` drops the `section-page-template: 1` header, the
  marker of the universe 0.2.0 declared dead.

Companion fix outside this skill: `haipipe-board/cli/pagestatus.py` counted
divisions with `^### \d+ · `, narrower than `check.py:1176`'s `§?[\d.]+`, so
every Section Page numbering its divisions by the MANUSCRIPT (`### §6.1 …`)
reported `§ 0`; and it counted only canonical `A<n>.<m>` Aims, not the LEGACY
checkbox form `src/common.py aim_progress` supports on purpose. On a 20-page
paper board that hid 45 divisions and 276 Aims.


## 0.4.0 — 2026-08-24

- **One B group per desk** (JL 260824, journey 0.5.0): main units, appendix
  units, and the desk's rounds share `B<x>-<desk>/`; split Ba1/Ba2 pair
  groups grandfathered. Tokens S<D>/A<D> unchanged.


## 0.3.0 — 2026-08-23

- **The 0.2.0 entry below had never reached the body** (found in the 260823
  family review: the frontmatter still said 0.1.1 and `outline.source` still
  pointed at the zero-file `section-page-template: 1` universe). The body now
  resolves structure from the QBv Venue Page's Unit Guidance division matching
  `section_kind`, through the governing Narrative's division-1 binding; the
  generic fallback is unchanged and a missing unit division is raised as a gap
  on the QBv page.
- **Runtime homes take the 260823 scaffold grammar**: main units as
  `S<D><NN>-<kind>` in the desk pair's `Ba1-…-main/` group, appendix units as
  `A<D><NN>-<slug>` in `Ba2-…-appendix/`; `1-SC-main/`, `2-SA-appendix/` and
  the `SC`/`SA` tokens are grandfathered.
- Frontmatter gains `last_updated`, `summary`, and the parametric
  `group-token: "S<D> | A<D>"`.

## 0.2.0 — 2026-08-21

- **Resolved source re-pointed at the QBv bank** (JL 260821): the declared
  universe `paper/venue/**/template.md` marked `section-page-template: 1` held
  ZERO files — every Section silently resolved to the generic fallback. The
  structure now comes from the QBv Venue Page's unit division matching
  `section_kind`, reached through the governing Narrative's division-1 binding
  (venue 0.3.0 made those divisions carry moves-as-slots, pack refusals,
  format values, and the language per desk unit).
- Raw pack `style.md` files stay informative and may never become
  `structure-source`; a missing unit division is raised as a gap on the QBv
  page, never filled locally.
- **Two runtime groups** (JL 260821: "we will have 1-SC-Section and
  2-SA-Appendix"): main reading order in `1-SC-main/` as `SC<NN>-<kind>`,
  appendices in `2-SA-appendix/` as `SA<NN>-<slug>`, one contract for both;
  Round moves to `3-RD-round/`.
- Frontmatter gains version, summary, and `group-token: SC | SA`.

## Unreleased — 2026-08-16

The outline this type supplies is RESOLVED, and it is now reachable in one step.

- Declares `outline: mode: resolved` and names the path:
  `paper/venue/playbook-<pack>/<venue>/<venue>-<kind>/template.md`, with a one-
  line `ls` that resolves it from the page's own two keys. Verified against five
  (venue × kind) pairs; 95 templates are on disk.
- Says what arrives: a fillable skeleton, not a description. The MISQ
  introduction hands over `### P1. Phenomenon hook`, `### P2. (optional) Deepen
  the stakes`, `### P3. What is known`, each with its paragraph budget and its
  named anti-pattern. DRAFT chooses the variant and the ¶ counts; it does not
  invent an arc.
- A `(venue × kind)` that resolves to nothing is a HOLE the venue pack owes, and
  copying a sibling section's shape is the failure this type exists to prevent.
- This type read as thinner than the others because its outline lived elsewhere.
  It is the RICHEST of the ten; only the path was missing.

haipipe-paper-section · Changelog
====================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match
SKILL.md frontmatter `version:`. Newest first.

**v0-series rule:** inherited from `haipipe-board`; this skill stays on `0.x.x` and
never reaches `1.0.0` without JL's explicit say-so.

## 0.1.1 - 2026-08-05

Review fixes:

- The venue-chain figure is no longer redrawn here; the section cites
  `-for-stage`'s "ONE stage reads the venue page" and adds only the unit
  grain, so the LOAD line's "restates none of that" is now true.
- Corrected: other stage pages carry a venue contract block too (S-Open-Pitch
  does); what no other stage page carries is one PER READER-ORDERED UNIT.
- The REQUIRED `page-type: section` frontmatter key is stated: the filename is
  letter for letter a stage filename (base type resolution ③).
- Plain English: "The kind is the one name that ties three things together:
  the venue division, the blueprint block, and the template."

## 0.1.0 - 2026-08-05

**Created on JL's 260805 admission** ("I want is also for-venue, for-meeting,
for-stage... and also for-section (connecting with for-venue)"), thought through
against the paper skill board and the MISQ paper board together.

- Reverses the for-main rejection with a reason, not a mood: for-main failed the
  host-agnostic name test (one family's region); for-section passes it (both the
  paper and application families run section-edit), and the `### Venue contract`
  block on the real `S-Main-3-theory` is a typed record no plain stage page has.
- Loads for-stage the way the topic types load the topic core: second-level
  variant, no restated chain rules.
