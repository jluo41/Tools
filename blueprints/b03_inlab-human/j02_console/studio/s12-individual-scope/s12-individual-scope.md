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

s12-D01 · Internal, External and Annotate (placeholders at Individual) leave the Individual rail (Q05, g02 261009)
s12-D02 · The Record chart draws a lane per table with a time column, naming no table (g02 261009)


Open
----

1. Build Internal first, then bring it back to the rail (Q05 Next).

(write here, or mark the drawing in red)
