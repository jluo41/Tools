# q-executor
🧱 STAKE FORBIDDEN · this is the ONLY file that is dispatched.

Walk the tree at
/Users/jluo41/Desktop/Physician-SPACE/Tools/plugins/haipipe-toolkit
and report two inventories.

① Every directory that DIRECTLY contains a file named `SKILL.md`. Give its
   folder name and its path relative to that root.
② Every file whose path matches `agents/*-agent.md`. Give its file name and
   its path relative to that root.

Report a total for each inventory, and group ① by its parent directory.
Where a directory holding a `SKILL.md` sits inside another such directory, say
so rather than folding it silently into the parent.
Count a symbolic link once, and say which entries are symbolic links.
If either inventory is empty, say empty; do not report the nearest similar
directory instead.
Aggregate output only; no row-level record, beneficiary id or physician id.
Deliverable: two name lists, each with a count. Accepted: an exact count with
the list | empty.
