s12 · The Individual scope
==========================

**Topic:** Every view with one synthetic human selected (SynthCGM_v0 · synth-cgm-001), shot on the fixtures, with what each reads on disk and the route that serves it (261009, g01).

**Feeds:** `reports/` q01_console_vs_toolkit


Files
-----

```text
s12-individual-scope/
├── s12-individual-scope.md            this face
├── build_s12_individual_scope.py      the builder (with ../_build/console_draw.py)
├── s12-individual-scope.excalidraw    the drawing; a person's marks are kept on rebuild
├── s12-individual-scope.png           its preview
└── shots/                 screenshots of the console on its SYNTHETIC fixtures
```

Rebuild: the console on its fixtures (`fixtures/run_fixture.sh`), then `uv run --no-project --with playwright python _build/shoot_console.py` (when the shots are stale), then `python build_s12_individual_scope.py` and haipipe-studio's `scripts/render_png.py`.


Decided
-------

(none yet: a decision is one line, s12-D01 · <what was decided> (<who> <date>))


Open
----

1. Internal and External are still placeholders here too (Q05).

(write here, or mark the drawing in red)
