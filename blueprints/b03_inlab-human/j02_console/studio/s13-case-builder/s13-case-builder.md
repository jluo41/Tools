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

s13-D01 · The Case view reads the dataset's cooked case set (3-CaseStore) when one is mounted (Q02, g02 261009)
s13-D02 · Without one, a row is a case only if it holds prose; a timeline has no cases until cooked (g02 261009)


Open
----

(none: both are decided; which TriggerFn cuts a dataset's cases is its Case stage's)

(write here, or mark the drawing in red)
