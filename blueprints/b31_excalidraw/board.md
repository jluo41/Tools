# b31 · Excalidraw drawings

board-kind: task-block
package: plugins/haipipe-toolkit
spine: How the toolkit's Excalidraw skills draw: the steps from a source file to a drawing, the script behind each step, and what each step costs.
close: Each Excalidraw skill mode in use has a Studio topic naming its steps, its scripts and its cost, measured on a real drawing.

## Topic

The Excalidraw skills (`1_base/display/excalidraw-read`, `excalidraw-report`, `excalidraw-slide`) and
haipipe-studio's writer (`canvas.py`) make the drawings every Block's Studio shows. This Block records how
they draw, one topic per mode, each from a drawing that was actually made, so the expensive and fragile
steps are known before the next one.

Excluded: what a Studio topic is and how its folder works (haipipe-studio); the look of a drawing
(excalidraw-report's rules).

## Pipeline

```text
a drawing made in some Block -> its steps, scripts and timings -> a Studio topic here -> a skill change
```

## Pages

No Jobs yet. Studio topics:

- s21-revise-mode-workflow: excalidraw-read's revise mode, from b04_prep_ai's s04 (SHIFT Task 3.1), 2026-10-11
