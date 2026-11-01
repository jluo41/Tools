s51 · The console runtime
=========================

**Stage:** explore

**For:** a deck, and how the console runs, its settings, and the routers its image is missing, for the people who build the console

**Delivery type:** code

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

s51-D01 · The image copies every module (COPY *.py) and personas/; built and run on the fixtures (g02 261009)


Open
----

1. Agree its **For:** line and **Delivery type:** (code), proposed by the agent 261030?

(none: the image starts; on this network pip needed a trusted package index to build)

(write here, or mark the drawing in red)
