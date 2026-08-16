# haipipe-application-draft · v0.1.5
state: 🔴 OPEN
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Opening
haipipe-application-draft is a shipped unit: what does it still owe, and is it healthy?

Write here what this unit is for in one paragraph a stranger could follow, why it exists on its own rather than as part of its neighbour, and what would have to be true for it to be considered finished.
The generated sections answer what it IS; only this one can answer whether it is any good.
`Opening` is the lead section's ONE name on every page kind (JL 260731: "just one single Opening"); `Question` survives only as a legacy alias for pages written before the rename.

## Writing Style
English only. One sentence per source line. Describe the shipped unit factually and keep generated inventory separate from human health judgment.

## Diagram
<!-- haipipe:skill:tree:start 815d49f5139df7a3 application/2-phase/0-draft/haipipe-application-draft -->

```
haipipe-application-draft/
  CHANGELOG.md          52 ln  haipipe-application-draft — Changelog
  SKILL.md             147 ln  Skill: haipipe-application-draft (internal phase worker)
```

<!-- haipipe:skill:tree:end -->

```
WORKFLOW  (authored: a folder can be read off disk, an intent cannot)
Draw how this skill is actually used: the entry point, what it reads,
what it writes, and where it hands off. Delete this fence if the tree
above is the whole story.
```

## Content
<!-- haipipe:skill:body:start 815d49f5139df7a3 application/2-phase/0-draft/haipipe-application-draft -->

**haipipe-application-draft** · `0.1.5` · last shipped 2026-07-19

- folder   `application/2-phase/0-draft/haipipe-application-draft/`
- tools    Bash, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent
- summary  DRAFT phase worker (internal): settle the stage doc's structure + sentences with the user (illuminate → elicit → write per the stage's template), and RAISE what the draft cannot answer as `## QX<n>` question ENTRIES in 1-probes/ AND author their probe plan (`### q-executor` + route + bank + target — PROBE runs the loop's ①ORGANIZE + ②MATCH); never writes an answer (`### a-executor`). Inline WebSearch is drafting fuel only, never durable evidence. The calling stage supplies the artifact spec + template; this worker carries neither. History: ./CHANGELOG.md.

### SKILL.md



Skill: haipipe-application-draft (internal phase worker)
=========================================================

DRAFT phase worker. Every stage skill calls this first. The calling stage passes its artifact spec (files, content structure, done-criteria); this worker turns intent into a settled stage doc.


- 1 · Rules (follow these — the model is haipipe-probe's)
      The DRAFT-phase rules live in `../../../../probe/haipipe-probe/SKILL.md` → **Phase rules · DRAFT phase** + **The DRAFT self-review checklist**. Follow those; on conflict, that file wins. Application-specific additions are the steps below.

- 2 · What DRAFT means
      ```
      1. ILLUMINATE   read what already exists (stage doc, upstream stage docs,
                      STATUS.md venue/audience when the stage is venue-ALIGNED);
                      surface the taste-bearing choices instead of guessing
      2. ELICIT       ask the user the few choices that shape the doc (framing,
                      emphasis, scope); mechanical structure is autonomous
      3. WRITE        the stage artifact per the calling stage's spec:
                      0-lifecycle/<N-stage>/<N-stage>.md + a [DRAFT] entry in _LOG
      4. RAISE+PLAN   FIND the questions first: read the calling stage's
                      **Questions this stage typically raises** and walk the draft
                      against it. Then every spot where the draft needs evidence it
                      does not have becomes a QUESTION -- a `Q-<Stage>-<n>` in the stage doc's
                      Q-consumer AND a `## QX<n>` ENTRY in the right topic's probe file
                      (1-probes/PPNN_<topic>/) -- then write the
                      `→ 1-probes/PP<NN> · QX<n>` pointer BACK into that
                      `Q-<Stage>-<n>`, so the stage doc says where its answer will
                      come from. Per
                      ../../../haipipe-application/fn/probes.md. DRAFT runs the loop's
                      ①ORGANIZE + ②MATCH: write `### q-executor` (general language,
                      stake stripped, + Deliverable/Accepted) + a `### q-consumer`
                      bullet + `### bank binding` (route · bank · target — an existing
                      path or `NEW <path>`). NEVER write `### a-executor` (the answer).
      4b. SELF-REVIEW a fresh-context sub-agent checks the draft + the probe plan
                      before the human sees either (creator/reviewer split — the drafter
                      does not grade its own work). Report-only; the drafter fixes.
                      Bounded at 2 rounds; a 3rd-round residual is SURFACED at the gate,
                      never hidden. See **Step 4b** below.
      5. PRESENT      ⛔ STOP and end the turn, presenting all THREE things the one
                      merged gate exists to review:
                        (a) the DRAFT -- structure + where the placeholders are;
                        (b) the PROBE PLAN -- one line per question:
                            PP id -- question -- route -- bank -- what it fills/settles;
                        (c) the SELF-REVIEW VERDICT, incl. any residual.
                      No open questions -> say "questions raised: none".
                      The user reviews structure AND plan and adds `> USER:` comments;
                      reply `> CC:` underneath each, never deleting or rewording one.
                      Iterate until the user advances -- their verb/"go" is the gate.
      6. CONFIRM      on approval: move resolved threads to `_LOG`, write the phase
                      summary + a `[GATE] draft-review: approved` line quoting the user,
                      mark draft ✅, hand off to PROBE.
      ```

- 3 · Step 4b. 🤖 SELF-REVIEW — check the draft + probe plan before the gate
      ```text
      Agent(general-purpose, prompt="
        Review this DRAFT phase output against the checklist. Report PASS or a numbered issue list
        (file + line + what's wrong + the fix). Do NOT edit anything — only report.

        READ:
          - the stage draft (the stage doc this run wrote/updated)
          - the probe plan (the 1-probes/PPNN_*.md files touched this run)
          - the calling stage's artifact spec, and probe's 'The DRAFT self-review checklist' at
            Tools/plugins/haipipe-toolkit/skills/probe/haipipe-probe/SKILL.md (repo-root-relative —
            you resolve from the repo root, not from the calling skill's folder)

        Surface A — the draft, vs the stage's artifact spec:
          - every section filled with REAL content (no unmarked placeholders)
          - one physical line per paragraph/bullet
          - every Q-<Stage>-<n> is cited inline [Q-<Stage>-<n>] on the sentence it hangs on
          - COMPLETENESS, the reverse direction: every unbacked statement is either owned by a
            Q-<Stage>-<n> or explicitly declined in _LOG. An unowned hole is a defect — nobody
            owns it, so nobody will ever fill it.

        Surface B — the probe plan (run probe's 'DRAFT self-review checklist' verbatim):
          LAW-2-clean q-executor · answerable+specific · route set · bank ROOTED to a specific folder
          (candidate READ + judged on the answer) · target agrees with bank · each ### q-consumer bullet
          copies a real stage-doc Q-consumer id · no stake leaked into a q-executor
      ")
      ```
      Issues → FIX them, then re-run (bounded: at most 2 rounds). The self-review PRECEDES the human gate; it never replaces it.
      DRAFT settles WHAT the doc says. It does NOT collect evidence (PROBE), polish prose (REVISE), or approve anything (CHECK).

- 4 · Template registry (WRITE reads the stage's canonical template)
      At WRITE, read TWO things from `../../../1-lifecycle/`: the calling stage's SKILL.md artifact spec (WHAT to produce, done-criteria) and its canonical template (section order, placeholders, formatting). This worker carries NO templates of its own -- the stage owns its format.
      | Stage | Artifact spec | Template |
      |---|---|---|
      | seed | `../../../1-lifecycle/0-seed/haipipe-application-seed/SKILL.md` | `ref/seed-template.md` |
      | descriptions | `../../../1-lifecycle/1a-descriptions/haipipe-application-descriptions/SKILL.md` | `ref/descriptions-template.md` |
      | themes | `../../../1-lifecycle/1b-themes/haipipe-application-themes/SKILL.md` | `ref/themes-template.md` |
      | claims | `../../../1-lifecycle/1c-claims/haipipe-application-claims/SKILL.md` | `ref/claims-template.md` |
      | advice | `../../../1-lifecycle/1d-advice/haipipe-application-advice/SKILL.md` | `ref/advice-template.md` |
      | venue | `../../../1-lifecycle/haipipe-application-venue/SKILL.md` | `ref/venue-template.md` |
      | pitch | `../../../1-lifecycle/2-pitch/haipipe-application-pitch/SKILL.md` | `ref/pitch-template.md` |
      | narrative | `../../../1-lifecycle/3-narrative/haipipe-application-narrative/SKILL.md` | `ref/narrative-template.md` |
      | display | `../../../1-lifecycle/4-display/haipipe-application-display/SKILL.md` | `ref/display-template.md` |
      | section name | `../../../1-lifecycle/5-section-edit/haipipe-application-section-edit/SKILL.md` | per-section scaffolds in that skill |
      (Template paths are relative to each stage skill's OWN folder, e.g. `../../../1-lifecycle/1a-descriptions/haipipe-application-descriptions/ref/descriptions-template.md`. Artifact formatting is uniform: `=====` title / `-----` sections / `**bold**` sub-items, one sentence per line, no `#` headings.)

- 5 · Boundaries
      - Venue-FREE stages (seed + the 1a-1d ladder: descriptions, themes, claims, advice): do not read venue packs; the doc must survive retargeting.
      - Venue-ALIGNED stages (pitch, narrative, display, section-edit): read `venue/venue-<name>` for structure and tone expectations (the pack carries tone-by-audience).
      - Never invent evidence: an unbacked statement is written as a raised question, not asserted.
      - Stage docs are markdown, one physical line per paragraph/bullet.

- 6 · DRAFT may search; PROBE must dispatch
      Inline WebSearch/WebFetch is ALLOWED in DRAFT -- as drafting fuel, NOT as evidence.
      DRAFT may search the web to orient (is this intervention space crowded? what response rates do comparable programs report? what are the channel's framing norms?) and to sharpen the stage doc. What that search produces has exactly two legal destinations:
      1. **PROSE** in the stage doc (Opportunity, Mechanism hypothesis, beat text, ...) -- phrased as orientation, never as settled fact; anything load-bearing stays a raised question.
      2. **A RAISED QUESTION** -- a gap the search reveals goes through step 4 RAISE+PLAN like any other question, with no special status. The entry contract lives there, not here.
      FORBIDDEN in DRAFT: writing an `### a-executor` (the ANSWER -- that is PROBE's ⑤ harvest), or treating an inline result as landed evidence. Real evidence lands ONLY via the PROBE phase dispatching `haipipe-application-probe` (the single door); inline search results bind to nothing -- evidence gathered any other way means "the PROBE phase did not happen."
      The line is no longer an empty `target:` (DRAFT now writes the `target:` plan) -- it is `### a-executor` / `state`: DRAFT leaves an entry at `planned` (a `NEW` target awaiting dispatch) or `answered` (an existing target already answered, awaiting harvest), never `read`; only PROBE's harvest writes `### a-executor` and reaches `read`. `check-probe-cards.sh` enforces this at the probe worker's VERIFY step and again at the CHECK gate -- a `planned` entry blocks green, so DRAFT search can never masquerade as evidence.

- 7 · Return contract
      ```
      status:    ok | blocked
      stage:     <stage-name>
      artifact:  <path written>
      needs:     <count of questions raised for PROBE>
      probes:    <each raised question: PPNN -- question -- route -- bank -- fills/settles; or "none">
      next:      PROBE (runs the approved entries forward: ③DISPATCH → ④POINT → ⑤INTERPRET)
      ```
<!-- haipipe:skill:body:end -->

## Aims
### P · Page-level health ruling
- P1 · Rule this skill's health.
  **Done when:** `state:` records a human judgment: stable, in flux, needs work, or parked.

## States
### P · Page-level health ruling
- ⬜ P1 · Page generated 260802 1200; nothing ruled yet.

## Log
260802 1200 · page generated from `application/2-phase/0-draft/haipipe-application-draft/` by `skillpage.py new`

<!-- haipipe:skill:log:start 815d49f5139df7a3 application/2-phase/0-draft/haipipe-application-draft -->

Converted from the skill's own `CHANGELOG.md`: 8 releases.

260724 · `0.1.5`
      Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.5.0; older entries below keep their original numbers).
260719 · `1.5.0` · self-review, the constitution pointer, and a top-level gate
      From `_console/closed/260719-01-DRAFT-RAISE-QUESTIONS.md` findings A1 A2 A3 A6 A7 · B3 B7 · C2 C5 C6 (JL: "现在我们以paper为主，然后apply到application上去" — paper landed first; this is the port).
      **A1 + A2 — there was no pre-gate SELF-REVIEW, and no tool to run one with.** `probe`'s DRAFT rule 4 requires a fresh-context reviewer for BOTH families; a grep of all of `application/2-phase/` returned zero. The flow jumped `4. RAISE+PLAN` → `5. PRESENT` → STOP, so the first eyes on the draft were the human's. Worse, `allowed-tools` had no `Agent`, so the rule was not merely unimplemented — it was unimplementable. New `Step 4b` mirrors the paper twin (Surface A vs the artifact spec + a COMPLETENESS check, Surface B verbatim from `probe`'s checklist, bounded at 2 rounds, residual surfaced not hidden), and `Agent` is declared.
      **A3 — the file never named the document that governs it.** One bare allusion to "the constitution's PHASE MAP", no path, no precedence rule. A reader could not find `probe`, and would not know it wins on conflict. Added the Rules block.
      **A6 — the gate presented only half of what it exists to review.** `5. PRESENT` listed the raised questions and stopped: no draft presentation, no `> USER:` / `> CC:` protocol, no iterate loop, no confirm/hand-off. (The paper twin had the mirror-image hole — it presented only the draft.) PRESENT now carries draft + plan + self-review verdict, and a step 6 CONFIRM records the `[GATE] draft-review: approved` line quoting the user.
      **A7** — the `→ 1-probes/PP<NN> · QX<n>` backlink into the stage-doc `Q-<Stage>-<n>` was never required (zero hits for it in the file), so a stage doc could not say where its own answer would come from · **B3** — RAISE+PLAN now opens by READING the calling stage's `Questions this stage typically raises`, instead of waiting to notice a gap · **B7** — the entry contract (route/bank/target) was stated only inside `## DRAFT may search`, conditioned on "when the search reveals something"; the normative half moved to step 4 and the search section keeps a pointer · **C2** — the Template registry's bare `1-lifecycle/…` paths do not resolve from this skill's folder; prefixed · **C5** — CHANGELOG claimed "Newest first" while 1.2.0 and 1.3.0 sat below 1.0.0; re-sorted · **C6** — the section-edit Template cell pointed at "per-section scaffolds in that skill", a folder holding only SKILL.md + CHANGELOG.md.
260719 · `1.4.0`
      - Owner ruling, 2026-07-19 (JL): "宪法 don't use this name, just use `probe`." The nickname
        "THE CONSTITUTION" / "the constitution" for `probe/haipipe-probe/SKILL.md` is dropped everywhere;
        each site now names either `probe` or the actual path.
        Touched: the RAISED QUESTIONS + THEIR PLAN step, which cited "the constitution's PHASE MAP".
260719 · `1.3.1`
      - Probe constitution v9.5.0 sync (Q-executor-entry probe-file format), mirroring the paper family. RAISE becomes RAISE+PLAN: DRAFT authors the WHOLE probe plan (①ORGANIZE + ②MATCH) — a `Q-<Stage>-<n>` in the stage doc's Q-consumer plus a `## QX<n>` ENTRY carrying `### q-executor` (+ Deliverable/Accepted), a `### q-consumer` bullet, and `### bank binding` (route · bank · target) — instead of a bare `state: planned` section with an empty `target:`.
      - FORBIDDEN narrows to writing `### a-executor` (the ANSWER, PROBE's ⑤ harvest); DRAFT now legitimately writes `target:`, so the DRAFT/PROBE line is `### a-executor` / `state` (planned or answered, never read), not an empty target.
      - Updated: frontmatter summary, "What DRAFT means" steps 4–5, "DRAFT may search; PROBE must dispatch", return contract (`next:` = PROBE runs ③DISPATCH → ④POINT → ⑤INTERPRET).
      - Archaeology strip: ruling citations and dates removed from the normative text.
260709 · `1.3.0`
      - RELEASE MENU (JL bench ruling: "at the end of each draft, it should let me know what probes to release as well"): DRAFT gains step 5 PRESENT — the phase reply ends by listing every buffered planned card (PP id — question — mode — route — fills/settles) and stops for the user's release picks. Return contract gains the `probes:` line. Pairs with the probe worker's STEP 1.5 RELEASE GATE (2.1.0), which remains the backstop for DRAFT-skipping paths.
260709 · `1.2.0`
      - Template registry added (ladder restage follow-up, JL: stage skills had "no ref/ no template"): WRITE now reads the calling stage's canonical `ref/<stage>-template.md` alongside its SKILL.md artifact spec — 10-row registry table covering seed, the 1a-1d rungs, venue, pitch, narrative, display, section-edit. This worker carries no templates of its own (paper draft parity). The 9 template files live with their stage skills.
260707 · `1.1.0`
      - Port of paper draft 3.4.0/3.5.0 (paper-alignment round 2, SOP §4 row 6, R3): allowed-tools gains WebSearch, WebFetch; new "DRAFT may search; PROBE must dispatch" section -- inline search is DRAFT-only orientation fuel with two legal destinations (stage-doc prose; buffered `status: planned` PPNN skeletons), never refs/findings into cards; real evidence lands only via haipipe-application-probe; the line is card state, mechanically enforced by check-probe-cards.sh at VERIFY/CHECK.
260706 · `1.0.0`
      - NEW phase worker (paper-alignment refactor, SOP archived in haipipe-application/CHANGELOG.md §5.0.0; full-DPRC ruling R4).

<!-- haipipe:skill:log:end -->
