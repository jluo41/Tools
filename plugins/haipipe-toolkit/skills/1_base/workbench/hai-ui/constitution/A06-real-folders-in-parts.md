# A06 · Files groups real paths by their role in the Block

The Files pane presents the owning Block's records and the real paths related to its work. One shared renderer
supplies the pane for every theme. Selecting a Job or Task keeps that Block as the owner and opens the path to
that selected record inside its Block folder.

## Parts

| Part | Content |
| --- | --- |
| Block | The owning Block's files and folders. |
| Maintain: ServerUI | The server code and page specifications that draw this Block's page. |
| Maintain: Skills | The skills that own this Block's page. |
| Maintain: Block-Example | The example Blocks this Block declares (`examples:`); it changes them as its design changes. |
| Maintain: Blueprint Blocks | For a blueprint Block: the other Blocks of its `blueprint/` folder that its traces planned or changed, one row per Block. |
| Maintain: OneDrive | The shared folders this Block declares (`onedrive:`). |
| Read-From | What this Block does not change: the Blocks it waits for (`waits-for:`) and each data store its `## Data` list places in a SPACE folder (`where:`). |
| Touch | Paths a relevant trace names outside the preceding parts. |

A part appears only when it has content. Its heading names the relationship, not a directory. A part appears
once, with its folders as rows. A Maintain part and Read-From open with one path relative to the SPACE: the folder
all their rows share; a row that sits deeper is named by its path below it (`cowork/b01_example_cowork`). Touch opens
each folder with its own path and shows every touched file inside its real folders below it, opened down to the
file; a run of folders that each hold one folder is written on one row, and a file still to create keeps one row
by its path. `./` means the SPACE root. Children retain their real names and nesting. A planned file that is not on
disk is shown with its creation mark through the trace layer.

## Identity and navigation

Folders inside each Maintain part and Read-From, and parent-path groups inside Touch, have display numbers
starting at one within that part ("Skills 3"). These numbers reflect the displayed order. They are not persistent addresses, record IDs or
keys for comments and traces. Source paths and authored record identities identify the targets.

Opening a row uses its source path. Reordering rows can change a display number while the folder's open target,
linked work and trace association remain the same. Job and Studio navigation must retain the owning Block.

## Checks

- The pane contains one Block part and only applicable `Maintain: <kind>`, Read-From and Touch parts, each once.
- Each part shows its SPACE-relative parent paths and source-backed rows.
- Folder paths resolve to directories inside the SPACE; role headings never masquerade as folder rows.
- Each part's display numbering starts at one and follows its rows or parent-path groups.
- Reordering role rows changes display positions while preserving source paths and open targets.
- Nested folders expand, file previews open, and long names remain readable at narrow widths.
- Clicking a Job or Studio reference retains the owning Block; verify this separately from folder-path checks.

`hai-ui/scripts/folder_icons_check.py --url <origin>` checks the rendered pane's roles, paths and numbering.
`servers/workbench/side_pane/files_tree/tests/test_role_parts.py` checks row ordering, path identity and linked work;
`servers/workbench/page/job_task_views/tests/test_work_frame.py` checks the Block and selected-record panes.
