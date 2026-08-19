# q-executor
🧱 STAKE FORBIDDEN · this is the ONLY file that is dispatched.

Walk the folder at
/Users/jluo41/Desktop/Physician-SPACE/Tools/plugins/haipipe-toolkit/skills/diagrams/BoardSkillBoard-260722/4-QPf-page-folder/QPf11-pagex/pagex/

Report every symbolic link under it, at any depth:
① the link's own path, relative to that folder
② its raw target string exactly as stored, NOT the resolved path
③ how many leading `../` steps that raw target uses
④ whether the target resolves to a file that exists on disk

Give the total number of symbolic links. Count only symbolic links; a regular
file is not one, and neither is a directory.
If the folder holds no symbolic link, say none; do not report the regular files
instead.
Aggregate output only; no row-level record, beneficiary id or physician id.
Deliverable: one row per link with its raw target, its step count and whether it
resolves, plus the total. Accepted: an exact count with the list | none.
