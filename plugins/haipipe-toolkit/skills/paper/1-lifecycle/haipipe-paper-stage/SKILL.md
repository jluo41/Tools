---
name: haipipe-paper-stage
description: "One door for every paper lifecycle stage: seed · resource · claims · venue · pitch · narrative · display · section-edit. Reads stages/index.yml, loads ONLY the requested stage's contract, and drives its declared phases. Trigger: 写 seed, 立项, resource, 我们有什么, claims, 主张, H1, venue, 选刊, 投哪个期刊, pitch, 卖点, hook, narrative, 叙事, 大纲, display, 图表, figure, table, section edit, 写某一节, /haipipe-paper-stage."
argument-hint: "[stage-name] [paper-dir | topic] [draft|probe|revise|check] [stage-args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.4.0"
  last_updated: "2026-07-20"
  summary: "Stage router. One registered skill replacing 8 per-stage skills; per-stage contract+craft live as DATA under stages/<order>-<key>/stage.md (no name: field, so they do not register). Only ONE stage's file is ever loaded per invocation. All 8 stages migrated; the legacy skills are still on disk and untouched. UNTESTED end-to-end."
---

Skill: haipipe-paper-stage
==========================

The single entry point for every stage of the paper lifecycle.

```text
/haipipe-paper-stage <stage-name> [paper-dir] [phase] [stage-args...]
                     ▲
               always first
```

The per-stage skills are GONE. `/haipipe-paper-seed`, `/haipipe-paper-venue`, and the other six
no longer exist — every stage comes through here, stage key first.

## Procedure

**Step 1 — resolve the stage.**
Read `stages/index.yml`. This is the ONLY file that enumerates all stages, and it is deliberately
small. Match `$1` against each row's `key`; if `$1` is not a key, match the user's phrasing against
`triggers`. Ambiguous or absent → list the keys and ask; never guess a stage.

**Step 2 — load exactly ONE stage.**

```text
migrated: true   -> Read stages/<dir>/stage.md   ← the contract (frontmatter) + craft (body)
migrated: false  -> Skill("<legacy_skill>", args="<the rest of $ARGUMENTS>") and STOP.
                    Say plainly that the stage has not been cut over yet.
```

⛔ NEVER read the other stages' `stage.md` files. Loading all eight is a 7.5x context regression
over the per-stage skills this replaces, and it is the specific failure mode this layout exists to
avoid. One invocation, one stage file.

**Step 3 — read the loop, once.**
The four-phase loop, the gates, and the phase-transition contract are NOT restated per stage.
They live at:

```text
probe/haipipe-probe/SKILL.md          the probe layer + the DRAFT/PROBE phase rules
paper/1-lifecycle/ref/08-stage-gate.md  the stage gate + Phase Transition Contract
```

**Step 4 — drive the stage's declared phases.**
Run the phases listed in that stage's `phases:` field, in order, each through its `Skill()`
dispatch (`haipipe-paper-draft` · `-probe` · `-revise` · `-check`). A phase executed inline did
not happen.

- `phases:` is a LIST, not a type. venue declares `[draft, probe, check]` — it raises real
  `Q-Venue-<n>` entries that PROBE answers, but produces a contract rather than prose, so it has
  no REVISE. Run what the stage declares; never pad a list to four.
- INVARIANT: `phases` always ends with `check`. That is the human gate.
- `runs: per-unit` (section-edit) means the phase list runs once PER UNIT, and `$2` is the unit,
  not the paper dir.
- `commissions:` names worker skills this stage hands units to (display → the four renderers).
  Those workers stay independently registered and are invoked by name.
- `gates:` declares this stage's HUMAN stops, the same way `phases:` declares its phases. The
  default is `[check]` — ONE gate, at the end. DRAFT, PROBE and REVISE run unattended.
  `1a-resource` is the exception and declares its own, per a standing ruling.
  Never open a gate a stage did not declare, and never skip one it did.

**Step 4b — the PROBE ceiling.**
`probe_depth:` is what makes a single CHECK gate safe: PROBE may only dispatch work whose cost
sits at or below the ceiling, so an unattended run cannot spend.

```text
depth  bank:    what it takes                        cost
  0    reuse    results already answer it            free — nothing runs
  1    run      old script, new config               costs
  2    code     must write new code first            costs
  3    new      open a new task-folder               costs most
```

The ladder is the bank's own (`task/haipipe-task/fn/qa.md`, "How deep"), and the consumer's
`bank:` verdict maps onto it 1:1. The rule is one line:

```text
dispatch when depth(bank) <= probe_depth, else DEFER the entry
```

Default is `0`, so a plain run HARVESTS and never orders. Raise it for one invocation:

```text
/haipipe-paper-stage <stage> <paper> probe             ceiling 0 — harvest only, free
/haipipe-paper-stage <stage> <paper> probe --depth 1   also allow reruns of existing code
/haipipe-paper-stage <stage> <paper> probe --depth 3   unsealed — may open new task-folders
```

⚠️ `--depth` AUTHORIZES SPEND. Passing it is the human act that a removed DRAFT gate used to be.
Report what each raise actually dispatched; never raise it on your own initiative.
⚠️ Depth is a proxy for KIND of work, not AMOUNT: a depth-1 rerun over a large cohort can cost
far more than a depth-2 script that counts rows.

**Step 5 — verify before CHECK.**
Run the probe-card checker scoped to THIS stage key. Locate it layout-agnostically (installed
skills flatten the tree) and filter on the paper family — two files of that name exist on disk
with different invariants:

```sh
# The RELATIVE path resolves even from an installed symlink, because the link's target
# sits in the real tree — prefer it. The find is the fallback, and it needs -L: installed
# skills are symlinks and a find without -L descends into nothing and returns zero hits.
CHK="../../../2-phase/1-probe/haipipe-paper-probe/check-probe-cards.sh"
[ -f "$CHK" ] || CHK=$(find -L ~/.claude/skills ./.claude/skills "${CLAUDE_PLUGIN_ROOT:-/nonexistent}" -maxdepth 4 \
                         -path '*haipipe-paper-probe/check-probe-cards.sh' 2>/dev/null | head -1)
[ -n "$CHK" ] && [ -f "$CHK" ] || { echo 'FAIL: paper probe checker not found'; exit 1; }
sh "$CHK" <paper_root> --stage <stage-key>
```

`--stage <key>` IS PART OF THE COMMAND. Without it the checker globs the whole paper and this
stage's gate inherits every other stage's open work.

PASS 1's vacuous-green test works for every stage key as of 2026-07-20. It fires when NO entry
serves this stage while the stage doc still has unanswered Q-consumer blocks — the case where a
green would mean "nothing was ever opened". Before that fix it was keyed on "any probe file
exists", so on a mature paper it was unreachable for every stage, resource included.

## Layout

```text
haipipe-paper-stage/
├── SKILL.md                   this file — the only registered skill here
└── stages/
    ├── index.yml              the index (small, always read)
    └── <order>-<key>/         one folder per stage
        ├── stage.md           frontmatter = CONTRACT · body = CRAFT
        │                      (no `name:` field — this is DATA, not a skill)
        ├── template.md        the artifact skeleton + its inline <!-- RULE --> comments
        └── …                  that stage's own support files. They are NOT uniform:
                               2b-pitch has readability.md · 4-display has checklist.md
                               and figure-logic.md · 5-section-edit has NEITHER — its
                               template is its own rulebook and its section norms come
                               from the venue packs. Never assume a file exists because
                               another stage has one.
```

Adding a stage = one folder + one row in `index.yml`. No new skill, no version bump, no
`description` edit.

## Status — v0.4.0, all 8 stages live, CUTOVER DONE, first real run driven 2026-07-21

```text
✅ seed · resource · claims · venue · pitch · narrative · display · section-edit
```

The 8 legacy stage skills are GONE — unregistered and retired to `../_old/`, which is treated as
DELETED, not as a rollback. Everything a live path needs was salvaged out of it first:
every `*-template.md`, `pitch-readability.md`, `figure-logic.md`, `CHECKLIST.md`,
the shared `display-unit-output-contract.md`.
Nothing under `../_old/` may be referenced by a live file.

Wired to this skill, all verified 2026-07-20:

```text
haipipe-paper-draft        Step 1 reads stages/<dir>/stage.md + template.md (was: the legacy SKILL.md)
haipipe-paper-lifecycle    every stage key -> Skill("haipipe-paper-stage", args="<key> …")
haipipe-paper              same rule stated in its dispatch block
haipipe-paper-check        gate table keyed on stage NAME, not skill name
4 display renderers        STAY registered; the shared contract moved to ../../4-display/ref/
                           and all 12 relative paths were rewritten
```

⚠️ NOT yet driven end-to-end on a real paper. The first real run is the acceptance test.

Known divergences found while migrating, none resolved:

```text
template vs contract disagree, 4 stages
  claims        SKILL says supported|refuted|inconclusive; template says supported/weak/GAP
  narrative     SKILL says no #/##/###; its own template uses ## throughout
  display       template uses `## Q1 · <title>`; every sibling + the checker's PASS 4 want
                the `## Q-Display-<n>` family form
  section-edit  heading is `### §<N>-Q<n>` while the inline anchor is `[Q-<Stage>-<n>]` —
                not the 1:1 token match seed has

resource        the source runs THREE human stops (GATE 1, GATE 1b spend-after-scan, GATE 2);
                ref/04-lifecycle-map.md records only two, and that map was the source used
                for `exit_when`. GATE 1b's substance is folded into gates.gate_1.
```
