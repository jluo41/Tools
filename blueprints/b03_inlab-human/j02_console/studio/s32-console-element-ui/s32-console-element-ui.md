s32 · The console's element UI
==============================

**Topic:** Every kind of element the console draws (25), shot on the synthetic fixtures with its computed style (`shots/facts.json`), beside the toolkit frame's element of the same kind where there is one (from b01 j03 s32's shots), so one look can be judged (261009, g01).

**Feeds:** `reports/` q04_one_look


Files
-----

```text
s32-console-element-ui/
├── s32-console-element-ui.md            this face
├── build_s32_console_element_ui.py      the builder (with ../_build/console_draw.py)
├── s32-console-element-ui.excalidraw    the drawing; a person's marks are kept on rebuild
├── s32-console-element-ui.png           its preview
└── shots/                 screenshots of the console on its SYNTHETIC fixtures
```

Rebuild: the console on its fixtures (`fixtures/run_fixture.sh`), then `uv run --no-project --with playwright python _build/shoot_console.py` (when the shots are stale), then `python build_s32_console_element_ui.py` and haipipe-studio's `scripts/render_png.py`.


Decided
-------

(none yet: a decision is one line, s32-D01 · <what was decided> (<who> <date>))


Open
----

1. One look for the console and the workbench, or keep the console's Databricks/Mattermost themes (Q04)?

(write here, or mark the drawing in red)
