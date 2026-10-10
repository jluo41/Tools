s11 · The Group scope
=====================

**Topic:** Every view with the scope toggle on Group, shot on the synthetic fixtures, with what each reads on disk. Only Case and Annotate are built at this scope; seven views show a placeholder (261009, g01).

**Feeds:** `reports/` q05_placeholder_views


Files
-----

```text
s11-group-scope/
├── s11-group-scope.md            this face
├── build_s11_group_scope.py      the builder (with ../_build/console_draw.py)
├── s11-group-scope.excalidraw    the drawing; a person's marks are kept on rebuild
├── s11-group-scope.png           its preview
└── shots/                 screenshots of the console on its SYNTHETIC fixtures
```

Rebuild: the console on its fixtures (`fixtures/run_fixture.sh`), then `uv run --no-project --with playwright python _build/shoot_console.py` (when the shots are stale), then `python build_s11_group_scope.py` and haipipe-studio's `scripts/render_png.py`.


Decided
-------

s11-D01 · A view that is a placeholder at Group leaves the Group rail; seven are hidden (Q05, g02 261009)
s11-D02 · Tasks reads the Block · Job · Task ladder (Q03, g02 261009)


Open
----

1. Which Group view to build first, now that the rail shows only built ones (Q05 Next).

(write here, or mark the drawing in red)
