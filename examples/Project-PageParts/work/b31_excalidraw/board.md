# b31 · Excalidraw drawings

board-kind: task-block
package: plugins/haipipe-toolkit
spine: How the toolkit's Excalidraw skills draw: the steps from a source file to a drawing, the script behind each step, and what each step costs.
close: Each Excalidraw skill mode in use has a Studio topic naming its steps, its scripts and its cost, measured on a real drawing.

## Topic

The Excalidraw skills (`1_base/draw/hai-draw`, the principles every Studio drawing follows, and
`hai-draw report`, `-slide`, `-read`, `-section`, `-job`, `-task`) and hai-studio's writer (`canvas.py`) make
the drawings every Block's Studio shows. This Block records how
they draw, one topic per mode, each from a drawing that was actually made, so the expensive and fragile
steps are known before the next one.

Excluded: what a Studio topic is and how its folder works (hai-studio). The look of a drawing is included since
261012: b31 s01 holds the principles (hai-draw).

## Pipeline

```text
a drawing made in some Block -> its steps, scripts and timings -> a Studio topic here -> a skill change
```

## Pages

No Jobs yet. Studio topics:

- s01-drawing-principles: the seven drawing principles, hai-draw's topic (closed 261012)
- s02 to s07: one topic per skill: hai-draw report, -slide, -read, -section, -job, -task
- s21-revise-mode-workflow: hai-draw draft, from b31_prep_ai's s04 (SHIFT Task 3.1), 2026-10-11
