Inputs: a Block's inputs versions and a Job's fence
===================================================

(JL 261007, designed in Tools/designs/b12_theme_design s11 · s12 · s13; the ladder is
haipipe-design/ref/design-ladder.md rule 4.) The design work of a Job sees only its own `inputs/`. This reference
gives each file's shape; `scripts/make_inputs.py` writes the manifests and the links.


The parts of step ①
-------------------

Step ① See input of a design method chooses what the design work sees, part by part. Every manifest names its
files by these parts (the design workbench reads them in this order):

```text
Goal · how much is set     the aim, N, leave out, the shared rules
Goal · for whom            who the design is for
Information · whose        ours (an insight Block's signed handoff, past designs) or theirs (literature)
Information · form         a theory or rule, a channel's setting
Examples                   past released designs
Tools                      what the design work may call
Reading                    papers it reads
From the last unit         the previous round's results (a looping method)
```


A Block's inputs version · inputs/iN/
-------------------------------------

Any files, then `manifest.yaml`, written last by `make_inputs.py freeze` and never edited:

```yaml
version: i2                  # the folder name
frozen: '261007'             # YYMMDD
new: <what changed from i1>
rules: r2                    # the shared rules' version it carries, if any
parts:
- part: Goal · how much is set
  file: rules.md
  says: the shared rules
- part: Information · whose
  file: handoff-W-03.md
  says: 'ours: the insight Block''s signed handoff'
files:
- path: rules.md
  sha256: 3f2a…              # the first 12 hex of the file's sha256
```

`parts:` is written by the Run (the agent says which part each file serves); `freeze` keeps a `parts:` already in a
draft manifest and lists every file under `files:`. A handoff is copied in, never linked: the insight Block may sign
a newer one, which is a new inputs version.


A Job's fence · jNN_<goal>_<method>/inputs/
-------------------------------------------

```text
inputs/
├── goal.md                  written: the pinned goal's entry (aim · who · venue · N · rules · leave out)
├── method.md                copied by run-setup-method-j<NN> (haipipe-design-method): the pinned version
├── rules.md -> ../../inputs/i2/rules.md            one relative link per Block input step ① sees
├── handoff-W-03.md -> ../../inputs/i2/handoff-W-03.md
└── manifest.yaml
```

Which Block inputs are linked is the method's choice, the `sees:` list in `method.md`'s front matter: the parts of
step ① it may read (`[Goal · how much is set, Information · whose]`). A method with no `sees:` sees only
`Goal · how much is set`. Every file of the inputs version whose part is in `sees:` is linked; nothing else is.

A part may hold several kinds of the same input (JL 261008: a method ladder where each method sees one more layer):
the inputs version's manifest gives such a file a `kind:` (`{part: Information · whose, kind: information, file: …}`),
and a `sees:` entry `<part> [<kind>, …]` links only the files of those kinds; a plain `<part>` links them all. The
Job's manifest copies each linked file's `kind:`.

```yaml
inputs: i2
frozen: '261007'
method: method.md
parts:                       # every part of step ①, in order; a part the method leaves out reads "nothing"
- {part: Goal · how much is set, choice: aim · N · leave out, file: goal.md}
- {part: Goal · how much is set, choice: the shared rules, file: rules.md}
- {part: Goal · for whom, choice: 'in goal.md: who', file: ''}
- {part: Information · whose, choice: 'ours: the insight Block''s signed handoff', file: handoff-W-03.md}
- {part: Examples, choice: nothing, file: ''}
files:                       # every file in the fence but the manifest
- {path: goal.md, source: written, sha256: <first 12 hex>}
- {path: method.md, source: <registry version, e.g. haipipe-design-method M04 m2>, sha256: <first 12 hex>}
- {path: rules.md, source: ../../inputs/i2/rules.md, sha256: <first 12 hex>}
```

`sha256` stores the first 12 hex of the file's sha256, here and in every inputs-version manifest.

1. **The fence is built once, after the method.** `make_inputs.py job` refuses to run until `inputs/method.md` is
   there (`run-setup-method-j<NN>` first), writes what is missing and never overwrites; with a manifest already there
   it does nothing. Rebuilding (a goal or method re-pinned before t00 ran) removes `inputs/` and runs
   again, as a new pass of `run-setup-inputs-j<NN>`.
2. **Links are relative**, `../../inputs/iN/<file>`, so the Block moves as one folder; no absolute path.
3. **Every reasoning step names its source**: a `from:` in t00's `chains.yaml` (a topic's, or a step's own) or a
   design's `elements.yaml` names a file in this manifest or says exactly `own knowledge`. The reviewer agent checks
   t00's in the first pass of `run-open-designs-j<NN>` (`passes/pNN-<MMDD>/fence-check.md`) before the design Tasks
   open; ④ checks each design's elements (T1).
