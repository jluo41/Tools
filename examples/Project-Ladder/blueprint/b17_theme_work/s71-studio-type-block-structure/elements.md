# Requirements of a Block Structure topic

The class of every Block Structure topic (s0N): the same top buttons and left tabs as an instance, each with the
requirement an instance must meet there. `## ` is a top button, `### ` a left tab under it. The type's own right side
shows the requirement (type_requirements.py builds the pages); an instance's right side shows the real thing; a
right-click on the button or tab, in the type or an instance, shows its What, Why and From.

instances: article[id^="s0"]

## Structure
what: The Block type's three models as rules: Folder, Job-Task and Studio.
why: The rule comes first; a reader learns the shape of a Block before looking at a real one.
from: the Block type's rule
check: `check_organization.py`: its tabs are Folder, Job-Task, Studio, each opening a file that exists

### Folder
what: The folders and files a Block of this type holds.
why: A writer knows where each thing goes before making it, and a reader knows where to look.
from: the naming patterns of the Block type's folders
must:
- naming patterns with 〈placeholders〉 (`bNN_〈block〉/`, `jNN_〈job〉/`), never a real folder's name
- every line's purpose on its hover
- one tree, opened to the Job, folders before files
check: by eye: the rule tree names no real path
> bNN_〈block〉/
>   board.md
>   jNN_〈job〉/
>     jNN_〈job〉.md
>     tNN_〈task〉/
>       tNN_〈task〉.md
>       runs/
>   sNN-〈topic〉/
>   trace/
>   related/
>   delivery/

### Job-Task
what: How a Block of this type divides its work: Job group, Job, Task group, Task.
why: Two Blocks of one type then divide their work the same way, so a reader finds a Task where it is expected.
from: the type's levels and their allowed types
must:
- at most four levels: Job group → Job → Task group → Task
- only the levels the type needs; a level it never uses is left out, not shown empty
- "optional" only where real Blocks of the type differ
- drawn as a folder tree like Folder, each level its own colour, the same colour in every Block type
- the four lists pinned in the topic's `types.md`: 〈Job group type 1〉, 〈2〉 …; 〈Job type 1〉, 〈2〉 …; 〈Task group type 1〉, 〈2〉 …; 〈Task type 1〉, 〈2〉 …
- each type with its name, what it is for, and what a Job or Task of that type must hold
- a type is fixed for the Block type; a group is named by each Block or Job on its `bands:` line, and is one of the group types
- a Task's Runs on its hover only when a Run means something structural
check: `block_types_check.py`: every Job type and Task type of the example Block is one `types.md` lists; by eye: the levels match the type
> bNN_〈block〉/
>   〈Job group〉  # 〈Job group type〉
>     jNN_〈job〉/  # 〈Job type〉
>       〈Task group〉  # 〈Task group type〉
>         tNN_〈task〉/  # 〈Task type〉

### Studio
what: The Studio bands a Block of this type keeps its topics in.
why: A topic's number and title then say what kind of topic it is.
from: `delivery/page-spec/studio-bands.json` and the Block type's Studio definitions
must:
- a collapsible Folder Tree: Block, then Band, then Studio topic; no Mind Map
- one line per band, with its emoji, name and numbers
- Blueprint bands read from the shared registry; a band is independent of a Studio type
- Blueprint type definitions reuse shared types by reference and add only theme-specific types
- ordinary Work Blocks show actual Studio topics without requiring type-definition topics
check: by eye: Blueprint band names and order match the shared registry; empty bands are omitted from the live Studio
> bNN_〈block〉/
>   〈emoji〉 〈band name〉  # sNN
>     sNN-〈topic〉/
>       sNN-〈topic〉.md
>       〈drawing〉.excalidraw

## Job types
what: The Job group types and the Job types of this Block type, one left tab each.
why: A reader knows which kinds of Job a Block of this type may hold before opening one.
from: the topic's `types.md`
check: `block_types_check.py`: `types.md` has the Job group type and Job type lists

### 〈Job group type 1〉
what: One Job group type of this Block type, the first of its list.
why: A group gathers the Jobs of one stretch of the work; its type says what kind of stretch it is.
from: the topic's `types.md`, `## Job group type`
must:
- its name
- what it is for, in one sentence
- what a Job group of this type must hold
- the groups of the example Block that are of this type
check: `block_types_check.py`: the type has `for:` and `holds:`
> sNN-〈topic〉/
>   types.md
>     ## Job group type
>       ### 〈Job group type 1〉
>         for: 〈what it is for, in one sentence〉
>         holds: 〈what a Job group of this type must hold〉

### 〈Job group type 2〉
what: One Job group type of this Block type, the next of its list.
why: A second group type shows where the first one ends.
from: the topic's `types.md`, `## Job group type`
must:
- its name
- what it is for, in one sentence
- what a Job group of this type must hold
- the real Jobs of this type in the example Block
check: `block_types_check.py`: the type has `for:` and `holds:`
> sNN-〈topic〉/
>   types.md
>     ## Job group type
>       ### 〈Job group type 2〉
>         for: 〈what it is for, in one sentence〉
>         holds: 〈what a Job group of this type must hold〉

### 〈Job type 1〉
what: One Job type of this Block type, the first of its list.
why: A Job's type says what kind of work it does, so Jobs of one type are read and checked the same way.
from: the topic's `types.md`, `## Job type`
must:
- its name, as a Job names it on its face (`job-type:`)
- what it is for, in one sentence
- what a Job of this type must hold
- the real Jobs of this type in the example Block
check: `block_types_check.py`: the type has `for:` and `holds:`
> sNN-〈topic〉/
>   types.md
>     ## Job type
>       ### 〈Job type 1〉
>         for: 〈what it is for, in one sentence〉
>         holds: 〈what a Job of this type must hold〉

### 〈Job type 2〉
what: One Job type of this Block type, the next of its list.
why: A second type shows what tells the types apart.
from: the topic's `types.md`, `## Job type`
must:
- its name, as a Job names it on its face (`job-type:`)
- what it is for, in one sentence
- what a Job of this type must hold
- the real Jobs of this type in the example Block
check: `block_types_check.py`: the type has `for:` and `holds:`
> sNN-〈topic〉/
>   types.md
>     ## Job type
>       ### 〈Job type 2〉
>         for: 〈what it is for, in one sentence〉
>         holds: 〈what a Job of this type must hold〉

## Task types
what: The Task group types and the Task types of this Block type, one left tab each.
why: A reader knows which kinds of Task a Job of this Block type may hold.
from: the topic's `types.md`
check: `block_types_check.py`: `types.md` has the Task group type and Task type lists

### 〈Task group type 1〉
what: One Task group type of this Block type, the first of its list.
why: A group gathers the Tasks of one step of the Job; its type says what kind of step it is.
from: the topic's `types.md`, `## Task group type`
must:
- its name
- what it is for, in one sentence
- what a Task group of this type must hold
- the real Tasks of this type in the example Block
check: `block_types_check.py`: the type has `for:` and `holds:`
> sNN-〈topic〉/
>   types.md
>     ## Task group type
>       ### 〈Task group type 1〉
>         for: 〈what it is for, in one sentence〉
>         holds: 〈what a Task group of this type must hold〉

### 〈Task group type 2〉
what: One Task group type of this Block type, the next of its list.
why: A second group type shows where the first one ends.
from: the topic's `types.md`, `## Task group type`
must:
- its name
- what it is for, in one sentence
- what a Task group of this type must hold
- the real Tasks of this type in the example Block
check: `block_types_check.py`: the type has `for:` and `holds:`
> sNN-〈topic〉/
>   types.md
>     ## Task group type
>       ### 〈Task group type 2〉
>         for: 〈what it is for, in one sentence〉
>         holds: 〈what a Task group of this type must hold〉

### 〈Task type 1〉
what: One Task type of this Block type, the first of its list.
why: A Task's type says which kind of hai-task it is, so its folder and Runs are known.
from: the topic's `types.md`, `## Task type`
must:
- its name, as a Task names it on its face (`task-type:`)
- what it is for, in one sentence
- what a Task of this type must hold
- the real Tasks of this type in the example Block
check: `block_types_check.py`: the type has `for:` and `holds:`
> sNN-〈topic〉/
>   types.md
>     ## Task type
>       ### 〈Task type 1〉
>         for: 〈what it is for, in one sentence〉
>         holds: 〈what a Task of this type must hold〉

### 〈Task type 2〉
what: One Task type of this Block type, the next of its list.
why: A second type shows what tells the types apart.
from: the topic's `types.md`, `## Task type`
must:
- its name, as a Task names it on its face (`task-type:`)
- what it is for, in one sentence
- what a Task of this type must hold
- the real Tasks of this type in the example Block
check: `block_types_check.py`: the type has `for:` and `holds:`
> sNN-〈topic〉/
>   types.md
>     ## Task type
>       ### 〈Task type 2〉
>         for: 〈what it is for, in one sentence〉
>         holds: 〈what a Task of this type must hold〉

## Draw
what: The topic's one Excalidraw drawing of the Block type's structure.
why: A picture shows how the Block, its Jobs and Tasks and its Studio hang together faster than a list.
from: the topic's own `.excalidraw` file
must:
- one drawing, full width, with no left tabs
- the folder, the Job-Task levels and the Studio bands of this Block type, drawn as a pattern, not listed as text
- the same names as Structure, nothing added or left out
check: `check_organization.py`: Draw is one item, the topic's own `.excalidraw` file, and it exists

## Skills
what: The skills that make and check a Block of this type, each read live.
why: The structure is only true while a skill keeps it; the reader goes from the rule to its owner.
from: the skill folders under `plugins/`
skills: plugins/haipipe-toolkit/skills/1_base/project/hai-block, plugins/haipipe-toolkit/skills/1_base/project/hai-job, plugins/haipipe-toolkit/skills/1_base/task/hai-task, plugins/haipipe-toolkit/skills/1_base/project/hai-studio
must:
- one left tab per skill, opening its own `SKILL.md`
- the skills that own the Block type, its Jobs and its Tasks; the type itself lists the owners of the Block, Job, Task and Studio levels (hai-block, hai-job, hai-task, hai-studio), an instance its own Block type's
check: `type_requirements.py --check`: every skill folder on the `skills:` line has a `SKILL.md`

## Jobs page
The rows a Block's Jobs page shows for these levels. They are not tabs of this topic: a right-click on a row of the
real page shows these words.

### Job type row
mark: job-types
from: `job-type:` on each Job face (code, check, doc)
what: Filters the Jobs by the kind of work a Job does.
why: A Block mixes Jobs that build, check and write; picking one kind shows only the Jobs you can act on the same way.

### Job group row
mark: job-topics
from: the Block's `board.md` `bands:` line (j0N, j1N)
what: Groups the Jobs by the decade of their number, each decade a named stretch of the work.
why: Fifteen Jobs in one row cannot be read; a named group says which stretch of the work a Job belongs to.

### Job row
mark: job-bar
from: the `jNN_*` folders of the picked group
what: The Jobs of the picked group, one button each; a click opens that Job in place.
why: A Job is worked on inside its Block, so its neighbours stay one click away.

### Main
mark: jsub-to=main
from: the picked Job's own face
what: The Job itself: its brief, its plan and results, its findings.
why: The Job's own page comes before its Tasks; a reader sees the goal first, then what was done.

### Task group row
mark: job-ttopics
from: the Job face's `bands:` line (t0N, t1N)
what: Groups the Job's Tasks by the decade of their number.
why: A Job with many Tasks reads as a few named steps, not a long list.

### Task row
mark: job-subs
from: the `tNN_*` folders of the picked Task group
what: The Tasks of the picked group, one button each, with the mark of where each stands.
why: A Task opens inside its Job, so the reader never loses the Job it serves.
