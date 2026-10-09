s13 · The case builder
======================

**Topic:** The Case view on each synthetic data type, and how a case is meant to be built (TriggerFn · Key · CaseFn, `diagram/07-case-builder.txt`). Today any record row with text is a case: on a timeline that is every reading (261009, g01).

**Feeds:** `reports/` q01_console_vs_toolkit


Files
-----

```text
s13-case-builder/
├── s13-case-builder.md            this face
├── build_s13_case_builder.py      the builder (with ../_build/console_draw.py)
├── s13-case-builder.excalidraw    the drawing; a person's marks are kept on rebuild
├── s13-case-builder.png           its preview
└── shots/                 screenshots of the console on its SYNTHETIC fixtures
```

Rebuild: the console on its fixtures (`fixtures/run_fixture.sh`), then `uv run --no-project --with playwright python _build/shoot_console.py` (when the shots are stale), then `python build_s13_case_builder.py` and haipipe-studio's `scripts/render_png.py`.


Decided
-------

(none yet: a decision is one line, s13-D01 · <what was decided> (<who> <date>))


Open
----

1. Read the cooked CaseSet, or name each data type's case stream?
2. On a timeline, is a case a 5-minute window rather than a row?

(write here, or mark the drawing in red)
