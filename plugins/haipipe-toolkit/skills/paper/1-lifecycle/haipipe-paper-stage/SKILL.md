---
name: haipipe-paper-stage
description: "One door for every paper lifecycle stage: seed · resource · claims · venue · pitch · narrative · display · section-edit. Reads stages/index.yml, loads ONLY the requested stage's contract, and drives its declared phases. Trigger: 写 seed, 立项, resource, 我们有什么, claims, 主张, H1, venue, 选刊, 投哪个期刊, pitch, 卖点, hook, narrative, 叙事, 大纲, display, 图表, figure, table, section edit, 写某一节, /haipipe-paper-stage."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.8.8"
  last_updated: "2026-07-27"
  summary: "Board-first stage router: Paper is the public page creator; Board owns the shell, filename, pages, and optional inherited contracts."
  # version history: ./CHANGELOG.md
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

**Step 2a — ensure this stage's Board page exists.**
The Paper stage is the only public creator for paper lifecycle pages. Resolve the page by the
selected contract's stable `board_family` + `board_unit`; do not store or guess a literal
filename. If the page is absent, create its Board shell and stage-specific Content scaffold with:

```sh
python3 create-page.py <stage-key> <paper-root>
```

`create-page.py` selects the stage template, then calls `haipipe-board/stage.py new` for the
filename, face grammar, listing under Pages, and managed Stage Contract. It does not draft the
research substance. For a dynamic `runs: per-unit` page, pass the resolved identity and directory
with `--family`, `--unit`, `--slug`, and `--directory`; Section-edit also requires
`--section-kind`, which resolves the exact template from the Venue page's `Section Styles`
record (or its declared generic fallback). `--template` is an explicit repair/testing override,
not the normal routing path. Do not create a sidecar request or handoff file; unfinished work
stays in that page's `## Items to Finish`.

**Step 3 — read the loop, once.**
The declared phase loop, the gates, and the phase-transition contract are NOT restated per stage.
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
- `runs: per-unit` means the phase list runs once PER UNIT. Use it when units have independent
  human gates. Section Edit already implements this grain; Display qualifies by the same rule,
  but its current central-artifact contract remains `runs: once` until the tracked migration is
  complete. A stage whose output gates as one thing remains `runs: once`.
- `commissions:` names worker skills this stage hands units to (display → the four renderers).
  Those workers stay independently registered and are invoked by name.
- `gates:` declares this stage's HUMAN stops, the same way `phases:` declares its phases. The
  default is `[check]` — ONE gate, at the end. DRAFT, PROBE and REVISE run unattended.
  Never open a gate a stage did not declare, and never skip one it did.

**Step 4a — synchronize the lifecycle board mapping.**
Each stage contract declares two stable identity fields:

```text
board_family   stable ownership group: Seed, Work, Venue, Display, Main, or Appendix
board_unit     the page's unit inside that family
```

Board tooling owns the filename and resolves it from that identity. These fields do not change
stage execution order and do not replace `artifact:`. The actual run still follows
`stages/index.yml`, `upstream`, and `downstream`; for example Narrative is followed by the
independent Display family before manuscript sections consume its assets. After any phase changes
the artifact, sync the resolved S face in the same turn: update its `state:`,
`## Items to Finish`, and `## Where we are`, then rebuild the board. When the S face embeds the
artifact, do not copy its Content. Submission and revision are downstream board rounds, not extra
router stages here.

The mapped S face may declare `requires:`, `style-from:`, and `provides:`; all three are optional.
When present, they are board contracts, not router edges: `requires` is the sole authoritative
dependency declaration and names upstream outputs this page must honor,
`style-from` names the venue or project writing contract, and `provides` states the compact
downstream handoff. A stage contract may carry `read_order:` as optional craft guidance for the
sequence in which DRAFT opens material; it is not a second dependency graph. Create or refresh the
managed `## Stage Contract` block with
`haipipe-board/stage.py`; never copy whole upstream Content, and never let `build.py` edit
Markdown. If the board reports a stale contract after an upstream change, run explicit
`stage.py sync` before CHECK.

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

## Rebuild the Board after every write

Ruled 2026-07-26 (design board `QA1`, `QA4`). `/haipipe-paper` is the single
thing a human types, and `enter` leaves them LOOKING at `⑧` in a browser. That
makes a stale `board.html` a defect, not an inconvenience: the human is reading
a picture of a paper that no longer exists.

```text
   a stage run writes S-<Family>-<n>-<slug>.md
        │
        ├─ DRAFT   → ## Content + Q-consumer records in ## Items to Finish
        ├─ PROBE   → the entry pointers
        ├─ REVISE  → the same page + %% why-comments, when declared
        ├─ CHECK   → state: ✅   (a HUMAN writes this)
        │
        └─ then ALWAYS: call ③ haipipe-board build on 0-lifecycle/
                        and put the deep link in the closing block
```

**Two directions, both mandatory.**

```text
AFTER a write   rebuild, or the browser shows the previous version
BEFORE a read   RE-READ the page off disk. A human comment or a `>` lane
                may have arrived through serve.py since this session last
                looked, so ⑧'s markdown can change underneath ①. Never
                cache a page across a phase boundary.
```

The second is the one that keeps the two-channel design honest: `③` writes `⑧`
from a human's click, so `①` may never assume it wrote the page last.

Calling is not owning. `③` owns the build, the filename rule and the html;
this skill calls it and renders nothing.

## Layout

```text
haipipe-paper-stage/
├── SKILL.md                   this file — the only registered skill here
├── create-page.py             Paper's public creator; composes Board shell + stage scaffold
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

## Status — all 8 stages live, Board-first creation ready

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

The stage system has been driven against a real MISQ paper. Known business
blockers remain declared on their S pages; they are not hidden by this router.
