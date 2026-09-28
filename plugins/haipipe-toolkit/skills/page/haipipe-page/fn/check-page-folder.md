---
name: haipipe-page-check-page-folder
description: >-
  Check whether one Page Folder, or every Page in a Board or group folder, is on
  the latest Page layout this skill ships, and name the command that brings each
  one there. Read-only.
argument-hint: "<page-folder | board-folder>..."
allowed-tools: Bash, Read
---

# check-page-folder · is this Page Folder on the latest layout?

Use `/haipipe-page check-page-folder <target>` when the person asks whether a
Page, a Board, or a group of Tasks follows the current skill, or before and
after a layout migration. It is read-only.

```bash
python3 <toolkit>/skills/page/haipipe-page/cli/page.py check-page-folder <page-folder | board-folder>... [--json]
```

A Page Folder is any folder `<name>/` holding `<name>.md`. A Board or group
folder is searched for every Page inside it (`_archive/` and `previous/` are
skipped). Exit 1 when any Page is behind.

## Three different checks

| Command | Question it answers |
|---|---|
| `check-page-folder` | Does the Folder follow the layout the skill ships today? |
| `health` | Does the Folder agree with itself (one plan, Drafts on the Page, Evidence ids, delivery age)? |
| `/haipipe-page-check` | Is one built Page version good enough to close? (Page CHECK, judges prose) |

## Rules (layout 0.118)

Each rule names the skill version that introduced it; `·` means it does not
apply yet (for example, no plan written).

| Rule | Since | Fix |
|---|---|---|
| plan folder is `draft/` (`·` when a Task has no plan folder yet; it appears with the first plan or record) | 0.118 | `page.py draft-layout <page>` |
| one current plan | 0.117 | `page.py draft-layout <page>` |
| plan named `<stem>-draft-v<G>.<S>.md` | 0.118 | `page.py draft-layout <page>` |
| plan in three sections (`## 1 Structure`, `## 2 Scratch`, `## 3 Draft`) | 0.118 | `page.py draft-layout <page>`; a plan with no `- B<k> ·` Bullets is written as Bullets first (OUTLINE work) |
| `### Structure Overview` present | 0.118 | `page.py draft-layout <page>` |
| process records in `draft/records/` | 0.117 | `page.py draft-layout <page>` |
| Evidence Markdown grouped (`## Citations`, `## Displays`, `## Values`) | 0.118 | `page.py draft-layout <page>`; an item of another kind is retyped first (EVIDENCE work) |
| Page runs (`rp-`, `re-`, `rd`) sorted into Space folders; Task Runs `rNN_` and Design Run tickets `rdNN_<commission\|generate\|verify\|adopt\|revise\|reject>_*` stay flat | 0.118 | `page.py draft-layout <page> --sort-runs` |
| `results/<run>/` flat by run name | 0.118 | move `results/<space>/<run>/` up |
| no links the Page server refuses | 0.118 | replace the link with the real folder |
| no `outline/` paths in the Page's own files, Python `/ "outline"` joins included ("outline/content" prose is not a path) | 0.118 | `page.py draft-layout <board>` (links between Pages need the Board run) |
| retired Outline evidence archived (`evidence/<lane>` except the live `bibex` and `materials`, plus `<stem>-evidence.md` and a root `pagex/`) | 0.117 | `page.py draft-layout <page> --archive-evidence` |
| no script reads retired evidence (code in the Project that names `evidence/<lane>`, `-evidence.md` or `pagex/` for a retired item) | 0.118 | EVIDENCE work: point the script at the Evidence Markdown or a Result, then `--archive-evidence` |
| display units are DISPLAY Results (each `evidence/display/<unit>/` has `results/<re-run>/payload/<unit>/`) | 0.117 | EVIDENCE work: make the DISPLAY Result, then `--archive-evidence` |

`src/layout_check.py` holds these rules and `LAYOUT_VERSION`. When the Page
layout changes, add its rule there in the same commit: that list is what
"latest" means.

## Fix

One command brings a Page, a Board or a Task tree to the latest layout:
`page.py draft-layout <page | board | tasks-dir> --sort-runs`. Preview it with
`--dry-run` (it counts the path rewrites too). Run it on the Board, not Page by
Page, so links between Pages (`../Other/outline/...`) are rewritten. Then
rebuild generated views that cite the old paths (`board/`, `delivery/`) and run
`check-page-folder` again. The printed fix commands use paths relative to where
you ran the check.

Retired Outline evidence (`draft/evidence/<lane>` except `bibex` and
`materials`, and `draft/<stem>-evidence.md`) moves with `--archive-evidence`:
the lanes go to `draft/_archive/legacy-outline-evidence/`, every path citing
them inside the Page follows (LaTeX `\\input` and `\\includegraphics` too), and
relative symlinks inside a moved lane keep pointing at the same file. An item
that code elsewhere in the Project still reads (a paper builder joining
`page / "draft" / f"{stem}-evidence.md"`) stays live, and the Page is reported
behind on "no script reads retired evidence". The pre-0.117 binding lane
`pagex/` at the Page root moves there too: its links become copies of what they
named, because the Page server refuses links, and a dead link is listed as
`links_dropped`. Rebuild that Page's delivery afterwards.

The plan rewrite keeps every line: a line that is neither a heading nor a
Bullet (a `%%` note, `- Note: ...`, a `### Cut` block) moves to section 2 under
its paragraph or division, and the run refuses if any line would still be lost.
Bullets written straight under `## C<n>` sit in paragraph `### C<n>.P1`, as
every reader already numbers them. A 0.117 `## Scratch` registry becomes the
section-2 note blocks (Run marker, notes, `> Summary:`); its time fields stay in
the Scratch Run's ticket and Result.
A legacy integer plan `vN` counts as `v0.N`, so it becomes `v0.<N+1>`; an old
`✅` rides along and only a person promotes it to `v1.0`.

Four cases stay behind on purpose, because the fix is Evidence or Outline work
rather than a folder move. A plan with no `- B<k> ·` Bullets (a plan written as
a table, for example) is left as it is. A `display/` lane stays while any unit
in it has no DISPLAY Result (`results/<re-run>/payload/<unit>/`): the paper
delivery still reads the lane by convention. An Evidence item typed outside
CITE, DISPLAY and VALUE (for example `E09-SCHEMA-...`) leaves its Evidence
Markdown ungrouped. A retired item a script still reads stays live. In a Board or
Task tree run, a Page that refuses is reported as `refused` and the other Pages
still move.

## In any SPACE

Every SPACE whose `Tools` points at the same toolkit has these commands. From
the SPACE root:

```bash
page() { .venv/bin/python Tools/plugins/haipipe-toolkit/skills/page/haipipe-page/cli/page.py "$@"; }   # bash and zsh
for d in examples*; do page check-page-folder "$d"; done   # every Page in the SPACE: latest or behind
page draft-layout <root> --sort-runs --archive-evidence --dry-run   # <root> = a Board, a paper, or tasks/
page draft-layout <root> --sort-runs --archive-evidence
page check-page-folder <root>                        # behind only where Evidence work is left
```

Work one git repo at a time (each Project is its own repo): back up its folder,
record `health` and the task-tree check before, migrate, compare after, rebuild
its boards (`haipipe-board/cli/build.py <board>`), then commit that repo.
Several repos can run in parallel, one subagent each, followed by one read-only
reviewer (`haipipe-task-reviewer-agent` for Tasks). Skip a folder another
session changed in the last hour, and a Project whose git status holds someone
else's uncommitted work (staged renames, untracked Pages): migrate it after that
work is committed. `results/` is never edited: a Result keeps its words.

## Report

Say the verdict first: how many Pages are on the latest layout and how many
are behind. Then list each behind Page with its failing rules and the fix
command. Do not run the fix unless the person asked for the migration.
