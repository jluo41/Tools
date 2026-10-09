s21 · The run bar
=================

**Topic:** The run bar's five steps (▶ Run · Interpret · Message · Judge · Feedback) with who does each and its route; both stub runs; and every HaiChat tool with the ConsoleAction it dispatches and its gate, read from `haichat_api.py` (261009, g01).

**Feeds:** `reports/` q01_console_vs_toolkit


Files
-----

```text
s21-run-bar/
├── s21-run-bar.md            this face
├── build_s21_run_bar.py      the builder (with ../_build/console_draw.py)
├── s21-run-bar.excalidraw    the drawing; a person's marks are kept on rebuild
├── s21-run-bar.png           its preview
└── shots/                 screenshots of the console on its SYNTHETIC fixtures
```

Rebuild: the console on its fixtures (`fixtures/run_fixture.sh`), then `uv run --no-project --with playwright python _build/shoot_console.py` (when the shots are stale), then `python build_s21_run_bar.py` and haipipe-studio's `scripts/render_png.py`.


Decided
-------

(none yet: a decision is one line, s21-D01 · <what was decided> (<who> <date>))


Open
----

1. Could this action list become an MCP that drives the toolkit's workbench (j04 Q02, b01 j05_chat Q02)?

(write here, or mark the drawing in red)
