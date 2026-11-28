# Requirements of a Skills topic

The class of every Skills topic in the Skills band, covering a work kind, related level skills or a shared capability: the same top buttons and left tabs as an
instance, each with the requirement an instance must meet there. `## ` is a top button, `### ` a left tab under it.
The type's own right side shows the requirement (type_requirements.py builds the pages); an instance's right side
shows the real skill file, read live. A left tab carries the file's or the folder's own name, a folder with its
slash. A name every instance fills in is written in 〈 〉: the skill on top, a skill's other folders and its loose
files on the left.

instances: article[id^="s5"],article[id="s60-skill-studio"],article[id="s61-skill-trace"],article[id="s62-skills-ladder"],article[id="s63-skill-draw"],article[id="s55-skills-knowledge"]

## 〈skill〉
what: One skill the topic covers; its button is the skill's name.
why: A reader first picks which skill to read, then what in it.
from: `plugins/〈plugin〉/skills/〈layer〉/〈family〉/〈skill〉/`

### SKILL.md
what: The skill's `SKILL.md`, the file an agent reads first.
why: The skill's own words are the contract; a copy would drift from it.
from: `〈skill〉/SKILL.md`, read live on every open
must:
- one top button per skill the topic covers, named by the skill (`hai-work`), nothing added to the name
- the theme's own skills first, then the shared ones every Block type uses
- `SKILL.md` is the first left tab of every skill
- every left tab reads as the file or folder does on disk, never an alias
- the file itself, never a copy or an excerpt
check: every top button's first tab is `SKILL.md` and its path ends in `/SKILL.md`

### CONSTITUTION.md
what: The skill's `CONSTITUTION.md`: the rules feedback made, which win over the skill's other files.
when: the skill has a `CONSTITUTION.md`
why: A rule is read before a page or a skill is changed, so it sits beside the skill it governs.
from: `〈skill〉/CONSTITUTION.md`
must:
- the second left tab, only for a skill that has a `CONSTITUTION.md`
- a skill without one has no such tab, never an empty one
check: every skill that has a `CONSTITUTION.md` has this tab

### ref/
what: The skill's reference files, one fold each; an opened fold shows the file.
when: the skill has a `ref/` that holds a file
why: The left stays as short as the skill's top level; the folds list what the folder holds before any is read.
from: the files directly in `〈skill〉/ref/`, read live
must:
- the tab ends in a slash, as every folder does
- one fold per file, named by the file, in name order, all closed at first
- an opened fold shows the file itself
- no `ref/` tab when the skill has no `ref/` or it holds no file
check: the tab names the skill's own `ref/` folder

### scripts/
what: The skill's scripts, one fold each: what makes and checks the things the skill owns.
when: the skill has a `scripts/` that holds a file
why: A rule holds only while a script keeps it; the reader goes from the rule to the code that enforces it.
from: the files directly in `〈skill〉/scripts/`, read live
must:
- one fold per script, named by the file (`new_topic.py`), in name order, all closed at first
- no `scripts/` tab when the skill has no `scripts/` or it holds no file
check: the tab names the skill's own `scripts/` folder

### 〈folder〉/
what: Any other folder of the skill (`constitution/`, `fn/`, `agents/`, `tests/`, `cli/`, `feedback/`), one fold per file.
why: The left is the skill's whole top level, so nothing the skill holds is out of sight.
from: every other folder directly in `〈skill〉/`, read live
must:
- one left tab per folder, named by the folder with its slash, after `scripts/`, in name order
- one fold per file directly in it, all closed at first
- no tab for a hidden folder, a cache (`__pycache__`) or a folder that holds no file
- a folder that holds only folders (hai-draw's `gallery/`) gets one tab per inner folder that holds a file, named
  `gallery/〈kind〉/`, in name order
check: every folder of the skill that holds a file has a tab

### 〈file〉
what: Any other file beside `SKILL.md` (`CHANGELOG.md`, `PREFERENCES.md`, `README.md`), shown as itself.
why: What sits beside `SKILL.md` is part of the skill too, and is found under its own name.
from: the files directly in `〈skill〉/`, without `SKILL.md` and `CONSTITUTION.md`, read live
must:
- one left tab per loose file, named by the file, after the folders, in name order
- never gathered under an invented word such as other
check: every loose file of the skill has a tab of its own name

## Draw
what: The topic's own drawing: how these skills work together, or the logic of the one skill.
when: the topic has its own drawing
why: A reader sees how the skills fit before reading any of their files.
from: the topic's `sNN-〈topic〉.excalidraw`
must:
- the last top button, only for a topic that has its own drawing
- one drawing, shown full width; a pattern (a flow, a loop, a tree), never the skills listed as text
- a topic without a drawing has no such button, never an empty one
check: a topic that has `sNN-〈topic〉.excalidraw` shows the Draw button, and it opens that file
