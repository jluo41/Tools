# t02 · Rewrite workbench-work's ref/workbench-table.md
state: 🔴 OPEN
goal: workbench-work's ref/workbench-table.md holds one row per page (block, job, task), section (Report, Work, Studio), view and Run type, in table-workbench's eight columns, read from the rewritten SKILL.md
close: every view the SKILL.md names has its row (Run type none when it starts nothing); every Run type names its agent and skill; `render_workbench_table.py --check` passes; the Guide · Scope · Task · Check · Delivery rows are gone
task-type: tool

Part of j02 · Rewrite workbench-work for the work pages. It makes b17-s02's `workbench-table` piece
(`../../s02-work-skills/delivery/render.yaml`). Its Run, in `runs/`: `run-write-workbench-table`, soft, agent work;
each pass follows t01's pass for the same page, so the table never names a view the SKILL.md does not.
