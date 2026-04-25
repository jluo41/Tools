Function: inventory
====================

Build or refresh the visual catalog for a haipipe project.

One rule:

  **Every task folder under  tasks/  contains exactly one
   build_inventory.py + {folder_name}.excalidraw + {folder_name}.png.**

  The figure filename matches the folder name — e.g. A_pretraining_clm/ contains
  A_pretraining_clm.{excalidraw,png}.  This makes  find -name "*.png"  produce
  unambiguous results across the whole project.

The folder name is the figure's identity — no separate "inventory/" dir at the
project root.  Data inventory lives in  tasks/0_data/  like any other task.
Rendering calls the shared excalidraw-diagram-skill; no parallel template.


Convention
----------

  tasks/
    ├── 0_data/                       <- foundational inputs (datasets, splits)
    │   ├── README.md
    │   ├── build_inventory.py
    │   └── {folder_name}.{excalidraw,png}
    ├── A_pretraining_clm/            <- 1:1 with this folder
    │   ├── README.md
    │   ├── A1_train_clm_num_modelsize/
    │   ├── ...
    │   ├── build_inventory.py
    │   └── {folder_name}.{excalidraw,png}
    ├── A_pretraining_mlm/
    │   └── {folder_name}.{excalidraw,png}    (mostly blank — planned)
    ├── B_evaluation_clm/
    │   └── {folder_name}.{excalidraw,png}
    └── ...

Rules:
  * One {folder_name}.excalidraw per task folder.  Multi-panel composition
    happens inside the one file (e.g. NUM + TKN + MC panels in pretrain_clm).
  * Use  HERE.name  to derive the output filename so renaming the folder
    automatically renames the figure.
  * `tasks/0_data/` holds cross-cutting data catalogues — datasets, splits —
    that no other task owns.  Sorts first alphabetically by design.
  * No special top-level `inventory/` folder — everything lives under `tasks/`.


Shared tooling (in this skill)
-------------------------------

  ref/inventory/helpers.py     <- Python primitives: Grid, Table, mk_title,
                                  mk_legend, mk_timestamp, write_excalidraw.
                                  Colour palette matches the existing
                                  plot_training_grid style (green ✓ / orange ?
                                  / yellow … / blank).

  ref/inventory/render.py      <- thin wrapper that invokes
                                  Tools/plugins/excalidraw-diagram-skill/
                                  references/render_excalidraw.py per file.
                                  No parallel CDN / template.


Execution protocol
-------------------

Step 0: Auto-detect PROJECT_PATH per SKILL.md rules.  Confirm to user.

Step 1: Decide scope.
  If cwd is a specific task folder (or --path is one):
    scope = single task folder.
  Else:
    scope = whole project → every  tasks/*/  directory.

Step 2: For each in-scope task folder:
  * If  build_inventory.py  exists: run it (it emits  {folder_name}.excalidraw
    in the same folder).
  * Else: skip and report "no builder" so user can decide whether to add one.

Step 3: Render every emitted .excalidraw via
  python Tools/plugins/haipipe/skills/haipipe-project/ref/inventory/render.py \
         --all tasks/

Step 4: Refresh  tasks/README.md  with a table that lists every task folder and
  embeds its  {folder_name}.png  inline.  Fence the auto-generated block:
    <!-- BEGIN haipipe-project inventory index -->
    ...
    <!-- END haipipe-project inventory index -->

Step 5: Report to user:
  * Files built (paths).
  * Task folders without a builder — flag as candidates for the user to address.
  * Render failures (if any).


How to write a  build_inventory.py  (task-folder template)
------------------------------------------------------------

Minimal pattern (see  examples/ProjC-Model-1-ScalingLaw/tasks/*/build_inventory.py
for concrete examples):

  import sys
  from pathlib import Path

  SKILL = Path("/home/jluo41/WellDoc-SPACE/Tools/plugins/haipipe/skills/haipipe-project/ref/inventory")
  sys.path.insert(0, str(SKILL))
  from helpers import Grid, mk_title, mk_legend, mk_timestamp, write_excalidraw

  HERE = Path(__file__).parent

  # 1. Collect status per (config × size) by scanning _WorkSpace/ or CSVs.
  row_labels = [...]          # e.g. training configs for this folder
  col_labels = [...]          # e.g. model sizes
  status = [[...]]            # "done" | "gap" | "in_progress" | "blank"

  # 2. Compose the figure.
  elems = []
  elems += mk_title(x=40, y=30, w=900, text="<folder name> — inventory",
                    subtitle="status as of build time")

  grid = Grid(row_labels=row_labels, col_labels=col_labels, status=status,
              phase1_row_idx=... or None)
  elems += grid.draw(x0=40, y0=100)

  gw, gh = grid.size()
  elems += mk_legend(x=40, y=100 + gh + 30)
  elems += mk_timestamp(x=40 + gw - 280, y=30)

  # 3. Save.
  write_excalidraw(HERE / f"{HERE.name}.excalidraw", elems)


Never modify  helpers.py  on a per-folder basis — extend it centrally in the
skill so every task folder benefits.
