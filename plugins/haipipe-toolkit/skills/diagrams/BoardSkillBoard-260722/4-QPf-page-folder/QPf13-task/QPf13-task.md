# Task · the page's citations into the repo's task folders
state: 🟡 PARTIAL · shipped and proven on its own specimen 260818 · open: the 🗂 tab itself
owner: JL
method: give a page a ranked list of TASK FOLDERS it is written about, and materialize each row as a symlink to the whole folder, with live status read from plan.yaml / report.yaml / QA/*.md

## Opening
Which `tasks/` folder actually backs a page's argument, and does that link still point at the right place next month?
A page argues something; the run that produced the number often sits three folders away, under a name nobody remembers by the time the page is reread.
This page decides the answer: the page keeps a short ranked list of task folders, and a symlink plus a live status badge are built from that list.

Writing the path in prose goes stale the moment a task folder moves, and it says nothing about whether that folder was ever reported.

**Its three cousins**: `bibex` lists the papers a page cites, `skill` lists the skills it leans on, `pagex` lists the files it borrows from other PAGES, and this one lists the FOLDERS it is written about under some project's `tasks/` tree.
The one rule that flips: pagex refuses a folder, because linking a page's whole home would hand board discovery a ghost page; task refuses a FILE, because a task folder is never itself a page, and linking half of one means nothing.

**Not a substitute for `page-type: task`**: `haipipe-page-for-task` (`examples/.../QC1-visitlbp.md` is a real instance) is a whole PAGE dedicated to ONE task folder, named by a `task-folder:` header field, built to READ that folder's results into Data/Method/Result/Meaning divisions. This plugin is the opposite case: a page that is NOT itself about reading one task folder's results, but leans on one or several as supporting material, the way a design page cites a task folder in passing. A page already wearing `page-type: task` never needs this plugin too; its header field already names the one folder it is about, and QC1-visitlbp was checked against this plugin on 260818 and found to be exactly that case, so it stayed untouched.

**Covered elsewhere**: the list of plugin names is `../../haipipe-plugin/ref/roster.md`. `QPf11` is the cousin whose store grammar and drag-to-rank this copies. `haipipe-task`, the skill family that plans, builds, executes and reports the folders this page links, owns what those folders mean; this page only reads their shape off disk. `../../../../task/page-types/haipipe-page-for-task/SKILL.md` is the whole-page variant this section rules against.

## Diagram
**The task store and its one shadow**: the ranked list a person keeps, and the symlink-plus-status a refresh re-mints from it.
```text
  🗂 examples/Project-X/tasks/A01_group/B02_unit/
        │   pick the WHOLE FOLDER, never a file inside it
        ▼
  🗃 task/<stem>.md          PRIMARY · one row per linked task folder
        🏷 row       <repo-relative path> · note: why it is wanted
        🥇 order     the person's rank, top first
        ✕ removed    a tombstone the refresh never re-seeds
        │
        ▼ refresh re-mints, from the store ONLY
  ⚙️ task/<project>/<inner path>/   DERIVED · a relative symlink to the folder
  ⚙️ task/<stem>-view.html          DERIVED · the 🗂 card view, status per row
```
The list is the truth; the symlink and the status badge are shadows re-minted from it, read fresh off `plan.yaml` / `report.yaml` / `QA/*.md` every time.

## Content
### 1 · What you keep, and what gets rebuilt
**Two files, one yours**: the ranked list is written by hand or the ＋ pen; the symlink and the status view are rebuilt from it.
```text
  🗃 PRIMARY   task/<stem>.md              rows · order · tombstones · committed
  ⚙️ DERIVED   task/<project>/<inner>/     a relative symlink · re-minted
  ⚙️ DERIVED   task/<stem>-view.html       the 🗂 card view · re-minted
  ⚖️ the rule  a refresh writes the derived half and never the store
```
📌 One file in this folder is yours to write; everything beside it is rebuilt from that file and may be overwritten.

A rebuild deletes only symlinks it made itself, then makes them again from the list: the same safety rule pagex proved on this same board.
The link's name keeps the path from the folder's nearest `tasks/` ancestor down (`task/Project-X/A01_group/B02_unit/`), so two folders from different groups never collide on a bare basename.

### 2 · Which paths a line may point at
**The check every rebuild runs**: what a line may reach, and what a refusal has to show you.
```text
  ✅ allowed   a directory somewhere under a `tasks/` tree, any project
  🚫 refused   a target resolving outside the repo root
  🚫 refused   a FILE, not a folder: task links whole task folders only
  🚫 refused   no `tasks` segment in the resolved path
  🚫 refused   a target inside this page's own task/ · a link of the link
  🔗 written   relative links, so a clone or a move stays portable
  📣 shown     a refused row keeps its reason on its card
```
📌 A line may point at any task folder in the repo; anything that is not one folder under a `tasks/` tree is refused, and the refusal says why.

Requiring a `tasks` path segment is the one guard this plugin adds that pagex has no need of: a page's home folder is unambiguous (`<name>/<name>.md` exists or it does not), but a plain directory has no such marker, and a wrong path linked by accident would otherwise mint silently and mean nothing.

### 3 · Status, read from the files, never a claim
**The badge is computed, not typed**: the same rule `plugview.py` already uses for display and probe.
```text
  ✅ reported   workflow/report.yaml (or a bare report.yaml) exists
                best-effort detail: the `# O: status=X` preview comment,
                shown, never load-bearing
  📝 planned    plan.yaml exists, report.yaml does not
  ❔ unknown    neither file found under workflow/ or the folder root
```
📌 A task folder's badge is read off its own files on every rebuild, so a report written five minutes ago shows up without anyone touching this page.

Each card also shows `plan.yaml` ✅/⬜, `report.yaml` ✅/⬜, a `QA/*.md` count, and the newest file's age, the same four facts a person would check by hand before trusting a linked folder.

### 4 · No auto-seed, and why
**Every row is typed on purpose**: unlike pagex, nothing here fills the list for you.
```text
  📄 a page id    matches a pattern a scanner can find: Q<letter><n>, S-<Family>-<unit>
  📁 a task path   examples/Project-X/tasks/A01_group/B02_unit, no such pattern
  ⛔ the result    a scan cannot tell "this page mentions a task" from prose
                    that happens to contain the word "task"
```
📌 A task-folder path does not look like anything a prose scanner could reliably lift, so the ＋ pen is the only door, and a refresh only mints what the store already holds.

## Aims
### A1 · 📐 What you keep, and what gets rebuilt
- ✅ A1.1 · A rebuild never touches the list you wrote.
  **Done when:** Running a rebuild over a hand-written list leaves it exactly as it was.
  **Now:** Reordering and a plain refresh over the one-row store left `task/QPf13-task.md` byte-for-byte the same; `_task_write` only ever rewrites from `st["rows"]`/`st["order"]`, the same shape pagex's own writer proved byte-stable.
- 🔨 A1.2 · You can edit the list from the tab: link, remove, put back, and reorder.
  **Done when:** All four actions work from the tab, and nothing outside the tab writes the list.
  **Now:** `task-entry` linked the real specimen, then refused it as a file when pointed at `.../workflow/report.yaml`, then removed it as a tombstone (`· removed`, kept, never deleted): all three proven directly over HTTP. The drag route (`task-order`) is coded the same as pagex's own proven route, and none of the four (link, note, remove, reorder) has been driven from the rendered 🗂 tab itself in a browser; this machine has no Chrome extension attached.


### A2 · 🌍 Which paths a line may point at
- ✅ A2.1 · A rebuild makes symlinks from the list only, and deletes nothing it did not make.
  **Done when:** It creates one symlink per live row and leaves every other file alone.
  **Now:** `_task_mint` built exactly one symlink, `task/Project-Personality-OpioidRx/R01_Reg_TraitOpioid/D01-reg_visitlbp_1stpair`, a relative link that `ls -la` resolves straight through to the real folder's contents; nothing else in `task/` moved.
- ✅ A2.2 · A file, a folder outside the repo, and a folder with no `tasks` ancestor are each refused, with the reason on the card.
  **Done when:** All three refusals happen on a test line and each shows its reason.
  **Now:** Both refusals fired on real rows: a file (`.../workflow/report.yaml`) refused at the pen, before a symlink was ever attempted; `examples/Project-Personality-OpioidRx` (a directory with no `tasks` segment in ITS OWN path) refused at mint, with `⛔ refused · no 'tasks' segment in the path` on its card.


### A3 · 🩺 Status, read from the files, never a claim
- ✅ A3.1 · A card's badge reflects `plan.yaml` / `report.yaml` / `QA/` as they stand today, not as they stood when the row was added.
  **Done when:** Editing a linked folder's `report.yaml` and rebuilding changes the badge without touching the store.
  **Now:** The linked specimen's card reads `✅ reported · warn` (the real `# O: status=warn` line from its `report.yaml`), `✅ plan.yaml`, `✅ report.yaml`, `0 QA files`, `40d ago`, all four read fresh off disk by `_task_status`, not typed into the store.


### A4 · 🔍 No auto-seed, and why
- ✅ A4.1 · A refresh with an empty store mints nothing and refuses nothing, because there is nothing to seed.
  **Done when:** An empty `task/<stem>.md` rebuilds to an empty card list with no error.
  **Now:** `task_refresh` calls `_task_mint` and `_task_view` with no seed step; an empty store mints an empty list by construction, since the loop over `st["order"]` has nothing to iterate.


## Discussion

### From the retired States section (merged 260831)
This page is the plugin's first user, and it links its own worked specimen: `examples/Project-Personality-OpioidRx/tasks/R01_Reg_TraitOpioid/D01-reg_visitlbp_1stpair`.
### 🗣 Decision Now
- [ ] 🗣 Should `task_refresh` gain a soft seed from this page's own `## Files` section, the way pagex seeds from page-id mentions?
      📍 `Content` §4
      🔔 `Why now` §4 argues no scan is possible for a task path in general prose, but this page's own `## Files` section already lists real repo paths in a fairly regular shape, which is a narrower, more matchable case than free prose
      ⭐ `A ·` stay pen-only. `## Files` mixes engines, contracts, and task folders with no tag telling them apart, so a seed would need a second convention before it could tell one from another.
      `B ·` seed from `## Files` rows that resolve to a directory containing `workflow/` or a bare `plan.yaml`/`report.yaml`: a shape check, not a path-string guess.
      🛑 `Blocks` nothing; the ＋ pen already reaches any task folder today.
      🤖 `If nobody answers` A. That is what shipped.

## Files
### ⚙️ Engines
- `../../haipipe-board/live/task.py`
  The whole plugin: the store reader and writer, the directory minter and its vet, the status reader, the two POST doors beyond refresh, and the card view.
- `../../haipipe-board/assets/js/10-drawer/86-plugin-task.js`
  The registry entry whose `tab` spec the shell builds the 🗂 tab from.
- `../../haipipe-board/live/pagex.py`
  The sibling this plugin's store grammar, drag route, and view shape were copied from, then inverted on the file-vs-folder rule.
- `../../haipipe-board/live/plugview.py`
  Where `_display_state` set the precedent this page's status reader follows: compute from files, never trust a typed word.

### 📋 Contracts
- `../../haipipe-plugin/ref/roster.md`
  The one list of plugin names; the `task/` row there is what this page rules.
- `../../page-plugins/haipipe-plugin-task/SKILL.md`
  The plugin's own delta-only skill, shipped with the row the same round.
- `../../../../task/page-types/haipipe-page-for-task/SKILL.md`
  The whole-page `page-type: task` variant this page's Opening rules against; a page wearing that type never needs this plugin too.

### 🧪 Checks
- `examples/Project-Personality-OpioidRx/tasks/R01_Reg_TraitOpioid/D01-reg_visitlbp_1stpair/workflow/report.yaml`
  The real file the status reader was written against: `workflow/report.yaml` present, a `# O: status=warn ...` preview comment read as the best-effort hint.

## Law
- 🏷 The name is `task/`, pagex's fourth twin (JL 260818).
- 📁 Task links FOLDERS, never files: the inverse of pagex's own rule, because a task folder is never itself a page and linking one file from it would answer the wrong question.
- 🧭 A path with no `tasks` ancestor is refused at mint time: the one vet pagex has no need of, because a task folder carries no `<name>/<name>.md` marker the way a page home does.
- ✂️ No scan-seed: a task-folder path is not a page id, so nothing here reads this page's own prose for candidates; every row is the ＋ pen.
- 🩺 Status is read from `plan.yaml` / `report.yaml` / `QA/*.md` on every rebuild, never stored as a word a person typed.

## Log
- 🚢 260831 1300 · [HAIPIPE-PAGE-SKILL] the lane gains its first ranked CONSUMER CONTRACT: `task/10_page/haipipe-task-for-page` 0.1.0 (JL ruling, this date).
      One collection job per Board Page answers the page's task-route probe cards with code — values.yaml + QA digests, `state: owed` + workflow/proposals.md for a value with no upstream — and the roster's `task/` row now says that job ranks FIRST in this lane when one exists. The card address `PP<NN>.v<n>` and this plugin's three POST doors are untouched. Registered the same day in haipipe-task 0.10.0, haipipe-page 0.44.0, plugin-chat 0.3.0, page-probe 0.12.0, page-evidence 0.13.0.
- 🩺 260818 · [BUILD-CC] checked against `QC1-visitlbp` (`examples/Project-Personality-OpioidRx/diagram/02-CMSRegBoard-260725/3-QC-our-regressions/QC1-visitlbp`), JL's proposed rollout candidate.
      That page already declares `page-type: task` and `task-folder: .../D01-reg_visitlbp_1stpair` in its own header, the pre-existing `haipipe-page-for-task` v0.5.0 mechanism this page had never named. Attaching this plugin there would duplicate the same one folder the header already names, so it was left alone; the Opening and Files sections above now name the boundary so the next rollout candidate can be checked against it without a fresh investigation.
- 🧪 260818 · [BUILD-CC] proven against a real task folder and a running server, not just read.
      An isolated verification server (`--root` the whole SPACE, a throwaway port, never the port JL's own session was attached to) exercised all three POST doors directly: `task-entry` linked `examples/Project-Personality-OpioidRx/tasks/R01_Reg_TraitOpioid/D01-reg_visitlbp_1stpair`, `task` minted it and rendered the card, and the two refusal paths (a file, a `tasks`-less directory) both fired with their stated reasons on real rows.
      `ls -la` on the minted symlink followed it straight through to the real folder's contents, proving the relative-path math, not just that a link exists.
      The status badge read `✅ reported · warn`, matching that folder's actual `report.yaml`; the test rows were then cleaned up (the file-refusal never minted anything to clean, the directory-refusal was tombstoned with `remove`, never deleted, per this plugin's own rule).
      What is NOT proven: the tab itself, end to end, through a browser. This machine has no Chrome extension attached (`tabs_context_mcp` refused, `Mac Studio` per `project-mac-studio-ssh-port-forward` memory), so the click path from the 🗂 tab to these same routes is unexercised; the routes themselves are.
- 🚢 260818 · [DRAFT-CC, JL ruled] page born from JL's ask on the QPf plugin board ("task: what task folder is associated with this page"), asked in the same breath as `meeting` (`QPf14`).
      Two shapes were offered for task: a plain ranked reference list, or the same list with live status pulled in; JL chose the live-status form ("I think here we want the same like pagex, and we use the symlink, and then create the html to show their status").
      `live/task.py` shipped whole the same round: store, directory minter with its `tasks`-ancestor vet, the status reader built and checked by hand against three real `report.yaml` files in `examples/Project-Personality-OpioidRx/`, the two POST doors beyond refresh, and the card view.

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0