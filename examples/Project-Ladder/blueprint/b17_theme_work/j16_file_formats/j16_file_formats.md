# j16 · File formats

goal: every kind of file a Block holds has one written format, and every real file of each kind renders on its page
close: never while the workbench draws these files; each Task's check reruns after a format change

## Topic

The other half of the workbench's map from folders to pages (PRINCIPLE.md: every work folder kind has a page part, every page part draws a work folder). The page code exists; what each kind of file must hold was written in many places or nowhere, and nothing proved that every real file of a kind draws on its page. t01 writes the formats down in one table, t02 renders every real file through its page code, t03 keeps one known-good example of each kind. When a format changes, its row, its example and the check move together.

Code: `plugins/haipipe-toolkit/servers/workbench/` (the page code each row names) and the writer scripts under `plugins/haipipe-toolkit/skills/`.

## Tasks

<!-- in order; new_job.py task adds each -->
1. t01_format_table · Format table
2. t02_render_check · Render check
3. t03_example_files · Example files

