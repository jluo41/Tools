# Paper Skill Handoff — 2026-07-18

A skill-dev session established a **stage-template charter** for the paper lifecycle and rolled the first **5 of 9** stages under it, plus **Option A**: lettered the paper-output folders (`1a/1b/2a/2b`) across the skills AND migrated 2 live manuscripts. Committed + pushed to `main` (`9be568f7`). This doc maps the remaining 4 stages and the conventions every future stage must follow. Design partner: JL, live co-design throughout.

## Where things stand

- Branch: **`main`** only (local + `origin`; the stale `wip/display-3.5x-unpushed` was deleted — v3.5.1, superseded by main's display v4.1.1 — and `origin/stata-specialists` pruned).
- This session = one commit: **`9be568f7`** "paper: stage-template charter (C1-C6) + Q-<Stage>-<n> ids + Option A paper-output lettering" — 82 files, scoped to `skills/paper/` only.
- **The charter hub is `1-lifecycle/TEMPLATES.md`** — the single source of truth for stage-template design. **Read it first.**
- **5 of 9 stages rolled**: seed · resource · claims · venue · pitch. Remaining: **narrative · display · section-edit · review**.

## The charter — what EVERY stage template must obey (`1-lifecycle/TEMPLATES.md`)

| # | Rule |
|---|---|
| C1 | Fill-rules live INLINE in `ref/<stage>-template.md` as `<!-- RULE: … -->` comments — follow then DELETE (never ship in the filled doc). The template is the single source of BOTH skeleton and rules; the SKILL never restates fill-rules. No wiki. |
| C2 | UNIFORM `Q-consumer` section, every stage: `## Q-<Stage>-<n> · <title>` + `Description` / `Reason` / `Answer` — the SAME fields everywhere (the PROBE stage collects every stage's questions through one pipeline). Stage-specific discipline → RULE guidance, not different fields. Every question ANSWERABLE + SPECIFIC (a concrete check, never "is it good?"). |
| C3 | Question ids are `Q-<Stage>-<n>` (Q-Seed-1, Q-Resource-1, Q-Claim-1, Q-Venue-1, Q-Pitch-1, …). Leading `Q-` = one greppable namespace AND disambiguates from content ids (`Resource 1`, `C1`). |
| C4 | A question is CITED inline in the sentence it hangs on: `[Q-<Stage>-1]` (forward link); `Reason` names the anchor(s) (back link). M:N allowed — a claim lists many questions; a question may serve many claims. |
| C5 | DPRC loop: DRAFT drops `[Q-…]` in → PROBE fills `Answer` (evidence, stops there) → REVISE weaves the answer into every citing sentence AND discharges the bracket. Born from content, dies into content. |
| C6 | Each SKILL states its ONE core question (seed "why might this paper exist?"; resource "does it EXIST + CARRY the claim?"; claims "what do we claim + is it supported?"; venue "which venue + what does it require of the final paper?"; pitch "why would the editor send it out for review?"). |

Also binding: **no pipe tables in filled stage docs** (use record lines); **prose-craft (readability) is a SEPARATE `ref/<stage>-readability.md`** for prose-heavy stages only (pitch has one), pointing to the shared REVISE-phase refs — never merged into the template.

## What changed this session (by area)

| Area | Change |
|---|---|
| **charter** | new `1-lifecycle/TEMPLATES.md` (C1–C6 + prefix table + live adoption matrix + per-stage notes). Retired the interim template-skill-split doc (JL: rules live in templates, not a wiki). |
| **seed** (v4.2.0) | template → `<!-- RULE -->` comments; `Probes` → `Q-consumer` (`## Q-Seed-<n>`); NEW `Landscape` section (seed-only); inline `[Q-Seed-1]` citation; PROBE-vs-REVISE loop boundary clarified. |
| **resource** (v2.3.0) | **description-first reframe**: `Demand` (N-per-hypothesis) → `Resource Description` (`## Resource <n>` + `### topics` + `### Serves & carries`); existence/fitness/**KILLS** discipline kept as RULE; CGM worked-example cut. |
| **claims** (v5.2.0) | uniform `## Q-Claim-<n>`; **M:N** claim↔question; **answerable+specific** rule (decompose a claim into small typed questions — fit/eval/robustness/placebo); **`Evidence Campaign` section DELETED** (redundant); each claim's `Evidence: [Q-Claim-1 …]` lists its questions; status aggregates. |
| **venue** (v3.4.0) | **resource-shaped**: 6 blocks → `Venue Decision` · `Relevant Files` (new) · `Requirements` (Structural Blueprint + Writing Principles) · `Q-consumer`; Fit Assessment **pipe table → record lines**; unwrapped the old ```text fence + `#` header. |
| **pitch** (v4.4.0) | markdown-`##` style → sibling `=====`/`-----`; added `## Q-Pitch-<n>` Q-consumer; **H→RQ pipe table → record lines**; venue-doc reads repointed to the reshaped venue (Venue Decision / Requirements). |
| **id format** | `<Stage>-Q<n>` → **`Q-<Stage>-<n>`** swept across all done stages + hub (~80 ids). |
| **Option A — paper-output lettering** | `0-lifecycle/{1-resource,1-claims,2-venue,2-pitch}` → `{1a-resource,1b-claims,2a-venue,2b-pitch}` (fixes the venue<pitch / claims<resource sort order). Swept ~60 skill files incl. `.sh` scripts (`check-probe-cards.sh`). |
| **venue+pitch skill FOLDERS** | `1-lifecycle/haipipe-paper-venue` → `1-lifecycle/2a-venue/haipipe-paper-venue` (fixed a real folder-DEPTH inconsistency — venue was one level shallow; `../../venue` → `../../../venue`); `2-pitch/` → `2b-pitch/`. Symlinks re-pointed. |
| **manuscripts migrated** | `Paper-Personality2Opioid-MISQ2026` (1-claims/2-venue/2-pitch → 1b/2a/2b) + `Paper-PhyPatSim` (1-claims → 1b): git mv folders + inner files + content refs. **Uncommitted in their own repos.** |

## Verified vs NOT verified

**Verified (static):** commit scoped to `skills/paper/` only (0 unrelated files bundled); 0 stale paper-output refs across skills + the 2 papers; `check-probe-cards.sh` reads `1a-resource`; venue's `../../../venue` resolves to the same (absent-in-this-checkout) `venue/` pack dir it always did; the LaTeX compile does NOT read `0-lifecycle/` (folder renames can't break compilation); skill descriptions + symlinks reflect the new paths.

**NOT verified (needs a real run):** no paper was DRAFTED through any reshaped template; the reshaped resource/claims/venue/pitch templates were never filled end-to-end; the DPRC citation loop (`[Q-…]` → PROBE → REVISE discharge) is unexercised.

## How to continue

1. **Roll the remaining 4 stages** under the charter, in order:
   - **narrative** — prose-heavy; also give it a `ref/narrative-readability.md` (craft only).
   - **display** — already has a Q-consumer; check for a pipe table to convert.
   - **section-edit** — rename its "Questions Raised" → `Q-consumer`. **OPEN DECISION**: per-section id scoping — `Q-Section-<n>` vs a `<Section>`-scoped id (a section stage runs per-section).
   - **review** — no template exists yet; create one under the charter (or decide it's template-free).
2. **pitch-readability decision** (JL, 2026-07-18): keep `pitch-readability.md` SEPARATE (prose-craft, not fill-rules); fix its stale `1-pitch.tex` ref; trim the rules that duplicate the REVISE-phase refs (`revise-content/ref/write-principles.md`, `revise-humanizer/ref/pattern-catalog.md`) → point instead. Add a charter line: prose-heavy stages MAY carry `ref/<stage>-readability.md`.
3. **Commit the 2 manuscript repos** (SELECTIVE staging — each carries pre-existing uncommitted edits, so NOT `add -A`) + **bump the parent `Physician-SPACE` submodule pointers** (Tools → `9be568f7`, plus the 2 migrated paper submodules).

## Deferred / out of scope

- **Manuscript-repo commits + parent pointer bumps** — continue #3 (the papers + tooling are already consistent on disk; this is housekeeping).
- **Prior 2026-07-17 delivery-side handoff items are STILL OPEN** (a different half of the family, untouched this session) — see below.

## Prior session — delivery side (2026-07-17), still open

The previous handoff (in git history, `9be568f7^`) reorganized the DELIVERY side (`3-deliver`, new `haipipe-paper-deliver` umbrella, `EVALUATION.md`, ~1000-line bloat trim) — all **committed but NOT run end-to-end**. Still open there: drive one paper through delivery (scaffold→conform→audit→polish→ship); `haipipe-paper-polish` (the merged 3-pass skill) never executed; `paper-poster` residual (~450 lines to rewrite, not just extract); and the **paper F2 bug** — `haipipe-paper-check` still asserts "DRAFT runs fully automatic", contradicting both DRAFT workers + the constitution.
