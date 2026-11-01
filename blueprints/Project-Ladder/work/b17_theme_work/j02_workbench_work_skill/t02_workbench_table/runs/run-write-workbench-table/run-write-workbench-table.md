# run-write-workbench-table

target: workbench-table
ask: rewrite plugins/haipipe-toolkit/skills/2_theme/work/workbench-work/ref/workbench-table.md: one row per page, section, view and Run type, in table-workbench's eight columns, read from the SKILL.md as t01 rewrote it
close: render_workbench_table.py --check passes; every view the SKILL.md names has its row
