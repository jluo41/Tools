# Design topics

The Design theme's topics, one section each (the repository's AGENTS.md § Report). A topic is the one thing
behind a message or a Report, not the case it showed up in. `fixed` means the case that raised it passes and
something keeps it passing (the guard); `open` names the work still owed.

```text
T01  three linked views: Folder, Element, Session   open
```

## T01 · Three linked views of a theme: Folder, Element, Session · open

- **From**: the user, relayed by the session tools-space-bc, 261117: "For the theme design, we should have three
  views. Folder Structure: how things are stored in the file system. Element Structure: how the UI presents the
  Folder Structure on the website. Session Structure: a view that records the important session history; the
  session keeps recording chat progress to the history, and shows how each session episode relates to each Folder
  and Element."
- **Questions**: which folder kinds does a design Board, Job, Task and Run hold? Which view and section shows each
  kind? Where does a design session already leave a trace, and in which folder? What in one shared Session view
  would not fit Design?
- **Answer so far** (the map sent to tools-space-bc; no code changed):
  - Folder: `haipipe-design/ref/design-ladder.md` § The tree is the whole list, Board and Method Book.
  - Element: the focus page's views, `servers/workbench-design/design_focus_layout.py` (`BLOCK_VIEWS`, `JOB_VIEWS`,
    `TASK_STEPS`), `design_focus_block.py` (`BOARD_LAYOUT`) and `design_book.py` (`BOOK_VIEWS`). The join from a
    section to its folder is in code only; nothing on disk states it.
  - Session: a Run is the episode. A soft Run keeps one round per sitting in `passes/pNN-<MMDD>/`; a hard Run keeps
    one `result/`; the card's `by:` names the agent. A face's `session:` line names the session a copied prompt
    should run in (`design_focus_parts.py` `_session`). A Studio topic keeps `passes/`. No design folder holds a
    chat transcript or a digest.
- **Does not fit**: a design Job's `inputs/` is a fence (the reasoning may read only what `manifest.yaml` lists),
  and a verify or rank must run in a context that generated nothing in the Job; an episode record written inside
  the Job must stay out of `inputs/` and must never be read by a maker or reviewer Run. A frozen folder
  (`inputs/inputs-vN/`, `observed/eNN_<exp>/`, a method's `mK.md`, a released Job) takes no new file, so its
  episodes are recorded beside it, not in it. One sitting often spans several Runs (generate, verify, revise), so
  an episode lists Runs, not one Run.
- **Owed**: the shared Session view and episode record (`servers/workbench/page`), then Design's hook: a
  folder-kind to section table read from the layout tables above, and a test that every folder kind in the tree
  has a section.
