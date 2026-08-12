# Thin paper PHASE 2: door fold + workers dissolved (JL "go", 260805)

Ruling chain: QC6 thin-paper row RULED A (fold stage into door) · JL 260805: "we just
remove all the workers/ ... or the worker will go to the haipipe-board" → workers/ goes
to ZERO skills; page rules stay in board/ (already there), LaTeX craft becomes STAGE DATA
files, checkers become scripts declared by stage.md. Board layer stays family-blind:
NO LaTeX knowledge moves into board/.

Root: Tools/plugins/haipipe-toolkit/skills/ (all paths below relative to it).

## Target tree

```
paper/
├── haipipe-paper/            THE one door (absorbs -enter, -lifecycle, -stage)
│   ├── SKILL.md              rewritten, see "Door rewrite"
│   ├── stages/               index.yml + CONTRACT.md + section-kinds.yml  (moved in)
│   ├── create-page.py        moved in (+ check-contracts.py, section-stats.py)
│   ├── probe/                family probe tooling (from workers/haipipe-paper-probe):
│   │                         check-probe-cards.sh · check_topic_entries.py ·
│   │                         topic-entry-contract.md · per-stage-dispatch.md
│   ├── ref/                  ex haipipe-paper-stage/ref/ + ex workers/REF/ (6 files)
│   └── fn/                   existing; probes.md gains unique deltas from probe worker
├── S01-opening … S10-round/  stage DATA (stage.md + template.md + NEW craft files)
├── container/                haipipe-paper-folder · haipipe-paper-conform  (unchanged)
├── S09-build leaves + S10 round/rebuttal   (unchanged skills)
├── venue/                    unchanged
└── _old/                     + haipipe-paper-enter, -lifecycle, -stage, workers/
```

## Move table (mv only, retire to _old/, NEVER delete; git mv when tracked, plain mv fallback)

```
haipipe-paper-stage/stages/*        → haipipe-paper/stages/
haipipe-paper-stage/create-page.py  → haipipe-paper/create-page.py
haipipe-paper-stage/check-contracts.py, section-stats.py → haipipe-paper/
haipipe-paper-stage/ref/*           → haipipe-paper/ref/
haipipe-paper-stage/ (rest)         → _old/haipipe-paper-stage/
haipipe-paper-enter/                → _old/haipipe-paper-enter/   (after absorbing, below)
haipipe-paper-lifecycle/            → _old/haipipe-paper-lifecycle/ (after absorbing)

workers/haipipe-paper-draft-citation/SKILL.md   → S03-literature/citation-craft.md
workers/haipipe-paper-draft-values/SKILL.md     → S04-value/values-craft.md
workers/haipipe-paper-draft-display/SKILL.md    → S05-display/display/draft-craft.md
workers/haipipe-paper-revise-place/SKILL.md     → S06-main/section-edit/revise-place-craft.md
workers/haipipe-paper-revise-results/SKILL.md   → S06-main/section-edit/revise-results-craft.md
workers/haipipe-paper-check-evidence/SKILL.md   → S02-work/claims/check-evidence-craft.md
                                                  (read it first; if its content is
                                                  section-prose-side, S06-main instead)
workers/haipipe-paper-proof-checker/            → S09-build/proof-checker/ (whole dir as
                                                  a craft pack: SKILL.md → proof-checker.md,
                                                  keep ref/ together; NOT registered)
workers/haipipe-paper-probe/check-probe-cards.sh, check_topic_entries.py,
  ref/topic-entry-contract.md, ref/per-stage-dispatch.md → haipipe-paper/probe/
workers/haipipe-paper-probe/SKILL.md unique deltas (MATCH mechanics, depth mapping)
  → merge into haipipe-paper/fn/probes.md; then SKILL.md → _old/
workers/REF/*                                    → haipipe-paper/ref/
workers/ (whatever remains: CHANGELOGs, feedback/) → _old/workers/
```

Craft-file conversion rule: strip the skill frontmatter (name/description/allowed-tools),
keep a 3-line header (`# <title>` + one line "Craft file for stage <key>, loaded by the
DRAFT/REVISE phase" + source note), keep the craft body, DELETE paragraphs that restate
page logic now owned by board/ (phases, registers, walls, bindings) and replace each with
one pointer line to the owning contract. Never delete `> USER:` comments. No em-dashes.
English only.

## Door rewrite (haipipe-paper/SKILL.md)

Merge 4 files (613 + 467 + 520 + 261 lines) into ONE door, target well under 700 lines:
1. Keep: verbs table, routing, closing block, comment lifecycle, delivery need routing,
   evidence routing, no-arg chooser (all from current haipipe-paper).
2. Absorb from -stage: stage resolution via stages/index.yml (Step 1-2), page creation via
   create-page.py (Step 2a), "load exactly ONE stage.md" rule, probe ceiling + the --depth
   SPEND AUTHORITY warning kept word-for-word loud, checker-before-CHECK step (now: run the
   script the stage.md declares via its `checker:` line; default for S03/S04-consuming
   stages is haipipe-paper/probe/check-probe-cards.sh --stage <key>), rebuild-after-write +
   re-read-before-read rules.
3. Absorb from -enter: the derive-from-disk console procedure (enter/status verb), get-or-
   create path. Compress; the console's exact section layout may point at a ref file if
   needed (move detail to haipipe-paper/ref/enter-console.md rather than bloating SKILL.md).
4. Absorb from -lifecycle: stage ordering / maturity rule / phase-verb pass-through.
   These are small once stage resolution is native.
5. Phase driving is NOT restated: the door ensures the page exists then hands to
   haipipe-page (WORK ON, or RUN with a packet); page-phases own DPRC.
6. Dispatch lines that said Skill("haipipe-paper-stage"|"haipipe-paper-enter"|
   "haipipe-paper-lifecycle") become internal steps of this one skill.

## stage.md edits (8 files)

Add to each stage.md frontmatter where relevant:
- `checker:` line (path relative to skills root) for stages that had a pre-CHECK script;
  S01/S02/S05/S06 stages that consume probe entries declare
  `checker: paper/haipipe-paper/probe/check-probe-cards.sh --stage <key>`.
- `craft:` list naming the stage's craft files added by the move table (path per file),
  e.g. section-edit: [revise-place-craft.md, revise-results-craft.md]. Keep it a plain
  list; the DRAFT/REVISE phase loads them after the type contract.
Fix any stage.md prose that references haipipe-paper-stage or workers/ paths.

## Board-side edits (small, versioned, ONE bump per skill at the END)

- page-types/haipipe-page-for-stage: add one paragraph: stage.md MAY declare
  `checker:` (CHECK runs it before judging) and `craft:` (DRAFT/REVISE load these data
  files last, in place of the old "family worker" skills). Bump 0.4.x → 0.5.0.
- page-phases draft/probe/revise + base haipipe-page: reword the load-order slot
  "family worker" → "family craft: the stage's declared craft files (and for probe, the
  family door's probe tooling)". Minimal diffs. Patch bumps.
- probe phase line "family workers own their persisted Probe Page shape and checker" →
  "the family DOOR owns the persisted Probe Page shape and checker".

## Reference sweep (verified-target-first: confirm the NEW target exists before editing a row)

Live files found referencing retired names (skip _old/, skip CHANGELOG history, skip
diagrams/_archive; CHANGELOGs are history and stay):
- paper/README.md (rewrite tree + routing to the new shape)
- paper/haipipe-paper/fn/feedback.md, fn/probes.md
- paper/S02-work/narrative/stage.md, paper/S06-main/section-edit/stage.md
- paper/S05-display/display/checklist.md
- paper/haipipe-paper-folder/SKILL.md, paper/haipipe-paper-conform/SKILL.md
- paper/S09-build/haipipe-paper-to-overleaf/SKILL.md, .../haipipe-paper-diffpdf/SKILL.md
- paper/S10-round/haipipe-paper-rebuttal/SKILL.md
- paper/S03-literature/README.md, paper/S04-value/README.md
- 0_utils/haipipe-run-timeline/SKILL.md (haipipe-paper-enter → haipipe-paper enter verb)
- board/ files per "Board-side edits" above
Search again AFTER moves: `grep -rn "haipipe-paper-stage\|haipipe-paper-enter\|
haipipe-paper-lifecycle\|paper/workers/" --include="*.md" --include="*.yml"
--include="*.py" --include="*.sh" .` excluding _old/ and CHANGELOG.md must return only
history/diagram rows. Diagrams boards (QC6, QCskill mirrors) are handled by the MAIN
session afterward, not by this agent.

## Verify

1. `bash Tools/install.sh --global` → no _old/ registrations, retired symlinks pruned,
   count reported.
2. `python3 paper/haipipe-paper/check-contracts.py` (fix its internal paths for the new
   home first; it must hard-FAIL on zero dirs).
3. Rebuild both design boards at baseline (haipipe-board build on diagrams/01-boardform-260722
   and diagrams/01-haipipe-paper-260725) — must build clean.
4. Final grep sweep per above returns clean.

## Do-not

- No commits. No deletions (retire to _old/). No em-dashes anywhere. English only in all
  written files. Never remove `> USER:` lines. One CHANGELOG entry + one version bump per
  touched skill, written at the END of the work, not per pass.
- Do not edit diagrams/ board pages (main session owns them).
- Do not touch display/skills/ renderers, venue/, container/ beyond the listed reference fixes.
