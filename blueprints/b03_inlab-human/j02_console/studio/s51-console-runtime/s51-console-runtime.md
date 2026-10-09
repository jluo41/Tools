s51 · The console runtime
=========================

**Topic:** How the console runs: standalone, embedded in a HAI-Chat thread, and on the fixtures; every INLAB_* setting and who reads it; and the image's contents checked against what `main.py` imports (four routers missing) (261009, g01).

**Feeds:** `reports/` q01_console_vs_toolkit


Files
-----

```text
s51-console-runtime/
├── s51-console-runtime.md            this face
├── build_s51_console_runtime.py      the builder (with ../_build/console_draw.py)
├── s51-console-runtime.excalidraw    the drawing; a person's marks are kept on rebuild
└── s51-console-runtime.png           its preview
```

Rebuild: `python build_s51_console_runtime.py`, then haipipe-studio's `scripts/render_png.py`.


Decided
-------

(none yet: a decision is one line, s51-D01 · <what was decided> (<who> <date>))


Open
----

1. Fix the Dockerfile so the image holds every module and personas/.

(write here, or mark the drawing in red)
