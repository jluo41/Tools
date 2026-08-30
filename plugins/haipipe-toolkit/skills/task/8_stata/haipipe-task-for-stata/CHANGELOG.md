haipipe-task-for-stata — Changelog
==================================

Skill-scoped changelog (never loaded at invocation; read on demand).
Versions match SKILL.md frontmatter `version:`.
Newest first.


## [0.3.0] - 2026-08-29

`ref/stata-dialect.md`: the multi-line brace rule now covers EVERY `if` in a
`.do`, not only the dispatcher's `step -> worker` ladder. JL ruled it on 260829
after reading the `capture quietly describe, varlist` guard written for
`[C01-05]`: "you might be rewrite all the things like this with { }".

The section was renamed from "Dispatcher coding style (multi-line braces)" to
"Brace style - every `if` body on its own line", and gained the `capture` / `_rc`
guard as a second worked example, since that is the shape that prompted it.

It is written as a READABILITY and edit-safety rule, explicitly NOT a
runnability blocker, because the one-line form is proven on the server: the
`v0827_Code0827` snapshot carries 43 one-line `if`s, three of them exactly
`if _rc == 0 global file_policy "`_polalt'"`. Without that sentence the next
reader would "repair" 43 working lines. The reasons to use braces anyway are
that a brace form is never in doubt, never traps when the body is later wrapped
with `///`, and shows the branch in a diff.

No checker rule was added. A gate that failed those 43 proven sites would be
noise, and this is style for new code.


## [0.2.9] - 2026-08-29

Named the boundary of the server-check mode. It is the OUTBOUND leg: everything
done before the code reaches the server. The return leg, where an error comes
back and has to become a rule, moved to the new sibling skill
`remote-error` in this same folder.

Both skills read this folder's `ref/cms-server-checklist.md`, so the three-gate
numbering and the issue-ID grammar stay identical across the two.


## [0.2.8] - 2026-08-22

Added the issue-register section to `ref/cms-server-checklist.md`: where the
register lives, and how an issue is named.

The ID now starts with the owning TASK FOLDER (`R01-07`, `A11-04`), replacing a
flat `S01..S37` counter. JL: "rename the issues starting with the task folder
index or names, and then I can follow it." Two prefixes are not folders, because
two kinds of problem have no single folder to open: `ENV-nn` is the server
itself, `ALL-nn` is the .ps1 runner + config shape that repeats in every folder.

Four rules recorded with it, each one paid for:
- the prefix is the folder's own index, verbatim, never an abbreviation
- every id is exactly 6 characters, because the register's tables are
  hand-aligned and a variable-width id ruins every column
- a renumber keeps a `was` column, since old ids are cited from code
- cite an issue as `[ID]` in code. The bracket is what makes a sweep safe:
  bare `S33` is also the ICD-10 code for lumbar sprain and bare `S10` is a
  plan step id in `workflow/*.yaml`. Matching the bare form would have
  corrupted 49 medical codes and 25 plan steps.


## [0.2.7] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 2.7.0; older entries below keep their original numbers).

## [2.7.0] — 2026-07-05

### Changed (JL: "还是都允许Resolve-StataExe吧" / "这个东西太细节了…没必要写到skill里吧" / "服务器里当然有")

- dialect A5: Resolve-StataExe now accepted for ANY stage (was: hardcoded preferred for cms, resolver standard for data/reg/case); build-stata Step 3 + review checklist aligned.
- dialect A4 + audit-stata: rangejoin exception KEPT (JL confirmed the server has it) but the server-install commentary stripped as too detailed for skill docs.
- data-stage topology CONFIRMED by JL 2026-07-05 ("case是by year的，然后data是几年combine到一起的"), matching the docs as written; thread closed, nothing pending.

## [2.6.0] — 2026-07-04

- deep-audit fixes: rangejoin carved as the ONE allowed SSC exception in audit-stata Step 4 + dialect A4 (both flat-banned it while build/checklist C1/server env authorize it); build-stata $stata rules aligned to dialect A5 (Resolve-StataExe standard for data/reg/case, hardcoded for cms); data stage no longer described as year-orchestrated in build/scaffold (SELF-ORCHESTRATING per SKILL 2.3.0 topology); checklist F2/F3 scoped to runners (results/ still carries config_snapshot.do + manifest.json per L3/L8/B3); dialect + plan-stata RUNNAME grammars aligned to SKILL 2.4.0 (case source dim, reg full grid); /cms-server-checklist skill refs -> SERVER CHECK mode; Gate-1 comment = local synth run; retired haipipe-task-logging pointer removed.

## [2.5.0] — 2026-07-04

- review sweep: 4 stage plan-sample schema headers task/haipipe-workflow (were dead project/ paths); fn/audit-stata.md + fn/plan-stata.md relative hub paths ../../../haipipe-task (were off-by-one).

## [2.4.0] — 2026-06-10

- align reg stage to D01 ground truth — add run-ps1-reg-template.ps1 + config-seed-reg-run.do; rewrite config-seed-reg.do (data path only, controls in workers); fix RUNNAME to include cohort+pairing+source; document DID policy as reg-stage concern (not C-stage); make describe optional for reg; add Step 3b to build-stata (reg runner authoring); fix workflow-plan-sample-reg.yaml (DID policy phase, correct skill name).

## [2.3.0] — 2026-06-10

- align templates+contract with production — add topology families (orchestrated vs self-orchestrating) to dialect; soften A5 (accept Resolve-StataExe); scope B2/B3 by topology; expand config-seed-data to production size (~80 globals); add run-data-runner-template.ps1; data-stage synth/real source dimension; STATATMP in orchestrator template; match-existing mode in build-stata.

## [2.2.0] — 2026-06-10

- fix 6 issues — rewrite 4 plan samples to match real pipeline phases; remove SSC from build-stata; fix scaffold config extension; update orchestrator template to working version (<=30 lines); fix ~15-><=30 budget; remove helper function references from build-stata.

## [2.1.0] — 2026-06-10

- absorb cms-server-checklist from 0_utils; add server check mode with three-gate protocol.

## [2.0.0] — 2026-06-10

- unified — absorb all 4 child specialists (cms/case/data/reg) into one skill; no child delegation.

## [1.2.0] — 2026-06-09

- unwrap prose; fix agent names to haipipe-task-{creator,reviewer}-agent; add lifecycle paragraph.

## [1.1.0] — 2026-06-08

- add metadata; workflow lifecycle compatible.

## [1.0.0] — 2026-05-31

- baseline.
