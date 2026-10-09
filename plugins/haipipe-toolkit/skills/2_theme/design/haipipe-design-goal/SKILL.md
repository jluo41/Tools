---
name: haipipe-design-goal
description: >-
  Everything a design reads, on the design ladder: a Block's goal list
  (board.md ## Goals, each goal signed by a person), its shared rules
  (design-goal.md), its frozen inputs versions (inputs/iN/ + manifest.yaml), and
  a Job's inputs/ fence (goal.md, links into one inputs version, manifest.yaml
  with each file's sha256), which is all the design work may see. Owns
  run-add-goal-<goal>, run-setup-rules, run-add-inputs-i<N>,
  run-setup-goal-j<NN> and run-setup-inputs-j<NN>. Use to add or sign a goal, set
  the shared rules, freeze an inputs version, or build a Job's fence. An older
  board's design-goal.md (Aim · Venue · Rules · Resources · Leave out) keeps its
  contract in ref/legacy/. Trigger: design goal, goal list, add a design goal,
  shared rules, inputs version, freeze inputs, inputs fence, inputs manifest,
  /haipipe-design-goal.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
metadata:
  version: "0.4.1"
  last_updated: "2026-10-09"
  # version history: ./CHANGELOG.md
---

# /haipipe-design-goal · what a design reads

Version governance: this skill keeps its current version, `0.4.0`. Only explicit user approval may authorize a
version change.

A design starts from an **aim**, **constraints** and **resources** (Theory of Design §2,
`servers/workbench-design/guide/method.md`). On the ladder (`haipipe-design/ref/design-ladder.md`) these are four
records, each written once and read by every Job that pins it:

```text
design/Design-<name>/
├── board.md ## Goals          the goal list: one entry per goal, signed by a person      run-add-goal-<goal>
├── design-goal.md             the shared rules every goal keeps; a person signs them     run-setup-rules
├── inputs/iN/                 one inputs version: rules · theory · handoff copies,       run-add-inputs-i<N>
│   └── manifest.yaml          frozen: each file, its part of step ①, its sha256
└── jNN_<goal>_<method>/
    └── inputs/                the fence: goal.md · method.md · links into ../../inputs/iN/ ·
        └── manifest.yaml      what the design work may see                                run-setup-inputs-j<NN>
```

An older board (`B00_DesignBoard-<name>/`) keeps its single `design-goal.md` (Aim · Venue · Rules · Resources ·
Leave out, `Task · <folder>` overrides) and the old page's Design Goal Space: its contract is
[ref/legacy/design-goal-older.md](ref/legacy/design-goal-older.md).


The goal list
-------------

`board.md ## Goals` holds one fenced yaml block, `goals:`, one entry per goal:

```yaml
goals:
- id: G01                       # G<NN>, never reused
  aim: <the behaviour to change>   # a change for the person, not an output
  who: <audience>
  venue: sms                     # a venue/venue-<channel>/ profile
  n: 10                          # how many designs a Job keeps
  rules: [<a rule for this goal only>]   # beyond the shared rules
  leave-out: <what no design for this goal may use>
  signed: ✅ <YYMMDD>              # empty until a person signs
```

1. **A goal is signed once, at the Block.** `run-add-goal-<goal>` writes the entry with `signed: ""`; it becomes
   usable only when a person writes the date. Before signing, `aim`, `who`, `venue` and `n` must be filled; only
   `leave-out` may stay `?` (a gap the person accepts). A Job never re-states the goal: `run-add-job` writes the
   face's `goal:` pin and copies the goal's `n` onto the face, and `run-setup-goal-j<NN>` only confirms the pin
   names a signed goal.
2. **A changed goal is a new goal.** Edit only an unsigned entry; a signed goal that must change becomes `G<NN+1>`,
   so every Job's pin keeps meaning what it meant.
3. **Every line has a source.** What the aim, audience or leave-out rests on is named in the Run's pass (a signed
   insight, a person, a file of an inputs version); a gap stays `?` and becomes a question for the person.


The shared rules
----------------

`design-goal.md` at the Block holds the rules every goal keeps (`## Rules`, `## Leave out`), each checkable on the
text alone, with two lines at its head: `rules: r<k>` (the rules version; a changed rule set is `r<k+1>`) and
`signed: ✅ <YYMMDD>` (empty until a person signs through `run-setup-rules`). The gate before `run-add-job` reads both.
An inputs version records which rules version it carries (`rules: r<k>` in its manifest). A rule for one goal only
goes in that goal's `rules:`.
The venue's own defaults live in `venue/venue-<channel>/README.md`; write a venue line here only where the Block
narrows it.


Inputs versions
---------------

An inputs version `inputs/iN/` is a frozen set of files a Job may read: the shared rules as signed, theory notes,
copies of the insight Block's signed handoff (copied, not linked: a later handoff is a new version), past released
designs. Its `manifest.yaml`:

```yaml
version: i2
frozen: '<YYMMDD>'
new: <what changed from i<N-1>>
rules: r2                                # the design-goal.md rules version this inputs version carries
parts:                                   # which part of step ① each file serves
- {part: Goal · how much is set, file: rules.md, says: the shared rules}
- {part: Information · whose, file: handoff-W-03.md, says: 'ours: the insight Block''s signed handoff'}
files:
- {path: rules.md, sha256: <first 12 hex>}  # sha256 is stored as the first 12 hex of the file's sha256
```

`run-add-inputs-i<N>` writes the files, then freezes them (`scripts/make_inputs.py freeze`). A frozen version is
never edited; new material is `i<N+1>`, and a Job on it is a new Job (one clock: `moved: inputs`). A newer handoff
never makes a released design stale.


The Job's fence
---------------

The design work of a Job sees only its `inputs/` (s12). `run-setup-inputs-j<NN>` builds it after the goal is
confirmed and the method is pinned, with `scripts/make_inputs.py job <job>`, which refuses to run until
`inputs/method.md` is there:

1. `goal.md`, written from the pinned goal's entry in `board.md ## Goals` (this Run is its only writer).
2. `method.md`, already there: `run-setup-method-j<NN>` (haipipe-design-method) copies the pinned version; the
   manifest records its source as that registry version.
3. One relative link per Block input the method's step ① lets it see (`sees:` in `method.md`), into
   `../../inputs/iN/`; nothing else.
4. `manifest.yaml`: each part of step ① with its choice and file (a part the method leaves out reads `nothing`),
   and each file with its source (`written` or the link) and sha256.

Each reasoning step's `from` (t00's chains, a design's elements) is a file in this manifest or says exactly
`own knowledge`; the reviewer checks it in the first pass of `run-open-designs-j<NN>` (`fence-check.md`) before the
design Tasks open. Rebuilding the fence after a goal or method change is a new pass of `run-setup-inputs-j<NN>` on a
Job whose t00 has not run; once t00 has run, a change is a new Job. A design that needs an input the fence lacks
(found by a verify) is never fixed by a revise: it is dropped, or a new inputs version (`run-add-inputs-i<N+1>`)
makes a new Job (`moved: inputs`).
The full contract, with each file's shape: [ref/inputs.md](ref/inputs.md).


The Runs
--------

| Run | Level | Writes | Person signs |
|---|---|---|---|
| `run-add-goal-<goal>` | Block | one entry in `board.md ## Goals` | the goal |
| `run-setup-rules` | Block | `design-goal.md` `## Rules` · `## Leave out` | the rules |
| `run-add-inputs-i<N>` | Block | `inputs/iN/` and its frozen `manifest.yaml` | none |
| `run-setup-goal-j<NN>` | Job | nothing but its pass: confirms the face's `goal:` pin names a signed, filled goal | none |
| `run-setup-inputs-j<NN>` | Job | `inputs/goal.md`, the links, `inputs/manifest.yaml` (after `inputs/method.md`) | none |

All five are soft (`run-<type>-<target>/run.yaml` and `passes/`; `haipipe-run`); `haipipe-designer-agent` runs
them (its run cards name it). Show the person the changed lines before writing a goal or a rule; write them only after the person says yes.

```bash
python scripts/make_inputs.py freeze design/Design-<name>/inputs/i2 --new "a new handoff"
python scripts/make_inputs.py job design/Design-<name>/j03_g01_m04
```


Boundary
--------

This skill writes the goal list, `design-goal.md`, `inputs/iN/` and a Job's `inputs/` (except `method.md`, which
`haipipe-design-method` copies). It does not choose or version a method, open Tasks, design, or score. It never
writes patient rows or raw data into an inputs version: a handoff is a signed counsel, an Exp's result is per-arm
totals at `observed/` (`haipipe-design-method`).
