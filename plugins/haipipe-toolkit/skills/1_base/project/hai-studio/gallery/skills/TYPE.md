# The Skills topic

Part of hai-studio's topic contract (`../../ref/topic-contract.md`). Rule: CONSTITUTION.md A08. Its Studio Type is `skills`
(`elements.md` beside this file: the requirement for every part).

A Skills topic shows the skills behind a work kind (`s51 · Skill: Work`), a related
group of level skills (`s62 · Skill: Project`), or a shared capability (`s60 · Skill: Studio`).
It holds a face and one `studio-views.json`; nothing is copied from a skill.

Levels, work kinds and capabilities describe the relationships between these topics;
they do not add UI groups. A shared skill may appear in every topic that uses it, with
the same source path each time. Put the topic's entry skill first, then its related
owners. Buttons name available capabilities, not a required process sequence.
`Skills: Knowledge` reads the existing learning skill and its evidence and practice
capabilities without changing their ownership.

```text
top     one button per skill, named by the skill          hai-work · hai-job · hai-task
left    the picked skill's whole top level, each tab the   SKILL.md · CONSTITUTION.md · ref/ · scripts/ ·
        file's or folder's own name, in this order         〈folder〉/ ... · 〈file〉 ...
right   a file: the file itself                            SKILL.md, CONSTITUTION.md, CHANGELOG.md
        a folder: one fold per file, closed; open = file   ref/, scripts/, constitution/, tests/ ...
```

1. **The names on disk, no alias.** A tab reads as the file or the folder does: `CONSTITUTION.md`, never "Rules";
   a folder carries its slash (`ref/`), so the reader knows the right side is folds; loose files are tabs of their
   own (`CHANGELOG.md`), never gathered under an invented word.
2. **A tab only for what the skill has.** No `CONSTITUTION.md`, no such tab; an empty or hidden folder, no tab.
   Other folders come after `scripts/`, in name order; caches (`__pycache__`) and hidden folders never.
3. **Files are read live; the tab list is written.** A new file in `ref/` shows as a new fold on the next open. A new
   folder or a first `CONSTITUTION.md` needs the views file written again; `--check` says when.
4. **Evaluation comes after the skills.** A top button `Evaluation`, one left tab per skill (a topic of one skill
   shows it full width): the skill measured live from its own files, one fold per criterion with its mark and what
   was found: found by its name, read in one sitting, no file too long, states the rule only, names only what
   exists, nothing unreachable, scripts tested, rules checkable, version recorded. No score, no tally; what no file
   can show (a fresh agent using the skill) is listed as a person's call. The page is the server's
   (`servers/workbench/studio/tabs/skill_evaluation.py`), so nothing is written and nothing goes stale.
5. **Its own drawing is the last button.** A topic that has `sNN-<topic>.excalidraw` gets a top button `Draw` after
   its skills: how the skills work together, or the logic of the one skill. No drawing, no button.
6. **The type shows the same.** the type's top is `〈skill〉`, its left `SKILL.md`, `CONSTITUTION.md`, `ref/`, `scripts/`, `〈folder〉/`, `〈file〉`, each
   with its requirement on the right (A06).

## The script

`scripts/skills_views.py` (in this folder) writes the views file; never write it by hand. Run with the host's Python, from the SPACE root.

```text
skills_views.py <topic> --skills <skill dir> [<skill dir> ...]    a new topic, or a changed list of skills
skills_views.py <topic>                                           write it again after a skill changed
skills_views.py <Block> --check                                   every Skills topic of the Block; exit 1 when stale
```

A skill dir is from the SPACE root (`plugins/haipipe-toolkit/skills/2_work/work/hai-work`). Order the theme's own
skills first, then the shared ones every Block type uses.

## The Checklist

`scripts/skills_checklist.py <Block or topic>` holds each Skills topic against its type and writes one line per
part of the type, the parts read from the type's own `elements.md`, at the top of the Checklist section of the topic's own face: ✅ has it, ❗ applies but is not
shown, — does not apply. The Block page's Checklist section shows it, one left tab per topic. A rerun replaces
exactly the list lines that start with a mark and one of the type's parts; other text of the section stays. No
marker comment fences them, since the page's Markdown shows a comment line as text. `--check` exits 1 when the
lines are stale or one is ❗. The lines are results computed
from the skills' folders; the Check top button (`../../ref/check-view.md`) lists the criteria and claims no result.

## The item a folder is

```json
{"name": "ref/", "folder": "plugins/<plugin>/skills/<layer>/<family>/<skill>/ref"}
```

Read by `servers/workbench/studio/tabs/studio_views.py`; drawn by `folder_folds.py` beside it. Any topic's views
file may use it, not only a Skills topic; an optional `"skip": ["<file>"]` leaves files out.
