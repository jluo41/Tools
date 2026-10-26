# haipipe-display · Changelog

## [0.5.0] — 2026-10-26

Merged 5 helper skill(s) into `_parts/`: `haipipe-display-table` -> `_parts/table`, `haipipe-display-figure` -> `_parts/figure`, `haipipe-display-diagram` -> `_parts/diagram`, `haipipe-display-illustration` -> `_parts/illustration`, `haipipe-display-tex` -> `_parts/tex`. /haipipe-display reads `_parts/<name>/PART.md` instead of calling a separate skill; allowed-tools gained the parts' tools. Old commands map as `/haipipe-display-table` -> `/haipipe-display table`. (merge-parts 261026)

## 0.4.0 · 2026-10-22 · the display revise loop is a must (JL 261022)

- New `ref/display-revise-loop.md` (JL: "display should also have a loop, like the draft is a loop"): one question
  per display, one colour scheme, a folder name that says what it is, a blind review by a fresh agent (the brief is
  in the ref, ready to paste), `review/rNN.md` per round, revise and review again; pass = overall >= 8/10 and no
  dimension under 7; stop after 4 rounds and hand the person what is open.
- `ref/display-unit-output-contract.md`: README needs `question:` and `review:`; a unit keeps `review/`;
  `accepted:` only after a passing round; displays are in colour from one scheme (and still read in grayscale).
- SKILL.md: § Revise loop (a must); triggers display review, display loop, revise the figures, blind review of
  displays, /haipipe-paper-display.
- § Where the unit lands: in a paper the unit frames a picture drawn by a Run of the paper's work Block (its
  `jNN_paper_displays` Job); the loop sends a picture fix to that Run's script, a caption fix to the unit.
- The loop ref, after a fresh-agent test: the caption title is short and is followed by the question (it need not be
  the answer); stop before round 4 only when every open problem needs what the maker may not change.

## 0.3.8 · 2026-10-20 · built_on names VALUE cards

- haipipe-evidence 0.6.0: a unit's `built_on:` names CITE and VALUE cards (VALUE was WORK); a draft Task shows its units in 4 · Display.

## 0.3.7 · 2026-10-16 · display/ beside draft/ and evidence/ (JL 261016)

- § Where the unit lands: a draft Task's units go to `<task>/display/Display<n>-<slug>/`, and each names the
  `built_on:` cards it reads from `<task>/evidence/cards.yaml` through haipipe-evidence.

## 0.3.6 · 2026-09-28 · No content hashes (JL 260928)

- AGENTS.md rule 9: `ref/display-intake-contract.md`, `ref/intake-manifest.template.yaml` and `ref/display-unit-output-contract.md` drop `origin.sha256` and `snapshot.sha256`; `snapshot.materialized_at` is required, and a local canonical artifact newer than it means the snapshot is stale.

## 0.3.5 · 2026-09-08
- Third naming pass (JL 260908): under a Paper Section page the unit is `Display<n>-<slug>`; the page id carries the index. Same in ref/display-unit-output-contract.md and ref/display-intake-contract.md.

## 0.3.4 · 2026-09-08
- Paper Section pages name a display unit `Sec<N>-Display<n>-<slug>` / `App<L>-Display<n>-<slug>` from the page H1 (JL 260908); `S-Display-*` retired. Stated in SKILL "Where the unit lands", ref/display-unit-output-contract.md, ref/display-intake-contract.md.

## 0.3.2 — 2026-09-04

- Make the Board Page numeric exception explicit in the shared Intake and
  output contracts: display-input Task → page-service `values.yaml` →
  Evidence Local Input → Page display Intake.

## 0.3.0 — 2026-08-16

- **0.2.0 and 0.3.0 shipped in SKILL.md with no entry here.** Reconstructed from
  the frontmatter rather than re-authored: the ✒️ tex kind gained its own skill,
  so the door now routes FIVE renderers — 📊 table · 📈 figure · 📐 diagram ·
  ✒️ tex · 🎨 illustration — and names none of them as unowned. Recorded 260822
  in a version-vs-changelog sweep across the toolkit.

## 0.1.0 · 2026-08-16
- Born in the consolidation round (JL 260816: "我们是不是只保留一个 … 没必要搞那么多"): the family gains its one door, routing by kind per QPf5 §3's taxonomy.
- `haipipe-display table` and `haipipe-display figure` retire as skills; their full rule sets live on as this door's `ref/table.md` and `ref/figure.md`, and their folders are parked under `_todo/`.
- The four specialists with real machinery stay: diagram, illustration, poster, slides.

## 0.2.0 · 2026-08-16
- Reversed the fold, kept the door (JL 260816: "figure 和 table 是不是也可以保留呢?"): `haipipe-display table` and `haipipe-display figure` return as full skills and the door's `ref/` recipes are gone; the door is now a pure router.
- `haipipe-display-poster` and `haipipe-display-slides` retired (JL: "poster 和 slides 我们都不要了"), with their paper-side doors `paper-poster`/`paper-slides` and the `content-plan-spec.md` they alone used; all parked under `_todo/`.
- Four renderers remain: table · figure · diagram · illustration. The ✒️ tikz method is named in the routing table as hand-authored, since no skill covers it.

## 0.3.0 · 2026-08-16
- The ✒️ row stopped being skill-less: `haipipe-display tex` was born the same day (JL), so the door now routes FIVE renderers and names none as unowned. The 0.2.0 note above is superseded on that one point.
