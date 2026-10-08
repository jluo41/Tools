Registered design methods
=========================

One folder per method, `MNN-<slug>/`: its `method.md` (name · type · family · card · versions · current) and one
file per version, `m<k>.md`, the version a Job pins (`pin_method.py`). A version is frozen once pinned; a change is
the next version. The type is one of the Guide's 13 cards (`servers/workbench-design/guide/methods/`).

```text
method  name                  type          family     versions
M01     Goal only             By goal       Goal Only  m1 · m2
M02     Overall performance   By precedent  Internal   m1 · m2
M03     Detailed evidence     By insight    Internal   m1 · m2
M04     Actionable insights   By insight    Internal   m1 · m2 · m3
M05     Raw-data agent        By insight    Internal   m1 · m2
```

Generic only: a version names parts of step ① and kinds of source, never an application, project, vendor or
person. The design workbench's reader names the same five (`servers/workbench-design/design_reader.py` `METHODS`);
`tests/test_method_registry.py` checks they agree.

How many ideas ② makes is the version's ② choice; when it names no count, ② makes N + 5 (N the goal's `n`). The rule
is stated once, in `haipipe-design-unit/references/reason.md`. ④ always runs T0 and T1; T2 only when the version's ④
lists it. T3 runs inside t99's rank Run when the version's ⑤ asks for it.

The input ladder (261008): M01 m2 · M02 m2 · M03 m2 · M04 m3 share ② to ⑤ and each sees what the one before sees plus one more layer of the same insight (`sees:` narrows a part to a `kind:` of the inputs version, e.g. `Information · whose [information]`; haipipe-design-goal `make_inputs.py`), so the designs differ by the input alone. M05 m2 is the benchmark beside it: the goal and the raw data's tools.
