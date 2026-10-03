Shared Workbench Table
======================

Shape and check: `skills/0_utils/table-workbench/SKILL.md`. Rows run input →
process → output. `(new)` marks a skill or agent planned but not built yet.

The Shared Workbench (`servers/workbench-shared/`) is what every workbench
reuses. **Studio** has no screen of its own: its Draw, Chat and Terminal views
appear inside each workbench that draws or chats, so its Level is `any`.
**Guide** is the Shared Workbench's own site (`/w/shared`) and the Guide button
on every workbench, so its Level is `site`.

Two makers: `haipipe-studio-agent` (new) draws and chats for the Page or Board
in view; `haipipe-guide-agent` (new) writes a family's Guide. A drawing or a
table is judged by `haipipe-board-reviewer-agent`, which never made it.

| Level | Space | View | Run type | Agent | Skill | Person signs |
|---|---|---|---|---|---|---|
| any | Studio | Draw | Draw it from the page | haipipe-studio-agent (new) | haipipe-studio-draw (new) | none |
| any | Studio | Draw | Redraw on ask | haipipe-studio-agent (new) | haipipe-studio-draw (new) | none |
| any | Studio | Draw | Review the drawing | haipipe-board-reviewer-agent | haipipe-studio-draw (new) | none |
| any | Studio | Chat | Talk about the page | haipipe-studio-agent (new) | haipipe-studio-chat (new) | none |
| any | Studio | Chat | Keep the session | haipipe-studio-agent (new) | haipipe-studio-chat (new) | keep or drop |
| any | Studio | Terminal | none | none | none | none |
| site | Guide | Description | Describe the family | haipipe-guide-agent (new) | haipipe-workbench-guide (new) | none |
| site | Guide | Method | Write the method | haipipe-guide-agent (new) | haipipe-workbench-guide (new) | none |
| site | Guide | RoadMap Draw | Write the Workbench Table | haipipe-guide-agent (new) | table-workbench | the table |
| site | Guide | RoadMap Draw | Review the Workbench Table | haipipe-board-reviewer-agent | table-workbench | none |
| site | Guide | Related Paper | Add a paper | haipipe-discovery-orchestrator-agent | haipipe-discovery | the source check |

Notes
-----

- **Draw is the Excalidraw skill.** `haipipe-studio-draw` (new) collects what
  is spread today over `ref/draw.md` (lanes, owners, the style contract) and the
  prompt in `servers/workbench-shared/autodraw.py`: transparent boxes, colored
  strokes, bound labels and arrows, under 40 elements, near 900 x 600.
- **Chat and Terminal.** "Talk about the page" and "Keep the session" follow
  `ref/chat.md`; a chat may redraw the open page's scene when the person asks
  ("Redraw on ask"). The Terminal is the person's own CLI: no run.
- **Guide's RoadMap is drawn from this table.** Guide › RoadMap Draw shows each
  family's Workbench Table (Space · View · Run type · Agent · Skill); a family
  that declares none shows its skills and folders instead.
- **Person signs.** Only the person keeps or drops a chat session, accepts a
  family's Workbench Table, and checks a paper's source.
- **Not rows here.** ✨ deck authoring (`autodeck.py`) is served from this
  folder but is a run of the Page workbench's Delivery tab.
