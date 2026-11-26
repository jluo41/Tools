# Principle: how a plugin is designed

A plugin is a harness for an agent's work. It has two sides, and each side has a Folder System and a UI System.

|            | Folder System                                                       | UI System                                                     |
| ---------- | ------------------------------------------------------------------- | ------------------------------------------------------------- |
| **Work**   | a Project's Blocks, where the work is stored: `jNN`, `sNN`, `cNN`    | the workbench pages of those Blocks                           |
| **Define** | `skills/`, `servers/` and `blueprints/`: everything that defines the plugin | the workbench page of the plugin's blueprint Block, which shows its UI's definition |

Design the Work side first, then the Define side that makes it, draws it and defines it.

1. **Work Folder**: decide what folders the work is stored in. Each Block holds three kinds of numbered folders,
   side by side.
   - `jNN` Job: the work, Job ▶ Task ▶ Run ▶ Result.
   - `sNN` Studio: a topic thought through and drawn.
   - `cNN` Chat: one chat session, numbered in time order, naming the folders it changed.
2. **Work UI**: decide how a page shows those folders; it shows nothing that is not on disk.
3. **Define Folder**: the folders that define the plugin.
   - `skills/`: what an agent knows how to do (`SKILL.md`, `ref/`, `scripts/`, `tests/`, agents), and the contract of
     each work folder kind. A skill folder holds no `jNN`, `sNN` or `cNN`.
   - `servers/`: the page code that draws the Work UI. Code is folders too.
   - `blueprints/`: the Projects that plan Tools. A plugin's blueprint Block is a Block like any other, with its own
     `jNN`, `sNN` and `cNN`, plus `ui/` (each level's views and buttons) and the example Blocks its `board.md` names.
4. **Define UI**: the workbench page of the blueprint Block (`/wb blueprints/<Project>/work/bNN_<theme>/`): each
   level's views and buttons as the `ui/` files define them, each linked to an example Block drawn by the real page
   code, so the definition and the pages cannot drift apart.
5. **The map**: every work folder kind has a page part, every page part draws a work folder.
   - Folder, Element and Session views each reach the other two.
6. **The rule**: on the Define side, a change lands everywhere at once: a new or changed work folder kind ships with
   its skill contract, its page code, its definition in the blueprint Block, and a test that it is drawn.

How a plugin works:

- **Using it**: the skills write the Work Folder, through their gates and checks; the page code reads those folders
  each time a page opens, so the Work UI follows them and keeps no copy.
- **Changing it**: the change is worked in the blueprint Block and seen on its page, the Define UI; the skills and the
  page code change with it. Work already on disk is read by the new code, or carried over by a script.
