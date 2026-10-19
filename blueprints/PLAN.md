PLAN: group the blueprints Blocks into Projects
===============================================

Status: proposal, nothing moved yet (2026-10-16).
Owner Block: b10_project_workbench (it owns the Project layout).


1. What changes
---------------

Today the 13 Blocks sit flat under `blueprints/`, and the Home page treats
`blueprints` as a special "Folder" level. The plan puts each Block under a
Project, laid out like every other Project in a SPACE:

    <Project>/README.md
    <Project>/project.yaml
    <Project>/work/bNN_<block>/      (all 13 are board-kind: task-block)

The block numbers already sort into three groups, so the grouping follows them:

    before                              after
    blueprints/                         blueprints/
      b01_haipipe-toolkit                 <ProjA>/work/b01_haipipe-toolkit
      b02_haipipe-utils                   <ProjA>/work/b02_haipipe-utils
      b03_inlab-human                     <ProjA>/work/b03_inlab-human
      b10_project_workbench               <ProjB>/work/b10_project_workbench
      b11_theme_insight                   <ProjB>/work/b11_theme_insight
      b12_theme_design                    <ProjB>/work/b12_theme_design
      b13_theme_cowork                    <ProjB>/work/b13_theme_cowork
      b14_theme_discovery                 <ProjB>/work/b14_theme_discovery
      b15_theme_labeling                  <ProjB>/work/b15_theme_labeling
      b16_theme_paper                     <ProjB>/work/b16_theme_paper
      b17_theme_work                      <ProjB>/work/b17_theme_work
      b31_excalidraw                      <ProjC>/work/b31_excalidraw
      b32_draft                           <ProjC>/work/b32_draft
      _build/                             _build/   (stays)
      PLAN.md                             (removed when done)

Rules:

- **Block numbers stay.** Each bNN stays unique across all of Tools.
- **Blocks move whole.** studio/, reports/, runs/, related/, delivery/,
  goals/, HANDOFF.md and every jNN_ Job move with their Block.
- **b32_draft** could go in ProjB (it runs the Page steps the themes use).
  It goes in ProjC because, like b31, it is shared base code, not a theme.


2. Names (to pick before any move)
----------------------------------

    option   packages (b0x)     ladder (b1x)       display (b3x)
    A        ProjA-Packages     ProjB-Ladder       ProjC-Display
    B        Proj01-Toolkit     Proj10-Themes      Proj30-Display
    C        Code               Structure          Drawing

Default if no pick: option A. `<ProjA>` `<ProjB>` `<ProjC>` below mean the
picked names.


3. What points at the old paths
-------------------------------

Measured 2026-10-16 with `grep -rl "blueprints/b[0-9]"`:

    where                                         files
    Tools-SPACE (skills, servers, tests, blocks)  179
    WellDoc-SPACE (SHIFT b21, b31 studio notes)   5
    other SPACEs                                  0
    .server_config/access.yaml grants (all)       0

Most-named Blocks: b10 (135 hits), b16 (68), b12 (52), b11 (43).

Code that builds a path, not just names one (these break if missed):

- `plugins/haipipe-toolkit/servers/workbench-design/designboard.py:497`:
  `parents[4] / "blueprints" / "b12_theme_design" / "studio"`
- `plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/block_index.py:886`:
  relative fallback for Tools' own blueprints
- the Home code read by `haipipe-draft/tests/test_home.py:801-841`
  (the `blueprints` "Folder" level)
- `plugins/haipipe-toolkit/servers/_host/live/share.py:13, 468`:
  example grant and old-link rewrite naming `blueprints/b10_...`

Everything else is a path in a comment, a SKILL.md, a CHANGELOG, a studio face
or a drawing builder.


4. Steps
--------

1. **Pick names** (section 2).
2. **Check nothing is open.** No session is mid-edit in a Block; stop the
   Tools board server (5623).
3. **Make the Projects.** Each gets README.md (what it groups, its Blocks) and
   project.yaml (the same keys as a WellDoc Project).
4. **Move with git.** `git mv blueprints/bNN_x <Proj>/work/bNN_x` for all 13,
   so history follows each Block.
5. **Sweep every reference, one pass, every file type.**
   `blueprints/bNN_` becomes `blueprints/<Proj>/work/bNN_` in skills, servers,
   tests, CHANGELOGs, studio faces, history/ notes, drawing builders and the 5
   WellDoc files. Generated files (rendered PNGs, board/ sites, delivery/)
   are rebuilt by rerunning their builder, never edited.
6. **Fix the code paths** in section 3, then drop Home's special `blueprints`
   Folder case so it reads Tools like any Project -> world -> Block.
7. **Rebuild** each moved Block's s00 index (`haipipe-studio` block_index.py)
   and any drawing whose builder reads a moved path.
8. **Verify** (section 5).
9. **Delete this PLAN.md** and commit Tools; point WellDoc's Tools pointer at
   the pushed head.


5. Done when
------------

- `grep -rn "blueprints/b[0-9]"` across all SPACEs returns 0 lines.
- `test_home.py`, `test_wb_share.py` and the haipipe-studio tests pass.
- The Tools Home (5623) shows 3 Projects, 13 Blocks, and each Block opens.
- The design workbench still loads b12's studio drawings.
- `/haipipe-project audit` on each new Project reports nothing missing.


6. Cheaper fallback (not chosen)
--------------------------------

Keep the folders flat and add `blueprints/projects.yaml` that only lists
which Block belongs to which group; Home draws the groups from it. One new
file, zero path changes, but Tools stays a special case in the Home code and
the groups have no README, project.yaml or Studio of their own.
