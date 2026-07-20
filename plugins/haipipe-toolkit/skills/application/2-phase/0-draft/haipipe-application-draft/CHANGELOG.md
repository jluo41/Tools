haipipe-application-draft — Changelog
================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## 1.5.0 — 2026-07-19 — self-review, the constitution pointer, and a top-level gate

From `_console/closed/260719-01-DRAFT-RAISE-QUESTIONS.md` findings A1 A2 A3 A6 A7 · B3 B7 · C2 C5 C6 (JL: "现在我们以paper为主，然后apply到application上去" — paper landed first; this is the port).

**A1 + A2 — there was no pre-gate SELF-REVIEW, and no tool to run one with.** `probe`'s DRAFT rule 4 requires a fresh-context reviewer for BOTH families; a grep of all of `application/2-phase/` returned zero. The flow jumped `4. RAISE+PLAN` → `5. PRESENT` → STOP, so the first eyes on the draft were the human's. Worse, `allowed-tools` had no `Agent`, so the rule was not merely unimplemented — it was unimplementable. New `Step 4b` mirrors the paper twin (Surface A vs the artifact spec + a COMPLETENESS check, Surface B verbatim from `probe`'s checklist, bounded at 2 rounds, residual surfaced not hidden), and `Agent` is declared.

**A3 — the file never named the document that governs it.** One bare allusion to "the constitution's PHASE MAP", no path, no precedence rule. A reader could not find `probe`, and would not know it wins on conflict. Added the Rules block.

**A6 — the gate presented only half of what it exists to review.** `5. PRESENT` listed the raised questions and stopped: no draft presentation, no `> USER:` / `> CC:` protocol, no iterate loop, no confirm/hand-off. (The paper twin had the mirror-image hole — it presented only the draft.) PRESENT now carries draft + plan + self-review verdict, and a step 6 CONFIRM records the `[GATE] draft-review: approved` line quoting the user.

**A7** — the `→ 1-probes/PP<NN> · QX<n>` backlink into the stage-doc `Q-<Stage>-<n>` was never required (zero hits for it in the file), so a stage doc could not say where its own answer would come from · **B3** — RAISE+PLAN now opens by READING the calling stage's `Questions this stage typically raises`, instead of waiting to notice a gap · **B7** — the entry contract (route/bank/target) was stated only inside `## DRAFT may search`, conditioned on "when the search reveals something"; the normative half moved to step 4 and the search section keeps a pointer · **C2** — the Template registry's bare `1-lifecycle/…` paths do not resolve from this skill's folder; prefixed · **C5** — CHANGELOG claimed "Newest first" while 1.2.0 and 1.3.0 sat below 1.0.0; re-sorted · **C6** — the section-edit Template cell pointed at "per-section scaffolds in that skill", a folder holding only SKILL.md + CHANGELOG.md.

## [1.4.0] — 2026-07-19

- Owner ruling, 2026-07-19 (JL): "宪法 don't use this name, just use `probe`." The nickname
  "THE CONSTITUTION" / "the constitution" for `probe/haipipe-probe/SKILL.md` is dropped everywhere;
  each site now names either `probe` or the actual path.
  Touched: the RAISED QUESTIONS + THEIR PLAN step, which cited "the constitution's PHASE MAP".

## [1.3.1] — 2026-07-19

- Probe constitution v9.5.0 sync (Q-executor-entry probe-file format), mirroring the paper family. RAISE becomes RAISE+PLAN: DRAFT authors the WHOLE probe plan (①ORGANIZE + ②MATCH) — a `Q-<Stage>-<n>` in the stage doc's Q-consumer plus a `## QX<n>` ENTRY carrying `### q-executor` (+ Deliverable/Accepted), a `### q-consumer` bullet, and `### bank binding` (route · bank · target) — instead of a bare `state: planned` section with an empty `target:`.
- FORBIDDEN narrows to writing `### a-executor` (the ANSWER, PROBE's ⑤ harvest); DRAFT now legitimately writes `target:`, so the DRAFT/PROBE line is `### a-executor` / `state` (planned or answered, never read), not an empty target.
- Updated: frontmatter summary, "What DRAFT means" steps 4–5, "DRAFT may search; PROBE must dispatch", return contract (`next:` = PROBE runs ③DISPATCH → ④POINT → ⑤INTERPRET).
- Archaeology strip: ruling citations and dates removed from the normative text.

## [1.3.0] — 2026-07-09

- RELEASE MENU (JL bench ruling: "at the end of each draft, it should let me know what probes to release as well"): DRAFT gains step 5 PRESENT — the phase reply ends by listing every buffered planned card (PP id — question — mode — route — fills/settles) and stops for the user's release picks. Return contract gains the `probes:` line. Pairs with the probe worker's STEP 1.5 RELEASE GATE (2.1.0), which remains the backstop for DRAFT-skipping paths.

## [1.2.0] — 2026-07-09

- Template registry added (ladder restage follow-up, JL: stage skills had "no ref/ no template"): WRITE now reads the calling stage's canonical `ref/<stage>-template.md` alongside its SKILL.md artifact spec — 10-row registry table covering seed, the 1a-1d rungs, venue, pitch, narrative, display, section-edit. This worker carries no templates of its own (paper draft parity). The 9 template files live with their stage skills.

## [1.1.0] — 2026-07-07

- Port of paper draft 3.4.0/3.5.0 (paper-alignment round 2, SOP §4 row 6, R3): allowed-tools gains WebSearch, WebFetch; new "DRAFT may search; PROBE must dispatch" section -- inline search is DRAFT-only orientation fuel with two legal destinations (stage-doc prose; buffered `status: planned` PPNN skeletons), never refs/findings into cards; real evidence lands only via haipipe-application-probe; the line is card state, mechanically enforced by check-probe-cards.sh at VERIFY/CHECK.

## [1.0.0] — 2026-07-06

- NEW phase worker (paper-alignment refactor, SOP archived in haipipe-application/CHANGELOG.md §5.0.0; full-DPRC ruling R4).

